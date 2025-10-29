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
import time

class EnhancedToolTip:
    """Enhanced tooltip with better positioning and visual effects"""
    def __init__(self, widget, text, delay=200):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip = None
        self.enter_time = 0
        self.scheduled = None
        
        # Bind events
        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", self.on_leave, add="+")
        self.widget.bind("<Motion>", self.on_motion, add="+")
        self.widget.bind("<Button-1>", self.on_click, add="+")
    
    def on_enter(self, event=None):
        self.enter_time = time.time() * 1000
        self.schedule_tooltip()
    
    def on_leave(self, event=None):
        self.cancel_tooltip()
        self.hide_tooltip()
    
    def on_motion(self, event=None):
        if self.tooltip:
            # Update tooltip position
            x = event.x_root + 15
            y = event.y_root + 10
            self.tooltip.geometry(f"+{x}+{y}")
    
    def on_click(self, event=None):
        self.hide_tooltip()
    
    def schedule_tooltip(self):
        self.cancel_tooltip()
        self.scheduled = self.widget.after(self.delay, self.show_tooltip)
    
    def cancel_tooltip(self):
        if self.scheduled:
            self.widget.after_cancel(self.scheduled)
            self.scheduled = None
    
    def show_tooltip(self):
        if self.tooltip:
            return
        
        # Get widget position
        x = self.widget.winfo_rootx() + 15
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        
        # Create tooltip window
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_attributes("-topmost", True)
        
        # Style the tooltip
        self.tooltip.configure(bg='#2d3748', relief='solid', bd=1)
        
        # Create frame with padding
        frame = tk.Frame(self.tooltip, bg='#2d3748', padx=3, pady=3)
        frame.pack()
        
        # Add text label
        label = tk.Label(frame, text=self.text, 
                        font=('Segoe UI', 9, 'bold'), 
                        bg='#2d3748', fg='#ffffff',
                        padx=10, pady=6, 
                        relief='flat')
        label.pack()
        
        # Position tooltip
        self.tooltip.geometry(f"+{x}+{y}")
        
        # Ensure tooltip is visible
        self.tooltip.update_idletasks()
        
        # Adjust position if tooltip goes off screen
        screen_width = self.tooltip.winfo_screenwidth()
        screen_height = self.tooltip.winfo_screenheight()
        tooltip_width = self.tooltip.winfo_width()
        tooltip_height = self.tooltip.winfo_height()
        
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        if y + tooltip_height > screen_height:
            y = self.widget.winfo_rooty() - tooltip_height - 5
        
        self.tooltip.geometry(f"+{x}+{y}")
    
    def hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class ToolTip(EnhancedToolTip):
    """Backward compatibility alias"""
    pass

class TableTooltipManager:
    """Enhanced tooltip manager for table action buttons"""
    def __init__(self, tree_widget, actions_config):
        self.tree_widget = tree_widget
        self.actions_config = actions_config  # List of (text, tooltip) tuples
        self.current_tooltip = None
        self.current_tooltip_text = None
        self.hover_delay = 300
        self.scheduled_tooltip = None
        
        # Bind events
        self.tree_widget.bind('<Motion>', self.on_motion, add="+")
        self.tree_widget.bind('<Leave>', self.on_leave, add="+")
        self.tree_widget.bind('<Button-1>', self.on_click, add="+")
    
    def on_motion(self, event):
        item = self.tree_widget.identify_row(event.y)
        column = self.tree_widget.identify_column(event.x)
        
        # Check if it's the actions column (last column)
        if column == f'#{len(self.tree_widget["columns"])}' and item:
            bbox = self.tree_widget.bbox(item, column)
            if bbox:
                relative_x = event.x - bbox[0]
                # Calculate button positions based on text and separators
                actions_text = ['Edit', 'Delete'] if len(self.actions_config) == 2 else ['Run', 'Edit', 'Delete']
                total_width = bbox[2]
                button_width = total_width // len(actions_text)
                
                for i, (action_text, tooltip_text) in enumerate(self.actions_config):
                    button_start = i * button_width
                    button_end = button_start + button_width
                    
                    if button_start <= relative_x <= button_end:
                        if self.current_tooltip_text != tooltip_text:
                            self.schedule_tooltip(event, tooltip_text)
                        return
        
        self.hide_tooltip()
    
    def schedule_tooltip(self, event, text):
        self.cancel_scheduled_tooltip()
        self.scheduled_tooltip = self.tree_widget.after(
            self.hover_delay, 
            lambda: self.show_tooltip(event, text)
        )
    
    def cancel_scheduled_tooltip(self):
        if self.scheduled_tooltip:
            self.tree_widget.after_cancel(self.scheduled_tooltip)
            self.scheduled_tooltip = None
    
    def show_tooltip(self, event, text):
        self.hide_tooltip()
        
        # Create tooltip window
        self.current_tooltip = tk.Toplevel(self.tree_widget)
        self.current_tooltip.wm_overrideredirect(True)
        self.current_tooltip.wm_attributes("-topmost", True)
        self.current_tooltip.configure(bg='#1f2937', relief='solid', bd=1)
        
        # Create frame
        frame = tk.Frame(self.current_tooltip, bg='#1f2937', padx=2, pady=2)
        frame.pack()
        
        # Add label
        label = tk.Label(frame, text=text, 
                        font=('Segoe UI', 9, 'bold'), 
                        bg='#1f2937', fg='#ffffff',
                        padx=10, pady=6, relief='flat')
        label.pack()
        
        # Position tooltip
        x = event.x_root + 15
        y = event.y_root - 30
        
        self.current_tooltip.geometry(f"+{x}+{y}")
        self.current_tooltip_text = text
        
        # Adjust position if off-screen
        self.current_tooltip.update_idletasks()
        screen_width = self.current_tooltip.winfo_screenwidth()
        screen_height = self.current_tooltip.winfo_screenheight()
        tooltip_width = self.current_tooltip.winfo_width()
        tooltip_height = self.current_tooltip.winfo_height()
        
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        if y < 0:
            y = event.y_root + 25
        
        self.current_tooltip.geometry(f"+{x}+{y}")
    
    def hide_tooltip(self):
        self.cancel_scheduled_tooltip()
        if self.current_tooltip:
            self.current_tooltip.destroy()
            self.current_tooltip = None
            self.current_tooltip_text = None
    
    def on_leave(self, event):
        self.hide_tooltip()
    
    def on_click(self, event):
        self.hide_tooltip()

def add_table_tooltips(tree_widget, actions_text):
    """Add tooltips for table action columns - backward compatibility"""
    actions_config = [(action, action) for action in actions_text]
    return TableTooltipManager(tree_widget, actions_config)

def create_button_with_tooltip(parent, text, tooltip_text, command=None, style=None, **kwargs):
    """Create a button with an enhanced tooltip"""
    if style:
        button = ttk.Button(parent, text=text, command=command, style=style, **kwargs)
    else:
        button = tk.Button(parent, text=text, command=command, **kwargs)
    
    # Add tooltip
    EnhancedToolTip(button, tooltip_text)
    
    return button