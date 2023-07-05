__version__ = '1.0.2'


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


def get_common_email_args_custom(doc, attachments=None):
    doctype = doc.get('doctype')
    docname = doc.get('name')
    print("Doc", doc)
    if doctype == "Purchase Invoice":
        if doc.workflow_state == "Approval Pending" or doc.workflow_state == "Approved" or doc.workflow_state == "On Hold By Department Head" or doc.workflow_state == "Management Approval Pending" or doc.workflow_state == "Approved By Management" or doc.workflow_state == "Rejected" or doc.workflow_state == "Rejected By Management" or doc.workflow_state == "On Hold By Management":
            message1 = """<b>{0} : {1}</b><br><br>""".format(doctype, docname)
            if doc.workflow_state == "Approved" or doc.workflow_state == "Management Approval Pending":
                var = frappe.get_doc(
                    "User", doc.cost_center_department_head).full_name
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

    # Purchase Order
    if doctype == "Purchase Order":
        if doc.workflow_state == "Approval Pending" or doc.workflow_state == "Approved" or doc.workflow_state == "On Hold By Department Head" or doc.workflow_state == "Management Approval Pending" or doc.workflow_state == "Approved By Management" or doc.workflow_state == "Rejected" or doc.workflow_state == "Rejected By Management" or doc.workflow_state == "On Hold By Management":
            message1 = """<b>{0} : {1}</b><br><br>""".format(doctype, docname)
            if doc.workflow_state == "Approved" or doc.workflow_state == "Management Approval Pending":
                var = frappe.get_doc(
                    "User", doc.cost_center_department_head).full_name
                message2 = """<b>Approved By :</b> {}<br><br>""".format(var)
            else:
                message2 = """<br>"""
            message3 = """<b>Details of Purchase Order</b>:<br><br>"""
            message4 = """<table border="1" cellspacing="0" cellpadding="5" align="" style=text-align:center>
						<tr><th>Party Name</th><th>Amount</th><th>Description</th></tr>
						"""
            for item in doc.items:
                message4 += "<tr><td>"+doc.supplier + "</td><td>" + str(item.amount) + "</td><td>" + item.description + "</td><tr>"
            message4 += "</table><br>* The above amount is exclusive of GST and TDS.<br><br>"

            attachments = frappe.get_all('File', filters={
                                         'attached_to_doctype': 'Purchase Order', 'attached_to_name': doc.name}, fields=['file_name', 'file_url'])
            if attachments:
                message6 = """<b>Attachments</b> : <ul>"""
                for attachment in attachments:
                    message6 += """<li><a href="{}">{}</a></li>""".format(
                        attachment.file_url, attachment.file_name)
                message6 += """</ul><br>"""
            else:
                message6 = """<br>"""

            messageFinal = message1 + message2 + message3 + message4 + message6

            email_template = get_email_template(doc)
            if email_template:
                subject = frappe.render_template(
                    email_template.subject, vars(doc))
                response = frappe.render_template(
                    email_template.response, vars(doc))
            else:
                subject = _('PURCHASE ORDER APPROVAL')
                response = _(messageFinal)

            common_args = {
                'template': 'workflow_action',
                'header': 'PURCHASE ORDER APPROVAL',
                'attachments': [],
                'subject': subject,
                'message': response
            }
            return common_args
    
    # Purchase Order Message End


def send_workflow_action_email_custom(users_data, doc):
    print("send", doc.doctype)
    print("##############")
    common_args = get_common_email_args_custom(doc)
    if doc.workflow_state == "Approval Pending" or doc.workflow_state == "On Hold By Department Head":
        message = common_args.pop('message', None)
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
        print("###############################3")
        message = common_args.pop('message', None)
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
        print("###############################3")

        message = common_args.pop('message', None)
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
        if workflow == "Purchase Invoice Workflow" or "Purchase Order Workflow":
            enqueue(send_workflow_action_email_custom, queue='short',
                    users_data=list(user_data_map.values()), doc=doc)
        else:
            enqueue(send_workflow_action_email, queue='short',
                    users_data=list(user_data_map.values()), doc=doc)
    # Purchase Order
    # Purchase Order Handling End


