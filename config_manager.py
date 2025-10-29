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
        """Setup browser configuration tab content"""
        # Original layout (preserves form formatting)
        browser_frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        browser_frame.pack(fill="both", expand=True)
        
        # Browser selection
        tk.Label(browser_frame, text="Browser:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=5)
        
        self.browser_var = tk.StringVar(value="edge")
        browser_frame_inner = tk.Frame(browser_frame, bg='#ffffff')
        browser_frame_inner.grid(row=0, column=1, sticky="w", padx=10)
        
        ttk.Radiobutton(browser_frame_inner, text="Edge", variable=self.browser_var, 
                       value="edge", cursor='hand2').pack(side="left", padx=(0, 10))
        ttk.Radiobutton(browser_frame_inner, text="Chrome", variable=self.browser_var, 
                       value="chrome", cursor='hand2').pack(side="left")
        
        # FSM URL
        tk.Label(browser_frame, text="FSM URL:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=5)
        self.url_entry = tk.Entry(browser_frame, width=50, font=('Segoe UI', 10))
        self.url_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        
        # Username
        tk.Label(browser_frame, text="Username:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(browser_frame, width=50, font=('Segoe UI', 10))
        self.username_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        
        # Password
        tk.Label(browser_frame, text="Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(browser_frame, width=50, show="•", font=('Segoe UI', 10))
        self.password_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # Options
        options_frame = tk.Frame(browser_frame, bg='#ffffff')
        options_frame.grid(row=4, column=1, sticky="w", padx=10, pady=5)
        
        self.incognito_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Incognito mode", variable=self.incognito_var, 
                      font=('Segoe UI', 10), bg='#ffffff').pack(side="left", padx=(0, 20))
        
        self.second_screen_var = tk.BooleanVar()
        tk.Checkbutton(options_frame, text="Open on 2nd screen", variable=self.second_screen_var, 
                      font=('Segoe UI', 10), bg='#ffffff').pack(side="left")
        
        # Buttons frame
        btn_frame = tk.Frame(browser_frame, bg='#ffffff')
        btn_frame.grid(row=5, column=1, sticky="w", padx=10, pady=10)
        
        # Save button
        save_btn = tk.Button(btn_frame, text="💾 Save Config", font=('Segoe UI', 10, 'bold'), 
                            bg='#10b981', fg='#ffffff', relief='flat', 
                            padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                            command=self.save_browser_config)
        save_btn.pack(side="left", padx=(0, 10))
        
        # Test button
        test_btn = tk.Button(btn_frame, text="🚀 Test Browser", font=('Segoe UI', 10, 'bold'), 
                            bg='#3b82f6', fg='#ffffff', relief='flat', 
                            padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                            command=self.test_browser)
        test_btn.pack(side="left")
        
        browser_frame.grid_columnconfigure(1, weight=1)
        
        # Load existing configuration
        self.load_global_config()
    
    def setup_file_channel_tab_content(self, parent):
        """Setup file channel configuration tab content"""
        # Main frame
        channel_frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        channel_frame.pack(fill="both", expand=True)
        
        # File Channels container
        channels_container = tk.Frame(channel_frame, bg='#ffffff')
        channels_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # Headers
        headers_frame = tk.Frame(channels_container, bg='#e5e7eb', height=25)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        # Static headers with padding
        name_label = tk.Label(headers_frame, text="Channel Name", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        name_label.place(relx=0, y=5, relwidth=0.8)
        
        tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#e5e7eb', fg='#374151', anchor='w', padx=18).place(relx=0.8, y=5, relwidth=0.2)
        
        # Column separator for headers
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.8, y=2, height=21)
        
        # File Channels scroll frame
        self.channels_scroll_frame = tk.Frame(channels_container, bg='#ffffff')
        self.channels_scroll_frame.pack(fill="both", expand=True)
        
        # Buttons
        btn_frame = tk.Frame(channel_frame, bg='#ffffff')
        btn_frame.pack(fill="x")
        
        add_channel_btn = ttk.Button(btn_frame, text="➕ Add Channel", style='Primary.TButton',
                                    command=self.add_channel)
        add_channel_btn.pack(side="left", padx=(0, 10))
        add_channel_btn.configure(cursor='hand2')
        
        # Initialize selection tracking
        self.selected_channel_id = None
        
        self.load_channels()
    
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
        """Load file channels with custom table"""
        # Clear existing channel rows
        for widget in self.channels_scroll_frame.winfo_children():
            widget.destroy()
        
        channels = self.db_manager.get_file_channels()
        
        # Display channels with custom rows
        for i, channel in enumerate(channels):
            channel_id, channel_name = channel
            
            # Use normal alternating colors (selection handled separately)
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            # Create row frame
            row_frame = tk.Frame(self.channels_scroll_frame, bg=bg_color, height=30)
            row_frame.pack(fill="x", pady=1)
            row_frame.pack_propagate(False)
            
            # Make entire row clickable and tag it with channel_id
            row_frame.bind('<Button-1>', lambda e, cid=channel_id: self.select_channel(cid))
            row_frame.configure(cursor='hand2')
            row_frame.channel_id = channel_id  # Tag the row with channel_id
            
            # Channel Name (clickable) with padding
            name_label = tk.Label(row_frame, text=channel_name, font=('Segoe UI', 9), 
                                 bg=bg_color, fg='#374151', cursor='hand2', anchor='w', padx=18)
            name_label.place(relx=0, y=8, relwidth=0.8)
            name_label.bind('<Button-1>', lambda e, cid=channel_id: self.select_channel(cid))
            
            # Column separator for rows
            tk.Frame(row_frame, bg='#d1d5db', width=1).place(relx=0.8, y=2, height=26)
            
            # Action buttons frame - dynamically centered (avoid overlapping column separator)
            btn_frame = tk.Frame(row_frame, bg=bg_color)
            btn_frame.place(relx=0.801, y=4, relwidth=0.199, height=22)
            
            # Create buttons
            edit_btn = tk.Button(btn_frame, text="Edit", font=('Segoe UI', 8, 'bold'), 
                               bg='#3b82f6', fg='white', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0,
                               command=lambda cid=channel_id: self.edit_channel(cid))
            
            delete_btn = tk.Button(btn_frame, text="Delete", font=('Segoe UI', 8, 'bold'), 
                                 bg='#ef4444', fg='white', relief='flat', 
                                 padx=4, pady=1, cursor='hand2', bd=0,
                                 command=lambda cid=channel_id: self.delete_channel(cid))
            
            # Left-align buttons with consistent padding
            edit_btn.place(x=18, y=0, width=35, height=22)
            delete_btn.place(x=58, y=0, width=45, height=22)
    
    def add_channel(self):
        """Add file channel dialog"""
        popup = tk.Toplevel()
        popup.title("Dialog")
        center_dialog(popup, 400, 200)
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
        
        # Center popup without animation
        x = self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 200
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 100
        popup.geometry(f"400x200+{x}+{y}")
        popup.withdraw()
        popup.update_idletasks()
        popup.deiconify()
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Channel Name
        tk.Label(frame, text="Channel Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        name_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
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
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=save_channel).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=popup.destroy).pack(side="left")
        
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
        """Edit file channel"""
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
        popup.title("Dialog")
        center_dialog(popup, 400, 200)
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
        
        # Center on screen
        x = (popup.winfo_screenwidth() // 2) - 200
        y = (popup.winfo_screenheight() // 2) - 100
        popup.geometry(f"400x200+{x}+{y}")
        popup.withdraw()
        popup.update_idletasks()
        popup.deiconify()
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Channel Name
        tk.Label(frame, text="Channel Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=40, font=('Segoe UI', 10))
        name_entry.insert(0, current_name)
        name_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
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
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=save_changes).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=popup.destroy).pack(side="left")
        
        popup.focus_set()
        name_entry.focus()
        name_entry.select_range(0, tk.END)
    
    def delete_channel(self, channel_id):
        """Delete file channel with confirmation"""
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
        
        # Confirmation dialog
        confirm_popup = tk.Toplevel()
        confirm_popup.title("Confirm")
        center_dialog(confirm_popup, 400, 236)
        confirm_popup.configure(bg='#ffffff')
        confirm_popup.grab_set()
        
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
        
        # Center on screen
        x = (confirm_popup.winfo_screenwidth() // 2) - 200
        y = (confirm_popup.winfo_screenheight() // 2) - 118
        confirm_popup.geometry(f"400x236+{x}+{y}")
        confirm_popup.withdraw()
        confirm_popup.update_idletasks()
        confirm_popup.deiconify()
        
        # Header
        header_frame = tk.Frame(confirm_popup, bg='#ef4444', height=50)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="⚠️ Delete File Channel", 
                               font=('Segoe UI', 14, 'bold'), bg='#ef4444', fg='#ffffff')
        header_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(confirm_popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        message_label = tk.Label(content_frame, text=f"Are you sure you want to delete:\n'{channel_name}'?\n\nThis action cannot be undone.", 
                                font=('Segoe UI', 10), bg='#ffffff', justify="center")
        message_label.pack(pady=(0, 20))
        
        # Buttons
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
        
        tk.Button(btn_frame, text="Yes, Delete", 
                 font=('Segoe UI', 10, 'bold'), bg='#ef4444', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2',
                 bd=0, highlightthickness=0,
                 command=confirm_delete).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", 
                 font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=6, cursor='hand2',
                 bd=0, highlightthickness=0,
                 command=confirm_popup.destroy).pack(side="left")
        
        confirm_popup.focus_set()