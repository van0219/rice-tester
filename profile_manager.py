#!/usr/bin/env python3

import tkinter as tk

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
import hashlib

class ProfileManager:
    def __init__(self, parent, user, db_manager, show_popup_callback):
        self.parent = parent
        self.user = user
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
    
    def show_profile(self):
        """Show enhanced user profile form with modern UI/UX"""
        popup = tk.Toplevel()
        popup.title("👤 User Profile")
        center_dialog(popup, 480, 628)
        popup.configure(bg='#f8fafc')
        popup.transient(self.parent)
        popup.grab_set()
        popup.resizable(False, False)
        
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
        
        # Modern header with gradient-like effect
        header_frame = tk.Frame(popup, bg='#1e40af', height=84)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#1e40af')
        header_content.pack(expand=True, fill="both", padx=20, pady=15)
        
        tk.Label(header_content, text="👤", font=('Segoe UI', 24), bg='#1e40af', fg='#ffffff').pack(side="left")
        
        header_text_frame = tk.Frame(header_content, bg='#1e40af')
        header_text_frame.pack(side="left", padx=(15, 0), fill="y")
        
        tk.Label(header_text_frame, text="User Profile", font=('Segoe UI', 16, 'bold'), 
                bg='#1e40af', fg='#ffffff').pack(anchor="w")
        tk.Label(header_text_frame, text="Manage your account settings", font=('Segoe UI', 9), 
                bg='#1e40af', fg='#bfdbfe').pack(anchor="w")
        
        # Main content with padding
        main_frame = tk.Frame(popup, bg='#f8fafc', padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)
        
        # Get user data
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT username, full_name, company, password_hash FROM users WHERE id = ?", (self.user['id'],))
        user_data = cursor.fetchone()
        
        if user_data:
            username, full_name, company, password_hash = user_data
        else:
            username, full_name, company = self.user['username'], self.user['full_name'], ''
        
        # Account Information Section
        account_section = tk.Frame(main_frame, bg='#ffffff', relief='solid', bd=1, 
                                  highlightbackground='#e5e7eb', highlightthickness=1)
        account_section.pack(fill="x", pady=(0, 20))
        
        # Section header
        section_header = tk.Frame(account_section, bg='#f3f4f6', height=40)
        section_header.pack(fill="x")
        section_header.pack_propagate(False)
        
        tk.Label(section_header, text="📋 Account Information", font=('Segoe UI', 11, 'bold'), 
                bg='#f3f4f6', fg='#374151').pack(side="left", padx=15, pady=10)
        
        # Account fields
        account_content = tk.Frame(account_section, bg='#ffffff', padx=20, pady=15)
        account_content.pack(fill="x")
        
        # Username (read-only with icon)
        self.create_field_row(account_content, 0, "🔑 Username:", username, readonly=True)
        username_entry = account_content.grid_slaves(row=0, column=1)[0]
        
        # Full Name with icon
        fullname_entry = self.create_field_row(account_content, 1, "👤 Full Name:", full_name)
        
        # Project with icon
        company_entry = self.create_field_row(account_content, 2, "📁 Project:", company or '')
        
        # Password Section
        password_section = tk.Frame(main_frame, bg='#ffffff', relief='solid', bd=1, 
                                   highlightbackground='#e5e7eb', highlightthickness=1)
        password_section.pack(fill="x", pady=(0, 20))
        
        # Password section header
        pwd_header = tk.Frame(password_section, bg='#fef3c7', height=40)
        pwd_header.pack(fill="x")
        pwd_header.pack_propagate(False)
        
        tk.Label(pwd_header, text="🔐 Change Password (Optional)", font=('Segoe UI', 11, 'bold'), 
                bg='#fef3c7', fg='#92400e').pack(side="left", padx=15, pady=10)
        
        # Password fields
        pwd_content = tk.Frame(password_section, bg='#ffffff', padx=20, pady=15)
        pwd_content.pack(fill="x")
        
        current_pwd_entry = self.create_field_row(pwd_content, 0, "🔒 Current Password:", "", password=True)
        new_pwd_entry = self.create_field_row(pwd_content, 1, "🆕 New Password:", "", password=True)
        confirm_pwd_entry = self.create_field_row(pwd_content, 2, "✅ Confirm Password:", "", password=True)
        
        # Password strength indicator
        self.strength_label = tk.Label(pwd_content, text="", font=('Segoe UI', 8), bg='#ffffff')
        self.strength_label.grid(row=3, column=1, sticky="w", pady=(5, 0))
        
        # Bind password strength checker
        new_pwd_entry.bind('<KeyRelease>', lambda e: self.check_password_strength(new_pwd_entry.get()))
        
        account_content.grid_columnconfigure(1, weight=1)
        pwd_content.grid_columnconfigure(1, weight=1)
        
        # Enhanced Action Buttons
        btn_frame = tk.Frame(main_frame, bg='#f8fafc')
        btn_frame.pack(fill="x", pady=(10, 0))
        
        def save_profile():
            new_fullname = fullname_entry.get().strip()
            new_company = company_entry.get().strip()
            current_pwd = current_pwd_entry.get()
            new_pwd = new_pwd_entry.get()
            confirm_pwd = confirm_pwd_entry.get()
            
            # Enhanced validation with better feedback
            if new_pwd or confirm_pwd:
                if not current_pwd:
                    self.show_popup("🔒 Password Required", "Please enter your current password to change it.", "warning")
                    return
                
                # Verify current password
                current_hash = hashlib.sha256(current_pwd.encode()).hexdigest()
                if current_hash != password_hash:
                    self.show_popup("❌ Authentication Failed", "Current password is incorrect. Please try again.", "error")
                    return
                
                if new_pwd != confirm_pwd:
                    self.show_popup("⚠️ Password Mismatch", "New passwords do not match. Please check and try again.", "warning")
                    return
                
                if len(new_pwd) < 6:
                    self.show_popup("📏 Password Too Short", "New password must be at least 6 characters long.", "warning")
                    return
                
                # Update password
                new_hash = hashlib.sha256(new_pwd.encode()).hexdigest()
                cursor.execute("UPDATE users SET full_name = ?, company = ?, password_hash = ? WHERE id = ?", 
                              (new_fullname, new_company, new_hash, self.user['id']))
                success_msg = "Profile and password updated successfully! 🎉"
            else:
                # Update profile only
                cursor.execute("UPDATE users SET full_name = ?, company = ? WHERE id = ?", 
                              (new_fullname, new_company, self.user['id']))
                success_msg = "Profile updated successfully! ✨"
            
            self.db_manager.conn.commit()
            self.user['full_name'] = new_fullname
            popup.destroy()
            self.show_popup("Success", success_msg, "success")
        
        # Modern button styling with hover effects
        save_btn = tk.Button(btn_frame, text="💾 Save Changes", font=('Segoe UI', 11, 'bold'), 
                            bg='#059669', fg='#ffffff', relief='flat', padx=20, pady=10, 
                            cursor='hand2', bd=0, highlightthickness=0, command=save_profile)
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = tk.Button(btn_frame, text="❌ Cancel", font=('Segoe UI', 11, 'bold'), 
                              bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
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
        
        popup.focus_set()
    
    def create_field_row(self, parent, row, label_text, value, readonly=False, password=False):
        """Create a modern field row with enhanced styling"""
        # Label with icon
        label = tk.Label(parent, text=label_text, font=('Segoe UI', 10, 'bold'), 
                        bg='#ffffff', fg='#374151')
        label.grid(row=row, column=0, sticky="w", pady=8, padx=(0, 15))
        
        # Entry field with modern styling
        if password:
            entry = tk.Entry(parent, width=25, font=('Segoe UI', 10), show="•",
                           bg='#f9fafb', fg='#111827', relief='solid', bd=1,
                           highlightbackground='#d1d5db', highlightthickness=1,
                           insertbackground='#3b82f6')
        else:
            entry = tk.Entry(parent, width=25, font=('Segoe UI', 10),
                           bg='#f9fafb' if not readonly else '#f3f4f6', 
                           fg='#111827' if not readonly else '#6b7280',
                           relief='solid', bd=1,
                           highlightbackground='#d1d5db', highlightthickness=1,
                           insertbackground='#3b82f6')
        
        entry.grid(row=row, column=1, sticky="ew", pady=8)
        
        if value:
            entry.insert(0, value)
        
        if readonly:
            entry.config(state='readonly')
        
        # Enhanced focus effects
        def on_focus_in(e):
            if not readonly:
                entry.config(highlightbackground='#3b82f6', highlightthickness=2)
        
        def on_focus_out(e):
            entry.config(highlightbackground='#d1d5db', highlightthickness=1)
        
        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)
        
        return entry
    
    def check_password_strength(self, password):
        """Check and display password strength"""
        if not password:
            self.strength_label.config(text="", fg='#6b7280')
            return
        
        strength = 0
        feedback = []
        
        if len(password) >= 8:
            strength += 1
        else:
            feedback.append("8+ chars")
        
        if any(c.isupper() for c in password):
            strength += 1
        else:
            feedback.append("uppercase")
        
        if any(c.islower() for c in password):
            strength += 1
        else:
            feedback.append("lowercase")
        
        if any(c.isdigit() for c in password):
            strength += 1
        else:
            feedback.append("number")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            strength += 1
        else:
            feedback.append("symbol")
        
        # Display strength
        if strength <= 2:
            self.strength_label.config(text="🔴 Weak - Need: " + ", ".join(feedback[:2]), fg='#dc2626')
        elif strength <= 3:
            self.strength_label.config(text="🟡 Fair - Consider: " + ", ".join(feedback[:1]), fg='#f59e0b')
        elif strength <= 4:
            self.strength_label.config(text="🟢 Good - Strong password!", fg='#059669')
        else:
            self.strength_label.config(text="🟢 Excellent - Very secure!", fg='#059669')
