#!/usr/bin/env python3
import sqlite3
import os

db_path = "fsm_tester.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("RICE Profiles:")
    cursor.execute("SELECT id, rice_id, name FROM rice_profiles ORDER BY id")
    profiles = cursor.fetchall()
    for profile_id, rice_id, name in profiles:
        print(f"  ID: {profile_id}, RICE_ID: {rice_id}, Name: {name}")
    
    print("\nTES-070 versions by RICE profile:")
    cursor.execute("SELECT DISTINCT rice_profile_id FROM tes070_versions")
    rice_ids = cursor.fetchall()
    for (rice_id,) in rice_ids:
        print(f"\nRICE {rice_id}:")
        cursor.execute("SELECT version_number, created_at FROM tes070_versions WHERE rice_profile_id = ? ORDER BY version_number DESC", (rice_id,))
        versions = cursor.fetchall()
        for version_number, created_at in versions:
            print(f"  v{version_number} - {created_at}")
    
    conn.close()
else:
    print("Database not found")