from __future__ import unicode_literals
import frappe

def execute():
    doc = frappe.get_doc('System Settings')
    doc.allow_guests_to_upload_files = 1
    doc.save()
    frappe.db.commit()