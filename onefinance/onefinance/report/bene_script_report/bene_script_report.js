// Copyright (c) 2016, Atrina and contributors
// For license information, please see license.txt
/* eslint-disable */



frappe.query_reports["Bene Script Report"] = {
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},
	onload: function(report) {
	    report.page.add_inner_button(__("Download Selected Records"), function() {
			let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
			let checked_rows = checked_rows_indexes.map(i => report.data[i]);
			console.log(checked_rows[0])
			var checked_list = []

			for (let i = 0; i < checked_rows.length; i++) {
				checked_list.push(Object.values(checked_rows[i]));
			}
			console.log(checked_list)
			
			var csv = [];  
      
			checked_list.forEach(function(row) {  
					csv += row.join(',');  
					csv += "\n";  
			}); 
			document.write(csv);  
  
     
			var hiddenElement = document.createElement('a');  
			hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);  
			hiddenElement.target = '_blank';  
			hiddenElement.download = 'Bene Report.csv';  
			hiddenElement.click(); 
			location.reload()  
			
		});
    },
	"filters": [
		{
			"fieldname":"supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
		},
		{
			"fieldname":"posting_date",
			"label": __("Posting Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
		}

	]
};