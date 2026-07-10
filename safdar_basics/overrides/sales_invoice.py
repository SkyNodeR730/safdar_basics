# In your app, e.g. safdar_basics/safdar_basics/overrides/sales_invoice.py

import frappe

def set_sales_invoice_ref_on_sales_order(doc, method=None):
    """On submit: save this Sales Invoice's name on the linked Sales Order(s)."""
    _update_sales_order_ref(doc, doc.name)

def clear_sales_invoice_ref_on_sales_order(doc, method=None):
    """On cancel: clear the field on the linked Sales Order(s)."""
    _update_sales_order_ref(doc, None)

def _update_sales_order_ref(doc, value):
    if not doc.items:
        return

    sales_orders = set()
    for item in doc.items:
        if item.sales_order:
            sales_orders.add(item.sales_order)

    if not sales_orders:
        return  # invoice not linked to any Sales Order — nothing to do

    for so_name in sales_orders:
        if not frappe.db.exists('Sales Order', so_name):
            continue  # safety net

        frappe.db.set_value(
            'Sales Order',
            so_name,
            'sales_invoice',
            value
        )