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
# Removed ui_components import to fix circular dependency

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
        self.root.configure(bg='#f3f4f6')
        self.root.resizable(True, True)
        
        # Start in full screen (maximized)
        self.root.state('zoomed')
        
        # Ensure window is properly sized
        self.root.update_idletasks()
        
        # Remove auto-centering to allow dragging between monitors
        # self.root.bind('<Configure>', self.on_window_configure)
        
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
        self.setup_enhanced_styles()
        
        self.setup_modern_ui()
        
        # Set light background matching main app
        self.main_frame.configure(bg='#f3f4f6')
        
        # Allow free dragging - no auto-centering
        # self.root.after(100, lambda: self.center_window() if self.root.state() != 'zoomed' else None)
        
        self.root.mainloop()
        return self.user

    def center_window(self):
        """Center the window on screen - disabled to allow dragging"""
        # Disabled to allow free dragging between monitors
        pass
    
    def on_window_configure(self, event=None):
        """Handle window state changes - disabled to allow dragging"""
        # Disabled to allow free dragging between monitors
        pass

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
        """🎨 Setup the modern, professional UI matching main app design"""
        # Create main frame with light background (matching main app)
        self.main_frame = tk.Frame(self.root, bg='#f3f4f6')
        self.main_frame.pack(fill="both", expand=True)
        
        # Professional header with Infor branding
        self.setup_infor_header()
        
        # Professional login card
        self.setup_infor_login_card()
        
        # Professional footer
        self.setup_infor_footer()

    def setup_infor_header(self):
        """🏢 Professional Infor header matching main app style"""
        header_frame = tk.Frame(self.main_frame, bg='#f3f4f6')
        header_frame.pack(fill="x", pady=(20, 15))
        
        # Main title matching main app style
        title_label = tk.Label(header_frame, text="🏢 RICE Tester", 
                              font=('Segoe UI', 16, 'bold'), bg='#f3f4f6', fg='#1f2937')
        title_label.pack()
        
        # Subtitle with version
        try:
            import json
            version_path = os.path.join(os.path.dirname(__file__), 'version.json')
            with open(version_path, 'r') as f:
                version_data = json.load(f)
            version_text = f"v{version_data['version']}"
        except:
            version_text = "v1.0.7"
        
        subtitle_label = tk.Label(header_frame, text=f"FSM Interface Testing Suite - Enterprise Edition {version_text}", 
                                 font=('Segoe UI', 10), bg='#f3f4f6', fg='#6b7280')
        subtitle_label.pack(pady=(3, 0))

    def setup_infor_login_card(self):
        """💳 Professional login card with responsive design"""
        # Responsive card container - adapts to screen size
        card_container = tk.Frame(self.main_frame, bg='#f3f4f6')
        card_container.pack(expand=True, fill="both", padx=50, pady=20)
        
        # Center frame for responsive card sizing
        center_frame = tk.Frame(card_container, bg='#f3f4f6')
        center_frame.pack(expand=True)
        
        # Professional card with modern shadow effect (simulated with border)
        self.card_frame = tk.Frame(center_frame, bg='#ffffff', relief='solid', bd=1,
                                  highlightbackground='#e5e7eb', highlightthickness=1)
        self.card_frame.pack(anchor="center", padx=20, pady=20)
        
        # Card header with compact height - matching main app blue
        card_header = tk.Frame(self.card_frame, bg='#3b82f6', height=50)
        card_header.pack(fill="x")
        card_header.pack_propagate(False)
        
        # Mode toggle buttons
        self.setup_infor_mode_toggle(card_header)
        
        # Form container with proper expansion
        self.form_container = tk.Frame(self.card_frame, bg='#ffffff')
        self.form_container.pack(fill="x", padx=40, pady=20)
        
        # Setup initial login form
        self.setup_enhanced_login_form()

    def setup_infor_mode_toggle(self, parent):
        """🔄 Professional toggle matching main app style"""
        toggle_frame = tk.Frame(parent, bg='#3b82f6', height=50)
        toggle_frame.pack(fill="x")
        toggle_frame.pack_propagate(False)
        
        # Login button (active tab) - darker blue
        self.login_toggle = tk.Button(toggle_frame, text="Sign In", 
                                     font=('Segoe UI', 11, 'bold'),
                                     bg='#1e40af', fg='#ffffff', relief='flat',
                                     padx=25, pady=8, cursor='hand2', bd=0,
                                     command=lambda: self.switch_mode('login'))
        self.login_toggle.pack(side="left", fill="both", expand=True)
        
        # Signup button (inactive tab) - matching main app gray
        self.signup_toggle = tk.Button(toggle_frame, text="Sign Up", 
                                      font=('Segoe UI', 11, 'bold'),
                                      bg='#6b7280', fg='#ffffff', relief='flat',
                                      padx=25, pady=8, cursor='hand2', bd=0,
                                      command=lambda: self.switch_mode('signup'))
        self.signup_toggle.pack(side="right", fill="both", expand=True)

    def switch_mode(self, mode):
        """🔄 Switch between login and signup modes with animation"""
        self.current_mode = mode
        
        # Update toggle buttons with main app styling
        if mode == 'login':
            self.login_toggle.configure(bg='#1e40af', fg='#ffffff')  # Active: darker blue
            self.signup_toggle.configure(bg='#6b7280', fg='#ffffff')  # Inactive: main app gray
        else:
            self.login_toggle.configure(bg='#6b7280', fg='#ffffff')  # Inactive: main app gray
            self.signup_toggle.configure(bg='#1e40af', fg='#ffffff')  # Active: darker blue
        
        # Clear and rebuild form
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        if mode == 'login':
            self.setup_enhanced_login_form()
        else:
            self.setup_enhanced_signup_form()
        
        # Let Tkinter calculate optimal size after content is added
        self.root.update_idletasks()

    def setup_enhanced_login_form(self):
        """🔐 Enhanced login form with modern styling"""
        # Enhanced welcome message with better typography
        welcome_label = tk.Label(self.form_container, text="Welcome back!", 
                                font=('Segoe UI', 16, 'bold'), bg='#ffffff', fg='#1f2937')
        welcome_label.pack(pady=(8, 4))
        
        subtitle_label = tk.Label(self.form_container, text="Sign in to continue to your testing dashboard", 
                                 font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        subtitle_label.pack(pady=(0, 16))
        
        # Username field with icon
        self.setup_modern_field("👤 Username", "username_entry")
        
        # Password field with icon
        self.setup_modern_field("🔒 Password", "password_entry", show="•")
        
        # Load remembered credentials if available
        self.load_remembered_credentials()
        
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
        
        # Modern login button with enhanced styling
        self.login_btn = tk.Button(self.form_container, text="🏢 Sign In", 
                                  font=('Segoe UI', 12, 'bold'),
                                  bg='#1e40af', fg='#ffffff', relief='flat',
                                  padx=25, pady=12, cursor='hand2', bd=0,
                                  highlightthickness=0, activebackground='#1d4ed8',
                                  command=self.enhanced_login)
        self.login_btn.pack(fill="x", pady=(20, 25), padx=5)
        
        # Add hover effects for better UX
        def on_enter(e):
            if self.login_btn['state'] != 'disabled':
                self.login_btn.configure(bg='#1d4ed8')
        
        def on_leave(e):
            if self.login_btn['state'] != 'disabled':
                self.login_btn.configure(bg='#1e40af')
        
        self.login_btn.bind('<Enter>', on_enter)
        self.login_btn.bind('<Leave>', on_leave)
        
        # Enhanced keyboard shortcuts
        if hasattr(self, 'password_entry'):
            self.password_entry.bind('<Return>', lambda e: self.enhanced_login())
        if hasattr(self, 'username_entry'):
            self.username_entry.bind('<Return>', lambda e: self.password_entry.focus() if hasattr(self, 'password_entry') else None)
            # Automatically focus on username field
            self.root.after(100, lambda: self.username_entry.focus())
        
        # Add escape key to close
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # Quick login options
        if ENHANCED_FEATURES:
            self.setup_quick_login_options()

    def setup_enhanced_signup_form(self):
        """📝 Enhanced signup form"""
        # Enhanced welcome message with better typography
        welcome_label = tk.Label(self.form_container, text="Create Account", 
                                font=('Segoe UI', 16, 'bold'), bg='#ffffff', fg='#1f2937')
        welcome_label.pack(pady=(8, 4))
        
        subtitle_label = tk.Label(self.form_container, text="Create your account to start testing today!!", 
                                 font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        subtitle_label.pack(pady=(0, 16))
        
        # Full name field
        self.setup_modern_field("👤 Full Name", "fullname_entry")
        
        # Project field
        self.setup_modern_field("📋 Project", "company_entry")
        
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
        
        # Modern signup button with enhanced styling
        self.signup_btn = tk.Button(self.form_container, text="🏢 Create Account", 
                                   font=('Segoe UI', 12, 'bold'),
                                   bg='#10b981', fg='#ffffff', relief='flat',
                                   padx=25, pady=15, cursor='hand2', bd=0,
                                   highlightthickness=0, activebackground='#059669',
                                   command=self.enhanced_signup)
        self.signup_btn.pack(fill="x", pady=(20, 25), padx=5, ipady=8)
        
        # Add hover effects for better UX
        def on_enter_signup(e):
            if self.signup_btn['state'] != 'disabled':
                self.signup_btn.configure(bg='#059669')
        
        def on_leave_signup(e):
            if self.signup_btn['state'] != 'disabled':
                self.signup_btn.configure(bg='#10b981')
        
        self.signup_btn.bind('<Enter>', on_enter_signup)
        self.signup_btn.bind('<Leave>', on_leave_signup)

    def setup_modern_field(self, label_text, entry_name, show=None):
        """🎨 Setup modern input field with enhanced UX"""
        field_frame = tk.Frame(self.form_container, bg='#ffffff')
        field_frame.pack(fill="x", pady=(0, 12))
        
        # Modern label with better typography
        label = tk.Label(field_frame, text=label_text, 
                        font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#374151')
        label.pack(anchor="w", pady=(0, 4))
        
        # Enhanced entry with modern styling
        entry = tk.Entry(field_frame, font=('Segoe UI', 11), 
                        bg='#f9fafb', fg='#1f2937', relief='solid',
                        bd=1, highlightthickness=2, highlightcolor='#1e40af',
                        insertbackground='#1e40af', show=show,
                        highlightbackground='#d1d5db')
        entry.pack(fill="x", ipady=8)
        
        # Store reference
        setattr(self, entry_name, entry)
        
        # Enhanced focus effects with smooth transitions
        def on_focus_in(e):
            entry.configure(highlightbackground='#1e40af', bg='#ffffff')
            label.configure(fg='#1e40af')
        
        def on_focus_out(e):
            entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
            label.configure(fg='#374151')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

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
        """📊 Professional footer matching main app style"""
        footer_frame = tk.Frame(self.main_frame, bg='#f3f4f6')
        footer_frame.pack(fill="x", side="bottom", pady=(15, 10))
        
        # Copyright matching main app colors
        copyright_label = tk.Label(footer_frame, text="© 2025 RICE Tester - Infor FSM Testing Suite", 
                                  font=('Segoe UI', 9), bg='#f3f4f6', fg='#9ca3af')
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
            
            # Handle Remember Me functionality
            if self.remember_var.get():
                self.save_remembered_credentials(username)
            else:
                self.clear_remembered_credentials()
            
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
            
            # Show loading screen with 3-second delay
            self.show_loading_screen(user[2])
            self.root.after(3000, self.cleanup_and_exit)
        else:
            # Reset login button to normal state
            self.login_btn.configure(text="🏢 Sign In", state='normal', bg='#1e40af')
            
            self.show_modern_popup("Error", "Invalid username or password", "error")
            
            # Log failed attempt
            if ENHANCED_FEATURES:
                try:
                    console.print(f"[red]Failed login attempt #{self.login_attempts} for user: {username}[/red]")
                except UnicodeEncodeError:
                    print(f"Failed login attempt #{self.login_attempts} for user: {username}")

    def show_infor_login_progress(self):
        """🔄 Show professional login progress animation"""
        # Disable login button and show progress
        self.login_btn.configure(text="🔄 Signing In...", state='disabled', bg='#9ca3af')
        
        if ENHANCED_FEATURES:
            try:
                console.print("[blue]Authenticating user credentials...[/blue]")
            except UnicodeEncodeError:
                print("Authenticating user credentials...")

    def show_loading_screen(self, full_name):
        """📊 Show dashboard preview loading screen"""
        # Update login button to show loading
        self.login_btn.configure(text="⚙️ Launching...", state='disabled', bg='#10b981')
        
        # Create clean dashboard preview overlay
        loading_overlay = tk.Toplevel(self.root)
        loading_overlay.configure(bg='#f3f4f6')
        loading_overlay.resizable(False, False)
        loading_overlay.transient(self.root)
        loading_overlay.overrideredirect(True)  # Remove title bar and decorations
        loading_overlay.attributes('-topmost', True)  # Ensure it stays on top
        loading_overlay.lift()  # Bring to front
        loading_overlay.focus_force()  # Force focus
        
        # Dashboard preview frame
        preview_frame = tk.Frame(loading_overlay, bg='#f3f4f6', padx=30, pady=20)
        preview_frame.pack(fill="both", expand=True)
        
        # Header (simulating app header)
        header_frame = tk.Frame(preview_frame, bg='#ffffff', relief='solid', bd=1, height=60)
        header_frame.pack(fill="x", pady=(0, 15))
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🏢 RICE Tester", font=('Segoe UI', 14, 'bold'), 
                bg='#ffffff', fg='#1f2937').pack(side="left", padx=20, pady=15)
        
        tk.Label(header_frame, text=f"Welcome, {full_name}!", font=('Segoe UI', 10), 
                bg='#ffffff', fg='#6b7280').pack(side="right", padx=20, pady=15)
        
        # Content area (simulating main interface)
        content_frame = tk.Frame(preview_frame, bg='#ffffff', relief='solid', bd=1, height=200)
        content_frame.pack(fill="x")
        content_frame.pack_propagate(False)
        
        # Loading content
        loading_content = tk.Frame(content_frame, bg='#ffffff')
        loading_content.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Spinner
        self.spinner_label = tk.Label(loading_content, text="◐", font=('Segoe UI', 20), 
                                     bg='#ffffff', fg='#1e40af')
        self.spinner_label.pack(pady=(0, 15))
        
        # Loading message
        self.loading_text = tk.Label(loading_content, text="Initializing dashboard", 
                                    font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#1f2937')
        self.loading_text.pack()
        
        # Center the overlay
        loading_overlay.update_idletasks()
        center_dialog(loading_overlay, 500, 320)
        
        # Start animations
        self.loading_step = 0
        self.animate_dashboard_loading()
        
        # Close overlay after 3 seconds
        self.root.after(3000, lambda: self.safe_destroy_overlay(loading_overlay))
        
        # Store reference
        self.loading_overlay = loading_overlay
    
    def safe_destroy_overlay(self, overlay):
        """Safely destroy loading overlay"""
        try:
            if overlay and overlay.winfo_exists():
                overlay.destroy()
        except tk.TclError:
            pass  # Already destroyed
    
    def animate_dashboard_loading(self):
        """Animate dashboard loading with changing messages and spinner"""
        try:
            if not (hasattr(self, 'loading_text') and self.loading_text.winfo_exists()):
                return
        except tk.TclError:
            # Widget was destroyed, stop animation
            return
        
        # Loading messages sequence
        messages = [
            "Initializing dashboard",
            "Loading RICE items", 
            "Preparing test scenarios",
            "Setting up workspace",
            "Almost ready"
        ]
        
        # Spinner animation
        spinners = ["◐", "◓", "◑", "◒"]
        
        # Get current message and add animated dots
        message_index = (self.loading_step // 4) % len(messages)
        dot_count = (self.loading_step % 4)
        dots = "." * dot_count
        
        current_message = messages[message_index] + dots
        current_spinner = spinners[self.loading_step % len(spinners)]
        
        # Update UI safely
        try:
            self.loading_text.configure(text=current_message)
            if hasattr(self, 'spinner_label') and self.spinner_label.winfo_exists():
                self.spinner_label.configure(text=current_spinner)
        except tk.TclError:
            # Widget was destroyed, stop animation
            return
        
        self.loading_step += 1
        
        # Continue animation every 300ms - only if widgets still exist
        if hasattr(self, 'root') and self.root.winfo_exists():
            self.root.after(300, self.animate_dashboard_loading)

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
        
        # Show signup progress
        self.signup_btn.configure(text="🏢 Creating Account...", state='disabled', bg='#9ca3af')
        
        self.root.after(500, lambda: self.process_signup(full_name, company, username, password))

    def process_signup(self, full_name, company, username, password):
        """📝 Process signup with enhanced features"""
        # 🚨 SECURITY: Block privileged usernames from signup
        restricted_usernames = ['vansilleza_fpi', 'van_silleza', 'admin', 'administrator', 'root', 'system']
        if username.lower() in [u.lower() for u in restricted_usernames]:
            self.signup_btn.configure(text="🏢 Create Account", state='normal', bg='#4CAF50')
            self.show_modern_popup("Username Restricted", "This username is reserved for system administrators.\n\nPlease choose a different username.", "error")
            return
        
        # Check if username exists
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            self.signup_btn.configure(text="🏢 Create Account", state='normal', bg='#10b981')
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
        self.signup_btn.configure(text="🏢 Create Account", state='normal', bg='#10b981')

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
        
        # Status colors matching main app palette
        if status == "success":
            icon = "✅"
            color = "#10b981"  # Main app success green
        elif status == "warning":
            icon = "⚠️"
            color = "#f59e0b"  # Main app warning orange
        else:
            icon = "❌"
            color = "#ef4444"  # Main app error red
        
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
        
        # Compact close button matching main app
        close_btn = tk.Button(content_frame, text="Close", 
                             font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                             relief='flat', padx=20, pady=6, cursor='hand2', bd=0,
                             highlightthickness=0, command=popup.destroy)
        close_btn.pack()
        
        # Center the popup properly
        popup.update_idletasks()  # Ensure popup is fully rendered
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
        
        # Create enhanced users table with immutable username restrictions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL CHECK (
                    LOWER(username) NOT IN ('vansilleza_fpi', 'van_silleza', 'admin', 'administrator', 'root', 'system')
                    OR id <= 3
                ),
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
    
    def save_remembered_credentials(self, username):
        """💾 Save credentials for Remember Me functionality"""
        try:
            remember_file = os.path.join(os.path.dirname(self.db_path), '.remember_me')
            with open(remember_file, 'w') as f:
                f.write(username)
        except Exception as e:
            print(f"Could not save remembered credentials: {e}")
    
    def load_remembered_credentials(self):
        """📂 Load remembered credentials"""
        try:
            remember_file = os.path.join(os.path.dirname(self.db_path), '.remember_me')
            if os.path.exists(remember_file):
                with open(remember_file, 'r') as f:
                    username = f.read().strip()
                if username and hasattr(self, 'username_entry'):
                    self.username_entry.insert(0, username)
                    self.remember_var.set(True)
                    # Focus on password field since username is filled
                    if hasattr(self, 'password_entry'):
                        self.root.after(100, lambda: self.password_entry.focus())
                else:
                    # No remembered username, focus on username field
                    if hasattr(self, 'username_entry'):
                        self.root.after(100, lambda: self.username_entry.focus())
        except Exception as e:
            print(f"Could not load remembered credentials: {e}")
    
    def clear_remembered_credentials(self):
        """🗑️ Clear remembered credentials"""
        try:
            remember_file = os.path.join(os.path.dirname(self.db_path), '.remember_me')
            if os.path.exists(remember_file):
                os.remove(remember_file)
        except Exception as e:
            print(f"Could not clear remembered credentials: {e}")
    
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
