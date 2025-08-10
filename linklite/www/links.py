import frappe


def get_context(context):
    csrf_token = frappe.sessions.get_csrf_token()
    frappe.db.commit()
    context.boot = frappe._dict()
    context.boot.csrf_token = csrf_token
    return context
