from cmath import cos
import frappe
from datetime import datetime
from frappe.utils import getdate
from datetime import date
from frappe.utils import date_diff
from jinja2 import Template

def reminders_at_ten():
    management_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Exco'""", as_list=1)]
    print(management_list,"management_list")
    for i in range(len(management_list)):
        print(management_list[i][1],"management_list")
        msg = """Hello {},<br><br>""".format(management_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"Management Approval Pending","cost_center_manager":management_list[i][0]}, as_list = True)
        print(invoicelist,"invoicelist")
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

    depthead_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Department Head'""", as_list=1)]
    for i in range(len(depthead_list)):
        print("***",depthead_list[i][1])
        msg = """Hello {},<br><br>""".format(depthead_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"Approval Pending","cost_center_department_head":depthead_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                print(l)
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

    #on Hold reminder
    management_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Exco'""", as_list=1)]
    for i in range(len(management_list)):
        print("***",management_list[i][1])
        msg = """Hello {},<br><br>""".format(management_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"On Hold By Management","cost_center_manager":management_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                print(l)
                today = date.today()
                diff = datetime.now() - l.modified
                print(f"Date Diff : {diff}")
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

    depthead_list =[x for x in frappe.db.sql("""select u.name,u.full_name from `tabUser` u inner join `tabHas Role` hr on hr.parent = u.name where hr.role = 'Department Head'""", as_list=1)]
    for i in range(len(depthead_list)):
        print("***",depthead_list[i][1])
        msg = """Hello {},<br><br>""".format(depthead_list[i][1])
        invoicelist = frappe.db.get_list('Purchase Invoice', fields=("name","supplier"),filters={"workflow_state":"On Hold By Department Head","cost_center_department_head":depthead_list[i][0]}, as_list = True)
        invoicelist2 = []
        if invoicelist:
            for invoice in invoicelist:
                l = frappe.get_doc('Purchase Invoice',invoice[0])
                print(l)
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