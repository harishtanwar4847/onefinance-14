Hello {% set var = frappe.get_doc('User', doc.checker) %} {{var.full_name}}, <br><br>
The below-mention payment approval is being Rejected.<br>
Reason : {{doc.reason_of_rejection}}
<table border="1" cellspacing="0" cellpadding="5" align="">
<th>Party Name</th>
<th>Invoice No.</th>
<th>Invoice Date</th>
<th>Amount</th>
<th>Description</th>
{% for i in doc.items %}
<tr>
<td>{{doc.supplier}}</td>
<td>{{doc.bill_no}}</td>
<td>{{doc.bill_date}}</td>
<td>{{i.amount}}</td>
<td>{{i.description}}</td>
</tr>
{% endfor %}
</table><br><br>