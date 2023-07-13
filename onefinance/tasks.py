from cmath import cos
from enum import unique
from queue import Empty
import re
from weakref import ref
import frappe
from datetime import datetime
from frappe.utils import getdate
from datetime import date
from frappe.utils import date_diff
from jinja2 import Template
import time
from frappe import _
from frappe.utils import today

def reminders_at_ten():
    management_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Exco'""", as_list=1)]
    for i in range(len(management_list)):
        msg = """Hello {},<br><br>""".format(management_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"Management Approval Pending","cost_center_manager":management_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if diff_in_hours >= 24:
                    invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'Reminder for Approval')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=management_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))
        #For Purchase Order
        invoicelist = frappe.db.get_list('Purchase Order', fields=("name","supplier"),filters={"workflow_state":"Management Approval Pending","cost_center_manager":management_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Order',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if diff_in_hours >= 24:
                    invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'Reminder for Approval Purchase Order')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=management_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))

    depthead_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Department Head'""", as_list=1)]
    for i in range(len(depthead_list)):
        msg = """Hello {},<br><br>""".format(depthead_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"Approval Pending","cost_center_department_head":depthead_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if diff_in_hours >= 24: 
                    invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'Reminder for Approval')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=depthead_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))
        #For Purchase Order
        invoicelist = frappe.db.get_list('Purchase Order', fields=("name","supplier"),filters={"workflow_state":"Approval Pending","cost_center_department_head":depthead_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Order',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if diff_in_hours >= 24:
                    invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'Reminder for Approval Purchase Order')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=depthead_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))

    #on Hold reminder
    management_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Exco'""", as_list=1)]
    for i in range(len(management_list)):
        msg = """Hello {},<br><br>""".format(management_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"On Hold By Management","cost_center_manager":management_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if l.release_date:        
                    if diff_in_hours >= 24 and today > l.release_date:
                        invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'On Hold Reminder')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=management_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))
        #For Purchase Order
        invoicelist = frappe.db.get_list('Purchase Order', fields=("name","supplier"),filters={"workflow_state":"On Hold By Management","cost_center_manager":management_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Order',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if l.release_date:        
                    if diff_in_hours >= 24 and today > l.release_date:
                        invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'On Hold Reminder Purchase Order')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=management_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))

    depthead_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Department Head'""", as_list=1)]
    for i in range(len(depthead_list)):
        msg = """Hello {},<br><br>""".format(depthead_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"On Hold By Department Head","cost_center_department_head":depthead_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if l.release_date:
                    if diff_in_hours > 24 and today > l.release_date: 
                        invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'On Hold Reminder')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=depthead_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))
                #For Purchase Order
        invoicelist = frappe.db.get_list('Purchase Order', fields=("name","supplier"),filters={"workflow_state":"On Hold By Department Head","cost_center_department_head":depthead_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Order',invoice[0])
                today = date.today()
                diff = datetime.now() - l.modified
                diff_in_hours = diff.total_seconds() / 3600
                if l.release_date:
                    if diff_in_hours > 24 and today > l.release_date:
                        invoicelist2.append(invoice)
            if invoicelist2:
                notification = frappe.get_doc('Notification', 'On Hold Reminder Purchase Order')
                l.leads = invoicelist2
                args={'doc': l}
                recipients,cc,bb = notification.get_list_of_recipients(l, args)
                frappe.enqueue(method=frappe.sendmail, recipients=depthead_list[i][0], sender=None, 
                subject=frappe.render_template(notification.subject, args), message=msg + frappe.render_template(notification.message, args))


def reminders_at_nine():
    ## Bank MIS
    payment_entries = frappe.db.sql("""select count(name) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.workflow_state = 'Submitted'""")
    
    if payment_entries[0][0] >= 1:
        payment_entry_amounts = frappe.db.sql("""select
        sum(p.paid_amount) as "Total Amount Paid By Bank::250",
        (select sum(p.paid_amount) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype="Purchase Invoice" or r.reference_doctype="Purchase Order" or r.reference_doctype="Journal Entry")) and p.workflow_state = "Submitted") as "Amount Paid Through Approval System-Purchase Invoice::250",
        (select sum(paid_amount) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and (not exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent) or exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype != "Purchase Invoice" and r.reference_doctype != "Purchase Order" and r.reference_doctype != "Journal Entry"))) and p.workflow_state = "Submitted") as "Amount Paid Wthout Approval System::250"
        from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.workflow_state = 'Submitted'""")

        if payment_entry_amounts[0][0] != None and payment_entry_amounts[0][1] != None and payment_entry_amounts[0][2] != None:
            payment_entry_amount = frappe.db.sql("""select
            sum(p.paid_amount) as "Total Amount Paid By Bank::250",
            (select sum(p.paid_amount) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype="Purchase Invoice" or r.reference_doctype="Purchase Order" or r.reference_doctype="Journal Entry")) and p.workflow_state = "Submitted") as "Amount Paid Through Approval System-Purchase Invoice::250",
            (select sum(paid_amount) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and (not exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent) or exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype != "Purchase Invoice" and r.reference_doctype != "Purchase Order" and r.reference_doctype != "Journal Entry"))) and p.workflow_state = "Submitted") as "Amount Paid Wthout Approval System::250"
            from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.workflow_state = 'Submitted'""")

        if payment_entry_amounts[0][0] != None and payment_entry_amounts[0][1] == None and payment_entry_amounts[0][2] != None:
            payment_entry_amount = frappe.db.sql("""select
            sum(p.paid_amount) as "Total Amount Paid By Bank::250",
            0 as "Amount Paid Through Approval System-Purchase Invoice::250",
            (select sum(paid_amount) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and (not exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent) or exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype != "Purchase Invoice" and r.reference_doctype != "Purchase Order" and r.reference_doctype != "Journal Entry"))) and p.workflow_state = "Submitted") as "Amount Paid Wthout Approval System::250"
            from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.workflow_state = 'Submitted'""")

        if payment_entry_amounts[0][0] != None and payment_entry_amounts[0][1] != None and payment_entry_amounts[0][2] == None:
            payment_entry_amount = frappe.db.sql("""select
            sum(p.paid_amount) as "Total Amount Paid By Bank::250",
            (select sum(p.paid_amount) from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype="Purchase Invoice" or r.reference_doctype="Purchase Order" or r.reference_doctype="Journal Entry")) and p.workflow_state = "Submitted") as "Amount Paid Through Approval System-Purchase Invoice::250",
            0 as "Amount Paid Wthout Approval System::250"
            from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.workflow_state = 'Submitted'""")

    else:
        payment_entry_amount = ((0,0,0),)

    print(payment_entry_amount,"payment_entry_amount")

    purchase_invoice_names = []
    payment_entry_amount_list = []
    approver = []
    description =[]
    supplier_list = []
    reference_date = []
    payment_entry_name = frappe.db.sql("""select p.name,p.paid_amount,p.party_name,p.reference_date from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype="Purchase Invoice" or r.reference_doctype="Purchase Order" or r.reference_doctype="Journal Entry")) and p.workflow_state = "Submitted" """)
    
    for i in payment_entry_name:
        purchase_invoice_name = frappe.db.sql("""select r.reference_name,r.allocated_amount,r.approver,r.description from `tabPayment Entry Reference` r where r.parent=%s and (r.reference_doctype="Purchase Invoice" or r.reference_doctype="Purchase Order" or r.reference_doctype="Journal Entry")""",(i[0]))
        for j in purchase_invoice_name:
            purchase_invoice_names.append(j[0])
            payment_entry_amount_list.append(j[1])    
            supplier_list.append(i[2])
            approver.append(j[2])
            description.append(j[3])
            reference_date.append(i[3])
    zip_list = list(zip(purchase_invoice_names,payment_entry_amount_list,supplier_list,approver,description,reference_date))

    payment_entry_name_without_approval = frappe.db.sql("""select p.approver,p.paid_amount,p.party_name,p.remarks,p.reference_date from `tabPayment Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and (not exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent) or exists(select r.reference_doctype from `tabPayment Entry Reference` r where p.name=r.parent and (r.reference_doctype != "Purchase Invoice" and r.reference_doctype != "Purchase Order" and r.reference_doctype != "Journal Entry"))) and p.workflow_state = "Submitted" """)
    print(payment_entry_name_without_approval, "payment_entry_name_without_approval")

    journal_entry_name = frappe.db.sql("""select p.name,p.cheque_date,p.approver,p.user_remark from `tabJournal Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.docstatus = 1 and p.voucher_type = 'Bank Entry' and p.mis = 1 """)
    journal_entry_without_approvals = []
    journal_entry_amount_list = []
    approver_2 = []
    description_2 =[]
    supplier_list_2 = []
    reference_date_2 = []
    print(journal_entry_name)
    if len(journal_entry_name) >= 1:
        for i in journal_entry_name:
            journal_entry_without_approval = frappe.db.sql("""select case WHEN ja.party_type != "" THEN ja.party else ja.account end, ja.debit_in_account_currency from `tabJournal Entry Account` ja where ja.parent = %s and ja.account != 'HDFC Bank Current A/C 5504 - 1F'""",(i[0]))
            for j in journal_entry_without_approval:
                journal_entry_without_approvals.append(i[0])
                journal_entry_amount_list.append(j[1])
                approver_2.append(i[2])
                description_2.append(i[3])
                supplier_list_2.append(j[0])
                reference_date_2.append(i[1])
    print(journal_entry_amount_list)
    if len(journal_entry_amount_list) >= 1:
        total_jornal_entry_amount = sum(journal_entry_amount_list)
    else:
        total_jornal_entry_amount = 0

    print(total_jornal_entry_amount,"*************")

    zip_list_2 = list(zip(approver_2,journal_entry_amount_list,supplier_list_2,description_2,reference_date_2))
    print(tuple(zip_list_2), "zip list")
    zip_tuple = tuple(zip_list_2)

    if len(zip_tuple) >= 1:
        final_without_approval = zip_tuple + payment_entry_name_without_approval
    else:
        final_without_approval = payment_entry_name_without_approval


    print(final_without_approval)

    msg1_today  = """<table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
                <tr><th colspan="3">Daily Payment Report - {} </th></tr>
                <tr><th>Amount Paid from Bank</th><th>ERP Approved Amount</th><th>Non ERP Approved Amount</th></tr>
                <tr><td>{}</td><td>{}</td><td>{}</td></tr>
            </table><br><br>""".format(frappe.utils.getdate().strftime("%d-%m-%Y"),payment_entry_amount[0][0]+total_jornal_entry_amount,payment_entry_amount[0][1],payment_entry_amount[0][2]+total_jornal_entry_amount)

    msg2_today = """<table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
                <tr><th colspan="5">ERP approval - {}</th></tr>
                <tr><th>Payment Date</th><th>Approver Name</th><th>Amount</th><th>Party Name/Remarks</th><th>Narration</th></tr>""".format(frappe.utils.getdate().strftime("%d-%m-%Y"))
    for p_name in zip_list:
        msg2_today+="<tr><td>"+str(p_name[5].strftime("%d-%m-%Y"))+"</td><td>"+str(p_name[3])+"</td><td>"+str(p_name[1])+"</td><td>"+str(p_name[2])+"</td><td>"+str(p_name[4])+"</td></tr>"
    msg2_today+="<tr><th>Total: </th><th>{}</th><th colspan ='3'></th></tr>".format(payment_entry_amount[0][1])
    msg2_today+="""</table><br><br>"""

    msg3_today="""<table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
                <tr><th colspan="5">Non ERP approval {}</th></tr>
                 <tr><th>Payment Date</th><th>Approver Name</th><th>Amount</th><th>Party Name/Remarks</th><th>Narration</th></tr>""".format(frappe.utils.getdate().strftime("%d-%m-%Y"))
    for i in final_without_approval:
        msg3_today+="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(i[4].strftime("%d-%m-%Y"),i[0],i[1],i[2],i[3])
    msg3_today+="<tr><th>Total: </th><th>{}</th><th colspan ='3'></th></tr>".format(payment_entry_amount[0][2]+total_jornal_entry_amount)
    msg3_today+= """</table>"""
    
    msg_today  = msg1_today+msg2_today+msg3_today
    frappe.sendmail(subject="MIS Report - Bank Payment", content=msg_today, recipients = '{},{},{},{},{}'.format("dipen.bhanushali@1finance.co.in","mohan@1finance.co.in","accounts@1finance.co.in","dilip.jaiswar@1finance.co.in","harish.tanwar@atriina.com"))
    
    ## Credit Card MIS
    journal_entry_name_credit_card = frappe.db.sql("""select p.name,p.cheque_date,p.approver,p.user_remark from `tabJournal Entry` p where p.submitted_date = CURDATE() and p.submitted_date = p.amended_from_submitted_date and p.docstatus = 1 and p.in_credit_card_mis = 1 """)
    journal_entry_without_approvals_credit_card = []
    journal_entry_amount_list_credit_card = []
    approver_2_credit_card = []
    description_2_credit_card =[]
    supplier_list_2_credit_card = []
    reference_date_2_credit_card = []
    print(journal_entry_name_credit_card)
    if len(journal_entry_name_credit_card) >= 1:
        for i in journal_entry_name_credit_card:
            journal_entry_without_approval_credit_card = frappe.db.sql("""select ja.party, ja.debit_in_account_currency from `tabJournal Entry Account` ja where ja.parent = %s and ja.debit_in_account_currency != 0""",(i[0]))
            print(journal_entry_without_approval_credit_card)
            for j in journal_entry_without_approval_credit_card:
                paid_from = frappe.db.sql("""select ja.party from `tabJournal Entry Account` ja where parent = %s and ja.debit_in_account_currency = 0""",(i[0]))
                print(paid_from)
                journal_entry_without_approvals_credit_card.append(paid_from[0][0])
                journal_entry_amount_list_credit_card.append(j[1])
                approver_2_credit_card.append(i[2])
                description_2_credit_card.append(i[3])
                supplier_list_2_credit_card.append(j[0])
                reference_date_2_credit_card.append(i[1])
    
    print(journal_entry_amount_list_credit_card)
    if len(journal_entry_amount_list_credit_card) >= 1:
        total_jornal_entry_amount = sum(journal_entry_amount_list_credit_card)
    else:
        total_jornal_entry_amount = 0

    print(total_jornal_entry_amount,"*************")

    zip_list_3 = list(zip(approver_2_credit_card,journal_entry_amount_list_credit_card,supplier_list_2_credit_card,description_2_credit_card,reference_date_2_credit_card,journal_entry_without_approvals_credit_card))
    print(tuple(zip_list_3), "zip list")
    zip_tuple_2 = tuple(zip_list_3)

    msg4_today="""<table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
                <tr><th colspan="6">Credit Card Payment (Non-ERP Approved) - {}</th></tr>
                 <tr><th>Payment Date</th><th>Approver Name</th><th>Amount</th><th>Party Name/Remarks</th><th>Narration</th><th>Paid from</th></tr>""".format(frappe.utils.getdate().strftime("%d-%m-%Y"))
    for i in zip_tuple_2:
        msg4_today+="<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(i[4].strftime("%d-%m-%Y"),i[0],i[1],i[2],i[3],i[5])
    msg4_today+="<tr><th>Total: </th><th>{}</th><th colspan ='4'></th></tr>".format(total_jornal_entry_amount)
    msg4_today+= """</table>"""
    
    frappe.sendmail(subject="MIS Report - Credit Card", content=msg4_today, recipients = '{},{},{},{},{}'.format("dipen.bhanushali@1finance.co.in","mohan@1finance.co.in","accounts@1finance.co.in","dilip.jaiswar@1finance.co.in","harish.tanwar@atriina.com"))



def create_payment_entry(doc, method):
    if "1FIPLCX_5860" in doc.file_name:
        content = frappe.db.sql("""select count(name) from `tabFile` where content_hash = %s""", doc.content_hash)
        if content[0][0] == 1:
            file_url = doc.file_url
            if file_url:
                my_list= []
                name = frappe.db.get("File", {"file_url": file_url}).name
                content = frappe.get_doc("File", name).get_content()
                if content:
                    line = content.split("\n")
                    for i in line:
                        words = i.split(',')
                        my_list.append(words)

                    for i in my_list:
                        if len(i) > 1 and "1F/PUR" in i[7] and i[11] == "E":
                            pi_supplier = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "supplier")
                            is_supplier = frappe.db.get_value("Supplier", {"name": pi_supplier}, "name")
                            pi_docstatus = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "docstatus")
                            pi_amount = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "outstanding_amount")
                            if is_supplier and pi_docstatus == 1 and pi_amount > 0:
                                pe = frappe.new_doc("Payment Entry")
                                pe.posting_date = datetime.strptime(datetime.strptime(i[5], "%d/%m/%Y").strftime("%d-%m-%Y"), '%d-%m-%Y')
                                pe.payment_type = "Pay"
                                pe.mode_of_payment = "Bank Transfer"
                                pe.party_type = "Supplier"
                                pe.party = pi_supplier
                                pe.party_name = pi_supplier
                                pe.paid_from = "HDFC Bank Current A/C 5504 - 1F"
                                pe.paid_amount = float(i[3])
                                pe.received_amount = float(i[3])
                                row = pe.append('references', {})
                                row.reference_doctype = "Purchase Invoice"
                                row.reference_name = i[7]
                                row.outstanding_amount = pi_amount
                                row.allocated_amount = float(i[3])
                                pe.reference_no = i[15]
                                pe.reference_date = datetime.strptime(datetime.strptime(i[5], "%d/%m/%Y").strftime("%d-%m-%Y"), '%d-%m-%Y')
                                pe.reverse_file_name = doc.name
                                pe.save()
                                frappe.db.commit()

                            else:
                                pass
                        elif len(i) > 1 and "ORD" in i[7] and i[11] == "E":
                            po_supplier = frappe.db.get_value("Purchase Order", {"name": i[7]}, "supplier")
                            is_supplier = frappe.db.get_value("Supplier", {"name": po_supplier}, "name")
                            po_docstatus = frappe.db.get_value("Purchase Order", {"name": i[7]}, "docstatus")
                            po_amount = frappe.db.get_value("Purchase Order", {"name": i[7]}, "rounded_total")
                            po_advance_paid = frappe.db.get_value("Purchase Order", {"name": i[7]}, "advance_paid")
                            po_per_billed = frappe.db.get_value("Purchase Order", {"name": i[7]}, "per_billed")
                            if is_supplier and po_docstatus ==1 and  po_per_billed < 100:
                                pe = frappe.new_doc("Payment Entry")
                                pe.posting_date = datetime.strptime(datetime.strptime(i[5], "%d/%m/%Y").strftime("%d-%m-%Y"), '%d-%m-%Y')
                                pe.payment_type = "Pay"
                                pe.mode_of_payment = "Bank Transfer"
                                pe.party_type = "Supplier"
                                pe.party = po_supplier
                                pe.party_name = po_supplier
                                pe.paid_from = "HDFC Bank Current A/C 5504 - 1F"
                                pe.paid_amount = float(i[3])
                                pe.received_amount = float(i[3])
                                row = pe.append('references', {})
                                row.reference_doctype = "Purchase Order"
                                row.reference_name = i[7]
                                row.outstanding_amount = po_amount - po_advance_paid
                                row.allocated_amount = float(i[3])
                                pe.reference_no = i[15]
                                pe.reference_date = datetime.strptime(datetime.strptime(i[5], "%d/%m/%Y").strftime("%d-%m-%Y"), '%d-%m-%Y')
                                pe.reverse_file_name = doc.name
                                pe.save()
                                frappe.db.commit()
                            
                            else:
                                pass

                        else:
                            pass

                    time.sleep(30)
                    print(my_list)
                    for i in my_list:
                        if len(i) > 1:
                            pi_name = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "name")
                            pi_supplier = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "supplier")
                            is_pi_supplier = frappe.db.get_value("Supplier", {"name": pi_supplier}, "name")
                            pi_docstatus = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "docstatus")
                            pi_amount = frappe.db.get_value("Purchase Invoice", {"name": i[7]}, "outstanding_amount")
                            po_name = frappe.db.get_value("Purchase Order", {"name": i[7]}, "name")
                            po_supplier = frappe.db.get_value("Purchase Order", {"name": i[7]}, "supplier")
                            is_po_supplier = frappe.db.get_value("Supplier", {"name": po_supplier}, "name")
                            po_docstatus = frappe.db.get_value("Purchase Order", {"name": i[7]}, "docstatus")
                            po_amount = frappe.db.get_value("Purchase Order", {"name": i[7]}, "rounded_total")
                            po_advance_paid = frappe.db.get_value("Purchase Order", {"name": i[7]}, "advance_paid")
                            po_per_billed = frappe.db.get_value("Purchase Order", {"name": i[7]}, "per_billed")
                            
                            if "1F/PUR" in i[7]:
                                if not pi_name:
                                    i.append("Reason - Purchase Invoice Not found")
                                elif not is_pi_supplier:
                                    i.append("Reason - Supplier Not found")
                                elif not pi_docstatus == 1:
                                    i.append("Reason - Purchase Invoice is not submitted")
                                elif i[11] == "R":
                                    i.append("Reason - This payment is rejected by Bank")
                                elif pi_amount == 0:
                                    i.append("Reason - Purchase Invoice is fully paid")
                                else:
                                    pass
                            
                            elif "ORD" in i[7]:
                                if not po_name:
                                    i.append("Reason - Purchase Order Not found")
                                elif not is_po_supplier:
                                    i.append("Reason - Supplier Not found")
                                elif not po_docstatus == 1:
                                    i.append("Reason - Purchase Order is not submitted")
                                if i[11] == "R":
                                    i.append("Reason - This payment is rejected by Bank")
                                elif po_per_billed == 100:
                                    i.append("Reason - Purchase Order is fully billed")
                                else:
                                    pass
                            
                            else:
                                i.append("Reason - Purchase Invoice/Order not found")                                                 
                            
                    print(my_list)

                    pay_list = []
                    pe_list = frappe.db.sql("""select name from `tabPayment Entry` where reverse_file_name = %s""", doc.name)
                    for i in pe_list:
                        pay_list.append(i[0])

                    reference_list = []
                    mail_list = []
                    for i in pay_list:
                        var = frappe.db.sql("""select reference_name from `tabPayment Entry Reference` where parent = %s""", i)
                        reference_list.append(var[0][0])
                    for i in my_list:
                        if len(i)> 1:
                            if i[7] not in reference_list:
                                mail_list.append(i)
                    if len(mail_list) >= 1:
                        msg = """Hello,<br><br>The payment entry for the below response is not created for the File Name - '{}'<br><br>{}""".format(doc.file_name,mail_list)
                        frappe.sendmail(subject="Payment entry rejected", content=msg, recipients = '{},{},{}'.format("dipen.bhanushali@1finance.co.in","rupak.pradhan@1finance.co.in","rajni.virvani@1finance.co.in"))

        else:
            frappe.throw("This file is already uploaded. So no Payment Entry is created.")

    else:
        pass

