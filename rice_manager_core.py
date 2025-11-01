#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from rice_ui import RiceUI
from rice_data_core import RiceDataManager
from rice_dialogs import center_dialog

class RiceManager:
    def __init__(self, parent, db_manager, show_popup_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        
        # Store reference to main app for user access
        self.main_app = self._find_main_app(parent)
        
        # Initialize UI components first
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
        
        # Initialize data manager with UI reference
        self.data_manager = RiceDataManager(db_manager, show_popup_callback, self, self.ui)
        

        
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
            'scenarios_scroll_frame': self.ui.scenarios_scroll_frame,
            'scenarios_label': self.ui.scenarios_label,
            # Add search UI references
            'rice_search_var': self.ui.rice_search_var,
            'rice_type_filter_var': self.ui.rice_type_filter_var,
            'rice_type_filter': self.ui.rice_type_filter
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
        """Add RICE profile dialog with modern 2-column layout"""
        from enhanced_popup_system import create_enhanced_dialog
        
        popup = create_enhanced_dialog(None, "Add RICE Item", 650, 420, modal=False)
        popup.configure(bg='#f8fafc')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Tooltip function
        def create_tooltip(widget, text):
            def on_enter(event):
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.configure(bg='#374151')
                label = tk.Label(tooltip, text=text, bg='#374151', fg='#ffffff', 
                                font=('Segoe UI', 9), padx=8, pady=4)
                label.pack()
                x, y, _, _ = widget.bbox("insert")
                x += widget.winfo_rootx() + 20
                y += widget.winfo_rooty() + 20
                tooltip.geometry(f"+{x}+{y}")
                widget.tooltip = tooltip
            def on_leave(event):
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
                    del widget.tooltip
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
        
        # Modern card-based layout
        card_frame = tk.Frame(popup, bg='#ffffff', relief='solid', bd=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Blue header with title
        header_frame = tk.Frame(card_frame, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="➕ Add RICE Item", font=('Segoe UI', 14, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content frame with better spacing
        content_frame = tk.Frame(card_frame, bg='#ffffff', padx=25, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Compact 2-column layout to reduce vertical space
        form_container = tk.Frame(content_frame, bg='#ffffff')
        form_container.pack(fill="both", expand=True)
        
        # Configure grid weights for responsive layout
        form_container.grid_columnconfigure(0, weight=1)
        form_container.grid_columnconfigure(1, weight=1)
        
        # Left Column - Core Information
        left_column = tk.Frame(form_container, bg='#ffffff')
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        
        # RICE ID (required) with tooltip
        rice_id_frame = tk.Frame(left_column, bg='#ffffff')
        rice_id_frame.pack(fill="x", pady=(0, 10))
        rice_id_label = tk.Label(rice_id_frame, text="🆔 RICE ID * ℹ️", font=('Segoe UI', 10, 'bold'), 
                                bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        rice_id_label.pack(anchor="w")
        rice_id_entry = tk.Entry(rice_id_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                                relief='solid', bd=1, highlightthickness=1, highlightcolor='#3b82f6')
        rice_id_entry.pack(fill="x", pady=(2, 0))
        
        create_tooltip(rice_id_label, "Unique identifier for this RICE item (e.g., INT-001, RPT-002)")
        
        # Name (required) with tooltip
        name_frame = tk.Frame(left_column, bg='#ffffff')
        name_frame.pack(fill="x", pady=(0, 10))
        name_label = tk.Label(name_frame, text="📝 Name * ℹ️", font=('Segoe UI', 10, 'bold'), 
                             bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        name_label.pack(anchor="w")
        name_entry = tk.Entry(name_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                             relief='solid', bd=1, highlightthickness=1, highlightcolor='#3b82f6')
        name_entry.pack(fill="x", pady=(2, 0))
        
        create_tooltip(name_label, "Descriptive name for this RICE item")
        
        # Project/Client (auto-populated from user's company) with tooltip
        client_frame = tk.Frame(left_column, bg='#ffffff')
        client_frame.pack(fill="x", pady=(0, 10))
        client_label = tk.Label(client_frame, text="🏢 Project/Client (Auto) ℹ️", font=('Segoe UI', 10, 'bold'), 
                               bg='#ffffff', fg='#059669', cursor='question_arrow')
        client_label.pack(anchor="w")
        client_entry = tk.Entry(client_frame, font=('Segoe UI', 10), bg='#f0f9ff', 
                               relief='solid', bd=1, highlightthickness=1, highlightcolor='#3b82f6',
                               state='readonly', readonlybackground='#f0f9ff')
        
        # Get user's company from database
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT company FROM users WHERE id = ?", (self.db_manager.user_id,))
            user_company = cursor.fetchone()
            if user_company and user_company[0]:
                client_entry.configure(state='normal')
                client_entry.delete(0, tk.END)
                client_entry.insert(0, user_company[0])
                client_entry.configure(state='readonly')
            else:
                # Fallback if no company found
                client_entry.configure(state='normal')
                client_entry.delete(0, tk.END)
                client_entry.insert(0, 'No Company Set')
                client_entry.configure(state='readonly')
        except Exception as e:
            # Fallback on error
            client_entry.configure(state='normal')
            client_entry.delete(0, tk.END)
            client_entry.insert(0, 'Error Loading Company')
            client_entry.configure(state='readonly')
        
        client_entry.pack(fill="x", pady=(2, 0))
        
        create_tooltip(client_label, "Auto-populated from your company profile (set during signup)")
        
        # Type (required) with tooltip
        type_frame = tk.Frame(left_column, bg='#ffffff')
        type_frame.pack(fill="x", pady=(0, 10))
        type_label = tk.Label(type_frame, text="🏷️ Type * ℹ️", font=('Segoe UI', 10, 'bold'), 
                             bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        type_label.pack(anchor="w")
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(type_frame, textvariable=type_var, font=('Segoe UI', 10))
        rice_types = [rt[1] for rt in self.db_manager.get_rice_types()]
        type_combo['values'] = rice_types
        type_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(type_label, "Select the RICE item type (Interface, Report, Conversion, Extension)")
        
        # Enable search in type dropdown
        def filter_type_values(event):
            typed = type_var.get().lower()
            if typed == '':
                type_combo['values'] = rice_types
            else:
                filtered = [t for t in rice_types if typed in t.lower()]
                type_combo['values'] = filtered
        type_combo.bind('<KeyRelease>', filter_type_values)
        
        # Right Column - Configuration & Environment
        right_column = tk.Frame(form_container, bg='#ffffff')
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)
        
        # Channel Name (optional) with tooltip and refresh
        channel_frame = tk.Frame(right_column, bg='#ffffff')
        channel_frame.pack(fill="x", pady=(0, 10))
        channel_header = tk.Frame(channel_frame, bg='#ffffff')
        channel_header.pack(fill="x")
        channel_label = tk.Label(channel_header, text="📡 Channel Name ℹ️", font=('Segoe UI', 10), 
                                bg='#ffffff', fg='#6b7280', cursor='question_arrow')
        channel_label.pack(side="left")
        refresh_channel_btn = tk.Button(channel_header, text="🔄", font=('Segoe UI', 8), 
                                       bg='#f3f4f6', fg='#6b7280', relief='flat', 
                                       padx=4, pady=2, cursor='hand2', bd=0)
        refresh_channel_btn.pack(side="right")
        
        channel_var = tk.StringVar()
        channel_combo = ttk.Combobox(channel_frame, textvariable=channel_var, font=('Segoe UI', 10))
        
        def load_channels():
            channels = [''] + [ch[1] for ch in self.db_manager.get_file_channels()]
            channel_combo['values'] = channels
            return channels
        
        channels = load_channels()
        channel_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(channel_label, "Optional: Select file channel for data transfer")
        refresh_channel_btn.configure(command=load_channels)
        
        # Enable search in channel dropdown
        def filter_channel_values(event):
            typed = channel_var.get().lower()
            if typed == '':
                channel_combo['values'] = channels
            else:
                filtered = [c for c in channels if c and typed in c.lower()]
                channel_combo['values'] = [''] + filtered
        channel_combo.bind('<KeyRelease>', filter_channel_values)
        
        # SFTP Profile (optional) with tooltip and refresh
        sftp_frame = tk.Frame(right_column, bg='#ffffff')
        sftp_frame.pack(fill="x", pady=(0, 10))
        sftp_header = tk.Frame(sftp_frame, bg='#ffffff')
        sftp_header.pack(fill="x")
        sftp_label = tk.Label(sftp_header, text="📁 SFTP Profile ℹ️", font=('Segoe UI', 10), 
                             bg='#ffffff', fg='#6b7280', cursor='question_arrow')
        sftp_label.pack(side="left")
        refresh_sftp_btn = tk.Button(sftp_header, text="🔄", font=('Segoe UI', 8), 
                                    bg='#f3f4f6', fg='#6b7280', relief='flat', 
                                    padx=4, pady=2, cursor='hand2', bd=0)
        refresh_sftp_btn.pack(side="right")
        
        sftp_var = tk.StringVar()
        sftp_combo = ttk.Combobox(sftp_frame, textvariable=sftp_var, font=('Segoe UI', 10))
        
        def load_sftp_profiles():
            sftp_profiles = [''] + [sp[1] for sp in self.db_manager.get_sftp_profiles()]
            sftp_combo['values'] = sftp_profiles
            return sftp_profiles
        
        sftp_profiles = load_sftp_profiles()
        sftp_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(sftp_label, "Optional: Select SFTP profile for file transfers")
        refresh_sftp_btn.configure(command=load_sftp_profiles)
        
        # Enable search in SFTP dropdown
        def filter_sftp_values(event):
            typed = sftp_var.get().lower()
            if typed == '':
                sftp_combo['values'] = sftp_profiles
            else:
                filtered = [s for s in sftp_profiles if s and typed in s.lower()]
                sftp_combo['values'] = [''] + filtered
        sftp_combo.bind('<KeyRelease>', filter_sftp_values)
        
        # Tenant (required) with tooltip and refresh
        tenant_frame = tk.Frame(right_column, bg='#ffffff')
        tenant_frame.pack(fill="x", pady=(0, 10))
        tenant_header = tk.Frame(tenant_frame, bg='#ffffff')
        tenant_header.pack(fill="x")
        tenant_label = tk.Label(tenant_header, text="🏗️ Tenant * ℹ️", font=('Segoe UI', 10, 'bold'), 
                               bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        tenant_label.pack(side="left")
        refresh_tenant_btn = tk.Button(tenant_header, text="🔄", font=('Segoe UI', 8), 
                                      bg='#f3f4f6', fg='#6b7280', relief='flat', 
                                      padx=4, pady=2, cursor='hand2', bd=0)
        refresh_tenant_btn.pack(side="right")
        
        tenant_var = tk.StringVar()
        tenant_combo = ttk.Combobox(tenant_frame, textvariable=tenant_var, font=('Segoe UI', 10))
        
        def load_tenants():
            try:
                tenants = self.db_manager.get_tenants()
                tenant_list = [f"{t[1]} ({t[2]})" for t in tenants]  # "TENANT_ID (Environment)"
                if not tenant_list:
                    tenant_list = ['TAMICS10_AX1 (Sandbox)']  # Default fallback
                tenant_combo['values'] = tenant_list
                return tenant_list
            except:
                # Fallback if tenant management not set up yet
                tenant_list = ['TAMICS10_AX1 (Sandbox)', 'PROD (Production)', 'TEST (Test)', 'DEV (Development)']
                tenant_combo['values'] = tenant_list
                return tenant_list
        
        tenant_list = load_tenants()
        tenant_combo.set("TAMICS10_AX1 (Sandbox)")  # Default value
        tenant_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(tenant_label, "Select tenant from configured list (managed in Other Settings)")
        refresh_tenant_btn.configure(command=load_tenants)
        
        # Enable search in tenant dropdown
        def filter_tenant_values(event):
            typed = tenant_var.get().lower()
            if typed == '':
                tenant_combo['values'] = tenant_list
            else:
                filtered = [t for t in tenant_list if typed in t.lower()]
                tenant_combo['values'] = filtered
        tenant_combo.bind('<KeyRelease>', filter_tenant_values)
        
        # Modern button frame
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(pady=(10, 0))
        
        # Real-time validation function
        def validate_field(entry, is_required=False):
            value = entry.get().strip()
            if is_required and not value:
                entry.configure(highlightcolor='#ef4444', highlightbackground='#fecaca')
                return False
            else:
                entry.configure(highlightcolor='#10b981', highlightbackground='#d1fae5')
                return True
        
        # Bind validation to required fields (excluding readonly client field)
        rice_id_entry.bind('<KeyRelease>', lambda e: validate_field(rice_id_entry, True))
        name_entry.bind('<KeyRelease>', lambda e: validate_field(name_entry, True))
        
        def save_rice_profile():
            # Validate all required fields (client is auto-populated, tenant is dropdown)
            valid_rice_id = validate_field(rice_id_entry, True)
            valid_name = validate_field(name_entry, True)
            valid_type = type_var.get().strip() != ''
            valid_tenant = tenant_var.get().strip() != ''
            # Client is always valid since it's auto-populated
            valid_client = True
            
            if not all([valid_rice_id, valid_name, valid_client, valid_type, valid_tenant]):
                self.show_popup("Validation Error", "Please fill in all required fields (marked with *)", "error")
                return
            
            try:
                rice_id = rice_id_entry.get().strip()
                name = name_entry.get().strip()
                # Get client name from readonly field
                client_entry.configure(state='normal')
                client_name = client_entry.get().strip()
                client_entry.configure(state='readonly')
                profile_type = type_var.get().strip()
                # Extract tenant ID from dropdown selection (before parentheses)
                tenant_selection = tenant_var.get().strip()
                tenant = tenant_selection.split(' (')[0] if ' (' in tenant_selection else tenant_selection
                channel_name = channel_var.get().strip() or None
                sftp_profile_name = sftp_var.get().strip() or None
                
                self.db_manager.save_rice_profile(rice_id, name, profile_type, client_name, channel_name, sftp_profile_name, tenant)
                popup.destroy()
                self.load_rice_profiles()
                self.show_popup("Success", f"RICE '{rice_id}' created successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to save RICE: {str(e)}", "error")
        
        # Modern button styling with enhanced hover effects
        save_btn = tk.Button(btn_frame, text="💾 Save RICE", font=('Segoe UI', 10, 'bold'), 
                            bg='#3b82f6', fg='#ffffff', relief='flat', padx=20, pady=10, 
                            cursor='hand2', bd=0, highlightthickness=0, command=save_rice_profile)
        save_btn.pack(side="left", padx=(0, 15))
        
        cancel_btn = tk.Button(btn_frame, text="✕ Cancel", font=('Segoe UI', 10, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                              cursor='hand2', bd=0, highlightthickness=0, command=popup.destroy)
        cancel_btn.pack(side="left")
        
        # Add hover effects
        def on_save_hover(event):
            save_btn.configure(bg='#2563eb')
        def on_save_leave(event):
            save_btn.configure(bg='#3b82f6')
        def on_cancel_hover(event):
            cancel_btn.configure(bg='#4b5563')
        def on_cancel_leave(event):
            cancel_btn.configure(bg='#6b7280')
        
        save_btn.bind('<Enter>', on_save_hover)
        save_btn.bind('<Leave>', on_save_leave)
        cancel_btn.bind('<Enter>', on_cancel_hover)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
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
        
        # Get TES-070 versions from database for this specific RICE (latest 5 only)
        all_versions = self.db_manager.get_tes070_versions(rice_id)
        versions = all_versions[:5]  # Limit to latest 5 versions
        
        if not versions:
            self.show_popup("No History", "No TES-070 versions found for this RICE profile.", "warning")
            return
        
        # Create history dialog
        from rice_dialogs import create_enhanced_dialog
        history_popup = create_enhanced_dialog(None, "TES-070 History", 628, 392, modal=False)
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
                # Debug: Print raw timestamp to see format
                print(f"Raw timestamp from DB: '{created_at}'")
                
                # Handle different timestamp formats from database
                if 'T' in created_at:
                    # ISO format with T separator
                    date_obj = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                else:
                    # SQLite CURRENT_TIMESTAMP format: YYYY-MM-DD HH:MM:SS
                    date_obj = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                formatted_date = date_obj.strftime('%m/%d/%Y %I:%M:%S %p')
                print(f"Formatted date: '{formatted_date}'")
            except Exception as e:
                print(f"Date parsing error: {e}")
                # Fallback to original timestamp if parsing fails
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
