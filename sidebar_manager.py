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
        self.menu_label = tk.Label(header_frame, text="Dashboard", 
                                  font=('Segoe UI', 14, 'bold'), bg='#f8fafc', fg='#1f2937')
        self.menu_label.pack(side="left", padx=(10, 0), pady=4)
        
        # Keep right side empty for clean design
        
        # Main content area (below header)
        self.content_frame = tk.Frame(content_container, bg='#ffffff')
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))
        
        # Menu items container with better spacing and top padding
        self.menu_container = tk.Frame(self.sidebar_frame, bg='#1e293b')
        self.menu_container.pack(fill="both", expand=True, padx=padding.get('tiny', 10), 
                                pady=(16, 20))
        
        # Menu sections for better organization
        self.menu_sections = {}
        
        # Settings section at bottom with proper spacing
        settings_section = tk.Frame(self.sidebar_frame, bg='#1e293b')
        settings_section.pack(fill="x", side="bottom", padx=padding.get('tiny', 10), pady=(0, 15))
        
        # Visual separator above settings
        separator = tk.Frame(settings_section, bg='#475569', height=1)
        separator.pack(fill="x", pady=(0, 15))
        
        self.settings_btn = tk.Button(settings_section, text="⚙️ Settings", font=('Segoe UI', 11, 'bold'),
                                     bg='#374151', fg='#f1f5f9', relief='flat',
                                     padx=padding.get('small', 15), pady=12, cursor='hand2', bd=0,
                                     anchor='w', activebackground='#4b5563', activeforeground='#ffffff',
                                     command=self.show_settings_menu)
        self.settings_btn.pack(fill="x")
        
        self.settings_menu = None
        
        return self.content_frame
    
    def add_menu_item(self, name, setup_func, icon="📄", section="main"):
        """Add a menu item to the sidebar with proper grouping"""
        # Get responsive values
        if self.responsive_config:
            fonts = self.responsive_config.get('fonts', {})
            scale_factor = self.responsive_config.get('scale_factor', 1.0)
            padding = self.responsive_config.get('padding', {})
        else:
            fonts = {'button': ('Segoe UI', 10, 'bold')}
            scale_factor = 1.0
            padding = {'tiny': 10}
        
        # Create section if it doesn't exist
        if section not in self.menu_sections:
            self.create_menu_section(section)
        
        section_frame = self.menu_sections[section]
        
        # Create menu button with improved spacing
        button_font = fonts.get('button', ('Segoe UI', 11, 'bold'))
        button_padx = int(18 * scale_factor)
        button_pady = int(14 * scale_factor)
        
        # Clean name for display
        display_name = name
        if not name.startswith(icon):
            display_name = f"{icon} {name.replace('📋 ', '').replace('🌐 ', '').replace('🔗 ', '').replace('📁 ', '').replace('👣 ', '').replace('👥 ', '').replace('🔑 ', '')}"
        
        menu_btn = tk.Button(section_frame, text=display_name, 
                           font=button_font, bg='#334155', fg='#f1f5f9',
                           relief='flat', padx=button_padx, pady=button_pady,
                           cursor='hand2', bd=0, anchor='w',
                           activebackground='#475569', activeforeground='#ffffff',
                           command=lambda: self.show_menu_content(name))
        menu_btn.pack(fill="x", pady=8)  # Increased from 5px to 8px for better spacing
        
        # Store menu info
        self.menu_buttons[name] = menu_btn
        self.menu_items[name] = {'setup_func': setup_func, 'icon': icon, 'section': section}
    
    def create_menu_section(self, section_name):
        """Create a menu section with proper spacing and separators"""
        # Add spacing before new section (except first)
        if self.menu_sections:
            spacer = tk.Frame(self.menu_container, bg='#1e293b', height=20)
            spacer.pack(fill="x")
            
            # Add visual separator
            separator = tk.Frame(self.menu_container, bg='#475569', height=1)
            separator.pack(fill="x", padx=10, pady=(0, 15))
        
        # Create section frame
        section_frame = tk.Frame(self.menu_container, bg='#1e293b')
        section_frame.pack(fill="x")
        
        # Store section
        self.menu_sections[section_name] = section_frame
    
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
        
        # Position next to settings button with better positioning
        x = self.settings_btn.winfo_rootx() + self.settings_btn.winfo_width() + 5
        y = self.settings_btn.winfo_rooty() - 140  # Move up more to show all 4 buttons
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
        
        # GitHub Manager (Admin only)
        github_btn = tk.Button(menu_frame, text="🐙 GitHub Manager", 
                              font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                              relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                              anchor='w', command=self.trigger_github)
        
        # Check if user is admin
        is_admin = False
        if hasattr(self, 'parent') and hasattr(self.parent, 'user'):
            username = self.parent.user.get('username', '').lower()
            user_id = self.parent.user.get('id', 0)
            is_admin = username in ['vansilleza_fpi', 'van_silleza', 'admin'] and user_id <= 3
        
        if is_admin:
            github_btn.pack(fill="x")
            github_btn.bind('<Enter>', lambda e: github_btn.configure(bg='#f3f4f6'))
            github_btn.bind('<Leave>', lambda e: github_btn.configure(bg='#ffffff'))
        else:
            github_btn.configure(fg='#9ca3af', cursor='arrow', state='disabled')
            github_btn.pack(fill="x")
        
        # Performance Optimizer
        perf_btn = tk.Button(menu_frame, text="📈 Performance Optimizer", 
                            font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                            relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                            anchor='w', command=self.trigger_performance)
        perf_btn.pack(fill="x")
        perf_btn.bind('<Enter>', lambda e: perf_btn.configure(bg='#f3f4f6'))
        perf_btn.bind('<Leave>', lambda e: perf_btn.configure(bg='#ffffff'))
        
        # TES-070 Document Format
        tes070_btn = tk.Button(menu_frame, text="📄 TES-070 Format", 
                              font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                              relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                              anchor='w', command=self.trigger_tes070_format)
        tes070_btn.pack(fill="x")
        tes070_btn.bind('<Enter>', lambda e: tes070_btn.configure(bg='#f3f4f6'))
        tes070_btn.bind('<Leave>', lambda e: tes070_btn.configure(bg='#ffffff'))
        
        # About
        about_btn = tk.Button(menu_frame, text="ℹ️ About", 
                             font=('Segoe UI', 10), bg='#ffffff', fg='#374151',
                             relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                             anchor='w', command=self.show_about)
        about_btn.pack(fill="x")
        about_btn.bind('<Enter>', lambda e: about_btn.configure(bg='#f3f4f6'))
        about_btn.bind('<Leave>', lambda e: about_btn.configure(bg='#ffffff'))
        
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
        """Trigger GitHub manager with admin verification"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        # Check if user is authorized
        if hasattr(self.parent, 'user'):
            username = self.parent.user.get('username', '').lower()
            user_id = self.parent.user.get('id', 0)
            is_admin = username in ['vansilleza_fpi', 'van_silleza', 'admin'] and user_id <= 3
            
            if is_admin:
                if hasattr(self.parent, 'show_github_integration'):
                    self.parent.show_github_integration()
            else:
                if hasattr(self.parent, 'show_popup'):
                    self.parent.show_popup("Access Restricted", "GitHub Integration is restricted to authorized administrators only.", "warning")
    
    def trigger_performance(self):
        """Trigger Performance Optimizer"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        # Call parent's performance optimizer
        if hasattr(self.parent, 'run_performance_optimizer'):
            self.parent.run_performance_optimizer()
    
    def trigger_tes070_format(self):
        """Show TES-070 document format configuration"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        # Show TES-070 format configuration dialog
        self.show_tes070_format_dialog()
    
    def show_tes070_format_dialog(self):
        """Show enhanced TES-070 document naming convention configuration dialog"""
        popup = tk.Toplevel()
        popup.title("📄 TES-070 Naming Convention")
        center_dialog(popup, 650, 749)  # Reduced height by 0.25 inch (18 pixels)
        popup.configure(bg='#f8fafc')
        popup.resizable(False, False)
        popup.transient(self.parent.root if hasattr(self.parent, 'root') else None)
        popup.grab_set()
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced Header with better description
        header_frame = tk.Frame(popup, bg='#1e40af', height=88)  # Increased by 0.1 inch (7 pixels)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#1e40af')
        header_content.pack(expand=True, fill="both", padx=25, pady=15)
        
        tk.Label(header_content, text="📄 TES-070 Document Naming Convention", 
                font=('Segoe UI', 16, 'bold'), bg='#1e40af', fg='#ffffff').pack(anchor="w")
        tk.Label(header_content, text="Define your custom naming format for TES-070 testing documentation", 
                font=('Segoe UI', 10), bg='#1e40af', fg='#bfdbfe').pack(anchor="w", pady=(5, 0))
        
        # Main Content with optimized spacing
        content_frame = tk.Frame(popup, bg='#f8fafc', padx=25, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        # Purpose explanation section
        purpose_section = tk.Frame(content_frame, bg='#fef3c7', relief='solid', bd=1, 
                                  highlightbackground='#f59e0b', highlightthickness=1)
        purpose_section.pack(fill="x", pady=(0, 15))
        
        purpose_header = tk.Frame(purpose_section, bg='#f59e0b', height=35)
        purpose_header.pack(fill="x")
        purpose_header.pack_propagate(False)
        
        tk.Label(purpose_header, text="ℹ️ Purpose", font=('Segoe UI', 10, 'bold'), 
                bg='#f59e0b', fg='#ffffff').pack(side="left", padx=15, pady=8)
        
        purpose_content = tk.Frame(purpose_section, bg='#fef3c7', padx=15, pady=10)
        purpose_content.pack(fill="x")
        
        purpose_text = "This template defines how TES-070 test documentation files will be automatically named when generated. Use placeholders to create consistent, professional file names that include relevant test information."
        tk.Label(purpose_content, text=purpose_text, font=('Segoe UI', 9), 
                bg='#fef3c7', fg='#92400e', wraplength=580, justify="left").pack(anchor="w")
        
        # Template Configuration section
        config_section = tk.Frame(content_frame, bg='#ffffff', relief='solid', bd=1, 
                                 highlightbackground='#e5e7eb', highlightthickness=1)
        config_section.pack(fill="x", pady=(0, 15))
        
        # Section header
        section_header = tk.Frame(config_section, bg='#f0f9ff', height=40)
        section_header.pack(fill="x")
        section_header.pack_propagate(False)
        
        tk.Label(section_header, text="📝 Template Configuration", font=('Segoe UI', 11, 'bold'), 
                bg='#f0f9ff', fg='#1e40af').pack(side="left", padx=15, pady=10)
        
        # Template content with optimized layout
        template_content = tk.Frame(config_section, bg='#ffffff', padx=20, pady=15)
        template_content.pack(fill="x")
        
        # Template input with enhanced styling
        tk.Label(template_content, text="Document Name Template:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor="w", pady=(0, 8))
        
        # Template entry with focus effects
        template_var = tk.StringVar()
        # Load current template from database
        try:
            if hasattr(self.parent, 'db_manager'):
                current_template = self.parent.db_manager.get_tes070_template()
                template_var.set(current_template)
            else:
                template_var.set("TES-070_{client_name}_{rice_id}_{name}_{date}_v{version}.docx")
        except:
            template_var.set("TES-070_{client_name}_{rice_id}_{name}_{date}_v{version}.docx")
        
        template_entry = tk.Entry(template_content, textvariable=template_var, 
                                 font=('Segoe UI', 11), bg='#f9fafb', relief='solid', bd=1,
                                 highlightbackground='#d1d5db', highlightthickness=1,
                                 insertbackground='#3b82f6')
        template_entry.pack(fill="x", pady=(0, 12), ipady=8)
        
        # Enhanced focus effects
        def on_focus_in(e):
            template_entry.config(highlightbackground='#3b82f6', highlightthickness=2)
        
        def on_focus_out(e):
            template_entry.config(highlightbackground='#d1d5db', highlightthickness=1)
        
        template_entry.bind('<FocusIn>', on_focus_in)
        template_entry.bind('<FocusOut>', on_focus_out)
        
        # Enhanced Help section with better organization
        help_section = tk.Frame(template_content, bg='#e0f2fe', relief='solid', bd=1)
        help_section.pack(fill="x", pady=(0, 12))
        
        tk.Label(help_section, text="Available Placeholders:", font=('Segoe UI', 9, 'bold'), 
                bg='#e0f2fe', fg='#0369a1').pack(anchor="w", padx=15, pady=(10, 5))
        
        # Organized placeholder list
        placeholders = [
            ("{rice_id}", "RICE item ID (e.g., INT001)"),
            ("{name}", "RICE item name (e.g., GLTotal_Outbound)"),
            ("{client_name}", "Project (e.g., FPI)"),
            ("{tenant}", "Tenant ID (e.g., TAMICS10_AX1)"),
            ("{date}", "Current date (YYYYMMDD_HHMMSS format)"),
            ("{version}", "Version number (1, 2, 3, etc.)")
        ]
        
        for placeholder, description in placeholders:
            placeholder_frame = tk.Frame(help_section, bg='#e0f2fe')
            placeholder_frame.pack(fill="x", padx=15, pady=1)
            
            tk.Label(placeholder_frame, text=placeholder, font=('Segoe UI', 9, 'bold'), 
                    bg='#e0f2fe', fg='#0c4a6e').pack(side="left")
            tk.Label(placeholder_frame, text=f" - {description}", font=('Segoe UI', 9), 
                    bg='#e0f2fe', fg='#0369a1').pack(side="left")
        
        # Spacer
        tk.Frame(help_section, bg='#e0f2fe', height=8).pack()
        
        # Enhanced Example with preview
        example_frame = tk.Frame(template_content, bg='#f3f4f6', relief='solid', bd=1)
        example_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(example_frame, text="Example Output:", font=('Segoe UI', 9, 'bold'), 
                bg='#f3f4f6', fg='#374151').pack(anchor="w", padx=12, pady=(8, 2))
        
        example_text = "TES-070_FPI_INT001_GLTotal_Outbound_20250130_143022_v1.docx"
        tk.Label(example_frame, text=example_text, font=('Segoe UI', 10, 'italic'), 
                bg='#f3f4f6', fg='#059669').pack(anchor="w", padx=12, pady=(0, 8))
        
        # Enhanced Action Buttons with better visibility
        btn_frame = tk.Frame(content_frame, bg='#f8fafc')
        btn_frame.pack(fill="x", pady=(15, 10))
        
        def save_template():
            template = template_var.get().strip()
            
            if not template:
                if hasattr(self.parent, 'show_popup'):
                    self.parent.show_popup("⚠️ Template Required", "Please enter a template format for TES-070 document naming.", "warning")
                return
            
            try:
                # Save to database
                if hasattr(self.parent, 'db_manager'):
                    self.parent.db_manager.save_tes070_template(template)
                    popup.destroy()
                    if hasattr(self.parent, 'show_popup'):
                        self.parent.show_popup("✨ Success", "TES-070 document naming convention saved successfully!\n\nNew TES-070 documents will use this format.", "success")
                else:
                    popup.destroy()
                    
            except Exception as e:
                if hasattr(self.parent, 'show_popup'):
                    self.parent.show_popup("❌ Error", f"Failed to save naming convention:\n{str(e)}", "error")
        
        # Enhanced buttons with hover effects
        save_btn = tk.Button(btn_frame, text="💾 Save Naming Convention", font=('Segoe UI', 11, 'bold'), 
                            bg='#059669', fg='#ffffff', relief='flat', padx=25, pady=12, 
                            cursor='hand2', bd=0, highlightthickness=0, command=save_template)
        save_btn.pack(side="right", padx=(15, 0))
        
        cancel_btn = tk.Button(btn_frame, text="❌ Cancel", font=('Segoe UI', 11, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=25, pady=12, 
                              cursor='hand2', bd=0, highlightthickness=0, command=popup.destroy)
        cancel_btn.pack(side="right")
        
        # Enhanced hover effects
        def on_save_enter(e): save_btn.config(bg='#047857')
        def on_save_leave(e): save_btn.config(bg='#059669')
        def on_cancel_enter(e): cancel_btn.config(bg='#4b5563')
        def on_cancel_leave(e): cancel_btn.config(bg='#6b7280')
        
        save_btn.bind('<Enter>', on_save_enter)
        save_btn.bind('<Leave>', on_save_leave)
        cancel_btn.bind('<Enter>', on_cancel_enter)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
        # Focus on template entry
        template_entry.focus()
        template_entry.select_range(0, tk.END)
    
    def show_about(self):
        """Show About dialog with app information"""
        if self.settings_menu:
            self.settings_menu.destroy()
            self.settings_menu = None
        
        about_dialog = tk.Toplevel()
        about_dialog.title("ℹ️ About RICE Tester")
        center_dialog(about_dialog, 600, 500)  # Compact 2-column layout
        about_dialog.configure(bg='#ffffff')
        about_dialog.resizable(False, False)
        about_dialog.transient(self.parent.root if hasattr(self.parent, 'root') else None)
        about_dialog.grab_set()
        
        try:
            about_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(about_dialog, bg='#0f172a', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#0f172a')
        header_content.pack(expand=True, fill="both", padx=25, pady=20)
        
        tk.Label(header_content, text="🧪 RICE Tester", 
                font=('Segoe UI', 18, 'bold'), bg='#0f172a', fg='#ffffff').pack(anchor="w")
        tk.Label(header_content, text="Enterprise FSM Testing Platform", 
                font=('Segoe UI', 11), bg='#0f172a', fg='#94a3b8').pack(anchor="w", pady=(2, 0))
        
        # Content with 2-column layout
        content_frame = tk.Frame(about_dialog, bg='#ffffff', padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        # Two-column container
        columns_frame = tk.Frame(content_frame, bg='#ffffff')
        columns_frame.pack(fill="both", expand=True)
        
        # Left column
        left_column = tk.Frame(columns_frame, bg='#ffffff')
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Right column
        right_column = tk.Frame(columns_frame, bg='#ffffff')
        right_column.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Version info (left column)
        version_frame = tk.Frame(left_column, bg='#f8fafc', relief='solid', bd=1)
        version_frame.pack(fill="x", pady=(0, 10))
        
        version_header = tk.Frame(version_frame, bg='#3b82f6', height=35)
        version_header.pack(fill="x")
        version_header.pack_propagate(False)
        
        tk.Label(version_header, text="📋 Version Information", font=('Segoe UI', 10, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(side="left", padx=15, pady=8)
        
        version_content = tk.Frame(version_frame, bg='#f8fafc', padx=15, pady=12)
        version_content.pack(fill="x")
        
        # Get current version
        try:
            import json
            import os
            version_path = os.path.join(os.path.dirname(__file__), 'version.json')
            if os.path.exists(version_path):
                with open(version_path, 'r') as f:
                    version_data = json.load(f)
                    current_version = version_data.get('version', '1.0.0')
            else:
                current_version = '1.0.0'
        except:
            current_version = '1.0.0'
        
        tk.Label(version_content, text=f"Version: {current_version}", 
                font=('Segoe UI', 10, 'bold'), bg='#f8fafc', fg='#1f2937').pack(anchor="w")
        tk.Label(version_content, text="Build: Enterprise Edition", 
                font=('Segoe UI', 9), bg='#f8fafc', fg='#6b7280').pack(anchor="w", pady=(2, 0))
        
        # Description (left column)
        desc_frame = tk.Frame(left_column, bg='#ffffff', relief='solid', bd=1)
        desc_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        desc_header = tk.Frame(desc_frame, bg='#10b981', height=35)
        desc_header.pack(fill="x")
        desc_header.pack_propagate(False)
        
        tk.Label(desc_header, text="📖 About", font=('Segoe UI', 10, 'bold'), 
                bg='#10b981', fg='#ffffff').pack(side="left", padx=15, pady=8)
        
        desc_content = tk.Frame(desc_frame, bg='#ffffff', padx=15, pady=12)
        desc_content.pack(fill="x")
        
        description = """RICE Tester is an enterprise-grade automated testing platform designed specifically for Infor FSM (Financials and Supply Management) systems. It provides comprehensive test automation capabilities including RICE profile management, scenario execution, and professional reporting.

