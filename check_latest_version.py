#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8
sys.path.append(os.path.dirname(__file__))

from database_manager import DatabaseManager

def check_latest_version():
    """Check the latest TES-070 version"""
    
    try:
        db_manager = DatabaseManager(user_id=1)
        
        # Get all versions for INT001
        versions = db_manager.get_tes070_versions("INT001")
        
        print(f"Total versions found: {len(versions)}")
        
        for i, (version_id, version_number, created_at, created_by) in enumerate(versions):
            print(f"  Version {i+1}: v{version_number} - ID {version_id} - {created_at} by {created_by}")
        
        if versions:
            latest = versions[0]
            print(f"\nLatest version: v{latest[1]} (ID: {latest[0]})")
            return latest[0]
        else:
            print("No versions found")
            return None
            
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    check_latest_version()