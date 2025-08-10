import frappe

def has_app_permission():
	"""Check if the user has permission to access the app."""
	if frappe.session.user == "Administrator":
		return True

	roles = frappe.get_roles()
	if "Link Manager" in roles:
		return True

	return False
