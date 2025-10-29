#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning without blinking"""
    # CSS-like centering: top 50%, left 50%, transform translate(-50%, -50%)
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    # Use provided dimensions or defaults
    w = width if width else 400
    h = height if height else 300
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    # Set geometry immediately without any hide/show operations
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()
import sqlite3
import hashlib
import os
import time
import threading
from datetime import datetime
from ui_components import configure_smooth_styles, create_popup

# 🚀 5-STAR ENHANCEMENTS
try:
    import pandas as pd
    import numpy as np
    from rich.console import Console
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.panel import Panel
    from rich.text import Text
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    ENHANCED_FEATURES = True
    console = Console(force_terminal=True, legacy_windows=False)
except ImportError:
    ENHANCED_FEATURES = False
    console = None

class AuthSystem:
    def __init__(self):
        self.root = None
        self.user = None
        # Set database path to RICE_Tester directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, "fsm_tester.db")
        self.login_attempts = 0
        self.session_start = time.time()
        self.init_database()
        
        # 🎨 Enhanced UI State
        self.current_mode = "login"  # login, signup, loading

    def show_startup_animation(self):
        """🎆 Beautiful startup animation with Rich"""
        if not ENHANCED_FEATURES:
            return
            
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Initializing FSM Automated Testing..."),
                BarColumn(),
                TimeElapsedColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Loading", total=100)
                
                steps = [
                    ("Loading authentication system", 20),
                    ("Connecting to database", 40),
                    ("Initializing UI components", 60),
                    ("Preparing enhanced features", 80),
                    ("Ready to launch!", 100)
                ]
                
                for step_text, step_value in steps:
                    progress.update(task, description=f"[bold blue]{step_text}...")
                    progress.update(task, completed=step_value)
                    time.sleep(0.3)
                
                console.print(Panel.fit(
                    "[bold green]FSM Automated Testing - Enterprise Edition Ready![/bold green]",
                    border_style="green"
                ))
        except UnicodeEncodeError:
            print("FSM Automated Testing - Enterprise Edition Ready!")

    def run(self):
        """🚀 Run the enhanced authentication system"""
        if ENHANCED_FEATURES:
            self.show_startup_animation()
        
        self.root = tk.Tk()
        self.root.title("RICE Tester - Login")
        self.root.state('zoomed')  # Maximize window on Windows
        self.root.configure(bg='#F5F6FA')
        self.root.resizable(True, True)
        
        # Ensure window is properly maximized and sized
        self.root.update_idletasks()
        self.root.state('zoomed')  # Force maximize again after idletasks
        
        # Bind window state change to handle centering when not maximized
        self.root.bind('<Configure>', self.on_window_configure)
        
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
        
        # Configure enhanced styles
        configure_smooth_styles()
        self.setup_enhanced_styles()
        
        self.setup_modern_ui()
        
        # Set static navy background color
        self.main_frame.configure(bg='#1E2A38')
        
        # Center window initially if not maximized
        self.root.after(100, lambda: self.center_window() if self.root.state() != 'zoomed' else None)
        
        self.root.mainloop()
        return self.user

    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2) - 50
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def on_window_configure(self, event=None):
        """Handle window state changes to center when not maximized"""
        if event and event.widget == self.root:
            # Check if window is not maximized (zoomed)
            if self.root.state() != 'zoomed':
                # Small delay to ensure window dimensions are updated
                self.root.after(10, self.center_window)

    def setup_enhanced_styles(self):
        """🎨 Setup enhanced visual styles"""
        style = ttk.Style()
        
        # Modern button styles
        style.configure('Modern.TButton',
                       background='#3b82f6',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 12))
        
        style.map('Modern.TButton',
                 background=[('active', '#2563eb'),
                           ('pressed', '#1d4ed8')])
        
        # Modern entry styles
        style.configure('Modern.TEntry',
                       fieldbackground='#f8fafc',
                       borderwidth=2,
                       insertcolor='#3b82f6',
                       padding=(15, 12))
        
        style.map('Modern.TEntry',
                 focuscolor=[('focus', '#3b82f6')])



    def setup_modern_ui(self):
        """🎨 Setup the modern, professional UI with dynamic sizing"""
        # Get screen dimensions for dynamic sizing
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Force consistent large screen layout to prevent size differences after logout
        self.is_small_screen = False  # Always use large screen layout for consistency
        
        # Create main frame with navy background
        self.main_frame = tk.Frame(self.root, bg='#1E2A38')
        self.main_frame.pack(fill="both", expand=True)
        
        # Professional header with Infor branding
        self.setup_infor_header()
        
        # Professional login card
        self.setup_infor_login_card()
        
        # Professional footer
        self.setup_infor_footer()

    def setup_infor_header(self):
        """🏢 Professional Infor header with dynamic sizing"""
        # Dynamic sizing based on screen size
        header_pady = (15, 10) if self.is_small_screen else (30, 20)
        title_font = 16
        subtitle_font = 10
        
        header_frame = tk.Frame(self.main_frame, bg='#1E2A38')
        header_frame.pack(fill="x", pady=header_pady)
        
        # Main title with dynamic font size
        title_label = tk.Label(header_frame, text="🏢 RICE Tester", 
                              font=('Segoe UI', title_font, 'bold'), bg='#1E2A38', fg='#FFFFFF')
        title_label.pack()
        
        # Subtitle with dynamic font size
        subtitle_label = tk.Label(header_frame, text="FSM Interface Testing Suite - Enterprise Edition", 
                                 font=('Segoe UI', subtitle_font), bg='#1E2A38', fg='#9E9E9E')
        subtitle_label.pack(pady=(3, 0))

    def setup_infor_login_card(self):
        """💳 Professional Infor login card with dynamic sizing"""
        # Dynamic sizing based on screen size
        container_padx = 80 if self.is_small_screen else 200
        container_pady = 15 if self.is_small_screen else 30
        # Expand the actual card panel by 0.5 inch (36px)
        card_padx = 2 if self.is_small_screen else 32   # Reduced by 18px each side
        card_pady = 5 if self.is_small_screen else 15   # Reduced by 5px each side
        
        # Card container with dynamic padding - allow expansion
        card_container = tk.Frame(self.main_frame, bg='#1E2A38')
        card_container.pack(expand=True, fill="both", padx=container_padx, pady=container_pady)
        
        # Professional card with dynamic sizing and static background
        self.card_frame = tk.Frame(card_container, bg='#FFFFFF', relief='solid', bd=2)
        self.card_frame.pack(anchor="center", padx=card_padx, pady=card_pady)
        
        # Card header with dynamic height - primary orange
        header_height = 60 if self.is_small_screen else 80
        card_header = tk.Frame(self.card_frame, bg='#F26A21', height=header_height)
        card_header.pack(fill="x", padx=0, pady=(0, 0))
        card_header.pack_propagate(False)
        
        # Mode toggle buttons
        self.setup_infor_mode_toggle(card_header)
        
        # Form container with dynamic padding
        form_padx = 30 if self.is_small_screen else 60
        form_pady = 10 if self.is_small_screen else 15
        self.form_container = tk.Frame(self.card_frame, bg='#FFFFFF')
        self.form_container.pack(fill="x", padx=form_padx, pady=form_pady)
        
        # Setup initial login form
        self.setup_enhanced_login_form()

    def setup_infor_mode_toggle(self, parent):
        """🔄 Professional toggle with dynamic sizing"""
        toggle_height = 40 if self.is_small_screen else 50
        toggle_frame = tk.Frame(parent, bg='#F26A21', height=toggle_height)
        toggle_frame.pack(fill="x")
        toggle_frame.pack_propagate(False)
        
        # Dynamic toggle button sizing
        toggle_font = 10 if self.is_small_screen else 12
        toggle_padx = 20 if self.is_small_screen else 30
        toggle_pady = 8 if self.is_small_screen else 10
        
        # Login button with dynamic sizing (active tab) - primary orange
        self.login_toggle = tk.Button(toggle_frame, text="Sign In", 
                                     font=('Segoe UI', toggle_font, 'bold'),
                                     bg='#F26A21', fg='#FFFFFF', relief='flat',
                                     padx=toggle_padx, pady=toggle_pady, cursor='hand2', bd=0,
                                     command=lambda: self.switch_mode('login'))
        self.login_toggle.pack(side="left", fill="both", expand=True)
        
        # Signup button with dynamic sizing (inactive tab) - neutral gray
        self.signup_toggle = tk.Button(toggle_frame, text="Sign Up", 
                                      font=('Segoe UI', toggle_font, 'bold'),
                                      bg='#9E9E9E', fg='#FFFFFF', relief='flat',
                                      padx=toggle_padx, pady=toggle_pady, cursor='hand2', bd=0,
                                      command=lambda: self.switch_mode('signup'))
        self.signup_toggle.pack(side="right", fill="both", expand=True)

    def switch_mode(self, mode):
        """🔄 Switch between login and signup modes with animation"""
        self.current_mode = mode
        
        # Update toggle buttons with consistent styling
        if mode == 'login':
            self.login_toggle.configure(bg='#F26A21', fg='#FFFFFF')  # Active: primary orange
            self.signup_toggle.configure(bg='#9E9E9E', fg='#FFFFFF')  # Inactive: neutral gray
        else:
            self.login_toggle.configure(bg='#9E9E9E', fg='#FFFFFF')  # Inactive: neutral gray
            self.signup_toggle.configure(bg='#F26A21', fg='#FFFFFF')  # Active: primary orange
        
        # Clear and rebuild form
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        if mode == 'login':
            self.setup_enhanced_login_form()
        else:
            self.setup_enhanced_signup_form()

    def setup_enhanced_login_form(self):
        """🔐 Enhanced login form with modern styling"""
        # Welcome message matching signup compact sizing
        welcome_font = 12 if self.is_small_screen else 14
        subtitle_font = 8 if self.is_small_screen else 9
        welcome_pady = (5, 2) if self.is_small_screen else (8, 3)
        subtitle_pady = (0, 5) if self.is_small_screen else (0, 8)
        
        welcome_label = tk.Label(self.form_container, text="Welcome back!", 
                                font=('Segoe UI', welcome_font, 'bold'), bg='#FFFFFF', fg='#1B2A41')
        welcome_label.pack(pady=welcome_pady)
        
        subtitle_label = tk.Label(self.form_container, text="Sign in to continue to your testing dashboard", 
                                 font=('Segoe UI', subtitle_font), bg='#FFFFFF', fg='#6C757D')
        subtitle_label.pack(pady=subtitle_pady)
        
        # Username field with icon
        self.setup_modern_field("👤 Username", "username_entry")
        
        # Password field with icon
        self.setup_modern_field("🔒 Password", "password_entry", show="•")
        
        # Remember me and forgot password with compact spacing
        options_frame = tk.Frame(self.form_container, bg='#FFFFFF')
        options_frame.pack(fill="x", pady=(3, 6))
        
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(options_frame, text="Remember me", 
                                       variable=self.remember_var,
                                       bg='#FFFFFF', fg='#9E9E9E', 
                                       selectcolor='#F26A21', cursor='hand2')
        remember_check.pack(side="left")
        
        forgot_label = tk.Label(options_frame, text="Forgot password?", 
                               font=('Segoe UI', 9), bg='#FFFFFF', fg='#2BBBAD', 
                               cursor='hand2')
        forgot_label.pack(side="right")
        forgot_label.bind('<Button-1>', self.show_forgot_password)
        
        # Professional login button matching signup sizing
        btn_font = 10 if self.is_small_screen else 12
        btn_padx = 25 if self.is_small_screen else 30
        btn_pady = 8 if self.is_small_screen else 10
        btn_margin_y = (8, 8) if self.is_small_screen else (10, 10)
        btn_margin_x = 5 if self.is_small_screen else 10
        
        self.login_btn = tk.Button(self.form_container, text="🏢 Sign In", 
                                  font=('Segoe UI', btn_font, 'bold'),
                                  bg='#F26A21', fg='#FFFFFF', relief='raised',
                                  padx=btn_padx, pady=btn_pady, cursor='hand2', bd=2,
                                  highlightbackground='#D85A1C',
                                  command=self.enhanced_login)
        self.login_btn.pack(fill="x", pady=btn_margin_y, padx=btn_margin_x)
        
        # Enhanced keyboard shortcuts
        if hasattr(self, 'password_entry'):
            self.password_entry.bind('<Return>', lambda e: self.enhanced_login())
        if hasattr(self, 'username_entry'):
            self.username_entry.bind('<Return>', lambda e: self.password_entry.focus() if hasattr(self, 'password_entry') else None)
        
        # Add escape key to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Quick login options
        if ENHANCED_FEATURES:
            self.setup_quick_login_options()

    def setup_enhanced_signup_form(self):
        """📝 Enhanced signup form"""
        # Welcome message with compact sizing for signup
        welcome_font = 12 if self.is_small_screen else 14
        subtitle_font = 8 if self.is_small_screen else 9
        welcome_pady = (5, 2) if self.is_small_screen else (8, 3)
        subtitle_pady = (0, 5) if self.is_small_screen else (0, 8)
        
        welcome_label = tk.Label(self.form_container, text="Register", 
                                font=('Segoe UI', welcome_font, 'bold'), bg='#FFFFFF', fg='#1B2A41')
        welcome_label.pack(pady=welcome_pady)
        
        subtitle_label = tk.Label(self.form_container, text="Create your account to get started", 
                                 font=('Segoe UI', subtitle_font), bg='#FFFFFF', fg='#6C757D')
        subtitle_label.pack(pady=subtitle_pady)
        
        # Full name field
        self.setup_modern_field("👤 Full Name", "fullname_entry")
        
        # Company field
        self.setup_modern_field("🏢 Company", "company_entry")
        
        # Username field
        self.setup_modern_field("🆔 Username", "new_username_entry")
        
        # Password field with strength meter
        self.setup_modern_field("🔒 Password", "new_password_entry", show="•")
        
        # Password strength meter
        if ENHANCED_FEATURES:
            self.setup_password_strength_meter()
        
        # Terms checkbox with minimal spacing
        terms_frame = tk.Frame(self.form_container, bg='#FFFFFF')
        terms_frame.pack(fill="x", pady=(3, 6))
        
        self.terms_var = tk.BooleanVar()
        terms_check = tk.Checkbutton(terms_frame, text="I agree to the Terms of Service", 
                                    variable=self.terms_var,
                                    bg='#FFFFFF', fg='#9E9E9E', 
                                    selectcolor='#F26A21', cursor='hand2')
        terms_check.pack()
        
        # Professional signup button with compact sizing
        btn_font = 10 if self.is_small_screen else 12
        btn_padx = 25 if self.is_small_screen else 30
        btn_pady = 8 if self.is_small_screen else 10
        btn_margin_y = (8, 8) if self.is_small_screen else (10, 10)
        btn_margin_x = 5 if self.is_small_screen else 10
        
        self.signup_btn = tk.Button(self.form_container, text="🏢 Create Account", 
                                   font=('Segoe UI', btn_font, 'bold'),
                                   bg='#4CAF50', fg='#ffffff', relief='raised',
                                   padx=btn_padx, pady=btn_pady, cursor='hand2', bd=2,
                                   highlightbackground='#45A049',
                                   command=self.enhanced_signup)
        self.signup_btn.pack(fill="x", pady=btn_margin_y, padx=btn_margin_x)

    def setup_modern_field(self, label_text, entry_name, show=None):
        """🎨 Setup professional input field with dynamic sizing"""
        field_pady = (0, 6) if self.is_small_screen else (0, 8)
        field_frame = tk.Frame(self.form_container, bg='#FFFFFF')
        field_frame.pack(fill="x", pady=field_pady)
        
        # Compact field sizing for better fit
        label_font = 8 if self.is_small_screen else 9
        entry_font = 9
        entry_pady = 4
        label_pady = (0, 2) if self.is_small_screen else (0, 3)
        
        # Label with dynamic sizing
        label = tk.Label(field_frame, text=label_text, 
                        font=('Segoe UI', label_font, 'bold'), bg='#FFFFFF', fg='#6C757D')
        label.pack(anchor="w", pady=label_pady)
        
        # Entry with dynamic sizing
        entry = tk.Entry(field_frame, font=('Segoe UI', entry_font), 
                        bg='#f8f9fa', fg='#1B2A41', relief='solid',
                        bd=2, highlightthickness=2, highlightcolor='#F26A21',
                        insertbackground='#F26A21', show=show)
        entry.pack(fill="x", ipady=entry_pady)
        
        # Store reference
        setattr(self, entry_name, entry)
        
        # Add focus effects with new theme colors
        entry.bind('<FocusIn>', lambda e: entry.configure(highlightbackground='#F26A21'))
        entry.bind('<FocusOut>', lambda e: entry.configure(highlightbackground='#9E9E9E'))

    def setup_password_strength_meter(self):
        """🔒 Password strength meter with real-time feedback"""
        if not ENHANCED_FEATURES:
            return
            
        strength_frame = tk.Frame(self.form_container, bg='#ffffff')
        strength_frame.pack(fill="x", pady=(0, 15))
        
        strength_label = tk.Label(strength_frame, text="Password Strength:", 
                                 font=('Segoe UI', 9), bg='#ffffff', fg='#666666')
        strength_label.pack(anchor="w")
        
        # Strength bars with Infor styling
        bars_frame = tk.Frame(strength_frame, bg='#ffffff')
        bars_frame.pack(fill="x", pady=(5, 0))
        
        self.strength_bars = []
        for i in range(4):
            bar = tk.Frame(bars_frame, bg='#e9ecef', height=4)
            bar.pack(side="left", fill="x", expand=True, padx=(0, 2))
            self.strength_bars.append(bar)
        
        # Bind password entry to strength checker
        self.root.after(100, lambda: (
            self.new_password_entry.bind('<KeyRelease>', self.update_password_strength)
            if hasattr(self, 'new_password_entry') else None
        ))

    def update_password_strength(self, event=None):
        """📊 Update password strength meter"""
        if not ENHANCED_FEATURES or not hasattr(self, 'strength_bars'):
            return
            
        password = self.new_password_entry.get()
        strength = self.calculate_password_strength(password)
        
        colors = ['#dc3545', '#ffc107', '#FF6B35', '#28a745']
        
        for i, bar in enumerate(self.strength_bars):
            if i < strength:
                bar.configure(bg=colors[min(i, len(colors)-1)])
            else:
                bar.configure(bg='#e9ecef')

    def calculate_password_strength(self, password):
        """🔢 Calculate password strength (0-4)"""
        if len(password) < 4:
            return 0
        
        strength = 0
        if len(password) >= 8:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            strength += 1
        
        return strength

    def setup_quick_login_options(self):
        """⚡ Quick login options for returning users"""
        # Get recent users
        recent_users = self.get_recent_users()
        
        if recent_users:
            quick_frame = tk.Frame(self.form_container, bg='#ffffff')
            quick_frame.pack(fill="x", pady=(10, 0))
            
            quick_label = tk.Label(quick_frame, text="Quick Login:", 
                                  font=('Segoe UI', 9, 'bold'), bg='#ffffff', fg='#666666')
            quick_label.pack(anchor="w", pady=(0, 5))
            
            for username in recent_users[:3]:  # Show top 3
                user_btn = tk.Button(quick_frame, text=f"👤 {username}", 
                                     font=('Segoe UI', 9), bg='#f8f9fa', fg='#666666',
                                     relief='solid', bd=1, padx=10, pady=5, cursor='hand2',
                                     command=lambda u=username: self.quick_login(u))
                user_btn.pack(fill="x", pady=1)

    def quick_login(self, username):
        """⚡ Quick login for returning users"""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, username)
        self.password_entry.focus()

    def setup_infor_footer(self):
        """📊 Professional Infor footer with dynamic sizing"""
        footer_pady = (10, 5) if self.is_small_screen else (20, 10)
        footer_font = 8 if self.is_small_screen else 10
        
        footer_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        footer_frame.pack(fill="x", side="bottom", pady=footer_pady)
        
        # Copyright with dynamic font size
        copyright_label = tk.Label(footer_frame, text="© 2025 RICE Tester - Infor FSM Testing Suite", 
                                  font=('Segoe UI', footer_font), bg='#f0f0f0', fg='#999999')
        copyright_label.pack()

    def enhanced_login(self):
        """🚀 Enhanced login with analytics and animations"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_modern_popup("Error", "Please enter both username and password", "error")
            return
        
        # Show loading animation with Infor styling
        self.show_infor_login_progress()
        
        # Simulate processing time for better UX
        self.root.after(500, lambda: self.process_login(username, password))

    def process_login(self, username, password):
        """🔐 Process login with enhanced security"""
        self.login_attempts += 1
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Check credentials
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, full_name, company FROM users WHERE username = ? AND password_hash = ?", 
                      (username, hashed_password))
        user = cursor.fetchone()
        
        if user:
            self.user = {
                'id': user[0],
                'username': user[1],
                'full_name': user[2],
                'company': user[3] if len(user) > 3 else 'Unknown'
            }
            
            # Update last login with error handling
            try:
                cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", 
                              (datetime.now().isoformat(), user[0]))
                self.conn.commit()
            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    # Continue without updating last login if database is locked
                    print(f"Warning: Could not update last login - database locked")
                else:
                    raise e
            
            # Show success with analytics
            if ENHANCED_FEATURES:
                self.show_login_success_analytics()
            else:
                self.show_modern_popup("Success", f"Welcome back, {user[2]}!", "success")
                self.root.after(1500, self.cleanup_and_exit)
        else:
            # Reset login button to normal state
            self.login_btn.configure(text="🏢 Sign In", state='normal', bg='#F26A21')
            
            self.show_modern_popup("Error", "Invalid username or password", "error")
            
            # Log failed attempt
            if ENHANCED_FEATURES:
                try:
                    console.print(f"[red]Failed login attempt #{self.login_attempts} for user: {username}[/red]")
                except UnicodeEncodeError:
                    print(f"Failed login attempt #{self.login_attempts} for user: {username}")

    def show_infor_login_progress(self):
        """🔄 Show professional login progress animation"""
        # Disable login button and show progress with Infor styling
        self.login_btn.configure(text="🔄 Signing In...", state='disabled', bg='#cccccc')
        
        if ENHANCED_FEATURES:
            try:
                console.print("[blue]Authenticating user credentials...[/blue]")
            except UnicodeEncodeError:
                print("Authenticating user credentials...")

    def show_login_success_analytics(self):
        """📊 Show login success with analytics"""
        if not ENHANCED_FEATURES:
            return
            
        try:
            # Calculate session time
            session_time = time.time() - self.session_start
            
            success_panel = Panel.fit(
                f"[bold green]Welcome back, {self.user['full_name']}![/bold green]\n"
                f"[blue]Company:[/blue] {self.user['company']}\n"
                f"[blue]Login Time:[/blue] {session_time:.1f}s\n"
                f"[blue]Attempts:[/blue] {self.login_attempts}\n"
                f"[green]Authentication Successful![/green]",
                title="Login Success",
                border_style="green"
            )
            console.print(success_panel)
        except UnicodeEncodeError:
            print(f"Welcome back, {self.user['full_name']}!")
        
        self.show_modern_popup("Success", f"Welcome back, {self.user['full_name']}!", "success")
        self.root.after(2000, self.cleanup_and_exit)

    def enhanced_signup(self):
        """✨ Enhanced signup with validation"""
        full_name = self.fullname_entry.get().strip()
        company = self.company_entry.get().strip()
        username = self.new_username_entry.get().strip()
        password = self.new_password_entry.get().strip()
        
        if not all([full_name, username, password]):
            self.show_modern_popup("Error", "Please fill in all required fields", "error")
            return
        
        if not self.terms_var.get():
            self.show_modern_popup("Error", "Please agree to the Terms of Service", "error")
            return
        
        # Validate password strength
        if ENHANCED_FEATURES and self.calculate_password_strength(password) < 2:
            self.show_modern_popup("Error", "Password is too weak. Please use a stronger password.", "error")
            return
        
        # Show signup progress with Infor styling
        self.signup_btn.configure(text="🏢 Creating Account...", state='disabled', bg='#cccccc')
        
        self.root.after(500, lambda: self.process_signup(full_name, company, username, password))

    def process_signup(self, full_name, company, username, password):
        """📝 Process signup with enhanced features"""
        # Check if username exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            self.signup_btn.configure(text="🏢 Create Account", state='normal', bg='#4CAF50')
            self.show_modern_popup("Error", "Username already exists. Please choose another.", "error")
            return
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create user
        cursor.execute("""
            INSERT INTO users (username, password_hash, full_name, company, created_at, last_login) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (username, hashed_password, full_name, company, 
              datetime.now().isoformat(), datetime.now().isoformat()))
        self.conn.commit()
        
        if ENHANCED_FEATURES:
            try:
                success_panel = Panel.fit(
                    f"[bold green]Account Created Successfully![/bold green]\n"
                    f"[blue]Name:[/blue] {full_name}\n"
                    f"[blue]Company:[/blue] {company}\n"
                    f"[blue]Username:[/blue] {username}\n"
                    f"[green]Ready to sign in![/green]",
                    title="Welcome to FSM Testing",
                    border_style="green"
                )
                console.print(success_panel)
            except UnicodeEncodeError:
                print(f"Account created for {full_name}!")
        
        self.show_modern_popup("Success", f"Account created successfully!\nWelcome, {full_name}!", "success")
        
        # Switch to login mode
        self.root.after(2000, lambda: self.switch_mode('login'))
        self.signup_btn.configure(text="🏢 Create Account", state='normal', bg='#4CAF50')

    def show_modern_popup(self, title, message, status):
        """🎨 Show compact popup with enhanced styling"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg='#ffffff')
        popup.resizable(False, False)
        popup.transient(self.root)
        
        # Set custom icon
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Status colors and icons with consistent palette
        if status == "success":
            icon = "✅"
            color = "#4CAF50"  # Success green
        elif status == "warning":
            icon = "⚠️"
            color = "#F26A21"  # Primary orange for warnings
        else:
            icon = "❌"
            color = "#E53935"  # Error red
        
        # Compact header
        header_frame = tk.Frame(popup, bg=color, height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text=f"{icon} {title}", 
                               font=('Segoe UI', 12, 'bold'), bg=color, fg='#ffffff')
        header_label.pack(expand=True)
        
        # Compact content
        content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=15)
        content_frame.pack(fill="both", expand=True)
        
        message_label = tk.Label(content_frame, text=message, 
                                font=('Segoe UI', 10), bg='#ffffff', fg='#333333',
                                justify="center", wraplength=280)
        message_label.pack(pady=(0, 15))
        
        # Compact close button
        close_btn = tk.Button(content_frame, text="Close", 
                             font=('Segoe UI', 10, 'bold'), bg='#9E9E9E', fg='#ffffff', 
                             relief='flat', padx=20, pady=6, cursor='hand2', bd=0,
                             command=popup.destroy)
        close_btn.pack()
        
        # Use CSS-like centering function with smaller size
        center_dialog(popup, 320, 180)
        
        popup.focus_set()

    def show_forgot_password(self, event=None):
        """🔑 Show forgot password dialog"""
        self.show_modern_popup("Forgot Password", 
                              "Password recovery feature coming soon!\n\nPlease contact your administrator for assistance.", 
                              "warning")

    def get_recent_users(self):
        """👥 Get recent users for quick login"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT username FROM users 
                WHERE last_login IS NOT NULL 
                ORDER BY last_login DESC 
                LIMIT 5
            """)
            return [row[0] for row in cursor.fetchall()]
        except:
            return []

    def get_login_analytics(self):
        """📊 Get login analytics for footer"""
        try:
            cursor = self.conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            # Active sessions (users who logged in today)
            today = datetime.now().date().isoformat()
            cursor.execute("SELECT COUNT(*) FROM users WHERE date(last_login) = ?", (today,))
            active_sessions = cursor.fetchone()[0]
            
            # Success rate (mock calculation)
            success_rate = max(85.0, min(99.9, 95.0 + np.random.normal(0, 2))) if ENHANCED_FEATURES else 95.0
            
            return {
                'total_users': total_users,
                'active_sessions': active_sessions,
                'success_rate': success_rate
            }
        except:
            return {
                'total_users': 0,
                'active_sessions': 0,
                'success_rate': 95.0
            }

    def init_database(self):
        """🗄️ Initialize enhanced database with analytics support"""
        try:
            # Ensure directory exists
            db_dir = os.path.dirname(self.db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_path)
            cursor = self.conn.cursor()
        except Exception as e:
            print(f"Database initialization error: {e}")
            print(f"Attempted database path: {self.db_path}")
            raise
        
        # Create enhanced users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                company TEXT,
                created_at TEXT NOT NULL,
                last_login TEXT,
                login_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # Add new columns if they don't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN last_login TEXT")
        except sqlite3.OperationalError:
            pass  # Column already exists
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN login_count INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT 1")
        except sqlite3.OperationalError:
            pass
        
        self.conn.commit()
        
        if ENHANCED_FEATURES:
            try:
                console.print("[green]Database initialized with enhanced features[/green]")
            except UnicodeEncodeError:
                print("Database initialized with enhanced features")

    def cleanup_and_exit(self):
        """🧹 Clean shutdown"""
        # Clean destroy
        if hasattr(self, 'root') and self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
    
    def __del__(self):
        """🧹 Cleanup resources"""
        if hasattr(self, 'conn'):
            self.conn.close()
        
        if ENHANCED_FEATURES:
            try:
                console.print("[blue]Authentication session ended[/blue]")
            except UnicodeEncodeError:
                print("Authentication session ended")

# Security: This module can only be launched through RICE_Tester.py
if __name__ == "__main__":
    print("SECURITY ERROR: Direct launch not allowed")
    print("Please use RICE_Tester.py to launch with proper authentication")
    input("Press Enter to exit...")
    exit(1)