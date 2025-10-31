#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def analyze_test_steps_join():
    conn = sqlite3.connect('fsm_tester.db')
    cursor = conn.cursor()
    
    print("ANALYZING TEST STEPS WITH JOIN TO TEST GROUPS")
    print("=" * 80)
    
    # Get scenario steps with proper JOIN to test_steps table
    cursor.execute("""
        SELECT 
            ss.step_order,
            ss.step_description as scenario_desc,
            ss.step_type as scenario_type,
            ts.name as test_step_name,
            ts.step_type as test_step_type,
            ts.target as test_step_target,
            ts.description as test_step_desc,
            tsg.group_name
        FROM scenario_steps ss
        LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
        LEFT JOIN test_step_groups tsg ON ts.group_id = tsg.id
        WHERE ss.rice_profile = '11' AND ss.scenario_number = 1
        ORDER BY ss.step_order
    """)
    
    steps = cursor.fetchall()
    print(f"Total steps for INT001 Scenario 1: {len(steps)}")
    print("\nDetailed step analysis with test groups:")
    print("-" * 120)
    
    for i, (order, sc_desc, sc_type, ts_name, ts_type, ts_target, ts_desc, group_name) in enumerate(steps, 1):
        print(f"\nStep {i:2d} (Order: {order}):")
        print(f"  Scenario Step: '{sc_desc}' (Type: {sc_type})")
        if ts_name:
            print(f"  Test Step:     '{ts_name}' (Type: {ts_type})")
            print(f"  Target:        '{ts_target}'")
            print(f"  Description:   '{ts_desc}'")
            print(f"  Group:         '{group_name}'")
        else:
            print(f"  Test Step:     [No linked test step - using scenario data]")
    
    # Check which description is used in TES-070 generation
    print("\n" + "=" * 80)
    print("TES-070 DESCRIPTION LOGIC ANALYSIS:")
    print("-" * 80)
    
    for i, (order, sc_desc, sc_type, ts_name, ts_type, ts_target, ts_desc, group_name) in enumerate(steps, 1):
        # This matches the logic in tes070_generator_new.py
        final_desc = sc_desc  # scenario_steps.step_description is used first
        
        # Check filtering conditions
        desc_lower = (final_desc or '').lower()
        is_wait = any(w in desc_lower for w in ['wait', 'sleep', 'pause', 'delay', 'implicit', 'explicit'])
        is_empty_short = not final_desc or len(final_desc.strip()) <= 5
        
        status = "KEPT"
        if is_wait:
            status = "FILTERED (WAIT)"
        elif is_empty_short:
            status = "FILTERED (EMPTY/SHORT)"
        
        print(f"Step {i:2d}: {status:18} - '{final_desc}'")
    
    # Check test step groups
    print("\n" + "=" * 80)
    print("TEST STEP GROUPS OVERVIEW:")
    print("-" * 80)
    
    cursor.execute("""
        SELECT tsg.group_name, COUNT(ts.id) as step_count
        FROM test_step_groups tsg
        LEFT JOIN test_steps ts ON tsg.id = ts.group_id
        GROUP BY tsg.id, tsg.group_name
        ORDER BY tsg.group_name
    """)
    
    groups = cursor.fetchall()
    for group_name, count in groups:
        print(f"  {group_name}: {count} test steps")
    
    conn.close()

if __name__ == "__main__":
    analyze_test_steps_join()