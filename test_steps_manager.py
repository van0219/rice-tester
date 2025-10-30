#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from selenium_tab_manager import center_dialog

class TestStepsManager:
    def __init__(self, root, db_manager, show_popup_callback):
        self.root = root
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.current_group_id = None
        self.current_steps_page = 1
        self.steps_per_page = 10
        self.steps_popup = None
    
    def setup_test_steps_tab(self, parent):
        """Test steps tab with groups and steps"""
        frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = tk.Frame(frame, bg='#ffffff')
        header_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(header_frame, text="Test Step Groups", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(side="left")
        
        # Groups container
        groups_container = tk.Frame(frame, bg='#ffffff')
        groups_container.pack(fill="x", pady=(0, 5))
        
        # Headers
        headers_frame = tk.Frame(groups_container, bg='#e5e7eb', height=25)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="Group Name", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0, y=5, relwidth=0.3)
        tk.Label(headers_frame, text="Description", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.3, y=5, relwidth=0.4)
        tk.Label(headers_frame, text="Steps", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.7, y=5, relwidth=0.1)
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.8, y=5, relwidth=0.2)
        
        # Groups scroll frame
        self.groups_scroll_frame = tk.Frame(groups_container, bg='#ffffff')
        self.groups_scroll_frame.pack(fill="x")
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack(fill="x", pady=(5, 0))
        
        tk.Button(btn_frame, text="➕ Add Group", font=('Segoe UI', 10, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self._add_test_group).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="🔄 Refresh", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self._load_test_groups).pack(side="left")
        
        self._load_test_groups()
    
    def _load_test_groups(self):
        """Load test step groups"""
        # Clear existing
        for widget in self.groups_scroll_frame.winfo_children():
            widget.destroy()
        
        groups = self.db_manager.get_test_step_groups()
        
        for i, group in enumerate(groups):
            group_id, group_name, description, step_count = group
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.groups_scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill='x')
            row_frame.pack_propagate(False)
            
            # Group name
            tk.Label(row_frame, text=group_name, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0, y=8, relwidth=0.3)
            
            # Description
            tk.Label(row_frame, text=description or '', font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.3, y=8, relwidth=0.4)
            
            # Step count
            tk.Label(row_frame, text=str(step_count), font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.7, y=8, relwidth=0.1)
            
            # Actions
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=5, relwidth=0.2, height=25)
            
            tk.Button(actions_frame, text="View", font=('Segoe UI', 8), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=6, pady=2, 
                     cursor='hand2', bd=0, command=lambda gid=group_id: self._view_group_steps(gid)).pack(side='left', padx=(0, 2))
            
            tk.Button(actions_frame, text="Edit", font=('Segoe UI', 8), 
                     bg='#10b981', fg='#ffffff', relief='flat', padx=6, pady=2, 
                     cursor='hand2', bd=0, command=lambda gid=group_id: self._edit_group(gid)).pack(side='left', padx=(0, 2))
            
            tk.Button(actions_frame, text="Delete", font=('Segoe UI', 8), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=6, pady=2, 
                     cursor='hand2', bd=0, command=lambda gid=group_id: self._delete_group(gid)).pack(side='left')
    
    def _add_test_group(self):
        """Add test group dialog"""
        popup = tk.Toplevel(self.root)
        popup.title("Add Test Group")
        center_dialog(popup, 400, 250)
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Group Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        name_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame, text="Description:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        desc_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        desc_entry.pack(fill="x", pady=(0, 20))
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_group():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            if not name:
                self.show_popup("Error", "Please enter a group name", "error")
                return
            
            try:
                self.db_manager.save_test_step_group(name, desc)
                popup.destroy()
                self._load_test_groups()
                self.show_popup("Success", f"Group '{name}' created successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to create group: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_group).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
    def _view_group_steps(self, group_id):
        """View steps in group with Add/Edit/Delete functionality"""
        # Get group name
        groups = self.db_manager.get_test_step_groups()
        group_name = next((g[1] for g in groups if g[0] == group_id), "Unknown")
        
        popup = tk.Toplevel(self.root)
        popup.title(f"Test Steps - {group_name}")
        center_dialog(popup, 700, 572)
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Header with Add button only
        header_frame = tk.Frame(frame, bg='#ffffff')
        header_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(header_frame, text=f"Test Steps - {group_name}", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(side='left')
        
        tk.Button(header_frame, text="➕ Add Step", font=('Segoe UI', 9, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=10, pady=4, 
                 cursor='hand2', bd=0, command=lambda: self._add_test_step(group_id, popup)).pack(side='right')
        
        # Steps container
        steps_container = tk.Frame(frame, bg='#ffffff')
        steps_container.pack(fill='both', expand=True, pady=(0, 10))
        
        # Headers
        headers_frame = tk.Frame(steps_container, bg='#e5e7eb', height=25)
        headers_frame.pack(fill='x')
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='center', padx=5).place(relx=0, y=5, relwidth=0.05)
        tk.Label(headers_frame, text="Step Name", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.05, y=5, relwidth=0.2)
        tk.Label(headers_frame, text="Type", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.25, y=5, relwidth=0.15)
        tk.Label(headers_frame, text="Click Type", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.4, y=5, relwidth=0.1)
        tk.Label(headers_frame, text="Selector", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.5, y=5, relwidth=0.15)
        tk.Label(headers_frame, text="Value", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.65, y=5, relwidth=0.15)
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 9, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=10).place(relx=0.8, y=5, relwidth=0.2)
        
        # Steps scroll frame
        self.steps_scroll_frame = tk.Frame(steps_container, bg='#ffffff')
        self.steps_scroll_frame.pack(fill='both', expand=True)
        
        # Store group_id for refresh and reset pagination
        self.current_group_id = group_id
        self.current_steps_page = 1
        self.steps_popup = popup
        
        # Records per page selector at bottom
        records_frame = tk.Frame(frame, bg='#ffffff')
        records_frame.pack(fill='x', pady=(10, 0))
        
        tk.Label(records_frame, text="Records per page:", font=('Segoe UI', 9), bg='#ffffff').pack(side='left', padx=(0, 5))
        
        records_var = tk.StringVar(value=str(self.steps_per_page))
        records_combo = ttk.Combobox(records_frame, textvariable=records_var, width=5, font=('Segoe UI', 9), state='readonly')
        records_combo['values'] = ['5', '10', '20', '50', '100']
        records_combo.pack(side='left')
        
        def change_records_per_page(*args):
            self.steps_per_page = int(records_var.get())
            self.current_steps_page = 1
            self._load_group_steps(group_id)
        
        records_combo.bind('<<ComboboxSelected>>', change_records_per_page)
        
        # Prevent form from minimizing
        popup.transient(self.root)
        popup.grab_set()
        
        self._load_group_steps(group_id)
        
        # Close button
        tk.Button(frame, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(pady=(10, 0))
    
    def _load_group_steps(self, group_id):
        """Load steps for a specific group with pagination"""
        # Clear existing steps
        for widget in self.steps_scroll_frame.winfo_children():
            widget.destroy()
        
        # Get all steps
        all_steps = self.db_manager.get_test_steps_by_group(group_id)
        
        # Pagination setup
        if not hasattr(self, 'current_steps_page'):
            self.current_steps_page = 1
        if not hasattr(self, 'steps_per_page'):
            self.steps_per_page = 10
        
        steps_per_page = self.steps_per_page
        total_steps = len(all_steps)
        total_pages = max(1, (total_steps + steps_per_page - 1) // steps_per_page)
        
        # Ensure current page is valid
        if self.current_steps_page > total_pages:
            self.current_steps_page = total_pages
        
        # Get steps for current page
        start_index = (self.current_steps_page - 1) * steps_per_page
        end_index = min(start_index + steps_per_page, total_steps)
        page_steps = all_steps[start_index:end_index]
        
        # Display steps
        for i, step in enumerate(page_steps):
            step_id, name, step_type, target, description = step
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.steps_scroll_frame, bg=bg_color, height=30)
            row_frame.pack(fill='x', pady=1)
            row_frame.pack_propagate(False)
            
            # Parse step data for display
            click_type, selector_type, value = self._parse_step_data(step_type, target, description)
            
            # Drag handle for reordering (leftmost column)
            drag_label = tk.Label(row_frame, text="⋮⋮", font=('Segoe UI', 10), 
                                bg=bg_color, fg='#6b7280', cursor='hand2', anchor='center')
            drag_label.place(relx=0, y=8, relwidth=0.05)
            
            # Bind drag events to the drag handle and row
            self._bind_drag_events(row_frame, step_id, i)
            
            # Step name
            name_label = tk.Label(row_frame, text=name, font=('Segoe UI', 8), 
                    bg=bg_color, fg='#374151', anchor='w', padx=10)
            name_label.place(relx=0.05, y=8, relwidth=0.2)
            self._add_tooltip(name_label, name)
            
            # Step type
            type_label = tk.Label(row_frame, text=step_type, font=('Segoe UI', 8), 
                    bg=bg_color, fg='#374151', anchor='w', padx=10)
            type_label.place(relx=0.25, y=8, relwidth=0.15)
            self._add_tooltip(type_label, step_type)
            
            # Click type (for Element Click steps)
            click_label = tk.Label(row_frame, text=click_type, font=('Segoe UI', 8), 
                    bg=bg_color, fg='#374151', anchor='w', padx=10)
            click_label.place(relx=0.4, y=8, relwidth=0.1)
            if click_type:
                self._add_tooltip(click_label, f"{click_type} Click")
            
            # Selector type
            selector_label = tk.Label(row_frame, text=selector_type, font=('Segoe UI', 8), 
                    bg=bg_color, fg='#374151', anchor='w', padx=10)
            selector_label.place(relx=0.5, y=8, relwidth=0.15)
            self._add_tooltip(selector_label, selector_type)
            
            # Value (truncated if too long)
            value_display = value[:15] + "..." if value and len(value) > 15 else value or ""
            value_label = tk.Label(row_frame, text=value_display, font=('Segoe UI', 8), 
                    bg=bg_color, fg='#374151', anchor='w', padx=10)
            value_label.place(relx=0.65, y=8, relwidth=0.15)
            if value:
                self._add_tooltip(value_label, value)
            
            # Actions (rightmost column)
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=4, relwidth=0.2, height=22)
            
            tk.Button(actions_frame, text="Edit", font=('Segoe UI', 7), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=2, pady=1, 
                     cursor='hand2', bd=0, command=lambda sid=step_id: self._edit_test_step(sid)).pack(side='left', padx=(0, 1))
            
            tk.Button(actions_frame, text="Dup", font=('Segoe UI', 7), 
                     bg='#8b5cf6', fg='#ffffff', relief='flat', padx=2, pady=1, 
                     cursor='hand2', bd=0, command=lambda sid=step_id: self._duplicate_test_step(sid)).pack(side='left', padx=(0, 1))
            
            tk.Button(actions_frame, text="Del", font=('Segoe UI', 7), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=2, pady=1, 
                     cursor='hand2', bd=0, command=lambda sid=step_id: self._delete_test_step(sid)).pack(side='left')
        
        # Add pagination controls if needed
        if total_pages > 1:
            self._add_steps_pagination(total_pages, total_steps)
    
    def _add_steps_pagination(self, total_pages, total_steps):
        """Add pagination controls for test steps"""
        pagination_frame = tk.Frame(self.steps_scroll_frame, bg='#ffffff', height=35)
        pagination_frame.pack(fill='x', pady=(10, 0))
        pagination_frame.pack_propagate(False)
        
        # Previous button
        prev_btn = tk.Button(pagination_frame, text="◀ Previous", font=('Segoe UI', 8), 
                            bg='#6b7280' if self.current_steps_page > 1 else '#d1d5db', 
                            fg='#ffffff', relief='flat', padx=8, pady=4, cursor='hand2', bd=0,
                            state='normal' if self.current_steps_page > 1 else 'disabled',
                            command=self._prev_steps_page)
        prev_btn.pack(side='left', padx=(0, 5))
        
        # Page info (no dropdown)
        page_frame = tk.Frame(pagination_frame, bg='#ffffff')
        page_frame.pack(side='left', padx=10)
        
        tk.Label(page_frame, text=f"Page {self.current_steps_page} of {total_pages} ({total_steps} steps)", 
                font=('Segoe UI', 8), bg='#ffffff', fg='#374151').pack(side='left')
        
        # Next button
        next_btn = tk.Button(pagination_frame, text="Next ▶", font=('Segoe UI', 8), 
                            bg='#6b7280' if self.current_steps_page < total_pages else '#d1d5db', 
                            fg='#ffffff', relief='flat', padx=8, pady=4, cursor='hand2', bd=0,
                            state='normal' if self.current_steps_page < total_pages else 'disabled',
                            command=self._next_steps_page)
        next_btn.pack(side='left', padx=(5, 0))
    
    def _prev_steps_page(self):
        """Go to previous page of test steps"""
        if self.current_steps_page > 1:
            self.current_steps_page -= 1
            self._load_group_steps(self.current_group_id)
    
    def _next_steps_page(self):
        """Go to next page of test steps"""
        self.current_steps_page += 1
        self._load_group_steps(self.current_group_id)
    
    def _bind_drag_events(self, row_frame, step_id, index):
        """Bind drag and drop events to drag handle only"""
        # Find the drag handle (first child should be the drag label)
        drag_handle = None
        for child in row_frame.winfo_children():
            if hasattr(child, 'cget') and child.cget('text') == '⋮⋮':
                drag_handle = child
                break
        
        if not drag_handle:
            return
        
        def on_drag_start(event):
            self.drag_data = {'step_id': step_id, 'source_index': index, 'widget': row_frame}
            row_frame.configure(bg='#e3f2fd')  # Highlight during drag
        
        def on_drag_motion(event):
            # Get mouse position relative to the steps container
            try:
                container_y = event.y_root - self.steps_scroll_frame.winfo_rooty()
                # Find which row we're over
                for i, child in enumerate(self.steps_scroll_frame.winfo_children()):
                    if hasattr(child, 'winfo_y'):
                        row_y = child.winfo_y()
                        row_height = child.winfo_height()
                        if row_y <= container_y <= row_y + row_height:
                            # We're over row i
                            if hasattr(self, 'drag_data'):
                                self.drag_data['target_index'] = i
                            break
            except:
                pass
        
        def on_drop(event):
            if hasattr(self, 'drag_data'):
                source_idx = self.drag_data['source_index']
                target_idx = self.drag_data.get('target_index', source_idx)
                
                if source_idx != target_idx:
                    self._reorder_steps(self.drag_data['step_id'], source_idx, target_idx)
                
                # Reset visual state - check if widget still exists
                try:
                    if self.drag_data['widget'].winfo_exists():
                        self.drag_data['widget'].configure(bg='#ffffff')
                except:
                    pass  # Widget was destroyed, ignore
                
                delattr(self, 'drag_data')
        
        # Bind events only to drag handle
        drag_handle.bind('<Button-1>', on_drag_start)
        drag_handle.bind('<B1-Motion>', on_drag_motion)
        drag_handle.bind('<ButtonRelease-1>', on_drop)
    
    def _reorder_steps(self, step_id, source_index, target_index):
        """Reorder steps by moving step from source to target position"""
        try:
            cursor = self.db_manager.conn.cursor()
            
            # Get all steps for this group
            all_steps = self.db_manager.get_test_steps_by_group(self.current_group_id)
            
            # Calculate actual indices considering pagination
            steps_per_page = 10
            page_offset = (self.current_steps_page - 1) * steps_per_page
            actual_source = page_offset + source_index
            actual_target = page_offset + target_index
            
            if actual_source == actual_target:
                return
            
            # Reorder the steps list
            step_to_move = all_steps[actual_source]
            all_steps.pop(actual_source)
            all_steps.insert(actual_target, step_to_move)
            
            # Update step_order in database
            for i, step in enumerate(all_steps):
                step_id_to_update = step[0]
                new_order = i + 1
                cursor.execute(
                    "UPDATE test_steps SET step_order = ? WHERE id = ? AND user_id = ?",
                    (new_order, step_id_to_update, self.db_manager.user_id)
                )
            
            self.db_manager.conn.commit()
            self._load_group_steps(self.current_group_id)
            
        except Exception as e:
            self.show_popup("Error", f"Failed to reorder steps: {str(e)}", "error")
    
    def _add_test_step(self, group_id, parent_popup):
        """Add test step - delegate to test_steps_methods"""
        from test_steps_methods import TestStepsMethods
        methods = TestStepsMethods()
        methods.db_manager = self.db_manager
        methods.show_popup = self.show_popup
        methods._load_group_steps = self._load_group_steps
        
        # Add selenium manager reference for step preview
        try:
            from selenium_manager import SeleniumManager
            methods.selenium_manager = SeleniumManager()
        except:
            methods.selenium_manager = None
            
        methods._add_test_step(group_id, parent_popup)
    
    def _edit_test_step(self, step_id):
        """Edit test step with dynamic form interface"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT name, step_type, target, description FROM test_steps WHERE id = ? AND user_id = ?", 
                      (step_id, self.db_manager.user_id))
        step_data = cursor.fetchone()
        
        if not step_data:
            self.show_popup("Error", "Test step not found", "error")
            return
        
        name, step_type, target, description = step_data
        
        # Use dynamic edit dialog
        from test_steps_methods import TestStepsMethods
        methods = TestStepsMethods()
        methods.db_manager = self.db_manager
        methods.show_popup = self.show_popup
        methods._load_group_steps = self._load_group_steps
        
        # Add selenium manager reference for enhanced element finding
        try:
            from selenium_manager import SeleniumManager
            methods.selenium_manager = SeleniumManager()
        except:
            methods.selenium_manager = None
            
        methods._edit_test_step(step_id, self.current_group_id, self.steps_popup)
    
    def _delete_test_step(self, step_id):
        """Delete test step with confirmation using consistent modal style"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT name FROM test_steps WHERE id = ? AND user_id = ?", (step_id, self.db_manager.user_id))
        step_data = cursor.fetchone()
        
        if not step_data:
            self.show_popup("Error", "Test step not found", "error")
            return
        
        step_name = step_data[0]
        
        # Use consistent modal style
        from selenium_tab_manager import center_dialog
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Confirm Delete")
        center_dialog(confirm_popup, 450, 250)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.transient(self.root)
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header with red background for delete confirmation
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🗑️ Delete Test Step", font=('Segoe UI', 12, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        tk.Label(content_frame, text=f"Are you sure you want to delete:", 
                font=('Segoe UI', 10), bg='#ffffff', fg='#374151').pack(pady=(0, 10))
        
        tk.Label(content_frame, text=f"'{step_name}'", 
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#ef4444').pack(pady=(0, 20))
        
        tk.Label(content_frame, text="This action cannot be undone.", 
                font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                cursor.execute("DELETE FROM test_steps WHERE id = ? AND user_id = ?", (step_id, self.db_manager.user_id))
                self.db_manager.conn.commit()
                confirm_popup.destroy()
                self._load_group_steps(self.current_group_id)
                self.show_popup("Success", f"Step '{step_name}' deleted!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Delete", font=('Segoe UI', 10, 'bold'), 
                 bg='#ef4444', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
    
    def _parse_step_data(self, step_type, target, description):
        """Parse step data to extract display fields"""
        click_type = ""
        selector_type = ""
        value = ""
        
        if step_type == 'Element Click':
            if '[RIGHT-CLICK]' in target:
                click_type = "Right"
                clean_target = target.replace(' [RIGHT-CLICK]', '')
            elif '[DOUBLE-CLICK]' in target:
                click_type = "Double"
                clean_target = target.replace(' [DOUBLE-CLICK]', '')
            else:
                click_type = "Left"
                clean_target = target
            
            if clean_target.startswith('#'):
                selector_type = "ID"
                value = clean_target[1:]
            elif clean_target.startswith('.'):
                selector_type = "Class"
                value = clean_target[1:]
            elif clean_target.startswith('//'):
                selector_type = "XPath"
                value = clean_target
            elif '[name=' in clean_target or '[id=' in clean_target or '[class=' in clean_target:
                selector_type = "XPath"
                value = clean_target
            else:
                selector_type = "CSS"
                value = clean_target
                
        elif step_type == 'Text Input':
            selector_type = "Input"
            value = description or target
            
        elif step_type == 'Navigate':
            selector_type = "URL"
            value = target
            
        elif step_type == 'Wait':
            if ':' in target:
                wait_type, wait_value = target.split(':', 1)
                selector_type = wait_type.strip()
                value = wait_value.strip()
            else:
                selector_type = "Time"
                value = target
        else:
            selector_type = step_type[:8]
            value = target
        
        return click_type, selector_type, value
    
    def _add_tooltip(self, widget, text):
        """Add hover tooltip to widget"""
        if not text or len(text) <= 15:
            return  # No tooltip needed for short text
        
        def on_enter(event):
            # Create tooltip
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.configure(bg='#2d3748')
            
            # Position tooltip near mouse
            x = event.x_root + 10
            y = event.y_root - 25
            tooltip.geometry(f"+{x}+{y}")
            
            # Tooltip content
            label = tk.Label(tooltip, text=text, font=('Segoe UI', 9), 
                           bg='#2d3748', fg='#ffffff', padx=8, pady=4, 
                           wraplength=300, justify='left')
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
    
    def _duplicate_test_step(self, step_id):
        """Duplicate test step"""
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT name, step_type, target, description, group_id FROM test_steps WHERE id = ? AND user_id = ?", 
                          (step_id, self.db_manager.user_id))
            step_data = cursor.fetchone()
            
            if not step_data:
                self.show_popup("Error", "Test step not found", "error")
                return
            
            name, step_type, target, description, group_id = step_data
            new_name = f"{name} (Copy)"
            
            cursor.execute("SELECT COALESCE(MAX(step_order), 0) + 1 FROM test_steps WHERE user_id = ? AND group_id = ?", 
                          (self.db_manager.user_id, group_id))
            next_order = cursor.fetchone()[0]
            
            rice_profiles = self.db_manager.get_rice_profiles()
            rice_profile_id = rice_profiles[0][0] if rice_profiles else 1
            
            cursor.execute("INSERT INTO test_steps (user_id, rice_profile_id, name, step_type, target, description, group_id, step_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                          (self.db_manager.user_id, rice_profile_id, new_name, step_type, target, description, group_id, next_order))
            
            self.db_manager.conn.commit()
            self._load_group_steps(self.current_group_id)
            self.show_popup("Success", f"Step '{new_name}' duplicated successfully!", "success")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to duplicate step: {str(e)}", "error")
    
    def _edit_group(self, group_id):
        """Edit test group with consistent modal styling"""
        groups = self.db_manager.get_test_step_groups()
        group_data = next((g for g in groups if g[0] == group_id), None)
        
        if not group_data:
            self.show_popup("Error", "Group not found", "error")
            return
        
        _, group_name, description, _ = group_data
        
        from selenium_tab_manager import center_dialog
        popup = tk.Toplevel(self.root)
        popup.title("Edit Test Group")
        center_dialog(popup, 450, 300)
        popup.configure(bg='#ffffff')
        popup.transient(self.root)
        popup.grab_set()
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header with blue background for edit
        header_frame = tk.Frame(popup, bg='#3b82f6', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✏️ Edit Test Group", font=('Segoe UI', 12, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(popup, bg='#ffffff', padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        tk.Label(content_frame, text="Group Name:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(content_frame, width=40, font=('Segoe UI', 10), 
                             relief='solid', bd=1, highlightthickness=1)
        name_entry.insert(0, group_name)
        name_entry.pack(fill="x", pady=(0, 15))
        
        tk.Label(content_frame, text="Description:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor="w", pady=(0, 5))
        desc_entry = tk.Entry(content_frame, width=40, font=('Segoe UI', 10), 
                             relief='solid', bd=1, highlightthickness=1)
        desc_entry.insert(0, description or '')
        desc_entry.pack(fill="x", pady=(0, 25))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_desc = desc_entry.get().strip()
            
            if not new_name:
                self.show_popup("Error", "Please enter a group name", "error")
                return
            
            try:
                self.db_manager.save_test_step_group(new_name, new_desc, group_id)
                popup.destroy()
                self._load_test_groups()
                self.show_popup("Success", f"Group '{new_name}' updated!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save Changes", font=('Segoe UI', 10, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
    def _delete_group(self, group_id):
        """Delete test group with confirmation using consistent modal style"""
        groups = self.db_manager.get_test_step_groups()
        group_data = next((g for g in groups if g[0] == group_id), None)
        
        if not group_data:
            self.show_popup("Error", "Group not found", "error")
            return
        
        group_name = group_data[1]
        step_count = group_data[3]
        
        from selenium_tab_manager import center_dialog
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Confirm Delete")
        center_dialog(confirm_popup, 500, 280)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.transient(self.root)
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header with red background for delete confirmation
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🗑️ Delete Test Group", font=('Segoe UI', 12, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=30, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        tk.Label(content_frame, text="Are you sure you want to delete:", 
                font=('Segoe UI', 10), bg='#ffffff', fg='#374151').pack(pady=(0, 10))
        
        tk.Label(content_frame, text=f"'{group_name}'", 
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#ef4444').pack(pady=(0, 10))
        
        if step_count > 0:
            tk.Label(content_frame, text=f"This will also delete {step_count} test steps.", 
                    font=('Segoe UI', 10), bg='#ffffff', fg='#f59e0b').pack(pady=(0, 10))
        
        tk.Label(content_frame, text="This action cannot be undone.", 
                font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                self.db_manager.delete_test_step_group(group_id)
                confirm_popup.destroy()
                self._load_test_groups()
                self.show_popup("Success", f"Group '{group_name}' deleted!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Delete Group", font=('Segoe UI', 10, 'bold'), 
                 bg='#ef4444', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
