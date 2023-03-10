frappe.ready(function() {
	// bind events here
	frappe.web_form.validate = () => {
        var email = frappe.web_form.get_values().email
        var email_pattern = /(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/; 
         if(!email.match(email_pattern))
        {
            frappe.msgprint('Enter Valid Email.')
            return false;
        }
        else{
        return true;
        }


}

frappe.web_form.handle_success = () => {
    frappe.msgprint({
        title: __('Success'),
        message: __('Your OTP has been sent on your email!'),
        primary_action: {
            label: 'Proceed',
            action: function() {
                window.location = frappe.web_form.success_url + '/new?new=1&email=' + frappe.web_form.doc.email
            }
        }
    });
    
}
})