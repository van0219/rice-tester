#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import time
import threading
from datetime import datetime
from rice_dialogs import center_dialog

class EnhancedRunAllScenarios:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self._rice_data_manager_ref = None
        self.execution_running = False
        self.stop_execution = False
    
    def set_rice_data_manager_ref(self, rice_data_manager):
        """Set reference to rice data manager for auto-refresh functionality"""
        self._rice_data_manager_ref = rice_data_manager
    
    def run_all_scenarios(self, current_profile):
        """Enhanced run all scenarios with smart login handling"""
        if self.execution_running:
            self.show_popup("Already Running", "Scenario execution is already in progress.", "warning")
            return
        
        # Get all scenarios for the profile
        scenarios = self.db_manager.get_scenarios(current_profile)
        if not scenarios:
            self.show_popup("No Scenarios", "No scenarios found for this RICE profile.", "warning")
            return
        
        # Filter out scenarios with "Not run" status for validation
        runnable_scenarios = [s for s in scenarios if s[3] != 'Not run']  # s[3] is result column
        if not runnable_scenarios:
            self.show_popup("No Runnable Scenarios", "All scenarios have 'Not run' status. Please run individual scenarios first to validate they work.", "warning")
            return
        
        # Show professional loading screen first
        self._show_loading_screen(scenarios, current_profile)
    
    def _show_loading_screen(self, scenarios, current_profile):
        """Show professional loading screen before execution"""
        loading_popup = tk.Toplevel()
        loading_popup.title("Preparing Execution")
        center_dialog(loading_popup, 500, 300)
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
        
        header_label = tk.Label(header_frame, text="🚀 Preparing Batch Execution", 
                               font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(loading_popup, bg='#ffffff', padx=30, pady=30)
        content_frame.pack(fill="both", expand=True)
        
        # Status message
        status_label = tk.Label(content_frame, text="Analyzing scenarios and optimizing execution order...", 
                               font=('Segoe UI', 11), bg='#ffffff', fg='#374151')
        status_label.pack(pady=(0, 20))
        
        # Progress dots
        progress_label = tk.Label(content_frame, text="●○○", 
                                 font=('Segoe UI', 20), bg='#ffffff', fg='#3b82f6')
        progress_label.pack(pady=(0, 20))
        
        # Info
        info_label = tk.Label(content_frame, text=f"Found {len(scenarios)} scenarios to execute\nSmart login optimization enabled", 
                             font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280', justify="center")
        info_label.pack()
        
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
            self._create_execution_dialog(scenarios, current_profile)
        
        loading_popup.after(5000, start_execution)  # 5 second minimum loading
    
    def _create_execution_dialog(self, scenarios, current_profile):
        """Create the main execution dialog"""
        popup = tk.Toplevel()
        popup.title("Batch Scenario Execution")
        center_dialog(popup, 800, 696)
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
        
        title_label = tk.Label(header_frame, text="🔄 Batch Scenario Execution", 
                              font=('Segoe UI', 16, 'bold'), bg='#1e40af', fg='#ffffff')
        title_label.pack(side="left", padx=25, pady=20)
        
        # Status indicator
        self.status_label = tk.Label(header_frame, text="Ready", 
                                    font=('Segoe UI', 12, 'bold'), bg='#1e40af', fg='#fbbf24')
        self.status_label.pack(side="right", padx=25, pady=20)
        
        # Main content
        main_frame = tk.Frame(popup, bg='#ffffff', padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)
        
        # Execution info
        info_frame = tk.Frame(main_frame, bg='#f8fafc', relief='solid', bd=1, padx=15, pady=15)
        info_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(info_frame, text=f"📊 Execution Summary", 
                font=('Segoe UI', 12, 'bold'), bg='#f8fafc', fg='#1e40af').pack(anchor="w")
        
        tk.Label(info_frame, text=f"• Total Scenarios: {len(scenarios)}", 
                font=('Segoe UI', 10), bg='#f8fafc', fg='#374151').pack(anchor="w", pady=(5, 0))
        
        tk.Label(info_frame, text="• Smart Login: Only first scenario will perform login", 
                font=('Segoe UI', 10), bg='#f8fafc', fg='#374151').pack(anchor="w")
        
        tk.Label(info_frame, text="• Delay Between Scenarios: 3 seconds for stability", 
                font=('Segoe UI', 10), bg='#f8fafc', fg='#374151').pack(anchor="w")
        
        # Progress section
        progress_frame = tk.Frame(main_frame, bg='#ffffff')
        progress_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(progress_frame, text="Execution Progress", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#374151').pack(anchor="w")
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=len(scenarios), length=750)
        self.progress_bar.pack(fill="x", pady=(10, 5))
        
        # Progress text
        self.progress_text = tk.Label(progress_frame, text="Ready to start execution...", 
                                     font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        self.progress_text.pack(anchor="w")
        
        # Live output
        output_frame = tk.Frame(main_frame, bg='#ffffff')
        output_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        tk.Label(output_frame, text="Live Execution Output", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#374151').pack(anchor="w")
        
        # Output text area with scrollbar
        output_container = tk.Frame(output_frame, bg='#ffffff')
        output_container.pack(fill="both", expand=True, pady=(10, 0))
        
        self.output_text = tk.Text(output_container, height=12, font=('Consolas', 9), 
                                  bg='#1f2937', fg='#f9fafb', relief='solid', bd=1,
                                  wrap=tk.WORD, state=tk.DISABLED)
        
        scrollbar = ttk.Scrollbar(output_container, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Control buttons
        btn_frame = tk.Frame(main_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        self.start_btn = tk.Button(btn_frame, text="🚀 START BATCH EXECUTION", 
                                  font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff', 
                                  relief='flat', padx=25, pady=12, cursor='hand2', bd=0,
                                  command=lambda: self._start_batch_execution(scenarios, current_profile))
        self.start_btn.pack(side="left", padx=(0, 15))
        
        self.stop_btn = tk.Button(btn_frame, text="⏹ STOP", 
                                 font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                                 relief='flat', padx=20, pady=12, cursor='hand2', bd=0,
                                 command=self._stop_execution, state=tk.DISABLED)
        self.stop_btn.pack(side="left", padx=(0, 15))
        
        tk.Button(btn_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=12, 
                 cursor='hand2', bd=0, command=popup.destroy).pack(side="right")
        
        self.execution_popup = popup
        self._add_initial_output()
    
    def _add_initial_output(self):
        """Add initial output to the console"""
        self._add_output("=== RICE Tester Batch Execution System ===")
        self._add_output("Smart Login Optimization: ENABLED")
        self._add_output("Inter-scenario Delay: 3 seconds")
        self._add_output("Ready to begin batch execution...")
        self._add_output("")
    
    def _add_output(self, message, color="#f9fafb"):
        """Add message to output console"""
        if hasattr(self, 'output_text') and self.output_text.winfo_exists():
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"
            
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, formatted_message)
            self.output_text.config(state=tk.DISABLED)
            self.output_text.see(tk.END)
            
            if hasattr(self, 'execution_popup'):
                self.execution_popup.update()
    
    def _start_batch_execution(self, scenarios, current_profile):
        """Start the batch execution in a separate thread"""
        if self.execution_running:
            return
        
        self.execution_running = True
        self.stop_execution = False
        
        # Update UI
        self.start_btn.config(state=tk.DISABLED, bg='#9ca3af')
        self.stop_btn.config(state=tk.NORMAL, bg='#ef4444')
        self.status_label.config(text="Running", fg='#10b981')
        
        # Start execution in separate thread
        execution_thread = threading.Thread(target=self._execute_scenarios_batch, 
                                           args=(scenarios, current_profile))
        execution_thread.daemon = True
        execution_thread.start()
    
    def _execute_scenarios_batch(self, scenarios, current_profile):
        """Execute all scenarios with smart login handling"""
        try:
            self._add_output("🚀 Starting batch execution...")
            self._add_output(f"Total scenarios to execute: {len(scenarios)}")
            
            successful_scenarios = 0
            failed_scenarios = 0
            login_performed = False
            
            for i, scenario in enumerate(scenarios):
                if self.stop_execution:
                    self._add_output("⏹ Execution stopped by user")
                    break
                
                scenario_id, scenario_number, description, current_result = scenario[:4]
                
                self._add_output(f"")
                self._add_output(f"{'='*50}")
                self._add_output(f"📋 Scenario {i+1}/{len(scenarios)}: #{scenario_number}")
                self._add_output(f"Description: {description}")
                
                # Update progress
                self.progress_var.set(i)
                self.progress_text.config(text=f"Executing Scenario {i+1}/{len(scenarios)}: {description[:50]}...")
                
                try:
                    # Get scenario steps
                    cursor = self.db_manager.conn.cursor()
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
                        self._add_output(f"⚠️ No steps found for scenario #{scenario_number}")
                        continue
                    
                    # Smart login handling
                    filtered_steps = self._filter_login_steps(steps, login_performed)
                    if not login_performed and len(filtered_steps) < len(steps):
                        self._add_output("🔐 Login steps detected - will be executed (first scenario only)")
                        login_performed = True
                    elif login_performed and len(filtered_steps) < len(steps):
                        self._add_output("🔐 Login steps detected - SKIPPED (already logged in)")
                    
                    self._add_output(f"📝 Executing {len(filtered_steps)} steps...")
                    
                    # Execute scenario with filtered steps
                    success = self._execute_single_scenario(scenario_id, scenario_number, 
                                                          filtered_steps, current_profile)
                    
                    if success:
                        successful_scenarios += 1
                        self._add_output(f"✅ Scenario #{scenario_number} completed successfully")
                        
                        # Update database
                        cursor.execute("""
                            UPDATE scenarios SET result = 'Passed', executed_at = CURRENT_TIMESTAMP 
                            WHERE id = ?
                        """, (scenario_id,))
                        self.db_manager.conn.commit()
                    else:
                        failed_scenarios += 1
                        self._add_output(f"❌ Scenario #{scenario_number} failed")
                        
                        # Update database
                        cursor.execute("""
                            UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                            WHERE id = ?
                        """, (scenario_id,))
                        self.db_manager.conn.commit()
                    
                    # Inter-scenario delay (except for last scenario)
                    if i < len(scenarios) - 1 and not self.stop_execution:
                        self._add_output("⏱️ Waiting 3 seconds before next scenario...")
                        for delay_second in range(3):
                            if self.stop_execution:
                                break
                            time.sleep(1)
                            self._add_output(f"   {3-delay_second} seconds remaining...")
                
                except Exception as e:
                    failed_scenarios += 1
                    self._add_output(f"❌ Error in scenario #{scenario_number}: {str(e)}")
                    
                    # Update database
                    try:
                        cursor = self.db_manager.conn.cursor()
                        cursor.execute("""
                            UPDATE scenarios SET result = 'Failed', executed_at = CURRENT_TIMESTAMP 
                            WHERE id = ?
                        """, (scenario_id,))
                        self.db_manager.conn.commit()
                    except:
                        pass
            
            # Final summary
            self._add_output("")
            self._add_output("="*60)
            self._add_output("🏁 BATCH EXECUTION COMPLETED")
            self._add_output(f"✅ Successful: {successful_scenarios}")
            self._add_output(f"❌ Failed: {failed_scenarios}")
            self._add_output(f"📊 Total: {len(scenarios)}")
            
            # Update final progress
            self.progress_var.set(len(scenarios))
            self.progress_text.config(text=f"Completed: {successful_scenarios} successful, {failed_scenarios} failed")
            self.status_label.config(text="Completed", fg='#6b7280')
            
            # Auto-refresh RICE List
            try:
                if hasattr(self, '_rice_data_manager_ref') and self._rice_data_manager_ref:
                    self._add_output("🔄 Refreshing RICE List...")
                    self._rice_data_manager_ref.refresh_rice_profiles_table()
                    self._add_output("✅ RICE List refreshed")
            except Exception as e:
                self._add_output(f"⚠️ Failed to refresh RICE List: {str(e)}")
        
        except Exception as e:
            self._add_output(f"💥 Critical error in batch execution: {str(e)}")
            self.status_label.config(text="Error", fg='#ef4444')
        
        finally:
            # Reset UI
            self.execution_running = False
            self.start_btn.config(state=tk.NORMAL, bg='#10b981')
            self.stop_btn.config(state=tk.DISABLED, bg='#9ca3af')
    
    def _filter_login_steps(self, steps, login_performed):
        """Filter out login steps if login was already performed"""
        if login_performed:
            # Remove steps that are likely login steps
            login_keywords = ['login', 'username', 'password', 'sign in', 'log in', 'auth']
            filtered_steps = []
            
            for step in steps:
                step_name = (step[1] or '').lower()
                step_type = (step[2] or '').lower()
                step_target = (step[3] or '').lower()
                step_description = (step[4] or '').lower()
                
                # Check if this step contains login-related keywords
                is_login_step = any(keyword in f"{step_name} {step_target} {step_description}" 
                                  for keyword in login_keywords)
                
                if not is_login_step:
                    filtered_steps.append(step)
            
            return filtered_steps
        else:
            return steps
    
    def _execute_single_scenario(self, scenario_id, scenario_number, steps, current_profile):
        """Execute a single scenario with the given steps"""
        try:
            from screenshot_executor import ScreenshotExecutor
            
            executor = ScreenshotExecutor(self.db_manager.user_id, current_profile, scenario_number)
            
            def progress_callback(current_step, total_steps, step_name, message):
                self._add_output(f"   Step {current_step}/{total_steps}: {step_name} - {message}")
            
            executor.set_progress_callback(progress_callback)
            
            # Execute with filtered steps
            success = executor.execute_scenario_with_steps(steps)
            return success
            
        except Exception as e:
            self._add_output(f"   Execution error: {str(e)}")
            return False
    
    def _stop_execution(self):
        """Stop the batch execution"""
        self.stop_execution = True
        self._add_output("🛑 Stop requested - will complete current scenario and stop...")
        self.stop_btn.config(state=tk.DISABLED, bg='#9ca3af')