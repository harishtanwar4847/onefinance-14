// Copyright (c) 2022, Atrina and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vendor', {
	// refresh: function(frm) {

	// }
	before_workflow_action: (frm) => {
        if (frm.selected_workflow_action === "Reject Vendor") {
            
            var me = this;
            var d = new frappe.ui.Dialog({
                title: __('Reason for Vendor Rejection'),
                fields: [
                    {
                        "fieldname": "reason_for_vendor_rejection",
                        "fieldtype": "Text",
                        "reqd": 1,
                    }
                ],
                primary_action: function() {
                    var data = d.get_values();
                    let reason_for_vendor_rejection = 'Reason for Vendor Rejection: ' + data.reason_for_vendor_rejection;
					if (window.timeout){
						clearTimeout(window.timeout)
						delete window.timeout
					}
					window.timeout=setTimeout(function(){
						frm.set_value("reason_of_rejection", data.reason_for_vendor_rejection) 
						frm.refresh_field("reason_of_rejection")              
						frm.save()
					},1500)
                    frappe.call({
                        method: "frappe.desk.form.utils.add_comment",
                        args: {
                            reference_doctype: frm.doc.doctype,
                            reference_name: frm.doc.name,
                            content: __(reason_for_vendor_rejection),
                            comment_email: frappe.session.user,
                            comment_by: frappe.session.user_fullname
                        },
                        callback: function(r) {
                            frm.reload_doc();
                            d.hide();
                        }
                    });   
                                   
                }

            });
            d.show();         
        }
    }
});
