#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from rice_dialogs import center_dialog
from scenario_edit_value import ScenarioEditValue

class ScenarioEditForm:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
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
            
            # Create edit dialog with initial size based on auto_login
            from Temp.enhanced_popup_system import create_enhanced_dialog
            
            # Set initial size based on auto_login status
            if auto_login:
                popup = create_enhanced_dialog(None, f"Edit Scenario #{scenario_number}", 900, 772, modal=False)
            else:
                popup = create_enhanced_dialog(None, f"Edit Scenario #{scenario_number}", 900, 700, modal=False)
            
            popup.configure(bg='#ffffff')
            
            try:
                popup.iconbitmap("infor_logo.ico")
            except:
                pass
            
            main_frame = tk.Frame(popup, bg='#ffffff')
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Header
            tk.Label(main_frame, text=f"Edit Scenario #{scenario_number}", 
                    font=('Segoe UI', 16, 'bold'), bg='#ffffff').pack(pady=(0, 20))
            
            # Left column - Scenario details
            left_frame = tk.Frame(main_frame, bg='#ffffff')
            left_frame.pack(fill="x", pady=(0, 20))
            
            tk.Label(left_frame, text="Scenario Details", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
            
            # Description
            tk.Label(left_frame, text="Description:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            desc_entry = tk.Entry(left_frame, width=40, font=('Segoe UI', 10))
            desc_entry.insert(0, description or '')
            desc_entry.pack(fill="x", pady=(0, 10))
            
            # File path (optional)
            tk.Label(left_frame, text="File Path (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            file_frame = tk.Frame(left_frame, bg='#ffffff')
            file_frame.pack(fill="x", pady=(0, 10))
            
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
            
            # Get existing steps with dynamic data
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
            
            # Steps management section
            steps_frame = tk.LabelFrame(main_frame, text="Test Steps Management", font=('Segoe UI', 12, 'bold'), bg='#ffffff')
            steps_frame.pack(fill="both", expand=True, pady=(0, 20))
            
            # Current steps display
            current_steps_frame = tk.LabelFrame(steps_frame, text=f"Current Steps ({len(existing_steps)})", font=('Segoe UI', 10, 'bold'), bg='#ffffff')
            current_steps_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create scrollable listbox for current steps
            steps_listbox = tk.Listbox(current_steps_frame, font=('Segoe UI', 9), height=10)
            steps_scrollbar = ttk.Scrollbar(current_steps_frame, orient="vertical", command=steps_listbox.yview)
            steps_listbox.configure(yscrollcommand=steps_scrollbar.set)
            
            steps_listbox.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            steps_scrollbar.pack(side="right", fill="y")
            
            # Separate login steps from regular steps
            login_steps_data = []
            current_steps_data = []
            
            def get_login_steps():
                """Get steps from Login test group dynamically with current credentials"""
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
                        {'order': 1, 'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                        {'order': 2, 'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': username},
                        {'order': 3, 'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': password},
                        {'order': 4, 'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                    ]
                
                # Get steps from Login group
                login_steps = self.db_manager.get_test_steps_by_group(login_group_id)
                result = []
                
                for i, step in enumerate(login_steps):
                    step_id, name, step_type, target, description = step
                    # Replace credentials for Text Input steps
                    if step_type == 'Text Input':
                        if 'username' in name.lower():
                            description = username
                        elif 'password' in name.lower():
                            description = password
                    
                    result.append({
                        'order': i + 1,
                        'name': name,
                        'type': step_type,
                        'target': target,
                        'description': description or ''
                    })
                
                return result
            
            # CRITICAL BUG FIX: Detect login steps by test_step_id references to Login group
            login_group_steps = get_login_steps()
            login_step_count = len(login_group_steps)
            has_login_steps = False
            
            # Get Login group ID for reliable detection
            groups = self.db_manager.get_test_step_groups()
            login_group_id = None
            for group in groups:
                if group[1].lower() == 'login':
                    login_group_id = group[0]
                    break
            
            # Check if scenario has steps that reference the Login group
            if login_group_id and auto_login:
                login_step_ids = {step[0] for step in self.db_manager.get_test_steps_by_group(login_group_id)}
                existing_step_ids = {step[5] for step in existing_steps if step[5]}  # test_step_id
                
                # If any existing steps reference Login group steps, we have login steps
                has_login_steps = bool(login_step_ids.intersection(existing_step_ids))
            
            # Split steps into login and regular using test_step_id references
            if has_login_steps and auto_login:
                # Find where login steps end by checking test_step_id references
                login_step_ids = {step[0] for step in self.db_manager.get_test_steps_by_group(login_group_id)}
                login_end_index = 0
                
                for i, step in enumerate(existing_steps):
                    test_step_id = step[5]  # test_step_id from scenario_steps
                    if test_step_id not in login_step_ids:
                        login_end_index = i
                        break
                else:
                    login_end_index = len(existing_steps)
                
                login_steps_raw = existing_steps[:login_end_index]
                regular_steps_raw = existing_steps[login_end_index:]
                
                for step in login_steps_raw:
                    step_order, step_name, step_type, step_target, step_description, test_step_id = step
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
                step_order, step_name, step_type, step_target, step_description, test_step_id = step
                current_steps_data.append({
                    'order': step_order,
                    'name': step_name,
                    'type': step_type,
                    'target': step_target,
                    'description': step_description,
                    'step_id': test_step_id
                })
            
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
                    elif step['type'] == 'Wait':
                        # CRITICAL FIX: Show scenario-specific value, not global test step value
                        scenario_value = step.get('description', '3')  # Use scenario's custom value
                        target = step.get('target', '')
                        
                        if target and ('Element Visible:' in target or 'Element Clickable:' in target):
                            display_text += f" - Selector: {scenario_value}"
                        else:
                            display_text += f" - Value: {scenario_value}s"
                    steps_listbox.insert(tk.END, display_text)
                    step_counter += 1
                
                current_steps_frame.config(text=f"Current Steps ({step_counter - 1})")
            
            def toggle_login_display():
                """Toggle login credentials and steps display"""
                try:
                    if auto_login_var.get():
                        login_creds_frame.pack(fill="x", pady=(0, 20))
                    else:
                        login_creds_frame.pack_forget()
                    update_steps_display()
                except tk.TclError:
                    # Widget has been destroyed, ignore
                    pass
            
            # Auto-login checkbox with manual command
            auto_login_var = tk.BooleanVar(value=bool(auto_login))
            
            def manual_toggle():
                """Manual toggle with smooth animation"""
                try:
                    current_geometry = popup.geometry()
                    width, height, x, y = current_geometry.replace('x', '+').replace('+', ' ').split()
                    start_height = int(height)
                    start_y = int(y)
                    
                    if auto_login_var.get():
                        login_creds_frame.pack(fill="x", pady=(0, 20))
                        target_height = 772
                        target_y = max(0, start_y - 36)  # Move up half the expansion
                    else:
                        target_height = 700
                        target_y = start_y + 36  # Move down half the contraction
                    
                    # Direct smooth transition
                    popup.geometry(f"900x{target_height}+{x}+{target_y}")
                    
                    if not auto_login_var.get():
                        popup.after(1, lambda: login_creds_frame.pack_forget())
                    
                    update_steps_display()
                except tk.TclError:
                    pass
            
            auto_login_checkbox = tk.Checkbutton(left_frame, text="Include Login (Add login steps as initial steps)", 
                          variable=auto_login_var, font=('Segoe UI', 10), bg='#ffffff', command=manual_toggle)
            auto_login_checkbox.pack(anchor="w", pady=(10, 10))
            
            # Step management buttons
            step_mgmt_frame = tk.Frame(steps_frame, bg='#ffffff')
            step_mgmt_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            def remove_selected_step():
                selection = steps_listbox.curselection()
                if selection:
                    index = selection[0]
                    login_step_count = len(get_login_steps()) if auto_login_var.get() else 0
                    
                    if index < login_step_count:
                        self.show_popup("Info", "Login steps can only be removed by unchecking 'Include Login'", "warning")
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
                    login_step_count = len(get_login_steps()) if auto_login_var.get() else 0
                    
                    # Can't move login steps or move regular steps above login steps
                    if index < login_step_count or index == login_step_count:
                        self.show_popup("Info", "Cannot move login steps or move steps above login steps", "warning")
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
                    login_step_count = len(get_login_steps()) if auto_login_var.get() else 0
                    
                    # Can't move login steps
                    if index < login_step_count:
                        self.show_popup("Info", "Cannot move login steps", "warning")
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
            
            def add_steps_from_groups():
                """Add steps from test groups to scenario"""
                # Get test step groups
                groups = self.db_manager.get_test_step_groups()
                if not groups:
                    self.show_popup("No Groups", "No test step groups found. Please create test groups first.", "warning")
                    return
                
                # Create selection dialog
                from Temp.enhanced_popup_system import create_enhanced_dialog
                select_popup = create_enhanced_dialog(popup, "Add Steps from Test Groups", 600, 500, modal=False)
                select_popup.configure(bg='#ffffff')
                select_popup.attributes('-topmost', False)
                select_popup.resizable(False, False)
                
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
                            
                            # Add to current steps
                            new_order = len(current_steps_data) + 1
                            current_steps_data.append({
                                'order': new_order,
                                'name': name,
                                'type': step_type,
                                'target': target,
                                'description': description or '',
                                'step_id': step_id
                            })
                    
                    # Update display
                    update_steps_display()
                    select_popup.destroy()
                
                tk.Button(btn_frame, text="Add Selected", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=add_selected).pack(side="left", padx=(0, 10))
                tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=select_popup.destroy).pack(side="left")
            
            def remove_multiple_steps():
                """Remove multiple selected steps at once"""
                # Change listbox to multiple selection mode temporarily
                steps_listbox.config(selectmode=tk.MULTIPLE)
                
                # Create selection dialog
                from Temp.enhanced_popup_system import create_enhanced_dialog
                select_popup = create_enhanced_dialog(popup, "Remove Multiple Steps", 644, 400, modal=False)
                select_popup.configure(bg='#ffffff')
                
                try:
                    select_popup.iconbitmap("infor_logo.ico")
                except:
                    pass
                
                # Header with red background for delete
                header_frame = tk.Frame(select_popup, bg='#ef4444', height=50)
                header_frame.pack(fill='x')
                header_frame.pack_propagate(False)
                
                tk.Label(header_frame, text="🗑️ Remove Multiple Steps", font=('Segoe UI', 12, 'bold'), 
                        bg='#ef4444', fg='#ffffff').pack(expand=True)
                
                # Content
                content_frame = tk.Frame(select_popup, bg='#ffffff', padx=20, pady=20)
                content_frame.pack(fill='both', expand=True)
                
                tk.Label(content_frame, text="Select steps to remove (Ctrl+Click for multiple):", 
                        font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
                
                # Steps listbox for selection
                select_listbox = tk.Listbox(content_frame, font=('Segoe UI', 9), selectmode=tk.MULTIPLE, height=12)
                select_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=select_listbox.yview)
                select_listbox.configure(yscrollcommand=select_scrollbar.set)
                
                select_listbox.pack(side="left", fill="both", expand=True, pady=(0, 15))
                select_scrollbar.pack(side="right", fill="y", pady=(0, 15))
                
                # Populate with current steps (excluding login steps)
                login_step_count = len(get_login_steps()) if auto_login_var.get() else 0
                
                for i, step in enumerate(current_steps_data):
                    display_text = f"{i + 1 + login_step_count}. {step['name']} ({step['type']})"
                    if step['type'] == 'Text Input' and step.get('description'):
                        is_password = 'password' in step['name'].lower()
                        if is_password:
                            display_text += f" - Value: {'•' * len(step['description'])}"
                        else:
                            display_text += f" - Value: '{step['description']}'"
                    select_listbox.insert(tk.END, display_text)
                
                if not current_steps_data:
                    tk.Label(content_frame, text="No regular steps to remove", 
                            font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280').pack(pady=20)
                
                # Info label
                info_frame = tk.Frame(content_frame, bg='#ffffff')
                info_frame.pack(fill='x', pady=(0, 15))
                
                tk.Label(info_frame, text="Note: Login steps cannot be removed here. Use 'Include Login' checkbox to manage login steps.", 
                        font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280', wraplength=450).pack()
                
                # Buttons
                btn_frame = tk.Frame(content_frame, bg='#ffffff')
                btn_frame.pack()
                
                def remove_selected():
                    selection = select_listbox.curselection()
                    if not selection:
                        # Create a custom info popup
                        info_popup = tk.Toplevel(select_popup)
                        info_popup.title("Info")
                        center_dialog(info_popup, 300, 150)
                        info_popup.configure(bg='#ffffff')
                        info_popup.transient(select_popup)
                        info_popup.grab_set()
                        
                        try:
                            info_popup.iconbitmap("infor_logo.ico")
                        except:
                            pass
                        
                        tk.Label(info_popup, text="Please select steps to remove", 
                                font=('Segoe UI', 10), bg='#ffffff').pack(pady=30)
                        tk.Button(info_popup, text="OK", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=info_popup.destroy).pack()
                        return
                    
                    try:
                        # Get the step orders to delete from database
                        login_step_count = len(get_login_steps()) if auto_login_var.get() else 0
                        steps_to_delete = []
                        
                        for index in selection:
                            if index < len(current_steps_data):
                                # Calculate actual step order in database (including login steps)
                                actual_step_order = index + 1 + login_step_count
                                steps_to_delete.append(actual_step_order)
                        
                        # Delete from database immediately
                        cursor = self.db_manager.conn.cursor()
                        for step_order in steps_to_delete:
                            cursor.execute("""
                                DELETE FROM scenario_steps 
                                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ? AND step_order = ?
                            """, (self.db_manager.user_id, str(current_profile), scenario_number, step_order))
                        
                        # Renumber remaining steps in database
                        cursor.execute("""
                            SELECT step_order FROM scenario_steps 
                            WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
                            ORDER BY step_order
                        """, (self.db_manager.user_id, str(current_profile), scenario_number))
                        
                        remaining_orders = [row[0] for row in cursor.fetchall()]
                        
                        # Update step orders to be sequential
                        for new_order, old_order in enumerate(remaining_orders, 1):
                            if new_order != old_order:
                                cursor.execute("""
                                    UPDATE scenario_steps 
                                    SET step_order = ? 
                                    WHERE user_id = ? AND rice_profile = ? AND scenario_number = ? AND step_order = ?
                                """, (new_order, self.db_manager.user_id, str(current_profile), scenario_number, old_order))
                        
                        self.db_manager.conn.commit()
                        
                        # Remove from memory (in reverse order to maintain indices)
                        for index in reversed(sorted(selection)):
                            if index < len(current_steps_data):
                                current_steps_data.pop(index)
                        
                        # Renumber remaining steps in memory
                        for i, step in enumerate(current_steps_data):
                            step['order'] = i + 1
                        
                        # Update main display
                        update_steps_display()
                        
                        # Reset listbox selection mode
                        steps_listbox.config(selectmode=tk.SINGLE)
                        
                        select_popup.destroy()
                        
                        # Refresh the scenarios table to update step count
                        if refresh_callback:
                            refresh_callback()
                        
                        # Show success message
                        removed_count = len(selection)
                        self.show_popup("Success", f"Removed {removed_count} step{'s' if removed_count != 1 else ''} from database successfully!", "success")
                        
                    except Exception as e:
                        self.show_popup("Error", f"Failed to remove steps from database: {str(e)}", "error")
                
                def cancel_remove():
                    # Reset listbox selection mode
                    steps_listbox.config(selectmode=tk.SINGLE)
                    select_popup.destroy()
                
                tk.Button(btn_frame, text="Remove Selected", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=remove_selected).pack(side="left", padx=(0, 10))
                tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                         relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=cancel_remove).pack(side="left")
            
            # Initialize edit value handler
            edit_value_handler = ScenarioEditValue(self.db_manager, self.show_popup)
            
            def edit_step_value():
                """Edit input value for Text Input and Wait steps"""
                selection = steps_listbox.curselection()
                if not selection:
                    self.show_popup("Error", "Please select a step to edit", "error")
                    return
                
                index = selection[0]
                login_step_count = len(get_login_steps()) if auto_login_var.get() else 0
                
                # Determine if this is a login step or regular step
                if index < login_step_count:
                    # Can't edit login steps directly - use credential fields
                    self.show_popup("Info", "Login step values can be edited using the Username/Password fields above", "warning")
                    return
                else:
                    actual_index = index - login_step_count
                    if actual_index >= len(current_steps_data):
                        return
                    step_data = current_steps_data[actual_index]
                
                # Use modular edit value handler
                edit_value_handler.edit_step_value(popup, step_data, index, update_steps_display, steps_listbox)
            
            tk.Button(step_mgmt_frame, text="📋 Add from Groups", font=('Segoe UI', 9), bg='#3b82f6', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=add_steps_from_groups).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="✏️ Edit Value", font=('Segoe UI', 9), bg='#3b82f6', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=edit_step_value).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="❌ Remove", font=('Segoe UI', 9), bg='#ef4444', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=remove_selected_step).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="🗑️ Remove Multiple", font=('Segoe UI', 9), bg='#dc2626', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=remove_multiple_steps).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="⬆️ Up", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_up).pack(side="left", padx=(0, 5))
            tk.Button(step_mgmt_frame, text="⬇️ Down", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=8, pady=4, cursor='hand2', bd=0, command=move_step_down).pack(side="left")
            
            # Initial display
            update_steps_display()
            
            # Bottom buttons
            btn_frame = tk.Frame(main_frame, bg='#ffffff')
            btn_frame.pack(fill="x", pady=(20, 0))
            
            def save_changes():
                # CRITICAL FIX: Capture all widget values BEFORE any database operations
                new_description = desc_entry.get().strip()
                new_file_path = file_entry.get().strip() or None
                new_auto_login = auto_login_var.get()
                current_username = username_entry.get().strip() if username_entry.get() else "[username]"
                current_password = password_entry.get().strip() if password_entry.get() else "[password]"
                
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
                    
                    # CRITICAL BUG FIX: Only insert login steps if they weren't already in the scenario
                    step_order = 1
                    if new_auto_login:
                        # Check if login steps were already detected in existing scenario
                        current_login_steps = get_login_steps()
                        
                        # Get Login group ID
                        groups = self.db_manager.get_test_step_groups()
                        login_group_id = None
                        for group in groups:
                            if group[1].lower() == 'login':
                                login_group_id = group[0]
                                break
                        
                        # Only add login steps if we don't already have them (check by test_step_id)
                        if login_group_id:
                            login_step_ids = {step[0] for step in self.db_manager.get_test_steps_by_group(login_group_id)}
                            existing_step_ids = {step.get('step_id') for step in current_steps_data if step.get('step_id')}
                            
                            # If login step IDs are not already in current_steps_data, add them
                            if not login_step_ids.intersection(existing_step_ids):
                                try:
                                    groups = self.db_manager.get_test_step_groups()
                                    login_group_id = None
                                    for group in groups:
                                        if group[1].lower() == 'login':
                                            login_group_id = group[0]
                                            break
                                    
                                    if login_group_id:
                                        login_group_steps = self.db_manager.get_test_steps_by_group(login_group_id)
                                        for step in login_group_steps:
                                            step_id, name, step_type, target, description = step
                                            # Replace credentials for Text Input steps
                                            if step_type == 'Text Input':
                                                if 'username' in name.lower():
                                                    description = current_username
                                                elif 'password' in name.lower():
                                                    description = current_password
                                            
                                            cursor.execute("""
                                                INSERT INTO scenario_steps 
                                                (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                                                VALUES (?, ?, ?, ?, ?, ?, ?)
                                            """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                                                  step_order, step_id, description, 1))
                                            step_order += 1
                                    else:
                                        # Fallback to hardcoded login steps
                                        login_steps_fallback = [
                                            {'name': 'Navigate to Login Page', 'type': 'Navigate', 'target': 'https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1', 'description': ''},
                                            {'name': 'Enter Username', 'type': 'Text Input', 'target': 'input[name="username"]', 'description': current_username},
                                            {'name': 'Enter Password', 'type': 'Text Input', 'target': 'input[name="password"]', 'description': current_password},
                                            {'name': 'Click Login', 'type': 'Element Click', 'target': 'span:contains("Login")', 'description': 'Click login button'}
                                        ]
                                        for login_step in login_steps_fallback:
                                            cursor.execute("""
                                                INSERT INTO scenario_steps 
                                                (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                                            """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                                                  step_order, login_step['name'], login_step['type'], login_step['target'], login_step['description'], 1))
                                            step_order += 1
                                except:
                                    pass
                    
                    # Insert regular steps with test_step_id references
                    for step in current_steps_data:
                        if step.get('step_id'):
                            cursor.execute("""
                                INSERT INTO scenario_steps 
                                (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?)
                            """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                                  step_order, step['step_id'], step['description'], 1))
                        else:
                            # Fallback for steps without test_step_id
                            cursor.execute("""
                                INSERT INTO scenario_steps 
                                (user_id, rice_profile, scenario_number, step_order, step_name, step_type, step_target, step_description, fsm_page_id)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (self.db_manager.user_id, str(current_profile), scenario_number, 
                                  step_order, step['name'], step['type'], step['target'], step['description'], 1))
                        step_order += 1
                    
                    self.db_manager.conn.commit()
                    
                    # Calculate total steps for success message
                    login_step_count = len(get_login_steps()) if new_auto_login else 0
                    total_steps = len(current_steps_data) + login_step_count
                    
                    # Close popup AFTER all operations are complete
                    popup.destroy()
                    
                    # Refresh and show success
                    if refresh_callback:
                        refresh_callback()
                    
                    self.show_popup("Success", f"Scenario #{scenario_number} updated with {total_steps} steps!", "success")
                    
                except Exception as e:
                    self.show_popup("Error", f"Failed to update scenario: {str(e)}", "error")
            
            tk.Button(btn_frame, text="💾 Save Changes", font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
            def cancel_dialog():
                popup.destroy()
            
            tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 12, 'bold'), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=20, pady=10, cursor='hand2', bd=0, command=cancel_dialog).pack(side="left")
            
            desc_entry.focus()
            desc_entry.select_range(0, tk.END)
            
        except Exception as e:
            self.show_popup("Error", f"Failed to edit scenario: {str(e)}", "error")