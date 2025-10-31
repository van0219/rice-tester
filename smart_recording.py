#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import json
import base64
import io
from PIL import Image
import threading

class SmartRecording:
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.driver = None
        self.recording = False
        self.recorded_steps = []
        self.screenshots = {}  # Store screenshots for each step
        self.element_highlights = []  # Track highlighted elements
        self.wait_conditions = []  # Smart wait detection
        self.last_screenshot = None
        self.step_counter = 0
        
    def show_smart_recording_dialog(self):
        """Enhanced Smart Recording interface with Phase 2 improvements"""
        dialog = tk.Toplevel()
        dialog.title("🎬 Smart Recording Studio")
        
        # Enhanced popup system integration
        from selenium_tab_manager import center_dialog
        
        # Responsive sizing based on screen
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        # Calculate responsive dimensions with better proportions
        dialog_width = min(800, int(screen_width * 0.55))
        dialog_height = max(750, min(950, int(screen_height * 0.8)))
        
        center_dialog(dialog, dialog_width, dialog_height)
        dialog.configure(bg='#ffffff')
        dialog.resizable(True, True)
        dialog.minsize(650, 650)
        dialog.maxsize(1000, 1200)
        
        try:
            dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced header with gradient-like styling
        header_frame = tk.Frame(dialog, bg='#ec4899', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#ec4899')
        header_content.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Enhanced title with subtitle
        title_frame = tk.Frame(header_content, bg='#ec4899')
        title_frame.pack(side="left")
        
        tk.Label(title_frame, text="🎬 Smart Recording Studio", 
                font=('Segoe UI', 18, 'bold'), bg='#ec4899', fg='#ffffff').pack(anchor='w')
        tk.Label(title_frame, text="Intelligent browser interaction capture", 
                font=('Segoe UI', 10), bg='#ec4899', fg='#f8d7da').pack(anchor='w')
        
        # Enhanced status indicator with recording state
        status_frame = tk.Frame(header_content, bg='#ec4899')
        status_frame.pack(side="right")
        
        self.header_status = tk.Label(status_frame, text="● Ready", 
                                     font=('Segoe UI', 12, 'bold'), bg='#ec4899', fg='#ffffff')
        self.header_status.pack()
        
        self.recording_time = tk.Label(status_frame, text="00:00", 
                                      font=('Segoe UI', 9), bg='#ec4899', fg='#f8d7da')
        self.recording_time.pack()
        
        # Enhanced content with better organization
        content_frame = tk.Frame(dialog, bg='#ffffff', padx=30, pady=30)
        content_frame.pack(fill="both", expand=True)
        
        # Enhanced instructions with visual hierarchy
        instruction_frame = tk.Frame(content_frame, bg='#f8fafc', relief='solid', bd=1)
        instruction_frame.pack(fill='x', pady=(0, 25))
        
        inst_header = tk.Frame(instruction_frame, bg='#e5e7eb', height=35)
        inst_header.pack(fill='x')
        inst_header.pack_propagate(False)
        
        tk.Label(inst_header, text="📋 Recording Workflow", font=('Segoe UI', 12, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        inst_content = tk.Frame(instruction_frame, bg='#f8fafc')
        inst_content.pack(fill='x', padx=20, pady=15)
        
        instructions = [
            "1️⃣ Configure your target URL and browser settings",
            "2️⃣ Click 'Start Recording' to launch the browser", 
            "3️⃣ Perform your test actions naturally in the browser",
            "4️⃣ Watch as steps are captured automatically with smart selectors",
            "5️⃣ Stop recording and save as reusable test step groups"
        ]
        
        for instruction in instructions:
            tk.Label(inst_content, text=instruction, font=('Segoe UI', 10), 
                    bg='#f8fafc', fg='#374151', anchor='w').pack(fill='x', pady=2)
        
        # Enhanced status with visual indicators
        status_frame = tk.Frame(content_frame, bg='#ffffff')
        status_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(status_frame, text="🔄 Recording Status:", font=('Segoe UI', 11, 'bold'), 
                bg='#ffffff', fg='#374151').pack(side='left')
        
        self.status_label = tk.Label(status_frame, text="Ready to record", 
                                   font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#10b981')
        self.status_label.pack(side='left', padx=(10, 0))
        
        # Recording metrics
        self.metrics_frame = tk.Frame(content_frame, bg='#f8fafc', relief='solid', bd=1)
        self.metrics_frame.pack(fill='x', pady=(0, 20))
        
        metrics_header = tk.Frame(self.metrics_frame, bg='#e5e7eb', height=30)
        metrics_header.pack(fill='x')
        metrics_header.pack_propagate(False)
        
        tk.Label(metrics_header, text="📊 Session Metrics", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        metrics_content = tk.Frame(self.metrics_frame, bg='#f8fafc')
        metrics_content.pack(fill='x', padx=15, pady=10)
        
        # Metrics display
        metrics_grid = tk.Frame(metrics_content, bg='#f8fafc')
        metrics_grid.pack(fill='x')
        
        self.steps_count = tk.Label(metrics_grid, text="Steps: 0", font=('Segoe UI', 9), 
                                   bg='#f8fafc', fg='#6b7280')
        self.steps_count.pack(side='left', padx=(0, 20))
        
        self.duration_label = tk.Label(metrics_grid, text="Duration: 00:00", font=('Segoe UI', 9), 
                                      bg='#f8fafc', fg='#6b7280')
        self.duration_label.pack(side='left', padx=(0, 20))
        
        self.last_action = tk.Label(metrics_grid, text="Last Action: None", font=('Segoe UI', 9), 
                                   bg='#f8fafc', fg='#6b7280')
        self.last_action.pack(side='left')
        
        # Enhanced URL configuration section
        url_section = tk.Frame(content_frame, bg='#ffffff')
        url_section.pack(fill='x', pady=(0, 20))
        
        tk.Label(url_section, text="🌐 Target Configuration", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 10))
        
        # URL input with validation
        url_input_frame = tk.Frame(url_section, bg='#ffffff')
        url_input_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(url_input_frame, text="Starting URL:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor="w", pady=(0, 5))
        
        self.url_var = tk.StringVar()
        self.url_combo = ttk.Combobox(url_input_frame, textvariable=self.url_var, 
                                     font=('Segoe UI', 11), height=8)
        
        # Load FSM URLs and set default from browser config
        fsm_urls = self.get_fsm_urls()
        self.url_combo['values'] = fsm_urls
        
        # Set default URL from browser config
        browser_config = self.get_browser_config()
        if browser_config and browser_config.get('base_url'):
            self.url_combo.set(browser_config['base_url'])
        elif fsm_urls:
            self.url_combo.set(fsm_urls[0])
        else:
            self.url_combo.set("https://")
        
        self.url_combo.pack(fill="x", ipady=6)
        
        # URL validation indicator
        self.url_validation = tk.Label(url_input_frame, text="", font=('Segoe UI', 9), 
                                      bg='#ffffff', fg='#10b981')
        self.url_validation.pack(anchor='w', pady=(2, 0))
        
        # URL validation function
        def validate_url(*args):
            url = self.url_var.get()
            if url and (url.startswith('http://') or url.startswith('https://')):
                self.url_validation.config(text="✅ Valid URL format", fg='#10b981')
            elif url:
                self.url_validation.config(text="⚠️ URL should start with http:// or https://", fg='#f59e0b')
            else:
                self.url_validation.config(text="❌ URL is required", fg='#ef4444')
        
        self.url_var.trace('w', validate_url)
        validate_url()  # Initial validation
        
        # Enhanced browser config display
        if browser_config:
            config_frame = tk.Frame(url_section, bg='#e0f2fe', relief='solid', bd=1)
            config_frame.pack(fill='x', pady=(10, 0))
            
            config_header = tk.Frame(config_frame, bg='#0284c7', height=25)
            config_header.pack(fill='x')
            config_header.pack_propagate(False)
            
            tk.Label(config_header, text="🔧 Browser Configuration", font=('Segoe UI', 9, 'bold'), 
                    bg='#0284c7', fg='#ffffff').pack(expand=True)
            
            config_content = tk.Frame(config_frame, bg='#e0f2fe')
            config_content.pack(fill='x', padx=10, pady=8)
            
            browser_name = browser_config.get('browser_type', 'Chrome').title()
            mode_name = 'InPrivate' if browser_config.get('incognito_mode') and browser_name == 'Edge' else 'Incognito' if browser_config.get('incognito_mode') else 'Normal'
            
            config_details = [
                f"Browser: {browser_name}",
                f"Mode: {mode_name}",
            ]
            
            if browser_config.get('window_x') is not None:
                config_details.append(f"Position: ({browser_config.get('window_x', 0)}, {browser_config.get('window_y', 0)})")
            
            for detail in config_details:
                tk.Label(config_content, text=f"• {detail}", font=('Segoe UI', 9), 
                        bg='#e0f2fe', fg='#0c4a6e').pack(anchor='w')
        
        # Enhanced recording controls with better UX
        controls_section = tk.Frame(content_frame, bg='#ffffff')
        controls_section.pack(fill='x', pady=(0, 25))
        
        tk.Label(controls_section, text="🎮 Recording Controls", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 15))
        
        controls_frame = tk.Frame(controls_section, bg='#ffffff')
        controls_frame.pack(fill="x")
        
        # Enhanced start button with validation
        self.start_btn = tk.Button(controls_frame, text="▶️ Start Recording", 
                                 font=('Segoe UI', 13, 'bold'), bg='#10b981', fg='#ffffff',
                                 relief='flat', padx=30, pady=15, cursor='hand2', bd=0,
                                 command=self.start_recording_with_validation)
        self.start_btn.pack(side="left", padx=(0, 20))
        
        # Enhanced stop button
        self.stop_btn = tk.Button(controls_frame, text="⏹️ Stop Recording", 
                                font=('Segoe UI', 13, 'bold'), bg='#ef4444', fg='#ffffff',
                                relief='flat', padx=30, pady=15, cursor='hand2', bd=0,
                                command=self.stop_recording, state='disabled')
        self.stop_btn.pack(side="left", padx=(0, 20))
        
        # Pause/Resume button (future enhancement)
        self.pause_btn = tk.Button(controls_frame, text="⏸️ Pause", 
                                 font=('Segoe UI', 11, 'bold'), bg='#f59e0b', fg='#ffffff',
                                 relief='flat', padx=20, pady=12, cursor='hand2', bd=0,
                                 state='disabled')
        self.pause_btn.pack(side="left")
        
        # Add hover effects
        def on_start_enter(e):
            if self.start_btn['state'] == 'normal':
                self.start_btn.configure(bg='#059669')
        def on_start_leave(e):
            if self.start_btn['state'] == 'normal':
                self.start_btn.configure(bg='#10b981')
        self.start_btn.bind('<Enter>', on_start_enter)
        self.start_btn.bind('<Leave>', on_start_leave)
        
        def on_stop_enter(e):
            if self.stop_btn['state'] == 'normal':
                self.stop_btn.configure(bg='#dc2626')
        def on_stop_leave(e):
            if self.stop_btn['state'] == 'normal':
                self.stop_btn.configure(bg='#ef4444')
        self.stop_btn.bind('<Enter>', on_stop_enter)
        self.stop_btn.bind('<Leave>', on_stop_leave)
        
        # Enhanced steps display with better organization
        steps_section = tk.Frame(content_frame, bg='#ffffff')
        steps_section.pack(fill='both', expand=True, pady=(0, 20))
        
        steps_header_frame = tk.Frame(steps_section, bg='#ffffff')
        steps_header_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(steps_header_frame, text="📝 Captured Steps", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(side='left')
        
        # Step count indicator
        self.step_count_label = tk.Label(steps_header_frame, text="(0 steps)", 
                                        font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        self.step_count_label.pack(side='left', padx=(10, 0))
        
        # Clear steps button
        clear_steps_btn = tk.Button(steps_header_frame, text="🗑️ Clear", 
                                   font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='#ffffff',
                                   relief='flat', padx=12, pady=4, cursor='hand2', bd=0,
                                   command=self.clear_steps)
        clear_steps_btn.pack(side='right')
        
        # Enhanced steps container
        steps_container = tk.Frame(steps_section, bg='#f8fafc', relief='solid', bd=1)
        steps_container.pack(fill='both', expand=True)
        
        # Steps header
        steps_list_header = tk.Frame(steps_container, bg='#e5e7eb', height=30)
        steps_list_header.pack(fill='x')
        steps_list_header.pack_propagate(False)
        
        tk.Label(steps_list_header, text="📋 Step Sequence", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        # Steps listbox with enhanced styling
        steps_frame = tk.Frame(steps_container, bg='#f8fafc')
        steps_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        self.steps_listbox = tk.Listbox(steps_frame, font=('Segoe UI', 10), 
                                       bg='#ffffff', fg='#374151',
                                       selectbackground='#dbeafe', selectforeground='#1e40af',
                                       relief='flat', bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(steps_frame, orient="vertical", command=self.steps_listbox.yview)
        self.steps_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.steps_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enhanced bottom action buttons
        bottom_frame = tk.Frame(content_frame, bg='#ffffff')
        bottom_frame.pack(fill="x", pady=(15, 0))
        
        # Left side - primary actions
        left_actions = tk.Frame(bottom_frame, bg='#ffffff')
        left_actions.pack(side='left')
        
        self.save_btn = tk.Button(left_actions, text="💾 Save Recording", 
                                 font=('Segoe UI', 12, 'bold'), bg='#3b82f6', fg='#ffffff',
                                 relief='flat', padx=25, pady=12, cursor='hand2', bd=0,
                                 command=self.save_steps, state='disabled')
        self.save_btn.pack(side="left", padx=(0, 15))
        
        preview_btn = tk.Button(left_actions, text="👁️ Preview Steps", 
                               font=('Segoe UI', 11, 'bold'), bg='#8b5cf6', fg='#ffffff',
                               relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                               command=self.preview_steps)
        preview_btn.pack(side="left", padx=(0, 10))
        
        # Right side - utility actions
        right_actions = tk.Frame(bottom_frame, bg='#ffffff')
        right_actions.pack(side='right')
        
        tk.Button(right_actions, text="❌ Close", 
                 font=('Segoe UI', 11, 'bold'), bg='#6b7280', fg='#ffffff',
                 relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                 command=dialog.destroy).pack(side="right")
        
        self.dialog = dialog
        self.recording_start_time = None
        self.step_counter = 0
        
        # Initialize timer update
        self.update_timer()
    
    def update_timer(self):
        """Update recording timer display"""
        if hasattr(self, 'recording_time') and hasattr(self, 'duration_label'):
            if self.recording and self.recording_start_time:
                elapsed = time.time() - self.recording_start_time
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                time_str = f"{minutes:02d}:{seconds:02d}"
                self.recording_time.config(text=time_str)
                self.duration_label.config(text=f"Duration: {time_str}")
            
            # Schedule next update
            if hasattr(self, 'dialog') and self.dialog.winfo_exists():
                self.dialog.after(1000, self.update_timer)
    
    def update_metrics(self):
        """Update session metrics display"""
        if hasattr(self, 'steps_count'):
            self.steps_count.config(text=f"Steps: {self.step_counter}")
        
        if hasattr(self, 'duration_label') and self.recording_start_time:
            elapsed = time.time() - self.recording_start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            self.duration_label.config(text=f"Duration: {minutes:02d}:{seconds:02d}")
    
    def preview_steps(self):
        """Preview recorded steps in a separate dialog"""
        if not self.recorded_steps:
            self.show_popup("No Steps", "No steps have been recorded yet", "warning")
            return
        
        preview_dialog = tk.Toplevel(self.dialog)
        preview_dialog.title("👁️ Step Preview")
        preview_dialog.configure(bg='#ffffff')
        preview_dialog.geometry("600x500")
        preview_dialog.transient(self.dialog)
        
        try:
            preview_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(preview_dialog, bg='#8b5cf6', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"👁️ Step Preview ({len(self.recorded_steps)} steps)", 
                font=('Segoe UI', 14, 'bold'), bg='#8b5cf6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(preview_dialog, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Steps tree view
        tree_frame = tk.Frame(content_frame, bg='#ffffff')
        tree_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        tree = ttk.Treeview(tree_frame, columns=('Action', 'Target', 'Value'), show='tree headings')
        tree.heading('#0', text='Step')
        tree.heading('Action', text='Action')
        tree.heading('Target', text='Target')
        tree.heading('Value', text='Value')
        
        tree.column('#0', width=60)
        tree.column('Action', width=120)
        tree.column('Target', width=200)
        tree.column('Value', width=150)
        
        # Populate tree
        for i, step in enumerate(self.recorded_steps, 1):
            action = step.get('action', 'Unknown')
            target = step.get('target', '')[:50] + '...' if len(step.get('target', '')) > 50 else step.get('target', '')
            value = step.get('value', '')[:30] + '...' if len(step.get('value', '')) > 30 else step.get('value', '')
            
            tree.insert('', 'end', text=str(i), values=(action, target, value))
        
        tree.pack(fill='both', expand=True)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        tree_scroll.pack(side='right', fill='y')
        
        # Close button
        tk.Button(content_frame, text="Close Preview", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0, command=preview_dialog.destroy).pack()
        
    def get_browser_config(self):
        """Get browser configuration from database"""
        try:
            config = self.db_manager.get_global_config()
            if config:
                return {
                    'browser_type': config[1],
                    'second_screen': config[2],
                    'incognito_mode': config[3],
                    'base_url': config[4],
                    'fsm_username': config[5],
                    'fsm_password': config[6],
                    'window_width': 1200,  # Default values
                    'window_height': 800,
                    'window_x': 1920 if config[2] else 0,  # 2nd screen if enabled
                    'window_y': 0
                }
            return None
        except Exception as e:
            print(f"Browser config error: {e}")
            return None
    
    def get_fsm_urls(self):
        """Get FSM URLs from browser config"""
        urls = []
        try:
            config = self.db_manager.get_global_config()
            if config and config[4]:  # fsm_url column
                urls.append(config[4])
        except Exception as e:
            print(f"URL query error: {e}")
        
        # Add default FSM URLs
        default_urls = [
            "https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1",
            "https://mingle-ionapi.inforcloudsuite.com/TAMICS10_AX1/FSM",
            "https://"
        ]
        
        return list(dict.fromkeys(urls + default_urls)) if urls else default_urls
    
    def start_recording_with_validation(self):
        """Start recording with enhanced validation"""
        # Validate URL first
        url = self.url_var.get().strip()
        if not url or url == "https://":
            self.show_popup("Validation Error", "Please enter a valid FSM URL before starting", "error")
            return
        
        if not (url.startswith('http://') or url.startswith('https://')):
            self.show_popup("Validation Error", "URL must start with http:// or https://", "error")
            return
        
        # Start recording
        self.start_recording()
    
    def start_recording(self):
        """Start browser recording"""
        try:
            url = self.url_var.get().strip()
            if not url or url == "https://":
                self.show_popup("Error", "Please enter a valid FSM URL", "error")
                return
            
            # Get browser configuration
            browser_config = self.get_browser_config()
            
            # Determine browser type from config
            browser_type = browser_config.get('browser_type', 'chrome').lower() if browser_config else 'chrome'
            
            if browser_type == 'edge':
                # Setup Edge with saved configuration
                from selenium.webdriver.edge.options import Options
                browser_options = Options()
                browser_options.add_argument("--disable-blink-features=AutomationControlled")
                browser_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                browser_options.add_experimental_option('useAutomationExtension', False)
            else:
                # Setup Chrome with saved configuration
                from selenium.webdriver.chrome.options import Options
                browser_options = Options()
                browser_options.add_argument("--disable-blink-features=AutomationControlled")
                browser_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                browser_options.add_experimental_option('useAutomationExtension', False)
            
            # Common browser arguments
            browser_options.add_argument("--disable-web-security")
            browser_options.add_argument("--allow-running-insecure-content")
            browser_options.add_argument("--ignore-certificate-errors")
            browser_options.add_argument("--start-maximized")  # Start in fullscreen
            
            # Apply browser config settings
            if browser_config:
                # Incognito mode
                if browser_config.get('incognito_mode') == 1:
                    if browser_type == 'edge':
                        browser_options.add_argument("--inprivate")
                    else:
                        browser_options.add_argument("--incognito")
                
                # Window size and position
                if browser_config.get('window_width') and browser_config.get('window_height'):
                    browser_options.add_argument(f"--window-size={browser_config['window_width']},{browser_config['window_height']}")
                
                # Second screen positioning
                if browser_config.get('window_x') and browser_config.get('window_y'):
                    browser_options.add_argument(f"--window-position={browser_config['window_x']},{browser_config['window_y']}")
            
            # Initialize browser driver based on config
            if browser_type == 'edge':
                self.driver = webdriver.Edge(options=browser_options)
            else:
                self.driver = webdriver.Chrome(options=browser_options)
            
            # Apply additional window settings and maximize
            try:
                # Maximize window for fullscreen recording
                self.driver.maximize_window()
                
                # Apply 2nd screen positioning if configured
                if browser_config and browser_config.get('window_x') is not None:
                    self.driver.set_window_position(browser_config['window_x'], browser_config['window_y'])
                    # Re-maximize after positioning
                    self.driver.maximize_window()
            except Exception as e:
                print(f"Window positioning error: {e}")
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # Navigate to URL
            self.driver.get(url)
            
            # Start recording
            self.recording = True
            self.recorded_steps = []
            self.step_counter = 0
            self.recording_start_time = time.time()
            self.steps_listbox.delete(0, tk.END)
            
            # Update UI with enhanced feedback
            self.start_btn.config(state='disabled', text="⏸️ Recording...")
            self.stop_btn.config(state='normal')
            self.pause_btn.config(state='normal')
            self.save_btn.config(state='disabled')
            
            self.status_label.config(text="🔴 Recording in progress...", fg='#ef4444')
            self.header_status.config(text="● RECORDING", fg='#ffffff')
            
            # Update metrics
            self.update_metrics()
            
            # Add initial navigation step
            self.add_step("Navigate", url, "")
            
            # Start monitoring (simplified approach)
            self.monitor_interactions()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to start recording: {str(e)}", "error")
    
    def monitor_interactions(self):
        """Advanced interaction monitoring with AI-powered element detection"""
        if not self.recording or not self.driver:
            return
        
        try:
            # Get current URL
            current_url = self.driver.current_url
            
            # Check for page changes and record pending inputs
            if hasattr(self, 'last_url') and self.last_url != current_url:
                # Record any pending inputs before page change
                try:
                    self.driver.execute_script("""
                        // Record all pending inputs before navigation
                        for (var selectorKey in window.currentInputs || {}) {
                            var inputData = window.currentInputs[selectorKey];
                            if (inputData && inputData.value) {
                                window.recordedEvents.push({
                                    type: 'Text Input',
                                    selector: inputData.selector.primary,
                                    alternatives: inputData.selector.alternatives,
                                    text: inputData.value,
                                    elementType: inputData.selector.type,
                                    tagName: inputData.selector.tagName,
                                    timestamp: Date.now(),
                                    waitCondition: 'element_visible'
                                });
                            }
                        }
                        window.currentInputs = {};
                    """)
                except:
                    pass
                
                self.add_advanced_step("Navigate", current_url, "", wait_condition="page_load")
            self.last_url = current_url
            
            # Advanced JavaScript injection for comprehensive event capture
            self.driver.execute_script("""
                if (!window.advancedRecordingSetup) {
                    window.advancedRecordingSetup = true;
                    window.recordedEvents = [];
                    window.lastHighlighted = null;
                    
                    // Advanced selector generation
                    function generateSmartSelector(element) {
                        var selectors = [];
                        
                        // Priority 1: ID (most reliable)
                        if (element.id) {
                            selectors.push('#' + element.id);
                        }
                        
                        // Priority 2: Data attributes
                        for (var attr of element.attributes) {
                            if (attr.name.startsWith('data-')) {
                                selectors.push('[' + attr.name + '="' + attr.value + '"]');
                            }
                        }
                        
                        // Priority 3: Name attribute
                        if (element.name) {
                            selectors.push('[name="' + element.name + '"]');
                        }
                        
                        // Priority 4: Class combinations
                        if (element.className) {
                            var classes = element.className.split(' ').filter(c => c.length > 0);
                            if (classes.length > 0) {
                                selectors.push('.' + classes.join('.'));
                            }
                        }
                        
                        return {
                            primary: selectors[0] || element.tagName,
                            alternatives: selectors,
                            tagName: element.tagName,
                            text: element.innerText || element.value || element.placeholder || '',
                            type: element.type || 'element'
                        };
                    }
                    
                    // Element highlighting
                    function highlightElement(element) {
                        if (window.lastHighlighted) {
                            window.lastHighlighted.style.outline = '';
                        }
                        element.style.outline = '3px solid #ff6b35';
                        element.style.outlineOffset = '2px';
                        window.lastHighlighted = element;
                        
                        setTimeout(() => {
                            if (element.style) element.style.outline = '';
                        }, 2000);
                    }
                    
                    // Smart click capture with focus-driven input recording
                    document.addEventListener('click', function(e) {
                        if (e.target) {
                            // Record any pending input from previously focused element
                            if (document.activeElement && document.activeElement !== e.target) {
                                var prevElement = document.activeElement;
                                if ((prevElement.tagName === 'INPUT' || prevElement.tagName === 'TEXTAREA') && prevElement.value) {
                                    var prevSelector = generateSmartSelector(prevElement);
                                    
                                    // Remove previous input events for this element
                                    window.recordedEvents = window.recordedEvents.filter(event => 
                                        !(event.type === 'Text Input' && event.selector === prevSelector.primary)
                                    );
                                    
                                    window.recordedEvents.push({
                                        type: 'Text Input',
                                        selector: prevSelector.primary,
                                        alternatives: prevSelector.alternatives,
                                        text: prevElement.value,
                                        elementType: prevSelector.type,
                                        tagName: prevSelector.tagName,
                                        timestamp: Date.now(),
                                        waitCondition: 'element_visible'
                                    });
                                }
                            }
                            
                            // Skip clicks on input fields (just for focus)
                            if (e.target.tagName === 'INPUT' && e.target.type !== 'submit' && e.target.type !== 'button') {
                                return;
                            }
                            
                            highlightElement(e.target);
                            var selector = generateSmartSelector(e.target);
                            
                            window.recordedEvents.push({
                                type: 'Click',
                                selector: selector.primary,
                                alternatives: selector.alternatives,
                                text: selector.text,
                                elementType: selector.type,
                                tagName: selector.tagName,
                                coordinates: { x: e.clientX, y: e.clientY },
                                timestamp: Date.now(),
                                waitCondition: 'element_clickable'
                            });
                        }
                    });
                    
                    // Event-driven text input capture
                    var currentInputs = {};
                    
                    // Track input changes
                    document.addEventListener('input', function(e) {
                        if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
                            var selector = generateSmartSelector(e.target);
                            currentInputs[selector.primary] = {
                                element: e.target,
                                value: e.target.value,
                                selector: selector
                            };
                        }
                    });
                    
                    // Record input when focus leaves element
                    document.addEventListener('blur', function(e) {
                        if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
                            var selector = generateSmartSelector(e.target);
                            var inputData = currentInputs[selector.primary];
                            
                            if (inputData && inputData.value) {
                                // Remove previous input events for this element
                                window.recordedEvents = window.recordedEvents.filter(event => 
                                    !(event.type === 'Text Input' && event.selector === selector.primary)
                                );
                                
                                window.recordedEvents.push({
                                    type: 'Text Input',
                                    selector: selector.primary,
                                    alternatives: selector.alternatives,
                                    text: inputData.value,
                                    elementType: selector.type,
                                    tagName: selector.tagName,
                                    timestamp: Date.now(),
                                    waitCondition: 'element_visible'
                                });
                            }
                        }
                    }, true);
                    
                    // Record all pending inputs before page unload
                    window.addEventListener('beforeunload', function() {
                        for (var selectorKey in currentInputs) {
                            var inputData = currentInputs[selectorKey];
                            if (inputData && inputData.value) {
                                window.recordedEvents.push({
                                    type: 'Text Input',
                                    selector: inputData.selector.primary,
                                    alternatives: inputData.selector.alternatives,
                                    text: inputData.value,
                                    elementType: inputData.selector.type,
                                    tagName: inputData.selector.tagName,
                                    timestamp: Date.now(),
                                    waitCondition: 'element_visible'
                                });
                            }
                        }
                    });
                    
                    // Dropdown/Select detection
                    document.addEventListener('change', function(e) {
                        if (e.target && e.target.tagName === 'SELECT') {
                            highlightElement(e.target);
                            var selector = generateSmartSelector(e.target);
                            var selectedText = e.target.options[e.target.selectedIndex].text;
                            
                            window.recordedEvents.push({
                                type: 'Select Option',
                                selector: selector.primary,
                                alternatives: selector.alternatives,
                                text: selectedText,
                                value: e.target.value,
                                timestamp: Date.now(),
                                waitCondition: 'element_visible'
                            });
                        }
                    });
                    
                    // File upload detection
                    document.addEventListener('change', function(e) {
                        if (e.target && e.target.type === 'file') {
                            highlightElement(e.target);
                            var selector = generateSmartSelector(e.target);
                            
                            window.recordedEvents.push({
                                type: 'File Upload',
                                selector: selector.primary,
                                alternatives: selector.alternatives,
                                text: Array.from(e.target.files).map(f => f.name).join(', '),
                                timestamp: Date.now(),
                                waitCondition: 'element_visible'
                            });
                        }
                    });
                }
            """)
            
            # Get recorded events
            events = self.driver.execute_script("return window.recordedEvents || [];")
            
            # Process new events with advanced features
            if hasattr(self, 'last_event_count'):
                new_events = events[self.last_event_count:]
                for event in new_events:
                    self.add_advanced_step(
                        event['type'], 
                        event['selector'], 
                        event['text'],
                        alternatives=event.get('alternatives', []),
                        wait_condition=event.get('waitCondition', 'none'),
                        element_type=event.get('elementType', 'element')
                    )
            
            self.last_event_count = len(events)
            
            # Schedule next check with optimized polling
            if self.recording:
                self.dialog.after(800, self.monitor_interactions)  # Slower polling for efficiency
                
        except Exception as e:
            print(f"Advanced monitoring error: {e}")
            if self.recording:
                self.dialog.after(1000, self.monitor_interactions)
    
    def add_advanced_step(self, action, target, value, alternatives=None, wait_condition='none', element_type='element'):
        """Add advanced recorded step with screenshots and smart features"""
        self.step_counter += 1
        
        # Capture screenshot before action
        screenshot_before = self.capture_screenshot()
        
        step = {
            "action": action,
            "target": target,
            "value": value,
            "alternatives": alternatives or [],
            "wait_condition": wait_condition,
            "element_type": element_type,
            "timestamp": time.time(),
            "step_id": self.step_counter,
            "screenshot_before": screenshot_before
        }
        
        # Add smart assertions for certain actions
        if action == "Click" and "submit" in target.lower():
            step["assertion"] = "page_change_expected"
        elif action == "Text Input":
            step["assertion"] = "value_entered"
        
        self.recorded_steps.append(step)
        
        # Enhanced display with icons and smart info
        icons = {
            "Navigate": "🌐",
            "Click": "👆",
            "Text Input": "⌨️",
            "Select Option": "📋",
            "File Upload": "📁",
            "Keyboard Shortcut": "⌨️",
            "Scroll": "📜"
        }
        
        icon = icons.get(action, "🔧")
        display_text = f"{self.step_counter}. {icon} {action}"
        
        if len(target) > 50:
            display_text += f": ...{target[-47:]}"
        else:
            display_text += f": {target}"
            
        if value and len(value) > 0:
            if len(value) > 30:
                display_text += f" = '{value[:27]}...'"
            else:
                display_text += f" = '{value}'"
        
        if wait_condition != 'none':
            display_text += f" [Wait: {wait_condition}]"
        
        self.steps_listbox.insert(tk.END, display_text)
        self.steps_listbox.see(tk.END)
        
        # Update status and metrics
        self.status_label.config(text=f"🔴 Recording... {self.step_counter} steps captured")
        self.step_count_label.config(text=f"({self.step_counter} steps)")
        self.steps_count.config(text=f"Steps: {self.step_counter}")
        self.last_action.config(text=f"Last Action: {action}")
        
        # Update metrics
        self.update_metrics()
    
    def capture_screenshot(self):
        """Capture screenshot for step documentation"""
        try:
            if self.driver:
                screenshot = self.driver.get_screenshot_as_png()
                # Convert to base64 for storage
                screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
                return screenshot_b64
        except Exception as e:
            print(f"Screenshot capture error: {e}")
        return None
    
    def add_step(self, action, target, value):
        """Legacy method - redirects to advanced step"""
        self.add_advanced_step(action, target, value)
    
    def stop_recording(self):
        """Enhanced stop recording with better feedback"""
        self.recording = False
        
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        # Update UI with enhanced feedback
        self.start_btn.config(state='normal', text="▶️ Start Recording")
        self.stop_btn.config(state='disabled')
        self.pause_btn.config(state='disabled')
        
        if len(self.recorded_steps) > 0:
            self.save_btn.config(state='normal')
            self.status_label.config(text=f"✅ Recording completed - {len(self.recorded_steps)} steps captured", fg='#10b981')
        else:
            self.status_label.config(text="⚠️ Recording stopped - No steps captured", fg='#f59e0b')
        
        self.header_status.config(text="● STOPPED", fg='#ffffff')
        
        # Final metrics update
        self.update_metrics()
    
    def save_steps(self):
        """Save recorded steps to database"""
        if not self.recorded_steps:
            self.show_popup("Warning", "No steps to save", "warning")
            return
        
        # Create save dialog
        save_dialog = tk.Toplevel(self.dialog)
        save_dialog.title("💾 Save Recording")
        
        # Responsive save dialog sizing
        screen_width = save_dialog.winfo_screenwidth()
        screen_height = save_dialog.winfo_screenheight()
        save_width = min(450, int(screen_width * 0.3))
        save_height = min(350, int(screen_height * 0.4))
        
        save_dialog.configure(bg='#ffffff')
        save_dialog.resizable(True, True)
        save_dialog.minsize(350, 250)
        save_dialog.transient(self.dialog)
        # Removed grab_set() to allow main app interaction
        save_dialog.lift()
        save_dialog.focus_force()
        # Removed topmost to prevent dialog layering issues
        
        # Center the save dialog
        x = (screen_width - save_width) // 2
        y = (screen_height - save_height) // 2
        save_dialog.geometry(f"{save_width}x{save_height}+{x}+{y}")
        
        # Header
        header_frame = tk.Frame(save_dialog, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="💾 Save Recording", 
                font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(save_dialog, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Test Group Name:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff').pack(anchor="w")
        
        name_entry = tk.Entry(content_frame, font=('Segoe UI', 10), width=40)
        name_entry.insert(0, f"Smart Recording {time.strftime('%Y%m%d_%H%M%S')}")
        name_entry.pack(fill="x", pady=(5, 15))
        
        tk.Label(content_frame, text="Description:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff').pack(anchor="w")
        
        # Responsive text area height
        text_height = max(3, min(6, (save_height - 200) // 25))
        desc_text = tk.Text(content_frame, font=('Segoe UI', 10), height=text_height, width=40)
        desc_text.insert("1.0", f"Automatically recorded test with {len(self.recorded_steps)} steps")
        desc_text.pack(fill="x", pady=(5, 15))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        def save_to_db():
            group_name = name_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            
            if not group_name:
                self.show_popup("Error", "Please enter a group name", "error")
                return
            
            # Disable save button to prevent double-click
            save_btn.config(state='disabled', text='Saving...')
            
            try:
                # Save group using correct database structure
                cursor = self.db_manager.conn.cursor()
                cursor.execute("""
                    INSERT INTO test_step_groups (user_id, group_name, description)
                    VALUES (?, ?, ?)
                """, (self.db_manager.user_id, group_name, description))
                
                group_id = cursor.lastrowid
                
                # Convert recorded steps to test steps
                for i, step in enumerate(self.recorded_steps):
                    step_name = f"Step {i+1}: {step['action']}"
                    step_description = f"{step['action']} on {step['target']}"
                    if step['value']:
                        step_description += f" with value '{step['value']}'"
                    
                    cursor.execute("""
                        INSERT INTO test_steps (user_id, rice_profile_id, group_id, name, step_type, target, description)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (self.db_manager.user_id, 1, group_id, step_name, step['action'], step['target'], step_description))
                
                self.db_manager.conn.commit()
                save_dialog.destroy()
                self.show_popup("Success", f"✨ Recording saved as '{group_name}' with {len(self.recorded_steps)} steps", "success")
                
                # Reset UI after successful save
                # Clear recorded steps
        self.recorded_steps = []
        self.step_counter = 0
        self.steps_listbox.delete(0, tk.END)
        self.status_label.config(text="Steps cleared - Ready to record", fg='#10b981')
        self.step_count_label.config(text="(0 steps)")
        self.steps_count.config(text="Steps: 0")
        self.last_action.config(text="Last Action: None")
        self.save_btn.config(state='disabled')
                self.save_btn.config(state='disabled')
                
            except Exception as e:
                save_btn.config(state='normal', text='💾 Save')
                self.show_popup("Error", f"Failed to save recording: {str(e)}", "error")
        
        save_btn = tk.Button(btn_frame, text="💾 Save", 
                           font=('Segoe UI', 11, 'bold'), bg='#10b981', fg='#ffffff',
                           relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                           command=save_to_db)
        save_btn.pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", 
                 font=('Segoe UI', 11, 'bold'), bg='#6b7280', fg='#ffffff',
                 relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                 command=save_dialog.destroy).pack(side="left")
    
    def clear_steps(self):
        """Clear recorded steps"""
        self.recorded_steps = []
        self.recorded_steps = []
        self.step_counter = 0
        self.steps_listbox.delete(0, tk.END)
        self.status_label.config(text="Steps cleared - Ready to record", fg='#10b981')
        self.step_count_label.config(text="(0 steps)")
        self.steps_count.config(text="Steps: 0")
        self.last_action.config(text="Last Action: None")
        self.save_btn.config(state='disabled')