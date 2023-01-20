__version__ = '0.0.1'


import frappe
from frappe import _
from frappe.utils.background_jobs import enqueue
from frappe.workflow.doctype.workflow_action.workflow_action import process_workflow_actions as process_workflow_actions_frappe, confirm_action
from frappe.model.workflow import apply_workflow, get_workflow_name, has_approval_access, \
    get_workflow_state_field, send_email_alert, get_workflow_field_value, is_transition_condition_satisfied
from frappe.desk.notifications import clear_doctype_notifications
from frappe.workflow.doctype.workflow_action.workflow_action import get_email_template, clear_workflow_actions, is_workflow_action_already_created, \
    clear_old_workflow_actions_using_user, update_completed_workflow_actions, get_next_possible_transitions, get_doc_workflow_state, get_users_next_action_data, \
    create_workflow_actions_for_roles, send_workflow_action_email, deduplicate_actions, return_success_page
    
    
from frappe.workflow.doctype.workflow_action.workflow_action import get_common_email_args as get_common_email_args_frappe
from frappe.workflow.doctype.workflow_action.workflow_action import return_action_confirmation_page as return_action_confirmation_page_frappe
from frappe.workflow.doctype.workflow_action.workflow_action import return_success_page as return_success_page_frappe
from frappe.workflow.doctype.workflow_action.workflow_action import confirm_action as confirm_action_frappe



# from frappe.workflow.doctype.workflow_action.workflow_action import return_success_page as return_success_page_frappe
# from frappe.workflow.doctype.workflow_action.workflow_action import confirm_action as confirm_action_frappe


"""

clear_old_workflow_actions_using_user does not exists in v14
create_workflow_actions_for_roles does not exists in v14

"""


def get_common_email_args_custom(doc, attachments=None):
    doctype = doc.get('doctype')
    docname = doc.get('name')
    print("Doc", doc)
    if doctype == "Purchase Invoice":
        if doc.workflow_state == "Approval Pending" or doc.workflow_state == "Approved" or doc.workflow_state == "On Hold By Department Head" or doc.workflow_state == "Management Approval Pending" or doc.workflow_state == "Approved By Management" or doc.workflow_state == "Rejected" or doc.workflow_state == "Rejected By Management" or doc.workflow_state == "On Hold By Management":
            message1 = """<b>{0} : {1}</b><br><br>""".format(doctype, docname)
            if doc.workflow_state == "Approved" or doc.workflow_state == "Management Approval Pending":
                var = frappe.get_doc("User", doc.department_head).full_name
                message2 = """<b>Approved By :</b> {}<br><br>""".format(var)
            else:
                message2 = """<br>"""
            message3 = """<b>Details of Invoice</b>:<br><br>"""
            message4 = """<table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
						<tr><th>Party Name</th><th>Invoice No.</th><th>Invoice Date</th><th>Amount</th><th>Description</th></tr>
						"""
            for item in doc.items:
                message4 += "<tr><td>"+doc.supplier + "</td><td>"+str(doc.bill_no if doc.bill_no else "--") + "</td><td>" + str(
                    doc.bill_date if doc.bill_date else "--") + "</td><td>" + str(item.amount) + "</td><td>" + item.description + "</td><tr>"
            message4 += "</table><br>* The above amount is exclusive of GST and TDS.<br><br>"

            if doc.pre_approved_items:
                message5 = """<b>Pre Approved terms :</b><br><br><table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center;>
						<tr><th>Monthly Amount</th><th>Description</th></tr>
						"""
                for item in doc.pre_approved_items:
                    message5 += "<tr><td>" + \
                        str(item.rate) + "</td><td>" + \
                        item.description + "</td><tr>"
                message5 += "</table><br>"
            else:
                message5 = """<br>"""

            attachments = frappe.get_all('File', filters={
                                         'attached_to_doctype': 'Purchase Invoice', 'attached_to_name': doc.name}, fields=['file_name', 'file_url'])
            if attachments:
                message6 = """<b>Attachments</b> : <ul>"""
                for attachment in attachments:
                    message6 += """<li><a href="{}">{}</a></li>""".format(
                        attachment.file_url, attachment.file_name)
                message6 += """</ul><br>"""
            else:
                message6 = """<br>"""

            messageFinal = message1 + message2 + message3 + message4 + message5 + message6

            email_template = get_email_template(doc)
            if email_template:
                subject = frappe.render_template(
                    email_template.subject, vars(doc))
                response = frappe.render_template(
                    email_template.response, vars(doc))
            else:
                subject = _('INVOICE APPROVAL')
                response = _(messageFinal)

            common_args = {
                'template': 'workflow_action',
                'header': 'INVOICE APPROVAL',
                'attachments': [],
                'subject': subject,
                'message': response
            }
            return common_args


