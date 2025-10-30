#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from selenium_tab_manager import center_dialog

class TestUsersManager:
    def __init__(self, root, db_manager, show_popup_callback):
        self.root = root
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def setup_test_users_tab(self, parent):
        """Test users tab"""
        frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Header
        tk.Label(frame, text="Test Users", font=('Segoe UI', 12, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 10))
        
        # Headers
        headers_frame = tk.Frame(frame, bg='#e5e7eb', height=25)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="Name", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0, y=5, relwidth=0.25)
        tk.Label(headers_frame, text="Email", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.25, y=5, relwidth=0.35)
        tk.Label(headers_frame, text="Password", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.6, y=5, relwidth=0.2)
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.8, y=5, relwidth=0.2)
        
        # Users scroll frame
        self.users_scroll_frame = tk.Frame(frame, bg='#ffffff')
        self.users_scroll_frame.pack(fill="x", pady=(0, 10))
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="➕ Add User", font=('Segoe UI', 10, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self._add_test_user).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="🔄 Refresh", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self._load_test_users).pack(side="left")
        
        self._load_test_users()
    
    def _load_test_users(self):
        """Load test users"""
        for widget in self.users_scroll_frame.winfo_children():
            widget.destroy()
        
        users = self.db_manager.get_test_users()
        
        for i, user in enumerate(users):
            user_id, name, email, password = user
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.users_scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill='x')
            row_frame.pack_propagate(False)
            
            tk.Label(row_frame, text=name, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0, y=8, relwidth=0.25)
            tk.Label(row_frame, text=email, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.25, y=8, relwidth=0.35)
            tk.Label(row_frame, text="••••••••", font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.6, y=8, relwidth=0.2)
            
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=5, relwidth=0.2, height=25)
            
            tk.Button(actions_frame, text="Edit", font=('Segoe UI', 8), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=6, pady=2, 
                     cursor='hand2', bd=0, command=lambda uid=user_id: self._edit_user(uid)).pack(side='left', padx=(0, 2))
            tk.Button(actions_frame, text="Delete", font=('Segoe UI', 8), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=6, pady=2, 
                     cursor='hand2', bd=0, command=lambda uid=user_id: self._delete_user(uid)).pack(side='left')
    
    def _add_test_user(self):
        """Add test user dialog"""
        popup = tk.Toplevel(self.root)
        popup.title("Add Test User")
        center_dialog(popup, 400, 300)
        popup.configure(bg='#ffffff')
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        name_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame, text="Email:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        email_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        email_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame, text="Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        password_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10), show="•")
        password_entry.pack(fill="x", pady=(0, 20))
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_user():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            
            if not all([name, email, password]):
                self.show_popup("Error", "Please fill in all fields", "error")
                return
            
            try:
                self.db_manager.save_test_user(name, email, password)
                popup.destroy()
                self._load_test_users()
                self.show_popup("Success", f"User '{name}' created successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to create user: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_user).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
    def _edit_user(self, user_id):
        """Edit test user"""
        users = self.db_manager.get_test_users()
        user_data = next((u for u in users if u[0] == user_id), None)
        
        if not user_data:
            self.show_popup("Error", "User not found", "error")
            return
        
        _, name, email, encrypted_password = user_data
        password = self.db_manager.decrypt_password(encrypted_password)
        
        popup = tk.Toplevel(self.root)
        popup.title("Edit Test User")
        center_dialog(popup, 400, 300)
        popup.configure(bg='#ffffff')
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        name_entry.insert(0, name)
        name_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame, text="Email:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        email_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        email_entry.insert(0, email)
        email_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame, text="Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        password_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10), show="•")
        password_entry.insert(0, password)
        password_entry.pack(fill="x", pady=(0, 20))
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            new_password = password_entry.get().strip()
            
            if not all([new_name, new_email, new_password]):
                self.show_popup("Error", "Please fill in all fields", "error")
                return
            
            try:
                self.db_manager.save_test_user(new_name, new_email, new_password, user_id)
                popup.destroy()
                self._load_test_users()
                self.show_popup("Success", f"User '{new_name}' updated successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update user: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
        name_entry.select_range(0, tk.END)
    
    def _delete_user(self, user_id):
        """Delete test user with confirmation"""
        users = self.db_manager.get_test_users()
        user_data = next((u for u in users if u[0] == user_id), None)
        
        if not user_data:
            self.show_popup("Error", "User not found", "error")
            return
        
        user_name = user_data[1]
        
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Confirm Delete")
        center_dialog(confirm_popup, 400, 250)
        confirm_popup.configure(bg='#ffffff')
        
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🗑️ Delete Test User", font=('Segoe UI', 14, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message = f"Delete test user '{user_name}'?\n\nThis action cannot be undone."
        tk.Label(content_frame, text=message, font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                self.db_manager.delete_test_user(user_id)
                confirm_popup.destroy()
                self._load_test_users()
                self.show_popup("Success", f"Test user '{user_name}' deleted successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete user: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
