frappe.ready(function () {
	
	// frappe.web_form.after_load = () => {
	// 	setTimeout(function() {
	// 		if(!frappe.web_form.doc.email_address || !frappe.web_form.doc.otp) {
	// 			frappe.msgprint({indicator: 'red', title: 'Error', message: 'Your OTP is not verified!'})
	// 			setTimeout(function() {
	// 				location.href = '/'
	// 			}, 5000)
	// 			return
	// 		}
	// 		frappe.msgprint('Please fill all the Details Carefully');
	// 	}, 500)
	// },

	// frappe.web_form.on('gst_status', (field, value) => {
	// 	params = "Declaration of GST Non-Enrollment <br><br>Sub: Declaration regarding non-requirement to be registered and/or not applicable under the Central / State/ UT/ Integrated Goods and Services Tax Act, 2017 <br><br>I/We do hereby state that I/We am/are not liable to registration under the provisions of Goods and Service Tax Act as (please 🗹 and fill below for the relevant reason) <br><br>I/We deal in to the category of goods or services ………. (Nature of goods / services) which are exempted under the Goods and Service Tax Act, 2017 <br><br>I/We have the turnover below the taxable limit as specified under the Goods and Services Tax Act, 2017 <br><br>I/We are yet to register ourselves under the Goods and Service Tax Act, 2017 I/We declare that as soon as our value of turnover exceeds Rs. 20 Lacs or during any financial year <br><br>I/we decide or require or become liable to register under the GST, I/we undertake to provide all the requisite documents and information to you. I/We shall get ourselves registered with the Goods and Services Tax department and give our GSTN to your company. <br><br>I/We request you to consider this communication as a declaration for not requiring to be registered under the Goods and Service Tax Act, 2017. <br><br>I/We hereby also confirm that 1 Finance Private Limited shall not be liable for any loss accrued to me/us, due to any registration default with the GST."
	// 	if (value == "Unregistered") {
	// 		frappe.web_form.set_value("declaration_of_gst_non_enrollment", params)
	// 	}
	// });

	frappe.web_form.validate_section = () => {
		//After load Working Perfectly In Desk Client Script.

		// frappe.web_form.doc.validate = () => {
		var gst_pattern = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$";
		var mobile_pattern = "^[0-9]{10}$";
		var pin_pattern = "^[1-9][0-9]{5}$";
		var pan_pattern = "[A-Z]{5}[0-9]{4}[A-Z]{1}";
		// var number_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

		//Getting Web Form Values.
		var post_code = frappe.web_form.get_value('postal_code')
		var mobile_number = frappe.web_form.get_value('mobile_number')
		// var mobile_number = frappe.web_form.doc.mobile_number  //Doest Work
		var pan_number = frappe.web_form.get_value('pan_number')
		var gst_number = frappe.web_form.get_value('gst_number')
		var pan_card_copy = frappe.web_form.get_value('pan_card_copy')

		// (Breaks the execution of next button(written in desk)so that ui will throw mandatory fields required error)
		let fields = ['company_name', 'address', 'country', 'state', 'website', 'contact_person_designation', 'contact_person_name', 'pan_card_copy']

		for (let i = 0; i < fields.length; i++) {
			if (frappe.web_form.get_value(fields[i]) == "" || frappe.web_form.get_value(fields[i]) == null) {
				frappe.throw()
				return false;
			}
		}

		//Adding Validation.
		if (!post_code.match(pin_pattern)) {
			// frappe.throw('Enter Correct Pin') // Not breaking the execution
			frappe.msgprint({
				title: 'Validation Error',
				indicator: 'red',
				message: 'Please Enter Correct Pin Code'
			})
			return false;
		}

		if (!mobile_number.match(mobile_pattern)) {
			frappe.msgprint({
				title: 'Validation Error',
				indicator: 'red',
				message: 'Please Enter Correct Phone Number'
			})
			return false;
		}
		if (!pan_number.match(pan_pattern)) {
			frappe.msgprint({
				title: 'Validation Error',
				indicator: 'red',
				message: 'Please Enter Valid Pan Card Number'
			})
			return false;
		}
		if (gst_number && !gst_number.match(gst_pattern)) {
			frappe.msgprint({
				title: 'Validation Error',
				indicator: 'red',
				message: 'Enter Valid GST Number'
			})
			return false;
		}

		else {
			return true;
		}
	}
})