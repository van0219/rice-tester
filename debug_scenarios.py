#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3

# Debug scenario data
db_path = r"d:\AmazonQ\InforQ\RICE_Tester\fsm_tester.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== DEBUGGING SCENARIO DATA ===")

# Get scenarios for INT001
cursor.execute("""
    SELECT s.rice_profile, s.scenario_number, s.description, s.result, s.executed_at
    FROM scenarios s
    JOIN rice_profiles rp ON s.rice_profile = rp.id
    WHERE s.result IS NOT NULL AND rp.rice_id = 'INT001'
    ORDER BY s.scenario_number
""")

scenarios = cursor.fetchall()
print(f"Found {len(scenarios)} scenarios:")
for i, (rice_prof, scenario_num, description, result, executed_at) in enumerate(scenarios):
    print(f"  Scenario {i}: rice_prof={rice_prof}, scenario_num={scenario_num}, desc='{description}'")

print("\n=== CHECKING SCENARIO STEPS ===")
for i, (rice_prof, scenario_num, description, result, executed_at) in enumerate(scenarios):
    print(f"\nScenario {i+1} (rice_prof={rice_prof}, scenario_num={scenario_num}):")
    
    cursor.execute("""
        SELECT ss.step_order, ss.step_description, ss.screenshot_after
        FROM scenario_steps ss
        WHERE ss.rice_profile = ? AND ss.scenario_number = ?
        ORDER BY ss.step_order
    """, (str(rice_prof), scenario_num))
    
    steps_data = cursor.fetchall()
    print(f"  Found {len(steps_data)} steps")
    
    if steps_data:
        for step_order, step_desc, screenshot_b64 in steps_data[:3]:  # Show first 3 steps
            print(f"    Step {step_order}: {step_desc[:50]}...")

conn.close()