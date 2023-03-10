# -*- coding: utf-8 -*-
# Copyright (c) 2021, Atrina Technologies Pvt Ltd and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Vendor(Document):
    def before_insert(self): 
        pass       
        # if frappe.get_all('Vendor', filters={'email_address': self.email_address, 'otp': self.otp}):
        #     frappe.throw('Your Information is already Submitted')  
        # if not frappe.get_all('Email OTP Verification', filters={'email': self.email_address, 'otp': self.otp, 'used': 0}):
        #     frappe.throw('Your OTP and Email are not Correct')

    def after_insert(self):
        frappe.db.sql('UPDATE `tabEmail OTP Verification` SET used = 1 WHERE email = %s AND otp = %s', (self.email_address, self.otp))
