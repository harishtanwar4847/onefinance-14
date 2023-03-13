frappe.listview_settings['Purchase Invoice'] = {
    onload(listview) {
        var route_options = {}
        if(frappe.user_roles.includes('System Manager'))
        {
            route_options = {
                "workflow_state": ["in", "Approval Pending, Management Approval Pending, On Hold By Department Head, On Hold By Management"]
            };
        }

        if(frappe.user_roles.includes('Department Head') && frappe.user_roles.includes('Exco'))
        {
            route_options = {
                "workflow_state": ["in", "Approval Pending, Management Approval Pending, On Hold By Department Head, On Hold By Management"],
            };
        }

        if(frappe.user_roles.includes('Department Head') && !frappe.user_roles.includes('System Manager') && !frappe.user_roles.includes('Exco'))
        {
            route_options = {
                "workflow_state": ["in", "Approval Pending, On Hold By Department Head"],
                "cost_center_department_head": ["=", frappe.session.user]
            };
        }

        if(frappe.user_roles.includes('Exco') && !frappe.user_roles.includes('System Manager') && !frappe.user_roles.includes('Department Head'))
        {
            route_options = {
                "workflow_state": ["in", "Management Approval Pending, On Hold By Management"],
                "cost_center_manager": ["=", frappe.session.user]
            };
        }
        frappe.route_options = route_options
        
	}
}