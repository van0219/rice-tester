#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def check_rice_data():
    conn = sqlite3.connect('fsm_tester.db')
    cursor = conn.cursor()
    
    print("RICE Profiles in database:")
    cursor.execute('SELECT id, rice_id, name FROM rice_profiles')
    rice_profiles = cursor.fetchall()
    for row in rice_profiles:
        print(f"  ID: {row[0]}, RICE_ID: {row[1]}, Name: {row[2]}")
    
    print("\nScenarios for INT001:")
    cursor.execute('''
        SELECT rice_profile, scenario_number, description 
        FROM scenarios 
        WHERE rice_profile LIKE "%INT001%" 
           OR rice_profile IN (SELECT id FROM rice_profiles WHERE rice_id = "INT001")
    ''')
    scenarios = cursor.fetchall()
    for row in scenarios:
        print(f"  Rice Profile: {row[0]}, Scenario: {row[1]}, Desc: {row[2]}")
    
    # Check scenario_steps for INT001
    print("\nScenario steps for INT001:")
    cursor.execute('''
        SELECT COUNT(*) 
        FROM scenario_steps 
        WHERE rice_profile LIKE "%INT001%" 
           OR rice_profile IN (SELECT id FROM rice_profiles WHERE rice_id = "INT001")
    ''')
    step_count = cursor.fetchone()[0]
    print(f"  Total steps found: {step_count}")
    
    # Get the actual rice_profile value used in scenario_steps
    cursor.execute('''
        SELECT DISTINCT rice_profile 
        FROM scenario_steps 
        ORDER BY rice_profile
    ''')
    rice_values = cursor.fetchall()
    print(f"\nDistinct rice_profile values in scenario_steps:")
    for row in rice_values:
        print(f"  '{row[0]}'")
    
    conn.close()

if __name__ == "__main__":
    check_rice_data()