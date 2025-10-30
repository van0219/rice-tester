#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# BACKUP FILE - Original SeleniumInboundTester_Lite.py before modular breakdown
# Created for future reference - DO NOT MODIFY

import tkinter as tk
from tkinter import ttk
from ui_components import configure_smooth_styles
from database_manager import DatabaseManager
from selenium_manager import SeleniumManager
from rice_manager import RiceManager
from config_manager import ConfigManager
from selenium_tab_manager import TabManager, center_dialog
from selenium_sftp_manager import SFTPManager

class SeleniumInboundTester:
    def __init__(self, root, user=None):
        self.root = root
        self.user = user or {'id': 1, 'username': 'demo', 'full_name': 'Demo User'}
        
        # Initialize managers
        self.db_manager = DatabaseManager(self.user['id'])
        self.selenium_manager = SeleniumManager()
        self.rice_manager = RiceManager(root, self.db_manager, self.show_popup)
        self.config_manager = ConfigManager(root, self.db_manager, self.selenium_manager, self.show_popup)
        self.sftp_manager = SFTPManager(self.db_manager, self.show_popup)
        
        from profile_manager import ProfileManager
        self.profile_manager = ProfileManager(root, self.user, self.db_manager, self.show_popup)
        
        # Configure UI
        configure_smooth_styles()
        self.root.title("FSM Automated Testing")
        self.root.configure(bg='#f1f5f9')
        
        # Set custom icon
        try:
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(script_dir, "infor_logo.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
            else:
                # Fallback to PNG
                png_path = os.path.join(script_dir, "infor_logo.png")
                if os.path.exists(png_path):
                    self.icon_image = tk.PhotoImage(file=png_path)
                    self.root.iconphoto(False, self.icon_image)
        except Exception as e:
            print(f"Icon loading failed: {e}")
            pass
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main UI"""
        # Header
        header_frame = tk.Frame(self.root, bg='#0f172a', height=65)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="FSM Automated Testing", 
                              font=('Segoe UI', 16, 'bold'), bg='#0f172a', fg='#f8fafc')
        title_label.pack(side="left", padx=25, pady=18)
        
        # User info
        user_frame = tk.Frame(header_frame, bg='#0f172a')
        user_frame.pack(side="right", padx=(0, 25), pady=5)
        
        user_label = tk.Label(user_frame, text=f"👤 Welcome, {self.user['full_name']}", 
                             font=('Segoe UI', 10), bg='#0f172a', fg='#f8fafc', cursor='hand2')
        user_label.pack(side="left", padx=(0, 10))
        user_label.bind('<Button-1>', lambda e: self.profile_manager.show_profile())
        
        signout_btn = tk.Button(user_frame, text="Sign Out", 
                               font=('Segoe UI', 9), bg='#ef4444', fg='#ffffff', 
                               relief='flat', padx=8, pady=4, cursor='hand2',
                               bd=0, highlightthickness=0,
                               command=self.signout)
        signout_btn.pack(side="left")
        
        # Main content
        main_container = tk.Frame(self.root, bg='#f8fafc')
        main_container.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Initialize tab manager
        self.tab_manager = TabManager(self.root)
        tab_content = self.tab_manager.setup_tab_system(main_container)
        
        # Setup tabs
        self.tab_manager.add_tab("📋 RICE List", lambda parent: self.rice_manager.setup_rice_tab_content(parent))
        self.tab_manager.add_tab("🌐 Browser Config", lambda parent: self.config_manager.setup_browser_tab_content(parent))
        self.tab_manager.add_tab("🔗 SFTP Config", lambda parent: self.sftp_manager.setup_sftp_tab_content(parent))
        self.tab_manager.add_tab("📁 File Channel", lambda parent: self.config_manager.setup_file_channel_tab_content(parent))
        self.tab_manager.add_tab("👣 Test Steps", lambda parent: self.setup_test_steps_placeholder(parent))
        self.tab_manager.add_tab("👥 Test Users", lambda parent: self.setup_test_users_placeholder(parent))
        self.tab_manager.add_tab("🔑 Service Account", lambda parent: self.setup_service_account_placeholder(parent))
        
        # Show first tab
        self.tab_manager.show_tab("📋 RICE List")