def send_workflow_action_email_custom(users_data, doc):
    print("send", doc.doctype)
    print("##############")
    common_args = get_common_email_args_custom(doc)
    message = common_args.pop('message', None)
    if doc.workflow_state == "Approval Pending" or doc.workflow_state == "On Hold By Department Head":
        for d in users_data:
            print(d)
            email_args = {
                'recipients': [doc.cost_center_department_head],
                'args': {
                    'actions': list(deduplicate_actions(d.get('possible_actions'))),
                    'message': message
                },
                'reference_name': doc.name,
                'reference_doctype': doc.doctype
            }
            email_args.update(common_args)
            enqueue(method=frappe.sendmail, queue='short', **email_args)
            break

    if doc.workflow_state == "Management Approval Pending" or doc.workflow_state == "On Hold By Management":
        for d in users_data:
            email_args = {
                'recipients': [doc.cost_center_manager],
                'args': {
                    'actions': list(deduplicate_actions(d.get('possible_actions'))),
                    'message': message
                },
                'reference_name': doc.name,
                'reference_doctype': doc.doctype
            }
            email_args.update(common_args)
            enqueue(method=frappe.sendmail, queue='short', **email_args)
            break

    if doc.workflow_state == "Approved" or doc.workflow_state == "Approved By Management" or doc.workflow_state == "Rejected" or doc.workflow_state == "Rejected By Management":
        for d in users_data:
            email_args = {
                'recipients': [d.get('email')],
                'args': {
                    'actions': list(deduplicate_actions(d.get('possible_actions'))),
                    'message': message
                },
                'reference_name': doc.name,
                'reference_doctype': doc.doctype
            }
            email_args.update(common_args)
            enqueue(method=frappe.sendmail, queue='short', **email_args)


def process_workflow_actions_custom(doc, state):
    workflow = get_workflow_name(doc.get("doctype"))
    if not workflow:
        return

    if state == "on_trash":
        clear_workflow_actions(doc.get("doctype"), doc.get("name"))
        return

    if is_workflow_action_already_created(doc):
        return

    clear_old_workflow_actions_using_user(doc)

    update_completed_workflow_actions(
        doc, workflow=workflow, workflow_state=get_doc_workflow_state(doc)
    )
    clear_doctype_notifications("Workflow Action")

    next_possible_transitions = get_next_possible_transitions(
        workflow, get_doc_workflow_state(doc), doc
    )

    if not next_possible_transitions:
        return

    user_data_map, roles = get_users_next_action_data(
        next_possible_transitions, doc)

    if not user_data_map:
        return

    create_workflow_actions_for_roles(roles, doc)

    if send_email_alert(workflow):
        print(workflow)
        if workflow == "Purchase Invoice Workflow":
            enqueue(send_workflow_action_email_custom, queue='short',
                    users_data=list(user_data_map.values()), doc=doc)
        else:
            enqueue(send_workflow_action_email, queue='short',
                    users_data=list(user_data_map.values()), doc=doc)


def return_action_confirmation_page_custom(doc, action, action_link, alert_doc_change=False):
    doctype = doc.get('doctype')
    docname = doc.get('name')
    print("Doc", doc)
    if doctype == "Purchase Invoice":
        template_params = {
            'title': doc.get('name'),
            'doctype': doc.get('doctype'),
            'docname': doc.get('name'),
            'action': action,
            'action_link': action_link,
            'alert_doc_change': alert_doc_change
        }

        # template_params['pdf_link'] = get_pdf_link(doc.get('doctype'), doc.get('name'))

        frappe.respond_as_web_page(title=None,
                                   html=None,
                                   indicator_color='blue',
                                   template='confirm_action_custom',
                                   context=template_params)

    else:
        return_action_confirmation_page_frappe(
            doc, action, action_link, alert_doc_change=False)


def return_action_confirmation_page_custom(doc, action, action_link, alert_doc_change=False):
    doctype = doc.get('doctype')
    docname = doc.get('name')
    print("Doc", doc)
    if doctype == "Purchase Invoice":
        template_params = {
            'title': doc.get('name'),
            'doctype': doc.get('doctype'),
            'docname': doc.get('name'),
            'action': action,
            'action_link': action_link,
            'alert_doc_change': alert_doc_change
        }

        # template_params['pdf_link'] = get_pdf_link(doc.get('doctype'), doc.get('name'))

        frappe.respond_as_web_page(title=None,
                                   html=None,
                                   indicator_color='blue',
                                   template='confirm_action_custom',
                                #    template='noname',
                                   context=template_params)

    else:
        return_action_confirmation_page_frappe(
            doc, action, action_link, alert_doc_change=False)