Key features include browser automation, SFTP testing, email verification, TES-070 documentation generation, and advanced analytics."""
        
        tk.Label(desc_content, text=description, font=('Segoe UI', 9), 
                bg='#ffffff', fg='#374151', wraplength=430, justify="left").pack(anchor="w")
        
        # Features (right column)
        features_frame = tk.Frame(right_column, bg='#fef3c7', relief='solid', bd=1)
        features_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        features_header = tk.Frame(features_frame, bg='#f59e0b', height=35)
        features_header.pack(fill="x")
        features_header.pack_propagate(False)
        
        tk.Label(features_header, text="⭐ Key Features", font=('Segoe UI', 10, 'bold'), 
                bg='#f59e0b', fg='#ffffff').pack(side="left", padx=15, pady=8)
        
        features_content = tk.Frame(features_frame, bg='#fef3c7', padx=15, pady=12)
        features_content.pack(fill="x")
        
        features = [
            "🧪 Test Case Management",
            "🤖 Browser Automation (Chrome/Edge)",
            "📁 SFTP File Transfer Testing",
            "📧 Email Verification System",
            "📄 TES-070 Documentation Generation",
            "📊 Personal Analytics Dashboard",
            "🔄 Auto-Update System",
            "🐙 GitHub CI/CD Integration"
        ]
        
        for feature in features:
            tk.Label(features_content, text=feature, font=('Segoe UI', 9), 
                    bg='#fef3c7', fg='#92400e').pack(anchor="w", pady=1)
        
        # Credits (right column)
        credits_frame = tk.Frame(right_column, bg='#e0f2fe', relief='solid', bd=1)
        credits_frame.pack(fill="x")
        
        credits_header = tk.Frame(credits_frame, bg='#0369a1', height=35)
        credits_header.pack(fill="x")
        credits_header.pack_propagate(False)
        
        tk.Label(credits_header, text="👨‍💻 Credits", font=('Segoe UI', 10, 'bold'), 
                bg='#0369a1', fg='#ffffff').pack(side="left", padx=15, pady=8)
        
        credits_content = tk.Frame(credits_frame, bg='#e0f2fe', padx=15, pady=12)
        credits_content.pack(fill="x")
        
        tk.Label(credits_content, text="Developed by: Van Anthony Silleza", 
                font=('Segoe UI', 10, 'bold'), bg='#e0f2fe', fg='#0c4a6e').pack(anchor="w")
        tk.Label(credits_content, text="Powered by: IQ (Infor Q) AI Assistant", 
                font=('Segoe UI', 9), bg='#e0f2fe', fg='#0369a1').pack(anchor="w", pady=(2, 0))
        tk.Label(credits_content, text="Enterprise FSM Testing Solutions", 
                font=('Segoe UI', 9), bg='#e0f2fe', fg='#0369a1').pack(anchor="w")
        
        # Close button
        tk.Button(content_frame, text="✅ Close", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=25, pady=10, 
                 cursor='hand2', bd=0, command=about_dialog.destroy).pack(pady=(10, 0))