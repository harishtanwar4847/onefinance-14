import frappe

def on_update_purchase_invoice(doc, method):
    p_list = []
    item_list = []
    po_list = []
    for i in doc.items:
        p_list.append(i.purchase_order)
        item_list.append(i.item_code)
    po_list = list(zip(p_list, item_list))
    print(po_list)
    res = []
    [res.append(x) for x in po_list if x[0] != None]
    print(res)
    res = list(set(res))
    print(res)
    if res:
        doc.set("pre_approved_items", [])
        for i in res:
            poi_list = frappe.db.get_all('Purchase Order Item', fields=['item_code', 'description', 'item_name', 'qty', 'rate', 'base_rate', 'uom', 'conversion_factor', 'stock_qty', 'amount', 'base_amount', 'parent'], filters={'parent': ["=", i[0]], 'item_code': ["=", i[1]]})
            print(poi_list)
            for i in poi_list:
                doc.append('pre_approved_items', {
                    'item_code': i['item_code'],
                    'description': i['description'],
                    'item_name': i['item_name'],
                    'qty': i['qty'],
                    'rate': i['rate'],
                    'base_rate': i['base_rate'],
                    'uom': i['uom'],
                    'conversion_factor': i['conversion_factor'],
                    'stock_qty': i['stock_qty'],
                    'amount': i['amount'],
                    'base_amount': i['base_amount'],
                    'purchase_order': i['parent']
                })
    else:
        doc.set("pre_approved_items", [])

    old_doc = doc.get_doc_before_save()
    if doc.workflow_state == "Approval Pending" and old_doc.workflow_state == "Verification Pending":
        doc.checker = frappe.session.user
    if doc.workflow_state == "Approved":
        doc.approver_1 = frappe.get_doc("User",doc.cost_center_department_head).full_name
        doc.approver_2 = frappe.get_doc("User",doc.cost_center_department_head).full_name
    if doc.workflow_state == "Management Approval Pending":
        doc.approver_1 = frappe.get_doc("User",doc.cost_center_department_head).full_name
    if doc.workflow_state == "Approved By Management":
        doc.approver_2 = frappe.get_doc("User",doc.cost_center_manager).full_name

# On Update Purchase Order # Setting checker field with current session user
def on_update_purchase_order(doc, method):
    old_doc = doc.get_doc_before_save()
    if doc.workflow_state == "Approval Pending" and old_doc.workflow_state == "Verification Pending":
        doc.checker = frappe.session.user
    if doc.workflow_state == "Approved":
        doc.approver_1 = frappe.get_doc("User",doc.cost_center_department_head).full_name
        doc.approver_2 = frappe.get_doc("User",doc.cost_center_department_head).full_name
    if doc.workflow_state == "Management Approval Pending":
        doc.approver_1 = frappe.get_doc("User",doc.cost_center_department_head).full_name
    if doc.workflow_state == "Approved By Management":
        doc.approver_2 = frappe.get_doc("User",doc.cost_center_manager).full_name

def before_save(doc,method):
    if doc.references:
        for item in doc.references:  
            if item.reference_doctype=="Purchase Invoice":
                item.approver = frappe.get_doc("Purchase Invoice", item.reference_name).approver_2
                print(item.approver,"item.approver")
                description = frappe.db.sql("""select description from `tabPurchase Invoice Item` pi where pi.parent=%s""",item.reference_name)
                print(description[0][0],"description")
                item.description=description[0][0]
        
            if item.reference_doctype=="Purchase Order":
                item.approver = frappe.get_doc("Purchase Order", item.reference_name).approver_2
                print(item.approver,"item.approver")
                description = frappe.db.sql("""select description from `tabPurchase Order Item` pi where pi.parent=%s""",item.reference_name)
                print(description[0][0],"description")
                item.description=description[0][0]

            if item.reference_doctype=="Journal Entry":
                item.approver = frappe.get_doc("Journal Entry", item.reference_name).approver
                item.description = frappe.get_doc("Journal Entry", item.reference_name).remark
                print(item.approver,"item.approver")

