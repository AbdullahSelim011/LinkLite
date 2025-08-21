from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate, nowdate, flt
from frappe.utils.csvutils import build_csv_response
from frappe.utils.xlsxutils import make_xlsx
import openpyxl
from datetime import datetime, timedelta
from io import BytesIO
from frappe.utils import get_url
from frappe.auth import LoginManager
from frappe.core.doctype.user.user import User
import json
from frappe.utils import today

@frappe.whitelist(allow_guest=True)
def get_delivery_trips():
    return frappe.get_all(
        "Delivery Trip",
        fields=[
            "name",
            "departure_time",
            "vehicle",
            "driver",
            "status",
            "docstatus"
        ],
        order_by="departure_time desc"
    )

@frappe.whitelist()
def submit_delivery_trip(name):
    try:
        # Fetch the Delivery Trip document
        trip = frappe.get_doc("Delivery Trip", name)
        
        # Submit the document
        trip.submit()
        
        # Commit the changes to the database
        frappe.db.commit()
        
        # Return a success message
        return {"message": "تم ترحيل الرحلة بنجاح"}
        
    except Exception as e:
        # Log the error for debugging
        frappe.log_error(frappe.get_traceback(), "Error in submit_delivery_trip")
        
        # Return an error message

@frappe.whitelist()
def cancel_delivery_trip(name):
    try:
        # Get the "Delivery Trip" document by its name
        trip = frappe.get_doc("Delivery Trip", name)
        
        # Check if the document exists before trying to cancel it
        if trip:
            # Call the standard "cancel" method for the document
            trip.cancel()
            
            # Commit the changes to the database
            frappe.db.commit()
            
            # Return a success message
            return {"message": "تم إلغاء الرحلة بنجاح"}
        else:
            # Handle the case where the document is not found
            return {"error": "لم يتم العثور على الرحلة بهذا الاسم"}

    except Exception as e:
        # Log the full traceback for debugging purposes
        frappe.log_error(frappe.get_traceback(), "Error in cancel_delivery_trip")
        
        # Return a user-friendly error message
        return {"error": f"فشل إلغاء الرحلة: {str(e)}"}

@frappe.whitelist()
def delete_delivery_trip(name):
    try:
        # Check if the document exists before trying to delete it
        if frappe.db.exists("Delivery Trip", name):
            # Delete the document using the frappe.delete_doc method
            frappe.delete_doc("Delivery Trip", name)
            
            # Commit the changes to the database
            frappe.db.commit()
            
            # Return a success message
            return {"message": "تم حذف الرحلة بنجاح"}
        else:
            # Handle the case where the document is not found
            return {"error": "لم يتم العثور على الرحلة بهذا الاسم"}

    except Exception as e:
        # Log the full traceback for debugging purposes
        frappe.log_error(frappe.get_traceback(), "Error in delete_delivery_trip")
        
        # Return a user-friendly error message
        return {"error": f"فشل حذف الرحلة: {str(e)}"}
    

@frappe.whitelist()
def create_delivery_trip(departure_time, vehicle, driver, delivery_stops):
    """
    Creates a new Delivery Trip document.
    """
    # 1. Validate inputs
    if not departure_time or not vehicle or not driver:
        frappe.throw(_("يجب إدخال جميع الحقول المطلوبة"))

    if not delivery_stops or not isinstance(delivery_stops, list):
        frappe.throw(_("يجب أن تحتوي الرحلة على توقف واحد على الأقل"))

    # 2. Create the Delivery Trip document
    try:
        doc = frappe.new_doc("Delivery Trip")
        doc.departure_time = departure_time
        doc.vehicle = vehicle
        doc.driver = driver

        # 3. Add delivery stops to the child table with a default address
        for stop in delivery_stops:
            if not stop.get("customer"):
                frappe.throw(_("يجب تحديد العميل لكل توقف"))
            
            # If no address is provided, get the first address for the customer
            address_name = stop.get("address")
            if not address_name:
                # Find a default address if none is provided
                default_address = frappe.get_value(
                    "Address",
                    filters={"customer": stop.get("customer")},
                    fieldname="name"
                )
                if not default_address:
                    frappe.throw(_("العميل '{0}' ليس لديه أي عنوان مسجل. يرجى إضافة عنوان أولاً.").format(stop.get("customer")))
                address_name = default_address

            doc.append("delivery_stops", {
                "customer": stop.get("customer"),
                "address": address_name
            })

        # 4. Save and return the result
        doc.insert()
        frappe.db.commit()
        return {"message": _("تم إنشاء رحلة توصيل جديدة بنجاح"), "trip_name": doc.name}

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(title="Delivery Trip Creation Error", message=str(e))
        frappe.throw(_("حدث خطأ أثناء إنشاء الرحلة: {0}").format(str(e)))


