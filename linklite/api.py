import frappe

@frappe.whitelist()
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
def create_delivery_trip(departure_time, vehicle, driver, delivery_stops):
    trip = frappe.get_doc({
        "doctype": "Delivery Trip",
        "departure_time": departure_time,
        "vehicle": vehicle,
        "driver": driver,
        "status": "Draft",
        "delivery_stops": delivery_stops
    })
    trip.insert()
    frappe.db.commit()
    return trip

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
def get_delivery_trips():
    """
    Retrieves all Delivery Trip documents with specific fields.
    """
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
def create_delivery_trip(departure_time, vehicle, driver, delivery_stops):
    """
    Creates a new Delivery Trip document.
    """
    trip = frappe.get_doc({
        "doctype": "Delivery Trip",
        "departure_time": departure_time,
        "vehicle": vehicle,
        "driver": driver,
        "status": "Draft",
        "delivery_stops": delivery_stops
    })
    trip.insert()
    frappe.db.commit()
    return trip

@frappe.whitelist()
def submit_delivery_trip(name):
    """
    Submits a Delivery Trip document by its name.
    """
    try:
        trip = frappe.get_doc("Delivery Trip", name)
        trip.submit()
        frappe.db.commit()
        return {"message": "تم ترحيل الرحلة بنجاح"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in submit_delivery_trip")
        return {"error": f"فشل ترحيل الرحلة: {e}"}

@frappe.whitelist()
def cancel_delivery_trip(name):
    """
    Cancels a submitted Delivery Trip document.
    """
    try:
        trip = frappe.get_doc("Delivery Trip", name)
        trip.cancel()
        frappe.db.commit()
        return {"message": "تم إلغاء الرحلة بنجاح"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in cancel_delivery_trip")
        return {"error": f"فشل إلغاء الرحلة: {e}"}

@frappe.whitelist()
def delete_delivery_trip(name):
    """
    Deletes a Delivery Trip document by its name.
    """
    try:
        frappe.delete_doc("Delivery Trip", name)
        frappe.db.commit()
        return {"message": "تم حذف الرحلة بنجاح"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in delete_delivery_trip")
        return {"error": f"فشل حذف الرحلة: {e}"}