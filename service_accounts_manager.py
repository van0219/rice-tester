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
        """Service account tab with modern UI/UX design"""
        frame = tk.Frame(parent, bg='#f8fafc', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Service Accounts Section with modern card design
        service_section = tk.Frame(frame, bg='#ffffff', relief='solid', bd=1, 
                                  highlightbackground='#e5e7eb', highlightthickness=1)
        service_section.pack(fill="x", pady=(0, 20))
        
        # Modern header with icon and better styling
        header_frame = tk.Frame(service_section, bg='#1e40af', height=45)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔑 Service Accounts", font=('Segoe UI', 14, 'bold'), 
                bg='#1e40af', fg='#ffffff').pack(expand=True, pady=12)
        
        # Content container with padding
        content_container = tk.Frame(service_section, bg='#ffffff', padx=20, pady=15)
        content_container.pack(fill="both", expand=True)
        
        # Professional table headers with icons
        headers_frame = tk.Frame(content_container, bg='#f8fafc', height=35, relief='solid', bd=1,
                                highlightbackground='#e5e7eb', highlightthickness=1)
        headers_frame.pack(fill="x", pady=(0, 5))
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="📝 Name", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0, y=8, relwidth=0.3)
        tk.Label(headers_frame, text="📁 File Path", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0.3, y=8, relwidth=0.35)
        tk.Label(headers_frame, text="📅 Date Added", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0.65, y=8, relwidth=0.15)
        tk.Label(headers_frame, text="⚙️ Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0.8, y=8, relwidth=0.2)
        
        # Scrollable accounts container with border
        accounts_container = tk.Frame(content_container, bg='#ffffff', relief='solid', bd=1,
                                     highlightbackground='#e5e7eb', highlightthickness=1)
        accounts_container.pack(fill="x", pady=(0, 15))
        
        self.accounts_scroll_frame = tk.Frame(accounts_container, bg='#ffffff')
        self.accounts_scroll_frame.pack(fill="x", padx=1, pady=1)
        
        # Action buttons with modern styling
        btn_frame = tk.Frame(content_container, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        add_btn = tk.Button(btn_frame, text="➕ Add Account", font=('Segoe UI', 10, 'bold'), 
                           bg='#059669', fg='#ffffff', relief='flat', padx=20, pady=10, 
                           cursor='hand2', bd=0, highlightthickness=0, command=self._add_service_account)
        add_btn.pack(side="left", padx=(0, 10))
        
        refresh_btn = tk.Button(btn_frame, text="🔄 Refresh", font=('Segoe UI', 10, 'bold'), 
                               bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                               cursor='hand2', bd=0, highlightthickness=0, command=self._load_service_accounts)
        refresh_btn.pack(side="left")
        
        # Add hover effects
        def on_add_enter(e): add_btn.config(bg='#047857')
        def on_add_leave(e): add_btn.config(bg='#059669')
        def on_refresh_enter(e): refresh_btn.config(bg='#4b5563')
        def on_refresh_leave(e): refresh_btn.config(bg='#6b7280')
        
        add_btn.bind('<Enter>', on_add_enter)
        add_btn.bind('<Leave>', on_add_leave)
        refresh_btn.bind('<Enter>', on_refresh_enter)
        refresh_btn.bind('<Leave>', on_refresh_leave)
        
        self._load_service_accounts()
        
        # Tenant Management Section with modern card design
        tenant_section = tk.Frame(frame, bg='#ffffff', relief='solid', bd=1, 
                                 highlightbackground='#e5e7eb', highlightthickness=1)
        tenant_section.pack(fill="x", pady=(0, 20))
        
        # Modern header with icon
        tenant_header_frame = tk.Frame(tenant_section, bg='#10b981', height=45)
        tenant_header_frame.pack(fill="x")
        tenant_header_frame.pack_propagate(False)
        
        tk.Label(tenant_header_frame, text="🏗️ Tenant Management", font=('Segoe UI', 14, 'bold'), 
                bg='#10b981', fg='#ffffff').pack(expand=True, pady=12)
        
        # Tenant content container with padding
        tenant_content_container = tk.Frame(tenant_section, bg='#ffffff', padx=20, pady=15)
        tenant_content_container.pack(fill="both", expand=True)
        
        # Professional tenant table headers with icons
        tenant_headers_frame = tk.Frame(tenant_content_container, bg='#f8fafc', height=35, relief='solid', bd=1,
                                       highlightbackground='#e5e7eb', highlightthickness=1)
        tenant_headers_frame.pack(fill="x", pady=(0, 5))
        tenant_headers_frame.pack_propagate(False)
        
        tk.Label(tenant_headers_frame, text="🆔 Tenant ID", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0, y=8, relwidth=0.25)
        tk.Label(tenant_headers_frame, text="🌍 Environment", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0.25, y=8, relwidth=0.25)
        tk.Label(tenant_headers_frame, text="📝 Description", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0.5, y=8, relwidth=0.3)
        tk.Label(tenant_headers_frame, text="⚙️ Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151', anchor='w', padx=15).place(relx=0.8, y=8, relwidth=0.2)
        
        # Scrollable tenants container with border
        tenants_container = tk.Frame(tenant_content_container, bg='#ffffff', relief='solid', bd=1,
                                    highlightbackground='#e5e7eb', highlightthickness=1)
        tenants_container.pack(fill="x", pady=(0, 15))
        
        self.tenants_scroll_frame = tk.Frame(tenants_container, bg='#ffffff')
        self.tenants_scroll_frame.pack(fill="x", padx=1, pady=1)
        
        # Tenant action buttons with modern styling
        tenant_btn_frame = tk.Frame(tenant_content_container, bg='#ffffff')
        tenant_btn_frame.pack(fill="x")
        
        add_tenant_btn = tk.Button(tenant_btn_frame, text="➕ Add Tenant", font=('Segoe UI', 10, 'bold'), 
                                  bg='#059669', fg='#ffffff', relief='flat', padx=20, pady=10, 
                                  cursor='hand2', bd=0, highlightthickness=0, command=self._add_tenant)
        add_tenant_btn.pack(side="left", padx=(0, 10))
        
        refresh_tenant_btn = tk.Button(tenant_btn_frame, text="🔄 Refresh", font=('Segoe UI', 10, 'bold'), 
                                      bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                                      cursor='hand2', bd=0, highlightthickness=0, command=self._load_tenants)
        refresh_tenant_btn.pack(side="left")
        
        # Add hover effects for tenant buttons
        def on_add_tenant_enter(e): add_tenant_btn.config(bg='#047857')
        def on_add_tenant_leave(e): add_tenant_btn.config(bg='#059669')
        def on_refresh_tenant_enter(e): refresh_tenant_btn.config(bg='#4b5563')
        def on_refresh_tenant_leave(e): refresh_tenant_btn.config(bg='#6b7280')
        
        add_tenant_btn.bind('<Enter>', on_add_tenant_enter)
        add_tenant_btn.bind('<Leave>', on_add_tenant_leave)
        refresh_tenant_btn.bind('<Enter>', on_refresh_tenant_enter)
        refresh_tenant_btn.bind('<Leave>', on_refresh_tenant_leave)
        
        self._load_tenants()
        
        # Removed Miscellaneous section - TES-070 formatting moved to Settings menu
        

    # TES-070 template methods removed - moved to Settings menu
    
    def _load_tenants(self):
        """Load tenants from database"""
        for widget in self.tenants_scroll_frame.winfo_children():
            widget.destroy()
        
        tenants = self.db_manager.get_tenants()
        
        for i, tenant in enumerate(tenants):
            tenant_id, tenant_name, environment, description = tenant
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.tenants_scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill='x')
            row_frame.pack_propagate(False)
            
            tk.Label(row_frame, text=tenant_name, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#374151', anchor='w', padx=15).place(relx=0, y=8, relwidth=0.25)
            tk.Label(row_frame, text=environment, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#6b7280', anchor='w', padx=15).place(relx=0.25, y=8, relwidth=0.25)
            tk.Label(row_frame, text=description or 'No description', font=('Segoe UI', 9), 
                    bg=bg_color, fg='#6b7280', anchor='w', padx=15).place(relx=0.5, y=8, relwidth=0.3)
            
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=5, relwidth=0.2, height=25)
            
            tk.Button(actions_frame, text="✏️ Edit", font=('Segoe UI', 8), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=6, pady=3, 
                     cursor='hand2', bd=0, command=lambda tid=tenant_id: self._edit_tenant(tid)).pack(side='left', padx=(0, 3))
            tk.Button(actions_frame, text="🗑️ Delete", font=('Segoe UI', 8), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=6, pady=3, 
                     cursor='hand2', bd=0, command=lambda tid=tenant_id: self._delete_tenant(tid)).pack(side='left')
    
    def _add_tenant(self):
        """Add new tenant dialog"""
        self._tenant_dialog("Add Tenant", None)
    
    def _edit_tenant(self, tenant_id):
        """Edit existing tenant dialog"""
        self._tenant_dialog("Edit Tenant", tenant_id)
    
    def _tenant_dialog(self, title, tenant_id=None):
        """Tenant add/edit dialog"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        center_dialog(popup, 450, 386)
        popup.configure(bg='#f8fafc')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Card layout
        card_frame = tk.Frame(popup, bg='#ffffff', relief='solid', bd=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header
        header_frame = tk.Frame(card_frame, bg='#059669', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"🏗️ {title}", font=('Segoe UI', 14, 'bold'), 
                bg='#059669', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(card_frame, bg='#ffffff', padx=25, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Tenant ID
        tk.Label(content_frame, text="🆔 Tenant ID *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#dc2626').pack(anchor="w", pady=(0, 5))
        tenant_name_entry = tk.Entry(content_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                                    relief='solid', bd=1, highlightthickness=1, highlightcolor='#059669')
        tenant_name_entry.pack(fill="x", pady=(0, 15))
        
        # Environment
        tk.Label(content_frame, text="🌍 Environment *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#dc2626').pack(anchor="w", pady=(0, 5))
        env_var = tk.StringVar()
        env_combo = ttk.Combobox(content_frame, textvariable=env_var, font=('Segoe UI', 10))
        env_combo['values'] = ['Production', 'Test', 'Development', 'Training', 'Sandbox', 'Demo', 'Preprod', 'Pristine', 'UAT', 'Staging', 'QA', 'Integration']
        env_combo.pack(fill="x", pady=(0, 15))
        
        # Description
        tk.Label(content_frame, text="📝 Description", font=('Segoe UI', 10), 
                bg='#ffffff', fg='#6b7280').pack(anchor="w", pady=(0, 5))
        desc_entry = tk.Entry(content_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                             relief='solid', bd=1, highlightthickness=1, highlightcolor='#059669')
        desc_entry.pack(fill="x", pady=(0, 20))
        
        # Load existing data if editing
        if tenant_id:
            try:
                tenant_data = self.db_manager.get_tenant_by_id(tenant_id)
                if tenant_data:
                    _, tenant_name, environment, description = tenant_data
                    tenant_name_entry.insert(0, tenant_name)
                    env_var.set(environment)
                    desc_entry.insert(0, description or '')
            except Exception as e:
                self.show_popup("Error", f"Failed to load tenant data: {str(e)}", "error")
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_tenant():
            tenant_name = tenant_name_entry.get().strip()
            environment = env_var.get().strip()
            description = desc_entry.get().strip()
            
            if not all([tenant_name, environment]):
                self.show_popup("Error", "Please fill in required fields (Tenant ID, Environment)", "error")
                return
            
            try:
                if tenant_id:
                    # Update existing
                    self.db_manager.update_tenant(tenant_id, tenant_name, environment, description)
                    action = "updated"
                else:
                    # Add new
                    self.db_manager.add_tenant(tenant_name, environment, description)
                    action = "added"
                
                popup.destroy()
                self._load_tenants()
                self.show_popup("Success", f"Tenant '{tenant_name}' {action} successfully!", "success")
                
            except Exception as e:
                self.show_popup("Error", f"Failed to save tenant: {str(e)}", "error")
        
        save_btn = tk.Button(btn_frame, text="💾 Save", font=('Segoe UI', 10, 'bold'), 
                            bg='#059669', fg='#ffffff', relief='flat', padx=20, pady=10, 
                            cursor='hand2', bd=0, highlightthickness=0, command=save_tenant)
        save_btn.pack(side="left", padx=(0, 15))
        
        cancel_btn = tk.Button(btn_frame, text="✕ Cancel", font=('Segoe UI', 10, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                              cursor='hand2', bd=0, highlightthickness=0, command=popup.destroy)
        cancel_btn.pack(side="left")
        
        tenant_name_entry.focus()
    
    def _delete_tenant(self, tenant_id):
        """Delete tenant with confirmation"""
        try:
            tenant_data = self.db_manager.get_tenant_by_id(tenant_id)
            if not tenant_data:
                self.show_popup("Error", "Tenant not found", "error")
                return
            
            tenant_name = tenant_data[1]
            
            confirm_popup = tk.Toplevel(self.root)
            confirm_popup.title("Confirm Delete")
            center_dialog(confirm_popup, 400, 250)
            confirm_popup.configure(bg='#ffffff')
            
            try:
                confirm_popup.iconbitmap("infor_logo.ico")
            except:
                pass
            
            header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
            header_frame.pack(fill="x")
            header_frame.pack_propagate(False)
            
            tk.Label(header_frame, text="🗑️ Delete Tenant", font=('Segoe UI', 14, 'bold'), 
                    bg='#ef4444', fg='#ffffff').pack(expand=True)
            
            content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
            content_frame.pack(fill="both", expand=True)
            
            message = f"Delete tenant '{tenant_name}'?\n\nThis action cannot be undone."
            tk.Label(content_frame, text=message, font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
            
            btn_frame = tk.Frame(content_frame, bg='#ffffff')
            btn_frame.pack()
            
            def confirm_delete():
                try:
                    self.db_manager.delete_tenant(tenant_id)
                    confirm_popup.destroy()
                    self._load_tenants()
                    self.show_popup("Success", f"Tenant '{tenant_name}' deleted successfully!", "success")
                except Exception as e:
                    self.show_popup("Error", f"Failed to delete tenant: {str(e)}", "error")
            
            tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                     relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
            tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                     relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
        
        except Exception as e:
            self.show_popup("Error", f"Failed to delete tenant: {str(e)}", "error")
    

    
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
                    bg=bg_color, fg='#374151', anchor='w', padx=15).place(relx=0, y=8, relwidth=0.3)
            tk.Label(row_frame, text=file_path, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#6b7280', anchor='w', padx=15).place(relx=0.3, y=8, relwidth=0.35)
            tk.Label(row_frame, text=date_added, font=('Segoe UI', 9), 
                    bg=bg_color, fg='#6b7280', anchor='w', padx=15).place(relx=0.65, y=8, relwidth=0.15)
            
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=5, relwidth=0.2, height=25)
            
            tk.Button(actions_frame, text="📥 Download", font=('Segoe UI', 8), 
                     bg='#3b82f6', fg='#ffffff', relief='flat', padx=6, pady=3, 
                     cursor='hand2', bd=0, command=lambda aid=account_id: self._download_account(aid)).pack(side='left', padx=(0, 3))
            tk.Button(actions_frame, text="🗑️ Delete", font=('Segoe UI', 8), 
                     bg='#ef4444', fg='#ffffff', relief='flat', padx=6, pady=3, 
                     cursor='hand2', bd=0, command=lambda aid=account_id: self._delete_account(aid)).pack(side='left')
    
    def _add_service_account(self):
        """Add service account dialog with modern UI/UX"""
        from tkinter import filedialog
        from datetime import datetime
        import os
        
        popup = tk.Toplevel(self.root)
        popup.title("Add Service Account")
        center_dialog(popup, 500, 350)
        popup.configure(bg='#f8fafc')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Card layout
        card_frame = tk.Frame(popup, bg='#ffffff', relief='solid', bd=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Header
        header_frame = tk.Frame(card_frame, bg='#1e40af', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔑 Add Service Account", font=('Segoe UI', 14, 'bold'), 
                bg='#1e40af', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(card_frame, bg='#ffffff', padx=25, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Account Name
        tk.Label(content_frame, text="📝 Account Name *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#dc2626').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(content_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                             relief='solid', bd=1, highlightthickness=1, highlightcolor='#1e40af')
        name_entry.pack(fill="x", pady=(0, 15))
        
        # Service Account File
        tk.Label(content_frame, text="📁 Service Account File (.ionapi) *", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#dc2626').pack(anchor="w", pady=(0, 5))
        
        file_frame = tk.Frame(content_frame, bg='#ffffff')
        file_frame.pack(fill="x", pady=(0, 20))
        
        file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=file_path_var, font=('Segoe UI', 10), 
                             bg='#f9fafb', relief='solid', bd=1, highlightthickness=1, 
                             highlightcolor='#1e40af', state='readonly')
        file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        def browse_file():
            file_path = filedialog.askopenfilename(
                title="Select Service Account File",
                filetypes=[("ION API Files", "*.ionapi"), ("All Files", "*.*")]
            )
            if file_path:
                file_path_var.set(file_path)
        
        browse_btn = tk.Button(file_frame, text="📂 Browse", font=('Segoe UI', 9, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=12, pady=6, 
                              cursor='hand2', bd=0, highlightthickness=0, command=browse_file)
        browse_btn.pack(side='right')
        
        # Add hover effect for browse button
        def on_browse_enter(e): browse_btn.config(bg='#4b5563')
        def on_browse_leave(e): browse_btn.config(bg='#6b7280')
        browse_btn.bind('<Enter>', on_browse_enter)
        browse_btn.bind('<Leave>', on_browse_leave)
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_account():
            name = name_entry.get().strip()
            file_path = file_path_var.get().strip()
            
            if not all([name, file_path]):
                self.show_popup("Error", "Please fill in required fields (Account Name, Service Account File)", "error")
                return
            
            try:
                date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db_manager.save_service_account(name, file_path, date_added)
                popup.destroy()
                self._load_service_accounts()
                self.show_popup("Success", f"Service account '{name}' added successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to add service account: {str(e)}", "error")
        
        save_btn = tk.Button(btn_frame, text="💾 Save", font=('Segoe UI', 10, 'bold'), 
                            bg='#1e40af', fg='#ffffff', relief='flat', padx=20, pady=10, 
                            cursor='hand2', bd=0, highlightthickness=0, command=save_account)
        save_btn.pack(side="left", padx=(0, 15))
        
        cancel_btn = tk.Button(btn_frame, text="✕ Cancel", font=('Segoe UI', 10, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                              cursor='hand2', bd=0, highlightthickness=0, command=popup.destroy)
        cancel_btn.pack(side="left")
        
        # Add hover effects
        def on_save_enter(e): save_btn.config(bg='#1d4ed8')
        def on_save_leave(e): save_btn.config(bg='#1e40af')
        def on_cancel_enter(e): cancel_btn.config(bg='#4b5563')
        def on_cancel_leave(e): cancel_btn.config(bg='#6b7280')
        
        save_btn.bind('<Enter>', on_save_enter)
        save_btn.bind('<Leave>', on_save_leave)
        cancel_btn.bind('<Enter>', on_cancel_enter)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
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
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
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
