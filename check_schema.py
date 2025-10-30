#!/usr/bin/env python3
import sqlite3
import os

db_path = "fsm_tester.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("TES-070 versions table schema:")
    cursor.execute("PRAGMA table_info(tes070_versions)")
    columns = cursor.fetchall()
    for column in columns:
        print(f"  {column}")
    
    print("\nForeign key constraints for tes070_versions:")
    cursor.execute("PRAGMA foreign_key_list(tes070_versions)")
    fks = cursor.fetchall()
    if fks:
        for fk in fks:
            print(f"  {fk}")
    else:
        print("  No foreign key constraints found!")
    
    print("\nRICE profiles table:")
    cursor.execute("SELECT id, rice_id FROM rice_profiles WHERE user_id = 1")
    profiles = cursor.fetchall()
    for profile_id, rice_id in profiles:
        print(f"  Profile ID: {profile_id}, RICE_ID: {rice_id}")
    
    conn.close()
else:
    print("Database not found")