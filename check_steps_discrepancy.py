#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def analyze_steps():
    conn = sqlite3.connect('fsm_tester.db')
    cursor = conn.cursor()
    
    # Get all steps for RICE INT001 Scenario 1
    cursor.execute("""
        SELECT ss.step_order, ss.step_description, COALESCE(ts.step_type, ss.step_type) as step_type
        FROM scenario_steps ss
        LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
        WHERE ss.rice_profile = 'INT001' AND ss.scenario_number = 1
        ORDER BY ss.step_order
    """)
    
    steps = cursor.fetchall()
    print(f"Total steps in database: {len(steps)}")
    print("\nStep-by-step analysis:")
    print("=" * 80)
    
    wait_count = 0
    empty_count = 0
    short_count = 0
    kept_count = 0
    
    for i, (order, desc, stype) in enumerate(steps, 1):
        desc_lower = (desc or '').lower()
        
        # Check if it's a wait step
        is_wait = any(w in desc_lower for w in ['wait', 'sleep', 'pause', 'delay', 'implicit', 'explicit'])
        
        # Check if it's empty or very short
        is_empty = not desc or len(desc.strip()) <= 5
        
        if is_wait:
            wait_count += 1
            print(f"{i:2d}. [WAIT STEP] {desc} (Type: {stype})")
        elif is_empty:
            empty_count += 1
            print(f"{i:2d}. [EMPTY/SHORT] '{desc}' (Type: {stype})")
        elif len(desc.strip()) <= 10:
            short_count += 1
            print(f"{i:2d}. [SHORT DESC] {desc} (Type: {stype})")
        else:
            kept_count += 1
            print(f"{i:2d}. [KEPT] {desc} (Type: {stype})")
    
    print("\n" + "=" * 80)
    print("SUMMARY:")
    print(f"Total steps in database: {len(steps)}")
    print(f"Wait steps (filtered out): {wait_count}")
    print(f"Empty/very short steps (filtered out): {empty_count}")
    print(f"Short description steps: {short_count}")
    print(f"Steps kept in TES-070: {kept_count}")
    print(f"Total filtered out: {wait_count + empty_count}")
    print(f"Expected in TES-070: {len(steps) - wait_count - empty_count}")
    
    conn.close()

if __name__ == "__main__":
    analyze_steps()