@frappe.whitelist()
def get_vehicles():
    """
    يجلب قائمة بجميع المركبات.
    """
    return frappe.get_all(
        "Vehicle",
        fields=["name", "license_plate"]
    )

@frappe.whitelist()
def get_drivers():
    """
    يجلب قائمة بجميع السائقين.
    """
    return frappe.get_all(
        "Driver",
        fields=["name", "full_name"]
    )

@frappe.whitelist()
def get_customers():
    """
    يجلب قائمة بجميع العملاء.
    """
    return frappe.get_all(
        "Customer",
        fields=["name", "customer_name"]
    )

@frappe.whitelist()
def get_salesInvoice():

    return frappe.get_all(
        "Sales Invoice",
        fields=["name", "customer", "posting_date", "grand_total", "status", "currency", "docstatus"]
    )

@frappe.whitelist()
def submit_sales_invoice(name):
    try:
        # Fetch the Delivery Trip document
        trip = frappe.get_doc("Sales Invoice", name)
        
        # Submit the document
        trip.submit()
        
        # Commit the changes to the database
        frappe.db.commit()
        
        # Return a success message
        return {"message": "Submitted"}
        
    except Exception as e:
        # Log the error for debugging
        frappe.log_error(frappe.get_traceback(), "Error in submit_sales_invoice")
        
        # Return an error message

@frappe.whitelist()
def cancel_sales_invoice(name):
    """
    Cancels a submitted Sales Invoice by its name.
    """
    try:
        # Get the Sales Invoice document
        invoice = frappe.get_doc("Sales Invoice", name)

        if not invoice:
            return {"error": "لم يتم العثور على الفاتورة بهذا الاسم"}

        # Check if the document is submitted
        if invoice.docstatus != 1:
            return {"error": "لا يمكن إلغاء الفاتورة لأنها ليست في حالة تم الإعتماد"}

        # Cancel the invoice
        invoice.cancel()
        frappe.db.commit()

        return {"message": "تم إلغاء الفاتورة بنجاح"}

    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(frappe.get_traceback(), "Error in cancel_sales_invoice")
        return {"error": f"فشل إلغاء الفاتورة: {str(e)}"}
# frappe.client.delete_sales_invoice
@frappe.whitelist()
def delete_sales_invoice(name):
    """
    Deletes a Sales Invoice document after ensuring it's not in a submitted state.
    """
    try:
        # Check if the Sales Invoice document exists
        if not frappe.db.exists("Sales Invoice", name):
            return {"error": "لم يتم العثور على الفاتورة بهذا الاسم"}

        # Get the document to check its status
        invoice_doc = frappe.get_doc("Sales Invoice", name)
        
        # If the invoice is submitted, cancel it first
        if invoice_doc.docstatus == 1:
            invoice_doc.cancel()
        
        # Delete the document
        frappe.delete_doc("Sales Invoice", name)
        
        # Commit the changes to the database
        frappe.db.commit()
        
        return {"message": "تم حذف الفاتورة بنجاح"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in delete_sales_invoice")
        return {"error": f"فشل حذف الفاتورة: {str(e)}"}

@frappe.whitelist()
def create_sales_invoice_custom(customer, items):
    """
    إنشاء فاتورة مبيعات جديدة مع التحقق من البيانات.
    :param customer: اسم العميل (string)
    :param items: قائمة ببنود الفاتورة (list of dicts)
    :return: dict يحتوي على رسالة النجاح أو الخطأ
    """
    try:
        if not customer:
            frappe.throw("يجب تحديد العميل.")

        if not items or not isinstance(items, list):
            frappe.throw("يجب أن تحتوي الفاتورة على بنود.")

        # حساب المجموع الكلي (grand_total)
        grand_total = 0
        for item in items:
            if not isinstance(item.get('qty'), (int, float)) or not isinstance(item.get('rate'), (int, float)):
                frappe.throw("كمية وسعر البنود يجب أن تكون أرقامًا.")
            item['amount'] = item.get('qty') * item.get('rate')
            grand_total += item['amount']

        # إنشاء مستند الفاتورة
        invoice_doc = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": customer,
            "posting_date": frappe.utils.nowdate(),
            "due_date": frappe.utils.add_months(frappe.utils.nowdate(), 1),
            "items": items,
            "grand_total": grand_total
        })

        # حفظ المستند
        invoice_doc.insert()
        frappe.db.commit()

        return {"message": "تم إنشاء الفاتورة بنجاح", "invoice_name": invoice_doc.name}

    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), "Error in create_sales_invoice_custom")
        return {"error": str(e)}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in create_sales_invoice_custom")
        return {"error": f"فشل إنشاء الفاتورة: {str(e)}"}

