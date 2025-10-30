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
        
        popup = create_enhanced_dialog(None, "Edit RICE Profile", 500, 350, modal=False)
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="RICE ID:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=5)
        rice_id_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        rice_id_entry.insert(0, profile_data[1])
        rice_id_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        
        tk.Label(frame, text="Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=5)
        name_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        name_entry.insert(0, profile_data[2])
        name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Project/Client
        tk.Label(frame, text="Project/Client:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky="w", pady=5)
        client_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        client_entry.insert(0, profile_data[3] or '')  # client_name is index 3
        client_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Type (dropdown)
        tk.Label(frame, text="Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky="w", pady=5)
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(frame, textvariable=type_var, width=27, font=('Segoe UI', 10), state='readonly')
        rice_types = [rt[1] for rt in self.db_manager.get_rice_types()]
        type_combo['values'] = rice_types
        if len(profile_data) > 6 and profile_data[6]:  # type_name is index 6
            type_combo.set(profile_data[6])
        type_combo.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Channel Name (dropdown - optional)
        tk.Label(frame, text="Channel Name (Optional):", font=('Segoe UI', 10), bg='#ffffff').grid(row=4, column=0, sticky="w", pady=5)
        channel_var = tk.StringVar()
        channel_combo = ttk.Combobox(frame, textvariable=channel_var, width=27, font=('Segoe UI', 10))
        channels = [''] + [ch[1] for ch in self.db_manager.get_file_channels()]  # Add empty option
        channel_combo['values'] = channels
        if len(profile_data) > 4 and profile_data[4]:  # channel_name is index 4
            channel_combo.set(profile_data[4])
        channel_combo.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        # SFTP Profile (dropdown - optional)
        tk.Label(frame, text="SFTP Profile (Optional):", font=('Segoe UI', 10), bg='#ffffff').grid(row=5, column=0, sticky="w", pady=5)
        sftp_var = tk.StringVar()
        sftp_combo = ttk.Combobox(frame, textvariable=sftp_var, width=27, font=('Segoe UI', 10))
        sftp_profiles = [''] + [sp[1] for sp in self.db_manager.get_sftp_profiles()]  # Add empty option
        sftp_combo['values'] = sftp_profiles
        if len(profile_data) > 5 and profile_data[5]:  # sftp_profile_name is index 5
            sftp_combo.set(profile_data[5])
        sftp_combo.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        
        # Tenant
        tk.Label(frame, text="Tenant:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=6, column=0, sticky="w", pady=5)
        tenant_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        if len(profile_data) > 7 and profile_data[7]:  # tenant is index 7
            tenant_entry.insert(0, profile_data[7])
        else:
            tenant_entry.insert(0, "TAMICS10_AX1")  # Default value
        tenant_entry.grid(row=6, column=1, sticky="ew", padx=10, pady=5)
        
        frame.grid_columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        def save_changes():
            new_rice_id = rice_id_entry.get().strip()
            new_name = name_entry.get().strip()
            new_client_name = client_entry.get().strip()
            new_type = type_var.get().strip()
            new_tenant = tenant_entry.get().strip()
            
            if not all([new_rice_id, new_name, new_client_name, new_type, new_tenant]):
                self.show_popup("Error", "Please fill in required fields (RICE ID, Name, Project/Client, Type, Tenant)", "error")
                return
            
            try:
                channel_name = channel_var.get().strip() or None
                sftp_profile_name = sftp_var.get().strip() or None
                
                cursor = self.db_manager.conn.cursor()
                cursor.execute("UPDATE rice_profiles SET rice_id = ?, name = ?, type = ?, client_name = ?, channel_name = ?, sftp_profile_name = ?, tenant = ? WHERE id = ?", 
                             (new_rice_id, new_name, new_type, new_client_name, channel_name, sftp_profile_name, new_tenant, profile_id))
                self.db_manager.conn.commit()
                popup.destroy()
                # Auto-refresh RICE profiles table
                refresh_callback()
                
                self.show_popup("Success", f"RICE '{new_rice_id}' updated successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update RICE: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
    
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
