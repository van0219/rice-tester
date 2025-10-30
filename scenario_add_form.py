#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from rice_dialogs import center_dialog

class ScenarioAddForm:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def add_scenario(self, current_profile, refresh_callback):
        """Add new scenario with test step selection from groups"""
        try:
            # Get next scenario number
            next_number = self.db_manager.get_next_scenario_number(current_profile)
            
            # Create add scenario dialog
            from enhanced_popup_system import create_enhanced_dialog
            popup = create_enhanced_dialog(None, "Add Scenario", 900, 700, modal=False)
            popup.configure(bg='#ffffff')
            
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
            
            # Step management
            selected_steps = []
            login_steps_data = []
            
            def get_login_steps():
                """Get steps from Login test group dynamically"""
                username = username_entry.get().strip() if username_entry.get() else "[username]"
                password = password_entry.get().strip() if password_entry.get() else "[password]"
                
                # Find Login test group
                groups = self.db_manager.get_test_step_groups()
                login_group_id = None
                for group in groups:
                    if group[1].lower() == 'login':
                        login_group_id = group[0]
                        break
                
                if not login_group_id:
                    # Fallback to hardcoded if no Login group exists
                    return [
                        {'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                        {'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': username},
                        {'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': password},
                        {'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                    ]
                
                # Get steps from Login group
                login_steps = self.db_manager.get_test_steps_by_group(login_group_id)
                result = []
                
                for step in login_steps:
                    step_id, name, step_type, target, description = step
                    # Replace credentials for Text Input steps
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
            
            def update_login_steps_display():
                """Update the display to show/hide login steps"""
                selected_listbox.delete(0, tk.END)
                
                if include_login_var.get():
                    login_steps_data.clear()
                    login_steps_data.extend(get_login_steps())
                else:
                    login_steps_data.clear()
                
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
                    elif step['type'] == 'Wait':
                        # Show appropriate value based on wait type
                        target = step.get('target', '')
                        value = step.get('description', '3')
                        if target and ('Element Visible:' in target or 'Element Clickable:' in target):
                            display_text += f" - Selector: {value}"
                        else:
                            display_text += f" - Value: {value}s"
                    selected_listbox.insert(tk.END, display_text)
                    step_counter += 1
            
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
            
            def on_credential_change(*args):
                if include_login_var.get():
                    update_login_steps_display()
            
            username_entry.bind('<KeyRelease>', on_credential_change)
            password_entry.bind('<KeyRelease>', on_credential_change)
            
            def load_group_steps():
                if not group_var.get():
                    return
                
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
                        
                        # For Wait steps, extract value from target field based on wait type
                        if step_type == 'Wait':
                            if target:
                                if target.startswith('Element Visible:'):
                                    description = target.replace('Element Visible:', '').strip()
                                elif target.startswith('Element Clickable:'):
                                    description = target.replace('Element Clickable:', '').strip()
                                elif target.startswith('Page Load:'):
                                    description = target.replace('Page Load:', '').strip()
                                elif target.startswith('Time (seconds):'):
                                    description = target.replace('Time (seconds):', '').strip()
                                elif ':' in target:
                                    # Generic format "Type: Value"
                                    description = target.split(':', 1)[1].strip()
                                else:
                                    # Just a value (time-based)
                                    description = target
                            else:
                                # Use existing description from test step or fallback
                                description = description or '3'
                        
                        selected_steps.append({
                            'step_id': step_id,
                            'name': name,
                            'type': step_type,
                            'target': target,
                            'description': description or ''
                        })
                
                update_login_steps_display()
            
            group_combo.bind('<<ComboboxSelected>>', lambda e: load_group_steps())
            
            # Step management buttons
            step_btn_frame = tk.Frame(right_frame, bg='#ffffff')
            step_btn_frame.pack(fill="x", pady=(10, 0))
            
            def remove_selected_step():
                selection = selected_listbox.curselection()
                if selection:
                    index = selection[0]
                    login_step_count = len(login_steps_data)
                    
                    if index < login_step_count:
                        self.show_popup("Info", "Login steps can only be removed by unchecking 'Include Login'", "warning")
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
                        self.show_popup("Info", "Cannot move login steps or move steps above login steps", "warning")
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
                    
                    # Can't move login steps
                    if index < login_step_count:
                        self.show_popup("Info", "Cannot move login steps", "warning")
                        return
                    
                    # Move within selected steps only
                    actual_index = index - login_step_count
                    if actual_index < len(selected_steps) - 1:
                        selected_steps[actual_index], selected_steps[actual_index+1] = selected_steps[actual_index+1], selected_steps[actual_index]
                        update_login_steps_display()
                        selected_listbox.selection_set(index+1)
            
            def edit_selected_value():
                selection = selected_listbox.curselection()
                if not selection:
                    self.show_popup("Error", "Please select a step to edit", "error")
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
                
                # Check if step can be edited
                if step_data['type'] == 'Text Input':
                    can_edit = True
                    edit_type = 'text'
                elif step_data['type'] == 'Wait':
                    can_edit = True
                    edit_type = 'wait_time'
                else:
                    can_edit = False
                
                if not can_edit:
                    self.show_popup("Info", "Only Text Input steps and Wait steps can have their values edited", "warning")
                    return
                
                # Create edit dialog
                from enhanced_popup_system import create_enhanced_dialog
                edit_popup = create_enhanced_dialog(popup, "Edit Input Value", 400, 250, modal=False)
                edit_popup.configure(bg='#ffffff')
                edit_popup.attributes('-topmost', False)
                edit_popup.resizable(False, False)
                
                try:
                    edit_popup.iconbitmap("infor_logo.ico")
                except:
                    pass
                
                edit_frame = tk.Frame(edit_popup, bg='#ffffff', padx=20, pady=20)
                edit_frame.pack(fill="both", expand=True)
                
                tk.Label(edit_frame, text=f"Edit Value for: {step_data['name']}", 
                        font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(pady=(0, 15))
                
                # Different labels and inputs based on step type
                if edit_type == 'text':
                    tk.Label(edit_frame, text="Input Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    
                    is_password = 'password' in step_data['name'].lower()
                    value_entry = tk.Entry(edit_frame, width=40, font=('Segoe UI', 10), 
                                          show="•" if is_password else "")
                    value_entry.insert(0, step_data.get('description', ''))
                    value_entry.pack(fill="x", pady=(0, 20))
                elif edit_type == 'wait_time':
                    tk.Label(edit_frame, text="Wait Time (seconds):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    
                    value_entry = tk.Entry(edit_frame, width=40, font=('Segoe UI', 10))
                    # Use description field for wait time value
                    current_value = step_data.get('description', '3')
                    
                    value_entry.insert(0, current_value)
                    value_entry.pack(fill="x", pady=(0, 20))
                
                edit_btn_frame = tk.Frame(edit_frame, bg='#ffffff')
                edit_btn_frame.pack()
                
                def save_value():
                    new_value = value_entry.get().strip()
                    
                    # Validate wait time if it's a wait step
                    if edit_type == 'wait_time':
                        try:
                            wait_seconds = float(new_value)
                            if wait_seconds <= 0:
                                self.show_popup("Error", "Wait time must be greater than 0 seconds", "error")
                                return
                        except ValueError:
                            self.show_popup("Error", "Please enter a valid number for wait time", "error")
                            return
                    
                    # Store the value in description field for consistency
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
            tk.Button(step_btn_frame, text="⬆️ Up", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_up).pack(side="left", padx=(0, 5))
            tk.Button(step_btn_frame, text="⬇️ Down", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_down).pack(side="left")
            
            # Bottom buttons
            btn_frame = tk.Frame(main_frame, bg='#ffffff')
            btn_frame.pack(fill="x", pady=(20, 0))
            
            def save_scenario():
                # CRITICAL FIX: Capture all widget values BEFORE any database operations
                description = desc_entry.get().strip()
                file_path = file_entry.get().strip() or None
                include_login = include_login_var.get()
                
                if not description:
                    self.show_popup("Error", "Please enter a description", "error")
                    return
                
                # CRITICAL FIX: Capture all widget values BEFORE any database operations
                username = username_entry.get().strip() if include_login else ""
                password = password_entry.get().strip() if include_login else ""
                
                try:
                    # Save scenario
                    scenario_id = self.db_manager.save_scenario(
                        current_profile, next_number, description, file_path, include_login
                    )
                    
                    # Save selected steps
                    step_order = 1
                    login_step_count = 0
                    
                    # Add login steps if requested
                    if include_login and username and password:
                        # Get login steps with captured credentials
                        login_steps = []
                        
                        # Find Login test group
                        groups = self.db_manager.get_test_step_groups()
                        login_group_id = None
                        for group in groups:
                            if group[1].lower() == 'login':
                                login_group_id = group[0]
                                break
                        
                        if login_group_id:
                            # Get steps from Login group
                            login_steps_raw = self.db_manager.get_test_steps_by_group(login_group_id)
                            
                            for step in login_steps_raw:
                                step_id, name, step_type, target, description = step
                                # Replace credentials for Text Input steps
                                if step_type == 'Text Input':
                                    if 'username' in name.lower():
                                        description = username
                                    elif 'password' in name.lower():
                                        description = password
                                
                                login_steps.append({
                                    'step_id': step_id,
                                    'name': name,
                                    'type': step_type,
                                    'target': target,
                                    'description': description or ''
                                })
                        else:
                            # Fallback to hardcoded if no Login group exists
                            login_steps = [
                                {'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                                {'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': username},
                                {'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': password},
                                {'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                            ]
                        
                        login_step_count = len(login_steps)
                        
                        for login_step in login_steps:
                            cursor = self.db_manager.conn.cursor()
                            # For login steps, store as reference if they come from test_steps, otherwise store directly
                            if 'step_id' in login_step:
                                cursor.execute("""
                                    INSERT INTO scenario_steps 
                                    (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                                    VALUES (?, ?, ?, ?, ?, ?, ?)
                                """, (self.db_manager.user_id, str(current_profile), next_number, step_order, 
                                      login_step['step_id'], login_step['description'], 1))
                            else:
                                # Fallback for hardcoded login steps
                                cursor.execute("""
                                    INSERT INTO scenario_steps 
                                    (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, (self.db_manager.user_id, str(current_profile), next_number, step_order, 
                                      login_step['name'], login_step['type'], login_step['target'], login_step['description'], 1))
                            step_order += 1
                    
                    # Add selected test steps with references
                    for step in selected_steps:
                        cursor = self.db_manager.conn.cursor()
                        cursor.execute("""
                            INSERT INTO scenario_steps 
                            (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (self.db_manager.user_id, str(current_profile), next_number, step_order, 
                              step['step_id'], step['description'], 1))
                        step_order += 1
                    
                    self.db_manager.conn.commit()
                    
                    # Calculate total steps for success message
                    total_steps = len(selected_steps) + login_step_count
                    
                    # Close popup AFTER all operations are complete
                    popup.destroy()
                    
                    # Refresh and show success
                    if refresh_callback:
                        refresh_callback()
                    
                    self.show_popup("Success", f"Scenario #{next_number} created with {total_steps} steps!", "success")
                    
                except Exception as e:
                    self.show_popup("Error", f"Failed to create scenario: {str(e)}", "error")
            
            tk.Button(btn_frame, text="💾 Save Scenario", font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=save_scenario).pack(side="left", padx=(0, 10))
            tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 12, 'bold'), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
            
            desc_entry.focus()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to add scenario: {str(e)}", "error")
