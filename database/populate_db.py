import sqlite3
from datetime import datetime, timedelta

# Connect to the SQLite database (adjust path as needed)
conn = sqlite3.connect('database/hospital.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor_availability (
    date TEXT,
    time_slot TEXT,
    specialization TEXT,
    doctor_name TEXT,
    is_available BOOLEAN,
    patient_id INT
)
''')

# Doctor and specialization mapping
entries = [
    ("general_dentist", "john doe"),
    ("cosmetic_dentist", "jane smith"),
    ("prosthodontist", "emily johnson"),
    ("pediatric_dentist", "michael green"),
    ("emergency_dentist", "lisa brown"),
    ("oral_surgeon", "kevin anderson"),
    ("orthodontist", "robert martinez"),
    ("general_dentist", "susan davis"),
    ("general_dentist", "daniel miller"),
    ("general_dentist", "sarah wilson"),
    ("general_medicine", "alex turner"),
]

# Date range and slots
start_date = datetime(2025, 7, 31)
end_date = datetime(2025, 8, 15)
time_slots = [f"{hour:02d}:00" for hour in range(9, 16)]  # 09:00 to 15:00

rows = []
current_date = start_date
while current_date <= end_date:
    if current_date.weekday() < 5:  # 0=Monday, ..., 4=Friday
        date_str = current_date.strftime("%d-%m-%Y")
        for specialization, doctor in entries:
            for slot in time_slots:
                rows.append((date_str, slot, specialization, doctor, True, None))
    current_date += timedelta(days=1)

# Clear previous data for a clean slate (optional, uncomment if needed)
# cursor.execute('DELETE FROM doctor_availability')

# Insert data
cursor.executemany('''
INSERT INTO doctor_availability (date, time_slot, specialization, doctor_name, is_available, patient_id)
VALUES (?, ?, ?, ?, ?, ?)
''', rows)

conn.commit()
conn.close()
