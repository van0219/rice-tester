#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import tkinter as tk
from tkinter import ttk, filedialog
from enhanced_popup_system import EnhancedPopupManager

class ModernScenarioAddForm:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.popup_manager = EnhancedPopupManager()
        
    def add_scenario(self, current_profile, refresh_callback):
        """Modern Add Scenario form with Test Users integration"""
        try:
            next_number = self.db_manager.get_next_scenario_number(current_profile)
            
            # Create modern dialog
            dialog = self.popup_manager.create_dynamic_dialog(
                parent=None,
                title=f"Add Scenario #{next_number}",
                width=1000,
                height=700,
                resizable=True
            )
            
            # Header with modern card design
            header_frame = tk.Frame(dialog, bg='#10b981', height=60)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            title_label = tk.Label(header_frame, text=f"📋 Add Scenario #{next_number}", 
                                  font=('Segoe UI', 16, 'bold'), 
                                  bg='#10b981', fg='white')
            title_label.pack(expand=True)
            
            # Main content with responsive layout
            content_frame = tk.Frame(dialog, bg='#f8fafc', padx=20, pady=20)
            content_frame.pack(fill='both', expand=True)
            
            # Left panel - Scenario Details
            left_panel = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
            left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
            
            self._create_scenario_details_panel(left_panel, next_number)
            
            # Right panel - Test Steps Selection
            right_panel = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
            right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
            
            self._create_test_steps_panel(right_panel)
            
            # Bottom action bar with increased height for button visibility
            action_frame = tk.Frame(content_frame, bg='#f8fafc', height=100)
            action_frame.pack(fill='x', pady=(20, 0))
            action_frame.pack_propagate(False)
            
            self._create_action_buttons(action_frame, dialog, current_profile, next_number, refresh_callback)
            
            # Initialize data
            self.selected_steps = []
            self.login_steps_data = []
            
            # Focus on description
            self.desc_entry.focus()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to create add scenario form: {str(e)}", "error")
    
    def _create_scenario_details_panel(self, parent, scenario_number):
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
        self.desc_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # File path field
        tk.Label(content, text="File Path (Optional)", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151').pack(anchor='w', pady=(0, 5))
        
        file_frame = tk.Frame(content, bg='white')
        file_frame.pack(fill='x', pady=(0, 15))
        
        self.file_entry = tk.Entry(file_frame, font=('Segoe UI', 11),
                                  relief='solid', bd=1, highlightthickness=1,
                                  highlightcolor='#3b82f6', highlightbackground='#d1d5db')
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
        
        self.include_login_var = tk.BooleanVar()
        login_check = tk.Checkbutton(login_section, 
                                    text="Include Login Steps", 
                                    variable=self.include_login_var,
                                    font=('Segoe UI', 10), bg='white',
                                    command=self._toggle_login_section)
        login_check.pack(anchor='w', pady=(0, 10))
        
        # Test User selection (modern approach)
        self.test_user_frame = tk.Frame(login_section, bg='white')
        
        tk.Label(self.test_user_frame, text="Select Test User:", 
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        
        user_select_frame = tk.Frame(self.test_user_frame, bg='white')
        user_select_frame.pack(fill='x', pady=(0, 10))
        
        self.test_user_var = tk.StringVar()
        self.test_user_combo = ttk.Combobox(user_select_frame, textvariable=self.test_user_var,
                                           font=('Segoe UI', 10), state='readonly')
        self.test_user_combo.pack(fill='x')
        
        # Load test users
        self._load_test_users()
        
        # Bind user selection change
        self.test_user_combo.bind('<<ComboboxSelected>>', self._on_user_selected)
        
        # Initially hide login section
        self.test_user_frame.pack_forget()
    
    def _create_test_steps_panel(self, parent):
        """Create modern test steps selection panel"""
        # Panel header
        header = tk.Frame(parent, bg='#10b981', height=45)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        header_content = tk.Frame(header, bg='#10b981')
        header_content.pack(fill='both', expand=True, padx=15, pady=10)
        
        tk.Label(header_content, text="🔧 Test Steps Selection", 
                font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='white').pack(side='left')
        
        # Header buttons
        header_buttons = tk.Frame(header_content, bg='#10b981')
        header_buttons.pack(side='right')
        
        # Import button
        import_btn = tk.Button(header_buttons, text="📥 Import Groups",
                              font=('Segoe UI', 9, 'bold'), bg='#059669', fg='white',
                              relief='flat', padx=10, pady=4, cursor='hand2', bd=0,
                              command=self._show_import_dialog)
        import_btn.pack(side='left', padx=(0, 5))
        
        # Save button
        save_btn = tk.Button(header_buttons, text="💾 Save",
                            font=('Segoe UI', 9, 'bold'), bg='#047857', fg='white',
                            relief='flat', padx=15, pady=4, cursor='hand2', bd=0,
                            command=lambda: self._save_scenario(self.dialog, self.current_profile, self.scenario_number, self.refresh_callback))
        save_btn.pack(side='left')
        
        # Content area
        content = tk.Frame(parent, bg='white', padx=15, pady=15)
        content.pack(fill='both', expand=True)
        
        # Test Group selection
        group_frame = tk.Frame(content, bg='white')
        group_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(group_frame, text="Test Step Group:", 
                font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        
        self.group_var = tk.StringVar()
        self.group_combo = ttk.Combobox(group_frame, textvariable=self.group_var,
                                       font=('Segoe UI', 10), state='readonly')
        self.group_combo.pack(fill='x', pady=(0, 10))
        self.group_combo.bind('<<ComboboxSelected>>', self._load_group_steps)
        
        # Available steps
        available_frame = tk.LabelFrame(content, text="Available Steps", 
                                       font=('Segoe UI', 10, 'bold'), bg='white')
        available_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.available_listbox = tk.Listbox(available_frame, font=('Segoe UI', 9), 
                                           selectmode=tk.MULTIPLE, height=8)
        available_scroll = ttk.Scrollbar(available_frame, orient='vertical', 
                                        command=self.available_listbox.yview)
        self.available_listbox.configure(yscrollcommand=available_scroll.set)
        
        self.available_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        available_scroll.pack(side='right', fill='y', pady=5)
        
        # Selected steps
        selected_frame = tk.LabelFrame(content, text="Selected Steps (Execution Order)", 
                                      font=('Segoe UI', 10, 'bold'), bg='white')
        selected_frame.pack(fill='both', expand=True)
        
        self.selected_listbox = tk.Listbox(selected_frame, font=('Segoe UI', 9), height=8)
        selected_scroll = ttk.Scrollbar(selected_frame, orient='vertical', 
                                       command=self.selected_listbox.yview)
        self.selected_listbox.configure(yscrollcommand=selected_scroll.set)
        
        self.selected_listbox.pack(side='left', fill='both', expand=True, padx=5, pady=5)
        selected_scroll.pack(side='right', fill='y', pady=5)
        
        # Step management buttons
        btn_frame = tk.Frame(content, bg='white')
        btn_frame.pack(fill='x', pady=(10, 0))
        
        tk.Button(btn_frame, text="▶️ Add Selected", 
                 font=('Segoe UI', 9, 'bold'), bg='#10b981', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._add_selected_steps).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="📋 Add Multiple", 
                 font=('Segoe UI', 9, 'bold'), bg='#059669', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._add_multiple_steps).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="✏️ Edit Value", 
                 font=('Segoe UI', 9, 'bold'), bg='#3b82f6', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._edit_step_value).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="❌ Remove", 
                 font=('Segoe UI', 9, 'bold'), bg='#ef4444', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._remove_selected_step).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="🗑️ Remove Multiple", 
                 font=('Segoe UI', 9, 'bold'), bg='#dc2626', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._remove_multiple_steps).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="⬆️ Up", 
                 font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._move_step_up).pack(side='left', padx=(0, 5))
        
        tk.Button(btn_frame, text="⬇️ Down", 
                 font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='white',
                 relief='flat', padx=10, pady=6, cursor='hand2', bd=0,
                 command=self._move_step_down).pack(side='left')
        
        # Load test groups
        self._load_test_groups()
    
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
        self._update_selected_steps_display()
    
    def _on_groups_imported(self):
        """Callback when test groups are imported"""
        # Refresh test groups dropdown
        self._load_test_groups()
        self.popup_manager.show_success("Success", "Test groups imported successfully!")
    
    def _create_action_buttons(self, parent, dialog, current_profile, scenario_number, refresh_callback):
        """Create modern action buttons"""
        # Center the button container
        btn_container = tk.Frame(parent, bg='#f8fafc')
        btn_container.pack(expand=True, pady=15)
        
        # Button frame for proper alignment
        button_frame = tk.Frame(btn_container, bg='#f8fafc')
        button_frame.pack()
        
        save_btn = tk.Button(button_frame, text="💾 Create Scenario",
                            font=('Segoe UI', 11, 'bold'), bg='#10b981', fg='white',
                            relief='flat', padx=25, pady=12, cursor='hand2', bd=0,
                            highlightthickness=0,
                            command=lambda: self._save_scenario(dialog, current_profile, scenario_number, refresh_callback))
        save_btn.pack(side='left', padx=(0, 10))
        
        cancel_btn = tk.Button(button_frame, text="❌ Cancel",
                              font=('Segoe UI', 11, 'bold'), bg='#6b7280', fg='white',
                              relief='flat', padx=25, pady=12, cursor='hand2', bd=0,
                              highlightthickness=0, command=dialog.destroy)
        cancel_btn.pack(side='left')
        
        # Store references
        self.dialog = dialog
        self.current_profile = current_profile
        self.scenario_number = scenario_number
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
        
        self._update_selected_steps_display()
    
    def _load_test_users(self):
        """Load test users into dropdown"""
        try:
            users = self.db_manager.get_test_users()
            user_options = [f"{user[1]} ({user[2]})" for user in users]  # name (email)
            self.test_user_combo['values'] = user_options
            
            if user_options:
                self.test_user_combo.current(0)
        except Exception as e:
            print(f"Error loading test users: {e}")
    

    
    def _load_test_groups(self):
        """Load test step groups (excluding Login group)"""
        try:
            groups = self.db_manager.get_test_step_groups()
            # Filter out Login group since it's handled by the checkbox
            filtered_groups = [group for group in groups if group[1].lower() != 'login']
            group_options = [f"{group[1]} ({group[3]} steps)" for group in filtered_groups]
            self.group_combo['values'] = group_options
        except Exception as e:
            print(f"Error loading test groups: {e}")
    
    def _load_group_steps(self, event=None):
        """Load steps from selected group"""
        if not self.group_var.get():
            return
        
        try:
            groups = self.db_manager.get_test_step_groups()
            # Filter out Login group since it's handled by the checkbox
            filtered_groups = [group for group in groups if group[1].lower() != 'login']
            group_index = self.group_combo.current()
            
            if group_index >= 0 and group_index < len(filtered_groups):
                group_id = filtered_groups[group_index][0]
                steps = self.db_manager.get_test_steps_by_group(group_id)
                
                self.available_listbox.delete(0, tk.END)
                for step in steps:
                    step_id, name, step_type, target, description = step
                    display_text = f"{name} ({step_type})"
                    self.available_listbox.insert(tk.END, display_text)
        except Exception as e:
            print(f"Error loading group steps: {e}")
    
    def _add_selected_steps(self):
        """Add selected steps to scenario"""
        selection = self.available_listbox.curselection()
        if not selection or not self.group_var.get():
            return
        
        try:
            groups = self.db_manager.get_test_step_groups()
            # Filter out Login group since it's handled by the checkbox
            filtered_groups = [group for group in groups if group[1].lower() != 'login']
            group_index = self.group_combo.current()
            
            if group_index >= 0 and group_index < len(filtered_groups):
                group_id = filtered_groups[group_index][0]
                steps = self.db_manager.get_test_steps_by_group(group_id)
                
                for index in selection:
                    if index < len(steps):
                        step_data = steps[index]
                        step_id, name, step_type, target, description = step_data
                        
                        self.selected_steps.append({
                            'step_id': step_id,
                            'name': name,
                            'type': step_type,
                            'target': target,
                            'description': description or ''
                        })
                
                self._update_selected_steps_display()
        except Exception as e:
            self.show_popup("Error", f"Failed to add steps: {str(e)}", "error")
    
    def _remove_selected_step(self):
        """Remove selected step"""
        selection = self.selected_listbox.curselection()
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
        if actual_index < len(self.selected_steps):
            self.selected_steps.pop(actual_index)
            self._update_selected_steps_display()
    
    def _move_step_up(self):
        """Move step up in execution order"""
        selection = self.selected_listbox.curselection()
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
            self.selected_steps[actual_index], self.selected_steps[actual_index-1] = \
                self.selected_steps[actual_index-1], self.selected_steps[actual_index]
            self._update_selected_steps_display()
            self.selected_listbox.selection_set(index-1)
    
    def _move_step_down(self):
        """Move step down in execution order"""
        selection = self.selected_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        login_step_count = len(self.login_steps_data)
        
        if index < login_step_count:
            self.popup_manager.show_info("Info", "Cannot move login steps", parent=self.dialog)
            return
        
        actual_index = index - login_step_count
        if actual_index < len(self.selected_steps) - 1:
            self.selected_steps[actual_index], self.selected_steps[actual_index+1] = \
                self.selected_steps[actual_index+1], self.selected_steps[actual_index]
            self._update_selected_steps_display()
            self.selected_listbox.selection_set(index+1)
    
    def _edit_step_value(self):
        """Edit step value for Text Input steps (excluding login steps)"""
        selection = self.selected_listbox.curselection()
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
        if actual_index >= len(self.selected_steps):
            return
        
        step = self.selected_steps[actual_index]
        
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
            self._update_selected_steps_display()
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
    
    def _add_multiple_steps(self):
        """Add multiple steps from test groups dialog"""
        try:
            # Create step selection dialog
            step_dialog = self.popup_manager.create_dynamic_dialog(
                parent=self.dialog,
                title="Add Multiple Steps from Test Groups",
                width=800,
                height=600,
                resizable=True
            )
            
            # Header
            header = tk.Frame(step_dialog, bg='#10b981', height=50)
            header.pack(fill='x')
            header.pack_propagate(False)
            
            tk.Label(header, text="📋 Add Multiple Steps from Test Groups", 
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
            
            steps_tree.pack(side='left', fill='both', expand=True)
            steps_scroll.pack(side='right', fill='y')
            
            # Load groups (excluding Login)
            all_groups = self.db_manager.get_test_step_groups()
            groups = [group for group in all_groups if group[1].lower() != 'login']
            
            if groups:
                group_options = [f"{group[1]} ({group[3]} steps)" for group in groups]
                group_combo['values'] = group_options
                if group_options:
                    group_combo.current(0)
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
            
            # Buttons
            btn_frame = tk.Frame(content, bg='white')
            btn_frame.pack(fill='x')
            
            def add_selected_steps():
                selection = steps_tree.selection()
                if not selection or not groups:
                    self.popup_manager.show_error("Error", "Please select steps to add", parent=step_dialog)
                    return
                
                try:
                    group_index = group_combo.current()
                    if 0 <= group_index < len(groups):
                        group_id = groups[group_index][0]
                        steps = self.db_manager.get_test_steps_by_group(group_id)
                        
                        added_count = 0
                        for item_id in selection:
                            try:
                                index = int(item_id)
                                if index < len(steps):
                                    step_data = steps[index]
                            except (ValueError, IndexError):
                                continue
                            if index < len(steps):
                                step_id, name, step_type, target, description = step_data
                                
                                self.selected_steps.append({
                                    'step_id': step_id,
                                    'name': name,
                                    'type': step_type,
                                    'target': target,
                                    'description': description or ''
                                })
                                added_count += 1
                        
                        self._update_selected_steps_display()
                        step_dialog.destroy()
                        
                        if added_count > 0:
                            self.popup_manager.show_success("Success", f"Added {added_count} steps to scenario")
                        
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
            self.popup_manager.show_error("Error", f"Failed to open add multiple dialog: {str(e)}", parent=self.dialog)
    
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
        for i, step in enumerate(self.selected_steps):
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
                if index < len(self.selected_steps):
                    self.selected_steps.pop(index)
            
            self._update_selected_steps_display()
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
    
    def _update_selected_steps_display(self):
        """Update selected steps display"""
        self.selected_listbox.delete(0, tk.END)
        
        # Update login steps data
        self.login_steps_data.clear()
        if self.include_login_var.get():
            self.login_steps_data = self._get_login_steps()
        
        step_counter = 1
        
        # Add login steps
        for login_step in self.login_steps_data:
            display_text = f"{step_counter}. {login_step['name']} ({login_step['type']}) [LOGIN]"
            self.selected_listbox.insert(tk.END, display_text)
            step_counter += 1
        
        # Add regular steps
        for step in self.selected_steps:
            display_text = f"{step_counter}. {step['name']} ({step['type']})"
            self.selected_listbox.insert(tk.END, display_text)
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
    

    
    def _save_scenario(self, dialog, current_profile, scenario_number, refresh_callback):
        """Save the new scenario"""
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
            # Save scenario
            scenario_id = self.db_manager.save_scenario(
                current_profile, scenario_number, description, file_path, include_login
            )
            
            # Save steps
            step_order = 1
            
            # Add login steps if requested
            if include_login:
                login_steps = self._get_login_steps()
                for login_step in login_steps:
                    cursor = self.db_manager.conn.cursor()
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
            
            # Add selected test steps
            for step in self.selected_steps:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("""
                    INSERT INTO scenario_steps 
                    (user_id, rice_profile, scenario_number, step_order, test_step_id, step_description, fsm_page_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.db_manager.user_id, str(current_profile), scenario_number, step_order,
                      step['step_id'], step['description'], 1))
                step_order += 1
            
            self.db_manager.conn.commit()
            
            # Success
            total_steps = len(self.selected_steps) + len(self.login_steps_data)
            dialog.destroy()
            
            if refresh_callback:
                refresh_callback()
            
            self.popup_manager.show_success("Success", 
                f"Scenario #{scenario_number} created successfully with {total_steps} steps!")
            
        except Exception as e:
            self.popup_manager.show_error("Error", f"Failed to create scenario: {str(e)}", parent=self.dialog)

def main():
    """Test the modern add scenario form"""
    root = tk.Tk()
    root.withdraw()
    
    # Mock database manager for testing
    class MockDB:
        def get_next_scenario_number(self, profile):
            return 1
        def get_test_users(self):
            return [(1, "Test User", "test@example.com", "encrypted_pass")]
        def get_test_step_groups(self):
            return [(1, "Login", "Login steps", 4), (2, "Navigation", "Nav steps", 3)]
        def get_test_steps_by_group(self, group_id):
            return [(1, "Navigate", "Navigate", "url", ""), (2, "Click", "Element Click", "button", "")]
    
    def mock_popup(title, message, type):
        print(f"{type}: {title} - {message}")
    
    form = ModernScenarioAddForm(MockDB(), mock_popup)
    form.add_scenario(1, lambda: print("Refreshed"))
    
    root.mainloop()

if __name__ == "__main__":
    main()