#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class EnhancedPopupManager:
    """Enhanced popup system that prevents hiding existing forms"""
    
    def __init__(self):
        self.active_popups = []
        self.popup_offset = 0
    
    def create_non_blocking_popup(self, parent, title, width=400, height=300, modal=False):
        """Create popup that doesn't hide existing forms"""
        popup = tk.Toplevel(parent)
        popup.title(title)
        popup.configure(bg='#ffffff')
        popup.resizable(False, False)
        
        # Set icon if available
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Calculate position with offset to avoid overlap
        screen_w = popup.winfo_screenwidth()
        screen_h = popup.winfo_screenheight()
        
        # Base center position
        base_x = (screen_w // 2) - (width // 2)
        base_y = (screen_h // 2) - (height // 2)
        
        # Apply offset for multiple popups
        offset_x = self.popup_offset * 30
        offset_y = self.popup_offset * 30
        
        x = base_x + offset_x
        y = base_y + offset_y
        
        # Keep within screen bounds
        if x + width > screen_w:
            x = screen_w - width - 50
        if y + height > screen_h:
            y = screen_h - height - 50
        
        # Position popup
        popup.withdraw()
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Configure window behavior
        if modal:
            popup.transient(parent)
            popup.grab_set()
        else:
            # Non-modal: don't grab focus, allow interaction with other windows
            popup.transient()
            popup.attributes('-topmost', False)
        
        popup.deiconify()
        
        # Track popup
        self.active_popups.append(popup)
        self.popup_offset += 1
        
        # Cleanup when popup closes
        def on_close():
            if popup in self.active_popups:
                self.active_popups.remove(popup)
            self.popup_offset = max(0, self.popup_offset - 1)
            popup.destroy()
        
        popup.protocol("WM_DELETE_WINDOW", on_close)
        
        return popup
    
    def center_dialog_enhanced(self, dialog, width=None, height=None, modal=True):
        """Enhanced center dialog that respects existing windows"""
        screen_w = dialog.winfo_screenwidth()
        screen_h = dialog.winfo_screenheight()
        
        w = width if width else 400
        h = height if height else 300
        
        # Calculate position with smart offset
        base_x = (screen_w // 2) - (w // 2)
        base_y = (screen_h // 2) - (h // 2)
        
        # Apply offset if other popups exist
        if len(self.active_popups) > 0:
            offset = len(self.active_popups) * 25
            base_x += offset
            base_y += offset
        
        # Keep within bounds
        if base_x + w > screen_w:
            base_x = screen_w - w - 50
        if base_y + h > screen_h:
            base_y = screen_h - h - 50
        
        dialog.withdraw()
        dialog.geometry(f"{w}x{h}+{base_x}+{base_y}")
        
        if modal:
            dialog.transient()
            dialog.grab_set()
        else:
            dialog.transient()
        
        dialog.deiconify()
        dialog.focus_set()

# Global popup manager instance
popup_manager = EnhancedPopupManager()

def create_enhanced_popup(parent, title, message, status, modal=False):
    """Create enhanced popup that doesn't hide existing forms"""
    popup = popup_manager.create_non_blocking_popup(parent, title, 400, 250, modal)
    
    # Status colors and icons
    if status == "success":
        icon = "✅"
        color = "#10b981"
    elif status == "warning":
        icon = "⚠️"
        color = "#f59e0b"
    else:
        icon = "❌"
        color = "#ef4444"
    
    # Header
    header_frame = tk.Frame(popup, bg=color, height=60)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    header_label = tk.Label(header_frame, text=f"{icon} {title}", 
                           font=('Segoe UI', 14, 'bold'), bg=color, fg='#ffffff')
    header_label.pack(expand=True)
    
    # Content
    content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
    content_frame.pack(fill="both", expand=True)
    
    message_label = tk.Label(content_frame, text=message, 
                            font=('Segoe UI', 10), bg='#ffffff', 
                            justify="left", wraplength=350)
    message_label.pack(pady=(0, 20))
    
    # Close button
    close_btn = tk.Button(content_frame, text="Close", 
                         font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                         relief='flat', padx=20, pady=8, cursor='hand2',
                         bd=0, highlightthickness=0,
                         command=popup.destroy)
    close_btn.pack()
    
    return popup

def create_enhanced_dialog(parent, title, width=400, height=300, modal=True):
    """Create enhanced dialog that doesn't interfere with existing forms"""
    return popup_manager.create_non_blocking_popup(parent, title, width, height, modal)

def enhanced_center_dialog(dialog, width=None, height=None, modal=True):
    """Enhanced centering that respects existing windows"""
    popup_manager.center_dialog_enhanced(dialog, width, height, modal)