#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from enhanced_popup_system import EnhancedPopupManager

class TestUsersManager:
    def __init__(self, root, db_manager, show_popup_callback):
        self.root = root
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.popup_manager = EnhancedPopupManager()
    
    def setup_test_users_tab(self, parent):
        """Modern test users tab with card-based design"""
        # Main container with light background
        main_container = tk.Frame(parent, bg='#f8fafc')
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern card container
        card_frame = tk.Frame(main_container, bg='#ffffff', relief='solid', bd=1,
                             highlightbackground='#e5e7eb', highlightthickness=1)
        card_frame.pack(fill="both", expand=True)
        
        # Professional header with integrated controls
        header_frame = tk.Frame(card_frame, bg='#8b5cf6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg='#8b5cf6')
        header_content.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(header_content, text="👤 Test Users", 
                font=('Segoe UI', 12, 'bold'), bg='#8b5cf6', fg='#ffffff').pack(side="left")
        
        # Header controls
        controls_frame = tk.Frame(header_content, bg='#8b5cf6')
        controls_frame.pack(side="right")
        
        tk.Button(controls_frame, text="＋ Add User", 
                 font=('Segoe UI', 9, 'bold'), bg='#7c3aed', fg='#ffffff',
                 relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                 command=self._add_test_user).pack(side='left', padx=(0, 5))
        
        tk.Button(controls_frame, text="⟲ Refresh", 
                 font=('Segoe UI', 9, 'bold'), bg='#7c3aed', fg='#ffffff',
                 relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                 command=self._load_test_users).pack(side='left')
        
        # Content container
        content_container = tk.Frame(card_frame, bg='#ffffff')
        content_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Modern table headers with icons
        headers_frame = tk.Frame(content_container, bg='#f3f4f6', height=35, relief='solid', bd=1)
        headers_frame.pack(fill="x", pady=(10, 0))
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="👤 Name", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0, y=8, relwidth=0.30)
        tk.Label(headers_frame, text="📧 Email", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.30, y=8, relwidth=0.35)
        tk.Label(headers_frame, text="🔒 Password", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.65, y=8, relwidth=0.15)
        tk.Label(headers_frame, text="⚙️ Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='center').place(relx=0.80, y=8, relwidth=0.20)
        
        # Users scroll frame with modern styling
        scroll_container = tk.Frame(content_container, bg='#ffffff', relief='solid', bd=1)
        scroll_container.pack(fill="both", expand=True, pady=(0, 10))
        
        self.users_scroll_frame = tk.Frame(scroll_container, bg='#ffffff')
        self.users_scroll_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self._load_test_users()
    
    def _load_test_users(self):
        """Load test users with modern table design"""
        for widget in self.users_scroll_frame.winfo_children():
            widget.destroy()
        
        users = self.db_manager.get_test_users()
        
        if not users:
            # Empty state
            empty_frame = tk.Frame(self.users_scroll_frame, bg='#ffffff', height=120)
            empty_frame.pack(fill='x', pady=10)
            empty_frame.pack_propagate(False)
            
            content_frame = tk.Frame(empty_frame, bg='#ffffff')
            content_frame.pack(expand=True)
            
            tk.Label(content_frame, text="👤", font=('Segoe UI', 24), bg='#ffffff', fg='#9ca3af').pack(pady=(0, 5))
            tk.Label(content_frame, text="No Test Users Found", font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#374151').pack()
            tk.Label(content_frame, text="Add test users to enable login step automation", 
                    font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(pady=(3, 0))
            return
        
        for i, user in enumerate(users):
            user_id, name, email, password = user
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.users_scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill='x')
            row_frame.pack_propagate(False)
            
            # Enhanced hover effects
            def on_enter(e, frame=row_frame, original_bg=bg_color):
                frame.config(bg='#f8fafc')
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg='#f8fafc')
                    elif isinstance(child, tk.Frame):
                        child.config(bg='#f8fafc')
            
            def on_leave(e, frame=row_frame, original_bg=bg_color):
                frame.config(bg=original_bg)
                for child in frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(bg=original_bg)
                    elif isinstance(child, tk.Frame):
                        child.config(bg=original_bg)
            
            row_frame.bind('<Enter>', on_enter)
            row_frame.bind('<Leave>', on_leave)
            
            # Name
            tk.Label(row_frame, text=name, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0, y=8, relwidth=0.30)
            
            # Email
            tk.Label(row_frame, text=email, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.30, y=8, relwidth=0.35)
            
            # Password (masked)
            tk.Label(row_frame, text="••••••••", font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.65, y=8, relwidth=0.15)
            
            # Actions with modern button styling
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.80, y=4, relwidth=0.20, height=27)
            
            # Center container for buttons
            center_frame = tk.Frame(actions_frame, bg=bg_color)
            center_frame.pack(expand=True)
            
            edit_btn = tk.Button(center_frame, text="✏ Edit", font=('Segoe UI', 8, 'bold'), 
                               bg='#3b82f6', fg='#ffffff', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0,
                               command=lambda uid=user_id: self._edit_user(uid))
            edit_btn.pack(side='left', padx=(0, 3))
            
            delete_btn = tk.Button(center_frame, text="× Delete", font=('Segoe UI', 8, 'bold'), 
                                 bg='#ef4444', fg='#ffffff', relief='flat', 
                                 padx=4, pady=1, cursor='hand2', bd=0,
                                 command=lambda uid=user_id: self._delete_user(uid))
            delete_btn.pack(side='left')
            
            # Column separators
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.30, y=2, height=31)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.65, y=2, height=31)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.80, y=2, height=31)
    
    def _add_test_user(self):
        """Modern add test user dialog"""
        dialog = self.popup_manager.create_dynamic_dialog(
            parent=self.root,
            title="Add Test User",
            width=500,
            height=400,
            resizable=True
        )
        
        # Header
        header_frame = tk.Frame(dialog, bg='#8b5cf6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="👤 Add Test User", 
                font=('Segoe UI', 14, 'bold'), bg='#8b5cf6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(dialog, bg='#ffffff', padx=30, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Configure grid
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Name field
        tk.Label(content_frame, text="👤 Name *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(0, 15))
        
        name_entry = tk.Entry(content_frame, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                             relief='solid', bd=1, highlightthickness=2, 
                             highlightcolor='#8b5cf6', highlightbackground='#d1d5db')
        name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 15), ipady=8)
        
        # Email field
        tk.Label(content_frame, text="📧 Email *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').grid(row=1, column=0, sticky="w", pady=(0, 5), padx=(0, 15))
        
        email_entry = tk.Entry(content_frame, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                              relief='solid', bd=1, highlightthickness=2, 
                              highlightcolor='#8b5cf6', highlightbackground='#d1d5db')
        email_entry.grid(row=1, column=1, sticky="ew", pady=(0, 15), ipady=8)
        
        # Password field with toggle
        tk.Label(content_frame, text="🔒 Password *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').grid(row=2, column=0, sticky="w", pady=(0, 5), padx=(0, 15))
        
        password_container = tk.Frame(content_frame, bg='#f9fafb', relief='solid', bd=1,
                                     highlightthickness=2, highlightcolor='#8b5cf6',
                                     highlightbackground='#d1d5db')
        password_container.grid(row=2, column=1, sticky="ew", pady=(0, 20))
        
        password_entry = tk.Entry(password_container, show="•", font=('Segoe UI', 11),
                                 bg='#f9fafb', fg='#1f2937', relief='flat', bd=0,
                                 highlightthickness=0)
        password_entry.pack(fill="both", expand=True, ipady=8, padx=(10, 35))
        
        # Toggle button
        password_visible = [False]
        toggle_btn = tk.Button(password_container, text="👁️", font=('Segoe UI', 9),
                              bg='#f9fafb', fg='#6b7280', relief='flat', bd=0,
                              padx=4, pady=0, cursor='hand2')
        toggle_btn.place(relx=1.0, rely=0.5, anchor='e', x=-8, width=25, height=20)
        
        def toggle_password():
            if password_visible[0]:
                password_entry.configure(show="•")
                toggle_btn.configure(text="👁️")
                password_visible[0] = False
            else:
                password_entry.configure(show="")
                toggle_btn.configure(text="🙈")
                password_visible[0] = True
        
        toggle_btn.configure(command=toggle_password)
        
        # Focus effects
        def add_focus_effects(entry, container=None):
            def on_focus_in(e):
                if container:
                    container.configure(highlightbackground='#8b5cf6', bg='#ffffff')
                    entry.configure(bg='#ffffff')
                else:
                    entry.configure(highlightbackground='#8b5cf6', bg='#ffffff')
            
            def on_focus_out(e):
                if container:
                    container.configure(highlightbackground='#d1d5db', bg='#f9fafb')
                    entry.configure(bg='#f9fafb')
                else:
                    entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        add_focus_effects(name_entry)
        add_focus_effects(email_entry)
        add_focus_effects(password_entry, password_container)
        
        # Action buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        def save_user():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            
            if not all([name, email, password]):
                self.popup_manager.show_error("Validation Error", "Please fill in all required fields", parent=dialog)
                return
            
            try:
                self.db_manager.save_test_user(name, email, password)
                dialog.destroy()
                self._load_test_users()
                self.popup_manager.show_success("Success", f"Test user '{name}' created successfully!")
            except Exception as e:
                self.popup_manager.show_error("Error", f"Failed to create user: {str(e)}", parent=dialog)
        
        tk.Button(btn_frame, text="✓ Save User", font=('Segoe UI', 10, 'bold'), 
                 bg='#8b5cf6', fg='#ffffff', relief='flat', padx=16, pady=8, 
                 cursor='hand2', bd=0, command=save_user).pack(side="left", padx=(0, 15))
        
        tk.Button(btn_frame, text="× Cancel", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=16, pady=8, 
                 cursor='hand2', bd=0, command=dialog.destroy).pack(side="left")
        
        name_entry.focus()
    
    def _edit_user(self, user_id):
        """Modern edit test user dialog"""
        users = self.db_manager.get_test_users()
        user_data = next((u for u in users if u[0] == user_id), None)
        
        if not user_data:
            self.popup_manager.show_error("Error", "User not found")
            return
        
        _, name, email, encrypted_password = user_data
        password = self.db_manager.decrypt_password(encrypted_password)
        
        dialog = self.popup_manager.create_dynamic_dialog(
            parent=self.root,
            title="Edit Test User",
            width=500,
            height=400,
            resizable=True
        )
        
        # Header
        header_frame = tk.Frame(dialog, bg='#f59e0b', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✏️ Edit Test User", 
                font=('Segoe UI', 14, 'bold'), bg='#f59e0b', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(dialog, bg='#ffffff', padx=30, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Configure grid
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Name field
        tk.Label(content_frame, text="👤 Name *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').grid(row=0, column=0, sticky="w", pady=(0, 5), padx=(0, 15))
        
        name_entry = tk.Entry(content_frame, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                             relief='solid', bd=1, highlightthickness=2, 
                             highlightcolor='#f59e0b', highlightbackground='#d1d5db')
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=1, sticky="ew", pady=(0, 15), ipady=8)
        
        # Email field
        tk.Label(content_frame, text="📧 Email *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').grid(row=1, column=0, sticky="w", pady=(0, 5), padx=(0, 15))
        
        email_entry = tk.Entry(content_frame, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                              relief='solid', bd=1, highlightthickness=2, 
                              highlightcolor='#f59e0b', highlightbackground='#d1d5db')
        email_entry.insert(0, email)
        email_entry.grid(row=1, column=1, sticky="ew", pady=(0, 15), ipady=8)
        
        # Password field with toggle
        tk.Label(content_frame, text="🔒 Password *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').grid(row=2, column=0, sticky="w", pady=(0, 5), padx=(0, 15))
        
        password_container = tk.Frame(content_frame, bg='#f9fafb', relief='solid', bd=1,
                                     highlightthickness=2, highlightcolor='#f59e0b',
                                     highlightbackground='#d1d5db')
        password_container.grid(row=2, column=1, sticky="ew", pady=(0, 20))
        
        password_entry = tk.Entry(password_container, show="•", font=('Segoe UI', 11),
                                 bg='#f9fafb', fg='#1f2937', relief='flat', bd=0,
                                 highlightthickness=0)
        password_entry.insert(0, password)
        password_entry.pack(fill="both", expand=True, ipady=8, padx=(10, 35))
        
        # Toggle button
        password_visible = [False]
        toggle_btn = tk.Button(password_container, text="👁️", font=('Segoe UI', 9),
                              bg='#f9fafb', fg='#6b7280', relief='flat', bd=0,
                              padx=4, pady=0, cursor='hand2')
        toggle_btn.place(relx=1.0, rely=0.5, anchor='e', x=-8, width=25, height=20)
        
        def toggle_password():
            if password_visible[0]:
                password_entry.configure(show="•")
                toggle_btn.configure(text="👁️")
                password_visible[0] = False
            else:
                password_entry.configure(show="")
                toggle_btn.configure(text="🙈")
                password_visible[0] = True
        
        toggle_btn.configure(command=toggle_password)
        
        # Focus effects
        def add_focus_effects(entry, container=None):
            def on_focus_in(e):
                if container:
                    container.configure(highlightbackground='#f59e0b', bg='#ffffff')
                    entry.configure(bg='#ffffff')
                else:
                    entry.configure(highlightbackground='#f59e0b', bg='#ffffff')
            
            def on_focus_out(e):
                if container:
                    container.configure(highlightbackground='#d1d5db', bg='#f9fafb')
                    entry.configure(bg='#f9fafb')
                else:
                    entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
        
        add_focus_effects(name_entry)
        add_focus_effects(email_entry)
        add_focus_effects(password_entry, password_container)
        
        # Action buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_email = email_entry.get().strip()
            new_password = password_entry.get().strip()
            
            if not all([new_name, new_email, new_password]):
                self.popup_manager.show_error("Validation Error", "Please fill in all required fields", parent=dialog)
                return
            
            try:
                self.db_manager.save_test_user(new_name, new_email, new_password, user_id)
                dialog.destroy()
                self._load_test_users()
                self.popup_manager.show_success("Success", f"Test user '{new_name}' updated successfully!")
            except Exception as e:
                self.popup_manager.show_error("Error", f"Failed to update user: {str(e)}", parent=dialog)
        
        tk.Button(btn_frame, text="✓ Update User", font=('Segoe UI', 10, 'bold'), 
                 bg='#f59e0b', fg='#ffffff', relief='flat', padx=16, pady=8, 
                 cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 15))
        
        tk.Button(btn_frame, text="× Cancel", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=16, pady=8, 
                 cursor='hand2', bd=0, command=dialog.destroy).pack(side="left")
        
        name_entry.focus()
        name_entry.select_range(0, tk.END)
    
    def _delete_user(self, user_id):
        """Modern delete test user confirmation"""
        users = self.db_manager.get_test_users()
        user_data = next((u for u in users if u[0] == user_id), None)
        
        if not user_data:
            self.popup_manager.show_error("Error", "User not found")
            return
        
        user_name = user_data[1]
        
        dialog = self.popup_manager.create_dynamic_dialog(
            parent=self.root,
            title="Delete Test User",
            width=450,
            height=280,
            resizable=False
        )
        
        # Header
        header_frame = tk.Frame(dialog, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🗑️ Delete Test User", 
                font=('Segoe UI', 14, 'bold'), bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(dialog, bg='#ffffff', padx=30, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message = f"Are you sure you want to delete test user:\n'{user_name}'?\n\nThis action cannot be undone and will affect\nany scenarios using this test user."
        tk.Label(content_frame, text=message, font=('Segoe UI', 10), 
                bg='#ffffff', fg='#374151', justify="center").pack(pady=(0, 20))
        
        # Action buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                self.db_manager.delete_test_user(user_id)
                dialog.destroy()
                self._load_test_users()
                self.popup_manager.show_success("Success", f"Test user '{user_name}' deleted successfully!")
            except Exception as e:
                self.popup_manager.show_error("Error", f"Failed to delete user: {str(e)}", parent=dialog)
        
        tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), 
                 bg='#ef4444', fg='#ffffff', relief='flat', padx=16, pady=8, 
                 cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 15))
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=16, pady=8, 
                 cursor='hand2', bd=0, command=dialog.destroy).pack(side="left")