# def return_success_page_custom(doc):
#     if doc.get('doctype') == "Purchase Invoice":
#         if get_doc_workflow_state(doc) == "Approved" or get_doc_workflow_state(doc) == "Approval Pending" or get_doc_workflow_state(doc) == "Management Approval Pending" or get_doc_workflow_state(doc) == "Approved By Management" or get_doc_workflow_state(doc) == "Submitted":
#             frappe.respond_as_web_page(_("Success"),
#                                        _("""<script>setTimeout("window.close()", 2000)</script><div align="center"><b>Thank you!</b><br><br><img src="https://w7.pngwing.com/pngs/179/1015/png-transparent-computer-icons-check-mark-adobe-acrobat-green-tick-trademark-logo-grass.png" alt="Thank You!" width="100" height="200"></div>"""), indicator_color='green')
#         if get_doc_workflow_state(doc) == "Rejected" or get_doc_workflow_state(doc) == "Rejected By Management":
#             frappe.respond_as_web_page(_("Success"),
#                                        _("""<script>setTimeout("window.close()", 2000)</script><div align="center"><b>You have rejected the invoice</b><br><br><img src="https://w7.pngwing.com/pngs/175/854/png-transparent-computer-icons-button-check-mark-cross-red-cross-photography-trademark-logo.png" alt="Thank You!" width="100" height="200"></div>"""), indicator_color='green')

#         if get_doc_workflow_state(doc) == "On Hold By Department Head" or get_doc_workflow_state(doc) == "On Hold By Management":
#             frappe.respond_as_web_page(_("Success"),
#                                        _("""<script>setTimeout("window.close()", 2000)</script><div align="center"><b>The invoice has been kept on hold</b><br><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmNCSC6w0QhhDMF7fYsIlhP6NwcmicMzA5zg&usqp=CAU" alt="Thank You!" width="100" height="200"></div>"""), indicator_color='green')

