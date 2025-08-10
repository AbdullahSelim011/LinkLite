import frappe

def after_install():
    create_link_manager_role()

def create_link_manager_role():
	"""Create Link Manager role if it does not exist."""
	if not frappe.db.exists("Role", "Link Manager"):
		role = frappe.get_doc({
			"doctype": "Role",
			"role_name": "Link Manager",
			"desk_access": 0,
		})
		role.insert()
		frappe.db.commit()
