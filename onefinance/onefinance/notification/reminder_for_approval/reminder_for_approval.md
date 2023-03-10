The below-mention payment approval is pending. Request you to take the required action.
<table border="1" cellspacing="0" cellpadding="5" align="">
<th>S. No.</th>
<th>Purchase Invoice ID</th>
<th>Party Name</th>
<th>Amount</th>
<th>Description</th>
{% for j in doc.leads %}
<tr>
<td>{{loop.index}}</td>
<td>{{j[0]}}</td>
<td>{{j[1]}}</td>
<td>{% set var = frappe.get_doc("Purchase Invoice",j[0]) %} {% for item in var.get("items") %} {{item.amount}} {% endfor %}</td>
<td>{% set var = frappe.get_doc("Purchase Invoice",j[0]) %} {% for item in var.get("items") %} {{item.description}} {% endfor %}</td>
</tr>
{% endfor %}
</table><br><br>

The link for approval of payment is {{frappe.get_url()}}/app/purchase-invoice<br>
In case of any queries, you can contact below.<br>
Email: accounts@1finance.co.in<br><br>