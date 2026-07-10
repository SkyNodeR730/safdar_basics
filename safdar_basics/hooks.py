app_name = "safdar_basics"
app_title = "Safdar Basics"
app_publisher = "Safar Ali"
app_description = "for customizations"
app_email = "safdar211@gmail.com"
app_license = "mit"

fixtures = ["Custom Field"]

doc_events = {
    "Sales Invoice": {
        "validate": "safdar_basics.overrides.tax_on_price_list_rate.validate",
        "before_save":"safdar_basics.overrides.calculate_fields.before_save",
        "before_save": "safdar_basics.overrides.sales_invoice.set_sales_invoice_ref_on_sales_order",
        "on_cancel": "safdar_basics.overrides.sales_invoice.clear_sales_invoice_ref_on_sales_order"
    },
    "Sales Order": {
        "validate": "safdar_basics.overrides.tax_on_price_list_rate.validate",
    },
    "Delivery Note": {
        "validate": "safdar_basics.overrides.tax_on_price_list_rate.validate",
    },
    "Purchase Order": {
        "validate": "safdar_basics.overrides.tax_on_price_list_rate.validate",
    },
    "Purchase Receipt": {
        "validate": "safdar_basics.overrides.tax_on_price_list_rate.validate",
    },
    "Purchase Invoice": {
        "validate": "safdar_basics.overrides.tax_on_price_list_rate.validate",
    },
    "Customer": {
        "before_save": "safdar_basics.overrides.set_sales_person.before_save",
    },
    "Payment Entry": {
        "before_save": "safdar_basics.overrides.set_sales_person_from_customer.set_sales_person_from_customer",
    },
}

regional_overrides = {
    "Pakistan": {
        "erpnext.controllers.taxes_and_totals.get_itemised_tax_breakup_data": "safdar_basics.overrides.tax_on_price_list_rate.get_itemised_tax_breakup_data"
    }
}

# Landing page as website home
home_page = "index"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "safdar_basics",
# 		"logo": "/assets/safdar_basics/logo.png",
# 		"title": "Safdar Basics",
# 		"route": "/safdar_basics",
# 		"has_permission": "safdar_basics.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/safdar_basics/css/safdar_basics.css"
# app_include_js = "/assets/safdar_basics/js/safdar_basics.js"

# include js, css files in header of web template
# web_include_css = "/assets/safdar_basics/css/safdar_basics.css"
# web_include_js = "/assets/safdar_basics/js/safdar_basics.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "safdar_basics/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"Payment Entry" : "public/js/payment_entry.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "safdar_basics/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "safdar_basics.utils.jinja_methods",
# 	"filters": "safdar_basics.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "safdar_basics.install.before_install"
# after_install = "safdar_basics.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "safdar_basics.uninstall.before_uninstall"
# after_uninstall = "safdar_basics.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "safdar_basics.utils.before_app_install"
# after_app_install = "safdar_basics.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "safdar_basics.utils.before_app_uninstall"
# after_app_uninstall = "safdar_basics.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "safdar_basics.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"safdar_basics.tasks.all"
# 	],
# 	"daily": [
# 		"safdar_basics.tasks.daily"
# 	],
# 	"hourly": [
# 		"safdar_basics.tasks.hourly"
# 	],
# 	"weekly": [
# 		"safdar_basics.tasks.weekly"
# 	],
# 	"monthly": [
# 		"safdar_basics.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "safdar_basics.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "safdar_basics.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "safdar_basics.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["safdar_basics.utils.before_request"]
# after_request = ["safdar_basics.utils.after_request"]

# Job Events
# ----------
# before_job = ["safdar_basics.utils.before_job"]
# after_job = ["safdar_basics.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"safdar_basics.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

