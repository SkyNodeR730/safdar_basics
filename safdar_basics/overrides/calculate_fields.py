import frappe


def before_save(doc, method=None):
    total_basic_amount = 0
    total_discount = 0
    total_sales_tax = 0

    for item in doc.get("items", []):
        item.sb_base_amount = (item.price_list_rate or 0) * (item.qty or 0)
        item.total_discount = (item.discount_amount or 0) * (item.qty or 0)
        item.sales_tax = (item.amount or 0) - (item.net_amount or 0)

        total_basic_amount += item.sb_base_amount
        total_discount += item.total_discount
        total_sales_tax += item.sales_tax

    doc.total_basic_amount = total_basic_amount
    doc.total_discount = total_discount
    doc.total_sales_tax = total_sales_tax

    # setting value for sales person
    if doc.sales_team[0].sales_person:
        doc.custom_sales_person = doc.sales_team[0].sales_person
