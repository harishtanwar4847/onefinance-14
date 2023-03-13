import frappe
from frappe import _
import itertools

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname': 'gcif_id',
			'label': _('GCIF ID'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'bene_id',
			'label': _('Bene Id'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'bene_name',
			'label': _('Bene Name'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'address_line_1',
			'label': _('Address Line 1'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'address_line_2',
			'label': _('Address Line 3'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'address_line_3',
			'label': _('Address Line 3'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'city',
			'label': _('City'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'state',
			'label': _('State'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'country',
			'label': _('Country'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'pin_code',
			'label': _('Pin Code'),
			'fieldtype': 'Int',
			'width':250
		},
		{
			'fieldname': 'email_id',
			'label': _('Email Id'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'Mobile No',
			'label': _('Mobile No'),
			'fieldtype': 'Int',
			'width':250
		},
		{
			'fieldname': 'daily_cumulative_limit',
			'label': _('Daily Cumulative Limit'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'payment_product',
			'label': _('Payment Product'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'account_number',
			'label': _('Account Number'),
			'fieldtype': 'Int',
			'width':250
		},
		{
			'fieldname': 'nre',
			'label': _('NRE'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'default',
			'label': _('Default'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'ifsc_code',
			'label': _('IFSC Code'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'bank_name',
			'label': _('Bank Name'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'branch_name',
			'label': _('Branch Name'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'txn_limit',
			'label': _('Txn Limit'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'bene_lei_code',
			'label': _('Bene LEI Code'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'lei_code_expiry_date',
			'label': _('LEI Code Expiry Date'),
			'fieldtype': 'Date',
			'width':250
		},
		{
			'fieldname': 'bene_details_change',
			'label': _('Bene Details Change'),
			'fieldtype': 'Data',
			'width':250
		},
		{
			'fieldname': 'product_account_no_change',
			'label': _('Product Account No Change'),
			'fieldtype': 'Data',
			'width':250
		}
	]
	return columns
def get_data(filters):
	return frappe.db.sql(
		"""
		select 
		ba.gcif_id as "GCIF ID",
		ba.account_name as "Bene Id",
		ba.account_name as "Bene Name",
		(select a.address_line1 from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "Address Line 1",
		(select a.address_line2 from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "Address Line 2",
		(select a.address_line_3 from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "Address Line 3",
		(select city from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "City",
		(select state from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "State",
		(select country from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "Country",
		(select pincode from `tabAddress` a join `tabDynamic Link` d where d.parent = a.name and d.link_name = p.supplier) as "Pin Code",
		ba.beneficiary_email_id as "Email Id",
		(select max(cp.phone) from `tabContact Phone` cp join `tabDynamic Link` d where cp.parent = d.parent and d.link_name = p.supplier) as "Mobile No",
		dc.daily_cumulative_limit as "Daily Cumulative Limit",
		dc.payment_product as "Payment Product",
		ba.bank_account_no as "Account Number",
		ba.nre as "NRE",
		ba.default as "Default",
		ba.branch_code as "IFSC Code",
		ba.bank as "Bank Name",
		ba.branch_name as "Branch Name",
		dc.txn_limit as "Txn Limit",
		null as "Bene LEI Code",
		null as "LEI Code Expiry Date",
		'A' as "Bene Details Change",
		'A' as "Product-Account No Change"
		from `tabPurchase Invoice` p join `tabBank Account` ba on p.supplier = ba.party{conditions} join `tabPayment Product Limit` dc on ba.name=dc.parent group by dc.payment_product,ba.name order by p.name
		""".format(conditions=get_conditions(filters)),filters)
	
def get_conditions(filters):
	conditions = []

	if filters.get("supplier"):
		conditions.append(" and p.supplier=%(supplier)s")

	if filters.get("posting_date"):
		conditions.append(" and p.posting_date=%(posting_date)s")

	if filters.get("cost_center"):
		conditions.append(" and p.cost_center=%(cost_center)s")

	return " ".join(conditions) if conditions else ""