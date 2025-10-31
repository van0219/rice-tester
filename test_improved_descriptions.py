#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

def test_improved_descriptions():
    conn = sqlite3.connect('fsm_tester.db')
    cursor = conn.cursor()
    
    print("TESTING IMPROVED TES-070 DESCRIPTIONS")
    print("=" * 80)
    
    # Use the same logic as the updated TES-070 generator
    cursor.execute("""
        SELECT ss.step_order, 
               ss.step_description as original_desc,
               CASE 
                   WHEN LOWER(COALESCE(ts.step_type, ss.step_type)) LIKE '%input%' 
                        AND (LOWER(ss.step_description) LIKE '%password%' 
                             OR LOWER(ts.description) LIKE '%password%'
                             OR LOWER(ts.name) LIKE '%password%')
                   THEN 'Password'
                   WHEN ss.step_description IS NULL OR LENGTH(TRIM(ss.step_description)) <= 5
                   THEN COALESCE(ts.description, ss.step_description, 'Step')
                   ELSE ss.step_description
               END as improved_desc,
               COALESCE(ts.step_type, ss.step_type) as step_type,
               ts.description as test_step_desc
        FROM scenario_steps ss
        LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
        WHERE ss.rice_profile = '11' AND ss.scenario_number = 1
        ORDER BY ss.step_order
    """)
    
    steps = cursor.fetchall()
    print(f"Total steps: {len(steps)}")
    print("\nStep filtering analysis with improved descriptions:")
    print("-" * 120)
    
    kept_count = 0
    wait_filtered = 0
    short_filtered = 0
    
    for i, (order, original, improved, step_type, test_desc) in enumerate(steps, 1):
        # Apply filtering logic
        step_type_lower = (step_type or '').lower()
        improved_lower = (improved or '').lower()
        
        is_wait_step = 'wait' in step_type_lower
        is_short = len((improved or '').strip()) <= 5
        
        status = "KEPT"
        if is_wait_step:
            status = "FILTERED (WAIT)"
            wait_filtered += 1
        elif is_short:
            status = "FILTERED (SHORT)"
            short_filtered += 1
        else:
            kept_count += 1
        
        print(f"Step {i:2d}: {status:15}")
        print(f"  Original: '{original}'")
        print(f"  Improved: '{improved}'")
        print(f"  Type:     '{step_type}'")
        if original != improved:
            print(f"  -> DESCRIPTION IMPROVED")
        print()
    
    print("=" * 80)
    print("FILTERING SUMMARY WITH IMPROVEMENTS:")
    print(f"Total steps: {len(steps)}")
    print(f"Wait steps filtered: {wait_filtered}")
    print(f"Short steps filtered: {short_filtered}")
    print(f"Steps kept in TES-070: {kept_count}")
    print(f"Improvement: {kept_count} steps (vs 15 before)")
    
    conn.close()

if __name__ == "__main__":
    test_improved_descriptions()