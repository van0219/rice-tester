#!/usr/bin/env python3
import sqlite3
import os

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), 'fsm_tester.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== RICE RECORDS DEBUG ===")

# Check if rice_profiles table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rice_profiles';")
table_exists = cursor.fetchone()
print(f"rice_profiles table exists: {table_exists is not None}")

if table_exists:
    # Check total RICE records
    cursor.execute("SELECT COUNT(*) FROM rice_profiles;")
    total_count = cursor.fetchone()[0]
    print(f"Total RICE records: {total_count}")
    
    # Check records by user
    cursor.execute("SELECT user_id, COUNT(*) FROM rice_profiles GROUP BY user_id;")
    user_counts = cursor.fetchall()
    print(f"Records by user: {user_counts}")
    
    # Show all RICE records
    cursor.execute("""
        SELECT rp.id, rp.user_id, rp.rice_id, rp.name, rp.client_name, rp.type, rt.type_name
        FROM rice_profiles rp
        LEFT JOIN rice_types rt ON rp.type = rt.type_name
        ORDER BY rp.id
    """)
    records = cursor.fetchall()
    print(f"\nAll RICE records ({len(records)}):")
    for record in records:
        print(f"  ID: {record[0]}, User: {record[1]}, RICE_ID: {record[2]}, Name: {record[3]}, Client: {record[4]}, Type: {record[5]}, Type_Name: {record[6]}")

# Check users table
cursor.execute("SELECT id, username FROM users ORDER BY id;")
users = cursor.fetchall()
print(f"\nUsers in database: {users}")

conn.close()