from __future__ import unicode_literals
import frappe

def execute():
    doc = frappe.get_doc('GST Settings')
    doc.enable_overseas_transactions = 1
    doc.save()
    frappe.db.commit()