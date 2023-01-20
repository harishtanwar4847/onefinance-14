import click
import frappe

def execute():
    hostname = click.prompt('Please enter hostname', type=str)
    site_name = frappe.utils.get_site_base_path().replace("./", "")
    frappe.commands.popen("bench --site {} set-config hostname {}".format(site_name,hostname))
