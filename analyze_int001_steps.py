#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def analyze_int001_steps():
    conn = sqlite3.connect('fsm_tester.db')
    cursor = conn.cursor()
    
    # Get all steps for RICE ID 11 (INT001) Scenario 1
    cursor.execute("""
        SELECT ss.step_order, ss.step_description, COALESCE(ts.step_type, ss.step_type) as step_type
        FROM scenario_steps ss
        LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
        WHERE ss.rice_profile = '11' AND ss.scenario_number = 1
        ORDER BY ss.step_order
    """)
    
    steps = cursor.fetchall()
    print(f"Total steps in database for INT001 Scenario 1: {len(steps)}")
    print("\nStep-by-step analysis:")
    print("=" * 100)
    
    wait_count = 0
    empty_count = 0
    short_count = 0
    kept_count = 0
    
    for i, (order, desc, stype) in enumerate(steps, 1):
        desc_lower = (desc or '').lower()
        
        # Check filtering conditions from TES-070 generator
        is_wait = any(w in desc_lower for w in ['wait', 'sleep', 'pause', 'delay', 'implicit', 'explicit'])
        is_empty_or_short = not desc or len(desc.strip()) <= 5
        
        status = ""
        if is_wait:
            wait_count += 1
            status = "[FILTERED - WAIT]"
        elif is_empty_or_short:
            empty_count += 1
            status = "[FILTERED - EMPTY/SHORT]"
        else:
            kept_count += 1
            status = "[KEPT IN TES-070]"
        
        print(f"{i:2d}. {status:20} '{desc}' (Type: {stype})")
    
    print("\n" + "=" * 100)
    print("FILTERING SUMMARY:")
    print(f"Total steps in database: {len(steps)}")
    print(f"Wait steps (filtered out): {wait_count}")
    print(f"Empty/short steps (filtered out): {empty_count}")
    print(f"Steps kept in TES-070: {kept_count}")
    print(f"Total filtered out: {wait_count + empty_count}")
    print(f"\nMATH CHECK:")
    print(f"Database total: {len(steps)}")
    print(f"TES-070 shows: 15 steps")
    print(f"You counted wait steps: 10")
    print(f"Actual wait steps found: {wait_count}")
    print(f"Actual empty/short steps: {empty_count}")
    print(f"Expected in TES-070: {len(steps)} - {wait_count} - {empty_count} = {kept_count}")
    
    conn.close()

if __name__ == "__main__":
    analyze_int001_steps()