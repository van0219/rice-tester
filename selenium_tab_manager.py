#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning without blinking"""
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    w = width if width else 400
    h = height if height else 300
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()

class TabManager:
    def __init__(self, parent):
        self.parent = parent
        self.tabs = {}
        self.tab_buttons = {}
        self.active_tab = None
        self._tab_scroll_pos = 0
        self._arrows_visible = False
        
    def setup_tab_system(self, container):
        """Setup modern tab system with scrolling"""
        self.tab_container = tk.Frame(container, bg='#f8fafc')
        self.tab_container.pack(fill="both", expand=True)
        
        # Tab header frame with arrow navigation
        self.tab_header_container = tk.Frame(self.tab_container, bg='#ffffff', height=50)
        self.tab_header_container.pack(fill="x", padx=1, pady=(1, 0))
        self.tab_header_container.pack_propagate(False)
        
        # Left arrow button
        self.left_arrow = tk.Button(self.tab_header_container, text="◀", font=('Segoe UI', 12), 
                                   bg='#f8fafc', fg='#6b7280', relief='flat', 
                                   padx=8, pady=12, cursor='hand2', bd=0,
                                   command=self._scroll_tabs_left)
        
        # Right arrow button  
        self.right_arrow = tk.Button(self.tab_header_container, text="▶", font=('Segoe UI', 12),
                                    bg='#f8fafc', fg='#6b7280', relief='flat',
                                    padx=8, pady=12, cursor='hand2', bd=0,
                                    command=self._scroll_tabs_right)
        
        # Tab canvas for scrolling
        self.tab_canvas = tk.Canvas(self.tab_header_container, bg='#ffffff', height=50, highlightthickness=0)
        self.tab_header = tk.Frame(self.tab_canvas, bg='#ffffff')
        
        self.tab_header.bind("<Configure>", lambda e: self._update_tab_arrows())
        self.tab_canvas.create_window((0, 0), window=self.tab_header, anchor="nw")
        self.tab_canvas.configure(scrollregion=(0, 0, 0, 0))
        
        # Pack elements
        self.tab_canvas.pack(side="left", fill="both", expand=True)
        
        # Tab content frame
        self.tab_content = tk.Frame(self.tab_container, bg='#ffffff')
        self.tab_content.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        return self.tab_content
    
    def add_tab(self, name, setup_func):
        """Add a modern flat tab"""
        # Create tab button with disabled hover effects
        tab_btn = tk.Button(self.tab_header, text=name, font=('Segoe UI', 10), 
                           bg='#ffffff', fg='#6b7280', relief='flat', 
                           padx=20, pady=12, cursor='hand2', bd=0,
                           activebackground='#ffffff', activeforeground='#6b7280',
                           command=lambda: self.show_tab(name))
        tab_btn.pack(side="left")
        
        # Create persistent border frame
        border_frame = tk.Frame(self.tab_header, bg='#ffffff', height=3)
        border_frame.place(in_=tab_btn, relx=0, rely=1, relwidth=1, anchor='sw')
        tab_btn.border_frame = border_frame
        
        # Store tab info
        self.tab_buttons[name] = tab_btn
        self.tabs[name] = {'setup_func': setup_func}
    
    def show_tab(self, name):
        """Show selected tab with modern styling"""
        # Update button styles
        for tab_name, btn in self.tab_buttons.items():
            if tab_name == name:
                # Active tab style
                btn.configure(bg='#f8fafc', fg='#1f2937', relief='flat',
                             activebackground='#f8fafc', activeforeground='#1f2937')
                # Show blue border
                btn.border_frame.configure(bg='#3b82f6')
            else:
                # Inactive tab style
                btn.configure(bg='#ffffff', fg='#6b7280', relief='flat',
                             activebackground='#ffffff', activeforeground='#6b7280')
                # Hide border
                btn.border_frame.configure(bg='#ffffff')
        
        # Clear current content
        for widget in self.tab_content.winfo_children():
            widget.destroy()
        
        # Execute tab setup function
        if name in self.tabs:
            self.tabs[name]['setup_func'](self.tab_content)
        
        self.active_tab = name
    
    def _update_tab_arrows(self):
        """Show/hide arrow buttons based on tab overflow"""
        try:
            self.parent.update_idletasks()
            canvas_width = self.tab_canvas.winfo_width()
            content_width = self.tab_header.winfo_reqwidth()
            
            # Update scroll region
            self.tab_canvas.configure(scrollregion=(0, 0, content_width, 0))
            
            needs_arrows = content_width > canvas_width and canvas_width > 50
            
            if needs_arrows and not self._arrows_visible:
                self.left_arrow.pack(side="left", padx=(0, 2))
                self.right_arrow.pack(side="right", padx=(2, 0))
                self._arrows_visible = True
                self._update_arrow_states()
            elif not needs_arrows and self._arrows_visible:
                self.left_arrow.pack_forget()
                self.right_arrow.pack_forget()
                self._arrows_visible = False
                self._tab_scroll_pos = 0
                self.tab_canvas.xview_moveto(0)
        except tk.TclError:
            pass
    
    def _update_arrow_states(self):
        """Show/hide arrow buttons based on scroll position"""
        try:
            # Get current scroll position
            left_pos, right_pos = self.tab_canvas.xview()
            
            # Show/hide left arrow
            if left_pos <= 0.01:  # At the beginning
                self.left_arrow.pack_forget()
            else:
                if not self.left_arrow.winfo_viewable():
                    self.left_arrow.pack(side="left", padx=(0, 2), before=self.tab_canvas)
            
            # Show/hide right arrow
            if right_pos >= 0.99:  # At the end
                self.right_arrow.pack_forget()
            else:
                if not self.right_arrow.winfo_viewable():
                    self.right_arrow.pack(side="right", padx=(2, 0))
        except tk.TclError:
            pass
    
    def _scroll_tabs_left(self):
        """Scroll tabs to the left"""
        current_left, current_right = self.tab_canvas.xview()
        new_pos = max(0, current_left - 0.3)
        self.tab_canvas.xview_moveto(new_pos)
        self._update_arrow_states()
    
    def _scroll_tabs_right(self):
        """Scroll tabs to the right"""
        current_left, current_right = self.tab_canvas.xview()
        new_pos = min(1.0, current_left + 0.3)
        self.tab_canvas.xview_moveto(new_pos)
        self._update_arrow_states()