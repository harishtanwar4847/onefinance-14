frappe.ui.form.on('Bank Account', {
    validate: function(frm){
        if (frm.doc.transaction_type==''){
            frappe.throw("Please select transaction type")
        }
        if (frm.doc.beneficiary_code!==undefined && frm.doc.beneficiary_code.length >13 ){
        frappe.throw("Length of beneficiary code cannot be greater than 13")
        }
        if (frm.doc.bank_account_no!==undefined && frm.doc.bank_account_no.length>25){
            frappe.throw("Length of bank account number cannot be greater than 25")
        }
        if (frm.doc.account_name!==undefined && frm.doc.account_name.length>200){
            frappe.throw("Length of account name cannot be greater than 200")
        }
        if (frm.doc.branch_code!==undefined && frm.doc.branch_code.length>15){
            frappe.throw("Length of branch code cannot be greater than 15")
        }
        if (frm.doc.bank!==undefined && frm.doc.bank.length>100){
            frappe.throw("Length of bank name cannot be greater than 100")
        }
        if (frm.doc.branch_name.includes(",")){
            frappe.throw("Please remove comma(,) from Branch Name")
        }
        if (frm.doc.branch_name!==undefined && frm.doc.branch_name.length>40){
            frappe.throw("Length of branch name cannot be greater than 40")
        }
          
    }
});