@frappe.whitelist()
def create_vehicle_custom(license_plate, make, model, last_odometer, fuel_type, uom, color=None):
    """
    إنشاء مستند مركبة (Vehicle) جديد مع التحقق من جميع البيانات الإلزامية.
    
    :param license_plate: رقم لوحة المركبة (string)
    :param make: اسم الشركة المصنعة (string)
    :param model: اسم طراز المركبة (string)
    :param last_odometer: قراءة عداد المسافات (اجباري)
    :param fuel_type: نوع الوقود (اجباري)
    :param uom: وحدة قياس الوقود (اجباري)
    :param color: لون المركبة (اختياري)
    :return: dict يحتوي على رسالة النجاح أو الخطأ
    """
    try:
        # التحقق من جميع الحقول الإلزامية
        if not license_plate:
            frappe.throw("رقم لوحة المركبة إلزامي.")
        if not make:
            frappe.throw("اسم الشركة المصنعة إلزامي.")
        if not model:
            frappe.throw("اسم طراز المركبة إلزامي.")
        if not last_odometer:
            frappe.throw("قراءة عداد المسافات إلزامي.")
        if not fuel_type:
            frappe.throw("نوع الوقود إلزامي.")
        if not uom:
            frappe.throw("وحدة قياس الوقود إلزامي.")

        # إنشاء مستند المركبة
        vehicle_doc = frappe.get_doc({
            "doctype": "Vehicle",
            "license_plate": license_plate,
            "make": make,
            "model": model,
            "color": color,
            "last_odometer": last_odometer,
            "fuel_type": fuel_type,
            "uom": uom
        })

        # حفظ المستند
        vehicle_doc.insert()
        frappe.db.commit()

        return {"message": "تم إنشاء المركبة بنجاح", "vehicle_name": vehicle_doc.name}

    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), "Error in create_vehicle_custom")
        return {"error": str(e)}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in create_vehicle_custom")
        return {"error": f"فشل إنشاء المركبة: {str(e)}"}
    
@frappe.whitelist()
def delete_driver(name):
    """
    Deletes a Driver document.
    """
    try:
        # Check if the Driver document exists
        if not frappe.db.exists("Driver", name):
            return {"error": "Driver not found with this name"}
        
        # Delete the document
        frappe.delete_doc("Driver", name)
        
        # Commit the changes to the database
        frappe.db.commit()
        
        return {"message": "Driver deleted successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in delete_driver")
        return {"error": f"Failed to delete driver: {str(e)}"}
    
    
@frappe.whitelist()
def create_driver_custom(full_name, status):
    """
    Creates a new Driver document with a name and status.
    
    :param full_name: The name of the driver (string).
    :param status: The status of the driver (e.g., 'Active', 'Inactive', 'On Leave').
    :return: A dictionary with a success or error message.
    """
    try:
        # Check for mandatory fields
        if not full_name:
            frappe.throw("اسم السائق إلزامي.")
        if not status:
            frappe.throw("الحالة إلزامي.")

        # Create the new Driver document
        driver_doc = frappe.get_doc({
            "doctype": "Driver",
            "full_name": full_name,
            "status": status
        })

        # Insert and commit the document to the database
        driver_doc.insert()
        frappe.db.commit()

        return {"message": "تم إنشاء السائق بنجاح", "full_name": driver_doc.name}

    except frappe.ValidationError as e:
        frappe.log_error(frappe.get_traceback(), "Error in create_driver_custom")
        return {"error": str(e)}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in create_driver_custom")
        return {"error": f"فشل إنشاء السائق: {str(e)}"}


