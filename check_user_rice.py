#!/usr/bin/env python3
import sqlite3
import os

db_path = "fsm_tester.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Users:")
    cursor.execute("SELECT id, username, full_name FROM users ORDER BY id")
    users = cursor.fetchall()
    for user_id, username, full_name in users:
        print(f"  ID: {user_id}, Username: {username}, Full Name: {full_name}")
    
    print("\nRICE Profiles by User:")
    for user_id, username, full_name in users:
        cursor.execute("SELECT id, rice_id, name FROM rice_profiles WHERE user_id = ?", (user_id,))
        profiles = cursor.fetchall()
        if profiles:
            print(f"\nUser {username} (ID: {user_id}):")
            for profile_id, rice_id, name in profiles:
                print(f"  Profile ID: {profile_id}, RICE_ID: {rice_id}, Name: {name}")
                
                # Check TES-070 versions for this profile
                cursor.execute("SELECT version_number, created_at FROM tes070_versions WHERE user_id = ? AND rice_profile_id = ? ORDER BY version_number DESC LIMIT 3", (user_id, rice_id))
                versions = cursor.fetchall()
                if versions:
                    print(f"    TES-070 versions:")
                    for version_number, created_at in versions:
                        print(f"      v{version_number} - {created_at}")
    
    conn.close()
else:
    print("Database not found")