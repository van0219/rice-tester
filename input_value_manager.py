#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from rice_dialogs import center_dialog

class InputValueManager:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def edit_input_value(self, scenario_id, step_name, current_value, refresh_callback):
        """Edit input value for Text Input step"""
        popup = tk.Toplevel()
        popup.title("Edit Input Value")
        center_dialog(popup, 400, 250)
        popup.configure(bg='#ffffff')
        popup.grab_set()
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text=f"Step: {step_name}", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(pady=(0, 10))
        
        is_password = 'password' in step_name.lower()
        value_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10), show="•" if is_password else "")
        value_entry.insert(0, current_value)
        value_entry.pack(fill="x", pady=(0, 15))
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_value():
            new_value = value_entry.get()
            cursor = self.db_manager.conn.cursor()
            cursor.execute("UPDATE scenario_steps SET step_description = ? WHERE step_name = ?", 
                          (new_value, step_name))
            self.db_manager.conn.commit()
            popup.destroy()
            if refresh_callback:
                refresh_callback()
        
        tk.Button(btn_frame, text="Save", bg='#10b981', fg='#ffffff', command=save_value).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", bg='#6b7280', fg='#ffffff', command=popup.destroy).pack(side="left")
        
        value_entry.focus()
    
    def create_edit_button(self, parent, step_name, current_value, refresh_callback):
        """Create edit button for Text Input steps"""
        return tk.Button(parent, text="✏️", font=('Segoe UI', 8), bg='#3b82f6', fg='#ffffff', 
                        relief='flat', padx=4, pady=2, cursor='hand2', bd=0,
                        command=lambda: self.edit_input_value(None, step_name, current_value, refresh_callback))
