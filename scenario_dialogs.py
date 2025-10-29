#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import os
from rice_dialogs import center_dialog
from Temp.enhanced_popup_system import create_enhanced_dialog, enhanced_center_dialog

class ScenarioDialogs:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def show_child_popup(self, parent_window, title, message, status):
        """Show popup as child of parent window"""
        popup = create_enhanced_dialog(parent_window, title, 320, 180, modal=False)
        popup.configure(bg='#ffffff')
        popup.attributes('-topmost', False)
        popup.resizable(False, False)
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Status colors
        if status == "success":
            icon = "✅"
            color = "#10b981"
        elif status == "warning":
            icon = "⚠️"
            color = "#f59e0b"
        else:
            icon = "❌"
            color = "#ef4444"
        
        # Header
        header_frame = tk.Frame(popup, bg=color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"{icon} {title}", font=('Segoe UI', 12, 'bold'), 
                bg=color, fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=message, font=('Segoe UI', 10), bg='#ffffff', 
                justify="center", wraplength=280).pack(pady=(0, 15))
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=6, cursor='hand2', bd=0, command=popup.destroy).pack()
        
        # Center relative to parent
        parent_window.update_idletasks()
        x = parent_window.winfo_x() + (parent_window.winfo_width() // 2) - 160
        y = parent_window.winfo_y() + (parent_window.winfo_height() // 2) - 90
        popup.geometry(f"320x180+{x}+{y}")
        
        popup.focus_set()
    
    def show_download_confirmation(self, file_path, original_name):
        """Show custom download confirmation dialog"""
        confirm_popup = create_enhanced_dialog(None, "Download File", 400, 200, modal=False)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.attributes('-topmost', False)
        confirm_popup.resizable(False, False)
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        header_frame = tk.Frame(confirm_popup, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📥 Download File", font=('Segoe UI', 14, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"Do you want to download:\n'{original_name}'?", 
                font=('Segoe UI', 10), bg='#ffffff', justify="center").pack(pady=(0, 20))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def proceed_download():
            confirm_popup.destroy()
            from tkinter import filedialog
            import shutil
            
            save_path = filedialog.asksaveasfilename(
                title="Save File As",
                initialfile=original_name,
                defaultextension=os.path.splitext(original_name)[1],
                filetypes=[("All Files", "*.*")]
            )
            
            if save_path:
                shutil.copy2(file_path, save_path)
                self.show_popup("Success", f"File saved to: {save_path}", "success")
        
        tk.Button(btn_frame, text="Yes, Download", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=proceed_download).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2', bd=0, command=confirm_popup.destroy).pack(side="left")