@frappe.whitelist()
def create_customer(customer_data):
    """Create a new customer"""
    try:
        # Validate required fields
        if not customer_data.get("customer_name"):
            frappe.throw(_("Customer Name is required"))
        
        if not customer_data.get("customer_type"):
            frappe.throw(_("Customer Type is required"))
        
        # Create new customer doc
        customer = frappe.new_doc("Customer")
        customer.update({
            "customer_name": customer_data.get("customer_name"),
            "customer_type": customer_data.get("customer_type"),
            "customer_primary_address": customer_data.get("customer_primary_address", ""),
            "tax_id": customer_data.get("tax_id", "")
        })
        
        customer.insert(ignore_permissions=True)
        
        return {
            "name": customer.name,
            "message": _("Customer created successfully")
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to create customer"))
        frappe.throw(_("Failed to create customer. Error: {0}").format(str(e)))
        
@frappe.whitelist()
def delete_customer(customer_name):
    """Delete a customer by name"""
    try:
        # التحقق من وجود العميل أولاً
        if not frappe.db.exists("Customer", customer_name):
            frappe.throw(_("Customer not found"))
        
        # الحصول على وثيقة العميل
        customer = frappe.get_doc("Customer", customer_name)
        
        # التحقق من عدم وجود معاملات مرتبطة بالعميل
        if has_linked_transactions(customer_name):
            frappe.throw(_("Cannot delete customer with linked transactions"))
        
        # حذف العميل
        frappe.delete_doc("Customer", customer_name, ignore_permissions=True)
        
        return {
            "success": True,
            "message": _("Customer deleted successfully")
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), _("Failed to delete customer"))
        frappe.throw(_("Failed to delete customer. Error: {0}").format(str(e)))

def has_linked_transactions(customer_name):
    """Check if customer has linked transactions"""
    # يمكنك إضافة الجداول الأخرى التي قد ترتبط بالعميل
    linked_doctypes = ["Sales Invoice", "Quotation", "Sales Order"]
    
    for doctype in linked_doctypes:
        if frappe.db.exists(doctype, {"customer": customer_name}):
            return True
    return False

@frappe.whitelist()
def create_address(**kwargs):
    """Create a new address"""
    doc = frappe.new_doc("Address")
    doc.update(kwargs)
    doc.insert()
    return doc.name

@frappe.whitelist()
def update_address(**kwargs):
    """Update an existing address"""
    if not kwargs.get("name"):
        frappe.throw("Name is required for update")
    
    doc = frappe.get_doc("Address", kwargs["name"])
    doc.update(kwargs)
    doc.save()
    return doc.name

@frappe.whitelist()
def delete_address(doctype, name):
    """Delete an address"""
    frappe.delete_doc(doctype, name)
    return "Address deleted successfully"

@frappe.whitelist()
def update_sales_invoice(invoice_name, customer=None, items=None, posting_date=None):
    try:
        # جلب الفاتورة الحالية
        invoice = frappe.get_doc("Sales Invoice", invoice_name)
        
        # تحديث البيانات
        if customer:
            invoice.customer = customer
        if posting_date:
            invoice.posting_date = posting_date
            
        # تحديث الأصناف
        if items:
            invoice.items = []
            for item in json.loads(items):
                invoice.append("items", {
                    "item_code": item.get("item_code"),
                    "qty": item.get("qty"),
                    "rate": item.get("rate")
                })
        
        # حفظ التعديلات
        invoice.save()
        
        return {"success": True, "message": "تم تحديث الفاتورة بنجاح"}
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to update sales invoice")
        return {"success": False, "message": str(e)}

@frappe.whitelist()
def get_counts():
    """
    Counts the number of documents in specific DocTypes based on a set of filters.
    """
    counts = frappe._dict()

    # 1. Count active Delivery Trips
    # Filters are passed using the `filters` keyword.
    counts.active_trips_count = frappe.db.count('Delivery Trip', filters={'status': 'Active'})

    # 2. Count Sales Invoices for the current day
    # frappe.utils.today() returns the current date as a string (YYYY-MM-DD).
    counts.today_invoices_count = frappe.db.count('Sales Invoice', filters={'posting_date': today()})

    # 3. Count available Vehicles
    counts.available_vehicles_count = frappe.db.count('Vehicle', filters={'status': 'Available'})

    # 4. Count active Drivers
    counts.active_drivers_count = frappe.db.count('Driver', filters={'status': 'Active'})

    return counts



# ######################################################### #
# Dashboard API - mostafa kadry
# ######################################################### #
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

