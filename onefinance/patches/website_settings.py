from __future__ import unicode_literals
import frappe

def execute():
    doc = frappe.get_doc('Website Settings')
    doc.append('top_bar_items', {
        'label' : 'Request for Vendor Registration',
        'url' : '/email-verification',
        'right' : 1
    })
    doc.save()
    frappe.db.commit()