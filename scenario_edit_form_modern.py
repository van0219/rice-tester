#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import tkinter as tk
from tkinter import ttk, filedialog
from enhanced_popup_system import EnhancedPopupManager

class ModernScenarioEditForm:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.popup_manager = EnhancedPopupManager()
        
    def edit_scenario(self, scenario_id, current_profile, refresh_callback):
        """Modern Edit Scenario form with Test Users integration"""
        try:
            # Get scenario details
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT scenario_number, description, file_path, COALESCE(auto_login, 0) as auto_login 
                FROM scenarios WHERE id = ? AND user_id = ?
            """, (scenario_id, self.db_manager.user_id))
            scenario_data = cursor.fetchone()
            
            if not scenario_data:
                self.popup_manager.show_error("Error", "Scenario not found")
                return
            
            scenario_number, description, file_path, auto_login = scenario_data
            
            # Create modern dialog
            dialog = self.popup_manager.create_dynamic_dialog(
                parent=None,
                title=f"Edit Scenario #{scenario_number}",
                width=1100,
                height=750,
                resizable=True
            )
            
            # Header with modern card design
            header_frame = tk.Frame(dialog, bg='#3b82f6', height=60)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            title_label = tk.Label(header_frame, text=f"✏️ Edit Scenario #{scenario_number}", 
                                  font=('Segoe UI', 16, 'bold'), 
                                  bg='#3b82f6', fg='white')
            title_label.pack(expand=True)
            
            # Main content with responsive layout
            content_frame = tk.Frame(dialog, bg='#f8fafc', padx=20, pady=20)
            content_frame.pack(fill='both', expand=True)
            
            # Left panel - Scenario Details
            left_panel = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
            left_panel.pack(side='left', fill='y', padx=(0, 10))
            left_panel.configure(width=350)
            left_panel.pack_propagate(False)
            
            self._create_scenario_details_panel(left_panel, scenario_number, description, file_path, auto_login)
            
            # Right panel - Steps Management
            right_panel = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
            right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
            
            self._create_steps_management_panel(right_panel, scenario_id, current_profile, scenario_number)
            
            # Bottom action bar with increased height for button visibility
            action_frame = tk.Frame(content_frame, bg='#f8fafc', height=100)
            action_frame.pack(fill='x', pady=(20, 0))
            action_frame.pack_propagate(False)
            
            self._create_action_buttons(action_frame, dialog, scenario_id, current_profile, scenario_number, refresh_callback)
            
            # Initialize data
            self.current_steps_data = []
            self.login_steps_data = []
            
            # Load existing steps
            self._load_existing_steps(scenario_id, current_profile, scenario_number)
            
            # Focus on description
            self.desc_entry.focus()
            self.desc_entry.select_range(0, tk.END)
            
        except Exception as e:
            self.popup_manager.show_error("Error", f"Failed to create edit scenario form: {str(e)}")
    
    def _create_scenario_details_panel(self, parent, scenario_number, description, file_path, auto_login):
        """Create modern scenario details panel"""
        # Panel header
        header = tk.Frame(parent, bg='#3b82f6', height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="📝 Scenario Details", 
                font=('Segoe UI', 12, 'bold'), bg='#3b82f6', fg='white').pack(expand=True)
        
        # Content area
        content = tk.Frame(parent, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        # Description field
        tk.Label(content, text="Description *", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151').pack(anchor='w', pady=(0, 5))
        
        self.desc_entry = tk.Entry(content, font=('Segoe UI', 11), 
                                  relief='solid', bd=1, highlightthickness=1,
                                  highlightcolor='#3b82f6', highlightbackground='#d1d5db')
        self.desc_entry.insert(0, description or '')
        self.desc_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # File path field
        tk.Label(content, text="File Path (Optional)", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151').pack(anchor='w', pady=(0, 5))
        
        file_frame = tk.Frame(content, bg='white')
        file_frame.pack(fill='x', pady=(0, 15))
        
        self.file_entry = tk.Entry(file_frame, font=('Segoe UI', 11),
                                  relief='solid', bd=1, highlightthickness=1,
                                  highlightcolor='#3b82f6', highlightbackground='#d1d5db')
        self.file_entry.insert(0, file_path or '')
        self.file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10), ipady=8)
        
        browse_btn = tk.Button(file_frame, text="📁 Browse", 
                              font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='white',
                              relief='flat', padx=12, pady=8, cursor='hand2', bd=0,
                              command=self._browse_file)
        browse_btn.pack(side='right')
        
        # Login section with modern toggle
        login_section = tk.LabelFrame(content, text="Login Configuration", 
                                     font=('Segoe UI', 10, 'bold'), bg='white',
                                     relief='solid', bd=1, padx=15, pady=10)
        login_section.pack(fill='x', pady=(0, 15))
        
        self.include_login_var = tk.BooleanVar(value=bool(auto_login))
        login_check = tk.Checkbutton(login_section, 
                                    text="Include Login Steps", 
                                    variable=self.include_login_var,
                                    font=('Segoe UI', 10), bg='white',
                                    command=self._toggle_login_section)
        login_check.pack(anchor='w', pady=(0, 10))
        
        # Test User selection
        self.test_user_frame = tk.Frame(login_section, bg='white')
        
        tk.Label(self.test_user_frame, text="Select Test User:", 
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        
        user_select_frame = tk.Frame(self.test_user_frame, bg='white')
        user_select_frame.pack(fill='x', pady=(0, 10))
        
        self.test_user_var = tk.StringVar()
        self.test_user_combo = ttk.Combobox(user_select_frame, textvariable=self.test_user_var,
                                           font=('Segoe UI', 10), state='readonly')
        self.test_user_combo.pack(fill='x')
        
        # Load test users and set current user
        self._load_test_users()
        
        # Bind user selection change
        self.test_user_combo.bind('<<ComboboxSelected>>', self._on_user_selected)
        
        # Show/hide login section based on auto_login
        if auto_login:
            self.test_user_frame.pack(fill='x', pady=(0, 10))
        else:
            self.test_user_frame.pack_forget()
    
    def _create_steps_management_panel(self, parent, scenario_id, current_profile, scenario_number):
        """Create modern steps management panel"""
        # Panel header
        header = tk.Frame(parent, bg='#10b981', height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#10b981')
        header_content.pack(fill='both', expand=True, padx=15, pady=10)
        
        tk.Label(header_content, text="🔧 Steps Management", 
                font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='white').pack(side='left')
        
        # Management buttons in header
        btn_container = tk.Frame(header_content, bg='#10b981')
        btn_container.pack(side='right')
        
        tk.Button(btn_container, text="📋 Add Steps",
                 font=('Segoe UI', 9, 'bold'), bg='#059669', fg='white',
                 relief='flat', padx=10, pady=4, cursor='hand2', bd=0,
                 command=self._add_steps_from_groups).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_container, text="📥 Import",
                 font=('Segoe UI', 9, 'bold'), bg='#059669', fg='white',
                 relief='flat', padx=10, pady=4, cursor='hand2', bd=0,
                 command=self._show_import_dialog).pack(side='left', padx=(0, 5))
        
        # Save button
        tk.Button(btn_container, text="💾 Save",
                 font=('Segoe UI', 9, 'bold'), bg='#047857', fg='white',
                 relief='flat', padx=15, pady=4, cursor='hand2', bd=0,
                 command=lambda: self._save_changes(self.dialog, self.scenario_id, self.current_profile, self.scenario_number, self.refresh_callback)).pack(side='left')
        
        # Content area
        content = tk.Frame(parent, bg='white', padx=15, pady=15)
        content.pack(fill='both', expand=True)
        
        # Current steps display
        steps_frame = tk.LabelFrame(content, text="Current Steps", 
                                   font=('Segoe UI', 10, 'bold'), bg='white')
        steps_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        self.steps_listbox = tk.Listbox(steps_frame, font=('Segoe UI', 9), height=15)
        steps_scroll = ttk.Scrollbar(steps_frame, orient='vertical', 
                                    command=self.steps_listbox.yview)
        self.steps_listbox.configure(yscrollcommand=steps_scroll.set)
        
        self.steps_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        steps_scroll.pack(side='right', fill='y', pady=5)
        
        # Step management buttons
        mgmt_frame = tk.Frame(content, bg='white')
        mgmt_frame.pack(fill='x')
        
        tk.Button(mgmt_frame, text="📋 Add Multiple", 
                 font=('Segoe UI', 9, 'bold'), bg='#059669', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._add_steps_from_groups).pack(side='left', padx=(0, 5))
        
        tk.Button(mgmt_frame, text="✏️ Edit Value", 
                 font=('Segoe UI', 9, 'bold'), bg='#3b82f6', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._edit_step_value).pack(side='left', padx=(0, 5))
        
        tk.Button(mgmt_frame, text="❌ Remove", 
                 font=('Segoe UI', 9, 'bold'), bg='#ef4444', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._remove_selected_step).pack(side='left', padx=(0, 5))
        
        tk.Button(mgmt_frame, text="🗑️ Remove Multiple", 
                 font=('Segoe UI', 9, 'bold'), bg='#dc2626', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._remove_multiple_steps).pack(side='left', padx=(0, 5))
        
        tk.Button(mgmt_frame, text="⬆️ Up", 
                 font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._move_step_up).pack(side='left', padx=(0, 5))
        
        tk.Button(mgmt_frame, text="⬇️ Down", 
                 font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._move_step_down).pack(side='left')
        
        # Store references
        self.scenario_id = scenario_id
        self.current_profile = current_profile
        self.scenario_number = scenario_number
    
    def _create_action_buttons(self, parent, dialog, scenario_id, current_profile, scenario_number, refresh_callback):
        """Create modern action buttons"""
        # Center the button container
        btn_container = tk.Frame(parent, bg='#f8fafc')
        btn_container.pack(expand=True, pady=15)
        
        # Button frame for proper alignment
        button_frame = tk.Frame(btn_container, bg='#f8fafc')
        button_frame.pack()
        
        save_btn = tk.Button(button_frame, text="💾 Save Changes",
                            font=('Segoe UI', 11, 'bold'), bg='#10b981', fg='white',
                            relief='flat', padx=25, pady=12, cursor='hand2', bd=0,
                            highlightthickness=0,
                            command=lambda: self._save_changes(dialog, scenario_id, current_profile, scenario_number, refresh_callback))
        save_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="❌ Cancel",
                              font=('Segoe UI', 11, 'bold'), bg='#6b7280', fg='white',
                              relief='flat', padx=25, pady=12, cursor='hand2', bd=0,
                              highlightthickness=0, command=dialog.destroy)
        cancel_btn.pack(side='left')
        
        # Store references
        self.dialog = dialog
        self.refresh_callback = refresh_callback
    
    def _browse_file(self):
        """Browse for file"""
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("All Files", "*.*")]
        )
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
    
    def _toggle_login_section(self):
        """Toggle login section visibility"""
        if self.include_login_var.get():
            self.test_user_frame.pack(fill='x', pady=(0, 10))
        else:
            self.test_user_frame.pack_forget()
        
        self._update_steps_display()
    
    def _load_test_users(self):
        """Load test users and detect current user from existing login steps"""
        try:
            users = self.db_manager.get_test_users()
            user_options = [f"{user[1]} ({user[2]})" for user in users]  # name (email)
            self.test_user_combo['values'] = user_options
            
            # Try to detect current user from existing login steps
            if self.include_login_var.get():
                current_username = self._detect_current_test_user()
                if current_username:
                    for i, user in enumerate(users):
                        if user[2] == current_username:  # email match
                            self.test_user_combo.current(i)
                            break
                elif user_options:
                    self.test_user_combo.current(0)
            elif user_options:
                self.test_user_combo.current(0)
                
        except Exception as e:
            print(f"Error loading test users: {e}")
    
    def _detect_current_test_user(self):
        """Detect current test user from existing login steps"""
        try:
            # Use stored references if available
            current_profile = getattr(self, 'current_profile', None)
            scenario_number = getattr(self, 'scenario_number', None)
            
            if not current_profile or not scenario_number:
                return None
            
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT step_description FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = ?
                AND (LOWER(COALESCE(ts.name, ss.step_name)) LIKE '%username%' 
                     OR LOWER(COALESCE(ts.name, ss.step_name)) LIKE '%email%')
                AND COALESCE(ts.step_type, ss.step_type) = 'Text Input'
                ORDER BY ss.step_order LIMIT 1
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            
            result = cursor.fetchone()
            return result[0] if result else None
            
        except Exception as e:
            print(f"Error detecting current test user: {e}")
            return None
    

    
    def _load_existing_steps(self, scenario_id, current_profile, scenario_number):
        """Load existing scenario steps"""
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("""
                SELECT ss.step_order, 
                       COALESCE(ts.name, ss.step_name) as step_name,
                       COALESCE(ts.step_type, ss.step_type) as step_type, 
                       COALESCE(ts.target, ss.step_target) as step_target,
                       ss.step_description,
                       ss.test_step_id
                FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = ?
                ORDER BY ss.step_order
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            
            existing_steps = cursor.fetchall()
            
            # Separate login steps from regular steps
            self._separate_login_and_regular_steps(existing_steps)
            
            # Update display
            self._update_steps_display()
            
        except Exception as e:
            print(f"Error loading existing steps: {e}")
    
    def _separate_login_and_regular_steps(self, existing_steps):
        """Separate login steps from regular steps"""
        self.current_steps_data.clear()
        
        # Get Login group ID for detection
        try:
            groups = self.db_manager.get_test_step_groups()
            login_group_id = None
            for group in groups:
                if group[1].lower() == 'login':
                    login_group_id = group[0]
                    break
            
            if login_group_id and self.include_login_var.get():
                login_step_ids = {step[0] for step in self.db_manager.get_test_steps_by_group(login_group_id)}
                
                # Find where login steps end
                login_end_index = 0
                for i, step in enumerate(existing_steps):
                    test_step_id = step[5]  # test_step_id from scenario_steps
                    if test_step_id not in login_step_ids:
                        login_end_index = i
                        break
                else:
                    login_end_index = len(existing_steps)
                
                regular_steps_raw = existing_steps[login_end_index:]
            else:
                regular_steps_raw = existing_steps
            
            # Load regular steps
            for step in regular_steps_raw:
                step_order, step_name, step_type, step_target, step_description, test_step_id = step
                self.current_steps_data.append({
                    'order': step_order,
                    'name': step_name,
                    'type': step_type,
                    'target': step_target,
                    'description': step_description,
                    'step_id': test_step_id
                })
                
        except Exception as e:
            print(f"Error separating steps: {e}")
            # Fallback: treat all as regular steps
            for step in existing_steps:
                step_order, step_name, step_type, step_target, step_description, test_step_id = step
                self.current_steps_data.append({
                    'order': step_order,
                    'name': step_name,
                    'type': step_type,
                    'target': step_target,
                    'description': step_description,
                    'step_id': test_step_id
                })
    
    def _update_steps_display(self):
        """Update steps display"""
        self.steps_listbox.delete(0, tk.END)
        
        # Update login steps data
        self.login_steps_data.clear()
        if self.include_login_var.get():
            self.login_steps_data = self._get_login_steps()
        
        step_counter = 1
        
        # Add login steps
        for login_step in self.login_steps_data:
            display_text = f"{step_counter}. {login_step['name']} ({login_step['type']}) [LOGIN]"
            if login_step['type'] == 'Text Input' and login_step['description']:
                is_password = 'password' in login_step['name'].lower()
                if is_password:
                    display_text += f" - Value: {'•' * len(login_step['description'])}"
                else:
                    display_text += f" - Value: '{login_step['description']}'"
            self.steps_listbox.insert(tk.END, display_text)
            step_counter += 1
        
        # Add regular steps
        for step in self.current_steps_data:
            display_text = f"{step_counter}. {step['name']} ({step['type']})"
            if step['type'] == 'Text Input' and step.get('description'):
                is_password = 'password' in step['name'].lower()
                if is_password:
                    display_text += f" - Value: {'•' * len(step['description'])}"
                else:
                    display_text += f" - Value: '{step['description']}'"
            elif step['type'] == 'Wait':
                scenario_value = step.get('description', '3')
                target = step.get('target', '')
                if target and ('Element Visible:' in target or 'Element Clickable:' in target):
                    display_text += f" - Selector: {scenario_value}"
                else:
                    display_text += f" - Value: {scenario_value}s"
            self.steps_listbox.insert(tk.END, display_text)
            step_counter += 1
    
    def _get_login_steps(self):
        """Get login steps from Test Users and Login group"""
        if not self.test_user_var.get():
            return []
        
        try:
            # Get selected test user
            users = self.db_manager.get_test_users()
            user_index = self.test_user_combo.current()
            
            if user_index < 0 or user_index >= len(users):
                return []
            
            user_data = users[user_index]
            username = user_data[2]  # email
            password = self.db_manager.decrypt_password(user_data[3])  # decrypted password
            
            # Find Login test group
            groups = self.db_manager.get_test_step_groups()
            login_group_id = None
            for group in groups:
                if group[1].lower() == 'login':
                    login_group_id = group[0]
                    break
            
            if not login_group_id:
                # Fallback to hardcoded steps
                return [
                    {'name': 'Navigate to Login Page', 'type': 'Navigate', 
                     'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                    {'name': 'Enter Username', 'type': 'Text Input', 
                     'target': 'input[name="username"]', 'description': username},
                    {'name': 'Enter Password', 'type': 'Text Input', 
                     'target': 'input[name="password"]', 'description': password},
                    {'name': 'Click Login', 'type': 'Element Click', 
                     'target': 'span:contains("Login")', 'description': 'Click login button'}
                ]
            
            # Get steps from Login group and populate with user credentials
            login_steps = self.db_manager.get_test_steps_by_group(login_group_id)
            result = []
            
            for step in login_steps:
                step_id, name, step_type, target, description = step
                
                if step_type == 'Text Input':
                    if 'username' in name.lower():
                        description = username
                    elif 'password' in name.lower():
                        description = password
                
                result.append({
                    'step_id': step_id,
                    'name': name,
                    'type': step_type,
                    'target': target,
                    'description': description or ''
                })
            
            return result
            
        except Exception as e:
            print(f"Error getting login steps: {e}")
            return []
    
    def _add_steps_from_groups(self):
        """Add steps from test groups"""
        try:
            # Create step selection dialog
            step_dialog = self.popup_manager.create_dynamic_dialog(
                parent=self.dialog,
                title="Add Steps from Test Groups",
                width=800,
                height=600,
                resizable=True
            )
            
            # Header
            header = tk.Frame(step_dialog, bg='#10b981', height=50)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(header, text="📋 Add Steps from Test Groups", 
                    font=('Segoe UI', 14, 'bold'), bg='#10b981', fg='white').pack(expand=True)
            
            # Content
            content = tk.Frame(step_dialog, bg='white', padx=20, pady=20)
            content.pack(fill='both', expand=True)
            
            # Group selection
            tk.Label(content, text="Select Test Group:", 
                    font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
            
            group_var = tk.StringVar()
            group_combo = ttk.Combobox(content, textvariable=group_var,
                                      font=('Segoe UI', 10), state='readonly')
            group_combo.pack(fill='x', pady=(0, 15))
            
            # Available steps
            tk.Label(content, text="Available Steps:", 
                    font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 2))
            
            tk.Label(content, text="💡 Tip: Hold Ctrl+Click for multiple selection, Shift+Click for range selection", 
                    font=('Segoe UI', 8), bg='white', fg='#6b7280').pack(anchor='w', pady=(0, 5))
            
            listbox_frame = tk.Frame(content, bg='white')
            listbox_frame.pack(fill='both', expand=True, pady=(0, 20))
            
            steps_tree = ttk.Treeview(listbox_frame, columns=('type',), show='tree headings', height=12, selectmode='extended')
            steps_tree.heading('#0', text='Step Name')
            steps_tree.heading('type', text='Type')
            steps_tree.column('#0', width=300)
            steps_tree.column('type', width=150)
            
            steps_scroll = ttk.Scrollbar(listbox_frame, orient='vertical', command=steps_tree.yview)
            steps_tree.configure(yscrollcommand=steps_scroll.set)
            
            steps_tree.pack(side='left', fill='both', expand=True, in_=listbox_frame)
            steps_scroll.pack(side='right', fill='y', in_=listbox_frame)
            
            # Load groups (excluding Login group)
            all_groups = self.db_manager.get_test_step_groups()
            groups = [group for group in all_groups if group[1].lower() != 'login']
            if groups:
                group_options = [f"{group[1]} ({group[3]} steps)" for group in groups]
                group_combo['values'] = group_options
                if group_options:
                    group_combo.current(0)  # Select first group by default
            else:
                group_combo['values'] = ["No test groups available"]
                steps_tree.insert('', 'end', text="No test step groups found. Create groups in Test Step Groups section first.", values=("",))
            
            def load_group_steps(event=None):
                if not groups:
                    for item in steps_tree.get_children():
                        steps_tree.delete(item)
                    steps_tree.insert('', 'end', text="No test groups available", values=("",))
                    return
                try:
                    group_index = group_combo.current()
                    if 0 <= group_index < len(groups):
                        group_id = groups[group_index][0]
                        steps = self.db_manager.get_test_steps_by_group(group_id)
                        for item in steps_tree.get_children():
                            steps_tree.delete(item)
                        if steps:
                            for i, step in enumerate(steps):
                                steps_tree.insert('', 'end', iid=str(i), text=step[1], values=(step[2],))
                        else:
                            steps_tree.insert('', 'end', text="No steps found in this group", values=("",))
                    else:
                        for item in steps_tree.get_children():
                            steps_tree.delete(item)
                        steps_tree.insert('', 'end', text="Invalid group selection", values=("",))
                except Exception as e:
                    print(f"Error loading group steps: {e}")
                    for item in steps_tree.get_children():
                        steps_tree.delete(item)
                    steps_tree.insert('', 'end', text=f"Error loading steps: {str(e)}", values=("",))
            
            group_combo.bind('<<ComboboxSelected>>', load_group_steps)
            
            # Load initial steps with delay to ensure widgets are ready
            if groups:
                step_dialog.after_idle(load_group_steps)
            
            # Store references for the add function
            step_dialog.groups = groups
            step_dialog.steps_tree = steps_tree
            step_dialog.group_combo = group_combo
            
            # Buttons
            btn_frame = tk.Frame(content, bg='white')
            btn_frame.pack(fill='x')
            
            def add_selected_steps():
                selection = steps_tree.selection()
                if not selection or not group_var.get() or not groups:
                    self.popup_manager.show_error("Error", "Please select steps to add", parent=step_dialog)
                    return
                
                try:
                    group_index = group_combo.current()
                    if group_index < 0 or group_index >= len(groups):
                        self.popup_manager.show_error("Error", "Invalid group selection", parent=step_dialog)
                        return
                    
                    group_id = groups[group_index][0]
                    steps = self.db_manager.get_test_steps_by_group(group_id)
                    
                    if not steps:
                        self.popup_manager.show_error("Error", "No steps found in selected group", parent=step_dialog)
                        return
                    
                    added_count = 0
                    for item_id in selection:
                        try:
                            index = int(item_id)
                            if index < len(steps):
                                step_data = steps[index]
                                step_id, name, step_type, target, description = step_data
                                
                                self.current_steps_data.append({
                                    'order': len(self.current_steps_data) + 1,
                                    'name': name,
                                    'type': step_type,
                                    'target': target,
                                    'description': description or '',
                                    'step_id': step_id
                                })
                                added_count += 1
                        except (ValueError, IndexError):
                            continue
                    
                    self._update_steps_display()
                    step_dialog.destroy()
                    
                    if added_count > 0:
                        self.popup_manager.show_success("Success", f"Added {added_count} steps to scenario")
                    else:
                        self.popup_manager.show_error("Error", "No steps were added")
                        
                except Exception as e:
                    self.popup_manager.show_error("Error", f"Failed to add steps: {str(e)}", parent=step_dialog)
            
            tk.Button(btn_frame, text="Cancel", 
                     font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='white',
                     relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                     command=step_dialog.destroy).pack(side='right', padx=(10, 0))
            
            tk.Button(btn_frame, text="Add Selected Steps", 
                     font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='white',
                     relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                     command=add_selected_steps).pack(side='right')
            
        except Exception as e:
            self.popup_manager.show_error("Error", f"Failed to open add steps dialog: {str(e)}", parent=self.dialog)
    
    def _show_import_dialog(self):
        """Show GitHub Test Groups import dialog"""
        try:
            from github_test_groups_importer import GitHubTestGroupsImporter
            importer = GitHubTestGroupsImporter(self.db_manager, self.show_popup)
            importer.show_import_browser(parent_dialog=self.dialog)
        except ImportError:
            self.popup_manager.show_info("Import Test Groups", 
                "📥 GitHub Test Groups Import\n\nBrowse and import community test groups from GitHub repository.",
                parent=self.dialog)
        except Exception as e:
            self.popup_manager.show_error("Error", f"Failed to open import dialog: {str(e)}", parent=self.dialog)
    
    def _on_user_selected(self, event=None):
        """Handle test user selection change"""
        self._update_steps_display()
    
    def _on_groups_imported(self):
        """Callback when test groups are imported"""
        self.popup_manager.show_success("Success", "Test groups imported successfully!")
    

    
    def _edit_step_value(self):
        """Edit step value for Text Input steps (excluding login steps)"""
        selection = self.steps_listbox.curselection()
        if not selection:
            self.popup_manager.show_error("Error", "Please select a step to edit", parent=self.dialog)
            return
        
        index = selection[0]
        login_step_count = len(self.login_steps_data)
        
        # Check if it's a login step
        if index < login_step_count:
            self.popup_manager.show_info("Info", "Login step values are managed through the Test User dropdown", parent=self.dialog)
            return
        
        # Get the actual step
        actual_index = index - login_step_count
        if actual_index >= len(self.current_steps_data):
            return
        
        step = self.current_steps_data[actual_index]
        
        # Check if it's a Text Input step
        if step['type'] != 'Text Input':
            self.popup_manager.show_info("Info", "Only Text Input steps can have their values edited", parent=self.dialog)
            return
        
        # Create edit dialog
        edit_dialog = self.popup_manager.create_dynamic_dialog(
            parent=self.dialog,
            title=f"Edit Value: {step['name']}",
            width=400,
            height=250
        )
        
        # Header
        header = tk.Frame(edit_dialog, bg='#3b82f6', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="✏️ Edit Step Value", 
                font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='white').pack(expand=True)
        
        # Content
        content = tk.Frame(edit_dialog, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        tk.Label(content, text=f"Step: {step['name']}", 
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
        
        tk.Label(content, text="Value:", 
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        
        value_entry = tk.Entry(content, font=('Segoe UI', 11), width=40)
        value_entry.insert(0, step.get('description', ''))
        value_entry.pack(fill='x', pady=(0, 20))
        value_entry.focus()
        value_entry.select_range(0, tk.END)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        def save_value():
            new_value = value_entry.get().strip()
            step['description'] = new_value
            self._update_steps_display()
            edit_dialog.destroy()
            self.popup_manager.show_success("Success", "Step value updated successfully")
        
        tk.Button(btn_frame, text="Save", 
                 font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='white',
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                 command=save_value).pack(side='right', padx=(10, 0))
        
        tk.Button(btn_frame, text="Cancel", 
                 font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='white',
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                 command=edit_dialog.destroy).pack(side='right')
    
    def _remove_selected_step(self):
        """Remove selected step"""
        selection = self.steps_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        login_step_count = len(self.login_steps_data)
        
        if index < login_step_count:
            self.popup_manager.show_info("Info", 
                "Login steps can only be removed by unchecking 'Include Login Steps'",
                parent=self.dialog)
            return
        
        actual_index = index - login_step_count
        if actual_index < len(self.current_steps_data):
            self.current_steps_data.pop(actual_index)
            self._update_steps_display()
    
    def _remove_multiple_steps(self):
        """Remove multiple selected steps"""
        # Create multi-selection dialog
        remove_dialog = self.popup_manager.create_dynamic_dialog(
            parent=self.dialog,
            title="Remove Multiple Steps",
            width=600,
            height=400
        )
        
        # Header
        header = tk.Frame(remove_dialog, bg='#ef4444', height=50)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🗑️ Remove Multiple Steps", 
                font=('Segoe UI', 14, 'bold'), bg='#ef4444', fg='white').pack(expand=True)
        
        # Content
        content = tk.Frame(remove_dialog, bg='white', padx=20, pady=20)
        content.pack(fill='both', expand=True)
        
        tk.Label(content, text="Select steps to remove:", 
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
        
        # Steps listbox with checkboxes simulation
        steps_frame = tk.Frame(content, bg='white')
        steps_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        steps_listbox = tk.Listbox(steps_frame, font=('Segoe UI', 9), selectmode=tk.MULTIPLE, height=12)
        steps_scroll = ttk.Scrollbar(steps_frame, orient='vertical', command=steps_listbox.yview)
        steps_listbox.configure(yscrollcommand=steps_scroll.set)
        
        steps_listbox.pack(side='left', fill='both', expand=True)
        steps_scroll.pack(side='right', fill='y')
        
        # Populate with non-login steps only
        login_count = len(self.login_steps_data)
        for i, step in enumerate(self.current_steps_data):
            display_text = f"{i + login_count + 1}. {step['name']} ({step['type']})"
            steps_listbox.insert(tk.END, display_text)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x')
        
        def remove_selected():
            selection = steps_listbox.curselection()
            if not selection:
                self.popup_manager.show_error("Error", "Please select steps to remove", parent=remove_dialog)
                return
            
            # Remove in reverse order to maintain indices
            for index in reversed(selection):
                if index < len(self.current_steps_data):
                    self.current_steps_data.pop(index)
            
            self._update_steps_display()
            remove_dialog.destroy()
            self.popup_manager.show_success("Success", f"Removed {len(selection)} steps")
        
        tk.Button(btn_frame, text="Cancel", 
                 font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='white',
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                 command=remove_dialog.destroy).pack(side='right', padx=(10, 0))
        
        tk.Button(btn_frame, text="Remove Selected", 
                 font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='white',
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                 command=remove_selected).pack(side='right')
    
    def _move_step_up(self):
        """Move step up"""
        selection = self.steps_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        index = selection[0]
        login_step_count = len(self.login_steps_data)
        
        if index <= login_step_count:
            self.popup_manager.show_info("Info", 
                "Cannot move login steps or move steps above login steps",
                parent=self.dialog)
            return
        
        actual_index = index - login_step_count
        if actual_index > 0:
            self.current_steps_data[actual_index], self.current_steps_data[actual_index-1] = \
                self.current_steps_data[actual_index-1], self.current_steps_data[actual_index]
            self._update_steps_display()
            self.steps_listbox.selection_set(index-1)
    
    def _move_step_down(self):
        """Move step down"""
        selection = self.steps_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        login_step_count = len(self.login_steps_data)
        
        if index < login_step_count:
            self.popup_manager.show_info("Info", "Cannot move login steps", parent=self.dialog)
            return
        
        actual_index = index - login_step_count
        if actual_index < len(self.current_steps_data) - 1:
            self.current_steps_data[actual_index], self.current_steps_data[actual_index+1] = \
                self.current_steps_data[actual_index+1], self.current_steps_data[actual_index]
            self._update_steps_display()
            self.steps_listbox.selection_set(index+1)
    
    def _save_changes(self, dialog, scenario_id, current_profile, scenario_number, refresh_callback):
        """Save scenario changes"""
        description = self.desc_entry.get().strip()
        file_path = self.file_entry.get().strip() or None
        include_login = self.include_login_var.get()
        
        if not description:
            self.popup_manager.show_error("Validation Error", "Please enter a scenario description", parent=self.dialog)
            return
        
        if include_login and not self.test_user_var.get():
            self.popup_manager.show_error("Validation Error", "Please select a test user for login steps", parent=self.dialog)
            return
        
        try:
            cursor = self.db_manager.conn.cursor()
            
            # Update scenario details
            cursor.execute("""
                UPDATE scenarios SET description = ?, file_path = ?, auto_login = ? 
                WHERE id = ? AND user_id = ?
            """, (description, file_path, include_login, scenario_id, self.db_manager.user_id))
            
            # Delete existing steps
            cursor.execute("""
                DELETE FROM scenario_steps 
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
            """, (self.db_manager.user_id, str(current_profile), scenario_number))
            
            # Add login steps if requested
            step_order = 1
            if include_login:
                login_steps = self._get_login_steps()
                for login_step in login_steps:
                    if 'step_id' in login_step:
                        cursor.execute("""
                            INSERT INTO scenario_steps 
                            (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                              step_order, login_step['step_id'], login_step['description'], 1))
                    else:
                        cursor.execute("""
                            INSERT INTO scenario_steps 
                            (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (self.db_manager.user_id, str(current_profile), scenario_number, step_order,
                              login_step['name'], login_step['type'], login_step['target'], login_step['description'], 1))
                    step_order += 1
            
            # Add regular steps
            for step in self.current_steps_data:
                if step.get('step_id'):
                    cursor.execute("""
                        INSERT INTO scenario_steps 
                        (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                          step_order, step['step_id'], step['description'], 1))
                else:
                    cursor.execute("""
                        INSERT INTO scenario_steps 
                        (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (self.db_manager.user_id, str(current_profile), scenario_number, step_order,
                          step['name'], step['type'], step['target'], step['description'], 1))
                step_order += 1
            
            self.db_manager.conn.commit()
            
            # Success
            total_steps = len(self.current_steps_data) + len(self.login_steps_data)
            dialog.destroy()
            
            if refresh_callback:
                refresh_callback()
            
            self.popup_manager.show_success("Success", 
                f"Scenario #{scenario_number} updated successfully with {total_steps} steps!")
            
        except Exception as e:
            self.popup_manager.show_error("Error", f"Failed to update scenario: {str(e)}", parent=self.dialog)

def main():
    """Test the modern edit scenario form"""
    root = tk.Tk()
    root.withdraw()
    
    # Mock database manager for testing
    class MockDB:
        user_id = 1
        conn = None
        def get_test_users(self):
            return [(1, "Test User", "test@example.com", "encrypted_pass")]
        def get_test_step_groups(self):
            return [(1, "Login", "Login steps", 4), (2, "Navigation", "Nav steps", 3)]
        def get_test_steps_by_group(self, group_id):
            return [(1, "Navigate", "Navigate", "url", ""), (2, "Click", "Element Click", "button", "")]
        def decrypt_password(self, encrypted):
            return "decrypted_password"
    
    def mock_popup(title, message, type):
        print(f"{type}: {title} - {message}")
    
    form = ModernScenarioEditForm(MockDB(), mock_popup)
    # Mock scenario data would be loaded here
    
    root.mainloop()

if __name__ == "__main__":
    main()