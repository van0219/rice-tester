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
        """View steps for a scenario with pagination"""
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
        tk.Label(headers_frame, text="Value/Target", font=('Segoe UI', 10, 'bold'), 
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
        
        # Get all steps from database with proper column handling
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT ss.step_order, 
                       COALESCE(ts.name, ss.step_name) as step_name,
                       COALESCE(ts.step_type, ss.step_type) as step_type, 
                       CASE 
                           WHEN COALESCE(ts.step_type, ss.step_type) IN ('Wait', 'Text Input') 
                           THEN COALESCE(NULLIF(ss.step_description, ''), NULLIF(ss.custom_value, 'None'), ts.default_value)
                           ELSE COALESCE(ts.target, ss.step_target)
                       END as step_target,
                       ss.execution_status
                FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = ?
                ORDER BY ss.step_order
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
                name_label = tk.Label(row_frame, text=step_name or '', font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10)
                name_label.place(relx=0.08, y=8, relwidth=0.25)
                if step_name and len(step_name) > 20:
                    self._add_tooltip(name_label, step_name)
                
                # Step type
                type_label = tk.Label(row_frame, text=step_type or '', font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10)
                type_label.place(relx=0.33, y=8, relwidth=0.15)
                if step_type and len(step_type) > 12:
                    self._add_tooltip(type_label, step_type)
                
                # Target (truncated) - Show appropriate display for different step types
                if step_type == 'Wait':
                    # For Wait steps, show the value with appropriate suffix
                    if step_target and step_target.isdigit():
                        target_display = f"{step_target}s"
                    else:
                        target_display = step_target or '3s'
                elif step_type == 'Text Input':
                    # For Text Input steps, show the input value
                    target_display = step_target or '[No value]'
                else:
                    target_display = (step_target[:40] + "...") if step_target and len(step_target) > 40 else step_target or ''
                
                target_label = tk.Label(row_frame, text=target_display, font=('Segoe UI', 9), 
                        bg=bg_color, fg='#374151', anchor='w', padx=10)
                target_label.place(relx=0.48, y=8, relwidth=0.35)
                if step_target and len(step_target) > 40:
                    self._add_tooltip(target_label, step_target)
                
                # Status
                status = execution_status or 'Pending'
                status_color = '#10b981' if status == 'completed' else '#f59e0b' if status == 'pending' else '#ef4444'
                tk.Label(row_frame, text=status.title(), font=('Segoe UI', 9), 
                        bg=bg_color, fg=status_color, anchor='w', padx=10).place(relx=0.83, y=8, relwidth=0.17)
            
            # Update pagination info
            page_label.config(text=f"Page {current_page} of {total_pages} ({total_steps} steps total)")
            
            # Update button states
            prev_btn.config(state='normal' if current_page > 1 else 'disabled',
                           bg='#6b7280' if current_page > 1 else '#9ca3af')
            next_btn.config(state='normal' if current_page < total_pages else 'disabled',
                           bg='#6b7280' if current_page < total_pages else '#9ca3af')
        
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
        pagination_frame.pack(fill='x', pady=(10, 20))
        
        # Center container for pagination
        pagination_container = tk.Frame(pagination_frame, bg='#ffffff')
        pagination_container.pack(expand=True)
        
        # Previous button
        prev_btn = tk.Button(pagination_container, text="◀ Previous", font=('Segoe UI', 9), 
                            bg='#6b7280', fg='#ffffff', relief='flat', padx=10, pady=4, 
                            cursor='hand2', bd=0, command=prev_page)
        prev_btn.pack(side='left')
        
        # Page info
        page_label = tk.Label(pagination_container, text="Page 1 of 1 (0 steps total)", 
                             font=('Segoe UI', 9), bg='#ffffff', fg='#374151')
        page_label.pack(side='left', padx=20)
        
        # Next button
        next_btn = tk.Button(pagination_container, text="Next ▶", font=('Segoe UI', 9), 
                            bg='#6b7280', fg='#ffffff', relief='flat', padx=10, pady=4, 
                            cursor='hand2', bd=0, command=next_page)
        next_btn.pack(side='left')
        
        # Load first page
        load_steps_page()
        
        # Action buttons
        action_frame = tk.Frame(frame, bg='#ffffff')
        action_frame.pack(fill="x", pady=(10, 0))
        
        # Center container for buttons
        button_container = tk.Frame(action_frame, bg='#ffffff')
        button_container.pack(expand=True)
        
        # Note: Generate Docs button removed - use main TES-070 generation instead
        
        # Close button (centered)
        tk.Button(button_container, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack()
    
    def _add_tooltip(self, widget, text):
        """Add hover tooltip to widget for long text content"""
        if not text:
            return
        
        def on_enter(event):
            # Create tooltip
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#2d3748')
            
            # Position tooltip near mouse
            x = event.x_root + 10
            y = event.y_root - 25
            tooltip.geometry(f"+{x}+{y}")
            
            # Tooltip content with word wrapping
            label = tk.Label(tooltip, text=text, font=('Segoe UI', 9), 
                           bg='#2d3748', fg='#ffffff', padx=8, pady=4, 
                           wraplength=400, justify='left')
            label.pack()
            
            # Store tooltip reference
            widget.tooltip = tooltip
        
        def on_leave(event):
            # Destroy tooltip
            if hasattr(widget, 'tooltip'):
                try:
                    widget.tooltip.destroy()
                    delattr(widget, 'tooltip')
                except:
                    pass
        
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
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
