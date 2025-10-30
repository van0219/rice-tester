#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import sqlite3

def test_tes070_requirements():
    """Test TES-070 generation requirements"""
    
    print("=== TES-070 Button Test ===")
    
    # Check database
    db_path = "fsm_tester.db"
    if not os.path.exists(db_path):
        print("[ERROR] Database not found: fsm_tester.db")
        return False
    
    print("[OK] Database found")
    
    # Check template
    template_path = "TES-070-Template/TES-070_Custom_Extension_Unit_Test_Results_v2.0.docx"
    if not os.path.exists(template_path):
        print("[ERROR] Template not found")
        return False
    
    print("[OK] Template found")
    
    # Check for RICE profiles
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM rice_profiles")
    rice_count = cursor.fetchone()[0]
    print(f"[INFO] RICE profiles: {rice_count}")
    
    if rice_count == 0:
        print("[WARNING] No RICE profiles found - create one first")
        conn.close()
        return False
    
    # Check for executed scenarios
    cursor.execute("SELECT COUNT(*) FROM scenarios WHERE result IS NOT NULL AND result != 'Not run'")
    executed_count = cursor.fetchone()[0]
    print(f"[INFO] Executed scenarios: {executed_count}")
    
    if executed_count == 0:
        print("[WARNING] No executed scenarios found - run scenarios first")
        conn.close()
        return False
    
    # Show sample RICE profiles with scenarios
    cursor.execute("""
        SELECT rp.rice_id, rp.name, COUNT(s.id) as scenario_count,
               SUM(CASE WHEN s.result IS NOT NULL AND s.result != 'Not run' THEN 1 ELSE 0 END) as executed_count
        FROM rice_profiles rp
        LEFT JOIN scenarios s ON s.rice_profile = rp.id
        GROUP BY rp.id, rp.rice_id, rp.name
        ORDER BY executed_count DESC
        LIMIT 5
    """)
    
    profiles = cursor.fetchall()
    print("\n[INFO] RICE Profiles Status:")
    for rice_id, name, total, executed in profiles:
        status = "[READY]" if executed > 0 else "[NO SCENARIOS]"
        print(f"  RICE {rice_id}: {name} ({executed}/{total} executed) - {status}")
    
    conn.close()
    
    print("\n[HELP] TES-070 Button Requirements:")
    print("1. Select a RICE profile from the list")
    print("2. Ensure scenarios are executed (not 'Not run')")
    print("3. Click 'Generate TES-070' button")
    
    return True

if __name__ == "__main__":
    test_tes070_requirements()