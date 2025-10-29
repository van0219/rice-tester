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
        """Setup SFTP configuration tab content"""
        sftp_frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        sftp_frame.pack(fill="both", expand=True)
        
        # SFTP profiles container
        sftp_container = tk.Frame(sftp_frame, bg='#ffffff')
        sftp_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # Headers
        headers_frame = tk.Frame(sftp_container, bg='#e5e7eb', height=25)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        # Static headers with padding
        name_label = tk.Label(headers_frame, text="Name", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        name_label.place(relx=0, y=5, relwidth=0.15)
        
        host_label = tk.Label(headers_frame, text="Host", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        host_label.place(relx=0.15, y=5, relwidth=0.125)
        
        port_label = tk.Label(headers_frame, text="Port", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        port_label.place(relx=0.275, y=5, relwidth=0.05)
        
        username_label = tk.Label(headers_frame, text="Username", font=('Segoe UI', 10, 'bold'), 
                                 bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        username_label.place(relx=0.325, y=5, relwidth=0.12)
        
        password_label = tk.Label(headers_frame, text="Password", font=('Segoe UI', 10, 'bold'), 
                                 bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        password_label.place(relx=0.445, y=5, relwidth=0.1)
        
        directory_label = tk.Label(headers_frame, text="Directory", font=('Segoe UI', 10, 'bold'), 
                                  bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        directory_label.place(relx=0.545, y=5, relwidth=0.235)
        
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.8, y=5, relwidth=0.2)
        
        # Column separators for headers
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.15, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.275, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.325, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.445, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.545, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.8, y=2, height=21)
        
        # SFTP profiles scroll frame
        self.sftp_scroll_frame = tk.Frame(sftp_container, bg='#ffffff')
        self.sftp_scroll_frame.pack(fill="both", expand=True)
        
        # Buttons
        btn_frame = tk.Frame(sftp_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        add_sftp_btn = ttk.Button(btn_frame, text="➕ Add SFTP", style='Primary.TButton',
                                 command=self.add_sftp_profile)
        add_sftp_btn.pack(side="left", padx=(0, 10))
        add_sftp_btn.configure(cursor='hand2')
        
        self.load_sftp_profiles()
    
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
            password_display = "••••••" if encrypted_password else "No Password"
            
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
            name_label.place(relx=0, y=8, relwidth=0.15)
            name_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Host (clickable) with padding
            host_label = tk.Label(row_frame, text=host, font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            host_label.place(relx=0.15, y=8, relwidth=0.125)
            host_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Port (clickable) with padding
            port_label = tk.Label(row_frame, text=str(port), font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            port_label.place(relx=0.275, y=8, relwidth=0.05)
            port_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Username (clickable) with padding
            username_label = tk.Label(row_frame, text=username, font=('Segoe UI', 9), 
                                     bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            username_label.place(relx=0.325, y=8, relwidth=0.12)
            username_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Password (clickable) with padding
            password_label = tk.Label(row_frame, text=password_display, font=('Segoe UI', 9), 
                                     bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            password_label.place(relx=0.445, y=8, relwidth=0.1)
            password_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Directory (clickable) with padding
            directory_display = directory if directory else "(not set)"
            directory_label = tk.Label(row_frame, text=directory_display, font=('Segoe UI', 9), 
                                      bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            directory_label.place(relx=0.545, y=8, relwidth=0.235)
            directory_label.bind('<Button-1>', lambda e, pid=profile_id: self.select_sftp_profile(pid))
            
            # Column separators for rows
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.15, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.275, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.325, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.445, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.545, y=2, height=26)
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.8, y=2, height=26)
            
            # Action buttons frame
            btn_frame = tk.Frame(row_frame, bg=bg_color)
            btn_frame.place(relx=0.801, y=4, relwidth=0.199, height=22)
            
            test_btn = tk.Button(btn_frame, text="Test", font=('Segoe UI', 8, 'bold'), 
                               bg='#10b981', fg='white', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0,
                               command=lambda pid=profile_id: self.test_sftp_profile(pid))
            
            edit_btn = tk.Button(btn_frame, text="Edit", font=('Segoe UI', 8, 'bold'), 
                               bg='#3b82f6', fg='white', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0,
                               command=lambda pid=profile_id: self.edit_sftp_profile(pid))
            
            delete_btn = tk.Button(btn_frame, text="Delete", font=('Segoe UI', 8, 'bold'), 
                                 bg='#ef4444', fg='white', relief='flat', 
                                 padx=4, pady=1, cursor='hand2', bd=0,
                                 command=lambda pid=profile_id: self.delete_sftp_profile(pid))
            
            # Left-align buttons with consistent padding
            test_btn.place(x=18, y=0, width=35, height=22)
            edit_btn.place(x=58, y=0, width=35, height=22)
            delete_btn.place(x=98, y=0, width=45, height=22)
    
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
    
    def add_sftp_profile(self):
        """Add SFTP profile dialog"""
        popup = tk.Toplevel()
        popup.title("Add SFTP Profile")
        center_dialog(popup, 500, 350)
        popup.configure(bg='#ffffff')
        popup.resizable(False, False)
        popup.transient()
        popup.grab_set()
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Profile Name
        tk.Label(frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Host
        tk.Label(frame, text="Host:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=5)
        host_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        host_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Port
        tk.Label(frame, text="Port:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky="w", pady=5)
        port_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        port_entry.insert(0, "22")
        port_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Username
        tk.Label(frame, text="Username:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky="w", pady=5)
        username_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        username_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Password
        tk.Label(frame, text="Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=4, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, width=30, show="•", font=('Segoe UI', 10))
        password_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        # Directory
        tk.Label(frame, text="Directory:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=5, column=0, sticky="w", pady=5)
        directory_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        directory_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        
        frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def save_profile():
            name = name_entry.get().strip()
            host = host_entry.get().strip()
            port = port_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            directory = directory_entry.get().strip()
            
            if not all([name, host, port, username]):
                self.show_popup("Error", "Name, Host, Port, and Username are required", "error")
                return
            
            try:
                port_num = int(port)
                encrypted_password = self.db_manager.hash_password_reversible(password) if password else ""
                
                cursor = self.db_manager.conn.cursor()
                cursor.execute("""
                    INSERT INTO sftp_profiles (user_id, profile_name, host, port, username, directory, password)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (self.db_manager.user_id, name, host, port_num, username, directory, encrypted_password))
                self.db_manager.conn.commit()
                
                popup.destroy()
                self.load_sftp_profiles()
                self.show_popup("Success", f"SFTP profile '{name}' created successfully!", "success")
            except ValueError:
                self.show_popup("Error", "Port must be a valid number", "error")
            except Exception as e:
                self.show_popup("Error", f"Failed to create SFTP profile: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=save_profile).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=popup.destroy).pack(side="left")
        
        popup.focus_set()
        name_entry.focus()
    
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
    
    def edit_sftp_profile(self, profile_id):
        """Edit SFTP profile"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT profile_name, host, port, username, directory, password FROM sftp_profiles WHERE id = ?", (profile_id,))
        profile = cursor.fetchone()
        
        if not profile:
            self.show_popup("Error", "SFTP profile not found", "error")
            return
        
        name, host, port, username, directory, encrypted_password = profile
        password = self.db_manager.decrypt_password(encrypted_password) if encrypted_password else ""
        
        popup = tk.Toplevel()
        popup.title("Edit SFTP Profile")
        center_dialog(popup, 500, 350)
        popup.configure(bg='#ffffff')
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Profile Name
        tk.Label(frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        name_entry.insert(0, name)
        name_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        # Host
        tk.Label(frame, text="Host:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=5)
        host_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        host_entry.insert(0, host)
        host_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Port
        tk.Label(frame, text="Port:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky="w", pady=5)
        port_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        port_entry.insert(0, str(port))
        port_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Username
        tk.Label(frame, text="Username:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky="w", pady=5)
        username_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        username_entry.insert(0, username)
        username_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Password
        tk.Label(frame, text="Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=4, column=0, sticky="w", pady=5)
        password_entry = tk.Entry(frame, width=30, show="•", font=('Segoe UI', 10))
        password_entry.insert(0, password)
        password_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        # Directory
        tk.Label(frame, text="Directory:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=5, column=0, sticky="w", pady=5)
        directory_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        directory_entry.insert(0, directory or '')
        directory_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        
        frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_host = host_entry.get().strip()
            new_port = port_entry.get().strip()
            new_username = username_entry.get().strip()
            new_password = password_entry.get().strip()
            new_directory = directory_entry.get().strip()
            
            if not all([new_name, new_host, new_port, new_username]):
                self.show_popup("Error", "Name, Host, Port, and Username are required", "error")
                return
            
            try:
                port_num = int(new_port)
                encrypted_password = self.db_manager.hash_password_reversible(new_password) if new_password else ""
                
                cursor = self.db_manager.conn.cursor()
                cursor.execute("""
                    UPDATE sftp_profiles 
                    SET profile_name = ?, host = ?, port = ?, username = ?, directory = ?, password = ?
                    WHERE id = ?
                """, (new_name, new_host, port_num, new_username, new_directory, encrypted_password, profile_id))
                self.db_manager.conn.commit()
                
                popup.destroy()
                self.load_sftp_profiles()
                self.show_popup("Success", f"SFTP profile '{new_name}' updated successfully!", "success")
            except ValueError:
                self.show_popup("Error", "Port must be a valid number", "error")
            except Exception as e:
                self.show_popup("Error", f"Failed to update SFTP profile: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
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