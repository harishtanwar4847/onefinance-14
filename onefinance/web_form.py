import frappe
from frappe.rate_limiter import rate_limit
import json
from frappe.website.doctype.web_form.web_form import accept as web_form_accept

@frappe.whitelist(allow_guest=True)
#@rate_limit(key='web_form', limit=5, seconds=60, methods=['POST'])
def accept(web_form, data, docname=None, for_payment=False):
    '''Save the web form'''
    if web_form == 'email-otp-verification':
        data = frappe._dict(json.loads(data))
        if frappe.get_all(data.doctype, filters={'email': data.email, 'otp': data.otp, 'used': 0, 'expiry': ['>=', frappe.utils.now_datetime()] }):
            return {}
        if frappe.get_all(data.doctype, filters={'email': data.email, 'otp': data.otp, 'used': 0, 'expiry': ['<=', frappe.utils.now_datetime()] }):
            frappe.throw('Your OTP has been Expired, Please retry the Registration process')
        else:
            frappe.throw('Invalid OTP, Please enter valid OTP')
    else:
        web_form_accept(web_form, data, docname, for_payment)
        