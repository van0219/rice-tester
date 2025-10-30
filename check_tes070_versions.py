#!/usr/bin/env python3
import sqlite3
import os

db_path = "fsm_tester.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT version_number, created_at, created_by FROM tes070_versions ORDER BY version_number DESC LIMIT 10")
    versions = cursor.fetchall()
    
    print("TES-070 Versions:")
    for version_number, created_at, created_by in versions:
        print(f"v{version_number} - {created_at} - {created_by}")
    
    conn.close()
else:
    print("Database not found")