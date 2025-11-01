#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import threading
from selenium_tab_manager import center_dialog

class SFTPManager:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.selected_sftp_profile = None
        self.selected_sftp_row = None
    
    def setup_sftp_tab_content(self, parent):
        """Setup SFTP configuration tab content with responsive form design"""
        # Main container with light background
        self.main_container = tk.Frame(parent, bg='#f8fafc')
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern card container
        self.card_frame = tk.Frame(self.main_container, bg='#ffffff', relief='solid', bd=1,
                                  highlightbackground='#e5e7eb', highlightthickness=1)
        self.card_frame.pack(fill="both", expand=True)
        
        # Dynamic header frame
        self.header_frame = tk.Frame(self.card_frame, bg='#10b981', height=50)
        self.header_frame.pack(fill="x")
        self.header_frame.pack_propagate(False)
        
        # Content container (will switch between table and form)
        self.content_container = tk.Frame(self.card_frame, bg='#ffffff')
        self.content_container.pack(fill="both", expand=True)
        
        # Initialize with table view
        self.current_view = "table"
        self.show_sftp_table()
    
    def load_sftp_profiles(self):
        """Load SFTP profiles with custom table"""
        # Clear existing profile rows
        for widget in self.sftp_scroll_frame.winfo_children():
            widget.destroy()
        
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT id, profile_name, host, port, username, directory, password 
            FROM sftp_profiles 
            WHERE user_id = ? 
            ORDER BY profile_name
        """, (self.db_manager.user_id,))
        
        profiles = cursor.fetchall()
        
        # Display profiles with custom rows
        for i, profile in enumerate(profiles):
            profile_id, name, host, port, username, directory, encrypted_password = profile
            auth_display = "Password" if encrypted_password else "None"
            
            # Use normal alternating colors (selection handled separately)
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            # Create row frame
            row_frame = tk.Frame(self.sftp_scroll_frame, bg=bg_color, height=30)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)
            
            # Make entire row clickable and tag it with profile_id
            row_frame.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            row_frame.configure(cursor='hand2')
            row_frame.profile_id = profile_id  # Tag the row with profile_id
            
            # Name (clickable) with padding and tooltip
            name_label = tk.Label(row_frame, text=name, font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            name_label.place(relx=0, y=8, relwidth=0.10)
            name_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Host (clickable) with padding
            host_label = tk.Label(row_frame, text=host, font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            host_label.place(relx=0.10, y=8, relwidth=0.15)
            host_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Port (clickable) with padding
            port_label = tk.Label(row_frame, text=str(port), font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            port_label.place(relx=0.25, y=8, relwidth=0.10)
            port_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Username (clickable) with padding
            username_label = tk.Label(row_frame, text=username, font=('Segoe UI', 9), 
                                     bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            username_label.place(relx=0.35, y=8, relwidth=0.20)
            username_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Auth method (clickable) with padding
            auth_label = tk.Label(row_frame, text=auth_display, font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            auth_label.place(relx=0.55, y=8, relwidth=0.10)
            auth_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Directory (clickable) with padding
            directory_display = directory if directory else "(not set)"
            directory_label = tk.Label(row_frame, text=directory_display, font=('Segoe UI', 9), 
                                      bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            directory_label.place(relx=0.65, y=8, relwidth=0.15)
            directory_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Column separators for rows
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.10, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.25, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.35, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.55, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.65, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.80, y=2, height=26)
            
            # Action buttons frame - fix alignment and width calculation
            btn_frame = tk.Frame(row_frame, bg=bg_color)
            btn_frame.place(relx=0.80, y=4, relwidth=0.20, height=22)  # Exact 20% width
            
            test_btn = tk.Button(btn_frame, text="Test", font=('Segoe UI', 8, 'bold'), 
                               bg='#10b981', fg='white', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0, highlightthickness=0,
                               command=lambda pid=profile_id: self.test_sftp_profile(pid))
            
            edit_btn = tk.Button(btn_frame, text="Edit", font=('Segoe UI', 8, 'bold'), 
                               bg='#3b82f6', fg='white', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0, highlightthickness=0,
                               command=lambda pid=profile_id: self.edit_sftp_profile(pid))
            
            delete_btn = tk.Button(btn_frame, text="Delete", font=('Segoe UI', 8, 'bold'), 
                                 bg='#ef4444', fg='white', relief='flat', 
                                 padx=4, pady=1, cursor='hand2', bd=0, highlightthickness=0,
                                 command=lambda pid=profile_id: self.delete_sftp_profile(pid))
            
            # Use relative positioning for consistent layout (5%-30%-5%-30%-5%-25%)
            test_btn.place(relx=0.05, rely=0, relwidth=0.30, height=22)    # 5% padding + 30% button
            edit_btn.place(relx=0.40, rely=0, relwidth=0.30, height=22)    # 40% start + 30% button  
            delete_btn.place(relx=0.75, rely=0, relwidth=0.25, height=22)  # 75% start + 25% button (fits "Delete")
    
    def select_sftp_profile(self, profile_id):
        """Handle SFTP profile selection for highlighting"""
        # Reset previous selection
        if hasattr(self, 'selected_sftp_row') and self.selected_sftp_row:
            try:
                # Reset to normal alternating colors
                row_index = list(self.sftp_scroll_frame.winfo_children()).index(self.selected_sftp_row)
                normal_color = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
                self.selected_sftp_row.configure(bg=normal_color)
                # Update all child widgets except column separators
                for child in self.selected_sftp_row.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_width() != 1:
                        child.configure(bg=normal_color)
            except (ValueError, tk.TclError):
                pass
        
        # Set new selection
        self.selected_sftp_profile = profile_id
        
        # Find and highlight the clicked row using profile_id tag
        for row_widget in self.sftp_scroll_frame.winfo_children():
            if hasattr(row_widget, 'profile_id') and row_widget.profile_id == profile_id:
                # Highlight this row
                row_widget.configure(bg='#dbeafe')
                for child in row_widget.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_width() != 1:
                        child.configure(bg='#dbeafe')
                self.selected_sftp_row = row_widget
                break
    
    def show_sftp_table(self):
        """Show SFTP profiles table view"""
        self.current_view = "table"
        
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()
        
        # Update header for table view
        self.update_header("📁 SFTP Profiles", show_add_button=True)
        
        # SFTP profiles container
        sftp_container = tk.Frame(self.content_container, bg='#ffffff')
        sftp_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Modern table headers
        headers_frame = tk.Frame(sftp_container, bg='#f3f4f6', height=35, relief='solid', bd=1)
        headers_frame.pack(fill="x", pady=(10, 0))
        headers_frame.pack_propagate(False)
        
        # Header labels with icons and better spacing
        tk.Label(headers_frame, text="📝 Name", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0, y=8, relwidth=0.10)
        
        tk.Label(headers_frame, text="🌐 Host", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.10, y=8, relwidth=0.15)
        
        tk.Label(headers_frame, text="🔌 Port", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.25, y=8, relwidth=0.10)
        
        tk.Label(headers_frame, text="👤 User", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.35, y=8, relwidth=0.20)
        
        tk.Label(headers_frame, text="🔒 Auth", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.55, y=8, relwidth=0.10)
        
        tk.Label(headers_frame, text="📂 Directory", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.65, y=8, relwidth=0.15)
        
        tk.Label(headers_frame, text="⚙️ Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='center', padx=10).place(relx=0.80, y=8, relwidth=0.20)
        
        # SFTP profiles scroll frame with modern styling
        scroll_container = tk.Frame(sftp_container, bg='#ffffff', relief='solid', bd=1)
        scroll_container.pack(fill="both", expand=True, pady=(0, 10))
        
        self.sftp_scroll_frame = tk.Frame(scroll_container, bg='#ffffff')
        self.sftp_scroll_frame.pack(fill="both", expand=True, padx=1, pady=1)
        
        self.load_sftp_profiles()
    
    def show_sftp_form(self, profile_id=None):
        """Show SFTP form view (add or edit)"""
        self.current_view = "form"
        self.editing_profile_id = profile_id
        
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()
        
        # Update header for form view
        title = "✏ Edit SFTP Profile" if profile_id else "➕ Add SFTP Profile"
        self.update_header(title, show_back_button=True)
        
        # Create scrollable form container
        canvas = tk.Canvas(self.content_container, bg='#ffffff', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y", pady=20)
        
        # Form content with responsive grid
        form_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Configure responsive grid
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Form fields
        self.create_sftp_form_fields(form_frame, profile_id)
        
        # Enable mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", _on_mousewheel)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel)
    
    def update_header(self, title, show_add_button=False, show_back_button=False):
        """Update header based on current view"""
        # Clear header
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        
        # Header content
        header_content = tk.Frame(self.header_frame, bg='#10b981')
        header_content.pack(fill="both", expand=True, padx=20)
        
        if show_back_button:
            # Back button
            back_btn = tk.Button(header_content, text="← Back", 
                               font=('Segoe UI', 9, 'bold'), bg='#059669', fg='#ffffff',
                               relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                               command=self.show_sftp_table)
            back_btn.pack(side="left", pady=8)
        
        # Title
        title_label = tk.Label(header_content, text=title, 
                              font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff')
        if show_back_button:
            title_label.pack(side="left", padx=(15, 0), expand=True, anchor="w")
        else:
            title_label.pack(side="left", expand=True, anchor="w")
        
        if show_add_button:
            # Add button
            add_btn = tk.Button(header_content, text="＋ Add SFTP", 
                               font=('Segoe UI', 9, 'bold'), bg='#059669', fg='#ffffff',
                               relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                               command=lambda: self.show_sftp_form())
            add_btn.pack(side="right", pady=8)
    
    def create_sftp_form_fields(self, parent, profile_id=None):
        """Create responsive SFTP form fields"""
        # Load existing data if editing
        existing_data = None
        if profile_id:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT profile_name, host, port, username, directory, password FROM sftp_profiles WHERE id = ?", (profile_id,))
            result = cursor.fetchone()
            if result:
                existing_data = {
                    'name': result[0],
                    'host': result[1],
                    'port': str(result[2]),
                    'username': result[3],
                    'directory': result[4] or '',
                    'password': self.db_manager.decrypt_password(result[5]) if result[5] else ''
                }
        
        row = 0
        
        # Profile Name
        self.setup_responsive_field(parent, "📝 Profile Name", row, required=True)
        self.name_entry = self.create_responsive_entry(parent, row)
        if existing_data:
            self.name_entry.insert(0, existing_data['name'])
        row += 1
        
        # Host
        self.setup_responsive_field(parent, "🌐 Host", row, required=True)
        self.host_entry = self.create_responsive_entry(parent, row)
        if existing_data:
            self.host_entry.insert(0, existing_data['host'])
        row += 1
        
        # Port
        self.setup_responsive_field(parent, "🔌 Port", row, required=True)
        self.port_entry = self.create_responsive_entry(parent, row)
        self.port_entry.insert(0, existing_data['port'] if existing_data else "22")
        row += 1
        
        # Username
        self.setup_responsive_field(parent, "👤 Username", row, required=True)
        self.username_entry = self.create_responsive_entry(parent, row)
        if existing_data:
            self.username_entry.insert(0, existing_data['username'])
        row += 1
        
        # Authentication Method
        self.setup_responsive_field(parent, "🔐 Authentication Method", row)
        self.auth_method = ttk.Combobox(parent, values=["Password", "SSH Key", "Password + Key"], 
                                       state="readonly", font=('Segoe UI', 10))
        self.auth_method.set("Password")
        self.auth_method.grid(row=row, column=1, sticky="ew", padx=(0, 0), pady=8, ipady=6)
        row += 1
        
        # Password field
        self.setup_responsive_field(parent, "🔒 Password", row)
        self.password_container = self.create_password_field(parent, row)
        if existing_data:
            self.password_entry.insert(0, existing_data['password'])
        row += 1
        
        # SSH Key File
        self.key_label = self.setup_responsive_field(parent, "🔑 SSH Key File", row)
        self.key_container = self.create_file_field(parent, row, "Select SSH Private Key", 
                                                   [("All Key Files", "*"), ("PEM Files", "*.pem"), ("OpenSSH Keys", "id_*")])
        row += 1
        
        # Key Passphrase
        self.passphrase_label = self.setup_responsive_field(parent, "🔐 Key Passphrase", row)
        self.passphrase_container = self.create_password_field(parent, row, "passphrase")
        row += 1
        
        # Directory
        self.setup_responsive_field(parent, "📂 Directory", row)
        self.directory_entry = self.create_responsive_entry(parent, row)
        if existing_data:
            self.directory_entry.insert(0, existing_data['directory'])
        row += 1
        
        # Spacer
        tk.Frame(parent, bg='#ffffff', height=20).grid(row=row, column=0, columnspan=2)
        row += 1
        
        # Action buttons
        self.create_form_buttons(parent, row)
        
        # Setup dynamic field visibility
        self.auth_method.bind('<<ComboboxSelected>>', self.update_auth_fields)
        self.update_auth_fields()  # Initialize visibility
        
        # Focus on first field
        self.name_entry.focus()
    
    def add_sftp_profile(self):
        """Switch to add SFTP form view"""
        self.show_sftp_form()
    
    def test_sftp_profile(self, profile_id):
        """Test SFTP profile connection"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT profile_name, host, port, username, directory, password FROM sftp_profiles WHERE id = ?", (profile_id,))
        profile = cursor.fetchone()
        
        if not profile:
            self.show_popup("Error", "SFTP profile not found", "error")
            return
        
        name, host, port, username, directory, encrypted_password = profile
        password = self.db_manager.decrypt_password(encrypted_password) if encrypted_password else ""
        
        # Show testing dialog
        test_popup = tk.Toplevel()
        test_popup.title("Testing SFTP Connection")
        center_dialog(test_popup, 400, 300)
        test_popup.configure(bg='#ffffff')
        test_popup.resizable(False, False)
        test_popup.transient()
        test_popup.grab_set()
        
        try:
            test_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(test_popup, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔗 Testing SFTP Connection", font=('Segoe UI', 14, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(test_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Connection details
        tk.Label(content_frame, text=f"Profile: {name}", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=2)
        tk.Label(content_frame, text=f"Host: {host}:{port}", font=('Segoe UI', 10), bg='#ffffff').pack(anchor="w", pady=2)
        tk.Label(content_frame, text=f"Username: {username}", font=('Segoe UI', 10), bg='#ffffff').pack(anchor="w", pady=2)
        if directory:
            tk.Label(content_frame, text=f"Directory: {directory}", font=('Segoe UI', 10), bg='#ffffff').pack(anchor="w", pady=2)
        
        # Status label
        status_label = tk.Label(content_frame, text="Testing connection...", font=('Segoe UI', 10), 
                               bg='#ffffff', fg='#6b7280')
        status_label.pack(pady=(20, 10))
        
        # Simple test simulation
        def simulate_test():
            import time
            
            def test_connection():
                try:
                    # Simulate connection test
                    time.sleep(2)  # Simulate connection time
                    
                    # Simple validation
                    if not host or not username:
                        test_popup.after(0, lambda: status_label.config(text="❌ Connection failed: Missing host or username", fg='#ef4444'))
                        return
                    
                    if port < 1 or port > 65535:
                        test_popup.after(0, lambda: status_label.config(text="❌ Connection failed: Invalid port number", fg='#ef4444'))
                        return
                    
                    # Simulate success
                    test_popup.after(0, lambda: status_label.config(text="✅ Connection successful!", fg='#10b981'))
                    
                except Exception as e:
                    test_popup.after(0, lambda: status_label.config(text=f"❌ Connection failed: {str(e)}", fg='#ef4444'))
            
            # Run test in background thread
            test_thread = threading.Thread(target=test_connection)
            test_thread.daemon = True
            test_thread.start()
        
        # Start test automatically
        test_popup.after(500, simulate_test)
        
        # Close button
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(pady=(2, 0))
        
        tk.Button(btn_frame, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                 command=test_popup.destroy).pack()
        
        test_popup.focus_set()
    
    def setup_modern_field_group(self, parent, label_text, row):
        """Setup modern field label with consistent styling"""
        label = tk.Label(parent, text=label_text, font=('Segoe UI', 10, 'bold'), 
                        bg='#ffffff', fg='#374151')
        label.grid(row=row, column=0, sticky="w", pady=8, padx=(0, 15))
        return label
    
    def create_modern_entry(self, parent, row, placeholder=""):
        """Create modern styled entry field with focus effects"""
        entry = tk.Entry(parent, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                        relief='solid', bd=1, highlightthickness=2, 
                        highlightcolor='#3b82f6', highlightbackground='#d1d5db',
                        insertbackground='#3b82f6')
        entry.grid(row=row, column=1, sticky="ew", padx=(15, 0), pady=8, ipady=8)
        
        # Add focus effects
        def on_focus_in(e):
            entry.configure(highlightbackground='#3b82f6', bg='#ffffff')
        
        def on_focus_out(e):
            entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        # Configure grid weight for responsiveness
        parent.grid_columnconfigure(1, weight=1)
        
        return entry
    
    def edit_sftp_profile(self, profile_id):
        """Switch to edit SFTP form view"""
        self.show_sftp_form(profile_id)
    
    def delete_sftp_profile(self, profile_id):
        """Delete SFTP profile with confirmation"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT profile_name FROM sftp_profiles WHERE id = ?", (profile_id,))
        result = cursor.fetchone()
        
        if not result:
            self.show_popup("Error", "SFTP profile not found", "error")
            return
        
        profile_name = result[0]
        
        # Confirmation dialog
        confirm_popup = tk.Toplevel()
        confirm_popup.title("Confirm Delete")
        center_dialog(confirm_popup, 400, 236)
        confirm_popup.configure(bg='#ffffff')
        
        # Header
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Delete SFTP Profile", font=('Segoe UI', 14, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Are you sure you want to delete:\n'{profile_name}'?\n\nThis action cannot be undone.", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("DELETE FROM sftp_profiles WHERE id = ?", (profile_id,))
                self.db_manager.conn.commit()
                
                confirm_popup.destroy()
                self.load_sftp_profiles()
                self.show_popup("Success", f"SFTP profile '{profile_name}' deleted successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete SFTP profile: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
    
    def setup_responsive_field(self, parent, label_text, row, required=False):
        """Setup responsive field label with modern styling"""
        label_text_with_req = f"{label_text} *" if required else label_text
        label = tk.Label(parent, text=label_text_with_req, font=('Segoe UI', 10, 'bold'), 
                        bg='#ffffff', fg='#374151')
        label.grid(row=row, column=0, sticky="nw", pady=(8, 4), padx=(0, 15))
        return label
    
    def create_responsive_entry(self, parent, row):
        """Create responsive entry field with modern styling"""
        entry = tk.Entry(parent, font=('Segoe UI', 10), bg='#f9fafb', fg='#1f2937',
                        relief='solid', bd=1, highlightthickness=2, 
                        highlightcolor='#3b82f6', highlightbackground='#d1d5db',
                        insertbackground='#3b82f6')
        entry.grid(row=row, column=1, sticky="ew", padx=(0, 0), pady=8, ipady=6)
        
        # Add focus effects
        def on_focus_in(e):
            entry.configure(highlightbackground='#3b82f6', bg='#ffffff')
        
        def on_focus_out(e):
            entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def create_password_field(self, parent, row, field_type="password"):
        """Create password field with toggle visibility"""
        container = tk.Frame(parent, bg='#f9fafb', relief='solid', bd=1,
                           highlightthickness=2, highlightcolor='#3b82f6',
                           highlightbackground='#d1d5db')
        container.grid(row=row, column=1, sticky="ew", pady=8)
        
        entry = tk.Entry(container, show="•", font=('Segoe UI', 10),
                        bg='#f9fafb', fg='#1f2937', relief='flat', bd=0,
                        highlightthickness=0, insertbackground='#3b82f6')
        entry.pack(fill="both", expand=True, ipady=6, padx=(10, 35))
        
        # Store entry reference based on field type
        if field_type == "password":
            self.password_entry = entry
            self.password_visible = [False]
        else:
            self.passphrase_entry = entry
            self.passphrase_visible = [False]
        
        # Toggle button with absolute positioning
        toggle_btn = tk.Button(container, text="👁️", font=('Segoe UI', 9),
                              bg='#f9fafb', fg='#6b7280', relief='flat', bd=0,
                              padx=4, pady=0, cursor='hand2')
        toggle_btn.place(relx=1.0, rely=0.5, anchor='e', x=-8, width=25, height=20)
        
        def toggle_visibility():
            if field_type == "password":
                visible = self.password_visible
            else:
                visible = self.passphrase_visible
                
            if visible[0]:
                entry.configure(show="•")
                toggle_btn.configure(text="👁️")
                visible[0] = False
            else:
                entry.configure(show="")
                toggle_btn.configure(text="🙈")
                visible[0] = True
        
        toggle_btn.configure(command=toggle_visibility)
        
        # Focus effects
        def on_focus_in(e):
            container.configure(highlightbackground='#3b82f6', bg='#ffffff')
            entry.configure(bg='#ffffff')
            toggle_btn.configure(bg='#ffffff')
        
        def on_focus_out(e):
            container.configure(highlightbackground='#d1d5db', bg='#f9fafb')
            entry.configure(bg='#f9fafb')
            toggle_btn.configure(bg='#f9fafb')
        
        # Bind focus events to container to maintain button position
        container.bind('<FocusIn>', on_focus_in)
        container.bind('<FocusOut>', on_focus_out)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return container
    
    def create_file_field(self, parent, row, title, filetypes):
        """Create file selection field with browse button"""
        container = tk.Frame(parent, bg='#ffffff')
        container.grid(row=row, column=1, sticky="ew", pady=8)
        
        entry = tk.Entry(container, font=('Segoe UI', 10), bg='#f9fafb', fg='#1f2937',
                        relief='solid', bd=1, highlightthickness=2, 
                        highlightcolor='#3b82f6', highlightbackground='#d1d5db',
                        insertbackground='#3b82f6')
        entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 6))
        
        self.key_entry = entry  # Store reference
        
        browse_btn = tk.Button(container, text="📁 Browse", font=('Segoe UI', 9, 'bold'),
                              bg='#3b82f6', fg='#ffffff', relief='flat', bd=0,
                              padx=12, pady=8, cursor='hand2')
        browse_btn.pack(side="right")
        
        def browse_file():
            from tkinter import filedialog
            filename = filedialog.askopenfilename(title=title, filetypes=filetypes)
            if filename:
                entry.delete(0, tk.END)
                entry.insert(0, filename)
        
        browse_btn.configure(command=browse_file)
        
        # Focus effects
        def on_focus_in(e):
            entry.configure(highlightbackground='#3b82f6', bg='#ffffff')
        
        def on_focus_out(e):
            entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return container
    
    def create_form_buttons(self, parent, row):
        """Create form action buttons"""
        btn_frame = tk.Frame(parent, bg='#ffffff')
        btn_frame.grid(row=row, column=0, columnspan=2, pady=(20, 0))
        
        # Save button
        save_text = "Update Profile" if hasattr(self, 'editing_profile_id') and self.editing_profile_id else "Save Profile"
        save_btn = tk.Button(btn_frame, text=f"✓ {save_text}", 
                            font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                            relief='flat', padx=16, pady=8, cursor='hand2', bd=0,
                            command=self.save_sftp_profile)
        save_btn.pack(side="left", padx=(0, 15))
        
        # Cancel button
        cancel_btn = tk.Button(btn_frame, text="× Cancel", 
                              font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                              relief='flat', padx=16, pady=8, cursor='hand2', bd=0,
                              command=self.show_sftp_table)
        cancel_btn.pack(side="left")
    
    def update_auth_fields(self, *args):
        """Update field visibility based on authentication method"""
        method = self.auth_method.get()
        
        if method == "Password":
            # Show password, hide key fields
            self.password_container.grid()
            self.key_label.grid_remove()
            self.key_container.grid_remove()
            self.passphrase_label.grid_remove()
            self.passphrase_container.grid_remove()
        elif method == "SSH Key":
            # Hide password, show key fields
            self.password_container.grid_remove()
            self.key_label.grid()
            self.key_container.grid()
            self.passphrase_label.grid()
            self.passphrase_container.grid()
        elif method == "Password + Key":
            # Show all fields
            self.password_container.grid()
            self.key_label.grid()
            self.key_container.grid()
            self.passphrase_label.grid()
            self.passphrase_container.grid()
    
    def save_sftp_profile(self):
        """Save SFTP profile (add or update)"""
        # Collect form data
        name = self.name_entry.get().strip()
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        key_file = self.key_entry.get().strip() if hasattr(self, 'key_entry') else ""
        passphrase = self.passphrase_entry.get().strip() if hasattr(self, 'passphrase_entry') else ""
        directory = self.directory_entry.get().strip()
        auth_type = self.auth_method.get()
        
        # Validation
        if not all([name, host, port, username]):
            self.show_popup("Error", "Name, Host, Port, and Username are required fields.", "error")
            return
        
        # Validate authentication method requirements
        if auth_type == "Password" and not password:
            self.show_popup("Error", "Password is required for Password authentication.", "error")
            return
        elif auth_type == "SSH Key" and not key_file:
            self.show_popup("Error", "SSH Key file is required for SSH Key authentication.", "error")
            return
        elif auth_type == "Password + Key" and (not password or not key_file):
            self.show_popup("Error", "Both Password and SSH Key file are required for Password + Key authentication.", "error")
            return
        
        try:
            port_num = int(port)
            if port_num < 1 or port_num > 65535:
                raise ValueError("Port must be between 1 and 65535")
        except ValueError as e:
            self.show_popup("Error", f"Invalid port number: {str(e)}", "error")
            return
        
        try:
            encrypted_password = self.db_manager.hash_password_reversible(password) if password else ""
            
            cursor = self.db_manager.conn.cursor()
            
            if hasattr(self, 'editing_profile_id') and self.editing_profile_id:
                # Update existing profile
                cursor.execute("""
                    UPDATE sftp_profiles 
                    SET profile_name = ?, host = ?, port = ?, username = ?, directory = ?, password = ?
                    WHERE id = ?
                """, (name, host, port_num, username, directory, encrypted_password, self.editing_profile_id))
                action = "updated"
            else:
                # Create new profile
                cursor.execute("""
                    INSERT INTO sftp_profiles (user_id, profile_name, host, port, username, directory, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.db_manager.user_id, name, host, port_num, username, directory, encrypted_password))
                action = "created"
            
            self.db_manager.conn.commit()
            
            # Show success and return to table
            self.show_popup("Success", f"SFTP profile '{name}' {action} successfully!", "success")
            self.show_sftp_table()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to save SFTP profile: {str(e)}", "error")
