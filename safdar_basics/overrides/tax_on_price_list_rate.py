import json

import frappe


def _get_item_tax_rate(item, tax):
	"""Mirrors erpnext.controllers.taxes_and_totals.TaxesAndTotalsMixin._get_tax_rate:
	an item's own Item Tax Template can override a tax account's rate for that
	item specifically - respect it instead of always using the header tax.rate."""
	item_tax_map = json.loads(item.item_tax_rate) if item.item_tax_rate else {}
	if tax.account_head in item_tax_map:
		return frappe.utils.flt(item_tax_map.get(tax.account_head))
	return tax.rate


def _price_list_tax_bases(doc):
	"""For each item, back-calculate the price_list_rate-based amount that
	'On Net Total' tax is actually charged on, mirroring core's
	determine_exclusive_rate (divide, not subtract, out the inclusive rows'
	combined fraction) but off price_list_rate * qty instead of item.amount.

	Exclusive rows contribute 0 to the fraction (same as core's
	get_current_tax_fraction), so with no inclusive rows this is just the
	plain price_list_rate * qty (unreduced by any discount).

	Returns (net_total_taxes, inclusive_taxes, tax_basis, base_tax_basis,
	embedded_tax, base_embedded_tax) all keyed by item.name, where
	embedded_tax is the absolute rupee amount of inclusive tax baked into
	that item's price_list_rate.
	"""
	net_total_taxes = [tax for tax in doc.taxes if tax.charge_type == "On Net Total"]
	inclusive_taxes = [tax for tax in net_total_taxes if frappe.utils.cint(tax.included_in_print_rate)]

	tax_basis, base_tax_basis = {}, {}
	embedded_tax, base_embedded_tax = {}, {}

	for item in doc.items:
		cumulated_fraction = sum(_get_item_tax_rate(item, tax) / 100 for tax in inclusive_taxes)
		gross = frappe.utils.flt((item.price_list_rate or 0) * (item.qty or 0))
		base_gross = frappe.utils.flt((item.base_price_list_rate or 0) * (item.qty or 0))
		basis = gross / (1 + cumulated_fraction) if cumulated_fraction else gross
		base_basis = base_gross / (1 + cumulated_fraction) if cumulated_fraction else base_gross

		tax_basis[item.name] = basis
		base_tax_basis[item.name] = base_basis
		embedded_tax[item.name] = gross - basis
		base_embedded_tax[item.name] = base_gross - base_basis

	return net_total_taxes, inclusive_taxes, tax_basis, base_tax_basis, embedded_tax, base_embedded_tax


