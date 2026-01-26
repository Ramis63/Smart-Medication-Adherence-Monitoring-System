#!/usr/bin/env python3
"""
Script to add sample medication and vital signs data to the database
"""

import sqlite3
import random
import os
from datetime import datetime, timedelta

# Connect to database - find the database file
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, 'backend', 'medhealth.db')
print(f"Connecting to database: {db_path}")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Clear existing data (optional - comment out if you want to keep existing data)
print("Clearing existing data...")
c.execute("DELETE FROM medication_logs")
c.execute("DELETE FROM vitals_logs")
c.execute("DELETE FROM medications")

# Add sample medications
medications = [
    ("Aspirin", "08:00"),
    ("Vitamin D", "12:00"),
    ("Blood Pressure Med", "18:00"),
    ("Evening Supplement", "20:00"),
]

print("Adding medications...")
for name, schedule_time in medications:
    c.execute(
        "INSERT INTO medications (name, schedule_time, active) VALUES (?, ?, 1)",
        (name, schedule_time)
    )
    print(f"  Added: {name} at {schedule_time}")

# Get medication IDs
c.execute("SELECT id, name, schedule_time FROM medications")
meds = c.fetchall()
med_dict = {name: (id, schedule_time) for id, name, schedule_time in meds}

# Generate medication logs for the past 7 days
print("\nAdding medication logs (past 7 days)...")
base_date = datetime.now()
statuses = ["taken", "taken", "taken", "missed"]  # 75% taken rate

for day_offset in range(7, 0, -1):  # Last 7 days
    date = base_date - timedelta(days=day_offset)
    
    for med_id, med_name, schedule_time in meds:
        # Determine status (mostly taken)
        status = random.choice(statuses)
        
        # Parse schedule time
        hour, minute = map(int, schedule_time.split(':'))
        scheduled_datetime = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if status == "taken":
            # Taken: actual time is within 30 minutes of scheduled
            actual_datetime = scheduled_datetime + timedelta(
                minutes=random.randint(-10, 30)
            )
            actual_time = actual_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
            # 60% chance of having vitals measured
            if random.random() < 0.6:
                temp = round(random.uniform(36.0, 37.5), 1)
                hr = random.randint(65, 85)
            else:
                temp = None
                hr = None
        else:
            # Missed: no actual time, no vitals
            actual_time = scheduled_datetime.strftime("%Y-%m-%d %H:%M:%S")
            temp = None
            hr = None
        
        scheduled_time_str = scheduled_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        c.execute("""
            INSERT INTO medication_logs 
            (medication_id, medication_name, scheduled_time, actual_time, status, temperature, heart_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (med_id, med_name, scheduled_time_str, actual_time, status, temp, hr))
    
    print(f"  Added logs for {date.strftime('%Y-%m-%d')}")

# Generate vital signs logs (standalone measurements, not tied to medications)
print("\nAdding standalone vital signs logs...")
for day_offset in range(7, 0, -1):
    date = base_date - timedelta(days=day_offset)
    
    # 2-4 measurements per day
    num_measurements = random.randint(2, 4)
    
    for _ in range(num_measurements):
        # Random time during the day
        hour = random.randint(8, 22)
        minute = random.choice([0, 15, 30, 45])
        measurement_time = date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        # Normal vital signs with slight variations
        temp = round(random.uniform(36.2, 37.3), 1)
        hr = random.randint(60, 90)
        
        # Determine status
        if temp < 36.0 or temp > 37.5 or hr < 60 or hr > 100:
            status = "abnormal"
        else:
            status = "normal"
        
        c.execute("""
            INSERT INTO vitals_logs (temperature, heart_rate, status, created_at)
            VALUES (?, ?, ?, ?)
        """, (temp, hr, status, measurement_time.strftime("%Y-%m-%d %H:%M:%S")))

print(f"  Added {7 * 3} vital signs measurements (average)")

# Commit all changes
conn.commit()
print("\n[SUCCESS] Sample data added successfully!")
print(f"\nSummary:")
print(f"  - Medications: {len(medications)}")
print(f"  - Medication logs: ~{len(medications) * 7} entries")
print(f"  - Vital signs logs: ~{7 * 3} entries")

# Show some stats
c.execute("SELECT COUNT(*) FROM medication_logs WHERE status = 'taken'")
taken_count = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM medication_logs WHERE status = 'missed'")
missed_count = c.fetchone()[0]
c.execute("SELECT COUNT(*) FROM vitals_logs")
vitals_count = c.fetchone()[0]

print(f"\nDatabase Statistics:")
print(f"  - Medications taken: {taken_count}")
print(f"  - Medications missed: {missed_count}")
print(f"  - Vital signs measurements: {vitals_count}")

conn.close()