def on_submit_payment(doc, method):
    supplier_list = [x[0] for x in frappe.db.sql("""select c.email_id from `tabContact Email` c join `tabDynamic Link` d where c.parent = d.parent and d.link_name = %s""", doc.party)]
    if supplier_list:
        for i in range(len(supplier_list)):
            msg = """Hello,<br><br>
            We have processed your payment kindly check and acknowledge the same.<br>
            <table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
                        <tr><th>Party Name</th><th>Invoice No.</th><th>Invoice Date</th><th>Invoice Value</th><th>TDS Deducted</th><th>Payment Amount</th><th>Payment Date</th><th>Bank Reference No.</th></tr>
                        """
            if doc.references:
                for item in doc.references:
                    if item.reference_doctype == "Purchase Invoice":
                        invoice_date = frappe.get_doc("Purchase Invoice", item.reference_name).bill_date
                        tds_deducted = frappe.get_doc("Purchase Invoice", item.reference_name).taxes_and_charges_deducted
                        invoice_value = frappe.get_doc("Purchase Invoice", item.reference_name).total + frappe.get_doc("Purchase Invoice", item.reference_name).taxes_and_charges_added
                        msg += "<tr><td>"+doc.party+ "</td><td>"+str(item.bill_no if item.bill_no else "--") + "</td><td>" + str(invoice_date if invoice_date else "--") + "</td><td>" + str(invoice_value) + "</td><td>" + str(tds_deducted) + "</td><td>" + str(item.allocated_amount) + "</td><td>" + str(doc.reference_date) + "</td><td>" + str(doc.reference_no) + "</td><tr>"
                    if item.reference_doctype == "Purchase Order":
                        tds_deducted = frappe.get_doc("Purchase Order", item.reference_name).taxes_and_charges_deducted
                        invoice_value = frappe.get_doc("Purchase Order", item.reference_name).total + frappe.get_doc("Purchase Order", item.reference_name).taxes_and_charges_added
                        msg += "<tr><td>"+doc.party+ "</td><td>"+"--"+ "</td><td>" +  "--" + "</td><td>" + str(invoice_value) + "</td><td>" + str(tds_deducted) + "</td><td>" + str(item.allocated_amount) + "</td><td>" + str(doc.reference_date) + "</td><td>" + str(doc.reference_no) + "</td><tr>"
                    if item.reference_doctype == "Journal Entry":
                        msg += "<tr><td>"+doc.party+ "</td><td>"+"--"+ "</td><td>" +  "--" + "</td><td>" + "--" + "</td><td>" + '--' + "</td><td>" + str(item.allocated_amount) + "</td><td>" + str(doc.reference_date) + "</td><td>" + str(doc.reference_no) + "</td><tr>"
                msg += "</table><br>"
                msg+= "In case of any queries, you can contact below.<br> Email: accounts@1finance.co.in <br>Phone: 022-69121147"
                frappe.sendmail(subject="1 Finance Payment Details", content=msg, recipients = '{}'.format(supplier_list[i]))
    
    frappe.db.set_value('Payment Entry', {'name': doc.name}, 'submitted_date', frappe.utils.today())
    approver_name = frappe.db.get_value('User', {'name':doc.approver_id}, 'full_name')
    frappe.db.set_value('Payment Entry', {'name': doc.name}, 'approver', approver_name)
    if doc.amended_from != None:
        amended_date = frappe.db.get_value('Payment Entry', {'name':doc.amended_from}, 'submitted_date')
        frappe.db.set_value('Payment Entry', {'name': doc.name}, 'amended_from_submitted_date', amended_date)
    else:
        frappe.db.set_value('Payment Entry', {'name': doc.name}, 'amended_from_submitted_date', frappe.utils.today())
    frappe.db.commit()
    doc.reload()  

def on_submit_journal(doc,method):
    frappe.db.set_value('Journal Entry', {'name': doc.name}, 'submitted_date', frappe.utils.today())
    approver_name = frappe.db.get_value('User', {'name':doc.approver_id}, 'full_name')
    frappe.db.set_value('Journal Entry', {'name': doc.name}, 'approver', approver_name)
    if doc.amended_from != None:
        amended_date = frappe.db.get_value('Journal Entry', {'name':doc.amended_from}, 'submitted_date')
        frappe.db.set_value('Journal Entry', {'name': doc.name}, 'amended_from_submitted_date', amended_date)
    else:
        frappe.db.set_value('Journal Entry', {'name': doc.name}, 'amended_from_submitted_date', frappe.utils.today())
    frappe.db.commit()
    doc.reload()  

