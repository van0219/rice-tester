#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import json

class BulkOperationsManager:
    """Bulk operations for test steps - Phase 3 advanced features"""
    
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.selected_steps = []
    
    def show_bulk_operations(self, parent, group_id, callback):
        """Show bulk operations interface"""
        self.group_id = group_id
        self.callback = callback
        
        dialog = tk.Toplevel(parent)
        dialog.title("⚡ Bulk Operations")
        dialog.configure(bg='#ffffff')
        dialog.geometry("800x600")
        dialog.resizable(True, True)
        dialog.minsize(700, 500)
        dialog.transient(parent)
        dialog.grab_set()
        
        try:
            dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced header
        header_frame = tk.Frame(dialog, bg='#6366f1', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#6366f1')
        header_content.pack(fill='both', expand=True, padx=25, pady=20)
        
        title_frame = tk.Frame(header_content, bg='#6366f1')
        title_frame.pack(side='left')
        
        tk.Label(title_frame, text="⚡ Bulk Operations", 
                font=('Segoe UI', 16, 'bold'), bg='#6366f1', fg='#ffffff').pack(anchor='w')
        tk.Label(title_frame, text="Manage multiple test steps efficiently", 
                font=('Segoe UI', 10), bg='#6366f1', fg='#c7d2fe').pack(anchor='w')
        
        # Selection count
        self.selection_count = tk.Label(header_content, text="0 selected", 
                                       font=('Segoe UI', 12, 'bold'), bg='#6366f1', fg='#ffffff')
        self.selection_count.pack(side='right')
        
        # Main content
        main_frame = tk.Frame(dialog, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Left panel - step selection
        left_panel = tk.Frame(main_frame, bg='#f8fafc', relief='solid', bd=1)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Steps header
        steps_header = tk.Frame(left_panel, bg='#e5e7eb', height=40)
        steps_header.pack(fill='x')
        steps_header.pack_propagate(False)
        
        steps_header_content = tk.Frame(steps_header, bg='#e5e7eb')
        steps_header_content.pack(fill='both', expand=True, padx=15, pady=10)
        
        tk.Label(steps_header_content, text="📋 Select Steps", font=('Segoe UI', 12, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(side='left')
        
        # Select all/none buttons
        select_frame = tk.Frame(steps_header_content, bg='#e5e7eb')
        select_frame.pack(side='right')
        
        tk.Button(select_frame, text="✅ All", font=('Segoe UI', 8, 'bold'),
                 bg='#10b981', fg='#ffffff', relief='flat', padx=8, pady=2,
                 cursor='hand2', bd=0, command=self.select_all).pack(side='left', padx=(0, 5))
        
        tk.Button(select_frame, text="❌ None", font=('Segoe UI', 8, 'bold'),
                 bg='#ef4444', fg='#ffffff', relief='flat', padx=8, pady=2,
                 cursor='hand2', bd=0, command=self.select_none).pack(side='left')
        
        # Steps list with checkboxes
        self.steps_container = tk.Frame(left_panel, bg='#f8fafc')
        self.steps_container.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Right panel - operations
        right_panel = tk.Frame(main_frame, bg='#ffffff', width=300)
        right_panel.pack(side='right', fill='y')
        right_panel.pack_propagate(False)
        
        # Operations header
        ops_header = tk.Frame(right_panel, bg='#ffffff')
        ops_header.pack(fill='x', pady=(0, 15))
        
        tk.Label(ops_header, text="🛠️ Available Operations", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor='w')
        
        # Operation categories
        self.create_operation_category(right_panel, "📝 Modify", [
            ("🔄 Reorder Steps", self.reorder_steps),
            ("✏️ Batch Edit", self.batch_edit),
            ("📋 Duplicate Selected", self.duplicate_selected),
            ("🏷️ Add Tags", self.add_tags)
        ])
        
        self.create_operation_category(right_panel, "📊 Organize", [
            ("📁 Move to Group", self.move_to_group),
            ("🔗 Create Sequence", self.create_sequence),
            ("📋 Export Steps", self.export_steps),
            ("📥 Import Steps", self.import_steps)
        ])
        
        self.create_operation_category(right_panel, "🗑️ Cleanup", [
            ("❌ Delete Selected", self.delete_selected),
            ("🧹 Remove Duplicates", self.remove_duplicates),
            ("⚠️ Find Issues", self.find_issues),
            ("🔧 Auto-Fix", self.auto_fix)
        ])
        
        # Bottom buttons
        bottom_frame = tk.Frame(dialog, bg='#ffffff')
        bottom_frame.pack(fill='x', padx=25, pady=(0, 25))
        
        tk.Button(bottom_frame, text="💾 Apply Changes", font=('Segoe UI', 11, 'bold'),
                 bg='#10b981', fg='#ffffff', relief='flat', padx=20, pady=10,
                 cursor='hand2', bd=0, command=self.apply_changes).pack(side='left', padx=(0, 10))
        
        tk.Button(bottom_frame, text="❌ Close", font=('Segoe UI', 11, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10,
                 cursor='hand2', bd=0, command=dialog.destroy).pack(side='right')
        
        self.dialog = dialog
        self.step_vars = {}
        
        # Load steps
        self.load_steps()
    
    def create_operation_category(self, parent, title, operations):
        """Create operation category section"""
        category_frame = tk.Frame(parent, bg='#f8fafc', relief='solid', bd=1)
        category_frame.pack(fill='x', pady=(0, 15))
        
        # Category header
        cat_header = tk.Frame(category_frame, bg='#e5e7eb', height=30)
        cat_header.pack(fill='x')
        cat_header.pack_propagate(False)
        
        tk.Label(cat_header, text=title, font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        # Operations
        ops_content = tk.Frame(category_frame, bg='#f8fafc')
        ops_content.pack(fill='x', padx=10, pady=10)
        
        for op_name, op_func in operations:
            op_btn = tk.Button(ops_content, text=op_name, font=('Segoe UI', 9, 'bold'),
                              bg='#ffffff', fg='#374151', relief='solid', bd=1,
                              anchor='w', padx=10, pady=6, cursor='hand2',
                              command=op_func)
            op_btn.pack(fill='x', pady=2)
            
            # Hover effects
            def on_enter(e, btn=op_btn):
                btn.configure(bg='#e5e7eb')
            def on_leave(e, btn=op_btn):
                btn.configure(bg='#ffffff')
            
            op_btn.bind('<Enter>', on_enter)
            op_btn.bind('<Leave>', on_leave)
    
    def load_steps(self):
        """Load steps for selection"""
        # Clear existing
        for widget in self.steps_container.winfo_children():
            widget.destroy()
        
        self.step_vars.clear()
        
        # Get steps from database
        steps = self.db_manager.get_test_steps_by_group(self.group_id)
        
        if not steps:
            tk.Label(self.steps_container, text="No steps in this group", 
                    font=('Segoe UI', 12), bg='#f8fafc', fg='#6b7280').pack(expand=True)
            return
        
        for i, step in enumerate(steps):
            step_id, name, step_type, target, description = step
            
            step_frame = tk.Frame(self.steps_container, bg='#ffffff' if i % 2 == 0 else '#f9fafb',
                                 relief='solid', bd=1)
            step_frame.pack(fill='x', pady=1)
            
            # Checkbox and step info
            content_frame = tk.Frame(step_frame, bg=step_frame['bg'])
            content_frame.pack(fill='x', padx=10, pady=8)
            
            # Checkbox
            var = tk.BooleanVar()
            self.step_vars[step_id] = var
            
            checkbox = tk.Checkbutton(content_frame, variable=var, bg=step_frame['bg'],
                                     command=self.update_selection_count)
            checkbox.pack(side='left', padx=(0, 10))
            
            # Step info
            info_frame = tk.Frame(content_frame, bg=step_frame['bg'])
            info_frame.pack(side='left', fill='x', expand=True)
            
            # Step name and type
            name_frame = tk.Frame(info_frame, bg=step_frame['bg'])
            name_frame.pack(fill='x')
            
            tk.Label(name_frame, text=name, font=('Segoe UI', 10, 'bold'), 
                    bg=step_frame['bg'], fg='#374151', anchor='w').pack(side='left')
            
            tk.Label(name_frame, text=f"({step_type})", font=('Segoe UI', 9), 
                    bg=step_frame['bg'], fg='#6b7280').pack(side='right')
            
            # Target/description
            if target:
                target_display = target[:50] + "..." if len(target) > 50 else target
                tk.Label(info_frame, text=f"Target: {target_display}", font=('Segoe UI', 8), 
                        bg=step_frame['bg'], fg='#6b7280', anchor='w').pack(fill='x')
    
    def update_selection_count(self):
        """Update selection count display"""
        selected_count = sum(1 for var in self.step_vars.values() if var.get())
        self.selection_count.config(text=f"{selected_count} selected")
    
    def select_all(self):
        """Select all steps"""
        for var in self.step_vars.values():
            var.set(True)
        self.update_selection_count()
    
    def select_none(self):
        """Deselect all steps"""
        for var in self.step_vars.values():
            var.set(False)
        self.update_selection_count()
    
    def get_selected_steps(self):
        """Get list of selected step IDs"""
        return [step_id for step_id, var in self.step_vars.items() if var.get()]
    
    # Operation implementations
    def reorder_steps(self):
        """Reorder selected steps"""
        selected = self.get_selected_steps()
        if len(selected) < 2:
            self.show_popup("Selection Error", "Please select at least 2 steps to reorder", "error")
            return
        
        self.show_popup("Feature", "Step reordering interface coming soon!", "info")
    
    def batch_edit(self):
        """Batch edit selected steps"""
        selected = self.get_selected_steps()
        if not selected:
            self.show_popup("Selection Error", "Please select steps to edit", "error")
            return
        
        # Create batch edit dialog
        edit_dialog = tk.Toplevel(self.dialog)
        edit_dialog.title("✏️ Batch Edit")
        edit_dialog.configure(bg='#ffffff')
        edit_dialog.geometry("500x400")
        edit_dialog.transient(self.dialog)
        
        try:
            edit_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(edit_dialog, bg='#10b981', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"✏️ Batch Edit ({len(selected)} steps)", 
                font=('Segoe UI', 14, 'bold'), bg='#10b981', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(edit_dialog, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Edit options
        tk.Label(content_frame, text="Select fields to modify:", font=('Segoe UI', 11, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 10))
        
        # Field options
        fields_frame = tk.Frame(content_frame, bg='#ffffff')
        fields_frame.pack(fill='x', pady=(0, 15))
        
        self.edit_name = tk.BooleanVar()
        self.edit_description = tk.BooleanVar()
        self.edit_type = tk.BooleanVar()
        
        tk.Checkbutton(fields_frame, text="Step Name Prefix/Suffix", variable=self.edit_name,
                      font=('Segoe UI', 10), bg='#ffffff').pack(anchor='w', pady=2)
        tk.Checkbutton(fields_frame, text="Description", variable=self.edit_description,
                      font=('Segoe UI', 10), bg='#ffffff').pack(anchor='w', pady=2)
        tk.Checkbutton(fields_frame, text="Step Type", variable=self.edit_type,
                      font=('Segoe UI', 10), bg='#ffffff').pack(anchor='w', pady=2)
        
        # Input fields
        inputs_frame = tk.Frame(content_frame, bg='#ffffff')
        inputs_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        tk.Label(inputs_frame, text="Name Prefix:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff').pack(anchor='w')
        self.name_prefix = tk.Entry(inputs_frame, font=('Segoe UI', 10))
        self.name_prefix.pack(fill='x', pady=(2, 10))
        
        tk.Label(inputs_frame, text="Description:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff').pack(anchor='w')
        self.batch_description = tk.Entry(inputs_frame, font=('Segoe UI', 10))
        self.batch_description.pack(fill='x', pady=(2, 10))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(fill='x')
        
        tk.Button(btn_frame, text="💾 Apply Changes", font=('Segoe UI', 10, 'bold'),
                 bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=lambda: self.apply_batch_edit(selected, edit_dialog)).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="❌ Cancel", font=('Segoe UI', 10, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=edit_dialog.destroy).pack(side='left')
    
    def apply_batch_edit(self, selected_steps, dialog):
        """Apply batch edit changes"""
        try:
            cursor = self.db_manager.conn.cursor()
            changes_made = 0
            
            for step_id in selected_steps:
                updates = []
                values = []
                
                if self.edit_name.get() and self.name_prefix.get().strip():
                    # Get current name
                    cursor.execute("SELECT name FROM test_steps WHERE id = ? AND user_id = ?", 
                                  (step_id, self.db_manager.user_id))
                    current_name = cursor.fetchone()[0]
                    new_name = f"{self.name_prefix.get().strip()} {current_name}"
                    updates.append("name = ?")
                    values.append(new_name)
                
                if self.edit_description.get() and self.batch_description.get().strip():
                    updates.append("description = ?")
                    values.append(self.batch_description.get().strip())
                
                if updates:
                    values.append(step_id)
                    values.append(self.db_manager.user_id)
                    
                    query = f"UPDATE test_steps SET {', '.join(updates)} WHERE id = ? AND user_id = ?"
                    cursor.execute(query, values)
                    changes_made += 1
            
            self.db_manager.conn.commit()
            dialog.destroy()
            
            if changes_made > 0:
                self.show_popup("Success", f"✨ Updated {changes_made} steps successfully!", "success")
                if self.callback:
                    self.callback(self.group_id)
            else:
                self.show_popup("No Changes", "No changes were made", "warning")
                
        except Exception as e:
            self.show_popup("Error", f"Failed to apply batch edit: {str(e)}", "error")
    
    def duplicate_selected(self):
        """Duplicate selected steps"""
        selected = self.get_selected_steps()
        if not selected:
            self.show_popup("Selection Error", "Please select steps to duplicate", "error")
            return
        
        try:
            cursor = self.db_manager.conn.cursor()
            duplicated = 0
            
            for step_id in selected:
                # Get step data
                cursor.execute("SELECT name, step_type, target, description, rice_profile_id FROM test_steps WHERE id = ? AND user_id = ?", 
                              (step_id, self.db_manager.user_id))
                step_data = cursor.fetchone()
                
                if step_data:
                    name, step_type, target, description, rice_profile_id = step_data
                    new_name = f"{name} (Copy)"
                    
                    # Get next order
                    cursor.execute("SELECT COALESCE(MAX(step_order), 0) + 1 FROM test_steps WHERE user_id = ? AND group_id = ?", 
                                  (self.db_manager.user_id, self.group_id))
                    next_order = cursor.fetchone()[0]
                    
                    # Insert duplicate
                    cursor.execute("INSERT INTO test_steps (user_id, rice_profile_id, name, step_type, target, description, group_id, step_order) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                                  (self.db_manager.user_id, rice_profile_id, new_name, step_type, target, description, self.group_id, next_order))
                    duplicated += 1
            
            self.db_manager.conn.commit()
            
            if duplicated > 0:
                self.show_popup("Success", f"✨ Duplicated {duplicated} steps successfully!", "success")
                self.load_steps()  # Refresh the list
                if self.callback:
                    self.callback(self.group_id)
            
        except Exception as e:
            self.show_popup("Error", f"Failed to duplicate steps: {str(e)}", "error")
    
    def delete_selected(self):
        """Delete selected steps"""
        selected = self.get_selected_steps()
        if not selected:
            self.show_popup("Selection Error", "Please select steps to delete", "error")
            return
        
        # Confirmation dialog
        confirm_dialog = tk.Toplevel(self.dialog)
        confirm_dialog.title("⚠️ Confirm Deletion")
        confirm_dialog.configure(bg='#ffffff')
        confirm_dialog.geometry("400x250")
        confirm_dialog.transient(self.dialog)
        confirm_dialog.grab_set()
        
        try:
            confirm_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(confirm_dialog, bg='#ef4444', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Confirm Deletion", font=('Segoe UI', 14, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_dialog, bg='#ffffff', padx=25, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        tk.Label(content_frame, text=f"Are you sure you want to delete {len(selected)} selected steps?", 
                font=('Segoe UI', 11), bg='#ffffff', fg='#374151').pack(pady=(0, 10))
        
        tk.Label(content_frame, text="This action cannot be undone.", 
                font=('Segoe UI', 10), bg='#ffffff', fg='#ef4444').pack(pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                cursor = self.db_manager.conn.cursor()
                for step_id in selected:
                    cursor.execute("DELETE FROM test_steps WHERE id = ? AND user_id = ?", 
                                  (step_id, self.db_manager.user_id))
                
                self.db_manager.conn.commit()
                confirm_dialog.destroy()
                
                self.show_popup("Success", f"✨ Deleted {len(selected)} steps successfully!", "success")
                self.load_steps()  # Refresh the list
                if self.callback:
                    self.callback(self.group_id)
                    
            except Exception as e:
                self.show_popup("Error", f"Failed to delete steps: {str(e)}", "error")
        
        tk.Button(btn_frame, text="🗑️ Delete", font=('Segoe UI', 10, 'bold'),
                 bg='#ef4444', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=confirm_delete).pack(side='left', padx=(0, 10))
        
        tk.Button(btn_frame, text="❌ Cancel", font=('Segoe UI', 10, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=confirm_dialog.destroy).pack(side='left')
    
    # Placeholder methods for other operations
    def add_tags(self):
        self.show_popup("Feature", "Step tagging system coming soon!", "info")
    
    def move_to_group(self):
        self.show_popup("Feature", "Move to group functionality coming soon!", "info")
    
    def create_sequence(self):
        self.show_popup("Feature", "Step sequence creation coming soon!", "info")
    
    def export_steps(self):
        self.show_popup("Feature", "Step export functionality coming soon!", "info")
    
    def import_steps(self):
        self.show_popup("Feature", "Step import functionality coming soon!", "info")
    
    def remove_duplicates(self):
        self.show_popup("Feature", "Duplicate detection coming soon!", "info")
    
    def find_issues(self):
        self.show_popup("Feature", "Issue detection coming soon!", "info")
    
    def auto_fix(self):
        self.show_popup("Feature", "Auto-fix functionality coming soon!", "info")
    
    def apply_changes(self):
        """Apply all pending changes"""
        self.show_popup("Success", "All changes have been applied!", "success")
        self.dialog.destroy()