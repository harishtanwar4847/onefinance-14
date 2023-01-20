Hello Vendor,<br><br>

Please find your OTP for Vendor Registration with 1 Finance {{ doc.otp }} .<br><br>

You can <a href="{{frappe.utils.get_url('/email-otp-verification?new=1&email={}&otp={}'.format(doc.email,doc.otp))}}">click here</a> to Verify Your Email!