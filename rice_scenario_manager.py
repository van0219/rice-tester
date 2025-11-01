#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import os
from rice_dialogs import center_dialog
from scenario_dialogs import ScenarioDialogs
from scenario_execution import ScenarioExecution
from scenario_forms import ScenarioForms

# Import personal analytics (from Temp folder)
import sys
temp_path = os.path.join(os.path.dirname(__file__), 'Temp')
if temp_path not in sys.path:
    sys.path.insert(0, temp_path)

try:
    from personal_analytics import PersonalAnalytics
except ImportError:
    PersonalAnalytics = None

class ScenarioManager:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.selected_scenario_id = None
        self.selected_scenario_row = None
        self._rice_data_manager_ref = None
        
        # Initialize helper modules
        self.dialogs = ScenarioDialogs(db_manager, show_popup_callback)
        self.execution = ScenarioExecution(db_manager, show_popup_callback)
        self.forms = ScenarioForms(db_manager, show_popup_callback)
        
        # Initialize personal analytics
        if PersonalAnalytics:
            self.analytics = PersonalAnalytics(db_manager, show_popup_callback)
        else:
            self.analytics = None
    
    def set_rice_data_manager_ref(self, rice_data_manager):
        """Set reference to rice data manager for auto-refresh functionality"""
        self._rice_data_manager_ref = rice_data_manager
        # Pass the reference to the execution module
        self.execution.set_rice_data_manager_ref(rice_data_manager)
    
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
        
        tk.Label(content_frame, text=f"Reset scenario:\n'{scenario_info}'?\n\nThis will clear screenshots and reset status to 'Not run'.\nSteps will remain unchanged.", 
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
                
                self.show_popup("Success", "Scenario reset successfully! Screenshots cleared and status set to 'Not run'. Steps preserved.", "success")
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
            if os.path.exists(file_path):
                # Get original filename
                original_name = os.path.basename(file_path)
                
                # Custom confirmation dialog
                self.dialogs.show_download_confirmation(file_path, original_name)
            else:
                self.show_popup("Error", f"File not found: {file_path}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to save file: {str(e)}", "error")
    
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
    
    def run_scenario(self, scenario_id, current_profile):
        """Run a single scenario"""
        self.execution.run_scenario(scenario_id, current_profile)
    
    def _show_child_popup(self, parent_window, title, message, status):
        """Show popup as child of parent window"""
        self.dialogs.show_child_popup(parent_window, title, message, status)
    
    def edit_scenario(self, scenario_id, current_profile, refresh_callback):
        """Edit scenario with modern form and Test Users integration"""
        try:
            from scenario_edit_form_modern import ModernScenarioEditForm
            modern_form = ModernScenarioEditForm(self.db_manager, self.show_popup)
            modern_form.edit_scenario(scenario_id, current_profile, refresh_callback)
        except Exception as e:
            print(f"Error in edit_scenario: {e}")
            import traceback
            traceback.print_exc()
            self.show_popup("Error", f"Failed to open edit scenario form: {str(e)}", "error")
    
    def add_scenario(self, current_profile, refresh_callback):
        """Add new scenario with modern form and Test Users integration"""
        try:
            from scenario_add_form_modern import ModernScenarioAddForm
            modern_form = ModernScenarioAddForm(self.db_manager, self.show_popup)
            modern_form.add_scenario(current_profile, refresh_callback)
        except Exception as e:
            print(f"Error in add_scenario: {e}")
            import traceback
            traceback.print_exc()
            self.show_popup("Error", f"Failed to open add scenario form: {str(e)}", "error")
    
    def view_scenario_steps(self, scenario_id, scenario_number, current_profile):
        """View steps for a scenario using reliable table approach (no canvas issues)"""
        popup = tk.Toplevel()
        popup.title(f"Scenario #{scenario_number} - Steps")
        center_dialog(popup, 900, 650)
        popup.configure(bg='#f8fafc')
        popup.resizable(True, True)
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Main container
        main_frame = tk.Frame(popup, bg='#f8fafc')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#3b82f6', height=50)
        header_frame.pack(fill='x', pady=(0, 15))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"📋 Scenario #{scenario_number} - Test Steps", 
                font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Get steps data from database
        try:
            cursor = self.db_manager.conn.cursor()
            
            # Enhanced query to handle both test_step_id references and direct step data
            cursor.execute("""
                SELECT ss.step_order, 
                       COALESCE(ts.name, ss.step_name, 'Unnamed Step') as step_name,
                       COALESCE(ts.step_type, ss.step_type, 'Unknown') as step_type, 
                       CASE 
                           WHEN COALESCE(ts.step_type, ss.step_type) IN ('Wait', 'Text Input') 
                           THEN COALESCE(NULLIF(ss.step_description, ''), NULLIF(ss.custom_value, 'None'), ts.target, 'No value')
                           ELSE COALESCE(ts.target, ss.step_target, 'No target')
                       END as step_target,
                       COALESCE(ss.execution_status, 'Pending') as execution_status
                FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = ?
                ORDER BY ss.step_order
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            all_steps = cursor.fetchall()
            
            print(f"Debug: Found {len(all_steps)} steps for scenario {scenario_number}")
            
        except Exception as e:
            print(f"Database error loading steps: {str(e)}")
            all_steps = []
        
        # Create simple table using Treeview (reliable approach)
        table_frame = tk.Frame(main_frame, bg='#ffffff', relief='solid', bd=1)
        table_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Create Treeview with columns
        columns = ('Step', 'Name', 'Type', 'Target', 'Status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configure column headings and widths
        tree.heading('Step', text='🔢 Step')
        tree.heading('Name', text='📝 Name')
        tree.heading('Type', text='🏷️ Type')
        tree.heading('Target', text='🎯 Value/Target')
        tree.heading('Status', text='📊 Status')
        
        tree.column('Step', width=60, anchor='center')
        tree.column('Name', width=200, anchor='w')
        tree.column('Type', width=120, anchor='w')
        tree.column('Target', width=300, anchor='w')
        tree.column('Status', width=120, anchor='center')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack tree and scrollbar
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Populate table with steps data
        if all_steps:
            for step in all_steps:
                step_order, step_name, step_type, step_target, execution_status = step
                
                # Format display values
                display_name = step_name or 'Unnamed Step'
                display_type = step_type or 'Unknown'
                display_target = step_target or 'No target'
                status = execution_status or 'Pending'
                
                # Format target display based on type
                if display_type == 'Wait':
                    if display_target and str(display_target).replace('.', '').isdigit():
                        target_display = f"⏱️ {display_target}s"
                    else:
                        target_display = f"⏱️ {display_target or '3'}s"
                elif display_type == 'Text Input':
                    if display_target and display_target != 'No target':
                        if 'password' in display_name.lower():
                            target_display = f"✏️ {'•' * min(8, len(str(display_target)))}"
                        else:
                            target_display = f"✏️ {display_target}"
                    else:
                        target_display = "✏️ [No value]"
                elif display_type == 'Navigate':
                    target_display = f"🌐 {display_target if display_target != 'No target' else 'No URL'}"
                elif display_type == 'Element Click':
                    target_display = f"🖱️ {display_target if display_target != 'No target' else 'No selector'}"
                elif display_type == 'Email Check':
                    target_display = f"📧 {display_target if display_target != 'No target' else 'Email verification'}"
                else:
                    target_display = (display_target[:50] + "...") if display_target and len(str(display_target)) > 50 else display_target
                
                # Format status with icons
                status_icons = {
                    'completed': '✅ Completed',
                    'pending': '⏳ Pending', 
                    'failed': '❌ Failed',
                    'success': '✅ Success',
                    'error': '❌ Error',
                    'not run': '⚪ Not Run',
                    'running': '🔄 Running',
                    'skipped': '⏭️ Skipped'
                }
                status_lower = status.lower() if status else 'pending'
                status_display = status_icons.get(status_lower, f'⏳ {status.title()}')
                
                # Insert row into table
                tree.insert('', 'end', values=(
                    str(step_order),
                    display_name,
                    display_type,
                    target_display,
                    status_display
                ))
        else:
            # Show empty state message
            tree.insert('', 'end', values=(
                '',
                'No steps found for this scenario',
                '',
                'Steps will appear here once added',
                ''
            ))
        
        # Action buttons
        action_frame = tk.Frame(main_frame, bg='#f8fafc')
        action_frame.pack(fill='x', pady=(15, 0))
        
        button_frame = tk.Frame(action_frame, bg='#f8fafc')
        button_frame.pack()
        
        # Export button (future feature)
        tk.Button(button_frame, text="📄 Export Steps", font=('Segoe UI', 10, 'bold'), 
                 bg='#3b82f6', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0,
                 command=lambda: self.show_popup("Feature", "Export functionality coming soon!", "info")).pack(side='left', padx=(0, 10))
        
        # Close button
        tk.Button(button_frame, text="✕ Close", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0, command=popup.destroy).pack(side='left')
    

    
    def run_all_scenarios(self, current_profile):
        """Run all scenarios for the selected RICE profile with enhanced batch execution"""
        try:
            # Import the enhanced run all scenarios module
            import sys
            import os
            temp_path = os.path.join(os.path.dirname(__file__), 'Temp')
            if temp_path not in sys.path:
                sys.path.insert(0, temp_path)
            
            from enhanced_run_all_scenarios import EnhancedRunAllScenarios
            
            # Create enhanced executor
            enhanced_executor = EnhancedRunAllScenarios(self.db_manager, self.show_popup)
            enhanced_executor.set_rice_data_manager_ref(self._rice_data_manager_ref)
            
            # Start enhanced batch execution
            enhanced_executor.run_all_scenarios(current_profile)
            
        except ImportError as e:
            self.show_popup("Module Error", f"Enhanced run all scenarios module not found: {str(e)}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to start batch execution: {str(e)}", "error")
    
    def show_personal_dashboard(self):
        """Show personal analytics dashboard"""
        if self.analytics:
            try:
                self.analytics.show_personal_dashboard()
            except Exception as e:
                self.show_popup("Analytics Error", f"Failed to load personal dashboard: {str(e)}", "error")
        else:
            self.show_popup("Feature Unavailable", "Personal analytics module not available. Please update RICE Tester.", "warning")
