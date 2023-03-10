from . import __version__ as app_version

app_name = "onefinance"
app_title = "OneFinance"
app_publisher = "harish.tanwar@atriina.com"
app_description = "this is onefinance app"
app_email = "harish.tanwar@atriina.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/onefinance/css/onefinance.css"
# app_include_js = "/assets/onefinance/js/onefinance.js"

# include js, css files in header of web template
# web_include_css = "/assets/onefinance/css/onefinance.css"
# web_include_js = "/assets/onefinance/js/onefinance.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "onefinance/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Invoice" : "public/js/purchase_invoice.js",
	"Purchase Order" : "public/js/purchase_order.js",
	"Cost Center" : "public/js/cost_center.js"
	}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "onefinance.utils.jinja_methods",
#	"filters": "onefinance.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "onefinance.install.before_install"
# after_install = "onefinance.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "onefinance.uninstall.before_uninstall"
# after_uninstall = "onefinance.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "onefinance.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
 	"Payment Entry": {
 		"on_submit": "onefinance.utils.on_submit",
# 		"on_cancel": "method",
# 		"on_trash": "method"
	},
	"Vendor": {
		"on_update": "onefinance.utils.on_update_vendor"
	},
	"Purchase Invoice":{
		"before_save":"onefinance.utils.on_update_purchase_invoice"
	},
	#Set Checker Field = session.user
 	"Purchase Order":{
		"before_save":"onefinance.utils.on_update_purchase_order"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron":{"30 09 * * *": ["onefinance.tasks.reminders_at_ten"]},
#	"all": [
#		"onefinance.tasks.all"
#	],
#	"daily": [
#		"onefinance.tasks.daily"
#	],
#	"hourly": [
#		"onefinance.tasks.hourly"
#	],
#	"weekly": [
#		"onefinance.tasks.weekly"
#	],
#	"monthly": [
#		"onefinance.tasks.monthly"
#	],
}

# Testing
# -------

# before_tests = "onefinance.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"frappe.website.doctype.web_form.web_form.accept": "onefinance.web_form.accept",
	"frappe.workflow.doctype.workflow_action.workflow_action.confirm_action" : "onefinance.confirm_action_custom"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "onefinance.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"onefinance.auth.validate"
# ]
