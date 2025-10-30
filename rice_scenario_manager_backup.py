#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import os
from rice_dialogs import center_dialog

class ScenarioManager:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.selected_scenario_id = None
        self.selected_scenario_row = None
    
    def reset_scenario(self, scenario_id, current_profile, refresh_callback):
        """Reset scenario by clearing screenshots and setting status to 'Not run'"""
        scenarios = self.db_manager.get_scenarios(current_profile)
        scenario_info = None
        for scenario in scenarios:
            if scenario[0] == scenario_id:
                scenario_info = f"Scenario {scenario[1]} - {scenario[2]}"
                break
        
        if not scenario_info:
            self.show_popup("Error", "Scenario not found", "error")
            return
        
        confirm_popup = tk.Toplevel()
        confirm_popup.title("Confirm")
        center_dialog(confirm_popup, 400, 236)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(confirm_popup, bg='#f59e0b', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔄 Reset Scenario", font=('Segoe UI', 14, 'bold'), 
                bg='#f59e0b', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Reset scenario:\n'{scenario_info}'?\n\nThis will clear screenshots and reset status to 'Not run'.", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_reset():
            try:
                cursor = self.db_manager.conn.cursor()
                
                # Clear screenshots from scenario_steps and reset status
                cursor.execute("""
                    UPDATE scenario_steps 
                    SET screenshot_before = NULL, screenshot_after = NULL, 
                        screenshot_timestamp = NULL, execution_status = NULL
                    WHERE user_id = ? AND rice_profile = ? AND scenario_number = (
                        SELECT scenario_number FROM scenarios WHERE id = ?
                    )
                """, (self.db_manager.user_id, str(current_profile), scenario_id))
                
                # Reset scenario status
                cursor.execute("UPDATE scenarios SET result = 'Not run', executed_at = NULL WHERE id = ?", (scenario_id,))
                
                self.db_manager.conn.commit()
                confirm_popup.destroy()
                
                # Auto-refresh scenarios table
                refresh_callback()
                
                self.show_popup("Success", "Scenario reset successfully! Screenshots cleared and status set to 'Not run'.", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to reset scenario: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Reset", font=('Segoe UI', 10, 'bold'), bg='#f59e0b', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_reset).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
    
    def delete_scenario(self, scenario_id, current_profile, refresh_callback):
        """Delete scenario with confirmation"""
        scenarios = self.db_manager.get_scenarios(current_profile)
        scenario_info = None
        for scenario in scenarios:
            if scenario[0] == scenario_id:
                scenario_info = f"Scenario {scenario[1]} - {scenario[2]}"
                break
        
        if not scenario_info:
            self.show_popup("Error", "Scenario not found", "error")
            return
        
        confirm_popup = tk.Toplevel()
        center_dialog(confirm_popup, 400, 236)
        confirm_popup.title("Confirm")
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.attributes('-topmost', True)
        confirm_popup.resizable(False, False)
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Delete Scenario", font=('Segoe UI', 14, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Delete scenario:\n'{scenario_info}'?\n\nThis action cannot be undone.", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                cursor = self.db_manager.conn.cursor()
                
                # Get the scenario number being deleted
                cursor.execute("SELECT scenario_number FROM scenarios WHERE id = ?", (scenario_id,))
                deleted_scenario_number = cursor.fetchone()[0]
                
                # Delete scenario steps and scenario
                cursor.execute("DELETE FROM scenario_steps WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?", (self.db_manager.user_id, str(current_profile), deleted_scenario_number))
                cursor.execute("DELETE FROM scenarios WHERE id = ?", (scenario_id,))
                
                # Renumber remaining scenarios to maintain sequential numbering
                cursor.execute("""
                    SELECT id, scenario_number FROM scenarios 
                    WHERE user_id = ? AND rice_profile = ? AND scenario_number > ?
                    ORDER BY scenario_number
                """, (self.db_manager.user_id, str(current_profile), deleted_scenario_number))
                
                scenarios_to_renumber = cursor.fetchall()
                
                # Update scenario numbers and corresponding scenario_steps
                for scenario_id_to_update, old_number in scenarios_to_renumber:
                    new_number = old_number - 1
                    
                    # Update scenario number
                    cursor.execute("UPDATE scenarios SET scenario_number = ? WHERE id = ?", (new_number, scenario_id_to_update))
                    
                    # Update scenario_steps table
                    cursor.execute("UPDATE scenario_steps SET scenario_number = ? WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?", 
                                 (new_number, self.db_manager.user_id, str(current_profile), old_number))
                
                self.db_manager.conn.commit()
                confirm_popup.destroy()
                
                # Auto-refresh scenarios table
                refresh_callback()
                
                self.show_popup("Success", "Scenario deleted successfully! Remaining scenarios renumbered.", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete scenario: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
    
    def download_file(self, file_path):
        """Download file from scenario using save dialog"""
        try:
            from tkinter import filedialog
            import shutil
            
            if os.path.exists(file_path):
                # Get original filename
                original_name = os.path.basename(file_path)
                
                # Custom confirmation dialog
                self._show_download_confirmation(file_path, original_name)
            else:
                self.show_popup("Error", f"File not found: {file_path}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to save file: {str(e)}", "error")
    
    def _show_download_confirmation(self, file_path, original_name):
        """Show custom download confirmation dialog"""
        confirm_popup = tk.Toplevel()
        confirm_popup.title("Download File")
        center_dialog(confirm_popup, 400, 200)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.attributes('-topmost', True)
        confirm_popup.resizable(False, False)
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        header_frame = tk.Frame(confirm_popup, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📥 Download File", font=('Segoe UI', 14, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Do you want to download:\n'{original_name}'?", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def proceed_download():
            confirm_popup.destroy()
            from tkinter import filedialog
            import shutil
            
            save_path = filedialog.asksaveasfilename(
                title="Save File As",
                initialfile=original_name,
                defaultextension=os.path.splitext(original_name)[1],
                filetypes=[("All Files", "*.*")]
            )
            
            if save_path:
                shutil.copy2(file_path, save_path)
                self.show_popup("Success", f"File saved to: {save_path}", "success")
        
        tk.Button(btn_frame, text="Yes, Download", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=proceed_download).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
    
    def select_scenario(self, scenario_id, ui_components):
        """Handle scenario selection for highlighting"""
        # Reset previous selection
        if hasattr(self, 'selected_scenario_row') and self.selected_scenario_row:
            try:
                # Reset to normal alternating colors
                row_index = list(ui_components['scenarios_scroll_frame'].winfo_children()).index(self.selected_scenario_row)
                normal_color = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
                self.selected_scenario_row.configure(bg=normal_color)
                # Update all child widgets except column separators and View buttons
                for child in self.selected_scenario_row.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_width() != 1:
                        # Don't change background of View buttons
                        try:
                            if hasattr(child, 'cget') and child.cget('text') == 'View':
                                continue
                        except tk.TclError:
                            pass
                        child.configure(bg=normal_color)
            except (ValueError, tk.TclError):
                pass
        
        # Set new selection
        self.selected_scenario_id = scenario_id
        
        # Find and highlight the clicked row using scenario_id tag
        for row_widget in ui_components['scenarios_scroll_frame'].winfo_children():
            if hasattr(row_widget, 'scenario_id') and row_widget.scenario_id == scenario_id:
                # Highlight this row
                row_widget.configure(bg='#dbeafe')
                for child in row_widget.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_width() != 1:
                        # Don't change background of View buttons
                        try:
                            if hasattr(child, 'cget') and child.cget('text') == 'View':
                                continue
                        except tk.TclError:
                            pass
                        child.configure(bg='#dbeafe')
                self.selected_scenario_row = row_widget
                break
    
    def view_scenario_steps(self, scenario_id, scenario_number, current_profile):
        """View steps for a scenario with pagination (10 steps per page)"""
        popup = tk.Toplevel()
        popup.title(f"Scenario #{scenario_number} - Steps")
        center_dialog(popup, 800, 600)
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Header
        tk.Label(frame, text=f"Scenario #{scenario_number} - Test Steps", 
                font=('Segoe UI', 14, 'bold'), bg='#ffffff').pack(pady=(0, 20))
        
        # Steps container
        steps_container = tk.Frame(frame, bg='#ffffff')
        steps_container.pack(fill='both', expand=True, pady=(0, 20))
        
        # Headers
        headers_frame = tk.Frame(steps_container, bg='#e5e7eb', height=30)
        headers_frame.pack(fill='x')
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="Step", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0, y=8, relwidth=0.08)
        tk.Label(headers_frame, text="Name", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.08, y=8, relwidth=0.25)
        tk.Label(headers_frame, text="Type", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.33, y=8, relwidth=0.15)
        tk.Label(headers_frame, text="Target", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.48, y=8, relwidth=0.35)
        tk.Label(headers_frame, text="Status", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.83, y=8, relwidth=0.17)
        
        # Steps scroll frame
        steps_scroll_frame = tk.Frame(steps_container, bg='#ffffff')
        steps_scroll_frame.pack(fill='both', expand=True)
        
        # Pagination variables
        current_page = 1
        steps_per_page = 10
        all_steps = []
        
        # Get all steps from database
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT step_order, step_name, step_type, step_target, execution_status
                FROM scenario_steps 
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                ORDER BY step_order
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            all_steps = cursor.fetchall()
        except Exception as e:
            tk.Label(steps_scroll_frame, text=f"Error loading steps: {str(e)}", 
                    font=('Segoe UI', 10), bg='#ffffff', fg='#ef4444').pack(pady=20)
            all_steps = []
        
        def load_steps_page():
            """Load steps for current page"""
            # Clear existing steps
            for widget in steps_scroll_frame.winfo_children():
                widget.destroy()
            
            if not all_steps:
                tk.Label(steps_scroll_frame, text="No steps found for this scenario", 
                        font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280').pack(pady=20)
                return
            
            # Calculate pagination
            total_steps = len(all_steps)
            total_pages = max(1, (total_steps + steps_per_page - 1) // steps_per_page)
            start_index = (current_page - 1) * steps_per_page
            end_index = min(start_index + steps_per_page, total_steps)
            
            # Display steps for current page
            page_steps = all_steps[start_index:end_index]
            
            for i, step in enumerate(page_steps):
                step_order, step_name, step_type, step_target, execution_status = step
                bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
                
                row_frame = tk.Frame(steps_scroll_frame, bg=bg_color, height=30)
                row_frame.pack(fill='x', pady=1)
                row_frame.pack_propagate(False)
                
                # Step number
                tk.Label(row_frame, text=str(step_order), font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10).place(relx=0, y=8, relwidth=0.08)
                
                # Step name
                tk.Label(row_frame, text=step_name or '', font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10).place(relx=0.08, y=8, relwidth=0.25)
                
                # Step type
                tk.Label(row_frame, text=step_type or '', font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10).place(relx=0.33, y=8, relwidth=0.15)
                
                # Target (truncated)
                target_display = (step_target[:40] + "...") if step_target and len(step_target) > 40 else step_target or ''
                tk.Label(row_frame, text=target_display, font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10).place(relx=0.48, y=8, relwidth=0.35)
                
                # Status
                status = execution_status or 'Pending'
                status_color = '#10b981' if status == 'completed' else '#f59e0b' if status == 'pending' else '#ef4444'
                tk.Label(row_frame, text=status.title(), font=('Segoe UI', 9), 
                        bg=bg_color, fg=status_color, anchor='w', padx=10).place(relx=0.83, y=8, relwidth=0.17)
            
            # Update pagination info
            page_label.config(text=f"Page {current_page} of {total_pages} ({total_steps} steps total)")
            
            # Update button states
            prev_btn.config(state='normal' if current_page > 1 else 'disabled')
            next_btn.config(state='normal' if current_page < total_pages else 'disabled')
        
        def prev_page():
            nonlocal current_page
            if current_page > 1:
                current_page -= 1
                load_steps_page()
        
        def next_page():
            nonlocal current_page
            total_pages = max(1, (len(all_steps) + steps_per_page - 1) // steps_per_page)
            if current_page < total_pages:
                current_page += 1
                load_steps_page()
        
        # Pagination controls
        pagination_frame = tk.Frame(frame, bg='#ffffff')
        pagination_frame.pack(fill='x', pady=(0, 20))
        
        # Previous button
        prev_btn = tk.Button(pagination_frame, text="◀ Previous", font=('Segoe UI', 9), 
                            bg='#6b7280', fg='#ffffff', relief='flat', padx=10, pady=4, 
                            cursor='hand2', bd=0, command=prev_page)
        prev_btn.pack(side='left')
        
        # Page info
        page_label = tk.Label(pagination_frame, text="Page 1 of 1 (0 steps total)", 
                             font=('Segoe UI', 9), bg='#ffffff', fg='#374151')
        page_label.pack(side='left', padx=20)
        
        # Next button
        next_btn = tk.Button(pagination_frame, text="Next ▶", font=('Segoe UI', 9), 
                            bg='#6b7280', fg='#ffffff', relief='flat', padx=10, pady=4, 
                            cursor='hand2', bd=0, command=next_page)
        next_btn.pack(side='left')
        
        # Load first page
        load_steps_page()
        
        # Close button
        tk.Button(frame, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack()
    
    def run_scenario(self, scenario_id, current_profile):
        """Run a single scenario with enhanced debugging"""
        import traceback
        from datetime import datetime
        
        # Create debug log file
        debug_log_path = os.path.join("Temp", f"debug_run_scenario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        def debug_log(message, level="INFO"):
            """Write debug message to both console and file"""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] [{level}] {message}"
            print(log_message)
            
            try:
                with open(debug_log_path, "a", encoding="utf-8") as f:
                    f.write(log_message + "\n")
            except Exception as e:
                print(f"Failed to write to debug log: {e}")
        
        debug_log("=== STARTING DEBUG RUN SCENARIO ===")
        debug_log(f"Scenario ID: {scenario_id}")
        debug_log(f"Current Profile: {current_profile}")
        
        from screenshot_executor import ScreenshotExecutor
        
        try:
            # Get scenario details and steps
            debug_log("Connecting to database...")
            cursor = self.db_manager.conn.cursor()
            debug_log("Database connection successful")
            
            debug_log("Querying scenario details...")
            cursor.execute("""
                SELECT scenario_number, description FROM scenarios 
                WHERE id = ? AND user_id = ?
            """, (scenario_id, self.db_manager.user_id))
            scenario_data = cursor.fetchone()
            debug_log(f"Scenario query result: {scenario_data}")
            
            if not scenario_data:
                debug_log("ERROR: Scenario not found", "ERROR")
                self.show_popup("Error", "Scenario not found", "error")
                return
            
            scenario_number, description = scenario_data
            debug_log(f"Scenario Number: {scenario_number}, Description: {description}")
            
            # Get scenario steps
            debug_log("Querying scenario steps...")
            cursor.execute("""
                SELECT step_name, step_type, step_target, step_description, 
                       COALESCE(user_input_required, 0) as user_input_required
                FROM scenario_steps 
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                ORDER BY step_order
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            steps = cursor.fetchall()
            debug_log(f"Found {len(steps)} steps")
            
            for i, step in enumerate(steps):
                debug_log(f"Step {i+1}: {step}")
            
            if not steps:
                debug_log("WARNING: No steps found", "WARNING")
                self.show_popup("No Steps", "This scenario has no test steps to execute.", "warning")
                return
            
            # Create SIMPLE execution dialog with debug enhancements
            debug_log("Creating execution dialog...")
            popup = tk.Toplevel()
            popup.title(f"Execute Scenario #{scenario_number}")
            center_dialog(popup, 600, 400)  # Much smaller for visibility
            popup.configure(bg='#ffffff')
            popup.grab_set()
            debug_log("Execution dialog created")
            
            try:
                popup.iconbitmap("infor_logo.ico")
                debug_log("Icon set successfully")
            except Exception as e:
                debug_log(f"Failed to set icon: {e}", "WARNING")
            
            main_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
            main_frame.pack(fill="both", expand=True)
            
            # Simple header
            tk.Label(main_frame, text=f"Execute Scenario #{scenario_number}", 
                    font=('Segoe UI', 16, 'bold'), bg='#ffffff', fg='#333333').pack(pady=(0, 10))
            
            # Description
            tk.Label(main_frame, text=description, font=('Segoe UI', 11), 
                    bg='#ffffff', wraplength=550, justify="center").pack(pady=(0, 20))
            
            # Steps info
            tk.Label(main_frame, text=f"This scenario has {len(steps)} test steps", 
                    font=('Segoe UI', 10), bg='#ffffff', fg='#666666').pack(pady=(0, 20))
            
            # Progress display
            progress_label = tk.Label(main_frame, text="Ready to execute...", 
                                    font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#333333')
            progress_label.pack(pady=(0, 20))
            
            # Debug output (smaller)
            debug_output = tk.Text(main_frame, height=6, font=('Consolas', 9), 
                                 bg='#f8f9fa', relief='solid', bd=1)
            debug_output.pack(fill="x", pady=(0, 20))
            
            def add_debug_output(message):
                timestamp = datetime.now().strftime("%H:%M:%S")
                debug_output.insert(tk.END, f"[{timestamp}] {message}\n")
                debug_output.see(tk.END)
                popup.update()
            
            add_debug_output("Ready to execute scenario with debug logging")
            
            step_widgets = []  # Simplified - no visual step widgets
            
            # Execution controls
            btn_frame = tk.Frame(main_frame, bg='#ffffff')
            btn_frame.pack(fill="x")
            
            execution_running = False
            
            def start_execution():
                nonlocal execution_running
                if execution_running:
                    add_debug_output("Execution already running, ignoring request")
                    return
                
                execution_running = True
                add_debug_output("=== STARTING DEBUG EXECUTION ===")
                progress_label.config(text="Starting execution...", fg='#dc2626')
                popup.update()
                
                try:
                    add_debug_output(f"Creating ScreenshotExecutor with params:")
                    add_debug_output(f"  user_id: {self.db_manager.user_id}")
                    add_debug_output(f"  rice_profile: {current_profile}")
                    add_debug_output(f"  scenario_number: {scenario_number}")
                    
                    executor = ScreenshotExecutor(self.db_manager.user_id, current_profile, scenario_number)
                    add_debug_output("ScreenshotExecutor created successfully")
                    debug_log("ScreenshotExecutor created successfully")
                    
                    total_steps = len(steps)
                    completed_steps = 0
                    
                    def progress_callback(current_step, total_steps, step_name, message):
                        nonlocal completed_steps
                        
                        add_debug_output(f"PROGRESS: Step {current_step}/{total_steps}: {step_name} - {message}")
                        debug_log(f"PROGRESS: Step {current_step}/{total_steps}: {step_name} - {message}")
                        
                        # Create display message
                        if len(message) > 40:
                            display_message = f"Step {current_step}/{total_steps}: {step_name} - {message[:40]}..."
                        else:
                            display_message = f"Step {current_step}/{total_steps}: {step_name} - {message}"
                        
                        # current_step_label.config(text=display_message, fg='#dc2626')  # Fixed: variable not defined
                        
                        # Update progress display
                        progress_label.config(text=display_message, fg='#dc2626')
                        popup.update()
                    
                    add_debug_output("Setting progress callback...")
                    executor.set_progress_callback(progress_callback)
                    add_debug_output("Progress callback set, starting execution...")
                    debug_log("Starting scenario execution...")
                    
                    # Execute scenario
                    success = executor.execute_scenario()
                    add_debug_output(f"Execution completed. Success: {success}")
                    debug_log(f"Scenario execution completed. Success: {success}")
                    
                    # Final status update
                    if success:
                        progress_label.config(text="Execution completed successfully!", fg='#10b981')
                        add_debug_output("=== EXECUTION SUCCESSFUL ===")
                        
                        # Update scenario status
                        cursor.execute("""
                            UPDATE scenarios SET result = 'Passed', executed_at = CURRENT_TIMESTAMP 
                            WHERE id = ?
                        """, (scenario_id,))
                        self.db_manager.conn.commit()
                        add_debug_output("Scenario status updated to Passed")
                        debug_log("Scenario status updated to Passed")
                    else:
                        progress_label.config(text="Execution failed - Check debug output", fg='#ef4444')
                        add_debug_output("=== EXECUTION FAILED ===")
                        cursor.execute("""
                            UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                            WHERE id = ?
                        """, (scenario_id,))
                        self.db_manager.conn.commit()
                        add_debug_output("Scenario status updated to Failed")
                        debug_log("Scenario status updated to Failed")
                        
                except Exception as e:
                    error_msg = str(e)
                    traceback_msg = traceback.format_exc()
                    
                    add_debug_output(f"=== EXECUTION ERROR ===")
                    add_debug_output(f"Error: {error_msg}")
                    add_debug_output(f"Traceback: {traceback_msg}")
                    
                    progress_label.config(text=f"Error: {error_msg}", fg='#ef4444')
                    debug_log(f"EXECUTION ERROR: {error_msg}", "ERROR")
                    debug_log(f"TRACEBACK: {traceback_msg}", "ERROR")
                    
                    cursor.execute("""
                        UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (scenario_id,))
                    self.db_manager.conn.commit()
                
                execution_running = False
                add_debug_output("=== DEBUG EXECUTION COMPLETED ===")
            
            # BIG VISIBLE START BUTTON
            tk.Button(btn_frame, text="▶ START EXECUTION", font=('Segoe UI', 14, 'bold'), 
                     bg='#10b981', fg='#ffffff', relief='flat', padx=30, pady=15, 
                     cursor='hand2', bd=0, command=start_execution).pack(side="left", padx=(0, 10))
            
            def open_debug_log():
                try:
                    os.startfile(debug_log_path)
                except Exception as e:
                    add_debug_output(f"Failed to open debug log: {e}")
            
            tk.Button(btn_frame, text="Debug Log", font=('Segoe UI', 10, 'bold'), 
                     bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=10, 
                     cursor='hand2', bd=0, command=open_debug_log).pack(side="left", padx=(0, 10))
            
            tk.Button(btn_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=15, pady=10, 
                     cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
            
            debug_log("Debug execution dialog setup completed")
            add_debug_output("Debug dialog ready. Click 'DEBUG Start Execution' to begin.")
            
        except Exception as e:
            error_msg = str(e)
            traceback_msg = traceback.format_exc()
            debug_log(f"SETUP ERROR: {error_msg}", "ERROR")
            debug_log(f"SETUP TRACEBACK: {traceback_msg}", "ERROR")
            self.show_popup("Debug Error", f"Failed to setup debug execution: {error_msg}", "error")
    

    
    def edit_scenario(self, scenario_id, current_profile, refresh_callback):
        """Edit scenario with step management"""
        try:
            # Get scenario details including auto_login
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT scenario_number, description, file_path, COALESCE(auto_login, 0) as auto_login FROM scenarios 
                WHERE id = ? AND user_id = ?
            """, (scenario_id, self.db_manager.user_id))
            scenario_data = cursor.fetchone()
            
            if not scenario_data:
                self.show_popup("Error", "Scenario not found", "error")
                return
            
            scenario_number, description, file_path, auto_login = scenario_data
            
            # Get existing steps
            cursor.execute("""
                SELECT step_order, step_name, step_type, step_target, step_description
                FROM scenario_steps 
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                ORDER BY step_order
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            existing_steps = cursor.fetchall()
            
            # Create edit dialog
            popup = tk.Toplevel()
            popup.title(f"Edit Scenario #{scenario_number}")
            center_dialog(popup, 900, 700)
            popup.configure(bg='#ffffff')
            popup.grab_set()
            
            try:
                popup.iconbitmap("infor_logo.ico")
            except:
                pass
            
            main_frame = tk.Frame(popup, bg='#ffffff')
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Header
            tk.Label(main_frame, text=f"Edit Scenario #{scenario_number}", 
                    font=('Segoe UI', 16, 'bold'), bg='#ffffff').pack(pady=(0, 20))
            
            # Create two-column layout
            content_frame = tk.Frame(main_frame, bg='#ffffff')
            content_frame.pack(fill="both", expand=True)
            
            # Left column - Scenario details
            left_frame = tk.Frame(content_frame, bg='#ffffff')
            left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            tk.Label(left_frame, text="Scenario Details", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
            
            # Description
            tk.Label(left_frame, text="Description:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            desc_entry = tk.Entry(left_frame, width=40, font=('Segoe UI', 10))
            desc_entry.insert(0, description or '')
            desc_entry.pack(fill="x", pady=(0, 10))
            
            # File path (optional)
            tk.Label(left_frame, text="File Path (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            file_frame = tk.Frame(left_frame, bg='#ffffff')
            file_frame.pack(fill="x", pady=(0, 20))
            
            file_entry = tk.Entry(file_frame, font=('Segoe UI', 10))
            file_entry.insert(0, file_path or '')
            file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            def browse_file():
                from tkinter import filedialog
                file_path = filedialog.askopenfilename(
                    title="Select File",
                    filetypes=[("All Files", "*.*")]
                )
                if file_path:
                    file_entry.delete(0, tk.END)
                    file_entry.insert(0, file_path)
            
            tk.Button(file_frame, text="Browse", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=10, pady=4, cursor='hand2', bd=0, command=browse_file).pack(side='right')
            
            # Auto-login checkbox
            auto_login_var = tk.BooleanVar(value=bool(auto_login))
            tk.Checkbutton(left_frame, text="Include Login (Add login steps as initial steps)", 
                          variable=auto_login_var, font=('Segoe UI', 10), bg='#ffffff').pack(anchor="w", pady=(10, 10))
            
            # Login credentials frame (for editing login step values)
            login_creds_frame = tk.Frame(left_frame, bg='#ffffff')
            login_creds_frame.pack(fill="x", pady=(0, 20))
            
            tk.Label(login_creds_frame, text="Username:", font=('Segoe UI', 10), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=2)
            username_entry = tk.Entry(login_creds_frame, width=20, font=('Segoe UI', 10))
            username_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)
            
            tk.Label(login_creds_frame, text="Password:", font=('Segoe UI', 10), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=2)
            password_entry = tk.Entry(login_creds_frame, width=20, font=('Segoe UI', 10), show="•")
            password_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)
            
            login_creds_frame.grid_columnconfigure(1, weight=1)
            
            # Extract existing login credentials if they exist
            existing_username = ""
            existing_password = ""
            for step in existing_steps:
                if step[2] == 'Text Input':  # step_type
                    if 'username' in step[1].lower():  # step_name
                        existing_username = step[4] or ""  # step_description
                    elif 'password' in step[1].lower():
                        existing_password = step[4] or ""
            
            username_entry.insert(0, existing_username)
            password_entry.insert(0, existing_password)
            
            # Show/hide login credentials based on auto_login
            if not auto_login:
                login_creds_frame.pack_forget()
            
            # Right column - Step management
            right_frame = tk.Frame(content_frame, bg='#ffffff')
            right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
            
            tk.Label(right_frame, text="Test Steps Management", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
            
            # Current steps display
            current_steps_frame = tk.LabelFrame(right_frame, text=f"Current Steps ({len(existing_steps)})", font=('Segoe UI', 10, 'bold'), bg='#ffffff')
            current_steps_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Create scrollable listbox for current steps
            steps_listbox = tk.Listbox(current_steps_frame, font=('Segoe UI', 9), height=15)
            steps_scrollbar = ttk.Scrollbar(current_steps_frame, orient="vertical", command=steps_listbox.yview)
            steps_listbox.configure(yscrollcommand=steps_scrollbar.set)
            
            steps_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            steps_scrollbar.pack(side="right", fill="y")
            
            # Separate login steps from regular steps
            login_steps_data = []
            current_steps_data = []
            
            # Check if existing steps include login steps (first 4 steps with specific patterns)
            has_login_steps = False
            if len(existing_steps) >= 4:
                first_four = existing_steps[:4]
                login_patterns = ['navigate', 'username', 'password', 'login']
                matches = sum(1 for i, step in enumerate(first_four) 
                             if any(pattern in step[1].lower() for pattern in [login_patterns[i]]))
                has_login_steps = matches >= 3  # At least 3 out of 4 match
            
            # Split steps into login and regular
            if has_login_steps and auto_login:
                login_steps_raw = existing_steps[:4]
                regular_steps_raw = existing_steps[4:]
                
                for step in login_steps_raw:
                    step_order, step_name, step_type, step_target, step_description = step
                    login_steps_data.append({
                        'order': step_order,
                        'name': step_name,
                        'type': step_type,
                        'target': step_target,
                        'description': step_description
                    })
            else:
                regular_steps_raw = existing_steps
            
            # Load regular steps
            for step in regular_steps_raw:
                step_order, step_name, step_type, step_target, step_description = step
                current_steps_data.append({
                    'order': step_order,
                    'name': step_name,
                    'type': step_type,
                    'target': step_target,
                    'description': step_description
                })
            
            def get_login_steps():
                """Get the standard login steps with current credentials"""
                username = username_entry.get().strip() if username_entry.get() else "[username]"
                password = password_entry.get().strip() if password_entry.get() else "[password]"
                
                return [
                    {'order': 1, 'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                    {'order': 2, 'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': username},
                    {'order': 3, 'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': password},
                    {'order': 4, 'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                ]
            
            def update_steps_display():
                """Update the steps listbox display"""
                steps_listbox.delete(0, tk.END)
                
                step_counter = 1
                
                # Add login steps if enabled
                if auto_login_var.get():
                    current_login_steps = get_login_steps()
                    for login_step in current_login_steps:
                        display_text = f"{step_counter}. {login_step['name']} ({login_step['type']}) [LOGIN]"
                        if login_step['type'] == 'Text Input' and login_step['description']:
                            is_password = 'password' in login_step['name'].lower()
                            if is_password:
                                display_text += f" - Value: {'•' * len(login_step['description'])}"
                            else:
                                display_text += f" - Value: '{login_step['description']}'"
                        steps_listbox.insert(tk.END, display_text)
                        step_counter += 1
                
                # Add regular steps
                for step in current_steps_data:
                    display_text = f"{step_counter}. {step['name']} ({step['type']})"
                    if step['type'] == 'Text Input' and step.get('description'):
                        is_password = 'password' in step['name'].lower()
                        if is_password:
                            display_text += f" - Value: {'•' * len(step['description'])}"
                        else:
                            display_text += f" - Value: '{step['description']}'"
                    steps_listbox.insert(tk.END, display_text)
                    step_counter += 1
                
                current_steps_frame.config(text=f"Current Steps ({step_counter - 1})")
            
            def toggle_login_display():
                """Toggle login credentials and steps display"""
                if auto_login_var.get():
                    login_creds_frame.pack(fill="x", pady=(0, 20))
                else:
                    login_creds_frame.pack_forget()
                update_steps_display()
            
            # Bind events
            auto_login_var.trace('w', lambda *args: toggle_login_display())
            username_entry.bind('<KeyRelease>', lambda *args: update_steps_display() if auto_login_var.get() else None)
            password_entry.bind('<KeyRelease>', lambda *args: update_steps_display() if auto_login_var.get() else None)
            
            # Initial display
            update_steps_display()
            
            # Step management buttons
            step_mgmt_frame = tk.Frame(right_frame, bg='#ffffff')
            step_mgmt_frame.pack(fill="x", pady=(0, 10))
            
            def add_new_step():
                # Add step dialog
                step_popup = tk.Toplevel(popup)
                step_popup.title("Add Test Step")
                center_dialog(step_popup, 500, 350)
                step_popup.configure(bg='#ffffff')
                step_popup.attributes('-topmost', True)
                step_popup.resizable(False, False)
                step_popup.grab_set()
                
                try:
                    step_popup.iconbitmap("infor_logo.ico")
                except:
                    pass
                
                step_frame = tk.Frame(step_popup, bg='#ffffff', padx=20, pady=20)
                step_frame.pack(fill="both", expand=True)
                
                tk.Label(step_frame, text="Add New Test Step", font=('Segoe UI', 14, 'bold'), bg='#ffffff').pack(pady=(0, 20))
                
                # Step fields
                tk.Label(step_frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                step_name_entry = tk.Entry(step_frame, width=50, font=('Segoe UI', 10))
                step_name_entry.pack(fill="x", pady=(0, 10))
                
                tk.Label(step_frame, text="Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                step_type_var = tk.StringVar()
                step_type_combo = ttk.Combobox(step_frame, textvariable=step_type_var, font=('Segoe UI', 10), state='readonly')
                step_type_combo['values'] = ['Navigate', 'Element Click', 'Text Input', 'JavaScript Execute', 'Wait', 'Screenshot']
                step_type_combo.pack(fill="x", pady=(0, 10))
                
                tk.Label(step_frame, text="Target:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                step_target_entry = tk.Entry(step_frame, width=50, font=('Segoe UI', 10))
                step_target_entry.pack(fill="x", pady=(0, 10))
                
                tk.Label(step_frame, text="Description:", font=('Segoe UI', 10), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                step_desc_entry = tk.Entry(step_frame, width=50, font=('Segoe UI', 10))
                step_desc_entry.pack(fill="x", pady=(0, 20))
                
                step_btn_frame = tk.Frame(step_frame, bg='#ffffff')
                step_btn_frame.pack()
                
                def save_new_step():
                    name = step_name_entry.get().strip()
                    step_type = step_type_var.get().strip()
                    target = step_target_entry.get().strip()
                    desc = step_desc_entry.get().strip()
                    
                    if not all([name, step_type, target]):
                        self.show_popup("Error", "Name, Type, and Target are required", "error")
                        return
                    
                    # Add to current steps
                    new_order = len(current_steps_data) + 1
                    current_steps_data.append({
                        'order': new_order,
                        'name': name,
                        'type': step_type,
                        'target': target,
                        'description': desc
                    })
                    
                    # Update display
                    update_steps_display()
                    
                    step_popup.destroy()
                
                tk.Button(step_btn_frame, text="Add Step", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_new_step).pack(side="left", padx=(0, 10))
                tk.Button(step_btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=step_popup.destroy).pack(side="left")
                
                step_name_entry.focus()
            
            def remove_selected_step():
                selection = steps_listbox.curselection()
                if selection:
                    index = selection[0]
                    login_step_count = 4 if auto_login_var.get() else 0
                    
                    if index < login_step_count:
                        self._show_child_popup(popup, "Info", "Login steps can only be removed by unchecking 'Include Login'", "warning")
                        return
                    
                    # Remove from regular steps
                    actual_index = index - login_step_count
                    if actual_index < len(current_steps_data):
                        current_steps_data.pop(actual_index)
                        # Renumber remaining steps
                        for i, step in enumerate(current_steps_data):
                            step['order'] = i + 1
                        update_steps_display()
            
            def move_step_up():
                selection = steps_listbox.curselection()
                if selection and selection[0] > 0:
                    index = selection[0]
                    login_step_count = 4 if auto_login_var.get() else 0
                    
                    # Can't move login steps or move regular steps above login steps
                    if index < login_step_count or index == login_step_count:
                        self._show_child_popup(popup, "Info", "Cannot move login steps or move steps above login steps", "warning")
                        return
                    
                    # Move within regular steps only
                    actual_index = index - login_step_count
                    if actual_index > 0:
                        current_steps_data[actual_index], current_steps_data[actual_index-1] = current_steps_data[actual_index-1], current_steps_data[actual_index]
                        # Renumber
                        for i, step in enumerate(current_steps_data):
                            step['order'] = i + 1
                        update_steps_display()
                        steps_listbox.selection_set(index-1)
            
            def move_step_down():
                selection = steps_listbox.curselection()
                if selection:
                    index = selection[0]
                    login_step_count = 4 if auto_login_var.get() else 0
                    total_steps = login_step_count + len(current_steps_data)
                    
                    # Can't move login steps
                    if index < login_step_count:
                        self._show_child_popup(popup, "Info", "Cannot move login steps", "warning")
                        return
                    
                    # Move within regular steps only
                    actual_index = index - login_step_count
                    if actual_index < len(current_steps_data) - 1:
                        current_steps_data[actual_index], current_steps_data[actual_index+1] = current_steps_data[actual_index+1], current_steps_data[actual_index]
                        # Renumber
                        for i, step in enumerate(current_steps_data):
                            step['order'] = i + 1
                        update_steps_display()
                        steps_listbox.selection_set(index+1)
            
            tk.Button(step_mgmt_frame, text="✏️ Edit Value", font=('Segoe UI', 9), bg='#3b82f6', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=lambda: self._edit_step_value(steps_listbox, current_steps_data, popup)).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="❌ Remove", font=('Segoe UI', 9), bg='#ef4444', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=remove_selected_step).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="⬆️ Up", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_up).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="⬇️ Down", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_down).pack(side="left")
            
            # Add from groups button
            tk.Button(right_frame, text="📋 Add from Test Groups", font=('Segoe UI', 10, 'bold'), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=15, pady=8, 
                     cursor='hand2', bd=0, command=lambda: self._add_steps_from_groups(current_steps_data, steps_listbox, current_steps_frame)).pack(fill="x", pady=(0, 20))
            
            # Bottom buttons
            btn_frame = tk.Frame(main_frame, bg='#ffffff')
            btn_frame.pack(fill="x", pady=(20, 0))
            
            def save_changes():
                new_description = desc_entry.get().strip()
                new_file_path = file_entry.get().strip() or None
                new_auto_login = auto_login_var.get()
                
                if not new_description:
                    self.show_popup("Error", "Please enter a description", "error")
                    return
                
                try:
                    # Update scenario details including auto_login
                    cursor.execute("""
                        UPDATE scenarios SET description = ?, file_path = ?, auto_login = ? 
                        WHERE id = ? AND user_id = ?
                    """, (new_description, new_file_path, new_auto_login, scenario_id, self.db_manager.user_id))
                    
                    # Delete existing steps
                    cursor.execute("""
                        DELETE FROM scenario_steps 
                        WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                    """, (self.db_manager.user_id, str(current_profile), scenario_number))
                    
                    # Insert login steps if enabled
                    step_order = 1
                    if new_auto_login:
                        login_steps = get_login_steps()
                        for login_step in login_steps:
                            cursor.execute("""
                                INSERT INTO scenario_steps 
                                (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                                  step_order, login_step['name'], login_step['type'], login_step['target'], login_step['description'], 1))
                            step_order += 1
                    
                    # Insert regular steps
                    for step in current_steps_data:
                        cursor.execute("""
                            INSERT INTO scenario_steps 
                            (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                              step_order, step['name'], step['type'], step['target'], step['description'], 1))
                        step_order += 1
                    
                    self.db_manager.conn.commit()
                    popup.destroy()
                    if refresh_callback:
                        refresh_callback()
                    total_steps = len(current_steps_data) + (4 if new_auto_login else 0)
                    self.show_popup("Success", f"Scenario #{scenario_number} updated with {total_steps} steps!", "success")
                    
                except Exception as e:
                    self.show_popup("Error", f"Failed to update scenario: {str(e)}", "error")
            
            tk.Button(btn_frame, text="💾 Save Changes", font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
            tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 12, 'bold'), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
            
            desc_entry.focus()
            desc_entry.select_range(0, tk.END)
            
        except Exception as e:
            self.show_popup("Error", f"Failed to edit scenario: {str(e)}", "error")
    
    def _edit_step_value(self, steps_listbox, current_steps_data, parent_window=None):
        """Edit input value for Text Input steps"""
        selection = steps_listbox.curselection()
        if not selection:
            if parent_window:
                self._show_child_popup(parent_window, "Error", "Please select a step to edit", "error")
            else:
                self.show_popup("Error", "Please select a step to edit", "error")
            return
        
        index = selection[0]
        step_data = current_steps_data[index]
        
        # Only allow editing Text Input steps
        if step_data['type'] != 'Text Input':
            if parent_window:
                self._show_child_popup(parent_window, "Info", "Only Text Input steps can have their values edited", "warning")
            else:
                self.show_popup("Info", "Only Text Input steps can have their values edited", "warning")
            return
        
        # Create edit value dialog
        edit_popup = tk.Toplevel()
        edit_popup.title("Edit Input Value")
        center_dialog(edit_popup, 400, 250)
        edit_popup.configure(bg='#ffffff')
        edit_popup.grab_set()
        
        try:
            edit_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        edit_frame = tk.Frame(edit_popup, bg='#ffffff', padx=20, pady=20)
        edit_frame.pack(fill="both", expand=True)
        
        tk.Label(edit_frame, text=f"Edit Value for: {step_data['name']}", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(pady=(0, 15))
        
        tk.Label(edit_frame, text="Input Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        
        # Determine if this is a password field
        is_password = 'password' in step_data['name'].lower()
        
        value_entry = tk.Entry(edit_frame, width=40, font=('Segoe UI', 10), 
                              show="•" if is_password else "")
        value_entry.insert(0, step_data.get('description', ''))
        value_entry.pack(fill="x", pady=(0, 20))
        
        edit_btn_frame = tk.Frame(edit_frame, bg='#ffffff')
        edit_btn_frame.pack()
        
        def save_value():
            new_value = value_entry.get()
            step_data['description'] = new_value
            
            # Update display
            display_text = f"{step_data['order']}. {step_data['name']} ({step_data['type']})"
            if new_value and step_data['type'] == 'Text Input':
                if is_password:
                    display_text += f" - Value: {'•' * len(new_value)}"
                else:
                    display_text += f" - Value: '{new_value}'"
            
            steps_listbox.delete(index)
            steps_listbox.insert(index, display_text)
            steps_listbox.selection_set(index)
            
            edit_popup.destroy()
        
        tk.Button(edit_btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_value).pack(side="left", padx=(0, 10))
        tk.Button(edit_btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=edit_popup.destroy).pack(side="left")
        
        value_entry.focus()
        value_entry.select_range(0, tk.END)
    
    def _add_steps_from_groups(self, current_steps_data, steps_listbox, current_steps_frame):
        """Add steps from test groups to scenario"""
        # Get test step groups
        groups = self.db_manager.get_test_step_groups()
        if not groups:
            self.show_popup("No Groups", "No test step groups found. Please create test groups first.", "warning")
            return
        
        # Create selection dialog
        select_popup = tk.Toplevel()
        select_popup.title("Add Steps from Test Groups")
        center_dialog(select_popup, 600, 500)
        select_popup.configure(bg='#ffffff')
        select_popup.attributes('-topmost', True)
        select_popup.resizable(False, False)
        select_popup.grab_set()
        
        try:
            select_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        select_frame = tk.Frame(select_popup, bg='#ffffff', padx=20, pady=20)
        select_frame.pack(fill="both", expand=True)
        
        tk.Label(select_frame, text="Select Steps from Test Groups", 
                font=('Segoe UI', 14, 'bold'), bg='#ffffff').pack(pady=(0, 15))
        
        # Group selection
        tk.Label(select_frame, text="Test Group:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        group_var = tk.StringVar()
        group_combo = ttk.Combobox(select_frame, textvariable=group_var, font=('Segoe UI', 10), state='readonly')
        group_names = [f"{group[1]} ({group[3]} steps)" for group in groups]
        group_combo['values'] = group_names
        group_combo.pack(fill="x", pady=(0, 10))
        
        # Available steps
        tk.Label(select_frame, text="Available Steps:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        steps_listbox_select = tk.Listbox(select_frame, font=('Segoe UI', 9), selectmode=tk.MULTIPLE, height=12)
        steps_listbox_select.pack(fill="both", expand=True, pady=(0, 15))
        
        def load_group_steps():
            if not group_var.get():
                return
            
            group_index = group_combo.current()
            if group_index >= 0:
                group_id = groups[group_index][0]
                steps = self.db_manager.get_test_steps_by_group(group_id)
                
                steps_listbox_select.delete(0, tk.END)
                for step in steps:
                    step_id, name, step_type, target, description = step
                    display_text = f"{name} ({step_type})"
                    steps_listbox_select.insert(tk.END, display_text)
        
        group_combo.bind('<<ComboboxSelected>>', lambda e: load_group_steps())
        
        # Buttons
        btn_frame = tk.Frame(select_frame, bg='#ffffff')
        btn_frame.pack()
        
        def add_selected():
            selection = steps_listbox_select.curselection()
            if not selection or not group_var.get():
                self.show_popup("Error", "Please select a group and steps", "error")
                return
            
            group_index = group_combo.current()
            group_id = groups[group_index][0]
            steps = self.db_manager.get_test_steps_by_group(group_id)
            
            for index in selection:
                if index < len(steps):
                    step_data = steps[index]
                    step_id, name, step_type, target, description = step_data
                    
                    # Add to current steps
                    new_order = len(current_steps_data) + 1
                    current_steps_data.append({
                        'order': new_order,
                        'name': name,
                        'type': step_type,
                        'target': target,
                        'description': description or ''
                    })
            
                # Update display
                update_steps_display()
            select_popup.destroy()
        
        tk.Button(btn_frame, text="Add Selected", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=add_selected).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=select_popup.destroy).pack(side="left")
    
    def add_scenario(self, current_profile, refresh_callback):
        """Add new scenario with test step selection from groups"""
        try:
            # Get next scenario number
            next_number = self.db_manager.get_next_scenario_number(current_profile)
            
            # Create add scenario dialog
            popup = tk.Toplevel()
            popup.title("Add Scenario")
            center_dialog(popup, 900, 700)
            popup.configure(bg='#ffffff')
            popup.grab_set()
            
            try:
                popup.iconbitmap("infor_logo.ico")
            except:
                pass
            
            main_frame = tk.Frame(popup, bg='#ffffff')
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Header
            tk.Label(main_frame, text=f"Add Scenario #{next_number}", 
                    font=('Segoe UI', 16, 'bold'), bg='#ffffff').pack(pady=(0, 20))
            
            # Create two-column layout
            content_frame = tk.Frame(main_frame, bg='#ffffff')
            content_frame.pack(fill="both", expand=True)
            
            # Left column - Scenario details
            left_frame = tk.Frame(content_frame, bg='#ffffff')
            left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
            
            tk.Label(left_frame, text="Scenario Details", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
            
            # Description
            tk.Label(left_frame, text="Description:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            desc_entry = tk.Entry(left_frame, width=40, font=('Segoe UI', 10))
            desc_entry.pack(fill="x", pady=(0, 10))
            
            # File path (optional)
            tk.Label(left_frame, text="File Path (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            file_frame = tk.Frame(left_frame, bg='#ffffff')
            file_frame.pack(fill="x", pady=(0, 10))
            
            file_entry = tk.Entry(file_frame, font=('Segoe UI', 10))
            file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            def browse_file():
                from tkinter import filedialog
                file_path = filedialog.askopenfilename(
                    title="Select File",
                    filetypes=[("All Files", "*.*")]
                )
                if file_path:
                    file_entry.delete(0, tk.END)
                    file_entry.insert(0, file_path)
            
            tk.Button(file_frame, text="Browse", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=10, pady=4, cursor='hand2', bd=0, command=browse_file).pack(side='right')
            
            # Include login checkbox
            include_login_var = tk.BooleanVar()
            login_frame = tk.Frame(left_frame, bg='#ffffff')
            login_frame.pack(fill="x", pady=(0, 10))
            
            tk.Checkbutton(login_frame, text="Include Login (Add login steps as initial steps)", 
                          variable=include_login_var, font=('Segoe UI', 10), bg='#ffffff').pack(anchor="w")
            
            # Login credentials (shown when checkbox is checked)
            login_creds_frame = tk.Frame(left_frame, bg='#ffffff')
            login_creds_frame.pack(fill="x", pady=(0, 10))
            
            tk.Label(login_creds_frame, text="Username:", font=('Segoe UI', 10), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=2)
            username_entry = tk.Entry(login_creds_frame, width=20, font=('Segoe UI', 10))
            username_entry.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=2)
            
            tk.Label(login_creds_frame, text="Password:", font=('Segoe UI', 10), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=2)
            password_entry = tk.Entry(login_creds_frame, width=20, font=('Segoe UI', 10), show="•")
            password_entry.grid(row=1, column=1, sticky="ew", padx=(10, 0), pady=2)
            
            login_creds_frame.grid_columnconfigure(1, weight=1)
            login_creds_frame.pack_forget()  # Initially hidden
            
            def toggle_login_creds():
                if include_login_var.get():
                    login_creds_frame.pack(fill="x", pady=(0, 10))
                    popup.geometry("900x750")  # Increase height
                    update_login_steps_display()
                else:
                    login_creds_frame.pack_forget()
                    popup.geometry("900x700")  # Original height
                    update_login_steps_display()
            
            include_login_var.trace('w', lambda *args: toggle_login_creds())
            
            # Right column - Test step selection
            right_frame = tk.Frame(content_frame, bg='#ffffff')
            right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
            
            tk.Label(right_frame, text="Select Test Steps", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
            
            # Test step groups dropdown
            tk.Label(right_frame, text="Test Step Group:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            group_var = tk.StringVar()
            group_combo = ttk.Combobox(right_frame, textvariable=group_var, font=('Segoe UI', 10), state='readonly')
            
            # Get test step groups
            groups = self.db_manager.get_test_step_groups()
            group_names = [f"{group[1]} ({group[3]} steps)" for group in groups]
            group_combo['values'] = group_names
            group_combo.pack(fill="x", pady=(0, 10))
            
            # Available steps frame
            available_frame = tk.LabelFrame(right_frame, text="Available Steps", font=('Segoe UI', 10, 'bold'), bg='#ffffff')
            available_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            available_listbox = tk.Listbox(available_frame, font=('Segoe UI', 9), selectmode=tk.MULTIPLE)
            available_listbox.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Selected steps frame
            selected_frame = tk.LabelFrame(right_frame, text="Selected Steps (Execution Order)", font=('Segoe UI', 10, 'bold'), bg='#ffffff')
            selected_frame.pack(fill="both", expand=True)
            
            selected_listbox = tk.Listbox(selected_frame, font=('Segoe UI', 9))
            selected_listbox.pack(fill="both", expand=True, padx=5, pady=5)
            
            # Step management buttons
            step_btn_frame = tk.Frame(right_frame, bg='#ffffff')
            step_btn_frame.pack(fill="x", pady=(10, 0))
            
            selected_steps = []  # Store selected step data
            login_steps_data = []  # Store login steps separately
            
            def get_login_steps():
                """Get the standard login steps"""
                username = username_entry.get().strip() if username_entry.get() else "[username]"
                password = password_entry.get().strip() if password_entry.get() else "[password]"
                
                return [
                    {'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                    {'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': username},
                    {'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': password},
                    {'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                ]
            
            def update_login_steps_display():
                """Update the display to show/hide login steps"""
                # Clear current display
                selected_listbox.delete(0, tk.END)
                
                # Update login steps data
                if include_login_var.get():
                    login_steps_data.clear()
                    login_steps_data.extend(get_login_steps())
                else:
                    login_steps_data.clear()
                
                # Rebuild display with login steps first, then selected steps
                step_counter = 1
                
                # Add login steps if enabled
                for login_step in login_steps_data:
                    display_text = f"{step_counter}. {login_step['name']} ({login_step['type']}) [LOGIN]"
                    if login_step['type'] == 'Text Input' and login_step['description']:
                        is_password = 'password' in login_step['name'].lower()
                        if is_password:
                            display_text += f" - Value: {'•' * len(login_step['description'])}"
                        else:
                            display_text += f" - Value: '{login_step['description']}'"
                    selected_listbox.insert(tk.END, display_text)
                    step_counter += 1
                
                # Add regular selected steps
                for step in selected_steps:
                    display_text = f"{step_counter}. {step['name']} ({step['type']})"
                    if step['type'] == 'Text Input' and step.get('description'):
                        is_password = 'password' in step['name'].lower()
                        if is_password:
                            display_text += f" - Value: {'•' * len(step['description'])}"
                        else:
                            display_text += f" - Value: '{step['description']}'"
                    selected_listbox.insert(tk.END, display_text)
                    step_counter += 1
            
            # Bind username/password changes to update login steps
            def on_credential_change(*args):
                if include_login_var.get():
                    update_login_steps_display()
            
            username_entry.bind('<KeyRelease>', on_credential_change)
            password_entry.bind('<KeyRelease>', on_credential_change)
            
            def load_group_steps():
                if not group_var.get():
                    return
                
                # Get group ID from selection
                group_index = group_combo.current()
                if group_index >= 0:
                    group_id = groups[group_index][0]
                    steps = self.db_manager.get_test_steps_by_group(group_id)
                    
                    available_listbox.delete(0, tk.END)
                    for step in steps:
                        step_id, name, step_type, target, description = step
                        display_text = f"{name} ({step_type})"
                        available_listbox.insert(tk.END, display_text)
            
            def add_selected_steps():
                selection = available_listbox.curselection()
                if not selection or not group_var.get():
                    return
                
                group_index = group_combo.current()
                group_id = groups[group_index][0]
                steps = self.db_manager.get_test_steps_by_group(group_id)
                
                for index in selection:
                    if index < len(steps):
                        step_data = steps[index]
                        step_id, name, step_type, target, description = step_data
                        
                        # Add to selected steps
                        selected_steps.append({
                            'step_id': step_id,
                            'name': name,
                            'type': step_type,
                            'target': target,
                            'description': description or ''
                        })
                
                # Refresh the entire display to maintain proper numbering
                update_login_steps_display()
            
            def remove_selected_step():
                selection = selected_listbox.curselection()
                if selection:
                    index = selection[0]
                    # Calculate which step to remove (accounting for login steps)
                    login_step_count = len(login_steps_data)
                    
                    if index < login_step_count:
                        # Can't remove login steps individually
                        self._show_child_popup(popup, "Info", "Login steps can only be removed by unchecking 'Include Login'", "warning")
                        return
                    else:
                        # Remove from selected steps
                        actual_index = index - login_step_count
                        if actual_index < len(selected_steps):
                            selected_steps.pop(actual_index)
                    
                    # Refresh display
                    update_login_steps_display()
            
            def move_step_up():
                selection = selected_listbox.curselection()
                if selection and selection[0] > 0:
                    index = selection[0]
                    login_step_count = len(login_steps_data)
                    
                    # Can't move login steps or move regular steps above login steps
                    if index < login_step_count or index == login_step_count:
                        self._show_child_popup(popup, "Info", "Cannot move login steps or move steps above login steps", "warning")
                        return
                    
                    # Move within selected steps only
                    actual_index = index - login_step_count
                    if actual_index > 0:
                        selected_steps[actual_index], selected_steps[actual_index-1] = selected_steps[actual_index-1], selected_steps[actual_index]
                        update_login_steps_display()
                        selected_listbox.selection_set(index-1)
            
            def move_step_down():
                selection = selected_listbox.curselection()
                if selection:
                    index = selection[0]
                    login_step_count = len(login_steps_data)
                    total_steps = login_step_count + len(selected_steps)
                    
                    # Can't move login steps
                    if index < login_step_count:
                        self._show_child_popup(popup, "Info", "Cannot move login steps", "warning")
                        return
                    
                    # Move within selected steps only
                    actual_index = index - login_step_count
                    if actual_index < len(selected_steps) - 1:
                        selected_steps[actual_index], selected_steps[actual_index+1] = selected_steps[actual_index+1], selected_steps[actual_index]
                        update_login_steps_display()
                        selected_listbox.selection_set(index+1)
            
            group_combo.bind('<<ComboboxSelected>>', lambda e: load_group_steps())
            
            def edit_selected_value():
                selection = selected_listbox.curselection()
                if not selection:
                    self._show_child_popup(popup, "Error", "Please select a step to edit", "error")
                    return
                
                index = selection[0]
                login_step_count = len(login_steps_data)
                
                # Determine if this is a login step or regular step
                if index < login_step_count:
                    step_data = login_steps_data[index]
                    is_login_step = True
                else:
                    step_data = selected_steps[index - login_step_count]
                    is_login_step = False
                
                if step_data['type'] != 'Text Input':
                    self._show_child_popup(popup, "Info", "Only Text Input steps can have their values edited", "warning")
                    return
                
                # Create edit dialog
                edit_popup = tk.Toplevel(popup)
                edit_popup.title("Edit Input Value")
                center_dialog(edit_popup, 400, 250)
                edit_popup.configure(bg='#ffffff')
                edit_popup.attributes('-topmost', True)
                edit_popup.resizable(False, False)
                edit_popup.grab_set()
                
                try:
                    edit_popup.iconbitmap("infor_logo.ico")
                except:
                    pass
                
                edit_frame = tk.Frame(edit_popup, bg='#ffffff', padx=20, pady=20)
                edit_frame.pack(fill="both", expand=True)
                
                tk.Label(edit_frame, text=f"Edit Value for: {step_data['name']}", 
                        font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(pady=(0, 15))
                
                tk.Label(edit_frame, text="Input Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                
                is_password = 'password' in step_data['name'].lower()
                value_entry = tk.Entry(edit_frame, width=40, font=('Segoe UI', 10), 
                                      show="•" if is_password else "")
                value_entry.insert(0, step_data.get('description', ''))
                value_entry.pack(fill="x", pady=(0, 20))
                
                edit_btn_frame = tk.Frame(edit_frame, bg='#ffffff')
                edit_btn_frame.pack()
                
                def save_value():
                    new_value = value_entry.get()
                    step_data['description'] = new_value
                    
                    # If editing login step, also update the entry fields
                    if is_login_step:
                        if 'username' in step_data['name'].lower():
                            username_entry.delete(0, tk.END)
                            username_entry.insert(0, new_value)
                        elif 'password' in step_data['name'].lower():
                            password_entry.delete(0, tk.END)
                            password_entry.insert(0, new_value)
                    
                    # Refresh display
                    update_login_steps_display()
                    selected_listbox.selection_set(index)
                    
                    edit_popup.destroy()
                
                tk.Button(edit_btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_value).pack(side="left", padx=(0, 10))
                tk.Button(edit_btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=edit_popup.destroy).pack(side="left")
                
                value_entry.focus()
                value_entry.select_range(0, tk.END)
            
            tk.Button(step_btn_frame, text="▶️ Add Selected", font=('Segoe UI', 9), bg='#10b981', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=add_selected_steps).pack(side="left", padx=(0, 5))
            tk.Button(step_btn_frame, text="✏️ Edit Value", font=('Segoe UI', 9), bg='#3b82f6', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=edit_selected_value).pack(side="left", padx=(0, 5))
            tk.Button(step_btn_frame, text="❌ Remove", font=('Segoe UI', 9), bg='#ef4444', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=remove_selected_step).pack(side="left", padx=(0, 5))
            tk.Button(step_btn_frame, text="↑ Up", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_up).pack(side="left", padx=(0, 5))
            tk.Button(step_btn_frame, text="↓ Down", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_down).pack(side="left")
            
            # Bottom buttons
            btn_frame = tk.Frame(main_frame, bg='#ffffff')
            btn_frame.pack(fill="x", pady=(20, 0))
            
            def save_scenario():
                description = desc_entry.get().strip()
                file_path = file_entry.get().strip() or None
                include_login = include_login_var.get()
                
                if not description:
                    self.show_popup("Error", "Please enter a description", "error")
                    return
                
                try:
                    # Save scenario
                    scenario_id = self.db_manager.save_scenario(
                        current_profile, next_number, description, file_path, include_login
                    )
                    
                    # Save selected steps
                    step_order = 1
                    
                    # Add login steps if requested
                    if include_login:
                        username = username_entry.get().strip()
                        password = password_entry.get().strip()
                        
                        if username and password:
                            # Add login steps
                            login_steps = [
                                {'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': username},
                                {'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': username},
                                {'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': password},
                                {'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                            ]
                            
                            for login_step in login_steps:
                                cursor = self.db_manager.conn.cursor()
                                cursor.execute("""
                                    INSERT INTO scenario_steps 
                                    (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (self.db_manager.user_id, str(current_profile), next_number, step_order, 
                                      login_step['name'], login_step['type'], login_step['target'], login_step['description'], 1))
                                step_order += 1
                    
                    # Add selected test steps
                    for step in selected_steps:
                        cursor = self.db_manager.conn.cursor()
                        cursor.execute("""
                            INSERT INTO scenario_steps 
                            (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (self.db_manager.user_id, str(current_profile), next_number, step_order, 
                              step['name'], step['type'], step['target'], step['description'], 1))
                        step_order += 1
                    
                    self.db_manager.conn.commit()
                    popup.destroy()
                    if refresh_callback:
                        refresh_callback()
                    self.show_popup("Success", f"Scenario #{next_number} created with {len(selected_steps) + (4 if include_login and username and password else 0)} steps!", "success")
                    
                except Exception as e:
                    self.show_popup("Error", f"Failed to create scenario: {str(e)}", "error")
            
            tk.Button(btn_frame, text="💾 Save Scenario", font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=save_scenario).pack(side="left", padx=(0, 10))
            tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 12, 'bold'), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
            
            desc_entry.focus()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to add scenario: {str(e)}", "error")
    
    def _show_child_popup(self, parent_window, title, message, status):
        """Show popup as child of parent window"""
        popup = tk.Toplevel(parent_window)
        popup.title(title)
        popup.configure(bg='#ffffff')
        popup.attributes('-topmost', True)
        popup.resizable(False, False)
        popup.transient(parent_window)
        popup.grab_set()
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Status colors
        if status == "success":
            icon = "✅"
            color = "#10b981"
        elif status == "warning":
            icon = "⚠️"
            color = "#f59e0b"
        else:
            icon = "❌"
            color = "#ef4444"
        
        # Header
        header_frame = tk.Frame(popup, bg=color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"{icon} {title}", font=('Segoe UI', 12, 'bold'), 
                bg=color, fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=message, font=('Segoe UI', 10), bg='#ffffff', 
                justify="center", wraplength=280).pack(pady=(0, 15))
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=6, cursor='hand2', bd=0, command=popup.destroy).pack()
        
        # Center relative to parent
        parent_window.update_idletasks()
        x = parent_window.winfo_x() + (parent_window.winfo_width() // 2) - 160
        y = parent_window.winfo_y() + (parent_window.winfo_height() // 2) - 90
        popup.geometry(f"320x180+{x}+{y}")
        
        popup.focus_set()
    
    def run_all_scenarios(self, current_profile):
        """Run all scenarios for the selected RICE profile"""
        from screenshot_executor import ScreenshotExecutor
        
        try:
            # Get all scenarios for this profile
            scenarios = self.db_manager.get_scenarios(current_profile)
            
            if not scenarios:
                self.show_popup("No Scenarios", "No scenarios found for this RICE profile.", "warning")
                return
            
            # Create execution dialog
            popup = tk.Toplevel()
            popup.title("Run All Scenarios")
            center_dialog(popup, 672, 622)
            popup.configure(bg='#ffffff')
            popup.grab_set()
            
            try:
                popup.iconbitmap("infor_logo.ico")
            except:
                pass
            
            frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
            frame.pack(fill="both", expand=True)
            
            # Header
            tk.Label(frame, text=f"Run All Scenarios ({len(scenarios)} scenarios)", 
                    font=('Segoe UI', 14, 'bold'), bg='#ffffff').pack(pady=(0, 20))
            
            # Progress label
            progress_label = tk.Label(frame, text="Ready to execute all scenarios...", 
                                    font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
            progress_label.pack(pady=(0, 10))
            
            # Progress details
            details_text = tk.Text(frame, height=15, width=70, font=('Segoe UI', 9), 
                                  bg='#f9fafb', relief='solid', bd=1)
            details_text.pack(fill='both', expand=True, pady=(0, 20))
            
            # Buttons
            btn_frame = tk.Frame(frame, bg='#ffffff')
            btn_frame.pack()
            
            def start_execution():
                progress_label.config(text="Starting execution of all scenarios...", fg='#f59e0b')
                details_text.delete(1.0, tk.END)
                popup.update()
                
                try:
                    executor = ScreenshotExecutor(self.db_manager)
                    total_scenarios = len(scenarios)
                    passed_count = 0
                    failed_count = 0
                    
                    for i, scenario in enumerate(scenarios, 1):
                        scenario_id, scenario_number, description, result, file_path = scenario
                        
                        details_text.insert(tk.END, f"\n=== Scenario {scenario_number}: {description} ===\n")
                        details_text.see(tk.END)
                        popup.update()
                        
                        def progress_callback(message):
                            # Handle multi-line progress messages
                            if len(message) > 40:
                                lines = message.split(' - ')
                                if len(lines) >= 2:
                                    progress_label.config(text=f"Scenario {i}/{total_scenarios}: {lines[0]}")
                                    details_text.insert(tk.END, f"  {lines[1]}\n")
                                else:
                                    progress_label.config(text=f"Scenario {i}/{total_scenarios}: {message[:40]}...")
                                    details_text.insert(tk.END, f"  {message}\n")
                            else:
                                progress_label.config(text=f"Scenario {i}/{total_scenarios}: {message}")
                                details_text.insert(tk.END, f"  {message}\n")
                            details_text.see(tk.END)
                            popup.update()
                        
                        try:
                            success = executor.execute_scenario_steps(
                                self.db_manager.user_id, current_profile, scenario_number, progress_callback
                            )
                            
                            if success:
                                passed_count += 1
                                details_text.insert(tk.END, f"  ✅ Scenario {scenario_number} PASSED\n\n")
                                # Update scenario status
                                cursor = self.db_manager.conn.cursor()
                                cursor.execute("""
                                    UPDATE scenarios SET result = 'Passed', executed_at = CURRENT_TIMESTAMP 
                                    WHERE id = ?
                                """, (scenario_id,))
                                self.db_manager.conn.commit()
                            else:
                                failed_count += 1
                                details_text.insert(tk.END, f"  ❌ Scenario {scenario_number} FAILED\n\n")
                                cursor = self.db_manager.conn.cursor()
                                cursor.execute("""
                                    UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                                    WHERE id = ?
                                """, (scenario_id,))
                                self.db_manager.conn.commit()
                                
                        except Exception as e:
                            failed_count += 1
                            details_text.insert(tk.END, f"  ❌ Scenario {scenario_number} ERROR: {str(e)}\n\n")
                            cursor = self.db_manager.conn.cursor()
                            cursor.execute("""
                                UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                                WHERE id = ?
                            """, (scenario_id,))
                            self.db_manager.conn.commit()
                        
                        details_text.see(tk.END)
                        popup.update()
                    
                    # Final summary
                    progress_label.config(
                        text=f"✅ Execution completed! {passed_count} passed, {failed_count} failed", 
                        fg='#10b981' if failed_count == 0 else '#f59e0b'
                    )
                    details_text.insert(tk.END, f"\n=== EXECUTION SUMMARY ===\n")
                    details_text.insert(tk.END, f"Total Scenarios: {total_scenarios}\n")
                    details_text.insert(tk.END, f"Passed: {passed_count}\n")
                    details_text.insert(tk.END, f"Failed: {failed_count}\n")
                    details_text.see(tk.END)
                    
                except Exception as e:
                    progress_label.config(text=f"❌ Execution failed: {str(e)}", fg='#ef4444')
                    details_text.insert(tk.END, f"\nEXECUTION ERROR: {str(e)}\n")
            
            tk.Button(btn_frame, text="▶️ Start All", font=('Segoe UI', 10, 'bold'), 
                     bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8, 
                     cursor='hand2', bd=0, command=start_execution).pack(side="left", padx=(0, 10))
            tk.Button(btn_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                     bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8, 
                     cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to run all scenarios: {str(e)}", "error")
