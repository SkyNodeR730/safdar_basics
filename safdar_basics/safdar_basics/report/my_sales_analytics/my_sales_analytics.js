// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.query_reports["My Sales Analytics"] = {
	filters: [
		{
			fieldname: "tree_type",
			label: __("Tree Type"),
			fieldtype: "Select",
			options: [
				"Customer Group",
				"Customer",
				"Item Group",
				"Item",
				"Territory",
				"Order Type",
				"Project",
			],
			default: "Customer",
			reqd: 1,
		},
		{
			fieldname: "doc_type",
			label: __("based_on"),
			fieldtype: "Select",
			options: ["Sales Order", "Delivery Note", "Sales Invoice"],
			default: "Sales Invoice",
			reqd: 1,
		},
		{
			fieldname: "value_quantity",
			label: __("Value Or Qty"),
			fieldtype: "Select",
			options: [
				{ value: "Value", label: __("Value") },
				{ value: "Quantity", label: __("Quantity") },
			],
			default: "Value",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[1],
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: erpnext.utils.get_fiscal_year(frappe.datetime.get_today(), true)[2],
			reqd: 1,
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
		},
		{
			fieldname: "sales_person",
			label: __("Sales Person"),
			fieldtype: "Link",
			options: "Sales Person",
		},
		{
			fieldname: "market_segment",
			label: __("Market Segment"),
			fieldtype: "Link",
			options: "Market Segment",
		},
		{
			fieldname: "industry",
			label: __("Industry"),
			fieldtype: "Link",
			options: "Industry Type",
		},
		{
			fieldname: "range",
			label: __("Range"),
			fieldtype: "Select",
			options: [
				{ value: "Weekly", label: __("Weekly") },
				{ value: "Monthly", label: __("Monthly") },
				{ value: "Quarterly", label: __("Quarterly") },
				{ value: "Yearly", label: __("Yearly") },
			],
			default: "Monthly",
			reqd: 1,
		},
		{
			fieldname: "show_aggregate_value_from_subsidiary_companies",
			label: __("Show Aggregate Value from Subsidiary Companies"),
			fieldtype: "Check",
		},
	],
};
