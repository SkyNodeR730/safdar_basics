frappe.ui.form.on('Payment Entry', {
    onload: function(frm) {
        set_sales_person_from_customer(frm);
    },
    refresh: function(frm) {
        set_sales_person_from_customer(frm);
    },
    party_type: function(frm) {
        if (frm.doc.party_type !== 'Customer') {
            frm.set_value('custom_sales_person', '');
        }
    },
    party: function(frm) {
        set_sales_person_from_customer(frm);
    }
});

function set_sales_person_from_customer(frm) {
    if (frm.doc.party_type !== 'Customer' || !frm.doc.party) {
        return; // nothing to do, no error
    }

    frappe.db.get_doc('Customer', frm.doc.party)
        .then(customer_doc => {
            if (!customer_doc || !customer_doc.sales_team || customer_doc.sales_team.length === 0) {
                return; // no sales team — leave field untouched, no error
            }

            let sales_person = customer_doc.sales_team[0].sales_person;

            if (!sales_person) {
                return; // sales team row has no sales_person — leave field untouched, no error
            }

            frm.set_value('custom_sales_person', sales_person);
        })
        .catch(() => {
            // any fetch error — silently ignore, no popup/console error
        });
}