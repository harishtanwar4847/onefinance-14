import frappe
import requests

def get_context(context):
	# do your magic here
	pass
	# print(context.pan_number)


# @frappe.whitelist(allow_guest = True)
# def pan_api(pan):
# 	print("Hello")
# 	url = "https://api.digio.in/v3/client/kyc/fetch_id_data/PAN"
# 	headers = {
# 		"Authorization": "Basic QUlTRUFBV0s4OFU5STVSRFZTQ1pHTUdFOVVPMU9YVEw6UzQxWlhXOVlOU041WkFJVU5GWDNSREtNMUY3TUdITkI=",
# 	}
# 	data = {
# 		"id_no": pan,
# 	}

# 	response = requests.post(url, headers=headers, json=data)
# 	response.raise_for_status()
# 	print(response.text)

# 	return response.text