def return_action_confirmation_page_custom(doc, action, action_link, alert_doc_change=False):
    doctype = doc.get('doctype')
    docname = doc.get('name')
    print("Doc", doc)
    if doctype == "Purchase Invoice" or doctype == "Purchase Order":
        template_params = {
            'title': doc.get('name'),
            'doctype': doc.get('doctype'),
            'docname': doc.get('name'),
            'action': action,
            'action_link': action_link,
            'alert_doc_change': alert_doc_change
        }

        frappe.respond_as_web_page(title=None,
                                   html=None,
                                   indicator_color='blue',
                                   template='confirm_action_custom',
                                   context=template_params)

    else:
        return_action_confirmation_page_frappe(
            doc, action, action_link, alert_doc_change=False)


def return_success_page_custom(doc):
    if doc.get('doctype') == "Purchase Invoice":
        if get_doc_workflow_state(doc) == "Approved" or get_doc_workflow_state(doc) == "Approval Pending" or get_doc_workflow_state(doc) == "Management Approval Pending" or get_doc_workflow_state(doc) == "Approved By Management" or get_doc_workflow_state(doc) == "Submitted":
            frappe.respond_as_web_page(_("Success"),
                                       _("""<div align="center"><b>Thank you!</b><br><br><img src="https://w7.pngwing.com/pngs/179/1015/png-transparent-computer-icons-check-mark-adobe-acrobat-green-tick-trademark-logo-grass.png" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')
        if get_doc_workflow_state(doc) == "Rejected" or get_doc_workflow_state(doc) == "Rejected By Management":
            frappe.respond_as_web_page(_("Success"),
                                       _("""<div align="center"><b>You have rejected the invoice</b><br><br><img src="https://w7.pngwing.com/pngs/175/854/png-transparent-computer-icons-button-check-mark-cross-red-cross-photography-trademark-logo.png" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')

        if get_doc_workflow_state(doc) == "On Hold By Department Head" or get_doc_workflow_state(doc) == "On Hold By Management":
            print("hjjjjjjjjjjjj")
            frappe.respond_as_web_page(_("Success"),
                                       _("""<div align="center"><b>The invoice has been kept on hold</b><br><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmNCSC6w0QhhDMF7fYsIlhP6NwcmicMzA5zg&usqp=CAU" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')
            print("hjjjjjjjjjj")
    elif doc.get('doctype') == "Purchase Order":
        if get_doc_workflow_state(doc) == "Approved" or get_doc_workflow_state(doc) == "Approval Pending" or get_doc_workflow_state(doc) == "Management Approval Pending" or get_doc_workflow_state(doc) == "Approved By Management" or get_doc_workflow_state(doc) == "Submitted":
            frappe.respond_as_web_page(_("Success"),
                                       _("""<div align="center"><b>Thank you!</b><br><br><img src="https://w7.pngwing.com/pngs/179/1015/png-transparent-computer-icons-check-mark-adobe-acrobat-green-tick-trademark-logo-grass.png" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')
        if get_doc_workflow_state(doc) == "Rejected" or get_doc_workflow_state(doc) == "Rejected By Management":
            frappe.respond_as_web_page(_("Success"),
                                       _("""<div align="center"><b>You have rejected the purchase order</b><br><br><img src="https://w7.pngwing.com/pngs/175/854/png-transparent-computer-icons-button-check-mark-cross-red-cross-photography-trademark-logo.png" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')

        if get_doc_workflow_state(doc) == "On Hold By Department Head" or get_doc_workflow_state(doc) == "On Hold By Management":
            frappe.respond_as_web_page(_("Success"),
                                       _("""<div align="center"><b>The purchase order has been kept on hold</b><br><br><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmNCSC6w0QhhDMF7fYsIlhP6NwcmicMzA5zg&usqp=CAU" alt="Thank You!" width="100" height="200"></div><script>setTimeout("window.close()", 2000)</script>"""), indicator_color='green')

    else:
        return_success_page_frappe(doc)


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

    if frappe.local.form_dict.doctype == "Purchase Order":
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
                    doc.add_comment(text="{} has kept the purchase order on Hold".format(
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
                    doc.add_comment(text="{} has kept the purchase order on Hold".format(
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
                    doc.add_comment(text="{} has rejected the purchase order".format(
                        usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
                    doc.reason_of_rejection = reason_reject
                    doc.save()

                if doc.workflow_state == "Management Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_manager).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_manager, usr_name)
                    doc.add_comment(text="{} has rejected the purchase order".format(
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
                    doc.add_comment(text="{} has approved the purchase order".format(
                        usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
                if doc.workflow_state == "Management Approval Pending":
                    usr_name = frappe.get_doc(
                        "User", doc.cost_center_manager).full_name
                    usr = frappe.utils.get_link_to_form(
                        "User", doc.cost_center_manager, usr_name)
                    doc.add_comment(text="{} has approved the purchase order".format(
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
                doc.add_comment(text="{} has reopened the purchase order".format(
                    usr), comment_email=doc.cost_center_department_head, comment_by=usr_name)
            if doc.workflow_state == "On Hold By Management":
                usr_name = frappe.get_doc(
                    "User", doc.cost_center_manager).full_name
                usr = frappe.utils.get_link_to_form(
                    "User", doc.cost_center_manager, usr_name)
                doc.add_comment(text="{} has reopened the purchase order".format(
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
            doc.add_comment(text="{} has submitted the purchase order".format(
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

@frappe.whitelist(allow_guest=True)
def collection_webhook_test(**kwargs):
    try:
        log = {
            "request": frappe.local.form_dict,
            "headers": {k: v for k, v in frappe.local.request.headers.items()},
        }
        create_log(log, file_name="collection_webhook")

    except Exception:
        frappe.log_error(
            message=frappe.get_traceback()
            + "\n\nLog details -\n{}".format(str(frappe.local.form_dict)),
            title="Collection Webhook",
        )

def create_log(log, file_name):
    try:
        log_file = frappe.utils.get_files_path("{}.json".format(file_name))
        logs = None
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                logs = f.read()
            f.close()
        logs = json.loads(logs or "[]")
        log["req_time"] = str(frappe.utils.now_datetime())
        logs.append(log)
        with open(log_file, "w") as f:
            f.write(json.dumps(logs))
        f.close()
    except json.decoder.JSONDecodeError:
        log_text_file = (
            log_file.replace(".json", "") + str(frappe.utils.now_datetime()) + ".txt"
        ).replace(" ", "-")
        with open(log_text_file, "w") as txt_f:
            txt_f.write(logs + "\nLast Log \n" + str(log))
        txt_f.close()
        os.remove(log_file)
        frappe.log_error(
            message=frappe.get_traceback()
            + "\n\nFile name -\n{}\n\nLog details -\n{}".format(file_name, str(log)),
            title="Create Log JSONDecodeError",
        )
    except Exception as e:
        frappe.log_error(
            message=frappe.get_traceback()
            + "\n\nFile name -\n{}\n\nLog details -\n{}".format(file_name, str(log)),
            title="Create Log Error",
        )

class APIException(Exception):
	"""
	Base Exception for API Requests

	Usage:
	try:
		...
	except APIException as e:
		return e.respond()
	"""

	http_status_code = 500
	message = frappe._('Something went Wrong')
	save_error_log = True
	errors = {}
	
	def __init__(self, message=None, errors=None):
		if message:
			self.message = message
		if errors:
			self.errors = errors

	def respond(self):
		if self.save_error_log:
			frappe.log_error()
		return respond(status=self.http_status_code, message=self.message, errors=self.errors)


class MethodNotAllowedException(APIException):
	http_status_code = 405
	message = frappe._('Method not allowed')
	save_error_log = False


class ValidationException(APIException):
	http_status_code = 422
	message = frappe._('Validation Error')
	save_error_log = False

	def __init__(self, errors, data=None):
		errors_ = dict()
		for key in errors.keys():
			# getting first error message
			errors_[key] = list(errors[key].values())[0]
		self.errors = errors_
		self.data = data

import json
from frappe.auth import CookieManager

def respond(status=200, message='Success', data={}, errors={}):
	response = frappe._dict({'message': frappe._(message)})
	if data:
		response['data'] = data
	if errors:
		response['errors'] = errors
	frappe.local.response = response
	frappe.local.response['http_status_code'] = status

	frappe.local.cookie_manager = CookieManager()
	frappe.local.cookie_manager.flush_cookies(response=frappe.local.response)
	# return Response(response=json.dumps(response), status=status, content_type='application/json')

def respondWithSuccess(status=200, message='Success', data={}):
	return respond(status=status, message=message, data=data)

def respondWithFailure(status=500, message='Something went wrong', data={}, errors={}):
	return respond(status=status, message=message, data=data, errors=errors)

def respondUnauthorized(status=401, message='Unauthorized'):
	return respond(status=status, message=message)

def respondForbidden(status=403, message='Forbidden'):
	return respond(status=status, message=message)

def respondNotFound(status=404, message='Not Found'):
	return respond(status=status, message=message)

@frappe.whitelist(allow_guest=True)
def collection_webhook():
	try:
		log = {
			"request": frappe.local.form_dict,
			"headers": {k: v for k, v in frappe.local.request.headers.items()},
		}
		create_log(log, file_name="collection_webhook")
		request_dict = frappe.local.form_dict.get("GenericCorporateAlertRequest")
		request_keys = (request_dict.keys() >= {'Alert Sequence No', 'BenefDetails2', 'Debit/Credit', 'Amount', 'Remitter Name', 'Remitter Account', 'Remitter Bank', 'RemitterIFSC', 'ChequeNo', 'User Reference Number', 'Mnemonic Code', 'TransactionDescription', 'Transaction Date'})
		print(request_keys)
		frappe.session.user = "Administrator"

		# if request_keys:
		request_sequence_no = request_dict.get("Alert Sequence No")
		# sequence_no = frappe.db.sql("""select count(alert_sequence_no) from `tabPayment Entry` where alert_sequence_no = %s""",request_sequence_no)
		sequence_no = frappe.db.get_value("Payment Entry", {"alert_sequence_no": request_sequence_no}, "name")

		print(sequence_no)
		if not sequence_no:
			pe = frappe.new_doc("Payment Entry")
			pe.payment_type = "Pay"
			pe.party_type = "Supplier"
			pe.party = "Atrina Technologies Pvt. Ltd."
			pe.party_name = "Atrina Technologies Pvt. Ltd."
			pe.paid_from = "HDFC Bank Current A/C 5504 - 1F"
			pe.paid_amount = float(request_dict.get("Amount"))
			pe.received_amount = float(request_dict.get("Amount"))
			pe.reference_no = "1234"
			pe.reference_date = datetime.strptime("20-04-2023", '%d-%m-%Y')
			pe.alert_sequence_no = request_dict.get("Alert Sequence No")
			pe.save()
			frappe.db.commit()
			data = {"GenericCorporateAlertResponse":{"errorCode":"0","errorMessage": "Success","domainReferenceNo":request_dict.get("Alert Sequence No")}}

			return respondWithSuccess(message="Success", data = data)

		else:
			data = {"GenericCorporateAlertResponse":{"errorCode":"0","errorMessage": "Duplicate","domainReferenceNo":request_dict.get("Alert Sequence No")}}
			return respondWithFailure(message="Duplicate", data = data, status = 422)
		# else:
		# 	data = {"GenericCorporateAlertResponse":{"errorCode":"1","errorMessage": "Technical Reject","domainReferenceNo":request_dict.get("Alert Sequence No")}}
		# 	return respondWithFailure(message="Technical Reject", data = data, status = 400)
	
        # utils.validator.validate_http_method("POST")

	except APIException as e:
		frappe.log_error()
		return e.respond()