#     else:
#         return_success_page_frappe(doc)
def return_success_page_custom(doc):
	if doc.get('doctype') == "Purchase Invoice":
		if get_doc_workflow_state(doc) == "Approved" or get_doc_workflow_state(doc) == "Approval Pending" or get_doc_workflow_state(doc) == "Management Approval Pending" or get_doc_workflow_state(doc) == "Approved By Management" or get_doc_workflow_state(doc) == "Submitted":
			frappe.respond_as_web_page(_("Success"),
				_("""<div align="center"><b>Thank you!</b><br><br><img src="https://w7.pngwing.com/pngs/179/1015/png-transparent-computer-icons-check-mark-adobe-acrobat-green-tick-trademark-logo-grass.png" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')
		if get_doc_workflow_state(doc) == "Rejected" or get_doc_workflow_state(doc) == "Rejected By Management":
			frappe.respond_as_web_page(_("Success"),
				_("""<div align="center"><b>You have rejected the invoice</b><br><br><img src="https://w7.pngwing.com/pngs/175/854/png-transparent-computer-icons-button-check-mark-cross-red-cross-photography-trademark-logo.png" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')

		if get_doc_workflow_state(doc) == "On Hold By Department Head" or get_doc_workflow_state(doc) == "On Hold By Management":
			frappe.respond_as_web_page(_("Success"),
				_("""<div align="center"><b>The invoice has been kept on hold</b><br><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmNCSC6w0QhhDMF7fYsIlhP6NwcmicMzA5zg&usqp=CAU" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')

	else:
		return_success_page_frappe(doc)




# /api/method/frappe.workflow.doctype.workflow_action.workflow_action.confirm_action?action=Hold&doctype=Purchase+Invoice&docname=ACC-PINV-2023-00022&user=harish.tanwar%40atriiina.com&_signature=9f114f66ee19d0cfd581bed10572b0ba

@frappe.whitelist(allow_guest=True)
def confirm_action_custom(**kwargs):
    if frappe.local.form_dict.doctype == "Purchase Invoice":
        doctype = frappe.local.form_dict.doctype
        docname = frappe.local.form_dict.docname
        action = frappe.local.form_dict.action
        user = frappe.local.form_dict.user
        reason_hold = frappe.local.form_dict.hold
        release_date = frappe.local.form_dict.date
        reason_reject = frappe.local.form_dict.reject
        if action == "Hold":
            # if not verify_request():
            # 	return

            logged_in_user = frappe.session.user
            if logged_in_user == 'Guest' and user:
                # to allow user to apply action without login
                frappe.set_user(user)

            doc = frappe.get_doc(doctype, docname)
            if doc:
                if doc.workflow_state == "Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_department_head).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_department_head, usr_name)
                    doc.add_comment(text="{} has kept the invoice on Hold".format(
                        usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
                    doc.on_hold = 1
                    doc.release_date = release_date
                    doc.hold_comment = reason_hold
                    doc.save()
                if doc.workflow_state == "Management Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_manager).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_manager, usr_name)
                    doc.add_comment(text="{} has kept the invoice on Hold".format(
                        usr), comment_email=doc.cost_center_manager, comment_by=usr_name)
                    doc.on_hold = 1
                    doc.release_date = release_date
                    doc.hold_comment = reason_hold
                    doc.save()

            newdoc = apply_workflow(doc, action)
            frappe.db.commit()
            return_success_page_custom(newdoc)

            # reset session user
            if logged_in_user == 'Guest':
                frappe.set_user(logged_in_user)

        if action == "Reject":
            # if not verify_request():
            # 	return

            logged_in_user = frappe.session.user
            if logged_in_user == 'Guest' and user:
                # to allow user to apply action without login
                frappe.set_user(user)
            doc = frappe.get_doc(doctype, docname)
            if doc:
                if doc.workflow_state == "Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_department_head).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_department_head, usr_name)
                    doc.add_comment(text="{} has rejected the invoice".format(
                        usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
                    doc.reason_of_rejection = reason_reject
                    doc.save()

                if doc.workflow_state == "Management Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_manager).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_manager, usr_name)
                    doc.add_comment(text="{} has rejected the invoice".format(
                        usr), comment_email=doc.cost_center_manager, comment_by=usr_name)
                    doc.reason_of_rejection = reason_reject
                    doc.save()

            newdoc = apply_workflow(doc, action)
            frappe.db.commit()
            return_success_page_custom(newdoc)

            # reset session user
            if logged_in_user == 'Guest':
                frappe.set_user(logged_in_user)

        if action == "Approve":
            # if not verify_request():
            # 	return

            logged_in_user = frappe.session.user
            if logged_in_user == 'Guest' and user:
                # to allow user to apply action without login
                frappe.set_user(user)

            doc = frappe.get_doc(doctype, docname)
            if doc:
                if doc.workflow_state == "Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_department_head).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_department_head, usr_name)
                    doc.add_comment(text="{} has approved the invoice".format(
                        usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
                if doc.workflow_state == "Management Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_manager).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_manager, usr_name)
                    doc.add_comment(text="{} has approved the invoice".format(
                        usr), comment_email=doc.cost_center_manager, comment_by=usr_name)

            newdoc = apply_workflow(doc, action)
            frappe.db.commit()
            return_success_page_custom(newdoc)

            # reset session user
            if logged_in_user == 'Guest':
                frappe.set_user(logged_in_user)

        if action == "Reopen":
            # if not verify_request():
            # 	return

            logged_in_user = frappe.session.user
            if logged_in_user == 'Guest' and user:
                # to allow user to apply action without login
                frappe.set_user(user)

            doc = frappe.get_doc(doctype, docname)

            if doc.workflow_state == "On Hold By Department Head":
                usr_name = frappe.get_doc(
                    "User", doc.cost_center_department_head).full_name
                usr = frappe.utils.get_link_to_form(
                    "User", doc.cost_center_department_head, usr_name)
                doc.add_comment(text="{} has reopened the invoice".format(
                    usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
            if doc.workflow_state == "On Hold By Management":
                usr_name = frappe.get_doc(
                    "User", doc.cost_center_manager).full_name
                usr = frappe.utils.get_link_to_form(
                    "User", doc.cost_center_manager, usr_name)
                doc.add_comment(text="{} has reopened the invoice".format(
                    usr), comment_email=doc.cost_center_manager, comment_by=usr_name)

            newdoc = apply_workflow(doc, action)
            frappe.db.commit()
            return_success_page_custom(newdoc)

            # reset session user
            if logged_in_user == 'Guest':
                frappe.set_user(logged_in_user)

        if action == "Submit":
            # if not verify_request():
            # 	return

            logged_in_user = frappe.session.user
            if logged_in_user == 'Guest' and user:
                # to allow user to apply action without login
                frappe.set_user(user)

            doc = frappe.get_doc(doctype, docname)
            usr_name = frappe.get_doc("User", user).full_name
            usr = frappe.utils.get_link_to_form("User", user, usr_name)
            doc.add_comment(text="{} has submitted the invoice".format(
                usr), comment_email=user, comment_by=usr_name)

            newdoc = apply_workflow(doc, action)
            frappe.db.commit()
            return_success_page_custom(newdoc)

            # reset session user
            if logged_in_user == 'Guest':
                frappe.set_user(logged_in_user)
    else:
        confirm_action_frappe(frappe.local.form_dict.doctype, frappe.local.form_dict.docname,
                              frappe.local.form_dict.user, frappe.local.form_dict.action)


frappe.workflow.doctype.workflow_action.workflow_action.get_common_email_args = get_common_email_args_custom
frappe.workflow.doctype.workflow_action.workflow_action.process_workflow_actions = process_workflow_actions_custom
frappe.workflow.doctype.workflow_action.workflow_action.return_action_confirmation_page = return_action_confirmation_page_custom
frappe.workflow.doctype.workflow_action.workflow_action.return_success_page = return_success_page_custom
