#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning without blinking"""
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    w = width if width else 400
    h = height if height else 300
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()

class SidebarManager:
    def __init__(self, parent):
        self.parent = parent
        self.menu_items = {}
        self.menu_buttons = {}
        self.active_menu = None
        self.responsive_config = None
        self.sidebar_visible = True
        self.sidebar_frame = None
        self.content_frame = None
        self.hamburger_btn = None
        self.floating_btn = None
        
    def set_responsive_config(self, config):
        """Set responsive configuration"""
        self.responsive_config = config
        
    def setup_sidebar_system(self, container):
        """Setup sidebar system with menu and content area"""
        # Main container with sidebar and content
        self.main_container = tk.Frame(container, bg='#f8fafc')
        self.main_container.pack(fill="both", expand=True)
        
        # Get responsive values
        if self.responsive_config:
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
            fonts = self.responsive_config.get('fonts', {})
            padding = self.responsive_config.get('padding', {})
        else:
            scale_factor = 1.0
            fonts = {'button': ('Segoe UI', 10, 'bold')}
            padding = {'small': 15, 'tiny': 10}
        
        # Sidebar menu (left side)
        sidebar_width = max(250, int(280 * scale_factor))
        self.sidebar_frame = tk.Frame(self.main_container, bg='#1e293b', width=sidebar_width)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        
        # Content area with header
        content_container = tk.Frame(self.main_container, bg='#f8fafc')
        content_container.pack(side="right", fill="both", expand=True)
        
        # Header area (compact height)
        header_frame = tk.Frame(content_container, bg='#f8fafc', height=30)
        header_frame.pack(fill="x", padx=15, pady=(5, 0))
        header_frame.pack_propagate(False)
        
        # Hamburger button in header
        hamburger_font = ('Segoe UI', 12, 'bold')
        self.hamburger_btn = tk.Button(header_frame, text="☰", font=hamburger_font,
                                      bg='#f8fafc', fg='#000000', relief='flat',
                                      padx=6, pady=2, cursor='hand2', bd=0,
                                      activebackground='#e5e7eb', activeforeground='#000000',
                                      command=self.toggle_sidebar)
        self.hamburger_btn.pack(side="left", pady=4)
        
        # Current menu label next to hamburger
        self.menu_label = tk.Label(header_frame, text="RICE List", 
                                  font=('Segoe UI', 14, 'bold'), bg='#f8fafc', fg='#1f2937')
        self.menu_label.pack(side="left", padx=(10, 0), pady=4)
        
        # Keep right side empty for clean design
        
        # Main content area (below header)
        self.content_frame = tk.Frame(content_container, bg='#ffffff')
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Menu items container
        self.menu_container = tk.Frame(self.sidebar_frame, bg='#1e293b')
        self.menu_container.pack(fill="both", expand=True, padx=padding.get('tiny', 10), 
                                pady=padding.get('small', 15))
        
        # Settings icon at bottom
        settings_frame = tk.Frame(self.sidebar_frame, bg='#1e293b', height=60)
        settings_frame.pack(fill="x", side="bottom")
        settings_frame.pack_propagate(False)
        
        self.settings_btn = tk.Button(settings_frame, text="⚙️ Settings", font=('Segoe UI', 12, 'bold'),
                                     bg='#1e293b', fg='#f1f5f9', relief='flat',
                                     padx=padding.get('small', 15), pady=10, cursor='hand2', bd=0,
                                     anchor='w', activebackground='#334155', activeforeground='#ffffff',
                                     command=self.show_settings_menu)
        self.settings_btn.pack(fill="x", padx=padding.get('tiny', 10))
        
        self.settings_menu = None
        
        return self.content_frame
    
    def add_menu_item(self, name, setup_func, icon="📄"):
        """Add a menu item to the sidebar"""
        # Get responsive values
        if self.responsive_config:
            fonts = self.responsive_config.get('fonts', {})
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
            padding = self.responsive_config.get('padding', {})
        else:
            fonts = {'button': ('Segoe UI', 10, 'bold')}
            scale_factor = 1.0
            padding = {'tiny': 10}
        
        # Create menu button
        button_font = fonts.get('button', ('Segoe UI', 10, 'bold'))
        button_padx = int(15 * scale_factor)
        button_pady = int(12 * scale_factor)
        
        # Clean name for display (remove emoji if already present)
        display_name = name
        if not name.startswith(icon):
            display_name = f"{icon} {name.replace('📋 ', '').replace('🌐 ', '').replace('🔗 ', '').replace('📁 ', '').replace('👣 ', '').replace('👥 ', '').replace('🔑 ', '')}"
        
        menu_btn = tk.Button(self.menu_container, text=display_name, 
                           font=button_font, bg='#334155', fg='#f1f5f9',
                           relief='flat', padx=button_padx, pady=button_pady,
                           cursor='hand2', bd=0, anchor='w',
                           activebackground='#475569', activeforeground='#ffffff',
                           command=lambda: self.show_menu_content(name))
        menu_btn.pack(fill="x", pady=padding.get('tiny', 5))
        
        # Store menu info
        self.menu_buttons[name] = menu_btn
        self.menu_items[name] = {'setup_func': setup_func, 'icon': icon}
    
    def show_menu_content(self, name):
        """Show selected menu content"""
        # Get responsive values
        if self.responsive_config:
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
        else:
            scale_factor = 1.0
        
        # Update button styles
        for menu_name, btn in self.menu_buttons.items():
            if menu_name == name:
                # Active menu style
                btn.configure(bg='#3b82f6', fg='#ffffff',
                             activebackground='#2563eb', activeforeground='#ffffff')
            else:
                # Inactive menu style
                btn.configure(bg='#334155', fg='#f1f5f9',
                             activebackground='#475569', activeforeground='#ffffff')
        
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # No form title needed - removed for more space
        
        # Content area
        content_area = tk.Frame(self.content_frame, bg='#ffffff')
        content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Update header menu label
        if hasattr(self, 'menu_label'):
            self.menu_label.configure(text=name)
        
        # Execute menu setup function
        if name in self.menu_items:
            self.menu_items[name]['setup_func'](content_area)
        
        self.active_menu = name
    
    def toggle_sidebar(self):
        """Toggle sidebar between minimized and full width"""
        if self.sidebar_visible:
            # Minimize sidebar - show only icons
            self.minimize_sidebar()
            self.sidebar_visible = False
        else:
            # Maximize sidebar - show full menu
            self.maximize_sidebar()
            self.sidebar_visible = True
    
    def minimize_sidebar(self):
        """Minimize sidebar to show only icons"""
        # Get responsive values
        if self.responsive_config:
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
            padding = self.responsive_config.get('padding', {})
        else:
            scale_factor = 1.0
            padding = {'small': 15, 'tiny': 10}
        
        # Change sidebar width to minimal
        minimal_width = max(80, int(90 * scale_factor))
        self.sidebar_frame.configure(width=minimal_width)
        
        # Hide menu text, show only icons
        for name, btn in self.menu_buttons.items():
            icon = self.menu_items[name].get('icon', '📄')
            btn.configure(text=icon, padx=8)
        
        # Hamburger button stays in header - no position change needed
    
    def maximize_sidebar(self):
        """Maximize sidebar to show full menu with text"""
        # Get responsive values
        if self.responsive_config:
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
            padding = self.responsive_config.get('padding', {})
        else:
            scale_factor = 1.0
            padding = {'small': 15}
        
        # Restore full sidebar width
        full_width = max(250, int(280 * scale_factor))
        self.sidebar_frame.configure(width=full_width)
        
        # Show full menu text with icons
        for name, btn in self.menu_buttons.items():
            icon = self.menu_items[name].get('icon', '📄')
            clean_name = name.replace('📋 ', '').replace('🌐 ', '').replace('🔗 ', '').replace('📁 ', '').replace('👣 ', '').replace('👥 ', '').replace('🔑 ', '')
            display_name = f"{icon} {clean_name}"
            btn.configure(text=display_name, padx=15)
        
        # Hamburger button stays in header - no position change needed
    
    def show_settings_menu(self):
        """Show settings popup menu next to settings icon"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
            return
        
        # Create popup menu
        self.settings_menu = tk.Toplevel()
        self.settings_menu.wm_overrideredirect(True)
        self.settings_menu.configure(bg='#ffffff', relief='solid', bd=1)
        
        # Position next to settings button
        x = self.settings_btn.winfo_rootx() + self.settings_btn.winfo_width() + 5
        y = self.settings_btn.winfo_rooty() - 60
        self.settings_menu.geometry(f"+{x}+{y}")
        
        # Menu items
        menu_frame = tk.Frame(self.settings_menu, bg='#ffffff', padx=5, pady=5)
        menu_frame.pack()
        
        # Check for Updates
        update_btn = tk.Button(menu_frame, text="🔄 Check for Updates", 
                              font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                              relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                              anchor='w', command=self.trigger_updates)
        update_btn.pack(fill="x")
        update_btn.bind('<Enter>', lambda e: update_btn.configure(bg='#f3f4f6'))
        update_btn.bind('<Leave>', lambda e: update_btn.configure(bg='#ffffff'))
        
        # Performance Optimizer
        perf_btn = tk.Button(menu_frame, text="📈 Performance Optimizer", 
                            font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                            relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                            anchor='w', command=self.trigger_performance)
        perf_btn.pack(fill="x")
        perf_btn.bind('<Enter>', lambda e: perf_btn.configure(bg='#f3f4f6'))
        perf_btn.bind('<Leave>', lambda e: perf_btn.configure(bg='#ffffff'))
        
        # GitHub Manager (Van only)
        github_btn = tk.Button(menu_frame, text="🐙 GitHub Manager", 
                              font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                              relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                              anchor='w', command=self.trigger_github)
        
        # Check if user is Van
        if hasattr(self, 'parent') and hasattr(self.parent, 'user'):
            username = self.parent.user.get('username', '').lower()
            user_id = self.parent.user.get('id', 0)
            is_van = username in ['vansilleza_fpi', 'van_silleza', 'admin'] and user_id <= 3
        else:
            is_van = False
        
        if is_van:
            github_btn.pack(fill="x")
            github_btn.bind('<Enter>', lambda e: github_btn.configure(bg='#f3f4f6'))
            github_btn.bind('<Leave>', lambda e: github_btn.configure(bg='#ffffff'))
        else:
            github_btn.configure(fg='#9ca3af', cursor='arrow', state='disabled')
            github_btn.pack(fill="x")
        
        # Close menu when clicking outside
        def close_menu(event=None):
            if self.settings_menu:
                self.settings_menu.destroy()
                self.settings_menu = None
        
        self.settings_menu.bind('<FocusOut>', close_menu)
        self.settings_menu.focus_set()
    
    def trigger_updates(self):
        """Trigger updates functionality"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        # Call parent's show_updates method
        if hasattr(self.parent, 'show_updates'):
            self.parent.show_updates()
    
    def trigger_github(self):
        """Trigger GitHub manager"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        # Call parent's GitHub integration
        if hasattr(self.parent, 'show_github_integration'):
            self.parent.show_github_integration()
    
    def trigger_performance(self):
        """Trigger Performance Optimizer"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        # Call parent's performance optimizer
        if hasattr(self.parent, 'run_performance_optimizer'):
            self.parent.run_performance_optimizer()