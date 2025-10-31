#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import os
import re
from rice_pagination import PaginationManager
from rice_dialogs import RiceDialogs, center_dialog
from rice_scenario_manager import ScenarioManager

class RiceDataManager:
    def __init__(self, db_manager, show_popup_callback, rice_manager_ref=None, rice_ui_ref=None):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self._rice_manager_ref = rice_manager_ref
        self._rice_ui_ref = rice_ui_ref
        
        # Initialize managers
        self.pagination = PaginationManager()
        self.dialogs = RiceDialogs(db_manager, show_popup_callback)
        self.scenario_manager = ScenarioManager(db_manager, show_popup_callback)
        
        # Set reference for auto-refresh functionality
        self.scenario_manager.set_rice_data_manager_ref(self)
        
        # Initialize current_profile as None to ensure proper validation
        self.current_profile = None
        self.selected_rice_profile = None
        self.selected_rice_row = None  # Track selected row widget
        
        # Initialize responsive configuration with dynamic scale factor
        try:
            import tkinter as tk
            root = tk._default_root or tk.Tk()
            screen_width = root.winfo_screenwidth()
            # Scale factor based on screen width: 1.0 for 1920px, higher for larger screens
            scale_factor = max(1.0, screen_width / 1920.0)
        except:
            scale_factor = 1.0
            
        self.responsive_config = {
            'scale_factor': scale_factor,
            'fonts': {
                'button': ('Segoe UI', 10, 'bold'),
                'header': ('Segoe UI', 14, 'bold')
            },
            'padding': {
                'small': 15,
                'tiny': 10
            }
        }
    
    def step_contains_url(self, step):
        """Check if a step contains a URL that might need tenant replacement"""
        step_type = step.get('type', '')
        step_target = step.get('target', '')
        
        # Web Navigation steps always contain URLs
        if step_type == 'Web Navigation':
            return True
        
        # Check for URL patterns in target for any step type
        url_indicators = ['http://', 'https://', 'inforcloudsuite.com', 'mingle-portal']
        if any(indicator in step_target.lower() for indicator in url_indicators):
            return True
        
        # Check for tenant patterns in target for any step type
        tenant_patterns = ['tamics10-ax1', 'TAMICS10_AX1', 'tamics10_ax1']
        if any(pattern in step_target for pattern in tenant_patterns):
            return True
        
        # Check for generic tenant patterns using regex
        # Pattern for dash format (tenant-env)
        if re.search(r'[a-zA-Z0-9]+-[a-zA-Z0-9]+', step_target):
            return True
        
        # Pattern for underscore format (TENANT_ENV)
        if re.search(r'[A-Z0-9]+_[A-Z0-9]+', step_target):
            return True
        
        return False
    
    def extract_tenant_from_url(self, url):
        """Extract tenant placeholder from URL or target, preserving exact format"""
        if not url:
            return 'tamics10-ax1'
        
        # Common tenant patterns
        # Look for specific tenant patterns - return exact match to preserve format
        # Pattern 1: TAMICS10_AX1 (uppercase underscore - check first for specificity)
        if 'TAMICS10_AX1' in url:
            return 'TAMICS10_AX1'
        
        # Pattern 2: tamics10-ax1 (lowercase dash)
        tamics_dash_match = re.search(r'(tamics10-ax1)', url, re.IGNORECASE)
        if tamics_dash_match:
            return tamics_dash_match.group(1)  # Returns exact case from URL
        
        # Pattern 3: tamics10_ax1 (lowercase underscore)
        if 'tamics10_ax1' in url:
            return 'tamics10_ax1'
        
        # Pattern 4: Generic underscore format (preserve case) - check before dash
        underscore_pattern = r'([a-zA-Z0-9]+_[a-zA-Z0-9]+)'
        underscore_match = re.search(underscore_pattern, url)
        if underscore_match:
            return underscore_match.group(1)  # Returns exact case from URL
        
        # Pattern 5: Generic dash format (preserve case)
        dash_pattern = r'([a-zA-Z0-9]+-[a-zA-Z0-9]+)'
        dash_match = re.search(dash_pattern, url)
        if dash_match:
            return dash_match.group(1)  # Returns exact case from URL
        
        # Default fallback
        return 'tamics10-ax1'
    
    # Delegate pagination methods
    def rice_prev_page(self, ui_components):
        self.pagination.rice_prev_page(ui_components, self.load_rice_profiles)
        self.clear_scenarios(ui_components)
    
    def rice_next_page(self, ui_components):
        self.pagination.rice_next_page(ui_components, self.load_rice_profiles)
        self.clear_scenarios(ui_components)
    
    def scenarios_prev_page(self, ui_components):
        self.pagination.scenarios_prev_page(ui_components, self.load_rice_scenarios)
    
    def scenarios_next_page(self, ui_components):
        self.pagination.scenarios_next_page(ui_components, self.load_rice_scenarios)
    
    def change_rice_per_page(self, new_per_page, ui_components):
        self.pagination.change_rice_per_page(new_per_page, ui_components, self.load_rice_profiles, self.clear_scenarios)
    
    def change_scenarios_per_page(self, new_per_page, ui_components):
        self.pagination.change_scenarios_per_page(new_per_page, ui_components, self.load_rice_scenarios)
    
    # Delegate dialog methods
    def edit_rice_profile(self, profile_id):
        self.dialogs.edit_rice_profile(profile_id, self.refresh_rice_profiles_table)
    
    def _show_rice_actions_menu(self, button, profile_id):
        """Show actions menu for RICE profile"""
        import tkinter as tk
        from tkinter import ttk
        
        # Create popup menu with left-aligned labels
        menu = tk.Menu(button, tearoff=0, font=('Segoe UI', 9))
        menu.add_command(label="📋 Duplicate", command=lambda: self.duplicate_rice_profile(profile_id))
        menu.add_separator()
        menu.add_command(label="🗑️ Delete", command=lambda: self.delete_rice_profile(profile_id))
        
        # Show menu at button location
        try:
            x = button.winfo_rootx()
            y = button.winfo_rooty() + button.winfo_height()
            menu.post(x, y)
        except:
            pass
    
    def duplicate_rice_profile(self, profile_id):
        """Duplicate RICE profile"""
        try:
            cursor = self.db_manager.conn.cursor()
            
            # Get original RICE profile details
            cursor.execute("""
                SELECT rice_id, name, type, client_name, channel_name, sftp_profile_name, tenant
                FROM rice_profiles 
                WHERE id = ? AND user_id = ?
            """, (profile_id, self.db_manager.user_id))
            original = cursor.fetchone()
            
            if not original:
                self.show_popup("Error", "RICE profile not found", "error")
                return
            
            rice_id, name, profile_type, client_name, channel_name, sftp_profile_name, tenant = original
            
            # Create new RICE ID by appending "_Copy"
            new_rice_id = f"{rice_id}_Copy"
            new_name = f"{name} (Copy)"
            
            # Check if the new RICE ID already exists
            cursor.execute("SELECT id FROM rice_profiles WHERE rice_id = ? AND user_id = ?", (new_rice_id, self.db_manager.user_id))
            if cursor.fetchone():
                # If exists, append a number
                counter = 2
                while True:
                    test_rice_id = f"{rice_id}_Copy{counter}"
                    cursor.execute("SELECT id FROM rice_profiles WHERE rice_id = ? AND user_id = ?", (test_rice_id, self.db_manager.user_id))
                    if not cursor.fetchone():
                        new_rice_id = test_rice_id
                        new_name = f"{name} (Copy {counter})"
                        break
                    counter += 1
            
            # Create new RICE profile
            cursor.execute("""
                INSERT INTO rice_profiles (user_id, rice_id, name, type, client_name, channel_name, sftp_profile_name, tenant)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.db_manager.user_id, new_rice_id, new_name, profile_type, client_name, channel_name, sftp_profile_name, tenant))
            
            self.db_manager.conn.commit()
            
            # Refresh the RICE profiles table
            self.refresh_rice_profiles_table()
            
            self.show_popup("Success", f"RICE profile '{new_rice_id}' created successfully!", "success")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to duplicate RICE profile: {str(e)}", "error")
    
    def delete_rice_profile(self, profile_id):
        self.dialogs.delete_rice_profile(profile_id, self.refresh_rice_profiles_table)
    
    # Delegate scenario methods
    def reset_scenario(self, scenario_id):
        self.scenario_manager.reset_scenario(scenario_id, self.current_profile, self.refresh_scenarios_table)
    
    def delete_scenario(self, scenario_id):
        self.scenario_manager.delete_scenario(scenario_id, self.current_profile, self.refresh_scenarios_table)
    
    def download_file(self, file_path):
        self.scenario_manager.download_file(file_path)
    
    def select_scenario(self, scenario_id, ui_components):
        self.scenario_manager.select_scenario(scenario_id, ui_components)
    
    def clear_scenarios(self, ui_components):
        """Clear scenarios when changing pages"""
        for widget in ui_components['scenarios_scroll_frame'].winfo_children():
            widget.destroy()
        self.current_profile = None
        self.pagination.scenarios_current_page = 1
        ui_components['scenarios_label'].config(text="Scenarios")
    
    def refresh_scenarios_table(self):
        """Auto-refresh scenarios table to show real-time updates"""
        if hasattr(self, '_ui_components_ref') and self._ui_components_ref:
            self.load_rice_scenarios(self._ui_components_ref)
    
    def load_rice_profiles(self, ui_components):
        """Load RICE profiles into the UI table and refresh scenarios if profile selected"""
        # Store reference for auto-refresh
        self._ui_components_ref = ui_components
        
        # Show loading indicator
        if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref and hasattr(self._rice_ui_ref, 'show_loading'):
            self._rice_ui_ref.show_loading()
        
        # Update filter options if UI exists
        self._update_filter_options(ui_components)
        
        # Clear existing profiles
        existing_widgets = ui_components['rice_scroll_frame'].winfo_children()
        print(f"DEBUG: Clearing {len(existing_widgets)} existing widgets")
        for widget in existing_widgets:
            widget.destroy()
        
        # Get search and filter criteria from UI
        search_term = ""
        type_filter = ""
        client_filter = ""
        
        # Extract search terms from UI components
        try:
            # Get search term
            if 'rice_search_var' in ui_components:
                search_term = ui_components['rice_search_var'].get()
                if search_term == "Search RICE items..." or not search_term.strip():
                    search_term = ""
            
            # Get type filter
            if 'rice_type_filter_var' in ui_components:
                type_filter = ui_components['rice_type_filter_var'].get()
                if type_filter == "All":
                    type_filter = ""
            
            # Client filter removed - users linked to single client
            client_filter = ""
                    
            print(f"DEBUG: Extracted filters - Search: '{search_term}', Type: '{type_filter}'")
        except Exception as e:
            print(f"DEBUG: Error extracting search terms: {e}")
            # Fallback to empty filters
            search_term = ""
            type_filter = ""
            client_filter = ""
        
        # Get total count first for result display
        total_profiles = len(self.db_manager.get_rice_profiles_filtered(0, 999999, "", "", ""))
        
        # Get filtered profiles from database (no pagination limits)
        profiles = self.db_manager.get_rice_profiles_filtered(0, 999999, 
                                                            search_term, type_filter, client_filter)
        filtered_count = len(profiles)
        
        # Debug output
        print(f"DEBUG: Loading RICE profiles for user_id={self.db_manager.user_id}")
        print(f"DEBUG: Found {filtered_count} profiles, total={total_profiles}")
        print(f"DEBUG: Search='{search_term}', Type='{type_filter}'")
        print(f"DEBUG: No pagination - showing all records")
        for i, profile in enumerate(profiles):
            print(f"DEBUG: Profile {i}: {profile}")
        
        # No pagination - showing all records with scroll
        
        # Create profile rows or show empty state
        if profiles:
            print(f"DEBUG: Creating {len(profiles)} profile rows")
            first_profile_id = None
            first_rice_id = None
            first_row_widget = None
            
            for i, profile in enumerate(profiles):
                row_widget = self._create_rice_profile_row(ui_components['rice_scroll_frame'], profile, i)
                print(f"DEBUG: Created row {i} widget: {row_widget}")
                
                # Store first profile for auto-selection
                if i == 0:
                    first_profile_id = profile[0]  # profile_id
                    first_rice_id = profile[1]     # rice_id
                    first_row_widget = row_widget
            
            # Auto-select first profile if no current selection
            if first_profile_id and not self.current_profile:
                # Use a small delay to ensure UI is fully rendered before selection
                ui_components['rice_scroll_frame'].after(100, 
                    lambda: self._select_rice_profile(first_profile_id, first_rice_id, first_row_widget)
                )
            
            # Calculate content height and adjust canvas
            content_height = len(profiles) * 35  # 35px per row
            print(f"DEBUG: Calculated content height: {content_height}px")
            if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref:
                # Use after_idle to ensure UI is ready before height calculation
                ui_components['rice_scroll_frame'].after_idle(
                    lambda: self._rice_ui_ref.adjust_rice_canvas_height(content_height)
                )
            else:
                print("DEBUG: No _rice_ui_ref available for height adjustment")
            
            # Update search results count and hide loading
            def _update_ui():
                if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref:
                    if hasattr(self._rice_ui_ref, 'update_search_results_count'):
                        self._rice_ui_ref.update_search_results_count(filtered_count, total_profiles)
                    if hasattr(self._rice_ui_ref, 'hide_loading'):
                        self._rice_ui_ref.hide_loading()
            
            ui_components['rice_scroll_frame'].after_idle(_update_ui)
        else:
            print("DEBUG: No profiles found, showing empty state")
            # Clear current selection and scenarios when no profiles match
            self.current_profile = None
            self.selected_rice_profile = None
            self.selected_rice_row = None
            ui_components['scenarios_label'].config(text="Scenarios")
            # Clear scenarios
            for widget in ui_components['scenarios_scroll_frame'].winfo_children():
                widget.destroy()
            self._create_scenarios_empty_state(ui_components['scenarios_scroll_frame'])
            
            self._create_rice_empty_state(ui_components['rice_scroll_frame'])
            # Adjust canvas for empty state (120px height)
            if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref:
                ui_components['rice_scroll_frame'].after_idle(
                    lambda: self._rice_ui_ref.adjust_rice_canvas_height(120)
                )
                if hasattr(self._rice_ui_ref, 'adjust_scenarios_canvas_height'):
                    ui_components['scenarios_scroll_frame'].after_idle(
                        lambda: self._rice_ui_ref.adjust_scenarios_canvas_height(100)
                    )
            
            # Update search results count and hide loading for empty state
            def _update_empty_ui():
                if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref:
                    if hasattr(self._rice_ui_ref, 'update_search_results_count'):
                        self._rice_ui_ref.update_search_results_count(0, total_profiles)
                    if hasattr(self._rice_ui_ref, 'hide_loading'):
                        self._rice_ui_ref.hide_loading()
            
            ui_components['rice_scroll_frame'].after_idle(_update_empty_ui)
        
        # If a profile is currently selected, refresh its scenarios too
        if self.current_profile:
            self.load_rice_scenarios(ui_components)
    
    def load_rice_scenarios(self, ui_components):
        """Load scenarios for selected RICE profile"""
        if not self.current_profile:
            return
        
        # Clear existing scenarios
        for widget in ui_components['scenarios_scroll_frame'].winfo_children():
            widget.destroy()
        
        # Get all scenarios from database (no pagination limits)
        scenarios = self.db_manager.get_scenarios_paginated(self.current_profile, 0, 999999)
        total_scenarios = len(scenarios)
        
        # No pagination - showing all scenarios with scroll
        
        # Create scenario rows or show empty state
        if scenarios:
            for i, scenario in enumerate(scenarios):
                self._create_scenario_row(ui_components['scenarios_scroll_frame'], scenario, i)
            # Adjust scenarios canvas height
            content_height = len(scenarios) * 35
            if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref and hasattr(self._rice_ui_ref, 'adjust_scenarios_canvas_height'):
                ui_components['scenarios_scroll_frame'].after_idle(
                    lambda: self._rice_ui_ref.adjust_scenarios_canvas_height(content_height)
                )
        else:
            self._create_scenarios_empty_state(ui_components['scenarios_scroll_frame'])
            if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref and hasattr(self._rice_ui_ref, 'adjust_scenarios_canvas_height'):
                ui_components['scenarios_scroll_frame'].after_idle(
                    lambda: self._rice_ui_ref.adjust_scenarios_canvas_height(100)
                )
    
    def _create_rice_profile_row(self, parent, profile, row_index):
        """Create a single RICE profile row"""
        # profile = (id, rice_id, name, client_name, channel_name, sftp_profile_name, type_name, tenant)
        profile_id, rice_id, name, client_name, channel_name, sftp_profile_name, type_name, tenant = profile
        
        # Row background color
        bg_color = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
        
        # Main row frame
        row_frame = tk.Frame(parent, bg=bg_color, height=35)
        row_frame.pack(fill='x')
        row_frame.pack_propagate(False)
        
        # Get column configuration from UI (passed via rice_ui_ref)
        if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref and hasattr(self._rice_ui_ref, 'RICE_COLUMNS'):
            RICE_COLS = self._rice_ui_ref.RICE_COLUMNS
        else:
            # Fallback configuration
            RICE_COLS = {
                'rice_id': {'start': 0.0, 'width': 0.12},
                'name': {'start': 0.12, 'width': 0.25},
                'type': {'start': 0.37, 'width': 0.18},
                'channel': {'start': 0.55, 'width': 0.12},
                'sftp': {'start': 0.67, 'width': 0.13},
                'actions': {'start': 0.80, 'width': 0.20}
            }
        
        # RICE ID
        rice_id_label = tk.Label(row_frame, text=rice_id or '', font=('Segoe UI', 9), 
                                bg=bg_color, fg='#374151', anchor='w', padx=18)
        rice_id_label.place(relx=RICE_COLS['rice_id']['start'], y=8, relwidth=RICE_COLS['rice_id']['width'])
        
        # Name
        name_label = tk.Label(row_frame, text=name or '', font=('Segoe UI', 9), 
                             bg=bg_color, fg='#374151', anchor='w', padx=18)
        name_label.place(relx=RICE_COLS['name']['start'], y=8, relwidth=RICE_COLS['name']['width'])
        
        # Type
        type_label = tk.Label(row_frame, text=type_name or '', font=('Segoe UI', 9), 
                             bg=bg_color, fg='#374151', anchor='w', padx=18)
        type_label.place(relx=RICE_COLS['type']['start'], y=8, relwidth=RICE_COLS['type']['width'])
        
        # Channel
        channel_label = tk.Label(row_frame, text=channel_name or '', font=('Segoe UI', 9), 
                                bg=bg_color, fg='#374151', anchor='w', padx=18)
        channel_label.place(relx=RICE_COLS['channel']['start'], y=8, relwidth=RICE_COLS['channel']['width'])
        
        # SFTP
        sftp_label = tk.Label(row_frame, text=sftp_profile_name or '', font=('Segoe UI', 9), 
                             bg=bg_color, fg='#374151', anchor='w', padx=18)
        sftp_label.place(relx=RICE_COLS['sftp']['start'], y=8, relwidth=RICE_COLS['sftp']['width'])
        
        # Actions buttons - Primary + Menu approach
        actions_frame = tk.Frame(row_frame, bg=bg_color)
        actions_frame.place(relx=RICE_COLS['actions']['start'], y=5, relwidth=RICE_COLS['actions']['width'], height=25)
        
        # Edit button (primary action for RICE)
        edit_btn = tk.Button(actions_frame, text="✎ Edit", font=('Segoe UI', 8), 
                            bg='#3b82f6', fg='#ffffff', relief='flat', padx=4, pady=2, 
                            cursor='hand2', bd=0, highlightthickness=0,
                            command=lambda: self.edit_rice_profile(profile_id))
        edit_btn.pack(side='left')
        
        # More actions menu button
        more_btn = tk.Button(actions_frame, text="•••", font=('Segoe UI', 8), 
                            bg='#6b7280', fg='#ffffff', relief='flat', padx=6, pady=2, 
                            cursor='hand2', bd=0, highlightthickness=0,
                            command=lambda: self._show_rice_actions_menu(more_btn, profile_id))
        more_btn.pack(side='left')
        
        # Enhanced hover effect
        def on_enter(e):
            if not hasattr(self, 'selected_rice_row') or row_frame != self.selected_rice_row:
                row_frame.config(bg='#f8fafc')
                for child in row_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#f8fafc')
                    elif isinstance(child, tk.Frame):
                        child.config(bg='#f8fafc')
        
        def on_leave(e):
            if not hasattr(self, 'selected_rice_row') or row_frame != self.selected_rice_row:
                row_frame.config(bg=bg_color)
                for child in row_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=bg_color)
                    elif isinstance(child, tk.Frame):
                        child.config(bg=bg_color)
        
        row_frame.bind('<Enter>', on_enter)
        row_frame.bind('<Leave>', on_leave)
        
        # Add click handler for row selection
        def on_click(e):
            self._select_rice_profile(profile_id, rice_id, row_frame)
        
        row_frame.bind('<Button-1>', on_click)
        row_frame.configure(cursor='hand2')
        
        # Make all labels clickable
        for child in [rice_id_label, name_label, type_label, channel_label, sftp_label]:
            child.bind('<Button-1>', on_click)
            child.configure(cursor='hand2')
        
        # Add mouse wheel scrolling to row and all its children
        def _on_row_mousewheel(event):
            # Find the canvas by traversing up the widget hierarchy
            widget = row_frame
            while widget and not isinstance(widget.master, tk.Canvas):
                widget = widget.master
            if widget and isinstance(widget.master, tk.Canvas):
                widget.master.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel with scroll prevention for insufficient content
        def _on_row_mousewheel_safe(event):
            # Only scroll if content height exceeds canvas height
            widget = row_frame
            while widget and not isinstance(widget.master, tk.Canvas):
                widget = widget.master
            if widget and isinstance(widget.master, tk.Canvas):
                canvas = widget.master
                canvas.update_idletasks()
                content_height = canvas.bbox("all")[3] if canvas.bbox("all") else 0
                canvas_height = canvas.winfo_height()
                if content_height > canvas_height:
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        row_frame.bind("<MouseWheel>", _on_row_mousewheel_safe)
        for child in row_frame.winfo_children():
            child.bind("<MouseWheel>", _on_row_mousewheel_safe)
            # Also bind to grandchildren (buttons in action frames)
            if hasattr(child, 'winfo_children'):
                for grandchild in child.winfo_children():
                    grandchild.bind("<MouseWheel>", _on_row_mousewheel_safe)
        
        return row_frame
    
    def _create_rice_empty_state(self, parent):
        """Create empty state for RICE profiles"""
        empty_frame = tk.Frame(parent, bg='#ffffff', height=120)
        empty_frame.pack(fill='x', pady=10)
        empty_frame.pack_propagate(False)
        
        # Center content
        content_frame = tk.Frame(empty_frame, bg='#ffffff')
        content_frame.pack(expand=True)
        
        # Icon and message
        tk.Label(content_frame, text="📋", font=('Segoe UI', 24), bg='#ffffff', fg='#9ca3af').pack(pady=(0, 5))
        tk.Label(content_frame, text="No RICE Items Found", font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#374151').pack()
        tk.Label(content_frame, text="Get started by creating your first RICE item for testing", 
                font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(pady=(3, 0))
        
        # Disable mouse wheel scrolling for empty state
        def _disable_scroll(event):
            return "break"
        
        empty_frame.bind("<MouseWheel>", _disable_scroll)
        content_frame.bind("<MouseWheel>", _disable_scroll)
        
        return empty_frame
    
    def _create_scenarios_empty_state(self, parent):
        """Create empty state for scenarios"""
        empty_frame = tk.Frame(parent, bg='#ffffff', height=100)
        empty_frame.pack(fill='x', pady=10)
        empty_frame.pack_propagate(False)
        
        # Center content
        content_frame = tk.Frame(empty_frame, bg='#ffffff')
        content_frame.pack(expand=True)
        
        # Get responsive values for proper scaling
        if hasattr(self, 'responsive_config') and self.responsive_config:
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
        else:
            scale_factor = 1.0
        
        # Dynamic font sizes and padding for scenarios with proper responsive scaling
        icon_size = max(28, int(36 * scale_factor))
        title_size = max(12, int(14 * scale_factor))
        desc_size = max(9, int(10 * scale_factor))
        btn_size = max(9, int(10 * scale_factor))
        btn_padx = max(20, int(35 * scale_factor))
        btn_pady = max(10, int(12 * scale_factor))
        
        if self.current_profile:
            # Has RICE selected but no scenarios
            tk.Label(content_frame, text="🎯", font=('Segoe UI', 20), bg='#ffffff', fg='#9ca3af').pack(pady=(0, 5))
            tk.Label(content_frame, text="No Test Scenarios Yet", font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#374151').pack()
            tk.Label(content_frame, text="Add test scenarios to start automating your testing process", 
                    font=('Segoe UI', 8), bg='#ffffff', fg='#6b7280').pack(pady=(2, 0))
        else:
            # No RICE selected
            tk.Label(content_frame, text="👆", font=('Segoe UI', 20), bg='#ffffff', fg='#9ca3af').pack(pady=(0, 5))
            tk.Label(content_frame, text="Select a RICE Item Above", font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#374151').pack()
            tk.Label(content_frame, text="Choose a RICE item from the list above to view its test scenarios", 
                    font=('Segoe UI', 8), bg='#ffffff', fg='#6b7280').pack(pady=(2, 0))
        
        # Disable mouse wheel scrolling for empty state
        def _disable_scroll(event):
            return "break"
        
        empty_frame.bind("<MouseWheel>", _disable_scroll)
        content_frame.bind("<MouseWheel>", _disable_scroll)
        
        return empty_frame
    
    def _trigger_add_rice(self):
        """Trigger add RICE profile from empty state"""
        if hasattr(self, '_rice_manager_ref') and self._rice_manager_ref:
            self._rice_manager_ref.add_rice_profile()
    
    def _trigger_add_scenario(self):
        """Trigger add scenario from empty state"""
        if hasattr(self, '_rice_manager_ref') and self._rice_manager_ref:
            self._rice_manager_ref.add_scenario()
    
    def _update_filter_options(self, ui_components):
        """Update filter dropdown options based on available data"""
        try:
            # Get unique types from database
            cursor = self.db_manager.conn.cursor()
            
            # Get types that are actually used in rice_profiles
            cursor.execute("""
                SELECT DISTINCT rt.type_name FROM rice_types rt
                JOIN rice_profiles rp ON rp.type = rt.type_name
                WHERE rp.user_id = ?
                ORDER BY rt.type_name
            """, (self.db_manager.user_id,))
            types = ["All"] + [row[0] for row in cursor.fetchall()]
            
            print(f"DEBUG: Found types for filter: {types}")
            
            # Update type filter dropdown directly from ui_components
            if 'rice_type_filter' in ui_components:
                try:
                    ui_components['rice_type_filter']['values'] = types
                    print(f"DEBUG: Updated type filter with {len(types)} options")
                except Exception as e:
                    print(f"DEBUG: Could not update type filter: {e}")
            
            # Also try to update via rice_ui_ref if available
            if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref and hasattr(self._rice_ui_ref, 'rice_type_filter'):
                try:
                    self._rice_ui_ref.rice_type_filter['values'] = types
                    print(f"DEBUG: Updated type filter via rice_ui_ref")
                except Exception as e:
                    print(f"DEBUG: Could not update type filter via rice_ui_ref: {e}")
                        
        except Exception as e:
            print(f"DEBUG: Error in _update_filter_options: {e}")
            # Ignore errors during filter update
            pass
    
    def _select_rice_profile(self, profile_id, rice_id, row_frame):
        """Select a RICE profile and load its scenarios"""
        # Clear previous selection
        if self.selected_rice_row:
            try:
                # Check if widget still exists before accessing it
                if self.selected_rice_row.winfo_exists():
                    # Get original background color based on row position
                    try:
                        row_index = list(self.selected_rice_row.master.winfo_children()).index(self.selected_rice_row)
                        original_bg = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
                    except:
                        original_bg = '#ffffff'
                    
                    self.selected_rice_row.config(bg=original_bg, relief='flat', bd=0)
                    for child in self.selected_rice_row.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg=original_bg, fg='#374151')
                        elif isinstance(child, tk.Frame):
                            child.config(bg=original_bg)
            except tk.TclError:
                # Widget has been destroyed, ignore
                pass
        
        # Set new selection
        self.selected_rice_row = row_frame
        self.selected_rice_profile = profile_id
        self.current_profile = profile_id
        
        # Enhanced selection highlighting with blue accent
        try:
            row_frame.config(bg='#dbeafe', relief='solid', bd=1)
            for child in row_frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg='#dbeafe', fg='#1e40af')
                elif isinstance(child, tk.Frame):
                    child.config(bg='#dbeafe')
        except tk.TclError:
            # Widget has been destroyed, ignore
            pass
        
        # Update scenarios label
        if hasattr(self, '_ui_components_ref') and self._ui_components_ref:
            self._ui_components_ref['scenarios_label'].config(text=f"Scenarios - {rice_id}")
            # Load scenarios for this profile
            self.load_rice_scenarios(self._ui_components_ref)
    
    def _create_scenario_row(self, parent, scenario, row_index):
        """Create a single scenario row"""
        # scenario = (id, scenario_number, description, result, file_path)
        scenario_id, scenario_number, description, result, file_path = scenario
        
        # Row background color
        bg_color = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
        
        # Main row frame
        row_frame = tk.Frame(parent, bg=bg_color, height=35)
        row_frame.pack(fill='x')
        row_frame.pack_propagate(False)
        
        # Get column configuration from UI (passed via rice_ui_ref)
        if hasattr(self, '_rice_ui_ref') and self._rice_ui_ref and hasattr(self._rice_ui_ref, 'SCENARIOS_COLUMNS'):
            SCENARIO_COLS = self._rice_ui_ref.SCENARIOS_COLUMNS
        else:
            # Fallback configuration
            SCENARIO_COLS = {
                'scenario': {'start': 0.0, 'width': 0.10},
                'description': {'start': 0.10, 'width': 0.35},
                'result': {'start': 0.45, 'width': 0.08},
                'steps': {'start': 0.53, 'width': 0.07},
                'file': {'start': 0.60, 'width': 0.06},
                'screenshot': {'start': 0.66, 'width': 0.07},
                'actions': {'start': 0.73, 'width': 0.27}
            }
        
        # Scenario number
        scenario_label = tk.Label(row_frame, text=f"#{scenario_number}", font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', anchor='w', padx=18)
        scenario_label.place(relx=SCENARIO_COLS['scenario']['start'], y=8, relwidth=SCENARIO_COLS['scenario']['width'])
        
        # Description
        desc_label = tk.Label(row_frame, text=description or '', font=('Segoe UI', 9), 
                             bg=bg_color, fg='#374151', anchor='w', padx=18)
        desc_label.place(relx=SCENARIO_COLS['description']['start'], y=8, relwidth=SCENARIO_COLS['description']['width'])
        
        # Result
        result_color = '#10b981' if result == 'Passed' else '#ef4444' if result == 'Failed' else '#6b7280'
        result_label = tk.Label(row_frame, text=result or 'Not run', font=('Segoe UI', 9), 
                               bg=bg_color, fg=result_color, anchor='w', padx=18)
        result_label.place(relx=SCENARIO_COLS['result']['start'], y=8, relwidth=SCENARIO_COLS['result']['width'])
        
        # Steps (get actual count from database)
        try:
            # Get step count for this scenario
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM scenario_steps 
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
            """, (self.db_manager.user_id, str(self.current_profile), scenario_number))
            step_count = cursor.fetchone()[0]
        except:
            step_count = 0
        
        # Steps with View button
        steps_frame = tk.Frame(row_frame, bg=bg_color)
        steps_frame.place(relx=SCENARIO_COLS['steps']['start'], y=5, relwidth=SCENARIO_COLS['steps']['width'], height=25)
        
        if step_count > 0:
            steps_btn = tk.Button(steps_frame, text=f"📋 {step_count}", font=('Segoe UI', 8), 
                                bg='#3b82f6', fg='#ffffff', relief='flat', padx=4, pady=2, 
                                cursor='hand2', bd=0, highlightthickness=0,
                                command=lambda: self._view_scenario_steps(scenario_id, scenario_number))
            steps_btn.pack()
        else:
            steps_label = tk.Label(steps_frame, text="0", font=('Segoe UI', 9), 
                                  bg=bg_color, fg='#374151', anchor='center')
            steps_label.pack(expand=True)
        
        # File download button
        file_frame = tk.Frame(row_frame, bg=bg_color)
        file_frame.place(relx=SCENARIO_COLS['file']['start'], y=5, relwidth=SCENARIO_COLS['file']['width'], height=25)
        
        if file_path:
            file_btn = tk.Button(file_frame, text="📁", font=('Segoe UI', 10), 
                                bg='#6b7280', fg='#ffffff', relief='flat', padx=4, pady=2, 
                                cursor='hand2', bd=0, highlightthickness=0,
                                command=lambda: self.download_file(file_path))
            file_btn.pack()
        
        # Screenshot button
        screenshot_frame = tk.Frame(row_frame, bg=bg_color)
        screenshot_frame.place(relx=SCENARIO_COLS['screenshot']['start'], y=5, relwidth=SCENARIO_COLS['screenshot']['width'], height=25)
        
        screenshot_btn = tk.Button(screenshot_frame, text="📷", font=('Segoe UI', 10), 
                                  bg='#3b82f6', fg='#ffffff', relief='flat', padx=4, pady=2, 
                                  cursor='hand2', bd=0, highlightthickness=0,
                                  command=lambda: self._view_screenshots(scenario_id))
        screenshot_btn.pack()
        
        # Actions buttons - Primary + Menu approach
        actions_frame = tk.Frame(row_frame, bg=bg_color)
        actions_frame.place(relx=SCENARIO_COLS['actions']['start'], y=5, relwidth=SCENARIO_COLS['actions']['width'], height=25)
        
        # Run button (primary action for scenarios)
        run_btn = tk.Button(actions_frame, text="▶ Run", font=('Segoe UI', 8), 
                           bg='#10b981', fg='#ffffff', relief='flat', padx=8, pady=2, 
                           cursor='hand2', bd=0, highlightthickness=0,
                           command=lambda: self._run_scenario(scenario_id))
        run_btn.pack(side='left', padx=(0, 5))
        
        # More actions menu button
        more_btn = tk.Button(actions_frame, text="•••", font=('Segoe UI', 8), 
                            bg='#6b7280', fg='#ffffff', relief='flat', padx=6, pady=2, 
                            cursor='hand2', bd=0, highlightthickness=0,
                            command=lambda: self._show_scenario_actions_menu(more_btn, scenario_id))
        more_btn.pack(side='left')
        
        # Add click handler for row selection
        def on_click(e):
            self._select_scenario(scenario_id, row_frame)
        
        row_frame.bind('<Button-1>', on_click)
        row_frame.configure(cursor='hand2')
        
        # Make all labels clickable (only include labels that exist)
        clickable_labels = [scenario_label, desc_label, result_label]
        for child in clickable_labels:
            child.bind('<Button-1>', on_click)
            child.configure(cursor='hand2')
        
        # Add mouse wheel scrolling to scenario row and all its children
        def _on_scenario_row_mousewheel(event):
            # Find the canvas by traversing up the widget hierarchy
            widget = row_frame
            while widget and not isinstance(widget.master, tk.Canvas):
                widget = widget.master
            if widget and isinstance(widget.master, tk.Canvas):
                widget.master.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel with scroll prevention for insufficient content
        def _on_scenario_row_mousewheel_safe(event):
            # Only scroll if content height exceeds canvas height
            widget = row_frame
            while widget and not isinstance(widget.master, tk.Canvas):
                widget = widget.master
            if widget and isinstance(widget.master, tk.Canvas):
                canvas = widget.master
                canvas.update_idletasks()
                content_height = canvas.bbox("all")[3] if canvas.bbox("all") else 0
                canvas_height = canvas.winfo_height()
                if content_height > canvas_height:
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        row_frame.bind("<MouseWheel>", _on_scenario_row_mousewheel_safe)
        for child in row_frame.winfo_children():
            child.bind("<MouseWheel>", _on_scenario_row_mousewheel_safe)
            # Also bind to grandchildren (buttons in action frames)
            if hasattr(child, 'winfo_children'):
                for grandchild in child.winfo_children():
                    grandchild.bind("<MouseWheel>", _on_scenario_row_mousewheel_safe)
        
        # Enhanced hover effect for scenarios
        def on_enter(e):
            if not hasattr(self, 'selected_scenario_row') or row_frame != self.selected_scenario_row:
                row_frame.config(bg='#f8fafc')
                for child in row_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#f8fafc')
                    elif isinstance(child, tk.Frame):
                        child.config(bg='#f8fafc')
        
        def on_leave(e):
            if not hasattr(self, 'selected_scenario_row') or row_frame != self.selected_scenario_row:
                row_frame.config(bg=bg_color)
                for child in row_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=bg_color)
                    elif isinstance(child, tk.Frame):
                        child.config(bg=bg_color)
        
        row_frame.bind('<Enter>', on_enter)
        row_frame.bind('<Leave>', on_leave)
        
        return row_frame
    
    def _select_scenario(self, scenario_id, row_frame):
        """Select a scenario and highlight it"""
        # Clear previous selection
        if hasattr(self, 'selected_scenario_row') and self.selected_scenario_row:
            # Reset to original color
            try:
                row_index = list(self.selected_scenario_row.master.winfo_children()).index(self.selected_scenario_row)
                original_bg = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
                self.selected_scenario_row.config(bg=original_bg, relief='flat', bd=0)
                for child in self.selected_scenario_row.winfo_children():
                    if isinstance(child, tk.Label):
                        # Reset text color based on content
                        if 'Passed' in child.cget('text'):
                            child.config(bg=original_bg, fg='#10b981')
                        elif 'Failed' in child.cget('text'):
                            child.config(bg=original_bg, fg='#ef4444')
                        else:
                            child.config(bg=original_bg, fg='#374151')
                    elif isinstance(child, tk.Frame):
                        child.config(bg=original_bg)
            except:
                pass
        
        # Set new selection
        self.selected_scenario_row = row_frame
        self.selected_scenario_id = scenario_id
        
        # Enhanced selection highlighting for scenarios
        row_frame.config(bg='#dbeafe', relief='solid', bd=1)
        for child in row_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.config(bg='#dbeafe', fg='#1e40af')
            elif isinstance(child, tk.Frame):
                child.config(bg='#dbeafe')
    
    def _view_screenshots(self, scenario_id):
        """View screenshots for scenario"""
        try:
            # Get screenshots from database with proper column handling
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT COALESCE(ts.name, ss.step_name) as step_name, 
                       ss.screenshot_before, ss.screenshot_after 
                FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = (
                    SELECT scenario_number FROM scenarios WHERE id = ? AND user_id = ?
                )
                ORDER BY ss.step_order
            """, (self.db_manager.user_id, str(self.current_profile), scenario_id, self.db_manager.user_id))
            screenshots = cursor.fetchall()
            
            if not screenshots:
                self.show_popup("No Screenshots", "No screenshots found for this scenario.", "warning")
                return
            
            # Get actual scenario number
            cursor.execute("""
                SELECT scenario_number FROM scenarios 
                WHERE id = ? AND user_id = ?
            """, (scenario_id, self.db_manager.user_id))
            scenario_result = cursor.fetchone()
            scenario_number = scenario_result[0] if scenario_result else scenario_id
            
            # Create screenshot viewer dialog
            popup = tk.Toplevel()
            popup.title(f"Screenshots - Scenario #{scenario_number}")
            popup.configure(bg='#ffffff')
            
            # Center the dialog
            center_dialog(popup, 800, 600)
            
            try:
                popup.iconbitmap("infor_logo.ico")
            except:
                pass
            
            # Header
            header_frame = tk.Frame(popup, bg='#8b5cf6', height=50)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            tk.Label(header_frame, text=f"📷 Screenshots - Scenario #{scenario_number}", 
                    font=('Segoe UI', 14, 'bold'), bg='#8b5cf6', fg='#ffffff').pack(expand=True)
            
            # Content frame with scrollbar
            content_frame = tk.Frame(popup, bg='#ffffff')
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Scrollable frame
            canvas = tk.Canvas(content_frame, bg='#ffffff')
            scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='#ffffff')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Enable mouse wheel scrolling
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            def _bind_to_mousewheel(event):
                canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
            def _unbind_from_mousewheel(event):
                canvas.unbind_all("<MouseWheel>")
            
            canvas.bind('<Enter>', _bind_to_mousewheel)
            canvas.bind('<Leave>', _unbind_from_mousewheel)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Display screenshots
            for i, (step_name, before_screenshot, after_screenshot) in enumerate(screenshots):
                step_frame = tk.Frame(scrollable_frame, bg='#f9fafb', relief='solid', bd=1)
                step_frame.pack(fill="x", pady=5)
                
                # Step header
                tk.Label(step_frame, text=f"Step {i+1}: {step_name}", 
                        font=('Segoe UI', 11, 'bold'), bg='#f9fafb', fg='#374151').pack(pady=5)
                
                # Screenshots row
                screenshots_row = tk.Frame(step_frame, bg='#f9fafb')
                screenshots_row.pack(fill="x", padx=10, pady=5)
                
                # Before screenshot
                if before_screenshot:
                    before_frame = tk.Frame(screenshots_row, bg='#ffffff', relief='solid', bd=1)
                    before_frame.pack(side="left", padx=5, pady=5)
                    
                    tk.Label(before_frame, text="Before", font=('Segoe UI', 9, 'bold'), 
                            bg='#ffffff', fg='#374151').pack(pady=2)
                    
                    try:
                        # Load and display image
                        import base64
                        from PIL import Image, ImageTk
                        from io import BytesIO
                        
                        image_data = base64.b64decode(before_screenshot)
                        image = Image.open(BytesIO(image_data))
                        image.thumbnail((600, 400), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        
                        img_label = tk.Label(before_frame, image=photo, bg='#ffffff')
                        img_label.image = photo  # Keep a reference
                        img_label.pack(padx=5, pady=5)
                    except Exception as e:
                        tk.Label(before_frame, text=f"Error loading image: {str(e)}", 
                                bg='#ffffff', fg='#ef4444').pack(padx=5, pady=5)
                
                # After screenshot
                if after_screenshot:
                    after_frame = tk.Frame(screenshots_row, bg='#ffffff', relief='solid', bd=1)
                    after_frame.pack(side="left", padx=5, pady=5)
                    
                    tk.Label(after_frame, text="After", font=('Segoe UI', 9, 'bold'), 
                            bg='#ffffff', fg='#374151').pack(pady=2)
                    
                    try:
                        # Load and display image
                        import base64
                        from PIL import Image, ImageTk
                        from io import BytesIO
                        
                        image_data = base64.b64decode(after_screenshot)
                        image = Image.open(BytesIO(image_data))
                        image.thumbnail((600, 400), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        
                        img_label = tk.Label(after_frame, image=photo, bg='#ffffff')
                        img_label.image = photo  # Keep a reference
                        img_label.pack(padx=5, pady=5)
                    except Exception as e:
                        tk.Label(after_frame, text=f"Error loading image: {str(e)}", 
                                bg='#ffffff', fg='#ef4444').pack(padx=5, pady=5)
            
            # Close button
            close_frame = tk.Frame(popup, bg='#ffffff')
            close_frame.pack(fill="x", padx=20, pady=10)
            
            tk.Button(close_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                     bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=8, 
                     cursor='hand2', bd=0, command=popup.destroy).pack()
            
            popup.transient()
            popup.grab_set()
            popup.focus_set()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to load screenshots: {str(e)}", "error")
    
    def _view_scenario_steps(self, scenario_id, scenario_number):
        """View steps for scenario"""
        self.scenario_manager.view_scenario_steps(scenario_id, scenario_number, self.current_profile)
    
    def _run_scenario(self, scenario_id):
        """Run a single scenario"""
        if not self.current_profile:
            self.show_popup("Error", "No RICE profile selected", "error")
            return
        
        # Call the scenario manager directly
        self.scenario_manager.run_scenario(scenario_id, self.current_profile)
    
    def _edit_scenario(self, scenario_id):
        """Edit scenario with confirmation and reset"""
        # Get scenario info for confirmation
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT scenario_number, description, result FROM scenarios 
            WHERE id = ? AND user_id = ?
        """, (scenario_id, self.db_manager.user_id))
        scenario_data = cursor.fetchone()
        
        if not scenario_data:
            self.show_popup("Error", "Scenario not found", "error")
            return
        
        scenario_number, description, result = scenario_data
        
        # If scenario status is "Not run", skip confirmation and go directly to edit
        if result == 'Not run':
            # Proceed directly with edit
            if hasattr(self, '_rice_manager_ref') and self._rice_manager_ref:
                self._rice_manager_ref.edit_scenario(scenario_id)
            else:
                self.scenario_manager.edit_scenario(scenario_id, self.current_profile, self.refresh_scenarios_table)
            return
        
        # Create confirmation dialog for scenarios that have been run
        confirm_popup = tk.Toplevel()
        confirm_popup.title("Edit Scenario")
        center_dialog(confirm_popup, 450, 280)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(confirm_popup, bg='#f59e0b', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Edit Scenario", font=('Segoe UI', 14, 'bold'), 
                bg='#f59e0b', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Edit Scenario #{scenario_number}:\n'{description}'?\n\nThis will reset the scenario (clear screenshots and\nset status to 'Not run') to maintain scenario integrity.\n\nDo you want to continue?", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_edit():
            try:
                # Reset scenario first
                cursor.execute("""
                    UPDATE scenario_steps 
                    SET screenshot_before = NULL, screenshot_after = NULL, 
                        screenshot_timestamp = NULL, execution_status = NULL
                    WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                """, (self.db_manager.user_id, str(self.current_profile), scenario_number))
                
                cursor.execute("UPDATE scenarios SET result = 'Not run', executed_at = NULL WHERE id = ?", (scenario_id,))
                self.db_manager.conn.commit()
                
                confirm_popup.destroy()
                
                # Refresh scenarios table
                self.refresh_scenarios_table()
                
                # Now proceed with edit
                if hasattr(self, '_rice_manager_ref') and self._rice_manager_ref:
                    self._rice_manager_ref.edit_scenario(scenario_id)
                else:
                    self.scenario_manager.edit_scenario(scenario_id, self.current_profile, self.refresh_scenarios_table)
                    
            except Exception as e:
                self.show_popup("Error", f"Failed to reset scenario: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Edit", font=('Segoe UI', 10, 'bold'), bg='#f59e0b', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_edit).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
        
        confirm_popup.focus_set()
    
    def _show_scenario_actions_menu(self, button, scenario_id):
        """Show actions menu for scenario"""
        import tkinter as tk
        from tkinter import ttk
        
        # Create popup menu with left-aligned labels
        menu = tk.Menu(button, tearoff=0, font=('Segoe UI', 9))
        menu.add_command(label="✏️ Edit", command=lambda: self._edit_scenario(scenario_id))
        menu.add_command(label="📋 Duplicate", command=lambda: self._duplicate_scenario(scenario_id))
        menu.add_command(label="↻ Reset", command=lambda: self.reset_scenario(scenario_id))
        menu.add_separator()
        menu.add_command(label="🗑️ Delete", command=lambda: self.delete_scenario(scenario_id))
        
        # Show menu at button location
        try:
            x = button.winfo_rootx()
            y = button.winfo_rooty() + button.winfo_height()
            menu.post(x, y)
        except:
            pass
    
    def _duplicate_scenario(self, scenario_id):
        """Duplicate scenario with description and test steps only"""
        try:
            cursor = self.db_manager.conn.cursor()
            
            # Get original scenario details
            cursor.execute("""
                SELECT scenario_number, description, auto_login
                FROM scenarios 
                WHERE id = ? AND user_id = ?
            """, (scenario_id, self.db_manager.user_id))
            original = cursor.fetchone()
            
            if not original:
                self.show_popup("Error", "Scenario not found", "error")
                return
            
            original_number, description, auto_login = original
            
            # Get next scenario number
            next_number = self.db_manager.get_next_scenario_number(self.current_profile)
            
            # Create new scenario (without result, screenshots)
            new_description = f"{description} (Copy)"
            cursor.execute("""
                INSERT INTO scenarios (user_id, rice_profile, scenario_number, description, auto_login, result)
                VALUES (?, ?, ?, ?, ?, 'Not run')
            """, (self.db_manager.user_id, str(self.current_profile), next_number, new_description, auto_login))
            
            # Get original scenario steps with test_step_id
            cursor.execute("""
                SELECT step_order, fsm_page_id, step_name, step_type, step_target, step_description, test_step_id
                FROM scenario_steps 
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                ORDER BY step_order
            """, (self.db_manager.user_id, str(self.current_profile), original_number))
            steps = cursor.fetchall()
            
            # Copy steps to new scenario (without screenshots, set to pending)
            for step_order, fsm_page_id, step_name, step_type, step_target, step_description, test_step_id in steps:
                cursor.execute("""
                    INSERT INTO scenario_steps 
                    (user_id, rice_profile, scenario_number, step_order, fsm_page_id, 
                     step_name, step_type, step_target, step_description, test_step_id, 
                     screenshot_before, screenshot_after, screenshot_timestamp, execution_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, 'pending')
                """, (self.db_manager.user_id, str(self.current_profile), next_number, 
                      step_order, fsm_page_id, step_name, step_type, step_target, step_description, test_step_id))
            
            self.db_manager.conn.commit()
            
            # Refresh the scenarios table
            self.refresh_scenarios_table()
            
            step_count = len(steps)
            self.show_popup("Success", f"Scenario #{next_number} created with {step_count} steps!", "success")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to duplicate scenario: {str(e)}", "error")
    
    def refresh_rice_profiles_table(self):
        """Auto-refresh RICE profiles table and scenarios to show real-time updates"""
        if hasattr(self, '_ui_components_ref') and self._ui_components_ref:
            self.load_rice_profiles(self._ui_components_ref)
            # Also refresh scenarios if a profile is selected
            if self.current_profile:
                self.load_rice_scenarios(self._ui_components_ref)
