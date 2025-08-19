import frappe
from frappe.utils import get_first_day, get_last_day, nowdate

def api_response(status_code: int, message: str, data=None):
    """
    Standardizes Frappe API responses.
    """
    frappe.local.response["http_status_code"] = status_code
    frappe.local.response["message"] = message
    if data is not None:
        frappe.local.response["data"] = data
    return frappe.local.response

def get_count(doctype: str, filters: dict = None):
    """
    Centralized function to get the count of a doctype with optional filters.
    """
    try:
        return frappe.db.count(doctype, filters=filters)
    except Exception as e:
        frappe.log_error(message=str(e), title=f"Error getting count for {doctype}")
        return None

def get_monthly_count(doctype: str, date_field: str):
    """
    A specific helper function to get the count for the current month.
    """
    start_date = get_first_day(nowdate())
    end_date = get_last_day(nowdate())
    filters = {date_field: ["between", [start_date, end_date]]}
    return get_count(doctype, filters)

@frappe.whitelist()
def get_total_delivered_orders_count_in_current_month(*args, **kwargs):
    """
    Returns the count of delivered orders in the current month.
    """
    count = get_monthly_count("Delivery Trip", "departure_time")
    return api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_revenue_in_current_month(*args, **kwargs):
    """
    Returns the count of sales invoices (revenue) in the current month.
    """
    count = get_monthly_count("Sales Invoice", "posting_date")
    return api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_vehicles_count(*args, **kwargs):
    """
    Returns the total number of vehicles.
    """
    count = get_count("Vehicle")
    return api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_drivers_count(*args, **kwargs):
    """
    Returns the total number of drivers.
    """
    count = get_count("Driver")
    return api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_customers_count(*args, **kwargs):
    """
    Returns the total number of customers.
    """
    count = get_count("Customer")
    return api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def dashboard_data(*args, **kwargs):
    """
    Retrieves all dashboard data points in a single request.
    """
    try:
        data = {
            "total_delivered_orders_count_in_current_month": get_monthly_count("Delivery Trip", "departure_time"),
            "total_revenue_in_current_month": get_monthly_count("Sales Invoice", "posting_date"),
            "total_vehicles_count": get_count("Vehicle"),
            "total_drivers_count": get_count("Driver"),
            "total_customers_count": get_count("Customer")
        }
        
        if any(value is None for value in data.values()):
            return api_response(500, "Error fetching some dashboard data.", None)
            
        return api_response(200, "success", data)
    except Exception as e:
        frappe.log_error(message=str(e), title="Dashboard data fetch error")
        return api_response(500, "error", str(e))