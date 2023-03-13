// Copyright (c) 2016, Atrina and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["HDFC Bank Payment Report"] = {
	get_datatable_options(options) {
		return Object.assign(options, {
			checkboxColumn: true,
		});
	},
	onload: function(report) {
	    report.page.add_inner_button(__("Download Selected Records"), function() {
			let checked_rows_indexes = report.datatable.rowmanager.getCheckedRows();
			let checked_rows = checked_rows_indexes.map(i => report.data[i]);
			var checked_list = []

			for (let i = 0; i < checked_rows.length; i++) {
				checked_list.push(Object.values(checked_rows[i]));
			}
			
			var csv = [];  
			if (checked_list.length>=1){
				checked_list.forEach(function(row) {  
						csv += row.join(',');  
						csv += "\n";  
				}); 
				document.write(csv);  
			}
			else{
				frappe.throw("Please select rows first")
			}
  
     
			var hiddenElement = document.createElement('a');  
			hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);  
			hiddenElement.target = '_blank';  
			hiddenElement.download = 'HDFC Bank Payment Report.csv';  
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
			"fieldtype": "Date"
		},
		{
			"fieldname":"cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
		}
		
	]
};