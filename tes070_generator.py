#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches
import tkinter as tk
from tkinter import filedialog
from database_manager import DatabaseManager

def generate_tes070_report(rice_profile, show_popup=None, current_user=None, db_manager=None):
    """Generate TES-070 and save to database only (no file download)"""
    
    # Show loading dialog
    loading_popup = None
    if show_popup:
        import tkinter as tk
        from rice_dialogs import center_dialog
        
        # Create loading dialog
        loading_popup = tk.Toplevel()
        loading_popup.title("Generating TES-070")
        center_dialog(loading_popup, 400, 236)
        loading_popup.configure(bg='#ffffff')
        loading_popup.resizable(False, False)
        loading_popup.grab_set()
        
        try:
            loading_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(loading_popup, bg='#3b82f6', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="📄 Generating TES-070 Report", 
                               font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(loading_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Loading message
        loading_label = tk.Label(content_frame, text="Please wait while generating your TES-070 report...\n\nSaving to database for version control.", 
                                font=('Segoe UI', 10), bg='#ffffff', justify="center")
        loading_label.pack(pady=(10, 20))
        
        # Progress indicator
        progress_label = tk.Label(content_frame, text="●●●", 
                                 font=('Segoe UI', 16), bg='#ffffff', fg='#3b82f6')
        progress_label.pack()
        
        # Animate the progress dots
        def animate_dots():
            current = progress_label.cget('text')
            if current == "●●●":
                progress_label.config(text="○●●")
            elif current == "○●●":
                progress_label.config(text="○○●")
            elif current == "○○●":
                progress_label.config(text="○○○")
            else:
                progress_label.config(text="●●●")
            
            if loading_popup.winfo_exists():
                loading_popup.after(300, animate_dots)
        
        # Start animation
        animate_dots()
        loading_popup.update()
        
        # Record start time for minimum 5-second display
        import time
        start_time = time.time()
    
    try:
        # Database path
        db_path = r"d:\AmazonQ\InforQ\RICE_Tester\fsm_tester.db"
        template_path = r"d:\AmazonQ\InforQ\RICE_Tester\TES-070-Template\TES-070_Custom_Extension_Unit_Test_Results_v2.0.docx"
    
        if not os.path.exists(db_path):
            if loading_popup and loading_popup.winfo_exists():
                elapsed_time = time.time() - start_time
                if elapsed_time < 5.0:
                    remaining_time = int((5.0 - elapsed_time) * 1000)
                    loading_popup.after(remaining_time, loading_popup.destroy)
                else:
                    loading_popup.destroy()
            if show_popup:
                show_popup("Error", "Database not found", "error")
            return
            
        if not os.path.exists(template_path):
            if loading_popup and loading_popup.winfo_exists():
                elapsed_time = time.time() - start_time
                if elapsed_time < 5.0:
                    remaining_time = int((5.0 - elapsed_time) * 1000)
                    loading_popup.after(remaining_time, loading_popup.destroy)
                else:
                    loading_popup.destroy()
            if show_popup:
                show_popup("Error", "TES-070 template not found", "error")
            return
        
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check for "not run" scenarios
        if rice_profile:
            cursor.execute("""
                SELECT COUNT(*) FROM scenarios s
                JOIN rice_profiles rp ON s.rice_profile = rp.id
                WHERE (rp.id = ? OR rp.rice_id = ?) AND (s.result IS NULL OR s.result = 'Not run')
            """, (rice_profile, rice_profile))
            not_run_count = cursor.fetchone()[0]
            
            if not_run_count > 0:
                cursor.execute("SELECT rice_id FROM rice_profiles WHERE id = ? OR rice_id = ?", (rice_profile, rice_profile))
                rice_id_result = cursor.fetchone()
                display_rice_id = rice_id_result[0] if rice_id_result else rice_profile
                
                if show_popup:
                    show_popup(
                        "Cannot Generate TES-070", 
                        f"Cannot generate TES-070 report for RICE {display_rice_id}.\n\n"
                        f"Found {not_run_count} scenario(s) with 'Not run' status.\n\n"
                        "Please execute all scenarios before generating the report.",
                        "error"
                    )
                conn.close()
                if loading_popup and loading_popup.winfo_exists():
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 5.0:
                        remaining_time = int((5.0 - elapsed_time) * 1000)
                        loading_popup.after(remaining_time, loading_popup.destroy)
                    else:
                        loading_popup.destroy()
                return
        
        # Get scenario data
        if rice_profile:
            cursor.execute("""
                SELECT s.rice_profile, s.scenario_number, s.description, s.result, s.executed_at
                FROM scenarios s
                JOIN rice_profiles rp ON s.rice_profile = rp.id
                WHERE s.result IS NOT NULL AND (rp.id = ? OR rp.rice_id = ?)
                ORDER BY s.scenario_number
            """, (rice_profile, rice_profile))
        else:
            cursor.execute("""
                SELECT rice_profile, scenario_number, description, result, executed_at
                FROM scenarios 
                WHERE result IS NOT NULL
                ORDER BY rice_profile, scenario_number
            """)
        
        scenarios = cursor.fetchall()
        
        if not scenarios:
            msg = f"No executed scenarios found for RICE {rice_profile}" if rice_profile else "No executed scenarios found"
            if show_popup:
                show_popup("Warning", msg, "warning")
            conn.close()
            if loading_popup and loading_popup.winfo_exists():
                elapsed_time = time.time() - start_time
                if elapsed_time < 5.0:
                    remaining_time = int((5.0 - elapsed_time) * 1000)
                    loading_popup.after(remaining_time, loading_popup.destroy)
                else:
                    loading_popup.destroy()
            return
        
        # Calculate test statistics
        total_tests = len(scenarios)
        passed_tests = sum(1 for s in scenarios if s[3] == "Passed")
        failed_tests = total_tests - passed_tests
        
        # Load template
        doc = Document(template_path)
        
        # Get RICE profile info
        cursor.execute("SELECT name, rice_id, client_name, tenant FROM rice_profiles WHERE rice_id = ?", (rice_profile,))
        rice_data = cursor.fetchone()
        
        if not rice_data:
            cursor.execute("SELECT name, rice_id, client_name, tenant FROM rice_profiles WHERE id = ?", (rice_profile,))
            rice_data = cursor.fetchone()
        
        if rice_data:
            rice_name, actual_rice_id, client_name, tenant_name = rice_data
            client_name = client_name or "Client Name Not Set"
            tenant_name = tenant_name or "Tenant Not Set"
        else:
            rice_name = f"RICE {rice_profile}"
            actual_rice_id = rice_profile
            client_name = "Client Name Not Set"
            tenant_name = "Tenant Not Set"
        
        # Replace placeholders in document (same logic as original function)
        user_full_name = current_user.get('full_name', 'User Name Not Set') if current_user else 'User Name Not Set'
        
        # First pass: Update all FR titles with actual scenario descriptions
        for i, para in enumerate(doc.paragraphs):
            if para.text.startswith('FR ') and any(x in para.text for x in ['1.1', '1.2', '1.3']):
                # Extract FR number (1.1, 1.2, 1.3)
                fr_number = None
                for num in ['1.1', '1.2', '1.3']:
                    if num in para.text:
                        fr_number = f'FR {num}'
                        scenario_index = int(num.split('.')[1]) - 1  # Convert to 0-based index
                        break
                
                if fr_number and scenario_index < len(scenarios):
                    scenario_desc = scenarios[scenario_index][2]  # Get scenario description
                    para.text = f'{fr_number}\t{scenario_desc}'
        
        for para in doc.paragraphs:
            if '<Client Name>' in para.text:
                para.text = para.text.replace('<Client Name>', client_name)
            if '<RICE ID Description>' in para.text:
                para.text = para.text.replace('<RICE ID Description>', f'RICE-{actual_rice_id}: {rice_name}')
            if '<Requirement Definition Narrative>' in para.text:
                # Check if this is an FR section and use scenario description
                if para.text.startswith('FR '):
                    for num in ['1.1', '1.2', '1.3']:
                        if num in para.text:
                            scenario_index = int(num.split('.')[1]) - 1
                            if scenario_index < len(scenarios):
                                scenario_desc = scenarios[scenario_index][2]
                                para.text = para.text.replace('<Requirement Definition Narrative>', scenario_desc)
                            break
                else:
                    para.text = para.text.replace('<Requirement Definition Narrative>', f'Automated testing for {rice_name}')

            if '<Scenario Description>' in para.text:
                para.text = para.text.replace('<Scenario Description>', 'Automated test scenario execution')
            if '<Passed/Failed>' in para.text:
                para.text = para.text.replace('<Passed/Failed>', 'See test results table below')
            if '<Screenshots and navigation>' in para.text:
                para.text = para.text.replace('<Screenshots and navigation>', 'Screenshots captured during automated execution')
            if '<Issue Description>' in para.text:
                para.text = para.text.replace('<Issue Description>', 'No issues identified during testing')
            if '<Description of proposed resolution>' in para.text:
                para.text = para.text.replace('<Description of proposed resolution>', 'N/A - All tests passed')
            if '<Author>' in para.text:
                para.text = para.text.replace('<Author>', user_full_name)
        
        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if '<Functional/Technical Resource>' in cell.text:
                        user_full_name = current_user.get('full_name', 'User Name Not Set') if current_user else 'User Name Not Set'
                        cell.text = cell.text.replace('<Functional/Technical Resource>', user_full_name)
                    if '<Tenant>' in cell.text:
                        cell.text = cell.text.replace('<Tenant>', tenant_name)
                    if '<Version>' in cell.text:
                        cell.text = cell.text.replace('<Version>', '1.0')
                    if 'MM/dd/yyyy' in cell.text:
                        current_date = datetime.now().strftime('%m/%d/%Y')
                        cell.text = cell.text.replace('MM/dd/yyyy', current_date)
                    if '<No. of scenarios>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios>', str(total_tests))
                    if '<No. of scenarios completed>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios completed>', str(total_tests))
                    if '<No. of scenarios that passed testing>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios that passed testing>', str(passed_tests))
                    if '<No. of scenarios that failed testing>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios that failed testing>', str(failed_tests))
        
        # Update summary table
        summary_table = doc.tables[4]
        summary_row = summary_table.rows[1]
        summary_row.cells[0].text = str(total_tests)
        summary_row.cells[1].text = str(total_tests)
        summary_row.cells[2].text = "100%"
        summary_row.cells[3].text = str(passed_tests)
        summary_row.cells[4].text = str(failed_tests)
        summary_row.cells[5].text = f"{(passed_tests/total_tests*100):.0f}%" if total_tests > 0 else "0%"
        
        # FINAL FIX: Process document systematically - populate ALL FR sections
        
        # Step 1: Replace all "Automated testing for Asset Accounts Extract" with scenario descriptions
        for para in doc.paragraphs:
            if 'Automated testing for Asset Accounts Extract' in para.text:
                if scenarios:
                    para.text = scenarios[0][2]  # Use first scenario description
        
        # Step 2: Replace <Steps and Screenshots> with actual steps for EACH FR section
        for para in doc.paragraphs:
            if '<Steps and Screenshots>' in para.text:
                # Determine which FR section this is by looking at preceding paragraphs
                fr_section = None
                scenario_index = 0
                
                # Look backwards to find the FR section header
                para_index = list(doc.paragraphs).index(para)
                for i in range(para_index - 1, -1, -1):
                    prev_para = doc.paragraphs[i]
                    if prev_para.text.startswith('FR 1.1'):
                        fr_section = 'FR 1.1'
                        scenario_index = 0
                        break
                    elif prev_para.text.startswith('FR 1.2'):
                        fr_section = 'FR 1.2'
                        scenario_index = 1
                        break
                    elif prev_para.text.startswith('FR 1.3'):
                        fr_section = 'FR 1.3'
                        scenario_index = 2
                        break
                
                # Only populate if we have a scenario for this FR section
                if fr_section and scenario_index < len(scenarios):
                    rice_prof, scenario_num, description, result, executed_at = scenarios[scenario_index]
                    
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
                        # Build steps content with actual screenshots
                        steps_content = "\n\nTEST EXECUTION STEPS:\n\n"
                        
                        # Filter out wait steps first, then renumber
                        filtered_steps = []
                        for step_order, step_desc, screenshot_b64 in steps_data:
                            if step_desc and 'wait' not in step_desc.lower():
                                filtered_steps.append((step_desc, screenshot_b64))
                        
                        # Build text content with proper numbering
                        for i, (step_desc, screenshot_b64) in enumerate(filtered_steps, 1):
                            steps_content += f"Step {i}: {step_desc}\n"
                            if screenshot_b64:
                                steps_content += "[Screenshot will be inserted here]\n"
                            steps_content += "\n"
                        
                        steps_content += f"\nResult: {result}\nExecution Date: {executed_at or 'Not recorded'}"
                        para.text = para.text.replace('<Steps and Screenshots>', steps_content)
                    else:
                        para.text = para.text.replace('<Steps and Screenshots>', '\n\nNo detailed steps recorded for this scenario.\nTest executed via automated framework.')
                else:
                    # Remove placeholder if no corresponding scenario
                    para.text = para.text.replace('<Steps and Screenshots>', '')
        
        # Step 3: Remove unused FR sections dynamically (only if fewer scenarios than FR sections)
        if len(scenarios) < 3:
            fr_sections_to_remove = []
            if len(scenarios) == 1:
                fr_sections_to_remove = ['FR 1.2', 'FR 1.3']
            elif len(scenarios) == 2:
                fr_sections_to_remove = ['FR 1.3']
            
            # Remove from TOC first (paragraphs with toc 2 style)
            toc_paragraphs_to_remove = []
            for i, para in enumerate(doc.paragraphs):
                if para.style.name == 'toc 2':
                    for fr_to_remove in fr_sections_to_remove:
                        if para.text.startswith(fr_to_remove):
                            toc_paragraphs_to_remove.append(i)
                            break
            
            # Remove TOC entries in reverse order
            for para_index in reversed(toc_paragraphs_to_remove):
                p = doc.paragraphs[para_index]
                p._element.getparent().remove(p._element)
            
            # Find and remove unused FR sections from content
            paragraphs_to_remove = []
            i = 0
            while i < len(doc.paragraphs):
                para = doc.paragraphs[i]
                
                # Check if this FR section should be removed
                for fr_to_remove in fr_sections_to_remove:
                    if para.text.startswith(fr_to_remove) and para.style.name != 'toc 2':
                        # Mark this FR section and all its content for removal
                        j = i
                        while j < len(doc.paragraphs):
                            # Stop when we hit the next FR section or section 4
                            if j > i and (doc.paragraphs[j].text.startswith('FR ') or doc.paragraphs[j].text.startswith('4\t')):
                                break
                            paragraphs_to_remove.append(j)
                            j += 1
                        i = j - 1  # Skip to after this section
                        break
                i += 1
            
            # Remove content paragraphs in reverse order to maintain indices
            for para_index in reversed(sorted(set(paragraphs_to_remove))):
                if para_index < len(doc.paragraphs):
                    p = doc.paragraphs[para_index]
                    p._element.getparent().remove(p._element)
        
        # Save to database only
        def save_to_database():
            if loading_popup and loading_popup.winfo_exists():
                loading_popup.destroy()
            
            try:
                from io import BytesIO
                buffer = BytesIO()
                doc.save(buffer)
                buffer.seek(0)
                file_content = buffer.getvalue()
                
                # Save to database using provided db_manager
                user_name = current_user.get('full_name', 'Current User') if current_user else 'Current User'
                version_id = db_manager.save_tes070_version(rice_profile, file_content, user_name)
                
                if show_popup:
                    show_popup("Success", f"TES-070 report generated and saved to database!\n\nVersion ID: {version_id}\nUse TES-070 History to download.", "success")
                    
            except Exception as e:
                if show_popup:
                    show_popup("Error", f"Failed to save TES-070: {str(e)}", "error")
        
        # Schedule save after minimum loading time
        if loading_popup and loading_popup.winfo_exists():
            elapsed_time = time.time() - start_time
            if elapsed_time < 5.0:
                remaining_time = int((5.0 - elapsed_time) * 1000)
                loading_popup.after(remaining_time, save_to_database)
            else:
                save_to_database()
        else:
            save_to_database()
        
        conn.close()
        
    except Exception as e:
        if loading_popup and loading_popup.winfo_exists():
            elapsed_time = time.time() - start_time
            if elapsed_time < 5.0:
                remaining_time = int((5.0 - elapsed_time) * 1000)
                loading_popup.after(remaining_time, loading_popup.destroy)
            else:
                loading_popup.destroy()
        if show_popup:
            show_popup("Error", f"Failed to generate report: {str(e)}", "error")



if __name__ == "__main__":
    # Create simple GUI for testing
    root = tk.Tk()
    root.withdraw()
    generate_tes070_report()