@frappe.whitelist(allow_guest=True)
def get_total_delivered_orders_count_in_current_month(*args, **kwargs):
    """
    Returns the count of delivered orders in the current month.
    """
    count = get_monthly_count("Delivery Trip", "departure_time")
    api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_revenue_in_current_month():
    """
    Returns the total revenue (sum of grand_total) of Sales Invoices in the current month.
    """
    invoices = frappe.db.get_all(
        "Sales Invoice",
        filters={
            "posting_date": ["between", [get_first_day(nowdate()), get_last_day(nowdate())]],
            
        },
        fields=["grand_total"]
    )

    total_revenue = sum([inv["grand_total"] for inv in invoices])
    return total_revenue

@frappe.whitelist()
def get_total_vehicles_count(*args, **kwargs):
    """
    Returns the total number of vehicles.
    """
    count = get_count("Vehicle")
    api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_drivers_count(*args, **kwargs):
    """
    Returns the total number of drivers.
    """
    count = get_count("Driver")
    api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")

@frappe.whitelist()
def get_total_customers_count(*args, **kwargs):
    """
    Returns the total number of customers.
    """
    count = get_count("Customer")
    api_response(200, "success", count) if count is not None else api_response(500, "error", "Could not fetch data.")


def completed_trips_count(*args, **kwargs):
    count = frappe.db.count("Delivery Trip", {"status": "Completed"})
    return count

def in_transit_trips_count(*args, **kwargs):
    count = frappe.db.count("Delivery Trip", {"status": "In Transit"})
    return count

def cancel_delivery_trip(*args, **kwargs):
    count = frappe.db.count("Delivery Trip", {"status": "Cancelled"})
    return count

def available_cars(*args, **kwargs):
    # To be implemented , the doctype it self is not submittable
    count = frappe.db.count("Vehicle")
    return count

def active_drivers_count(*args, **kwargs):
    count = frappe.db.count("Driver", {"status": "Active"})
    return count
def safe_int(value, default=30):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# get all sales invoices on accrual basis
@frappe.whitelist(allow_guest=True)
def revenueChartData(*args, **kwargs):
    period = safe_int(kwargs.get("period", 30))

    # Ensure period is an integer (fallback to 30 if not valid)
    if not isinstance(period, int) or period <= 0:
        print("Invalid period, defaulting to 30 days",type(period), period)
        period = 30
    
    # Calculate start and end dates
    start_date = (datetime.now() - timedelta(days=period)).date()
    end_date = datetime.now().date()
    
    data = frappe.db.get_list("Sales Invoice", filters={"posting_date": ["between", [start_date, end_date]]}, order_by="posting_date asc",
            fields=["posting_date", "grand_total"], ignore_permissions=True)
    
    return {
        "period_days": period,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "records": data
    }
    
    
    

@frappe.whitelist(allow_guest=True)
def dashboard_data(*args, **kwargs):
    """
    Retrieves all dashboard data points in a single request.
    """
    try:
        data = {}
        
        funcs = {
            "totalTrips": lambda: get_monthly_count("Delivery Trip", "departure_time"),
            "totalRevenue": lambda: get_total_revenue_in_current_month(),
            "totalVehicles": lambda: get_count("Vehicle"),
            "totalDrivers": lambda: get_count("Driver"),
            "activeCustomers": lambda: get_count("Customer"),
            "completedTrips": completed_trips_count,
            "ongoingTrips": in_transit_trips_count,
            "cancelledTrips": cancel_delivery_trip,
            "availableVehicles": available_cars,
            "activeDrivers": active_drivers_count,
            "revenueChartData": lambda: revenueChartData(period=kwargs.get("period", 30)),
        }

        for key, fn in funcs.items():
            try:
                data[key] = fn()
            except Exception as e:
                frappe.log_error(f"Dashboard metric `{key}` failed: {e}", "Dashboard Debug")
                data[key] = None

        if any(value is None for value in data.values()):
            api_response(500, "Error fetching some dashboard data.", data)
        
        api_response(200, "success", data)

    except Exception as e:
        frappe.log_error(message=str(e), title="Dashboard data fetch error")
        api_response(501, "error", str(e))

@frappe.whitelist(allow_guest=True)
def get_drivers_data(*args, **kwargs):
    try:
        data = frappe.db.get_list("Driver", fields=["name", "full_name", "status"])
        api_response(200, "success", data)
    except Exception as e:
        frappe.log_error(message=str(e), title="Drivers data fetch error")
        api_response(501, "error", str(e))
    
