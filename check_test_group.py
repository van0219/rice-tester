#!/usr/bin/env python3
import sqlite3
import os

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), 'fsm_tester.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check for the Smart Recording test group
cursor.execute("""
    SELECT tsg.id, tsg.group_name, tsg.description, tsg.created_at
    FROM test_step_groups tsg 
    WHERE tsg.group_name LIKE '%Smart Recording_CIS_Outbound2%'
""")

groups = cursor.fetchall()
print("=== Test Groups Found ===")
for group in groups:
    print(f"ID: {group[0]}")
    print(f"Name: {group[1]}")
    print(f"Description: {group[2]}")
    print(f"Created: {group[3]}")
    print("-" * 50)
    
    # Get steps for this group
    cursor.execute("""
        SELECT ts.id, ts.name, ts.step_type, ts.target, ts.description
        FROM test_steps ts 
        WHERE ts.group_id = ?
        ORDER BY ts.id
    """, (group[0],))
    
    steps = cursor.fetchall()
    print(f"=== Steps in Group '{group[1]}' ===")
    for step in steps:
        print(f"Step {step[0]}: {step[1]}")
        print(f"  Type: {step[2]}")
        print(f"  Target: {step[3]}")
        print(f"  Description: {step[4]}")
        print()

conn.close()