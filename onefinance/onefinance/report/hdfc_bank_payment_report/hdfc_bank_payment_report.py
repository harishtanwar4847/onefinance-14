import frappe
from frappe import _
import itertools

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			'fieldname': 'transaction_type',
			'label': _('Transaction Type'),
			'fieldtype': 'data',
			'width':250
		},
		{
			'fieldname': 'beneficiary_code',
			'label': _('Beneficiary Code'),
			'fieldtype': 'Data',
			'width':200
		},
		{
			'fieldname': 'beneficiary_account_number',
			'label': _('Beneficiary Account Number'),
			'fieldtype': 'Data',
			'width':200
		},
		{
			'fieldname' : 'instrument_amount',
			'label' : _('Instrument Amount'),
			'fieldtype' : 'Int',
			'width': 200
		},
		{
			'fieldname' : 'beneficiary_name',
			'label' : _('Beneficiary Name'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname': 'drawee_location',
			'label': _('Drawee Location'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'print_location',
			'label': _('Print Location'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'bene_address_1',
			'label': _('Bene Address 1'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'bene_address_2',
			'label': _('Bene Address 2'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			
			'fieldname':'bene_address_3',
			'label': _('Bene Address 3'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'bene_address_4',
			'label': _('Bene Address 4'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'bene_address_5',
			'label': _('Bene Address 5'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'instruction_reference_number',
			'label': _('Instruction Reference Number'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'customer_reference_number',
			'label': _('Customer Reference Number'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_1',
			'label': _('Payment Details 1'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_2',
			'label': _('Payment Details 2'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_3',
			'label': _('Payment Details 3'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_4',
			'label': _('Payment Details 4'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_5',
			'label': _('Payment Details 5'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_6',
			'label': _('Payment Details 6'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'payment_details_7',
			'label': _('Payment Details 7'),
			'fieldtype' : 'Data',
			'width' : 200
		},
		{
			'fieldname':'cheque_number',
			'label':_('Cheque Number'),
			'fieldtype':'Data',
			'width':200
		},
		{
			'fieldname':'chq_trn_date',
			'label':_('Chq / Trn Date'),
			'fieldtype':'Data',
			'width':200
		},
		{
			'fieldname':'micr_number',
			'label':_('MICR Number'),
			'fieldtype':'Data',
			'width':200
		},
		{
			'fieldname':'ifc_code',
			'label':_('IFC Code'),
			'fieldtype':'Data',
			'width':200
		},
		{
			'fieldname':'bene_bank_name',
			'label':_('Bene Bank Name'),
			'fieldtype':'Data',
			'width':200
		},
		{
			'fieldname':'bene_bank_branch_name',
			'label':_('Bene Bank Branch Name'),
			'fieldtype':'Data',
			'width':200
		},
		{
			'fieldname':'beneficiary_email_id',
			'label':_('Beneficiary Email Id'),
			'fieldtype':'Data',
			'width':200
		},		
	]
	return columns
def get_data(filters):
	return frappe.db.sql(
		"""
		select 
		ba.transaction_type as "Transaction Type",
		ba.beneficiary_code as "Beneficiary Code",
		ba.bank_account_no as "Beneficiary Account Number",
		(CAST(p.outstanding_amount as INT)) as "Instrument amount",
		ba.account_name as "Beneficiary Name",
		null as "Drawee Location",
		null as "Print Location",
		null as "Bene Address 1",
		null as "Bene Address 2",
		null as "Bene Address 3",
		null as "Bene Address 4",
		null as "Bene Address 5",
		p.bill_no as "Instruction Reference Number",
		p.bill_no as "Customer Reference Number",
		null as "Payment details 1",
		null as "Payment details 2",
		null as "Payment details 3",
		null as "Payment details 4",
		null as "Payment details 5",
		null as "Payment details 6",
		null as "Payment details 7",
		null as "Cheque Number",
		date_format(CURDATE(), "%%d/%%m/%%Y") as "Chq / Trn Date",
		null as "MICR Number",
		ba.branch_code as "IFC Code",
		ba.bank as "Bene Bank Name",
		ba.branch_name as "Bene Bank Branch Name",
		ba.beneficiary_email_id as "Beneficiary email id"
		from `tabPurchase Invoice` p join `tabBank Account` ba on p.supplier = ba.party {conditions} and p.outstanding_amount !=0
		group by p.name;
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