// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["My Sales Register"] = {
	filters: [
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			width: "80",
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "customer_group",
			label: __("Customer Group"),
			fieldtype: "Link",
			options: "Customer Group",
		},
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
		},
		{
			fieldname: "mode_of_payment",
			label: __("Mode of Payment"),
			fieldtype: "Link",
			options: "Mode of Payment",
		},
		{
			fieldname: "owner",
			label: __("Owner"),
			fieldtype: "Link",
			options: "User",
		},
		{
			fieldname: "cost_center",
			label: __("Cost Center"),
			fieldtype: "Link",
			options: "Cost Center",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			fieldname: "brand",
			label: __("Brand"),
			fieldtype: "Link",
			options: "Brand",
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			fieldname: "include_payments",
			label: __("Show Ledger View"),
			fieldtype: "Check",
			default: 0,
		},
		{
			fieldname: "custom_bill_location",
			label: __("Bill Location"),
			fieldtype: "Data",
			reqd: 0,
		},
		{
			fieldname: "custom_driver",
			label: __("Driver"),
			fieldtype: "Link",
			options: "Driver",
			reqd: 0,
		},
		{
			fieldname: "custom_sales_person",
			label: __("Sales Person"),
			fieldtype: "Link",
			options: "Sales Person",
			reqd: 0,
		},
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: [
				"",
				"Draft",
				"Return",
				"Credit Note Issued",
				"Submitted",
				"Paid",
				"Partly Paid",
				"Unpaid",
				"Unpaid and Discounted",
				"Partly Paid and Discounted",
				"Overdue and Discounted",
				"Overdue",
				"Cancelled",
				"Internal Transfer",
			].join("\n"),
			reqd: 0,
		},
	],
};

erpnext.utils.add_dimensions("My Sales Register", 7);