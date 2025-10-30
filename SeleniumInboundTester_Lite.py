#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from ui_components import configure_smooth_styles
from database_manager import DatabaseManager
from selenium_manager import SeleniumManager
from rice_manager import RiceManager
from config_manager import ConfigManager
from selenium_tab_manager import TabManager, center_dialog
from selenium_sftp_manager import SFTPManager
from test_steps_manager import TestStepsManager
from test_users_manager import TestUsersManager
from service_accounts_manager import ServiceAccountsManager

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
        self.test_steps_manager = TestStepsManager(root, self.db_manager, self.show_popup)
        self.test_users_manager = TestUsersManager(root, self.db_manager, self.show_popup)
        self.service_accounts_manager = ServiceAccountsManager(root, self.db_manager, self.show_popup)
        
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
        """Setup the main UI with enhanced enterprise header and responsive design"""
        # Calculate responsive scaling factor based on screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Base design for 1920x1080 (24" monitor reference)
        base_width, base_height = 1920, 1080
        
        # Calculate scaling factors with minimum size protection
        self.scale_x = screen_width / base_width
        self.scale_y = screen_height / base_height
        self.scale_factor = max(min(self.scale_x, self.scale_y), 0.8)  # Minimum 80% scaling
        
        # Use 95% of screen size
        app_width = int(screen_width * 0.95)
        app_height = int(screen_height * 0.95)
        
        # Center on screen
        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 2
        
        self.root.geometry(f"{app_width}x{app_height}+{x}+{y}")
        self.root.state('zoomed')  # Auto full screen on Windows
        self.root.minsize(800, 600)  # Prevent shrinking too small
        
        # Responsive font calculations with readability protection
        font_scale = max(self.scale_factor, 0.9)  # Ensure fonts don't go below 90%
        self.fonts = {
            'title': ('Segoe UI', max(int(16 * font_scale), 14), 'bold'),
            'header': ('Segoe UI', max(int(14 * font_scale), 12), 'bold'),
            'subheader': ('Segoe UI', max(int(12 * font_scale), 11), 'bold'),
            'body': ('Segoe UI', max(int(10 * font_scale), 9)),
            'button': ('Segoe UI', max(int(10 * font_scale), 9), 'bold')
        }
        
        self.padding = {
            'large': int(30 * self.scale_factor),
            'medium': int(20 * self.scale_factor),
            'small': int(15 * self.scale_factor),
            'tiny': int(10 * self.scale_factor)
        }
        
        # Enhanced Header with Enterprise Navigation
        header_height = max(65, int(65 * self.scale_factor))
        header_frame = tk.Frame(self.root, bg='#0f172a', height=header_height)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_frame, bg='#0f172a')
        left_frame.pack(side="left", padx=self.padding['medium'], pady=int(18 * self.scale_factor))
        
        title_label = tk.Label(left_frame, text="FSM Automated Testing", 
                              font=self.fonts['title'], bg='#0f172a', fg='#f8fafc')
        title_label.pack(side="left")
        
        # Version display - read from config
        try:
            import json
            version_path = os.path.join(os.path.dirname(__file__), 'version.json')
            with open(version_path, 'r') as f:
                version_data = json.load(f)
            version_text = f"v{version_data['version']}"
        except:
            version_text = "v1.0.7"
        
        version_label = tk.Label(left_frame, text=version_text, 
                                font=self.fonts['body'], bg='#0f172a', fg='#94a3b8')
        version_label.pack(side="left", padx=(10, 0))
        
        # Right side - User info
        user_frame = tk.Frame(header_frame, bg='#0f172a')
        user_frame.pack(side="right", padx=(0, 25), pady=5)
        
        user_label = tk.Label(user_frame, text=f"👤 Welcome, {self.user['full_name']}", 
                             font=self.fonts['body'], bg='#0f172a', fg='#f8fafc', cursor='hand2')
        user_label.pack(side="left", padx=(0, self.padding['tiny']))
        user_label.bind('<Button-1>', lambda e: self.profile_manager.show_profile())
        
        # Updates button  
        updates_btn = tk.Button(user_frame, text="🔄 Updates",
                               font=self.fonts['button'], bg='#10b981', fg='#ffffff', 
                               relief='flat', padx=int(12 * self.scale_factor), 
                               pady=int(6 * self.scale_factor), cursor='hand2', bd=0,
                               command=self.show_updates)
        updates_btn.pack(side="left", padx=int(10 * self.scale_factor))
        
        # Tools button
        tools_btn = tk.Button(user_frame, text="⚙️ Tools",
                             font=self.fonts['button'], bg='#f59e0b', fg='#ffffff',
                             relief='flat', padx=int(12 * self.scale_factor), 
                             pady=int(6 * self.scale_factor), cursor='hand2', bd=0, 
                             command=self.show_tools)
        tools_btn.pack(side="left", padx=int(5 * self.scale_factor))
        
        signout_btn = tk.Button(user_frame, text="Sign Out", 
                               font=self.fonts['button'], bg='#ef4444', fg='#ffffff', 
                               relief='flat', padx=int(8 * self.scale_factor), 
                               pady=int(4 * self.scale_factor), cursor='hand2',
                               bd=0, highlightthickness=0,
                               command=self.signout)
        signout_btn.pack(side="left", padx=(int(10 * self.scale_factor), 0))
        
        # Main container with sidebar support - responsive sizing
        self.main_container = tk.Frame(self.root, bg='#f8fafc')
        self.main_container.pack(fill="both", expand=True)
        
        # Content area (existing tabs) - responsive padding
        content_padx = max(20, int(30 * self.scale_factor))
        content_pady = max(15, int(30 * self.scale_factor))
        self.content_frame = tk.Frame(self.main_container, bg='#f8fafc')
        self.content_frame.pack(side="left", fill="both", expand=True, padx=content_padx, pady=content_pady)
        
        # Sidebar (always visible) - responsive width + 1 inch (96 pixels)
        sidebar_width = max(300, int(350 * self.scale_factor)) + 96
        self.sidebar_frame = tk.Frame(self.main_container, bg='#ffffff', width=sidebar_width, 
                                     relief='solid', bd=1)
        self.sidebar_frame.pack_propagate(False)  # Maintain fixed width
        self.sidebar_visible = True
        
        # Show sidebar immediately
        sidebar_padding = self.padding.get('medium', 20)
        self.sidebar_frame.pack(side="right", fill="y", padx=(0, sidebar_padding), pady=sidebar_padding)
        
        # Populate sidebar with dashboard content
        self.setup_permanent_dashboard_sidebar()
        
        # Use content_frame for tabs instead of main_container with responsive padding
        main_container = self.content_frame
        
        # Store responsive properties for other components
        self.responsive_config = {
            'scale_factor': self.scale_factor,
            'fonts': self.fonts,
            'padding': self.padding,
            'screen_width': screen_width,
            'screen_height': screen_height
        }
        
        # Initialize tab manager with responsive config
        self.tab_manager = TabManager(self.root)
        # Pass responsive config to tab manager if it supports it
        if hasattr(self.tab_manager, 'set_responsive_config'):
            self.tab_manager.set_responsive_config(self.responsive_config)
        tab_content = self.tab_manager.setup_tab_system(main_container)
        
        # Pass responsive config to all managers
        for manager in [self.rice_manager, self.config_manager, self.sftp_manager, 
                       self.test_steps_manager, self.test_users_manager, self.service_accounts_manager]:
            if hasattr(manager, 'set_responsive_config'):
                manager.set_responsive_config(self.responsive_config)
        
        # Setup tabs
        self.tab_manager.add_tab("📋 RICE List", lambda parent: self.rice_manager.setup_rice_tab_content(parent))
        self.tab_manager.add_tab("🌐 Browser Config", lambda parent: self.config_manager.setup_browser_tab_content(parent))
        self.tab_manager.add_tab("🔗 SFTP Config", lambda parent: self.sftp_manager.setup_sftp_tab_content(parent))
        self.tab_manager.add_tab("📁 File Channel", lambda parent: self.config_manager.setup_file_channel_tab_content(parent))
        self.tab_manager.add_tab("👣 Test Steps", lambda parent: self.test_steps_manager.setup_test_steps_tab(parent))
        self.tab_manager.add_tab("👥 Test Users", lambda parent: self.test_users_manager.setup_test_users_tab(parent))
        self.tab_manager.add_tab("🔑 Other Settings", lambda parent: self.service_accounts_manager.setup_service_accounts_tab(parent))
        
        # Show first tab
        self.tab_manager.show_tab("📋 RICE List")
    
    def show_popup(self, title, message, status):
        """Show popup message with responsive sizing"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        
        # Responsive popup size
        popup_width = int(400 * getattr(self, 'scale_factor', 1.0))
        popup_height = int(250 * getattr(self, 'scale_factor', 1.0))
        center_dialog(popup, popup_width, popup_height)
        popup.configure(bg='#ffffff')
        popup.resizable(False, False)
        popup.transient(self.root)
        popup.grab_set()
        
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
        
        # Header with responsive sizing
        header_height = int(60 * getattr(self, 'scale_factor', 1.0))
        header_frame = tk.Frame(popup, bg=color, height=header_height)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_font = getattr(self, 'fonts', {}).get('header', ('Segoe UI', 14, 'bold'))
        header_label = tk.Label(header_frame, text=f"{icon} {title}", 
                               font=header_font, bg=color, fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content with responsive padding
        content_padding = self.padding.get('medium', 20)
        content_frame = tk.Frame(popup, bg='#ffffff', padx=content_padding, pady=content_padding)
        content_frame.pack(fill="both", expand=True)
        
        message_font = getattr(self, 'fonts', {}).get('body', ('Segoe UI', 10))
        wrap_length = int(350 * getattr(self, 'scale_factor', 1.0))
        message_label = tk.Label(content_frame, text=message, 
                                font=message_font, bg='#ffffff', 
                                justify="left", wraplength=wrap_length)
        message_label.pack(pady=(0, self.padding.get('medium', 20)))
        
        # Close button with responsive sizing
        close_font = getattr(self, 'fonts', {}).get('button', ('Segoe UI', 10, 'bold'))
        close_padx = int(20 * getattr(self, 'scale_factor', 1.0))
        close_pady = int(8 * getattr(self, 'scale_factor', 1.0))
        close_btn = tk.Button(content_frame, text="Close", 
                             font=close_font, bg='#6b7280', fg='#ffffff', 
                             relief='flat', padx=close_padx, pady=close_pady, cursor='hand2',
                             bd=0, highlightthickness=0,
                             command=popup.destroy)
        close_btn.pack()
        
        popup.focus_set()
    
    def signout(self):
        """Sign out user with responsive dialog"""
        confirm_popup = tk.Toplevel(self.root)
        confirm_popup.title("Sign Out")
        
        # Responsive dialog size
        dialog_width = int(400 * getattr(self, 'scale_factor', 1.0))
        dialog_height = int(236 * getattr(self, 'scale_factor', 1.0))
        center_dialog(confirm_popup, dialog_width, dialog_height)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.resizable(False, False)
        confirm_popup.transient(self.root)
        confirm_popup.grab_set()
        
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        header_height = int(50 * getattr(self, 'scale_factor', 1.0))
        header_frame = tk.Frame(confirm_popup, bg='#f59e0b', height=header_height)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_font = getattr(self, 'fonts', {}).get('header', ('Segoe UI', 14, 'bold'))
        header_label = tk.Label(header_frame, text="⚠️ Sign Out", 
                               font=header_font, bg='#f59e0b', fg='#ffffff')
        header_label.pack(expand=True)
        
        content_padding = self.padding.get('medium', 20)
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=content_padding, pady=content_padding)
        content_frame.pack(fill="both", expand=True)
        
        message_font = getattr(self, 'fonts', {}).get('subheader', ('Segoe UI', 11))
        message_label = tk.Label(content_frame, text="Are you sure you want to sign out?", 
                                font=message_font, bg='#ffffff')
        message_label.pack(pady=(0, self.padding.get('medium', 20)))
        
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_signout():
            confirm_popup.destroy()
            
            # Clean up resources
            try:
                self.selenium_manager.close()
            except:
                pass
            try:
                self.db_manager.close()
            except:
                pass
            
            # Clear current content and go directly to login
            for widget in self.root.winfo_children():
                widget.destroy()
            
            # Import and show login screen directly in same window
            from AuthSystem import AuthSystem
            
            # Create new auth system in the same window
            auth = AuthSystem()
            auth.root = self.root  # Use existing window
            auth.root.title("RICE Tester - Login")
            
            # Setup login UI in existing window
            auth.setup_modern_ui()
            
            # Set up the login completion handler
            def on_login_complete():
                user = auth.user
                if user:
                    # Clear login UI
                    for widget in self.root.winfo_children():
                        widget.destroy()
                    
                    # Reinitialize the main app with new user
                    self.__init__(self.root, user)
            
            # Override the cleanup method to handle login completion
            original_cleanup = auth.cleanup_and_exit
            auth.cleanup_and_exit = on_login_complete
        
        button_font = getattr(self, 'fonts', {}).get('button', ('Segoe UI', 10, 'bold'))
        button_padx = int(15 * getattr(self, 'scale_factor', 1.0))
        button_pady = int(6 * getattr(self, 'scale_factor', 1.0))
        
        tk.Button(btn_frame, text="Yes, Sign Out", 
                 font=button_font, bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=button_padx, pady=button_pady, cursor='hand2',
                 bd=0, highlightthickness=0,
                 command=confirm_signout).pack(side="left", padx=(0, self.padding.get('tiny', 10)))
        
        tk.Button(btn_frame, text="Cancel", 
                 font=button_font, bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=button_padx, pady=button_pady, cursor='hand2',
                 bd=0, highlightthickness=0,
                 command=confirm_popup.destroy).pack(side="left")
        
        confirm_popup.focus_set()
    
    def setup_permanent_dashboard_sidebar(self):
        """Setup permanent dashboard sidebar"""
        # Clear and populate sidebar
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
            
        # Sidebar header
        header_height = int(50 * getattr(self, 'scale_factor', 1.0))
        header = tk.Frame(self.sidebar_frame, bg='#1e40af', height=header_height)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_font = getattr(self, 'fonts', {}).get('subheader', ('Segoe UI', 12, 'bold'))
        tk.Label(header, text="🏆 Personal Dashboard", font=header_font,
                bg='#1e40af', fg='#ffffff').pack(expand=True)
        
        # Dashboard content
        content_padding = self.padding.get('small', 15)
        content = tk.Frame(self.sidebar_frame, bg='#ffffff', padx=content_padding, pady=content_padding)
        content.pack(fill="both", expand=True)
        
        # Quick metrics
        summary_font = getattr(self, 'fonts', {}).get('subheader', ('Segoe UI', 11, 'bold'))
        tk.Label(content, text="Today's Summary", font=summary_font,
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, self.padding.get('tiny', 10)))
        
        metrics = [
            ("Tests Run", "12", "#10b981"),
            ("Success Rate", "94%", "#3b82f6"),
            ("Time Saved", "2.5h", "#f59e0b"),
            ("Scenarios", "8", "#8b5cf6")
        ]
        
        for title, value, color in metrics:
            metric_frame = tk.Frame(content, bg='#ffffff')
            metric_frame.pack(fill="x", pady=int(2 * getattr(self, 'scale_factor', 1.0)))
            
            metric_font = getattr(self, 'fonts', {}).get('body', ('Segoe UI', 9))
            tk.Label(metric_frame, text=title, font=metric_font,
                    bg='#ffffff', anchor="w").pack(side="left")
            
            value_font = (metric_font[0], metric_font[1], 'bold')
            tk.Label(metric_frame, text=value, font=value_font,
                    bg='#ffffff', fg=color).pack(side="right")
        
        # Action buttons
        button_font = getattr(self, 'fonts', {}).get('button', ('Segoe UI', 10, 'bold'))
        button_padx = int(15 * getattr(self, 'scale_factor', 1.0))
        button_pady = int(8 * getattr(self, 'scale_factor', 1.0))
        
        tk.Button(content, text="📈 Full Analytics", font=button_font,
                 bg='#3b82f6', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_full_analytics).pack(fill="x", pady=(self.padding.get('medium', 20), self.padding.get('tiny', 5)))
        
        tk.Button(content, text="🏆 Achievements", font=button_font,
                 bg='#8b5cf6', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady, 
                 cursor='hand2', bd=0, command=self.show_achievements).pack(fill="x", pady=self.padding.get('tiny', 5))
    

    
    def show_full_dashboard(self):
        """Show full personal analytics dashboard"""
        try:
            from personal_analytics import PersonalAnalytics
            analytics = PersonalAnalytics(self.db_manager, self.show_popup)
            analytics.show_personal_dashboard()
        except Exception as e:
            self.show_popup("Analytics Error", f"Failed to load dashboard: {str(e)}", "error")
    
    def show_full_analytics(self):
        """Show full analytics dashboard"""
        try:
            from personal_analytics import PersonalAnalytics
            analytics = PersonalAnalytics(self.db_manager, self.show_popup)
            analytics.show_full_analytics()
        except Exception as e:
            self.show_popup("Analytics Error", f"Failed to load analytics: {str(e)}", "error")
    
    def show_achievements(self):
        """Show achievements dashboard"""
        try:
            from personal_analytics import PersonalAnalytics
            analytics = PersonalAnalytics(self.db_manager, self.show_popup)
            analytics.show_achievements()
        except Exception as e:
            self.show_popup("Analytics Error", f"Failed to load achievements: {str(e)}", "error")
    
    def show_updates(self):
        """Show update confirmation dialog first"""
        # Show confirmation dialog first
        confirm_dialog = tk.Toplevel(self.root)
        confirm_dialog.title("🔄 Update Confirmation")
        center_dialog(confirm_dialog, 500, 400)
        confirm_dialog.configure(bg='#ffffff')
        confirm_dialog.resizable(False, False)
        confirm_dialog.transient(self.root)
        confirm_dialog.grab_set()
        
        try:
            confirm_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(confirm_dialog, bg='#3b82f6', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔄 Check for Updates", 
                font=('Segoe UI', 16, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_dialog, bg='#ffffff', padx=25, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        # Warning message
        tk.Label(content_frame, text="⚠️ Update Process Information", 
                font=('Segoe UI', 14, 'bold'), bg='#ffffff', fg='#f59e0b').pack(anchor="w", pady=(0, 15))
        
        info_text = """This will check for RICE Tester updates from GitHub and may:

• Download and install new versions automatically
• Replace current files with updated versions
• Restart the application to apply changes
• Backup current version before updating

⚠️ Make sure to save any unsaved work before proceeding.

Do you want to proceed with the update check?"""
        
        tk.Label(content_frame, text=info_text, font=('Segoe UI', 10), 
                bg='#ffffff', fg='#374151', justify="left", wraplength=450).pack(anchor="w", pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        def proceed_with_update():
            confirm_dialog.destroy()
            self._show_update_loading()
        
        tk.Button(btn_frame, text="✅ Yes, Check for Updates", 
                 font=('Segoe UI', 11, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                 command=proceed_with_update).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="❌ Cancel", 
                 font=('Segoe UI', 11, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                 command=confirm_dialog.destroy).pack(side="left")
    
    def _show_update_loading(self):
        """Show loading screen after user confirms"""
        # Create exciting loading dialog
        loading_dialog = tk.Toplevel(self.root)
        loading_dialog.title("🚀 Checking for Updates")
        center_dialog(loading_dialog, 450, 300)
        loading_dialog.configure(bg='#ffffff')
        loading_dialog.resizable(False, False)
        loading_dialog.transient(self.root)
        loading_dialog.grab_set()
        
        try:
            loading_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Animated header
        header_frame = tk.Frame(loading_dialog, bg='#3b82f6', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🚀 Checking for Updates", 
                              font=('Segoe UI', 16, 'bold'), bg='#3b82f6', fg='#ffffff')
        title_label.pack(expand=True)
        
        # Content with progress
        content_frame = tk.Frame(loading_dialog, bg='#ffffff', padx=30, pady=30)
        content_frame.pack(fill="both", expand=True)
        
        # Progress steps
        steps = [
            "🔍 Connecting to GitHub...",
            "📊 Analyzing repository...",
            "🎆 Checking for awesome updates...",
            "✨ Preparing results..."
        ]
        
        self.current_step = 0
        self.step_label = tk.Label(content_frame, text=steps[0], 
                                  font=('Segoe UI', 12), bg='#ffffff', fg='#1e40af')
        self.step_label.pack(pady=(0, 20))
        
        # Animated progress bar
        self.progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(content_frame, variable=self.progress_var, 
                                     maximum=100, length=350, mode='determinate')
        progress_bar.pack(pady=(0, 15))
        
        # Progress percentage
        self.progress_label = tk.Label(content_frame, text="0%", 
                                      font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#6b7280')
        self.progress_label.pack()
        
        # Fun loading messages
        fun_messages = [
            "🎉 Getting ready for something awesome!",
            "🚀 Launching update rockets...",
            "✨ Sprinkling some magic dust...",
            "🎆 Almost there! Preparing surprises..."
        ]
        
        self.fun_label = tk.Label(content_frame, text=fun_messages[0], 
                                 font=('Segoe UI', 9), bg='#ffffff', fg='#8b5cf6')
        self.fun_label.pack(pady=(10, 0))
        
        # Animate the loading process
        def animate_loading():
            for i in range(4):
                self.step_label.config(text=steps[i])
                self.fun_label.config(text=fun_messages[i])
                
                # Animate progress for this step
                start_progress = i * 25
                end_progress = (i + 1) * 25
                
                for progress in range(start_progress, end_progress + 1, 2):
                    self.progress_var.set(progress)
                    self.progress_label.config(text=f"{progress}%")
                    loading_dialog.update()
                    
                    import time
                    time.sleep(0.05)  # Smooth animation
            
            # Complete loading
            loading_dialog.destroy()
            
            # Now show the actual updater
            try:
                import sys
                import os
                temp_path = os.path.join(os.path.dirname(__file__), 'Temp')
                if temp_path not in sys.path:
                    sys.path.insert(0, temp_path)
                
                from auto_updater import RiceAutoUpdater
                updater = RiceAutoUpdater()
                updater.check_for_updates(show_ui=True)
            except Exception as e:
                self.show_popup("Update Check", f"Auto-updater error: {str(e)}\n\nPlease set up GitHub integration first.", "warning")
        
        # Start animation in background
        import threading
        threading.Thread(target=animate_loading, daemon=True).start()
    
    def show_tools(self):
        """Show tools menu with responsive sizing"""
        tools_popup = tk.Toplevel(self.root)
        tools_popup.title("⚙️ Enterprise Tools")
        
        # Responsive dialog size - expanded for Phase 3 tools + 2 inches
        dialog_width = int(500 * getattr(self, 'scale_factor', 1.0))
        dialog_height = int(792 * getattr(self, 'scale_factor', 1.0))  # 600 + 192 pixels (2 inches)
        center_dialog(tools_popup, dialog_width, dialog_height)
        tools_popup.configure(bg='#ffffff')
        tools_popup.resizable(False, False)
        tools_popup.maxsize(dialog_width, dialog_height)
        
        try:
            tools_popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header with responsive sizing
        header_height = int(60 * getattr(self, 'scale_factor', 1.0))
        header_frame = tk.Frame(tools_popup, bg='#000000', height=header_height)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_font = getattr(self, 'fonts', {}).get('header', ('Segoe UI', 14, 'bold'))
        tk.Label(header_frame, text="Enterprise Tools", font=header_font,
                bg='#000000', fg='#ffffff').pack(expand=True)
        
        # Content with responsive padding
        content_padding = self.padding.get('medium', 20)
        content_frame = tk.Frame(tools_popup, bg='#ffffff', padx=content_padding, pady=content_padding)
        content_frame.pack(fill="both", expand=True)
        
        # Tools buttons with responsive sizing
        button_font = getattr(self, 'fonts', {}).get('subheader', ('Segoe UI', 11, 'bold'))
        button_padx = int(15 * getattr(self, 'scale_factor', 1.0))
        button_pady = int(10 * getattr(self, 'scale_factor', 1.0))
        button_spacing = int(5 * getattr(self, 'scale_factor', 1.0))
        
        tk.Button(content_frame, text="📈 Performance Optimizer", font=button_font,
                 bg='#10b981', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.run_performance_optimizer).pack(fill="x", pady=button_spacing)
        
        tk.Button(content_frame, text="🐙 GitHub Integration", font=button_font,
                 bg='#6f42c1', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_github_integration).pack(fill="x", pady=button_spacing)
        
        # Phase 2 Enhancement Tools
        tk.Button(content_frame, text="🚀 Smart Execution", font=button_font,
                 bg='#3b82f6', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_smart_execution).pack(fill="x", pady=button_spacing)
        
        tk.Button(content_frame, text="📊 Advanced Reporting", font=button_font,
                 bg='#8b5cf6', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_advanced_reporting).pack(fill="x", pady=button_spacing)
        
        tk.Button(content_frame, text="⚙️ Performance Monitor", font=button_font,
                 bg='#f59e0b', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_performance_monitor).pack(fill="x", pady=button_spacing)
        
        tk.Button(content_frame, text="👥 Team Collaboration", font=button_font,
                 bg='#10b981', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_team_collaboration).pack(fill="x", pady=button_spacing)
        
        # Phase 3 Enhancement Tools
        tk.Button(content_frame, text="🤖 Smart Test Generator", font=button_font,
                 bg='#ec4899', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_smart_test_generator).pack(fill="x", pady=button_spacing)
        
        tk.Button(content_frame, text="🎨 Visual Designer", font=button_font,
                 bg='#06b6d4', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_visual_designer).pack(fill="x", pady=button_spacing)
        
        tk.Button(content_frame, text="🏢 Enterprise Dashboard", font=button_font,
                 bg='#7c3aed', fg='#ffffff', relief='flat', padx=button_padx, pady=button_pady,
                 cursor='hand2', bd=0, command=self.show_enterprise_dashboard).pack(fill="x", pady=button_spacing)
        
        close_font = getattr(self, 'fonts', {}).get('button', ('Segoe UI', 10, 'bold'))
        close_pady = int(8 * getattr(self, 'scale_factor', 1.0))
        tk.Button(content_frame, text="Close", font=close_font,
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=button_padx, pady=close_pady,
                 cursor='hand2', bd=0, command=tools_popup.destroy).pack(pady=(self.padding.get('tiny', 10), 0))
    
    def run_performance_optimizer(self):
        """Run performance optimization tools"""
        try:
            import sys
            import os
            temp_path = os.path.join(os.path.dirname(__file__), 'Temp')
            if temp_path not in sys.path:
                sys.path.insert(0, temp_path)
            
            from performance_optimizer import optimize_database
            optimize_database()
            self.show_popup("Success", "Performance optimization completed!", "success")
        except Exception as e:
            self.show_popup("Tools", "Performance optimizer coming soon!", "warning")
    
    def show_github_integration(self):
        """Show GitHub CI/CD integration - Restricted Access"""
        # 🚨 ENHANCED SECURITY: Multi-layer authorization check
        authorized_users = ['vansilleza_fpi', 'van_silleza', 'admin']
        current_username = self.user.get('username', '').lower()
        current_user_id = self.user.get('id', 0)
        
        # Primary check: Username must be in authorized list
        if current_username not in authorized_users:
            self.show_popup("Access Restricted", "GitHub Integration is restricted to authorized users only.\n\nThis feature manages CI/CD pipelines and repository access.", "warning")
            return
        
        # 🚨 SECONDARY SECURITY: Verify user is original account (ID 1-3 reserved for Van)
        # This prevents newly created accounts with same usernames from accessing
        if current_user_id > 3:
            self.show_popup("Access Restricted", "GitHub Integration access denied.\n\nThis feature is restricted to original system administrators only.", "warning")
            return
        
        try:
            from github_integration_manager import GitHubIntegrationManager
            github_manager = GitHubIntegrationManager(self.db_manager, self.show_popup)
            github_manager.show_github_integration_dialog()
        except ImportError:
            self.show_popup("Feature Unavailable", "GitHub Integration module not available. Please update RICE Tester.", "warning")
        except Exception as e:
            self.show_popup("GitHub Integration", f"GitHub CI/CD integration coming soon!\n\nFeatures:\n• Automated testing pipeline\n• Professional releases\n• Team distribution\n• Performance monitoring", "warning")
    
    def show_smart_execution(self):
        """Show smart execution dialog"""
        try:
            from Temp.smart_execution import SmartExecutionManager
            smart_manager = SmartExecutionManager(self.db_path, self.selenium_manager)
            smart_manager.show_smart_execution_dialog(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Smart execution module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open smart execution: {e}", "error")
    
    def show_advanced_reporting(self):
        """Show advanced reporting dialog"""
        try:
            from Temp.advanced_reporting import AdvancedReportingManager
            reporting_manager = AdvancedReportingManager(self.db_manager.db_path)
            reporting_manager.show_advanced_reporting_dialog(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Advanced reporting module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open advanced reporting: {e}", "error")
    
    def show_performance_monitor(self):
        """Show performance monitor"""
        try:
            from Temp.performance_monitor import PerformanceMonitor
            perf_monitor = PerformanceMonitor(self.db_manager.db_path)
            perf_monitor.show_performance_monitor(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Performance monitor module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open performance monitor: {e}", "error")
    
    def show_team_collaboration(self):
        """Show team collaboration dialog"""
        try:
            from Temp.team_collaboration import TeamCollaborationManager
            collab_manager = TeamCollaborationManager(self.db_manager.db_path)
            collab_manager.show_team_collaboration_dialog(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Team collaboration module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open team collaboration: {e}", "error")
    
    def show_smart_test_generator(self):
        """Show smart test generator dialog"""
        try:
            from Temp.ai_test_generator import AITestGenerator
            smart_generator = AITestGenerator(self.db_manager.db_path, self.selenium_manager)
            smart_generator.show_smart_generator_dialog(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Smart test generator module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open smart test generator: {e}", "error")
    
    def show_visual_designer(self):
        """Show visual test designer dialog"""
        try:
            from Temp.visual_test_designer import VisualTestDesigner
            visual_designer = VisualTestDesigner(self.db_manager.db_path)
            visual_designer.show_visual_designer_dialog(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Visual test designer module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open visual test designer: {e}", "error")
    
    def show_enterprise_dashboard(self):
        """Show enterprise dashboard"""
        try:
            from Temp.enterprise_dashboard import EnterpriseDashboard
            dashboard = EnterpriseDashboard(self.db_manager.db_path, self.user)
            dashboard.show_enterprise_dashboard(self.root)
        except ImportError as e:
            self.show_popup("Import Error", f"Enterprise dashboard module not found: {e}", "error")
        except Exception as e:
            self.show_popup("Error", f"Failed to open enterprise dashboard: {e}", "error")

# Security: This module can only be launched through RICE_Tester.py with proper authentication
if __name__ == "__main__":
    print("SECURITY ERROR: Direct launch not allowed")
    print("Please use RICE_Tester.py to launch with proper authentication")
    input("Press Enter to exit...")
    exit(1)