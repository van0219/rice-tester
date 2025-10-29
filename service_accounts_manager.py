#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from selenium_tab_manager import center_dialog

class ServiceAccountsManager:
    def __init__(self, root, db_manager, show_popup_callback):
        self.root = root
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def setup_service_accounts_tab(self, parent):
        """Service account tab"""
        frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Service Accounts Section with enclosure
        service_section = tk.Frame(frame, bg='#f8f9fa', relief='solid', bd=1, padx=15, pady=15)
        service_section.pack(fill="x", pady=(0, 20))
        
        # Header
        tk.Label(service_section, text="Service Accounts", font=('Segoe UI', 12, 'bold'), bg='#f8f9fa').pack(anchor="w", pady=(0, 10))
        
        # Headers
        headers_frame = tk.Frame(service_section, bg='#e5e7eb', height=25)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="Name", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0, y=5, relwidth=0.3)
        tk.Label(headers_frame, text="File Path", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.3, y=5, relwidth=0.35)
        tk.Label(headers_frame, text="Date Added", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.65, y=5, relwidth=0.15)
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.8, y=5, relwidth=0.2)
        
        # Accounts scroll frame
        self.accounts_scroll_frame = tk.Frame(service_section, bg='#ffffff')
        self.accounts_scroll_frame.pack(fill="x", pady=(0, 10))
        
        # Buttons
        btn_frame = tk.Frame(service_section, bg='#f8f9fa')
        btn_frame.pack(fill="x")
        
        tk.Button(btn_frame, text="➕ Add Account", font=('Segoe UI', 10, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self._add_service_account).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="🔄 Refresh", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self._load_service_accounts).pack(side="left")
        
        self._load_service_accounts()
        
        # Miscellaneous section with enclosure
        misc_section = tk.Frame(frame, bg='#f0f9ff', relief='solid', bd=1, padx=15, pady=15)
        misc_section.pack(fill="x")
        
        tk.Label(misc_section, text="Miscellaneous", font=('Segoe UI', 12, 'bold'), bg='#f0f9ff').pack(anchor="w", pady=(0, 10))
        
        # TES-070 Name Format
        self.tes070_format_var = tk.BooleanVar()
        tes070_check = tk.Checkbutton(misc_section, text="Configure TES-070 Name Format", 
                                     variable=self.tes070_format_var, bg='#f0f9ff', 
                                     font=('Segoe UI', 10), command=self._toggle_tes070_format)
        tes070_check.pack(anchor="w", pady=(0, 10))
        
        # TES-070 format configuration (always visible)
        self.tes070_config_frame = tk.Frame(misc_section, bg='#f0f9ff')
        self.tes070_config_frame.pack(fill="x", padx=(20, 0), pady=(0, 10))
        
        # Template string approach
        tk.Label(self.tes070_config_frame, text="Template (use placeholders):", font=('Segoe UI', 10, 'bold'), bg='#f0f9ff').pack(anchor="w", pady=(0, 5))
        
        self.template_var = tk.StringVar()
        # Load current template from database
        try:
            current_template = self.db_manager.get_tes070_template()
            self.template_var.set(current_template)
        except:
            self.template_var.set("TES-070_{rice_id}_{date}_v{version}.docx")
        
        template_entry = tk.Entry(self.tes070_config_frame, textvariable=self.template_var, width=60, font=('Segoe UI', 10))
        template_entry.pack(fill="x", pady=(0, 10))
        
        # Available placeholders help
        self.help_frame = tk.Frame(self.tes070_config_frame, bg='#e0f2fe', relief='solid', bd=1)
        self.help_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(self.help_frame, text="Available placeholders:", font=('Segoe UI', 9, 'bold'), bg='#e0f2fe').pack(anchor="w", padx=10, pady=(5, 0))
        placeholders = "{rice_id} {name} {client_name} {tenant} {date} {version}"
        tk.Label(self.help_frame, text=placeholders, font=('Segoe UI', 9), bg='#e0f2fe', fg='#0369a1').pack(anchor="w", padx=10, pady=(0, 5))
        
        # Save button
        save_btn = tk.Button(self.tes070_config_frame, text="💾 Save Template", font=('Segoe UI', 10, 'bold'), 
                            bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8, 
                            cursor='hand2', bd=0, command=self._save_tes070_template)
        save_btn.pack(anchor="w", pady=(0, 10))
        

    
    def _toggle_tes070_format(self):
        """Toggle TES-070 format configuration visibility"""
        # Configuration frame is always visible now
        # This method kept for checkbox functionality but doesn't hide/show frame
        pass
    
    def _save_tes070_template(self):
        """Save TES-070 name format template"""
        template = self.template_var.get().strip()
        
        if not template:
            self.show_popup("Error", "Please enter a template format", "error")
            return
        
        try:
            # Save to database
            self.db_manager.save_tes070_template(template)
            
            # Reset checkbox only (configuration stays visible)
            self.tes070_format_var.set(False)
            
            self.show_popup("Success", "TES-070 name format template saved successfully!", "success")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to save template: {str(e)}", "error")
    

    
    def _load_service_accounts(self):
        """Load service accounts"""
        for widget in self.accounts_scroll_frame.winfo_children():
            widget.destroy()
        
        accounts = self.db_manager.get_service_accounts()
        
        for i, account in enumerate(accounts):
            account_id, name, file_path, date_added = account
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.accounts_scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill='x')
            row_frame.pack_propagate(False)
            
            tk.Label(row_frame, text=name, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0, y=8, relwidth=0.3)
            tk.Label(row_frame, text=file_path, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.3, y=8, relwidth=0.35)
            tk.Label(row_frame, text=date_added, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=18).place(relx=0.65, y=8, relwidth=0.15)
            
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=5, relwidth=0.2, height=25)
            
            tk.Button(actions_frame, text="Download", font=('Segoe UI', 8), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=4, pady=2, 
                     cursor='hand2', bd=0, command=lambda aid=account_id: self._download_account(aid)).pack(side='left', padx=(0, 2))
            tk.Button(actions_frame, text="Delete", font=('Segoe UI', 8), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=4, pady=2, 
                     cursor='hand2', bd=0, command=lambda aid=account_id: self._delete_account(aid)).pack(side='left')
    
    def _add_service_account(self):
        """Add service account dialog"""
        from tkinter import filedialog
        from datetime import datetime
        import os
        
        popup = tk.Toplevel(self.root)
        popup.title("Add Service Account")
        center_dialog(popup, 500, 300)
        popup.configure(bg='#ffffff')
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Account Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=50, font=('Segoe UI', 10))
        name_entry.pack(fill="x", pady=(0, 10))
        
        tk.Label(frame, text="Service Account File (.ionapi):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        
        file_frame = tk.Frame(frame, bg='#ffffff')
        file_frame.pack(fill="x", pady=(0, 20))
        
        file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=file_path_var, width=40, font=('Segoe UI', 10), state='readonly')
        file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        def browse_file():
            file_path = filedialog.askopenfilename(
                title="Select Service Account File",
                filetypes=[("ION API Files", "*.ionapi"), ("All Files", "*.*")]
            )
            if file_path:
                file_path_var.set(file_path)
        
        tk.Button(file_frame, text="Browse", font=('Segoe UI', 9), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=10, pady=4, cursor='hand2', bd=0, command=browse_file).pack(side='right')
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_account():
            name = name_entry.get().strip()
            file_path = file_path_var.get().strip()
            
            if not all([name, file_path]):
                self.show_popup("Error", "Please fill in all fields", "error")
                return
            
            try:
                date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db_manager.save_service_account(name, file_path, date_added)
                popup.destroy()
                self._load_service_accounts()
                self.show_popup("Success", f"Service account '{name}' added successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to add service account: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_account).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
    def _download_account(self, account_id):
        """Download service account file"""
        from tkinter import filedialog
        import os
        
        try:
            # Get account content from database
            account_data = self.db_manager.get_service_account_content(account_id)
            if not account_data:
                self.show_popup("Error", "Service account not found", "error")
                return
            
            name, file_content = account_data
            
            if not file_content:
                self.show_popup("Error", "No file content available for download", "error")
                return
            
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(
                title="Save Service Account File",
                defaultextension=".ionapi",
                filetypes=[("ION API Files", "*.ionapi"), ("All Files", "*.*")],
                initialfile=f"{name}.ionapi"
            )
            
            if file_path:
                # Write file content
                with open(file_path, 'wb') as f:
                    f.write(file_content)
                
                self.show_popup("Success", f"Service account '{name}' downloaded successfully!", "success")
        
        except Exception as e:
            self.show_popup("Error", f"Failed to download service account: {str(e)}", "error")
    
    def _delete_account(self, account_id):
        """Delete service account with confirmation"""
        # Get account name for confirmation
        accounts = self.db_manager.get_service_accounts()
        account_data = next((a for a in accounts if a[0] == account_id), None)
        
        if not account_data:
            self.show_popup("Error", "Service account not found", "error")
            return
        
        account_name = account_data[1]
        
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Confirm Delete")
        center_dialog(confirm_popup, 400, 250)
        confirm_popup.configure(bg='#ffffff')
        
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🗑️ Delete Service Account", font=('Segoe UI', 14, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message = f"Delete service account '{account_name}'?\n\nThis action cannot be undone."
        tk.Label(content_frame, text=message, font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                self.db_manager.delete_service_account(account_id)
                confirm_popup.destroy()
                self._load_service_accounts()
                self.show_popup("Success", f"Service account '{account_name}' deleted successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete service account: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")