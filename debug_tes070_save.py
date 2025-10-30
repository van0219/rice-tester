#!/usr/bin/env python3
import sqlite3
import os
from database_manager import DatabaseManager

# Test the TES-070 save process
db_manager = DatabaseManager(1)  # Assuming user_id 1

# Check current versions
print("Current TES-070 versions:")
versions = db_manager.get_tes070_versions("INT001")
for version_id, version_number, created_at, created_by in versions:
    print(f"  v{version_number} - {created_at} - {created_by}")

# Test saving a new version
print("\nTesting save_tes070_version...")
try:
    test_content = b"Test TES-070 content"
    version_id = db_manager.save_tes070_version("INT001", test_content, "Test User")
    print(f"Save completed, returned version_id: {version_id}")
    
    # Check versions again
    print("\nVersions after save:")
    versions = db_manager.get_tes070_versions("INT001")
    for version_id, version_number, created_at, created_by in versions:
        print(f"  v{version_number} - {created_at} - {created_by}")
        
except Exception as e:
    print(f"Error during save: {e}")

db_manager.close()