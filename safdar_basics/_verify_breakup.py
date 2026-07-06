import frappe

def run():
    print("regional_overrides:", frappe.get_hooks("regional_overrides", {}).get("Pakistan"))

    doc = frappe.get_doc("Sales Invoice", "ACC-SINV-2026-00003")
    doc.save()
    print("other_charges_calculation snippet:")
    print(doc.other_charges_calculation)
    frappe.db.commit()
