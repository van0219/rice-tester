#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import os
import traceback
from datetime import datetime
from rice_dialogs import center_dialog

class ScenarioExecution:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self._rice_data_manager_ref = None
    
    def set_rice_data_manager_ref(self, rice_data_manager):
        """Set reference to rice data manager for auto-refresh functionality"""
        self._rice_data_manager_ref = rice_data_manager
    
    def run_scenario(self, scenario_id, current_profile):
        """Run a single scenario with professional execution"""
        
        from screenshot_executor import ScreenshotExecutor
        
        try:
            # Get scenario details and steps
            cursor = self.db_manager.conn.cursor()
            
            cursor.execute("""
                SELECT scenario_number, description FROM scenarios 
                WHERE id = ? AND user_id = ?
            """, (scenario_id, self.db_manager.user_id))
            scenario_data = cursor.fetchone()
            
            if not scenario_data:
                self.show_popup("Error", "Scenario not found", "error")
                return
            
            scenario_number, description = scenario_data
            
            # Get scenario steps using the new database design
            cursor.execute("""
                SELECT 
                    ss.step_order,
                    COALESCE(ts.name, ss.step_name) as step_name,
                    COALESCE(ts.step_type, ss.step_type) as step_type,
                    COALESCE(ts.target, ss.step_target) as step_target,
                    CASE 
                        WHEN COALESCE(ts.step_type, ss.step_type) IN ('Text Input', 'Wait') 
                        THEN COALESCE(NULLIF(ss.step_description, ''), NULLIF(ss.custom_value, 'None'), ts.default_value)
                        ELSE COALESCE(ss.step_description, ts.description)
                    END as step_description,
                    COALESCE(ss.user_input_required, 0) as user_input_required
                FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = ?
                ORDER BY ss.step_order
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            steps = cursor.fetchall()
            
            if not steps:
                self.show_popup("No Steps", "This scenario has no test steps to execute.", "warning")
                return
            
            # Create execution dialog
            self._create_execution_dialog(scenario_id, scenario_number, description, steps, current_profile)
            
        except Exception as e:
            error_msg = str(e)
            traceback_msg = traceback.format_exc()
            self.show_popup("Execution Error", f"Failed to setup execution: {error_msg}", "error")
    
    def _create_execution_dialog(self, scenario_id, scenario_number, description, steps, current_profile):
        """Create the professional execution dialog"""
        # Show loading screen first
        self._show_loading_screen(scenario_id, scenario_number, description, steps, current_profile)
    
    def _show_loading_screen(self, scenario_id, scenario_number, description, steps, current_profile):
        """Show professional loading screen before execution"""
        loading_popup = tk.Toplevel()
        loading_popup.title("Preparing Execution")
        center_dialog(loading_popup, 450, 280)
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
        
        header_label = tk.Label(header_frame, text="⚡ Preparing Scenario Execution", 
                               font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(loading_popup, bg='#ffffff', padx=30, pady=30)
        content_frame.pack(fill="both", expand=True)
        
        # Scenario info
        tk.Label(content_frame, text=f"Scenario #{scenario_number}", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#1e40af').pack(pady=(0, 5))
        
        tk.Label(content_frame, text=description, 
                font=('Segoe UI', 10), bg='#ffffff', fg='#374151', 
                wraplength=380, justify="center").pack(pady=(0, 20))
        
        # Status message
        status_label = tk.Label(content_frame, text="Initializing browser and test environment...", 
                               font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        status_label.pack(pady=(0, 15))
        
        # Progress dots
        progress_label = tk.Label(content_frame, text="●○○", 
                                 font=('Segoe UI', 18), bg='#ffffff', fg='#3b82f6')
        progress_label.pack()
        
        # Animate progress dots
        dot_states = ["●○○", "○●○", "○○●", "●●○", "●○●", "○●●", "●●●"]
        current_dot = 0
        
        def animate_dots():
            nonlocal current_dot
            if loading_popup.winfo_exists():
                progress_label.config(text=dot_states[current_dot])
                current_dot = (current_dot + 1) % len(dot_states)
                loading_popup.after(300, animate_dots)
        
        animate_dots()
        
        # Auto-close after 5 seconds and start execution
        def start_execution():
            if loading_popup.winfo_exists():
                loading_popup.destroy()
            self._create_main_execution_dialog(scenario_id, scenario_number, description, steps, current_profile)
        
        loading_popup.after(5000, start_execution)  # 5 second minimum loading
    
    def _create_main_execution_dialog(self, scenario_id, scenario_number, description, steps, current_profile):
        """Create the main execution dialog"""
        popup = tk.Toplevel()
        popup.title(f"Execute Scenario #{scenario_number}")
        center_dialog(popup, 700, 596)
        popup.configure(bg='#ffffff')
        popup.grab_set()
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(popup, bg='#1e40af', height=70)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text=f"▶️ Execute Scenario #{scenario_number}", 
                              font=('Segoe UI', 16, 'bold'), bg='#1e40af', fg='#ffffff')
        title_label.pack(side="left", padx=25, pady=20)
        
        # Status indicator
        status_indicator = tk.Label(header_frame, text="Ready", 
                                   font=('Segoe UI', 12, 'bold'), bg='#1e40af', fg='#fbbf24')
        status_indicator.pack(side="right", padx=25, pady=20)
        
        # Main content
        main_frame = tk.Frame(popup, bg='#ffffff', padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)
        
        # Scenario info
        info_frame = tk.Frame(main_frame, bg='#f8fafc', relief='solid', bd=1, padx=15, pady=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(info_frame, text=description, font=('Segoe UI', 11, 'bold'), 
                bg='#f8fafc', fg='#1e40af', wraplength=600, justify="center").pack(pady=(0, 10))
        
        tk.Label(info_frame, text=f"📝 {len(steps)} test steps ready for execution", 
                font=('Segoe UI', 10), bg='#f8fafc', fg='#374151').pack()
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg='#ffffff')
        progress_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(progress_frame, text="Execution Progress", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#374151').pack(anchor="w")
        
        # Progress display
        progress_label = tk.Label(progress_frame, text="Ready to execute...", 
                                font=('Segoe UI', 11), bg='#ffffff', fg='#6b7280')
        progress_label.pack(anchor="w", pady=(5, 10))
        
        # Live output
        output_frame = tk.Frame(main_frame, bg='#ffffff')
        output_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        tk.Label(output_frame, text="Live Execution Output", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#374151').pack(anchor="w")
        
        # Output text area
        output_text = tk.Text(output_frame, height=8, font=('Consolas', 9), 
                             bg='#1f2937', fg='#f9fafb', relief='solid', bd=1,
                             wrap=tk.WORD, state=tk.DISABLED)
        output_text.pack(fill="both", expand=True, pady=(10, 0))
        
        def add_output(message, color="#f9fafb"):
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"
            
            output_text.config(state=tk.NORMAL)
            output_text.insert(tk.END, formatted_message)
            output_text.config(state=tk.DISABLED)
            output_text.see(tk.END)
            popup.update()
        
        add_output("=== RICE Tester Professional Execution ===")
        add_output(f"Scenario: #{scenario_number} - {description}")
        add_output(f"Steps to execute: {len(steps)}")
        add_output("Ready to begin execution...")
        
        # Control buttons
        btn_frame = tk.Frame(main_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        execution_running = False
        
        def start_execution():
            nonlocal execution_running
            if execution_running:
                add_output("Execution already running, ignoring request")
                return
            
            execution_running = True
            add_output("🚀 Starting professional execution...")
            progress_label.config(text="Starting execution...", fg='#dc2626')
            status_indicator.config(text="Running", fg='#10b981')
            popup.update()
            
            try:
                from screenshot_executor import ScreenshotExecutor
                add_output("Creating execution engine...")
                
                executor = ScreenshotExecutor(self.db_manager.user_id, current_profile, scenario_number)
                add_output("✅ Execution engine ready")
                
                def progress_callback(current_step, total_steps, step_name, message):
                    add_output(f"Step {current_step}/{total_steps}: {step_name} - {message}")
                    
                    # Create display message
                    if len(message) > 50:
                        display_message = f"Step {current_step}/{total_steps}: {step_name} - {message[:50]}..."
                    else:
                        display_message = f"Step {current_step}/{total_steps}: {step_name} - {message}"
                    
                    progress_label.config(text=display_message, fg='#dc2626')
                    popup.update()
                
                add_output("Setting up progress monitoring...")
                executor.set_progress_callback(progress_callback)
                add_output("🎯 Starting scenario execution...")
                
                # Execute scenario
                success = executor.execute_scenario()
                add_output(f"Execution completed. Success: {success}")
                
                # Final status update
                cursor = self.db_manager.conn.cursor()
                if success:
                    progress_label.config(text="✅ Execution completed successfully!", fg='#10b981')
                    status_indicator.config(text="Success", fg='#10b981')
                    add_output("🎉 EXECUTION SUCCESSFUL")
                    cursor.execute("""
                        UPDATE scenarios SET result = 'Passed', executed_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (scenario_id,))
                    self.db_manager.conn.commit()
                    add_output("✅ Scenario status updated to Passed")
                else:
                    progress_label.config(text="❌ Execution failed", fg='#ef4444')
                    status_indicator.config(text="Failed", fg='#ef4444')
                    add_output("❌ EXECUTION FAILED")
                    cursor.execute("""
                        UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                        WHERE id = ?
                    """, (scenario_id,))
                    self.db_manager.conn.commit()
                    add_output("📝 Scenario status updated to Failed")
                
                # Auto-refresh RICE List
                try:
                    if hasattr(self, '_rice_data_manager_ref') and self._rice_data_manager_ref:
                        add_output("🔄 Refreshing RICE List...")
                        self._rice_data_manager_ref.refresh_rice_profiles_table()
                        add_output("✅ RICE List refreshed")
                except Exception as refresh_error:
                    add_output(f"⚠️ Failed to refresh RICE List: {refresh_error}")
                    
            except Exception as e:
                error_msg = str(e)
                add_output(f"💥 EXECUTION ERROR: {error_msg}")
                progress_label.config(text=f"Error: {error_msg}", fg='#ef4444')
                status_indicator.config(text="Error", fg='#ef4444')
                
                cursor = self.db_manager.conn.cursor()
                cursor.execute("""
                    UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                    WHERE id = ?
                """, (scenario_id,))
                self.db_manager.conn.commit()
            
            execution_running = False
            add_output("=== EXECUTION COMPLETED ===")
        
        # Buttons
        start_btn = tk.Button(btn_frame, text="🚀 START EXECUTION", font=('Segoe UI', 12, 'bold'), 
                             bg='#10b981', fg='#ffffff', relief='flat', padx=25, pady=12, 
                             cursor='hand2', bd=0, command=start_execution)
        start_btn.pack(side="left", padx=(0, 15))
        
        tk.Button(btn_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=12, 
                 cursor='hand2', bd=0, command=popup.destroy).pack(side="right")
        
        add_output("Ready to begin execution. Click 'START EXECUTION' to proceed.")
