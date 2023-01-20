# Copyright (c) 2023, harish.tanwar@atriina.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import random
from datetime import timedelta

class EmailOTPVerification(Document):
    def before_insert(self):
        self.otp = "".join((random.choice("0123456789") for i in range(4)))
        self.expiry = frappe.utils.now_datetime() + timedelta(minutes=10)
        
