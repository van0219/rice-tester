#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

def center_dialog(dialog, width=None, height=None):
    """Enhanced center dialog that doesn't hide existing forms"""
    from Temp.enhanced_popup_system import enhanced_center_dialog
    enhanced_center_dialog(dialog, width, height, modal=False)

def configure_smooth_styles():
    """Configure smooth button styles for the application"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure smooth button style
    style.configure('Smooth.TButton',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    style.map('Smooth.TButton',
             background=[('active', '#0ea5e9'),
                        ('pressed', '#0284c7')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Success button (green)
    style.configure('Success.TButton',
                   background='#10b981',
                   foreground='white',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    style.map('Success.TButton',
             background=[('active', '#059669'),
                        ('pressed', '#047857')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Error button (red)
    style.configure('Error.TButton',
                   background='#E53935',
                   foreground='white',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    style.map('Error.TButton',
             background=[('active', '#D32F2F'),
                        ('pressed', '#C62828')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Warning button (blue)
    style.configure('Warning.TButton',
                   background='#2D8CFF',
                   foreground='white',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    style.map('Warning.TButton',
             background=[('active', '#1E7CE8'),
                        ('pressed', '#1A6CD1')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    # Primary button (orange)
    style.configure('Primary.TButton',
                   background='#F15A24',
                   foreground='white',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    # Secondary button (gray)
    style.configure('Secondary.TButton',
                   background='#6b7280',
                   foreground='white',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    # Analytics button (purple)
    style.configure('Analytics.TButton',
                   background='#8b5cf6',
                   foreground='white',
                   relief='flat',
                   borderwidth=0,
                   focuscolor='none',
                   padding=(10, 8),
                   cursor='hand2')
    
    style.map('Primary.TButton',
             background=[('active', '#D14A1F'),
                        ('pressed', '#B8421C')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    style.map('Secondary.TButton',
             background=[('active', '#4b5563'),
                        ('pressed', '#374151')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])
    
    style.map('Analytics.TButton',
             background=[('active', '#7c3aed'),
                        ('pressed', '#6d28d9')],
             relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')])

def create_button_with_tooltip(parent, text, tooltip_text, command=None, style_type='primary', **kwargs):
    """Create a styled button with tooltip"""
    from tooltip_manager import EnhancedToolTip
    
    # Style mapping
    style_map = {
        'primary': 'Primary.TButton',
        'success': 'Success.TButton', 
        'error': 'Error.TButton',
        'warning': 'Warning.TButton',
        'smooth': 'Smooth.TButton'
    }
    
    style = style_map.get(style_type, 'Primary.TButton')
    
    button = ttk.Button(parent, text=text, command=command, style=style, **kwargs)
    EnhancedToolTip(button, tooltip_text, delay=300)
    
    return button

def create_icon_button_with_tooltip(parent, text, tooltip_text, command=None, bg_color='#F15A24', **kwargs):
    """Create an icon-style button with tooltip"""
    from tooltip_manager import EnhancedToolTip
    
    button = tk.Button(parent, text=text, command=command,
                      font=('Segoe UI', 10, 'bold'),
                      bg=bg_color, fg='white',
                      relief='flat', bd=0,
                      padx=8, pady=6,
                      cursor='hand2',
                      **kwargs)
    
    # Add hover effects
    def on_enter(e):
        button.configure(bg=adjust_color(bg_color, -20))
    
    def on_leave(e):
        button.configure(bg=bg_color)
    
    button.bind('<Enter>', on_enter)
    button.bind('<Leave>', on_leave)
    
    EnhancedToolTip(button, tooltip_text, delay=200)
    
    return button

def adjust_color(color, amount):
    """Adjust color brightness"""
    # Simple color adjustment - convert hex to RGB, adjust, convert back
    color = color.lstrip('#')
    rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
    rgb = tuple(max(0, min(255, c + amount)) for c in rgb)
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def create_popup(root, title, message, status):
    """Create a reusable popup window with consistent styling"""
    from Temp.enhanced_popup_system import create_enhanced_popup
    return create_enhanced_popup(root, title, message, status, modal=False)
    
    # Status icon and colors
    if status == "success":
        icon = "✅"
        color = "#10b981"
    elif status == "warning":
        icon = "⚠️"
        color = "#f59e0b"
    else:
        icon = "❌"
        color = "#ef4444"
    
    # Header frame
    header_frame = tk.Frame(popup, bg=color, height=60)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    header_label = tk.Label(header_frame, text=f"{icon} {title}", 
                           font=('Segoe UI', 14, 'bold'), bg=color, fg='#ffffff')
    header_label.pack(expand=True)
    
    # Content frame
    content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
    content_frame.pack(fill="both", expand=True)
    
    # Message text
    message_label = tk.Label(content_frame, text=message, 
                            font=('Segoe UI', 10), bg='#ffffff', 
                            justify="left", wraplength=350)
    message_label.pack(pady=(0, 20))
    
    # Close button
    close_btn = tk.Button(content_frame, text="Close", 
                         font=('Segoe UI', 10, 'bold'), bg='#6C757D', fg='#ffffff', 
                         relief='flat', padx=20, pady=8, cursor='hand2',
                         bd=0, highlightthickness=0,
                         command=popup.destroy)
    close_btn.pack()
    
    popup.focus_set()
    return popup