def validate(doc, method=None):
	"""When enabled in My Settings, charge 'On Net Total' taxes on each item's
	price_list_rate (the pre-discount list price), regardless of any
	line-item discount applied. Otherwise, leave taxes untouched.

	'Is this Tax included in Basic Rate?' (included_in_print_rate) still works,
	re-based on price_list_rate instead of the discounted rate:
	- unchecked (exclusive): tax adds on top of net_total into grand_total,
	  computed on the full price_list_rate (or, if another tax on the same
	  item is inclusive, on price_list_rate net of that embedded tax - same
	  dilution quirk core has when mixing inclusive/exclusive rows on one item).
	- checked (inclusive): the tax is already embedded in price_list_rate, so
	  its absolute rupee amount is carved out of the item's actual (discounted)
	  revenue instead of being added on top - grand_total ends up unaffected by
	  that row. Revenue itself is still based on the item's real selling rate,
	  not price_list_rate, so discounts keep working as before.
	"""
	if not frappe.get_cached_doc("My Settings").tax_on_price_list_rate:
		return

	if not doc.items:
		return

	net_total_taxes, inclusive_taxes, tax_basis, base_tax_basis, embedded_tax, base_embedded_tax = (
		_price_list_tax_bases(doc)
	)

	if not net_total_taxes:
		return

	for item in doc.items:
		# Revenue is the actual invoiced (discounted) amount, reduced only by
		# whatever tax is embedded in it (inclusive rows). Exclusive tax never
		# touches revenue - it's added on top separately below.
		revenue = frappe.utils.flt(item.rate * item.qty) - embedded_tax[item.name]
		base_revenue = frappe.utils.flt(item.base_rate * item.qty) - base_embedded_tax[item.name]

		item.net_amount = frappe.utils.flt(revenue, item.precision("net_amount"))
		item.base_net_amount = frappe.utils.flt(base_revenue, item.precision("base_net_amount"))
		item.net_rate = (
			frappe.utils.flt(item.net_amount / item.qty, item.precision("net_rate")) if item.qty else 0
		)
		item.base_net_rate = (
			frappe.utils.flt(item.base_net_amount / item.qty, item.precision("base_net_rate")) if item.qty else 0
		)

	for tax in net_total_taxes:
		tax_amount = 0.0
		base_tax_amount = 0.0
		item_wise_tax_detail = {}

		for item in doc.items:
			effective_rate = _get_item_tax_rate(item, tax)
			item_tax_amount = frappe.utils.flt(tax_basis[item.name] * effective_rate / 100)
			base_item_tax_amount = frappe.utils.flt(base_tax_basis[item.name] * effective_rate / 100)

			tax_amount += item_tax_amount
			base_tax_amount += base_item_tax_amount

			key = item.item_code or item.item_name
			item_wise_tax_detail[key] = [effective_rate, item_tax_amount]

		tax.tax_amount = frappe.utils.flt(tax_amount, tax.precision("tax_amount"))
		tax.base_tax_amount = frappe.utils.flt(base_tax_amount, tax.precision("base_tax_amount"))

		# tax_amount_after_discount_amount is what GL posting (make_tax_gl_entries)
		# and the Tax Breakup table actually read - keep it in sync or the ledger
		# and breakup silently fall back to the stale net_total-based amount.
		tax.tax_amount_after_discount_amount = tax.tax_amount
		tax.base_tax_amount_after_discount_amount = tax.base_tax_amount

		# Rebuild the item-wise tax breakup against price_list_rate so the Tax
		# Breakup table matches the overridden tax_amount instead of the
		# original net_amount-based split.
		tax.item_wise_tax_detail = json.dumps(item_wise_tax_detail, separators=(",", ":"))

	doc.net_total = frappe.utils.flt(
		sum(item.net_amount for item in doc.items), doc.precision("net_total")
	)
	doc.base_net_total = frappe.utils.flt(
		sum(item.base_net_amount for item in doc.items), doc.precision("base_net_total")
	)

	# Standard Frappe semantics: each tax row's total/base_total is the
	# running cumulative sum from net_total down through that row.
	running_total = doc.net_total
	running_base_total = doc.base_net_total

	for tax in doc.taxes:
		running_total += tax.tax_amount
		running_base_total += tax.base_tax_amount
		tax.total = frappe.utils.flt(running_total, tax.precision("total"))
		tax.base_total = frappe.utils.flt(running_base_total, tax.precision("base_total"))

	doc.total_taxes_and_charges = frappe.utils.flt(
		sum(tax.tax_amount for tax in doc.taxes), doc.precision("total_taxes_and_charges")
	)
	doc.base_total_taxes_and_charges = frappe.utils.flt(
		sum(tax.base_tax_amount for tax in doc.taxes), doc.precision("base_total_taxes_and_charges")
	)

	doc.grand_total = frappe.utils.flt(doc.net_total + doc.total_taxes_and_charges, doc.precision("grand_total"))
	doc.base_grand_total = frappe.utils.flt(
		doc.base_net_total + doc.base_total_taxes_and_charges, doc.precision("base_grand_total")
	)

	# Mirror core's set_rounded_total exactly (round_based_on_smallest_currency_fraction,
	# not plain decimal rounding - e.g. PKR has no paisa in circulation, so it
	# rounds to the nearest whole rupee) - a plain frappe.utils.rounded() call
	# here would silently disagree with what core produces when this setting
	# is off, and ignoring is_rounded_total_disabled() would round totals for
	# companies that have that turned off.
	if doc.meta.get_field("rounded_total") and doc.is_rounded_total_disabled():
		doc.rounded_total = doc.base_rounded_total = 0
		doc.rounding_adjustment = doc.base_rounding_adjustment = 0
	else:
		doc.rounded_total = frappe.utils.round_based_on_smallest_currency_fraction(
			doc.grand_total, doc.currency, doc.precision("rounded_total")
		)
		doc.rounding_adjustment = frappe.utils.flt(
			doc.rounded_total - doc.grand_total, doc.precision("rounding_adjustment")
		)
		doc.base_rounding_adjustment = frappe.utils.flt(
			doc.rounding_adjustment * doc.conversion_rate, doc.precision("base_rounding_adjustment")
		)
		doc.base_rounded_total = frappe.utils.flt(
			doc.rounded_total * doc.conversion_rate, doc.precision("base_rounded_total")
		)

	doc.in_words = frappe.utils.money_in_words(doc.rounded_total or doc.grand_total, doc.currency)
	doc.base_in_words = frappe.utils.money_in_words(
		doc.base_rounded_total or doc.base_grand_total,
		frappe.get_cached_value("Company", doc.company, "default_currency"),
	)

	# The "Tax Breakup" section on the form is a stored HTML snapshot
	# (other_charges_calculation) rendered by the standard
	# calculate_taxes_and_totals() *before* this hook runs, so it's still
	# showing the old net_total-based split. Regenerate it now that
	# item_wise_tax_detail reflects price_list_rate.
	if doc.meta.get_field("other_charges_calculation"):
		from erpnext.controllers.taxes_and_totals import get_itemised_tax_breakup_html

		doc.other_charges_calculation = get_itemised_tax_breakup_html(doc)


def get_itemised_tax_breakup_data(doc):
	"""Regional override (see hooks.py regional_overrides) of ERPNext's
	get_itemised_tax_breakup_data. Reuses the item_wise_tax_detail already
	rebuilt by validate() above, but also swaps the "Taxable Amount" column
	from item.net_amount to the price_list_rate based tax basis so it lines up
	with the tax actually charged."""
	from erpnext.controllers.taxes_and_totals import get_itemised_tax, get_itemised_taxable_amount

	itemised_tax = get_itemised_tax(doc.taxes)

	if doc.doctype == "Sales Invoice" and frappe.get_cached_doc("My Settings").tax_on_price_list_rate:
		_, _, tax_basis, _, _, _ = _price_list_tax_bases(doc)
		itemised_taxable_amount = frappe._dict()
		for item in doc.items:
			key = item.item_code or item.item_name
			itemised_taxable_amount.setdefault(key, 0)
			itemised_taxable_amount[key] += tax_basis.get(item.name, 0)
	else:
		itemised_taxable_amount = get_itemised_taxable_amount(doc.items)

	itemised_tax_data = []
	for item_code, taxes in itemised_tax.items():
		itemised_tax_data.append(
			frappe._dict({"item": item_code, "taxable_amount": itemised_taxable_amount.get(item_code, 0), **taxes})
		)

	return itemised_tax_data