def create_dues():
    """
    this function create dues for all contract if setting check automtic
    """
	
    is_creat_dues_auto = frappe.db.get_single_value("Contract Payment Settings", "auto_create_dues") 

    if not is_creat_dues_auto:
        return 
    contract_dues = frappe.get_list(
        "Contract Dues", filters={"date_dues": today()}, fields=["*"]
    )
    for d in contract_dues:
        parent_doc = frappe.get_doc('Contract', d['parent'])
        if parent_doc.docstatus != 1:
            return
        if parent_doc.party_type == 'Supplier':
            parent_doc.create_purchase_invoice()
        if parent_doc.party_type == 'Customer':
            parent_doc.create_sales_invoice()

def reminders_for_contract():
    contract_list = frappe.db.sql("""select name from `tabContract`""")
    print(contract_list)
    if len(contract_list) >= 1:
        for i in contract_list:
            contract_dues = frappe.db.sql("""select date_dues, amount, paid_amount, is_paid, is_partial_paid, is_late, party_type, party_name from `tabContract Dues` where parent = %s""",(i[0]))
            print(i[0])
            approver_email = frappe.get_doc("Contract", i[0])
            approver_email_id = approver_email.approver_email_id
            approver_name = approver_email.approver_name
            responsible_email_id = approver_email.responsible_person_email_id
            responsible_name = approver_email.responsible_person_name
            supplier = approver_email.party_name
            url = (frappe.utils.get_url()) + "/" + "app" + "/" + "contract"
            print(url)
            print(approver_email_id)
            if len(contract_dues) >= 1:
                for j in contract_dues:        
                    today = date.today()
                    diff = j[0] - today
                    print(diff.days)
                    if j[3] == 0 and j[4] == 0:
                        if diff.days == 8:
                            print("Hello")
                            msg = """Dear {},<br><br>
                            This email serves as a friendly reminder about an outstanding payment 
                            for our <b>{}</b> services. The payment is now overdue, and we kindly 
                            request your immediate attention.<br> Failure to pay within eight days 
                            may result in service disruption. Please settle the outstanding amount 
                            promptly to ensure uninterrupted service. <br><br>
                            For payment details, kindly refer to the below Link. If you have any questions or concerns, feel free to contact our accounts 
                            receivable team.<br><br>
                            Thank you for your prompt action.<br><br>Link - {}<br><br>""".format(approver_name,supplier,url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Service Disruption Possible", content=msg, recipients = '{}'.format(approver_email_id))

                            msg1 = """Dear {},<br><br>
                            This email serves as a friendly reminder about an outstanding payment 
                            for our <b>{}</b> services. The payment is now overdue, and we kindly 
                            request your immediate attention.<br> Failure to pay within eight days 
                            may result in service disruption. Please settle the outstanding amount 
                            promptly to ensure uninterrupted service. <br><br>
                            For payment details, kindly refer to the below Link. If you have any questions or concerns, feel free to contact our accounts 
                            receivable team.<br><br>
                            Thank you for your prompt action.<br><br>Link - {}<br><br>""".format(responsible_name,supplier,url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Service Disruption Possible", content=msg1, recipients = '{}'.format(responsible_email_id))
                        
                        if diff.days == 2:
                            msg = """Dear {},<br><br>
                            We hope this email finds you well. We wanted to remind 
                            you about the outstanding balance on your account for 
                            <b>{}</b> services provided by our company.<br><br>
                            Please settle this amount as soon as possible to avoid any 
                            further inconvenience.<br><br>
                            Below is a Link for your reference. If you have already made the payment or have any questions, 
                            please contact our accounts department.<br><br>
                            Thank you for your prompt attention to this matter.<br><br>
                            Link - {}<br><br>""".format(approver_name,i[0],url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Outstanding Balance", content=msg, recipients = '{}'.format(approver_email_id))

                            msg1 = """Dear {},<br><br>
                            We hope this email finds you well. We wanted to remind 
                            you about the outstanding balance on your account for 
                            <b>{}</b> services provided by our company.<br><br>
                            Please settle this amount as soon as possible to avoid any 
                            further inconvenience.<br><br>
                            Below is a Link for your reference. If you have already made the payment or have any questions, 
                            please contact our accounts department.<br><br>
                            Thank you for your prompt attention to this matter.<br><br>
                            Link - {}<br><br>""".format(approver_name,i[0],url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Outstanding Balance", content=msg1, recipients = '{}'.format(responsible_email_id))


                    elif j[3] == 0 and j[4] == 1:
                        if diff.days == 8:
                            print("Hello")
                            msg = """Dear {},<br><br>
                            This email serves as a friendly reminder about an outstanding payment 
                            for our <b>{}</b> services. The payment is now overdue, and we kindly 
                            request your immediate attention.<br> Failure to pay within eight days may result in 
                            service disruption. Please settle the outstanding amount promptly to ensure uninterrupted service. <br><br>
                            For payment details, kindly refer to the below Link. If you have any questions or concerns, feel free to contact our accounts receivable team.<br><br>
                            Thank you for your prompt action.<br><br>Link - {}<br><br>""".format(approver_name,supplier,url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Service Disruption Possible", content=msg, recipients = '{}'.format(approver_email_id))

                            msg1 = """Dear {},<br><br>
                            This email serves as a friendly reminder about an outstanding payment 
                            for our <b>{}</b> services. The payment is now overdue, and we kindly 
                            request your immediate attention.<br> Failure to pay within eight days may result in 
                            service disruption. Please settle the outstanding amount promptly to ensure uninterrupted service. <br><br>
                            For payment details, kindly refer to the below Link. If you have any questions or concerns, feel free to contact our accounts receivable team.<br><br>
                            Thank you for your prompt action.<br><br>Link - {}<br><br>""".format(responsible_name,supplier,url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Service Disruption Possible", content=msg1, recipients = '{}'.format(responsible_email_id))
                        
            
                        if diff.days == 2:
                            msg = """Dear {},<br><br>
                            We hope this email finds you well. We wanted to remind 
                            you about the outstanding balance on your account for 
                            <b>{}</b> services provided by our company.<br><br>
                            Please settle this amount as soon as possible to avoid any 
                            further inconvenience.<br><br>
                            Below is a Link for your reference. If you have already made the payment or have any questions, 
                            please contact our accounts department.<br><br>
                            Thank you for your prompt attention to this matter.<br><br>
                            Link - {}<br><br>""".format(approver_name,i[0],url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Outstanding Balance", content=msg, recipients = '{}'.format(approver_email_id))

                            msg1 = """Dear {},<br><br>
                            We hope this email finds you well. We wanted to remind 
                            you about the outstanding balance on your account for 
                            <b>{}</b> services provided by our company.<br><br>
                            Please settle this amount as soon as possible to avoid any 
                            further inconvenience.<br><br>
                            Below is a Link for your reference. If you have already made the payment or have any questions, 
                            please contact our accounts department.<br><br>
                            Thank you for your prompt attention to this matter.<br><br>
                            Link - {}<br><br>""".format(approver_name,i[0],url)
                            frappe.sendmail(subject="Urgent Payment Reminder - Outstanding Balance", content=msg1, recipients = '{}'.format(responsible_email_id))


                    elif j[3] == 1 and j[4] == 0:
                        pass

                    else:
                        pass