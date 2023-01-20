frappe.ui.form.on('Cost Center',{
    apply_amount_limit:function(frm){
        if(frm.doc.apply_amount_limit == 0){
            frm.set_value("amount",0.0);
        }
    }
});