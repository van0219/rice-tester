#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from enhanced_popup_system import enhanced_center_dialog, create_enhanced_dialog

def center_dialog(dialog, width=None, height=None):
    """Enhanced center dialog that doesn't hide existing forms"""
    enhanced_center_dialog(dialog, width, height, modal=False)

class RiceDialogs:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def edit_rice_profile(self, profile_id, refresh_callback):
        """Edit RICE profile"""
        profiles = self.db_manager.get_rice_profiles()
        profile_data = None
        for profile in profiles:
            if profile[0] == profile_id:
                profile_data = profile
                break
        
        if not profile_data:
            self.show_popup("Error", "RICE profile not found", "error")
            return
        
        popup = create_enhanced_dialog(None, "Edit RICE Item", 650, 420, modal=False)
        popup.configure(bg='#f8fafc')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Modern card-based layout
        card_frame = tk.Frame(popup, bg='#ffffff', relief='solid', bd=1)
        card_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Blue header with title
        header_frame = tk.Frame(card_frame, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✏️ Edit RICE Item", font=('Segoe UI', 14, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content frame with better spacing
        content_frame = tk.Frame(card_frame, bg='#ffffff', padx=25, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Tooltip function (defined at top for scope)
        def create_tooltip(widget, text):
            def on_enter(event):
                tooltip = tk.Toplevel()
                tooltip.wm_overrideredirect(True)
                tooltip.configure(bg='#374151')
                label = tk.Label(tooltip, text=text, bg='#374151', fg='#ffffff', 
                                font=('Segoe UI', 9), padx=8, pady=4)
                label.pack()
                x, y, _, _ = widget.bbox("insert")
                x += widget.winfo_rootx() + 20
                y += widget.winfo_rooty() + 20
                tooltip.geometry(f"+{x}+{y}")
                widget.tooltip = tooltip
            def on_leave(event):
                if hasattr(widget, 'tooltip'):
                    widget.tooltip.destroy()
                    del widget.tooltip
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
        
        # Compact 2-column layout to reduce vertical space
        form_container = tk.Frame(content_frame, bg='#ffffff')
        form_container.pack(fill="both", expand=True)
        
        # Configure grid weights for responsive layout
        form_container.grid_columnconfigure(0, weight=1)
        form_container.grid_columnconfigure(1, weight=1)
        
        # Left Column - Core Information
        left_column = tk.Frame(form_container, bg='#ffffff')
        left_column.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)
        
        # RICE ID (required) with tooltip
        rice_id_frame = tk.Frame(left_column, bg='#ffffff')
        rice_id_frame.pack(fill="x", pady=(0, 10))
        rice_id_label = tk.Label(rice_id_frame, text="🆔 RICE ID * ℹ️", font=('Segoe UI', 10, 'bold'), 
                                bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        rice_id_label.pack(anchor="w")
        rice_id_entry = tk.Entry(rice_id_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                                relief='solid', bd=1, highlightthickness=1, highlightcolor='#3b82f6')
        rice_id_entry.insert(0, profile_data[1])
        rice_id_entry.pack(fill="x", pady=(2, 0))
        
        create_tooltip(rice_id_label, "Unique identifier for this RICE item (e.g., INT-001, RPT-002)")
        
        # Name (required) with tooltip
        name_frame = tk.Frame(left_column, bg='#ffffff')
        name_frame.pack(fill="x", pady=(0, 10))
        name_label = tk.Label(name_frame, text="📝 Name * ℹ️", font=('Segoe UI', 10, 'bold'), 
                             bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        name_label.pack(anchor="w")
        name_entry = tk.Entry(name_frame, font=('Segoe UI', 10), bg='#f9fafb', 
                             relief='solid', bd=1, highlightthickness=1, highlightcolor='#3b82f6')
        name_entry.insert(0, profile_data[2])
        name_entry.pack(fill="x", pady=(2, 0))
        
        create_tooltip(name_label, "Descriptive name for this RICE item")
        
        # Project/Client (readonly - from user's company) with tooltip
        client_frame = tk.Frame(left_column, bg='#ffffff')
        client_frame.pack(fill="x", pady=(0, 10))
        client_label = tk.Label(client_frame, text="🏢 Project/Client (Auto) ℹ️", font=('Segoe UI', 10, 'bold'), 
                               bg='#ffffff', fg='#059669', cursor='question_arrow')
        client_label.pack(anchor="w")
        client_entry = tk.Entry(client_frame, font=('Segoe UI', 10), bg='#f0f9ff', 
                               relief='solid', bd=1, highlightthickness=1, highlightcolor='#3b82f6',
                               state='readonly', readonlybackground='#f0f9ff')
        
        # Get user's company from database
        try:
            cursor = self.db_manager.conn.cursor()
            cursor.execute("SELECT company FROM users WHERE id = ?", (self.db_manager.current_user_id,))
            user_company = cursor.fetchone()
            if user_company and user_company[0]:
                client_entry.configure(state='normal')
                client_entry.delete(0, tk.END)
                client_entry.insert(0, user_company[0])
                client_entry.configure(state='readonly')
            else:
                # Fallback to existing data if no company found
                client_entry.configure(state='normal')
                client_entry.delete(0, tk.END)
                client_entry.insert(0, profile_data[3] or 'No Company Set')
                client_entry.configure(state='readonly')
        except Exception as e:
            # Fallback to existing data on error
            client_entry.configure(state='normal')
            client_entry.delete(0, tk.END)
            client_entry.insert(0, profile_data[3] or 'Error Loading Company')
            client_entry.configure(state='readonly')
        
        client_entry.pack(fill="x", pady=(2, 0))
        
        create_tooltip(client_label, "Auto-populated from your company profile (set during signup)")
        
        # Type (required) with tooltip
        type_frame = tk.Frame(left_column, bg='#ffffff')
        type_frame.pack(fill="x", pady=(0, 10))
        type_label = tk.Label(type_frame, text="🏷️ Type * ℹ️", font=('Segoe UI', 10, 'bold'), 
                             bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        type_label.pack(anchor="w")
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(type_frame, textvariable=type_var, font=('Segoe UI', 10))
        rice_types = [rt[1] for rt in self.db_manager.get_rice_types()]
        type_combo['values'] = rice_types
        if len(profile_data) > 6 and profile_data[6]:
            type_combo.set(profile_data[6])
        type_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(type_label, "Select the RICE item type (Interface, Report, Conversion, Extension)")
        
        # Enable search in type dropdown
        def filter_type_values(event):
            typed = type_var.get().lower()
            if typed == '':
                type_combo['values'] = rice_types
            else:
                filtered = [t for t in rice_types if typed in t.lower()]
                type_combo['values'] = filtered
        type_combo.bind('<KeyRelease>', filter_type_values)
        
        # Right Column - Configuration & Environment
        right_column = tk.Frame(form_container, bg='#ffffff')
        right_column.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)
        
        # Channel Name (optional) with tooltip and refresh
        channel_frame = tk.Frame(right_column, bg='#ffffff')
        channel_frame.pack(fill="x", pady=(0, 10))
        channel_header = tk.Frame(channel_frame, bg='#ffffff')
        channel_header.pack(fill="x")
        channel_label = tk.Label(channel_header, text="📡 Channel Name ℹ️", font=('Segoe UI', 10), 
                                bg='#ffffff', fg='#6b7280', cursor='question_arrow')
        channel_label.pack(side="left")
        refresh_channel_btn = tk.Button(channel_header, text="🔄", font=('Segoe UI', 8), 
                                       bg='#f3f4f6', fg='#6b7280', relief='flat', 
                                       padx=4, pady=2, cursor='hand2', bd=0)
        refresh_channel_btn.pack(side="right")
        
        channel_var = tk.StringVar()
        channel_combo = ttk.Combobox(channel_frame, textvariable=channel_var, font=('Segoe UI', 10))
        
        def load_channels():
            channels = [''] + [ch[1] for ch in self.db_manager.get_file_channels()]
            channel_combo['values'] = channels
            return channels
        
        channels = load_channels()
        if len(profile_data) > 4 and profile_data[4]:
            channel_combo.set(profile_data[4])
        channel_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(channel_label, "Optional: Select file channel for data transfer")
        refresh_channel_btn.configure(command=load_channels)
        
        # Enable search in channel dropdown
        def filter_channel_values(event):
            typed = channel_var.get().lower()
            if typed == '':
                channel_combo['values'] = channels
            else:
                filtered = [c for c in channels if c and typed in c.lower()]
                channel_combo['values'] = [''] + filtered
        channel_combo.bind('<KeyRelease>', filter_channel_values)
        
        # SFTP Profile (optional) with tooltip and refresh
        sftp_frame = tk.Frame(right_column, bg='#ffffff')
        sftp_frame.pack(fill="x", pady=(0, 10))
        sftp_header = tk.Frame(sftp_frame, bg='#ffffff')
        sftp_header.pack(fill="x")
        sftp_label = tk.Label(sftp_header, text="📁 SFTP Profile ℹ️", font=('Segoe UI', 10), 
                             bg='#ffffff', fg='#6b7280', cursor='question_arrow')
        sftp_label.pack(side="left")
        refresh_sftp_btn = tk.Button(sftp_header, text="🔄", font=('Segoe UI', 8), 
                                    bg='#f3f4f6', fg='#6b7280', relief='flat', 
                                    padx=4, pady=2, cursor='hand2', bd=0)
        refresh_sftp_btn.pack(side="right")
        
        sftp_var = tk.StringVar()
        sftp_combo = ttk.Combobox(sftp_frame, textvariable=sftp_var, font=('Segoe UI', 10))
        
        def load_sftp_profiles():
            sftp_profiles = [''] + [sp[1] for sp in self.db_manager.get_sftp_profiles()]
            sftp_combo['values'] = sftp_profiles
            return sftp_profiles
        
        sftp_profiles = load_sftp_profiles()
        if len(profile_data) > 5 and profile_data[5]:
            sftp_combo.set(profile_data[5])
        sftp_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(sftp_label, "Optional: Select SFTP profile for file transfers")
        refresh_sftp_btn.configure(command=load_sftp_profiles)
        
        # Enable search in SFTP dropdown
        def filter_sftp_values(event):
            typed = sftp_var.get().lower()
            if typed == '':
                sftp_combo['values'] = sftp_profiles
            else:
                filtered = [s for s in sftp_profiles if s and typed in s.lower()]
                sftp_combo['values'] = [''] + filtered
        sftp_combo.bind('<KeyRelease>', filter_sftp_values)
        
        # Tenant (required) with tooltip and refresh
        tenant_frame = tk.Frame(right_column, bg='#ffffff')
        tenant_frame.pack(fill="x", pady=(0, 10))
        tenant_header = tk.Frame(tenant_frame, bg='#ffffff')
        tenant_header.pack(fill="x")
        tenant_label = tk.Label(tenant_header, text="🏗️ Tenant * ℹ️", font=('Segoe UI', 10, 'bold'), 
                               bg='#ffffff', fg='#dc2626', cursor='question_arrow')
        tenant_label.pack(side="left")
        refresh_tenant_btn = tk.Button(tenant_header, text="🔄", font=('Segoe UI', 8), 
                                      bg='#f3f4f6', fg='#6b7280', relief='flat', 
                                      padx=4, pady=2, cursor='hand2', bd=0)
        refresh_tenant_btn.pack(side="right")
        
        tenant_var = tk.StringVar()
        tenant_combo = ttk.Combobox(tenant_frame, textvariable=tenant_var, font=('Segoe UI', 10))
        
        def load_tenants():
            try:
                tenants = self.db_manager.get_tenants()
                tenant_list = [f"{t[1]} ({t[2]})" for t in tenants]  # "TENANT_ID (Environment)"
                if not tenant_list:
                    tenant_list = ['TAMICS10_AX1 (Sandbox)']  # Default fallback
                tenant_combo['values'] = tenant_list
                return tenant_list
            except:
                # Fallback if tenant management not set up yet
                tenant_list = ['TAMICS10_AX1 (Sandbox)', 'PROD (Production)', 'TEST (Test)', 'DEV (Development)']
                tenant_combo['values'] = tenant_list
                return tenant_list
        
        tenant_list = load_tenants()
        
        # Set current value
        if len(profile_data) > 7 and profile_data[7]:
            current_tenant = profile_data[7]
            # Try to match existing tenant with new format
            matching_tenant = next((t for t in tenant_list if t.startswith(current_tenant)), None)
            if matching_tenant:
                tenant_combo.set(matching_tenant)
            else:
                tenant_combo.set(f"{current_tenant} (Unknown)")
        else:
            tenant_combo.set("TAMICS10_AX1 (Sandbox)")
        
        tenant_combo.pack(fill="x", pady=(2, 0))
        
        create_tooltip(tenant_label, "Select tenant from configured list (managed in Other Settings)")
        refresh_tenant_btn.configure(command=load_tenants)
        
        # Enable search in tenant dropdown
        def filter_tenant_values(event):
            typed = tenant_var.get().lower()
            if typed == '':
                tenant_combo['values'] = tenant_list
            else:
                filtered = [t for t in tenant_list if typed in t.lower()]
                tenant_combo['values'] = filtered
        tenant_combo.bind('<KeyRelease>', filter_tenant_values)
        
        # Modern button frame
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(pady=(10, 0))
        
        # Real-time validation function
        def validate_field(entry, is_required=False):
            value = entry.get().strip()
            if is_required and not value:
                entry.configure(highlightcolor='#ef4444', highlightbackground='#fecaca')
                return False
            else:
                entry.configure(highlightcolor='#10b981', highlightbackground='#d1fae5')
                return True
        
        # Bind validation to required fields (excluding readonly client field)
        rice_id_entry.bind('<KeyRelease>', lambda e: validate_field(rice_id_entry, True))
        name_entry.bind('<KeyRelease>', lambda e: validate_field(name_entry, True))
        
        def save_changes():
            # Validate all required fields (client is auto-populated, tenant is dropdown)
            valid_rice_id = validate_field(rice_id_entry, True)
            valid_name = validate_field(name_entry, True)
            valid_type = type_var.get().strip() != ''
            valid_tenant = tenant_var.get().strip() != ''
            # Client is always valid since it's auto-populated
            valid_client = True
            
            if not all([valid_rice_id, valid_name, valid_client, valid_type, valid_tenant]):
                self.show_popup("Validation Error", "Please fill in all required fields (marked with *)", "error")
                return
            
            try:
                new_rice_id = rice_id_entry.get().strip()
                new_name = name_entry.get().strip()
                # Get client name from readonly field
                client_entry.configure(state='normal')
                new_client_name = client_entry.get().strip()
                client_entry.configure(state='readonly')
                new_type = type_var.get().strip()
                # Extract tenant ID from dropdown selection (before parentheses)
                tenant_selection = tenant_var.get().strip()
                new_tenant = tenant_selection.split(' (')[0] if ' (' in tenant_selection else tenant_selection
                channel_name = channel_var.get().strip() or None
                sftp_profile_name = sftp_var.get().strip() or None
                
                cursor = self.db_manager.conn.cursor()
                cursor.execute("UPDATE rice_profiles SET rice_id = ?, name = ?, type = ?, client_name = ?, channel_name = ?, sftp_profile_name = ?, tenant = ? WHERE id = ?", 
                             (new_rice_id, new_name, new_type, new_client_name, channel_name, sftp_profile_name, new_tenant, profile_id))
                self.db_manager.conn.commit()
                popup.destroy()
                refresh_callback()
                
                self.show_popup("Success", f"RICE '{new_rice_id}' updated successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update RICE: {str(e)}", "error")
        
        # Modern button styling with enhanced hover effects
        save_btn = tk.Button(btn_frame, text="💾 Save Changes", font=('Segoe UI', 10, 'bold'), 
                            bg='#3b82f6', fg='#ffffff', relief='flat', padx=20, pady=10, 
                            cursor='hand2', bd=0, highlightthickness=0, command=save_changes)
        save_btn.pack(side="left", padx=(0, 15))
        
        cancel_btn = tk.Button(btn_frame, text="✕ Cancel", font=('Segoe UI', 10, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                              cursor='hand2', bd=0, highlightthickness=0, command=popup.destroy)
        cancel_btn.pack(side="left")
        
        # Add hover effects
        def on_save_hover(event):
            save_btn.configure(bg='#2563eb')
        def on_save_leave(event):
            save_btn.configure(bg='#3b82f6')
        def on_cancel_hover(event):
            cancel_btn.configure(bg='#4b5563')
        def on_cancel_leave(event):
            cancel_btn.configure(bg='#6b7280')
        
        save_btn.bind('<Enter>', on_save_hover)
        save_btn.bind('<Leave>', on_save_leave)
        cancel_btn.bind('<Enter>', on_cancel_hover)
        cancel_btn.bind('<Leave>', on_cancel_leave)
    
    def delete_rice_profile(self, profile_id, refresh_callback):
        """Delete RICE profile with confirmation"""
        profiles = self.db_manager.get_rice_profiles()
        profile_name = None
        for profile in profiles:
            if profile[0] == profile_id:
                profile_name = f"{profile[1]} - {profile[2]}"
                break
        
        if not profile_name:
            self.show_popup("Error", "RICE profile not found", "error")
            return
        
        confirm_popup = create_enhanced_dialog(None, "Confirm", 400, 236, modal=False)
        confirm_popup.configure(bg='#ffffff')
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Delete RICE Profile", font=('Segoe UI', 14, 'bold'), 
                bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Delete RICE profile:\n'{profile_name}'?\n\nThis will also delete all scenarios.", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                cursor = self.db_manager.conn.cursor()
                cursor.execute("DELETE FROM scenarios WHERE rice_profile = ?", (str(profile_id),))
                cursor.execute("DELETE FROM rice_profiles WHERE id = ?", (profile_id,))
                self.db_manager.conn.commit()
                confirm_popup.destroy()
                
                # Auto-refresh RICE profiles table
                refresh_callback()
                
                # Show success popup
                self._show_rice_delete_success_popup()
            except Exception as e:
                self.show_popup("Error", f"Failed to delete RICE: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Yes, Delete", font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_delete).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")
    
    def _show_rice_delete_success_popup(self):
        """Show RICE delete success popup"""
        popup = create_enhanced_dialog(None, "Success", 400, 250, modal=False)
        popup.configure(bg='#ffffff')
        popup.resizable(False, False)
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(popup, bg='#10b981', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="✅ Success", 
                               font=('Segoe UI', 14, 'bold'), bg='#10b981', fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message_label = tk.Label(content_frame, text="RICE profile deleted successfully!", 
                                font=('Segoe UI', 10), bg='#ffffff', 
                                justify="left", wraplength=350)
        message_label.pack(pady=(0, 56))  # Move Close button 0.5 inch (36px) lower
        
        # Close button
        close_btn = tk.Button(content_frame, text="Close", 
                             font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                             relief='flat', padx=20, pady=8, cursor='hand2',
                             bd=0, highlightthickness=0,
                             command=popup.destroy)
        close_btn.pack()
        
        popup.focus_set()
