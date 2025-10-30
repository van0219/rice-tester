#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from rice_ui import RiceUI
from rice_data import RiceDataManager
from rice_dialogs import center_dialog

class RiceManager:
    def __init__(self, parent, db_manager, show_popup_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        
        # Store reference to main app for user access
        self.main_app = self._find_main_app(parent)
        
        # Initialize data manager
        self.data_manager = RiceDataManager(db_manager, show_popup_callback, self)
        
        # Initialize UI components
        callbacks = {
            'rice_prev_page': self.rice_prev_page,
            'rice_next_page': self.rice_next_page,
            'scenarios_prev_page': self.scenarios_prev_page,
            'scenarios_next_page': self.scenarios_next_page,
            'change_rice_per_page': self.change_rice_per_page,
            'change_scenarios_per_page': self.change_scenarios_per_page,
            'add_rice_profile': self.add_rice_profile,
            'load_rice_profiles': self.load_rice_profiles,
            'add_scenario': self.add_scenario,
            'execute_scenario': self.execute_scenario,
            'run_all_scenarios': self.run_all_scenarios,
            'generate_tes_070': self.generate_tes_070,
            'show_tes070_history': self.show_tes070_history,
            'show_personal_dashboard': self.show_personal_dashboard
        }
        self.ui = RiceUI(parent, callbacks)
        
        # UI component references (set after setup)
        self.ui_components = {}
    
    def _find_main_app(self, widget):
        """Find the main application instance with user object"""
        # Check current widget
        if hasattr(widget, 'user'):
            return widget
        
        # Check parent chain
        current = widget
        while current:
            if hasattr(current, 'user'):
                return current
            current = getattr(current, 'master', None)
        
        # Check root and its children
        try:
            root = widget.winfo_toplevel()
            if hasattr(root, 'user'):
                return root
            
            # Check all children of root
            def check_children(parent):
                if hasattr(parent, 'user'):
                    return parent
                for child in parent.winfo_children():
                    result = check_children(child)
                    if result:
                        return result
                return None
            
            return check_children(root)
        except:
            return None
    
    def setup_rice_tab_content(self, parent):
        """Setup RICE profiles tab content for new tab system"""
        self.ui.setup_rice_tab_content(parent)
        
        # Store UI component references
        self.ui_components = {
            'rice_scroll_frame': self.ui.rice_scroll_frame,
            'rice_page_label': self.ui.rice_page_label,
            'rice_prev_btn': self.ui.rice_prev_btn,
            'rice_next_btn': self.ui.rice_next_btn,
            'scenarios_scroll_frame': self.ui.scenarios_scroll_frame,
            'scenarios_label': self.ui.scenarios_label,
            'scenarios_page_label': self.ui.scenarios_page_label,
            'scenarios_prev_btn': self.ui.scenarios_prev_btn,
            'scenarios_next_btn': self.ui.scenarios_next_btn
        }
        
        # Reset current profile state when tab is recreated
        self.data_manager.current_profile = None
        self.data_manager.selected_rice_profile = None
        self.data_manager.selected_rice_row = None
        self.data_manager.selected_scenario_id = None
        self.data_manager.selected_scenario_row = None
        
        self.load_rice_profiles()
    
    def load_rice_profiles(self):
        """Load RICE profiles with pagination"""
        self.data_manager.load_rice_profiles(self.ui_components)
    
    def rice_prev_page(self):
        """Go to previous page of RICE profiles"""
        self.data_manager.rice_prev_page(self.ui_components)
    
    def rice_next_page(self):
        """Go to next page of RICE profiles"""
        self.data_manager.rice_next_page(self.ui_components)
    
    def scenarios_prev_page(self):
        """Go to previous page of scenarios"""
        self.data_manager.scenarios_prev_page(self.ui_components)
    
    def scenarios_next_page(self):
        """Go to next page of scenarios"""
        self.data_manager.scenarios_next_page(self.ui_components)
    
    def change_rice_per_page(self, new_per_page):
        """Change RICE records per page"""
        self.data_manager.change_rice_per_page(new_per_page, self.ui_components)
    
    def change_scenarios_per_page(self, new_per_page):
        """Change scenarios records per page"""
        self.data_manager.change_scenarios_per_page(new_per_page, self.ui_components)
    
    def add_rice_profile(self):
        """Add RICE profile dialog"""
        popup = tk.Toplevel(self.parent)
        popup.title("Add RICE Profile")
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Use CSS-like centering function
        center_dialog(popup, 500, 350)
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # RICE ID
        tk.Label(frame, text="RICE ID:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=5)
        rice_id_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        rice_id_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Name
        tk.Label(frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Project/Client
        tk.Label(frame, text="Project/Client:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky="w", pady=5)
        client_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        client_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Type
        tk.Label(frame, text="Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky="w", pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(frame, textvariable=type_var, width=27, font=('Segoe UI', 10), state='readonly')
        rice_types = [rt[1] for rt in self.db_manager.get_rice_types()]  # Get type names
        type_combo['values'] = rice_types
        type_combo.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Channel Name (dropdown - optional)
        tk.Label(frame, text="Channel Name (Optional):", font=('Segoe UI', 10), bg='#ffffff').grid(row=4, column=0, sticky="w", pady=5)
        channel_var = tk.StringVar()
        channel_combo = ttk.Combobox(frame, textvariable=channel_var, width=27, font=('Segoe UI', 10))
        channels = [''] + [ch[1] for ch in self.db_manager.get_file_channels()]  # Add empty option
        channel_combo['values'] = channels
        channel_combo.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        # SFTP Profile (dropdown - optional)
        tk.Label(frame, text="SFTP Profile (Optional):", font=('Segoe UI', 10), bg='#ffffff').grid(row=5, column=0, sticky="w", pady=5)
        sftp_var = tk.StringVar()
        sftp_combo = ttk.Combobox(frame, textvariable=sftp_var, width=27, font=('Segoe UI', 10))
        sftp_profiles = [''] + [sp[1] for sp in self.db_manager.get_sftp_profiles()]  # Add empty option
        sftp_combo['values'] = sftp_profiles
        sftp_combo.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        
        # Tenant
        tk.Label(frame, text="Tenant:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=6, column=0, sticky="w", pady=5)
        tenant_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        tenant_entry.grid(row=6, column=1, sticky="ew", padx=10, pady=5)
        tenant_entry.insert(0, "TAMICS10_AX1")  # Default value
        
        frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        def save_rice_profile():
            rice_id = rice_id_entry.get().strip()
            name = name_entry.get().strip()
            client_name = client_entry.get().strip()
            profile_type = type_var.get()
            channel_name = channel_var.get().strip() or None
            sftp_profile_name = sftp_var.get().strip() or None
            tenant = tenant_entry.get().strip() or None
            
            if not all([rice_id, name, client_name, profile_type, tenant]):
                self.show_popup("Error", "Please fill in required fields (RICE ID, Name, Project/Client, Type, Tenant)", "error")
                return
            
            try:
                self.db_manager.save_rice_profile(rice_id, name, profile_type, client_name, channel_name, sftp_profile_name, tenant)
                popup.destroy()
                self.load_rice_profiles()
                self.show_popup("Success", f"RICE '{rice_id}' for {client_name} saved successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to save RICE: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=save_rice_profile).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=popup.destroy).pack(side="left")
        
        popup.focus_set()
        rice_id_entry.focus()
    
    def add_scenario(self):
        """Add scenario dialog"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Select RICE First", "Please select a RICE item from the list above before adding scenarios.", "warning")
            return
        
        self.data_manager.scenario_manager.add_scenario(self.data_manager.current_profile, self.data_manager.refresh_scenarios_table)
    
    def execute_scenario(self):
        """Execute a single selected scenario"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Error", "Please select a RICE first", "error")
            return
        
        if not hasattr(self.data_manager, 'selected_scenario_id') or not self.data_manager.selected_scenario_id:
            self.show_popup("Select Scenario", "Please select a scenario from the list to execute.", "warning")
            return
        
        self.data_manager.scenario_manager.run_scenario(self.data_manager.selected_scenario_id, self.data_manager.current_profile)
    
    def run_all_scenarios(self):
        """Run all scenarios for the selected RICE profile"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Error", "Please select a RICE first", "error")
            return
        
        self.data_manager.scenario_manager.run_all_scenarios(self.data_manager.current_profile)
    
    def edit_scenario(self, scenario_id):
        """Edit a specific scenario"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Error", "Please select a RICE first", "error")
            return
        
        self.data_manager.scenario_manager.edit_scenario(scenario_id, self.data_manager.current_profile, self.data_manager.refresh_scenarios_table)
    
    def run_scenario(self, scenario_id):
        """Run a specific scenario"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Error", "Please select a RICE first", "error")
            return
        
        self.data_manager.scenario_manager.run_scenario(scenario_id, self.data_manager.current_profile)
    
    def generate_tes_070(self):
        """Generate TES-070 Test Execution Summary report"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Error", "Please select a RICE first", "error")
            return
        
        # Get current user from main application
        current_user = None
        if self.main_app and hasattr(self.main_app, 'user'):
            current_user = self.main_app.user
        elif hasattr(self.parent, 'user'):
            current_user = self.parent.user
        elif hasattr(self.parent, 'master') and hasattr(self.parent.master, 'user'):
            current_user = self.parent.master.user
        
        # Try to get user from database if not found in UI
        if not current_user:
            try:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT full_name FROM users WHERE id = ?", (self.db_manager.user_id,))
                result = cursor.fetchone()
                if result:
                    current_user = {'full_name': result[0], 'username': 'user'}
                else:
                    current_user = {'full_name': 'Unknown User', 'username': 'user'}
            except Exception:
                current_user = {'full_name': 'Unknown User', 'username': 'user'}
        
        # Import and use TES-070 from-scratch generator (per requirements)
        from tes070_generator_new import create_tes070_from_scratch
        create_tes070_from_scratch(self.data_manager.current_profile, self.show_popup, current_user, self.db_manager)
    
    def show_tes070_history(self):
        """Show TES-070 history for selected RICE profile"""
        if not hasattr(self.data_manager, 'current_profile') or not self.data_manager.current_profile:
            self.show_popup("Error", "Please select a RICE first", "error")
            return
        
        # Get the RICE ID from current profile (current_profile contains the rice_id)
        rice_id = self.data_manager.current_profile
        
        # Get TES-070 versions from database for this specific RICE
        versions = self.db_manager.get_tes070_versions(rice_id)
        
        if not versions:
            self.show_popup("No History", "No TES-070 versions found for this RICE profile.", "warning")
            return
        
        # Create history dialog
        from rice_dialogs import create_enhanced_dialog
        history_popup = create_enhanced_dialog(None, "TES-070 History", 628, 446, modal=False)
        history_popup.configure(bg='#ffffff')
        
        try:
            history_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(history_popup, bg='#6366f1', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📚 TES-070 Version History", 
                font=('Segoe UI', 14, 'bold'), bg='#6366f1', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(history_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Table headers
        headers_frame = tk.Frame(content_frame, bg='#e5e7eb', height=30)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="Version", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').place(x=10, y=5, width=80)
        tk.Label(headers_frame, text="Created Date", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').place(x=100, y=5, width=150)
        tk.Label(headers_frame, text="Created By", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').place(x=260, y=5, width=150)
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').place(x=420, y=5, width=100)
        
        # Versions list
        versions_frame = tk.Frame(content_frame, bg='#ffffff')
        versions_frame.pack(fill="both", expand=True)
        
        for i, (version_id, version_number, created_at, created_by) in enumerate(versions):
            row_bg = '#ffffff' if i % 2 == 0 else '#f9fafb'
            row_frame = tk.Frame(versions_frame, bg=row_bg, height=35)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)
            
            # Version info
            tk.Label(row_frame, text=f"v{version_number}", font=('Segoe UI', 9), 
                    bg=row_bg, fg='#374151').place(x=10, y=8, width=80)
            
            from datetime import datetime
            try:
                date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%m/%d/%Y %I:%M %p')
            except:
                formatted_date = created_at
            
            tk.Label(row_frame, text=formatted_date, font=('Segoe UI', 9), 
                    bg=row_bg, fg='#374151').place(x=100, y=8, width=150)
            tk.Label(row_frame, text=created_by, font=('Segoe UI', 9), 
                    bg=row_bg, fg='#374151').place(x=260, y=8, width=150)
            
            # Download button
            download_btn = tk.Button(row_frame, text="📥 Download", font=('Segoe UI', 8), 
                                   bg='#10b981', fg='#ffffff', relief='flat', padx=8, pady=2, 
                                   cursor='hand2', bd=0,
                                   command=lambda vid=version_id, vnum=version_number: self.download_tes070_version(vid, vnum))
            download_btn.place(x=420, y=5, width=80, height=25)
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=history_popup.destroy).pack(pady=(20, 0))
    
    def download_tes070_version(self, version_id, version_number):
        """Download specific TES-070 version"""
        try:
            # Get file content from database
            file_content = self.db_manager.get_tes070_content(version_id)
            if not file_content:
                self.show_popup("Error", "TES-070 version not found", "error")
                return
            
            # Show save dialog
            from tkinter import filedialog
            from datetime import datetime
            import os
            
            # Get saved TES-070 template format
            template_format = self.db_manager.get_tes070_template()
            if not template_format:
                template_format = "TES-070_{rice_id}_{date}_v{version}.docx"
            
            # Get RICE profile data for placeholders
            rice_data = None
            try:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("SELECT name, rice_id, client_name, tenant FROM rice_profiles WHERE rice_id = ? OR id = ?", 
                              (self.data_manager.current_profile, self.data_manager.current_profile))
                rice_data = cursor.fetchone()
            except:
                pass
            
            # Prepare placeholder values
            current_date = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            if rice_data:
                rice_name, rice_id, client_name, tenant = rice_data
                placeholders = {
                    'rice_id': rice_id or 'RICE',
                    'name': rice_name or 'Report',
                    'client_name': client_name or 'Client',
                    'tenant': tenant or 'Tenant',
                    'date': current_date,
                    'version': str(version_number)
                }
            else:
                placeholders = {
                    'rice_id': str(self.data_manager.current_profile),
                    'name': 'Report',
                    'client_name': 'Client',
                    'tenant': 'Tenant',
                    'date': current_date,
                    'version': str(version_number)
                }
            
            # Apply template format
            try:
                default_name = template_format.format(**placeholders)
            except (KeyError, ValueError):
                default_name = f"TES-070_{placeholders['rice_id']}_v{version_number}_{current_date}.docx"
            
            # Ensure .docx extension
            if not default_name.lower().endswith('.docx'):
                default_name += '.docx'
            downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            
            output_path = filedialog.asksaveasfilename(
                defaultextension=".docx",
                filetypes=[("Word documents", "*.docx")],
                title="Save TES-070 Version",
                initialfile=default_name,
                initialdir=downloads_folder
            )
            
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(file_content)
                self.show_popup("Success", f"TES-070 version {version_number} downloaded:\n{output_path}", "success")
                
        except Exception as e:
            self.show_popup("Error", f"Failed to download TES-070: {str(e)}", "error")
    
    def show_personal_dashboard(self):
        """Show personal analytics dashboard"""
        try:
            # Import personal analytics from main folder
            from personal_analytics import PersonalAnalytics
            
            # Create and show personal analytics dashboard
            analytics = PersonalAnalytics(self.db_manager, self.show_popup)
            analytics.show_personal_dashboard()
            
        except ImportError as e:
            self.show_popup("Feature Unavailable", "Personal analytics module not available. Please update RICE Tester.", "warning")
        except Exception as e:
            self.show_popup("Analytics Error", f"Failed to load personal dashboard: {str(e)}", "error")
