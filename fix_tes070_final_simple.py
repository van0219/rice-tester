#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# FINAL SIMPLE FIX: Replace the entire problematic section with working logic

import os

# Read current generator
with open('tes070_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire problematic section with simple working logic
old_section = '''        # Step 1: Remove unused FR sections FIRST (before any content population)
        if len(scenarios) < 3:
            # Simple approach: Remove <Steps and Screenshots> placeholders for unused FR sections
            steps_placeholders_to_remove = []
            if len(scenarios) == 1:
                # Keep only first <Steps and Screenshots>, remove 2nd and 3rd
                steps_placeholders_to_remove = [1, 2]  # Remove 2nd and 3rd occurrences
            elif len(scenarios) == 2:
                # Keep first two <Steps and Screenshots>, remove 3rd
                steps_placeholders_to_remove = [2]  # Remove 3rd occurrence
            
            # Find and remove unused <Steps and Screenshots> sections
            steps_count = 0
            paragraphs_to_remove = []
            
            for i, para in enumerate(doc.paragraphs):
                if '<Steps and Screenshots>' in para.text:
                    if steps_count in steps_placeholders_to_remove:
                        # Mark this paragraph and surrounding content for removal
                        # Look backwards to find the FR header
                        start_idx = i
                        for j in range(i-1, -1, -1):
                            if doc.paragraphs[j].text.startswith('FR 1.'):
                                start_idx = j
                                break
                        
                        # Look forwards to find the end (next FR section or section 4)
                        end_idx = len(doc.paragraphs)
                        for j in range(i+1, len(doc.paragraphs)):
                            if (doc.paragraphs[j].text.startswith('FR 1.') or 
                                doc.paragraphs[j].text.startswith('4\\t')):
                                end_idx = j
                                break
                        
                        # Mark all paragraphs in this section for removal
                        for k in range(start_idx, end_idx):
                            paragraphs_to_remove.append(k)
                    
                    steps_count += 1
            
            # Remove paragraphs in reverse order to maintain indices
            for para_index in reversed(sorted(set(paragraphs_to_remove))):
                if para_index < len(doc.paragraphs):
                    p = doc.paragraphs[para_index]
                    p._element.getparent().remove(p._element)'''

new_section = '''        # Step 1: SIMPLE FIX - Only process scenarios that exist
        # Don't remove sections, just don't populate unused ones'''

# Replace the section
new_content = content.replace(old_section, new_section)

# Also fix the step population logic to be simpler
old_population = '''        # Step 3: Replace <Steps and Screenshots> with actual steps - SIMPLE APPROACH
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

new_population = '''        # Step 3: ULTRA SIMPLE - Replace <Steps and Screenshots> only for scenarios that exist
        scenario_count = 0
        
        for para in doc.paragraphs:
            if '<Steps and Screenshots>' in para.text:
                # Only populate if we have a scenario for this occurrence
                if scenario_count < len(scenarios):
                    rice_prof, scenario_num, description, result, executed_at = scenarios[scenario_count]
                    
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
                        para.text = para.text.replace('<Steps and Screenshots>', steps_content)
                    else:
                        para.text = para.text.replace('<Steps and Screenshots>', '\\n\\nNo detailed steps recorded for this scenario.\\nTest executed via automated framework.')
                else:
                    # No scenario for this FR section - remove placeholder
                    para.text = para.text.replace('<Steps and Screenshots>', '')
                
                scenario_count += 1'''

# Replace the population logic
new_content = new_content.replace(old_population, new_population)

# Write back
with open('tes070_generator.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Applied ULTRA SIMPLE TES-070 fix!")
print("- Only populates <Steps and Screenshots> for scenarios that actually exist")
print("- First occurrence gets scenario 1, second gets scenario 2, etc.")
print("- Unused occurrences get empty content")