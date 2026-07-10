 # setting value for sales person
import frappe


def before_save(doc, method=None):
            
    # setting value for sales person
    sales_team_row = doc.sales_team[0] if doc.sales_team else None
    if sales_team_row and sales_team_row.sales_person:
        doc.custom_sales_person = sales_team_row.sales_person