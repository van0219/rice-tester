#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning"""
    dialog.withdraw()
    dialog.update_idletasks()
    
    # Get dimensions
    if width and height:
        dialog.geometry(f"{width}x{height}")
    
    dialog.update_idletasks()
    w = dialog.winfo_reqwidth() if not width else width
    h = dialog.winfo_reqheight() if not height else height
    
    # CSS-like centering: top 50%, left 50%, transform translate(-50%, -50%)
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.deiconify()
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()
import threading
import time

class ConfigManager:
    def __init__(self, parent, db_manager, selenium_manager, show_popup_callback):
        self.parent = parent
        self.db_manager = db_manager
        self.selenium_manager = selenium_manager
        self.show_popup = show_popup_callback
    

        
    def setup_browser_tab_content(self, parent):
        """Setup browser configuration tab content with modern card design"""
        # Main container with padding
        main_container = tk.Frame(parent, bg='#f8fafc')
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern card container
        card_frame = tk.Frame(main_container, bg='#ffffff', relief='solid', bd=1,
                             highlightbackground='#e5e7eb', highlightthickness=1)
        card_frame.pack(fill="x", pady=(0, 20))
        
        # Card header
        header_frame = tk.Frame(card_frame, bg='#3b82f6', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🌐 Browser Configuration", 
                font=('Segoe UI', 12, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Form content with better spacing
        browser_frame = tk.Frame(card_frame, bg='#ffffff', padx=30, pady=25)
        browser_frame.pack(fill="both", expand=True)
        
        # Browser selection with modern styling
        self.setup_modern_field_group(browser_frame, "🌐 Browser", 0)
        self.browser_var = tk.StringVar(value="edge")
        browser_options = tk.Frame(browser_frame, bg='#ffffff')
        browser_options.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=8)
        
        # Modern radio buttons with better styling
        edge_radio = tk.Radiobutton(browser_options, text="Microsoft Edge", variable=self.browser_var, 
                                   value="edge", cursor='hand2', bg='#ffffff', fg='#374151',
                                   font=('Segoe UI', 10), selectcolor='#3b82f6')
        edge_radio.pack(side="left", padx=(0, 20))
        
        chrome_radio = tk.Radiobutton(browser_options, text="Google Chrome", variable=self.browser_var, 
                                     value="chrome", cursor='hand2', bg='#ffffff', fg='#374151',
                                     font=('Segoe UI', 10), selectcolor='#3b82f6')
        chrome_radio.pack(side="left")
        
        # FSM URL with enhanced styling
        self.setup_modern_field_group(browser_frame, "🔗 FSM URL", 1)
        self.url_entry = self.create_modern_entry(browser_frame, 1, placeholder="https://your-fsm-server.com")
        
        # Username with enhanced styling
        self.setup_modern_field_group(browser_frame, "👤 Username", 2)
        self.username_entry = self.create_modern_entry(browser_frame, 2, placeholder="Enter your username")
        
        # Password with integrated show/hide toggle
        self.setup_modern_field_group(browser_frame, "🔒 Password", 3)
        password_container = tk.Frame(browser_frame, bg='#f9fafb', relief='solid', bd=1,
                                     highlightthickness=2, highlightcolor='#3b82f6',
                                     highlightbackground='#d1d5db')
        password_container.grid(row=3, column=1, sticky="ew", padx=(15, 0), pady=8)
        
        self.password_entry = tk.Entry(password_container, show="•", font=('Segoe UI', 11),
                                      bg='#f9fafb', fg='#1f2937', relief='flat', bd=0,
                                      highlightthickness=0, insertbackground='#3b82f6')
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(8, 0))
        
        # Password toggle button inside the textbox
        self.password_visible = False
        self.toggle_btn = tk.Button(password_container, text="👁️", font=('Segoe UI', 9),
                                   bg='#f9fafb', fg='#6b7280', relief='flat', bd=0,
                                   padx=6, pady=0, cursor='hand2',
                                   command=self.toggle_password_visibility)
        self.toggle_btn.pack(side="right", padx=(0, 8))
        
        # Add focus effects to container
        def on_password_focus_in(e):
            password_container.configure(highlightbackground='#3b82f6', bg='#ffffff')
            self.password_entry.configure(bg='#ffffff')
            self.toggle_btn.configure(bg='#ffffff')
        
        def on_password_focus_out(e):
            password_container.configure(highlightbackground='#d1d5db', bg='#f9fafb')
            self.password_entry.configure(bg='#f9fafb')
            self.toggle_btn.configure(bg='#f9fafb')
        
        self.password_entry.bind('<FocusIn>', on_password_focus_in)
        self.password_entry.bind('<FocusOut>', on_password_focus_out)
        
        # Options
        options_frame = tk.Frame(browser_frame, bg='#ffffff')
        options_frame.grid(row=4, column=1, sticky="w", padx=(15, 0), pady=15)
        
        # Modern checkboxes with better styling
        self.incognito_var = tk.BooleanVar()
        incognito_check = tk.Checkbutton(options_frame, text="🕵️ Incognito mode", 
                                        variable=self.incognito_var, font=('Segoe UI', 10), 
                                        bg='#ffffff', fg='#374151', selectcolor='#3b82f6',
                                        cursor='hand2')
        incognito_check.pack(side="left", padx=(0, 25))
        
        self.second_screen_var = tk.BooleanVar()
        screen_check = tk.Checkbutton(options_frame, text="🖥️ Open on 2nd screen", 
                                     variable=self.second_screen_var, font=('Segoe UI', 10), 
                                     bg='#ffffff', fg='#374151', selectcolor='#3b82f6',
                                     cursor='hand2')
        screen_check.pack(side="left")
        
        # Modern buttons frame with better spacing
        btn_frame = tk.Frame(browser_frame, bg='#ffffff')
        btn_frame.grid(row=5, column=1, sticky="w", padx=(15, 0), pady=20)
        
        # Save button with hover effects
        save_btn = tk.Button(btn_frame, text="💾 Save Configuration", 
                            font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                            relief='flat', padx=16, pady=8, cursor='hand2', 
                            bd=0, highlightthickness=0, command=self.save_browser_config)
        save_btn.pack(side="left", padx=(0, 15))
        
        # Add hover effects for save button
        def on_save_enter(e):
            save_btn.configure(bg='#059669')
        def on_save_leave(e):
            save_btn.configure(bg='#10b981')
        save_btn.bind('<Enter>', on_save_enter)
        save_btn.bind('<Leave>', on_save_leave)
        
        # Test button with hover effects
        test_btn = tk.Button(btn_frame, text="🚀 Test Browser", 
                            font=('Segoe UI', 10, 'bold'), bg='#3b82f6', fg='#ffffff', 
                            relief='flat', padx=16, pady=8, cursor='hand2', 
                            bd=0, highlightthickness=0, command=self.test_browser)
        test_btn.pack(side="left")
        
        # Add hover effects for test button
        def on_test_enter(e):
            test_btn.configure(bg='#2563eb')
        def on_test_leave(e):
            test_btn.configure(bg='#3b82f6')
        test_btn.bind('<Enter>', on_test_enter)
        test_btn.bind('<Leave>', on_test_leave)
        
        # Configure grid for responsiveness
        browser_frame.grid_columnconfigure(1, weight=1)
        
        # Load existing configuration
        self.load_global_config()
    
    def setup_file_channel_tab_content(self, parent):
        """Setup file channel configuration tab content with modern card design"""
        # Main container with padding
        main_container = tk.Frame(parent, bg='#f8fafc')
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern card container
        card_frame = tk.Frame(main_container, bg='#ffffff', relief='solid', bd=1,
                             highlightbackground='#e5e7eb', highlightthickness=1)
        card_frame.pack(fill="both", expand=True)
        
        # Card header with integrated buttons
        header_frame = tk.Frame(card_frame, bg='#10b981', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Header title and buttons in same row
        header_content = tk.Frame(header_frame, bg='#10b981')
        header_content.pack(fill="both", expand=True, padx=20, pady=12)
        
        tk.Label(header_content, text="📁 File Channel Configuration", 
                font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='#ffffff').pack(side="left")
        
        # Header buttons
        header_btn_frame = tk.Frame(header_content, bg='#10b981')
        header_btn_frame.pack(side="right")
        
        add_btn = tk.Button(header_btn_frame, text="＋ Add", 
                           font=('Segoe UI', 9, 'bold'), bg='#059669', fg='#ffffff', 
                           relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                           command=self.add_channel)
        add_btn.pack(side="left", padx=(0, 8))
        
        refresh_btn = tk.Button(header_btn_frame, text="⟲ Refresh", 
                               font=('Segoe UI', 9, 'bold'), bg='#059669', fg='#ffffff', 
                               relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                               command=self.load_channels)
        refresh_btn.pack(side="left")
        
        # Table container
        table_container = tk.Frame(card_frame, bg='#ffffff')
        table_container.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        # Headers with modern styling
        headers_frame = tk.Frame(table_container, bg='#d1d5db', height=35)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        # Column headers with optimized widths
        tk.Label(headers_frame, text="Channel Name", font=('Segoe UI', 10, 'bold'), 
                bg='#d1d5db', fg='#374151', anchor='w').place(relx=0, y=8, relwidth=0.8, x=18)
        
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#d1d5db', fg='#374151', anchor='w').place(relx=0.8, y=8, relwidth=0.2, x=18)
        
        # Column separator
        tk.Frame(headers_frame, bg='#9ca3af', width=1).place(relx=0.8, y=4, height=27)
        
        # Scrollable table frame
        self.channels_scroll_frame = tk.Frame(table_container, bg='#ffffff')
        self.channels_scroll_frame.pack(fill="both", expand=True)
        
        # Initialize selection tracking
        self.selected_channel_id = None
        
        self.load_channels()
    
    def setup_modern_field_group(self, parent, label_text, row):
        """Setup modern field label with consistent styling"""
        label = tk.Label(parent, text=label_text, font=('Segoe UI', 10, 'bold'), 
                        bg='#ffffff', fg='#374151')
        label.grid(row=row, column=0, sticky="w", pady=8, padx=(0, 15))
        return label
    
    def create_modern_entry(self, parent, row, placeholder=""):
        """Create modern styled entry field with focus effects"""
        entry = tk.Entry(parent, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                        relief='solid', bd=1, highlightthickness=2, 
                        highlightcolor='#3b82f6', highlightbackground='#d1d5db',
                        insertbackground='#3b82f6')
        entry.grid(row=row, column=1, sticky="ew", padx=(15, 0), pady=8, ipady=8)
        
        # Add focus effects
        def on_focus_in(e):
            entry.configure(highlightbackground='#3b82f6', bg='#ffffff')
        
        def on_focus_out(e):
            entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        # Configure grid weight for responsiveness
        parent.grid_columnconfigure(1, weight=1)
        
        return entry
    
    def toggle_password_visibility(self):
        """Toggle password field visibility"""
        if self.password_visible:
            self.password_entry.configure(show="•")
            self.toggle_btn.configure(text="👁️")
            self.password_visible = False
        else:
            self.password_entry.configure(show="")
            self.toggle_btn.configure(text="🙈")
            self.password_visible = True
    
    def load_global_config(self):
        """Load global configuration"""
        config = self.db_manager.get_global_config()
        if config and hasattr(self, 'browser_var'):
            self.browser_var.set(config[1] or "edge")
            self.second_screen_var.set(bool(config[2]) if config[2] is not None else False)
            self.incognito_var.set(bool(config[3]) if config[3] is not None else False)
            
            if config[4]:  # fsm_url
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, config[4])
            if config[5]:  # fsm_username
                self.username_entry.delete(0, tk.END)
                self.username_entry.insert(0, config[5])
            if config[13]:  # fsm_password (encrypted) - column 13
                self.password_entry.delete(0, tk.END)
                decrypted_password = self.db_manager.decrypt_password(config[13])
                print(f"DEBUG: Loading config - Encrypted: '{config[13]}' -> Decrypted: '{decrypted_password}'")
                if decrypted_password:  # Only insert if decryption was successful
                    self.password_entry.insert(0, decrypted_password)
    
    def save_browser_config(self):
        """Save browser configuration"""
        try:
            # Get current values
            browser = self.browser_var.get()
            second_screen = self.second_screen_var.get()
            incognito = self.incognito_var.get()
            fsm_url = self.url_entry.get().strip()
            fsm_username = self.username_entry.get().strip()
            fsm_password = self.password_entry.get().strip()
            
            # Encrypt password if provided
            encrypted_password = self.db_manager.hash_password_reversible(fsm_password) if fsm_password else ""
            
            # Debug output
            print(f"DEBUG: Saving config - Password: '{fsm_password}' -> Encrypted: '{encrypted_password}'")
            
            # Save to database (matching the expected tuple format)
            config_data = (
                browser, second_screen, incognito, 
                fsm_url, fsm_username, encrypted_password,
                "", 22, "", "", ""  # SFTP fields (empty for now)
            )
            self.db_manager.save_global_config(config_data)
            
            self.show_popup("Success", "Browser configuration saved successfully!", "success")
        except Exception as e:
            self.show_popup("Error", f"Failed to save configuration: {str(e)}", "error")
    
    def test_browser(self):
        """Test browser configuration in separate thread"""
        # Store reference to testing popup
        testing_popup = None
        
        def run_test():
            nonlocal testing_popup
            driver = None
            try:
                driver = self.selenium_manager.create_driver(
                    self.browser_var.get(),
                    self.incognito_var.get(),
                    self.second_screen_var.get()
                )
                
                if driver:
                    # Set shorter timeouts to prevent hanging
                    driver.set_page_load_timeout(8)
                    driver.implicitly_wait(3)
                    
                    # Simple local test - fastest and most reliable
                    driver.get("data:text/html,<html><head><title>Test</title></head><body><h1>OK</h1></body></html>")
                    
                    # Quick verification
                    browser_name = self.browser_var.get().title()
                    if driver.title and len(driver.page_source) > 50:
                        self.selenium_manager.close()
                        # Close testing popup first
                        if testing_popup:
                            testing_popup.destroy()
                        self.show_popup(f"{browser_name} Test", f"✅ {browser_name} test successful!\n{browser_name} is working properly.", "success")
                    else:
                        self.selenium_manager.close()
                        # Close testing popup first
                        if testing_popup:
                            testing_popup.destroy()
                        self.show_popup(f"{browser_name} Test", f"⚠️ {browser_name} opened but test page didn't load properly.", "warning")
                else:
                    browser_name = self.browser_var.get().title()
                    # Close testing popup first
                    if testing_popup:
                        testing_popup.destroy()
                    self.show_popup(f"{browser_name} Test", f"❌ Failed to create {browser_name} driver", "error")
                    
            except Exception as e:
                # Clean up driver if it exists
                if driver:
                    try:
                        self.selenium_manager.close()
                    except:
                        pass
                
                browser_name = self.browser_var.get().title()
                # Close testing popup first
                if testing_popup:
                    testing_popup.destroy()
                
                error_msg = str(e)
                self.show_popup(f"{browser_name} Test", f"❌ {browser_name} test failed: {error_msg[:100]}...", "error")
        
        # Create and show testing popup
        testing_popup = self.create_testing_popup()
        
        # Run test in separate thread to keep UI responsive
        test_thread = threading.Thread(target=run_test, daemon=True)
        test_thread.start()
    
    def create_testing_popup(self):
        """Create a testing popup with consistent application styling"""
        popup = tk.Toplevel()
        popup.title("Testing Browser")
        center_dialog(popup, 400, 250)
        popup.configure(bg='#ffffff')
        popup.resizable(False, False)
        popup.transient(self.parent)
        popup.grab_set()
        
        # Set custom icon
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            try:
                icon_path = "infor_logo.png"
                popup_icon = tk.PhotoImage(file=icon_path)
                popup.iconphoto(False, popup_icon)
            except:
                pass
        
        # Center popup without animation
        x = (popup.winfo_screenwidth() // 2) - 200
        y = (popup.winfo_screenheight() // 2) - 125
        popup.geometry(f"400x250+{x}+{y}")
        popup.withdraw()
        popup.update_idletasks()
        popup.deiconify()
        
        # Get browser name for display
        browser_name = self.browser_var.get().title()  # "edge" -> "Edge", "chrome" -> "Chrome"
        
        # Header (consistent with other popups)
        header_frame = tk.Frame(popup, bg='#f59e0b', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text=f"🔄 {browser_name} Test", 
                               font=('Segoe UI', 14, 'bold'), bg='#f59e0b', fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content (consistent with other popups)
        content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message_label = tk.Label(content_frame, text=f"Testing {browser_name} configuration...\nPlease wait...", 
                                font=('Segoe UI', 10), bg='#ffffff', 
                                justify="center", wraplength=350)
        message_label.pack(pady=(0, 20))
        
        return popup
    
    def load_channels(self):
        """Load file channels with modern table styling"""
        # Clear existing channel rows
        for widget in self.channels_scroll_frame.winfo_children():
            widget.destroy()
        
        channels = self.db_manager.get_file_channels()
        
        if not channels:
            # Empty state with professional styling
            empty_frame = tk.Frame(self.channels_scroll_frame, bg='#ffffff', height=100)
            empty_frame.pack(fill="x", pady=20)
            empty_frame.pack_propagate(False)
            
            tk.Label(empty_frame, text="📁 No File Channels Found", 
                    font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#6b7280').pack(expand=True)
            tk.Label(empty_frame, text="Click 'Add' to create your first file channel", 
                    font=('Segoe UI', 10), bg='#ffffff', fg='#9ca3af').pack()
            return
        
        # Display channels with modern card-based rows
        for i, channel in enumerate(channels):
            channel_id, channel_name = channel
            
            # Alternating row colors
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            # Create row frame with hover effects
            row_frame = tk.Frame(self.channels_scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill="x")
            row_frame.pack_propagate(False)
            
            # Add hover effects
            def on_row_enter(e, frame=row_frame):
                if frame.cget('bg') != '#dbeafe':  # Don't override selection color
                    frame.configure(bg='#f8fafc')
                    for child in frame.winfo_children():
                        if hasattr(child, 'configure') and child.winfo_width() != 1:
                            child.configure(bg='#f8fafc')
            
            def on_row_leave(e, frame=row_frame, original_bg=bg_color):
                if frame.cget('bg') != '#dbeafe':  # Don't override selection color
                    frame.configure(bg=original_bg)
                    for child in frame.winfo_children():
                        if hasattr(child, 'configure') and child.winfo_width() != 1:
                            child.configure(bg=original_bg)
            
            row_frame.bind('<Enter>', on_row_enter)
            row_frame.bind('<Leave>', on_row_leave)
            
            # Make row clickable for selection
            row_frame.bind('<Button-1>', lambda e, cid=channel_id: self.select_channel(cid))
            row_frame.configure(cursor='hand2')
            row_frame.channel_id = channel_id
            
            # Channel Name with modern styling
            name_label = tk.Label(row_frame, text=channel_name, font=('Segoe UI', 10), 
                                 bg=bg_color, fg='#1f2937', cursor='hand2', anchor='w')
            name_label.place(relx=0, y=8, relwidth=0.8, x=18)
            name_label.bind('<Button-1>', lambda e, cid=channel_id: self.select_channel(cid))
            name_label.bind('<Enter>', on_row_enter)
            name_label.bind('<Leave>', on_row_leave)
            
            # Column separator
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.8, y=2, height=31)
            
            # Actions column with proper positioning (20% width)
            actions_frame = tk.Frame(row_frame, bg=bg_color)
            actions_frame.place(relx=0.8, y=2, relwidth=0.2, height=31)
            
            # Action buttons matching SFTP Config table exactly
            edit_btn = tk.Button(actions_frame, text="✏ Edit", font=('Segoe UI', 8, 'bold'), 
                               bg='#3b82f6', fg='#ffffff', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0,
                               command=lambda cid=channel_id: self.edit_channel(cid))
            edit_btn.place(relx=0.05, rely=0, relwidth=0.45, relheight=1.0)
            
            delete_btn = tk.Button(actions_frame, text="× Delete", font=('Segoe UI', 8, 'bold'), 
                                 bg='#ef4444', fg='#ffffff', relief='flat', 
                                 padx=4, pady=1, cursor='hand2', bd=0,
                                 command=lambda cid=channel_id: self.delete_channel(cid))
            delete_btn.place(relx=0.55, rely=0, relwidth=0.45, relheight=1.0)
    
    def add_channel(self):
        """Add file channel dialog with modern styling"""
        popup = tk.Toplevel()
        popup.title("📁 Add File Channel")
        center_dialog(popup, 450, 280)
        popup.configure(bg='#ffffff')
        popup.transient(self.parent)
        popup.grab_set()
        
        # Set custom icon
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            try:
                icon_path = "infor_logo.png"
                popup_icon = tk.PhotoImage(file=icon_path)
                popup.iconphoto(False, popup_icon)
            except:
                pass
        
        # Modern header
        header_frame = tk.Frame(popup, bg='#10b981', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📁 Add File Channel", 
                font=('Segoe UI', 14, 'bold'), bg='#10b981', fg='#ffffff').pack(expand=True)
        
        # Content frame
        content_frame = tk.Frame(popup, bg='#ffffff', padx=30, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        # Channel Name with modern styling
        tk.Label(content_frame, text="🏷️ Channel Name", 
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#374151').pack(anchor="w", pady=(0, 8))
        
        name_entry = tk.Entry(content_frame, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                             relief='solid', bd=1, highlightthickness=2, 
                             highlightcolor='#10b981', highlightbackground='#d1d5db',
                             insertbackground='#10b981')
        name_entry.pack(fill="x", pady=(0, 25), ipady=8)
        
        # Add focus effects
        def on_focus_in(e):
            name_entry.configure(highlightbackground='#10b981', bg='#ffffff')
        
        def on_focus_out(e):
            name_entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
        
        name_entry.bind('<FocusIn>', on_focus_in)
        name_entry.bind('<FocusOut>', on_focus_out)
        
        # Buttons with modern styling
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        def save_channel():
            name = name_entry.get().strip()
            if not name:
                self.show_popup("Error", "Please enter a channel name", "error")
                return
            
            try:
                self.db_manager.save_file_channel(name)
                popup.destroy()
                self.load_channels()
                self.show_popup("Success", f"Channel '{name}' saved successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to save channel: {str(e)}", "error")
        
        save_btn = tk.Button(btn_frame, text="✓ Save Channel", 
                            font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                            relief='flat', padx=16, pady=8, cursor='hand2', bd=0,
                            command=save_channel)
        save_btn.pack(side="left", padx=(0, 12))
        
        cancel_btn = tk.Button(btn_frame, text="× Cancel", 
                              font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                              relief='flat', padx=16, pady=8, cursor='hand2', bd=0,
                              command=popup.destroy)
        cancel_btn.pack(side="left")
        
        # Add hover effects
        def on_save_enter(e):
            save_btn.configure(bg='#059669')
        def on_save_leave(e):
            save_btn.configure(bg='#10b981')
        save_btn.bind('<Enter>', on_save_enter)
        save_btn.bind('<Leave>', on_save_leave)
        
        def on_cancel_enter(e):
            cancel_btn.configure(bg='#4b5563')
        def on_cancel_leave(e):
            cancel_btn.configure(bg='#6b7280')
        cancel_btn.bind('<Enter>', on_cancel_enter)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
        # Enter key binding
        name_entry.bind('<Return>', lambda e: save_channel())
        
        popup.focus_set()
        name_entry.focus()
    
    def select_channel(self, channel_id):
        """Handle file channel selection for highlighting"""
        # Reset previous selection
        if hasattr(self, 'selected_channel_row') and self.selected_channel_row:
            try:
                # Reset to normal alternating colors
                row_index = list(self.channels_scroll_frame.winfo_children()).index(self.selected_channel_row)
                normal_color = '#ffffff' if row_index % 2 == 0 else '#f9fafb'
                self.selected_channel_row.configure(bg=normal_color)
                # Update all child widgets except column separators
                for child in self.selected_channel_row.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_width() != 1:
                        child.configure(bg=normal_color)
            except (ValueError, tk.TclError):
                pass
        
        # Set new selection
        self.selected_channel_id = channel_id
        
        # Find and highlight the clicked row using channel_id tag
        for row_widget in self.channels_scroll_frame.winfo_children():
            if hasattr(row_widget, 'channel_id') and row_widget.channel_id == channel_id:
                # Highlight this row
                row_widget.configure(bg='#dbeafe')
                for child in row_widget.winfo_children():
                    if hasattr(child, 'configure') and child.winfo_width() != 1:
                        child.configure(bg='#dbeafe')
                self.selected_channel_row = row_widget
                break
    
    def edit_channel(self, channel_id):
        """Edit file channel with modern styling"""
        # Get current channel data
        channels = self.db_manager.get_file_channels()
        channel_data = None
        for channel in channels:
            if channel[0] == channel_id:
                channel_data = channel
                break
        
        if not channel_data:
            self.show_popup("Error", "Channel not found", "error")
            return
        
        current_name = channel_data[1]
        
        popup = tk.Toplevel()
        popup.title("✏️ Edit File Channel")
        center_dialog(popup, 450, 280)
        popup.configure(bg='#ffffff')
        popup.transient(self.parent)
        popup.grab_set()
        
        # Set custom icon
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            try:
                icon_path = "infor_logo.png"
                popup_icon = tk.PhotoImage(file=icon_path)
                popup.iconphoto(False, popup_icon)
            except:
                pass
        
        # Modern header
        header_frame = tk.Frame(popup, bg='#3b82f6', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✏️ Edit File Channel", 
                font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content frame
        content_frame = tk.Frame(popup, bg='#ffffff', padx=30, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        # Channel Name with modern styling
        tk.Label(content_frame, text="🏷️ Channel Name", 
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#374151').pack(anchor="w", pady=(0, 8))
        
        name_entry = tk.Entry(content_frame, font=('Segoe UI', 11), bg='#f9fafb', fg='#1f2937',
                             relief='solid', bd=1, highlightthickness=2, 
                             highlightcolor='#3b82f6', highlightbackground='#d1d5db',
                             insertbackground='#3b82f6')
        name_entry.insert(0, current_name)
        name_entry.pack(fill="x", pady=(0, 25), ipady=8)
        
        # Add focus effects
        def on_focus_in(e):
            name_entry.configure(highlightbackground='#3b82f6', bg='#ffffff')
        
        def on_focus_out(e):
            name_entry.configure(highlightbackground='#d1d5db', bg='#f9fafb')
        
        name_entry.bind('<FocusIn>', on_focus_in)
        name_entry.bind('<FocusOut>', on_focus_out)
        
        # Buttons with modern styling
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        def save_changes():
            new_name = name_entry.get().strip()
            if not new_name:
                self.show_popup("Error", "Please enter a channel name", "error")
                return
            
            try:
                self.db_manager.update_file_channel(channel_id, new_name)
                popup.destroy()
                self.load_channels()
                self.show_popup("Success", f"Channel '{new_name}' updated successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update channel: {str(e)}", "error")
        
        save_btn = tk.Button(btn_frame, text="✓ Save Changes", 
                            font=('Segoe UI', 10, 'bold'), bg='#3b82f6', fg='#ffffff', 
                            relief='flat', padx=16, pady=8, cursor='hand2', bd=0,
                            command=save_changes)
        save_btn.pack(side="left", padx=(0, 12))
        
        cancel_btn = tk.Button(btn_frame, text="× Cancel", 
                              font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                              relief='flat', padx=16, pady=8, cursor='hand2', bd=0,
                              command=popup.destroy)
        cancel_btn.pack(side="left")
        
        # Add hover effects
        def on_save_enter(e):
            save_btn.configure(bg='#2563eb')
        def on_save_leave(e):
            save_btn.configure(bg='#3b82f6')
        save_btn.bind('<Enter>', on_save_enter)
        save_btn.bind('<Leave>', on_save_leave)
        
        def on_cancel_enter(e):
            cancel_btn.configure(bg='#4b5563')
        def on_cancel_leave(e):
            cancel_btn.configure(bg='#6b7280')
        cancel_btn.bind('<Enter>', on_cancel_enter)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
        # Enter key binding
        name_entry.bind('<Return>', lambda e: save_changes())
        
        popup.focus_set()
        name_entry.focus()
        name_entry.select_range(0, tk.END)
    
    def delete_channel(self, channel_id):
        """Delete file channel with modern confirmation dialog"""
        # Get channel name for confirmation
        channels = self.db_manager.get_file_channels()
        channel_name = None
        for channel in channels:
            if channel[0] == channel_id:
                channel_name = channel[1]
                break
        
        if not channel_name:
            self.show_popup("Error", "Channel not found", "error")
            return
        
        # Modern confirmation dialog with responsive sizing
        confirm_popup = tk.Toplevel()
        confirm_popup.title("⚠️ Delete Confirmation")
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.transient(self.parent)
        confirm_popup.grab_set()
        
        # Calculate responsive height based on content
        base_height = 374  # Base height for content (320 + 54px = 0.75 inch)
        channel_name_lines = len(channel_name) // 30 + 1  # Estimate lines needed
        dynamic_height = base_height + (channel_name_lines * 20)  # Add space for long names
        dialog_height = min(dynamic_height, 454)  # Cap at 454px (400 + 54px)
        
        center_dialog(confirm_popup, 450, dialog_height)
        
        # Set custom icon
        try:
            confirm_popup.iconbitmap("infor_logo.ico")
        except:
            try:
                icon_path = "infor_logo.png"
                popup_icon = tk.PhotoImage(file=icon_path)
                confirm_popup.iconphoto(False, popup_icon)
            except:
                pass
        
        # Modern header
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=70)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="⚠️ Delete File Channel", 
                font=('Segoe UI', 16, 'bold'), bg='#ef4444', fg='#ffffff').pack(expand=True)
        
        # Content with better spacing
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=30, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        # Warning message with modern styling
        warning_frame = tk.Frame(content_frame, bg='#fef2f2', relief='solid', bd=1,
                                highlightbackground='#fecaca', highlightthickness=1)
        warning_frame.pack(fill="x", pady=(0, 20))
        
        warning_content = tk.Frame(warning_frame, bg='#fef2f2', padx=15, pady=12)
        warning_content.pack(fill="x")
        
        tk.Label(warning_content, text="🗑️ Channel to Delete:", 
                font=('Segoe UI', 10, 'bold'), bg='#fef2f2', fg='#991b1b').pack(anchor="w")
        
        tk.Label(warning_content, text=f"'{channel_name}'", 
                font=('Segoe UI', 12, 'bold'), bg='#fef2f2', fg='#dc2626',
                wraplength=380, justify='left').pack(anchor="w", pady=(5, 0))
        
        tk.Label(content_frame, text="⚠️ This action cannot be undone!", 
                font=('Segoe UI', 11, 'bold'), bg='#ffffff', fg='#f59e0b').pack(pady=(0, 20))
        
        tk.Label(content_frame, text="Are you sure you want to permanently delete this file channel?", 
                font=('Segoe UI', 10), bg='#ffffff', fg='#374151').pack(pady=(0, 25))
        
        # Buttons with modern styling
        btn_frame = tk.Frame(content_frame, bg='#ffffff')
        btn_frame.pack()
        
        def confirm_delete():
            try:
                self.db_manager.delete_file_channel(channel_id)
                confirm_popup.destroy()
                self.load_channels()
                self.show_popup("Success", f"Channel '{channel_name}' deleted successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to delete channel: {str(e)}", "error")
        
        delete_btn = tk.Button(btn_frame, text="🗑️ Yes, Delete", 
                              font=('Segoe UI', 11, 'bold'), bg='#ef4444', fg='#ffffff', 
                              relief='flat', padx=18, pady=10, cursor='hand2', bd=0,
                              command=confirm_delete)
        delete_btn.pack(side="left", padx=(0, 15))
        
        cancel_btn = tk.Button(btn_frame, text="× Cancel", 
                              font=('Segoe UI', 11, 'bold'), bg='#6b7280', fg='#ffffff', 
                              relief='flat', padx=18, pady=10, cursor='hand2', bd=0,
                              command=confirm_popup.destroy)
        cancel_btn.pack(side="left")
        
        # Add hover effects
        def on_delete_enter(e):
            delete_btn.configure(bg='#dc2626')
        def on_delete_leave(e):
            delete_btn.configure(bg='#ef4444')
        delete_btn.bind('<Enter>', on_delete_enter)
        delete_btn.bind('<Leave>', on_delete_leave)
        
        def on_cancel_enter(e):
            cancel_btn.configure(bg='#4b5563')
        def on_cancel_leave(e):
            cancel_btn.configure(bg='#6b7280')
        cancel_btn.bind('<Enter>', on_cancel_enter)
        cancel_btn.bind('<Leave>', on_cancel_leave)
        
        confirm_popup.focus_set()
