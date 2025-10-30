#!/usr/bin/env python3
import sqlite3
import os

db_path = "fsm_tester.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("ALL TES-070 versions in database:")
    cursor.execute("SELECT id, user_id, rice_profile_id, version_number, created_at, created_by FROM tes070_versions ORDER BY id")
    versions = cursor.fetchall()
    for version_id, user_id, rice_profile_id, version_number, created_at, created_by in versions:
        print(f"  ID: {version_id}, User: {user_id}, RICE: {rice_profile_id}, v{version_number}, {created_at}, {created_by}")
    
    conn.close()
else:
    print("Database not found")