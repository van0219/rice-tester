#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches
import tkinter as tk
from tkinter import filedialog
# Import will be handled through parameter passing

def generate_tes070_report(rice_profile=None, show_popup=None):
    """Generate TES-070 report from RICE Tester database"""
    
    # Show loading dialog
    loading_popup = None
    if show_popup:
        import tkinter as tk
        from rice_dialogs import center_dialog
        
        # Create loading dialog (increased height by 0.5 inch = 36 pixels)
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
        loading_label = tk.Label(content_frame, text="Please wait while generating your TES-070 report...\n\nThis may take a few moments.", 
                                font=('Segoe UI', 10), bg='#ffffff', justify="center")
        loading_label.pack(pady=(10, 20))
        
        # Progress indicator (simple animated dots)
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
        
        # Update the display
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
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "Database not found")
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
            else:
                from tkinter import messagebox
                messagebox.showerror("Error", "TES-070 template not found")
            return
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # First, check for "not run" scenarios in the selected RICE profile
        if rice_profile:
            # Try both rice_profile as ID and as rice_id
            cursor.execute("""
                SELECT COUNT(*) FROM scenarios s
                JOIN rice_profiles rp ON s.rice_profile = rp.id
                WHERE (rp.id = ? OR rp.rice_id = ?) AND (s.result IS NULL OR s.result = 'Not run')
            """, (rice_profile, rice_profile))
            not_run_count = cursor.fetchone()[0]
            
            if not_run_count > 0:
                # Get the actual RICE ID for the error message
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
                else:
                    from tkinter import messagebox
                    messagebox.showerror(
                        "Cannot Generate TES-070", 
                        f"Cannot generate TES-070 report for RICE {display_rice_id}.\n\n"
                        f"Found {not_run_count} scenario(s) with 'Not run' status.\n\n"
                        "Please execute all scenarios before generating the report."
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
        
        # Get scenario data (filter by rice_profile if provided)
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
            else:
                from tkinter import messagebox
                messagebox.showwarning("Warning", msg)
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
        pass_percentage = f"{(passed_tests/total_tests*100):.0f}%" if total_tests > 0 else "0%"
        
        # Load template
        doc = Document(template_path)
        
        # Get RICE profile info - rice_profile could be ID or rice_id
        # First try as rice_id (string)
        cursor.execute("SELECT name, rice_id FROM rice_profiles WHERE rice_id = ?", (rice_profile,))
        rice_data = cursor.fetchone()
        
        if not rice_data:
            # If not found, try as database ID (integer)
            cursor.execute("SELECT name, rice_id FROM rice_profiles WHERE id = ?", (rice_profile,))
            rice_data = cursor.fetchone()
        
        if rice_data:
            rice_name, actual_rice_id = rice_data
        else:
            rice_name = f"RICE {rice_profile}"
            actual_rice_id = rice_profile
        
        # Replace placeholders in paragraphs
        for para in doc.paragraphs:
            if '<Client Name>' in para.text:
                para.text = para.text.replace('<Client Name>', 'White Plains Hospital')
            if '<RICE ID Description>' in para.text:
                para.text = para.text.replace('<RICE ID Description>', f'RICE-{actual_rice_id}: {rice_name}')
            if '<Requirement Definition Narrative>' in para.text:
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
        
        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if '<Functional/Technical Resource>' in cell.text:
                        cell.text = cell.text.replace('<Functional/Technical Resource>', 'Van Anthony Silleza')
                    if '<Tenant>' in cell.text:
                        cell.text = cell.text.replace('<Tenant>', 'TAMICS10_AX1')
                    if '<Version>' in cell.text:
                        cell.text = cell.text.replace('<Version>', '1.0')
                    if '<No. of scenarios>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios>', str(total_tests))
                    if '<No. of scenarios completed>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios completed>', str(total_tests))
                    if '<No. of scenarios that passed testing>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios that passed testing>', str(passed_tests))
                    if '<No. of scenarios that failed testing>' in cell.text:
                        cell.text = cell.text.replace('<No. of scenarios that failed testing>', str(failed_tests))
        
        # Update summary table (Table 5) with actual counts
        summary_table = doc.tables[4]  # Table 5 based on analysis
        summary_row = summary_table.rows[1]
        summary_row.cells[0].text = str(total_tests)
        summary_row.cells[1].text = str(total_tests)
        summary_row.cells[2].text = "100%"
        summary_row.cells[3].text = str(passed_tests)
        summary_row.cells[4].text = str(failed_tests)
        summary_row.cells[5].text = f"{(passed_tests/total_tests*100):.0f}%" if total_tests > 0 else "0%"
        
        # Find and populate section 3 - CUSTOM EXTENSION UNIT TEST DETAILED RESULTS
        from docx.shared import Inches
        
        # Clear existing FR content and add scenario details under section 3
        for rice_prof, scenario_num, description, result, executed_at in scenarios:
            # Add scenario heading
            doc.add_heading(f'Scenario {scenario_num}: {description}', level=3)
            
            # Add scenario info
            doc.add_paragraph(f'Test ID: RICE-{actual_rice_id}-{scenario_num:02d}')
            doc.add_paragraph(f'Result: {"Pass" if result == "Passed" else "Fail"}')
            doc.add_paragraph(f'Execution Date: {executed_at or datetime.now().strftime("%Y-%m-%d")}')
            doc.add_paragraph()  # Spacing
            
            # Get steps and screenshots from database
            cursor.execute("""
                SELECT ss.step_order, ss.step_description, ss.screenshot_after
                FROM scenario_steps ss
                JOIN rice_profiles rp ON ss.rice_profile = rp.id
                WHERE (rp.id = ? OR rp.rice_id = ?) AND ss.scenario_number = ?
                ORDER BY ss.step_order
            """, (rice_prof, rice_prof, scenario_num))
            
            steps_data = cursor.fetchall()
            
            if steps_data:
                for step_order, step_desc, screenshot_b64 in steps_data:
                    # Add step description
                    doc.add_paragraph(f'Step {step_order}: {step_desc or "Test step execution"}')
                    
                    # Add screenshot if available
                    if screenshot_b64:
                        try:
                            import base64
                            
                            # Decode base64 screenshot
                            screenshot_data = base64.b64decode(screenshot_b64)
                            
                            # Save temporarily and add to document
                            temp_path = f"temp_screenshot_{scenario_num}_{step_order}.png"
                            with open(temp_path, 'wb') as f:
                                f.write(screenshot_data)
                            
                            doc.add_picture(temp_path, width=Inches(4))
                            
                            # Clean up temp file
                            os.remove(temp_path)
                            
                        except Exception as e:
                            doc.add_paragraph("[Screenshot available but could not be embedded]")
                    
                    doc.add_paragraph()  # Add spacing between steps
            else:
                doc.add_paragraph("No detailed steps recorded for this scenario.")
            
            doc.add_paragraph()  # Add spacing between scenarios
        
        # Ensure minimum 5-second loading display before showing file dialog
        def show_save_dialog():
            # Save file
            default_name = f"TES-070_RICE-{actual_rice_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx" if rice_profile else f"TES-070_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            
            # Close loading dialog first
            if loading_popup and loading_popup.winfo_exists():
                loading_popup.destroy()
            
            output_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word documents", "*.docx")],
                title="Save TES-070 Report",
                initialfile=default_name
            )
            
            if output_path:
                doc.save(output_path)
                if show_popup:
                    show_popup("Success", f"TES-070 report generated:\n{output_path}", "success")
                else:
                    from tkinter import messagebox
                    messagebox.showinfo("Success", f"TES-070 report generated:\n{output_path}")
        
        # Schedule file dialog after minimum loading time
        if loading_popup and loading_popup.winfo_exists():
            elapsed_time = time.time() - start_time
            if elapsed_time < 5.0:
                remaining_time = int((5.0 - elapsed_time) * 1000)
                loading_popup.after(remaining_time, show_save_dialog)
            else:
                show_save_dialog()
        else:
            show_save_dialog()
        
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
        else:
            from tkinter import messagebox
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

def show_tes070_dialog(rice_profile, show_popup=None):
    """Show TES-070 generation dialog for specific RICE profile"""
    generate_tes070_report(rice_profile, show_popup)

if __name__ == "__main__":
    # Create simple GUI for testing
    root = tk.Tk()
    root.withdraw()
    generate_tes070_report()