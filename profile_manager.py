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
        """Show user profile form"""
        popup = tk.Toplevel()
        popup.title("User Profile")
        center_dialog(popup, 400, 350)
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
        y = self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 175
        popup.geometry(f"400x350+{x}+{y}")
        popup.withdraw()
        popup.update_idletasks()
        popup.deiconify()
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Get user data
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT username, full_name, company, password_hash FROM users WHERE id = ?", (self.user['id'],))
        user_data = cursor.fetchone()
        
        if user_data:
            username, full_name, company, password_hash = user_data
        else:
            username, full_name, company = self.user['username'], self.user['full_name'], ''
        
        # Username (read-only)
        tk.Label(frame, text="Username:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=0, column=0, sticky="w", pady=5)
        username_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10), state='readonly')
        username_entry.grid(row=0, column=1, sticky="ew", padx=10, pady=5)
        username_entry.config(state='normal')
        username_entry.insert(0, username)
        username_entry.config(state='readonly')
        
        # Full Name
        tk.Label(frame, text="Full Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=1, column=0, sticky="w", pady=5)
        fullname_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        fullname_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        fullname_entry.insert(0, full_name)
        
        # Company
        tk.Label(frame, text="Company:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=2, column=0, sticky="w", pady=5)
        company_entry = tk.Entry(frame, width=30, font=('Segoe UI', 10))
        company_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        company_entry.insert(0, company or '')
        
        # Current Password
        tk.Label(frame, text="Current Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=3, column=0, sticky="w", pady=5)
        current_pwd_entry = tk.Entry(frame, width=30, show="•", font=('Segoe UI', 10))
        current_pwd_entry.grid(row=3, column=1, sticky="ew", padx=10, pady=5)
        
        # New Password
        tk.Label(frame, text="New Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=4, column=0, sticky="w", pady=5)
        new_pwd_entry = tk.Entry(frame, width=30, show="•", font=('Segoe UI', 10))
        new_pwd_entry.grid(row=4, column=1, sticky="ew", padx=10, pady=5)
        
        # Confirm Password
        tk.Label(frame, text="Confirm Password:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').grid(row=5, column=0, sticky="w", pady=5)
        confirm_pwd_entry = tk.Entry(frame, width=30, show="•", font=('Segoe UI', 10))
        confirm_pwd_entry.grid(row=5, column=1, sticky="ew", padx=10, pady=5)
        
        frame.grid_columnconfigure(1, weight=1)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        def save_profile():
            new_fullname = fullname_entry.get().strip()
            new_company = company_entry.get().strip()
            current_pwd = current_pwd_entry.get()
            new_pwd = new_pwd_entry.get()
            confirm_pwd = confirm_pwd_entry.get()
            
            # Validate password change if provided
            if new_pwd or confirm_pwd:
                if not current_pwd:
                    self.show_popup("Error", "Please enter current password", "error")
                    return
                
                # Verify current password
                current_hash = hashlib.sha256(current_pwd.encode()).hexdigest()
                if current_hash != password_hash:
                    self.show_popup("Error", "Current password is incorrect", "error")
                    return
                
                if new_pwd != confirm_pwd:
                    self.show_popup("Error", "New passwords do not match", "error")
                    return
                
                if len(new_pwd) < 6:
                    self.show_popup("Error", "New password must be at least 6 characters", "error")
                    return
                
                # Update password
                new_hash = hashlib.sha256(new_pwd.encode()).hexdigest()
                cursor.execute("UPDATE users SET full_name = ?, company = ?, password_hash = ? WHERE id = ?", 
                              (new_fullname, new_company, new_hash, self.user['id']))
            else:
                # Update profile only
                cursor.execute("UPDATE users SET full_name = ?, company = ? WHERE id = ?", 
                              (new_fullname, new_company, self.user['id']))
            
            self.db_manager.conn.commit()
            self.user['full_name'] = new_fullname
            popup.destroy()
            self.show_popup("Success", "Profile updated successfully!", "success")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=save_profile).pack(side="left", padx=(0, 10))
        
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, highlightthickness=0,
                 command=popup.destroy).pack(side="left")
        
        popup.focus_set()