#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from rice_dialogs import center_dialog

class ScenarioEditValue:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def edit_step_value(self, popup, step_data, index, update_display_callback, steps_listbox):
        """Edit input value for Text Input and Wait steps"""
        # Check if step can be edited
        if step_data['type'] == 'Text Input':
            can_edit = True
            edit_type = 'text'
        elif step_data['type'] == 'Wait':
            can_edit = True
            # Determine wait type from target
            target = step_data.get('target', '')
            if target and ('Element Visible:' in target or 'Element Clickable:' in target):
                edit_type = 'wait_selector'
            else:
                edit_type = 'wait_time'
        else:
            can_edit = False
        
        if not can_edit:
            self._show_cannot_edit_popup(popup)
            return
        
        # Create edit value dialog
        edit_popup = tk.Toplevel(popup)
        edit_popup.title("Edit Input Value")
        center_dialog(edit_popup, 400, 250)
        edit_popup.configure(bg='#ffffff')
        edit_popup.transient(popup)
        edit_popup.grab_set()
        
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
            
            # Determine if this is a password field
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
        elif edit_type == 'wait_selector':
            tk.Label(edit_frame, text="Element Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
            tk.Label(edit_frame, text="Enter CSS selector (#id, .class) or XPath (//...)", 
                    font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(anchor="w", pady=(0, 5))
            
            value_entry = tk.Entry(edit_frame, width=40, font=('Segoe UI', 10))
            current_value = step_data.get('description', '')
            value_entry.insert(0, current_value)
            value_entry.pack(fill="x", pady=(0, 20))
        
        edit_btn_frame = tk.Frame(edit_frame, bg='#ffffff')
        edit_btn_frame.pack()
        
        def save_value():
            new_value = value_entry.get().strip()
            
            # Validate based on edit type
            if edit_type == 'wait_time':
                try:
                    wait_seconds = float(new_value)
                    if wait_seconds <= 0:
                        self.show_popup("Error", "Wait time must be greater than 0 seconds", "error")
                        return
                except ValueError:
                    self.show_popup("Error", "Please enter a valid number for wait time", "error")
                    return
            elif edit_type == 'wait_selector':
                if not new_value:
                    self.show_popup("Error", "Please enter a selector", "error")
                    return
            
            # Store the value in description field for consistency
            step_data['description'] = new_value
            
            # Update display
            update_display_callback()
            steps_listbox.selection_set(index)
            
            edit_popup.destroy()
        
        tk.Button(edit_btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_value).pack(side="left", padx=(0, 10))
        tk.Button(edit_btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=edit_popup.destroy).pack(side="left")
        
        value_entry.focus()
        value_entry.select_range(0, tk.END)
    
    def _show_cannot_edit_popup(self, parent_popup):
        """Show info popup for non-editable steps"""
        info_popup = tk.Toplevel(parent_popup)
        info_popup.title("Info")
        center_dialog(info_popup, 320, 180)
        info_popup.configure(bg='#ffffff')
        info_popup.attributes('-topmost', True)
        info_popup.resizable(False, False)
        info_popup.transient(parent_popup)
        info_popup.grab_set()
        
        try:
            info_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(info_popup, bg='#f59e0b', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Info", font=('Segoe UI', 12, 'bold'), 
                bg='#f59e0b', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(info_popup, bg='#ffffff', padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Only Text Input steps and Wait steps can have their values edited", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center", wraplength=280).pack(pady=(0, 15))
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=6, cursor='hand2', bd=0, command=info_popup.destroy).pack()
        
        info_popup.focus_set()