def on_update_vendor(doc, method):
    if doc.workflow_state == "Vendor Created":
        supp = frappe.get_doc({"doctype": "Supplier", "supplier_name": doc.company_name, "supplier_group": "All Supplier Groups", "gst_category": doc.gst_status, "gstin": doc.gst_number, "pan": doc.pan_number, "msme_number": doc.vendor_status_on_msme_if_yes_mention_msme_no, "country": doc.country, "website": doc.website})
        supp.insert(ignore_permissions=True)

        add = frappe.new_doc("Address")
        add.address_title = doc.company_name + "-" + doc.address
        add.address_line1 = doc.address
        add.city = doc.city
        add.state = doc.state
        add.gst_state = doc.state
        add.country = doc.country
        add.pincode = doc.postal_code
        add.email_id = doc.email_address
        add.phone = doc.landline_number
        add.gst_category = doc.gst_status
        add.gstin = doc.gst_number
        add.append('links', {
            'link_doctype': 'Supplier',
            'link_name': doc.company_name
        })

        add.insert()

        cont = frappe.new_doc("Contact")
        cont.first_name = doc.contact_person_name
        cont.designation = doc.contact_person_designation
        cont.append('phone_nos', {
            'phone': doc.mobile_number
        })
        cont.append('links', {
            'link_doctype': 'Supplier',
            'link_name': doc.company_name
        })

        cont.insert()

        bank = frappe.new_doc("Bank Account")
        if doc.bank_name != "Other":
            bank.bank_account_no = doc.bank_account_number
            bank.branch_code = doc.ifsc_code
            bank.bank = doc.bank_name
            bank.account_name = doc.beneficiary_name
            bank.party_type = "Supplier"
            bank.party = doc.company_name
            bank.insert()
        if doc.bank_name == "Other":
            new_bank = frappe.new_doc("Bank")
            new_bank.bank_name = doc.enter_bank_name
            new_bank.insert()
            bank.bank_account_no = doc.bank_account_number
            bank.branch_code = doc.ifsc_code
            bank.bank = doc.enter_bank_name
            bank.account_name = doc.beneficiary_name
            bank.party_type = "Supplier"
            bank.party = doc.company_name
            bank.insert()


        file = frappe.new_doc("File")
        if doc.gst_registration_copy:
            file.file_name = doc.company_name + " - " + "Gst registration copy"
            file.file_url = doc.gst_registration_copy
            file.attached_to_doctype = "Supplier"
            file.attached_to_name = doc.company_name
            file.name = doc.company_name + " - " + "Gst registration copy"
            file.insert()
        if doc.pan_card_copy:
            file.file_name = doc.company_name + " - " + "PAN card copy"
            file.file_url = doc.pan_card_copy
            file.attached_to_doctype = "Supplier"
            file.attached_to_name = doc.company_name
            file.name = doc.company_name + " - " + "PAN card copy"
            file.insert()
        if doc.valid_msme_certificate_if_applicable:
            file.file_name = doc.company_name + " - " + "Valid msme certificate"
            file.file_url = doc.valid_msme_certificate_if_applicable
            file.attached_to_doctype = "Supplier"
            file.attached_to_name = doc.company_name
            file.name = doc.company_name + " - " + "Valid msme certificate"
            file.insert()
        if doc.cancelled_cheque_leafbank_letter_copy:
            file.file_name = doc.company_name + " - " + "Cancelled cheque copy"
            file.file_url = doc.cancelled_cheque_leafbank_letter_copy
            file.attached_to_doctype = "Supplier"
            file.attached_to_name = doc.company_name
            file.name = doc.company_name + " - " + "Cancelled cheque copy"
            file.insert()
            
@frappe.whitelist()
def workflow_changed_comment(doc_name):
    usr_name = frappe.get_doc("User",frappe.session.user).full_name
    usr = frappe.utils.get_link_to_form("User",frappe.session.user,usr_name)
    doc = frappe.get_doc("Purchase Invoice",doc_name)
    if doc.workflow_state == "Verification Pending":
        doc.add_comment(text="{} has send the invoice for verification pending".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Approval Pending":
        doc.add_comment(text="{} has send the invoice for approval pending".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Management Approval Pending":
        doc.add_comment(text="{} has send the invoice for management approval pending".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Approved" or doc.workflow_state == "Approved By Management":
        doc.add_comment(text="{} has approved the invoice".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "On Hold By Department Head" or doc.workflow_state == "On Hold By Management":
        doc.add_comment(text="{} has kept the invoice on Hold".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Rejected By Department Head" or doc.workflow_state == "Rejected By Management":
        doc.add_comment(text="{} has rejected the invoice".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Submitted":
        doc.add_comment(text="{} has submitted the invoice".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Cancelled":
        doc.add_comment(text="{} has cancelled the invoice".format(usr), comment_email=frappe.session.user, comment_by=usr_name)

@frappe.whitelist()
def workflow_changed_comment_order(doc_name):
    usr_name = frappe.get_doc("User",frappe.session.user).full_name
    usr = frappe.utils.get_link_to_form("User",frappe.session.user,usr_name)
    doc = frappe.get_doc("Purchase Order",doc_name)
    if doc.workflow_state == "Verification Pending":
        doc.add_comment(text="{} has send the purchase order for verification pending".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Approval Pending":
        doc.add_comment(text="{} has send the purchase order for approval pending".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Management Approval Pending":
        doc.add_comment(text="{} has send the purchase order for management approval pending".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Approved" or doc.workflow_state == "Approved By Management":
        doc.add_comment(text="{} has approved the purchase order".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "On Hold By Department Head" or doc.workflow_state == "On Hold By Management":
        doc.add_comment(text="{} has kept the purchase order on Hold".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Rejected By Department Head" or doc.workflow_state == "Rejected By Management":
        doc.add_comment(text="{} has rejected the purchase order".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Submitted":
        doc.add_comment(text="{} has submitted the purchase order".format(usr), comment_email=frappe.session.user, comment_by=usr_name)
    if doc.workflow_state == "Cancelled":
        doc.add_comment(text="{} has cancelled the purchase order".format(usr), comment_email=frappe.session.user, comment_by=usr_name)