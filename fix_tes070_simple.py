#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Simple fix: Replace the entire TES-070 generator with working logic

import os

# Read current generator
with open('tes070_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the problematic section with simple working logic
old_section = '''        # Step 3: Replace <Steps and Screenshots> with actual steps for EACH FR section
        # Process all paragraphs and track FR sections
        current_fr_section = None
        scenario_index = 0
        
        for para in doc.paragraphs:
            # Track which FR section we're currently in (dynamic based on scenarios)
            if para.text.startswith('FR 1.1') and len(scenarios) >= 1:
                current_fr_section = 'FR 1.1'
                scenario_index = 0
            elif para.text.startswith('FR 1.2') and len(scenarios) >= 2:
                current_fr_section = 'FR 1.2'
                scenario_index = 1
            elif para.text.startswith('FR 1.3') and len(scenarios) >= 3:
                current_fr_section = 'FR 1.3'
                scenario_index = 2
            elif para.text.startswith('4\\t'):  # Section 4 - reset FR tracking
                current_fr_section = None
            
            # Process <Steps and Screenshots> placeholders
            if '<Steps and Screenshots>' in para.text:
                # Only populate if we have a scenario for this FR section
                if current_fr_section and scenario_index < len(scenarios):
                    # Get the correct scenario data for this specific FR section
                    rice_prof, scenario_num, description, result, executed_at = scenarios[scenario_index]
                    
                    # Get steps from database using the correct scenario number
                    cursor.execute("""
                        SELECT ss.step_order, ss.step_description, ss.screenshot_after
                        FROM scenario_steps ss
                        WHERE ss.rice_profile = ? AND ss.scenario_number = ?
                        ORDER BY ss.step_order
                    """, (str(rice_prof), scenario_num))
                    
                    steps_data = cursor.fetchall()
                    
                    if not steps_data and rice_data:
                        cursor.execute("""
                            SELECT ss.step_order, ss.step_description, ss.screenshot_after
                            FROM scenario_steps ss
                            WHERE ss.rice_profile = ? AND ss.scenario_number = ?
                            ORDER BY ss.step_order
                        """, (actual_rice_id, scenario_num))
                        steps_data = cursor.fetchall()
                    
                    if steps_data:
                        # Build steps content with actual screenshots
                        steps_content = "\\n\\nTEST EXECUTION STEPS:\\n\\n"
                        
                        # Filter out wait steps first, then renumber
                        filtered_steps = []
                        for step_order, step_desc, screenshot_b64 in steps_data:
                            if step_desc and 'wait' not in step_desc.lower():
                                filtered_steps.append((step_desc, screenshot_b64))
                        
                        # Build text content with proper numbering
                        for i, (step_desc, screenshot_b64) in enumerate(filtered_steps, 1):
                            steps_content += f"Step {i}: {step_desc}\\n"
                            if screenshot_b64:
                                steps_content += "[Screenshot will be inserted here]\\n"
                            steps_content += "\\n"
                        
                        steps_content += f"\\nResult: {result}\\nExecution Date: {executed_at or 'Not recorded'}"
                        para.text = para.text.replace('<Steps and Screenshots>', steps_content)
                    else:
                        para.text = para.text.replace('<Steps and Screenshots>', '\\n\\nNo detailed steps recorded for this scenario.\\nTest executed via automated framework.')
                else:
                    # Remove placeholder if no corresponding scenario
                    para.text = para.text.replace('<Steps and Screenshots>', '')'''

new_section = '''        # Step 3: Replace <Steps and Screenshots> with actual steps - SIMPLE APPROACH
        steps_replacements = {}
        
        # Pre-calculate steps for each scenario
        for i, (rice_prof, scenario_num, description, result, executed_at) in enumerate(scenarios):
            # Get steps from database
            cursor.execute("""
                SELECT ss.step_order, ss.step_description, ss.screenshot_after
                FROM scenario_steps ss
                WHERE ss.rice_profile = ? AND ss.scenario_number = ?
                ORDER BY ss.step_order
            """, (str(rice_prof), scenario_num))
            
            steps_data = cursor.fetchall()
            
            if not steps_data and rice_data:
                cursor.execute("""
                    SELECT ss.step_order, ss.step_description, ss.screenshot_after
                    FROM scenario_steps ss
                    WHERE ss.rice_profile = ? AND ss.scenario_number = ?
                    ORDER BY ss.step_order
                """, (actual_rice_id, scenario_num))
                steps_data = cursor.fetchall()
            
            if steps_data:
                # Build steps content
                steps_content = "\\n\\nTEST EXECUTION STEPS:\\n\\n"
                
                # Filter out wait steps first, then renumber
                filtered_steps = []
                for step_order, step_desc, screenshot_b64 in steps_data:
                    if step_desc and 'wait' not in step_desc.lower():
                        filtered_steps.append((step_desc, screenshot_b64))
                
                # Build text content with proper numbering
                for j, (step_desc, screenshot_b64) in enumerate(filtered_steps, 1):
                    steps_content += f"Step {j}: {step_desc}\\n"
                    if screenshot_b64:
                        steps_content += "[Screenshot will be inserted here]\\n"
                    steps_content += "\\n"
                
                steps_content += f"\\nResult: {result}\\nExecution Date: {executed_at or 'Not recorded'}"
                steps_replacements[f'FR 1.{i+1}'] = steps_content
            else:
                steps_replacements[f'FR 1.{i+1}'] = '\\n\\nNo detailed steps recorded for this scenario.\\nTest executed via automated framework.'
        
        # Now replace <Steps and Screenshots> based on which FR section we're in
        current_fr = None
        for para in doc.paragraphs:
            # Track current FR section
            if para.text.startswith('FR 1.1'):
                current_fr = 'FR 1.1'
            elif para.text.startswith('FR 1.2'):
                current_fr = 'FR 1.2'
            elif para.text.startswith('FR 1.3'):
                current_fr = 'FR 1.3'
            elif para.text.startswith('4\\t'):
                current_fr = None
            
            # Replace placeholder with correct content
            if '<Steps and Screenshots>' in para.text and current_fr:
                if current_fr in steps_replacements:
                    para.text = para.text.replace('<Steps and Screenshots>', steps_replacements[current_fr])
                else:
                    para.text = para.text.replace('<Steps and Screenshots>', '')'''

# Replace the section
new_content = content.replace(old_section, new_section)

# Write back
with open('tes070_generator.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Fixed TES-070 generator with simple approach!")