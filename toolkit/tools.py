from models.model import DateModel, DateTimeModel, IdentificationNumberModel
from typing import  Literal
from langchain_core.tools import tool
from datetime import datetime
import sqlite3
import os

# Use absolute path for database
DB_URL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'hospital.db')

def get_db_connection():
    """Get database connection with row factory for better data access"""
    conn = sqlite3.connect(DB_URL)
    conn.row_factory = sqlite3.Row  # This allows dict-like access to rows
    return conn


def convert_datetime_format(dt_str):
    """Convert datetime string to separate date and time components for database"""
    # Parse the input datetime string in DD-MM-YYYY HH:MM format
    dt = datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
    
    # Extract date and time components for separate database columns
    date_part = dt.strftime("%d-%m-%Y")
    time_part = dt.strftime("%H:%M")
    
    return date_part, time_part


def convert_to_am_pm(time_str):
    """Convert 24-hour time format to 12-hour AM/PM format"""
    # Split the time string into hours and minutes
    hours, minutes = map(int, time_str.split(":"))
    
    # Determine AM or PM
    period = "AM" if hours < 12 else "PM"
    
    # Convert hours to 12-hour format
    hours = hours % 12 or 12
    
    # Format the output
    return f"{hours}:{minutes:02d} {period}"

@tool
def check_availability_by_doctor(desired_date:DateModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe','alex turner']):
    """
    Checking the database if we have availability for the specific doctor.
    The parameters should be mentioned by the user in the query
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for available slots for the specific doctor on the desired date
    query = """
    SELECT time_slot FROM doctor_availability 
    WHERE date = ? AND doctor_name = ? AND is_available = 1
    ORDER BY time_slot
    """
    
    cursor.execute(query, [desired_date.date, doctor_name])
    results = cursor.fetchall()
    conn.close()
    
    if len(results) == 0:
        output = "No availability in the entire day"
    else:
        time_slots = [row['time_slot'] for row in results]
        formatted_slots = [convert_to_am_pm(slot) for slot in time_slots]
        output = f'Availability for {doctor_name} on {desired_date.date}:\n'
        output += "Available slots: " + ', '.join(formatted_slots)

    return output

@tool
def check_availability_by_specialization(desired_date:DateModel, specialization:Literal["general_dentist", "cosmetic_dentist", "prosthodontist", "pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist","general_medicine"]):
    """
    Checking the database if we have availability for the specific specialization.
    The parameters should be mentioned by the user in the query
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query the database for available slots for the specific specialization on the desired date
    query = """
    SELECT doctor_name, time_slot FROM doctor_availability 
    WHERE date = ? AND specialization = ? AND is_available = 1
    ORDER BY doctor_name, time_slot
    """
    
    cursor.execute(query, [desired_date.date, specialization])
    results = cursor.fetchall()
    conn.close()
    
    if len(results) == 0:
        output = "No availability in the entire day"
    else:
        # Group results by doctor
        doctors_slots = {}
        for row in results:
            doctor_name = row['doctor_name']
            time_slot = row['time_slot']
            if doctor_name not in doctors_slots:
                doctors_slots[doctor_name] = []
            doctors_slots[doctor_name].append(time_slot)
        
        output = f'Availability for {specialization} on {desired_date.date}:\n'
        for doctor_name, time_slots in doctors_slots.items():
            formatted_slots = [convert_to_am_pm(slot) for slot in time_slots]
            output += f"{doctor_name.title()}: " + ', '.join(formatted_slots) + '\n'

    return output


@tool
def reschedule_appointment(old_date:DateTimeModel, new_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe','alex turner']):
    """
    Rescheduling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert datetime formats to separate date and time components
    new_date_part, new_time_part = convert_datetime_format(new_date.date)
    
    # Check if the new slot is available
    query = """
    SELECT * FROM doctor_availability 
    WHERE date = ? AND time_slot = ? AND doctor_name = ? AND is_available = 1
    """
    
    cursor.execute(query, [new_date_part, new_time_part, doctor_name])
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return "No available slots in the desired period"
    else:
        # Cancel the old appointment and set the new one
        cancel_result = cancel_appointment.invoke({'date': old_date, 'id_number': id_number, 'doctor_name': doctor_name})
        if "don´t have any appointment" in cancel_result:
            return cancel_result
        
        set_result = set_appointment.invoke({'desired_date': new_date, 'id_number': id_number, 'doctor_name': doctor_name})
        if "Successfully done" in set_result:
            return "Successfully rescheduled for the desired time"
        else:
            return set_result

@tool
def cancel_appointment(date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe','alex turner']):
    """
    Canceling an appointment.
    The parameters MUST be mentioned by the user in the query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert datetime format to separate date and time components
    date_part, time_part = convert_datetime_format(date.date)
    
    # Check if the appointment exists
    query = """
    SELECT * FROM doctor_availability 
    WHERE date = ? AND time_slot = ? AND doctor_name = ? AND patient_id = ? AND is_available = 0
    """
    
    cursor.execute(query, [date_part, time_part, doctor_name, id_number.id])
    result = cursor.fetchone()
    
    if result is None:
        conn.close()
        return "You don´t have any appointment with that specifications"
    else:
        # Cancel the appointment by setting is_available to True and patient_id to None
        update_query = """
        UPDATE doctor_availability 
        SET is_available = 1, patient_id = NULL 
        WHERE date = ? AND time_slot = ? AND doctor_name = ? AND patient_id = ?
        """
        
        cursor.execute(update_query, [date_part, time_part, doctor_name, id_number.id])
        conn.commit()
        conn.close()
        
        return "Successfully cancelled"
    

@tool
def set_appointment(desired_date:DateTimeModel, id_number:IdentificationNumberModel, doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe','alex turner']):
    """
    Set appointment or slot with the doctor.
    The parameters MUST be mentioned by the user in the query.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert datetime format to separate date and time components
    date_part, time_part = convert_datetime_format(desired_date.date)
    
    # Check if the slot is available
    query = """
    SELECT * FROM doctor_availability 
    WHERE date = ? AND time_slot = ? AND doctor_name = ? AND is_available = 1
    """
    
    cursor.execute(query, [date_part, time_part, doctor_name])
    result = cursor.fetchone()
    
    if result is None:
        conn.close()
        return "No available appointments for that particular case"
    else:
        # Book the appointment by setting is_available to False and patient_id to the user's ID
        update_query = """
        UPDATE doctor_availability 
        SET is_available = 0, patient_id = ? 
        WHERE date = ? AND time_slot = ? AND doctor_name = ? AND is_available = 1
        """
        
        cursor.execute(update_query, [id_number.id, date_part, time_part, doctor_name])
        conn.commit()
        conn.close()
        
        return "Successfully done"