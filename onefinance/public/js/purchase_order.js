frappe.ui.form.on('Purchase Order', {
    refresh: function (frm) {
        $('.modal-actions').hide();
        $(".actions").hide();
        if (frm.doc.workflow_state != "On Hold By Management" && frm.doc.workflow_state != "On Hold By Department Head" && frm.doc.on_hold && frm.doc.release_date && frm.doc.hold_comment) {
            if (window.timeout){
                clearTimeout(window.timeout)
                delete window.timeout
            }
            window.timeout = setTimeout(function () {
                frm.set_value("on_hold", 0)
                frm.set_value("release_date",)
                frm.set_value("hold_comment", "")
                frm.refresh_field("on_hold")
                frm.refresh_field("release_date")
                frm.refresh_field("hold_comment")
                frm.save()
            }, 2500)
        }
        if (frm.doc.workflow_state == "Approved" || frm.doc.workflow_state == "Approved By Management") {
            frm.fields.forEach(function (l) { frm.set_df_property(l.df.fieldname, "read_only", 1); })
        }
        if ((frm.doc.workflow_state == "Approval Pending" || frm.doc.workflow_state == "On Hold By Department Head") && frappe.session.user != frm.doc.cost_center_department_head) {
            $(".user-action").hide();
        }
        if ((frm.doc.workflow_state == "Management Approval Pending" || frm.doc.workflow_state == "On Hold By Management") && frappe.session.user != frm.doc.cost_center_manager) {
            $(".user-action").hide();
        }
    },

    cost_center: function (frm) {
        $.each(frm.doc.items || [], function (i, v) {
            frappe.model.set_value(v.doctype, v.name, "cost_center", frm.doc.cost_center)
        })
    },

    before_workflow_action: (frm) => {
        if (frm.selected_workflow_action === "Hold") {

            var me = this;
            var d = new frappe.ui.Dialog({
                title: __('Reason for Hold'),
                fields: [
                    {
                        "fieldname": "reason_for_hold",
                        "fieldtype": "Text",
                        "reqd": 1,
                    },
                    {
                        "label": "On Hold Till",
                        "fieldname": "on_hold_till",
                        "fieldtype": "Date",
                        "reqd": 1,
                    }
                ],
                primary_action: function () {
                    var data = d.get_values();
                    let reason_for_hold = 'Reason for Hold: ' + data.reason_for_hold;
                    if (window.timeout) {
                        clearTimeout(window.timeout)
                        delete window.timeout
                    }
                    window.timeout = setTimeout(function () {
                        frm.set_value("on_hold", 1)
                        frm.set_value("release_date", data.on_hold_till)
                        frm.set_value("hold_comment", data.reason_for_hold)
                        frm.refresh_field("on_hold")
                        frm.refresh_field("release_date")
                        frm.refresh_field("hold_comment") 
                        frm.save()
                    }, 2500)
                    frappe.call({
                        method: "frappe.desk.form.utils.add_comment",
                        args: {
                            reference_doctype: frm.doc.doctype,
                            reference_name: frm.doc.name,
                            content: __(reason_for_hold),
                            comment_email: frappe.session.user,
                            comment_by: frappe.session.user_fullname
                        },
                        callback: function (r) {
                            frm.reload_doc();
                            d.hide();
                        }
                    });
                }
            });
            d.show();
        }

        if (frm.selected_workflow_action === "Reject") {

            var me = this;
            var d = new frappe.ui.Dialog({
                title: __('Reason for Reject'),
                fields: [
                    {
                        "fieldname": "reason_for_reject",
                        "fieldtype": "Text",
                        "reqd": 1,
                    }
                ],
                primary_action: function () {
                    var data = d.get_values();
                    let reason_for_reject = 'Reason for Reject: ' + data.reason_for_reject;
                    if (window.timeout) {
                        clearTimeout(window.timeout)
                        delete window.timeout
                    }
                    window.timeout = setTimeout(function () {
                        frm.set_value("reason_of_rejection", data.reason_for_reject)
                        frm.refresh_field("reason_of_rejection")
                        frm.save()
                    }, 2500)

                    frappe.call({
                        method: "frappe.desk.form.utils.add_comment",
                        args: {
                            reference_doctype: frm.doc.doctype,
                            reference_name: frm.doc.name,
                            content: __(reason_for_reject),
                            comment_email: frappe.session.user,
                            comment_by: frappe.session.user_fullname
                        },
                        callback: function (r) {
                            frm.reload_doc();
                            d.hide();
                        }
                    });
                }
            });
            d.show();
        }

    },

    after_workflow_action: (frm) => {
        frappe.call({
            method: "onefinance.utils.workflow_changed_comment",
            args: {
                doc_name: frm.doc.name,
                doctype_name : 'Purchase Order'
            },
            callback: function (r) {
                frm.reload_doc();
            }
        });
    },

    //Fetch Total from  Purchase Order For Purchase Invoice.
    onload: (frm) => {
        if (frm.doc.purchase_order) {
            frappe.db.get_doc("Purchase Order", frm.doc.purchase_order).then(doc => {
                frm.set_value('purchase_order_amount', doc.total)
            })
        }
    },

    //EXP
    // workflow_state : (frm) => {
    //     frappe.call({
    //         method: "onefinance.__init__.apply_action_custom",
    //         args: {
    //             doc_name: frm.doc.name,
    //             doctype_name : 'Purchase Order',
    //             action : action,
    //             // current_state, user : None,
    //             // last_modified : None
    //         },
    //         callback: function (r) {
    //             frappe.msgprint('Function Triggered')
    //             frm.reload_doc();
    //         }
    //     });
    // }
    //EXP
});







// //     after_save:(frm) => {
// //         if(frm.doc.is_approval_required != 1){

// //             // Not Working We cannot change workflow state directly as it is not allowed due to security issues.
            
// //             // frm.doc.workflow_state == "Created"
// //             // frm.set_value("workflow_state", "Draft")
// //             // frm.save()
// //             frappe.call({
// //                 method: "onefinance.utils.set_workflow_state_to_draft",
// //                 args: {
// //                     reference_doctype: frm.doc.doctype, //get doctype name
// //                     reference_name: frm.doc.name //get document name
// //                 },
// //                 freeze : true,
// //                 callback: function(r) {
// //                     frm.refresh_field('workflow_state');
// //                     frm.refresh()
// //                     frm.reload_doc();
// //                     // frappe.msgprint(r.message)
// //                     // frm.reload_doc(reference_name);

// //                 }
// //             }); 
// //         }

// //     }
// })