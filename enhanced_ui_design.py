#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Enhanced RICE Tester UI Design - Best Practice Implementation
Preserves existing functionality while integrating enterprise features
"""

import tkinter as tk
from tkinter import ttk

class EnhancedRiceUI:
    """
    Enhanced UI that follows enterprise testing application best practices:
    1. Dashboard-first approach with contextual integration
    2. Persistent navigation in header
    3. Progressive disclosure via collapsible sidebar
    4. Preserves existing RICE workflow
    """
    
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        self.sidebar_visible = False
        
    def setup_enhanced_header(self, parent):
        """Enhanced header with enterprise navigation"""
        header_frame = tk.Frame(parent, bg='#0f172a', height=65)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Left side - Logo and title
        left_frame = tk.Frame(header_frame, bg='#0f172a')
        left_frame.pack(side="left", padx=25, pady=18)
        
        title_label = tk.Label(left_frame, text="FSM Automated Testing", 
                              font=('Segoe UI', 16, 'bold'), bg='#0f172a', fg='#f8fafc')
        title_label.pack(side="left")
        
        # Center - Enterprise navigation
        nav_frame = tk.Frame(header_frame, bg='#0f172a')
        nav_frame.pack(expand=True)
        
        # Dashboard button
        dashboard_btn = tk.Button(nav_frame, text="📊 Dashboard", 
                                 font=('Segoe UI', 10), bg='#3b82f6', fg='#ffffff',
                                 relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                                 command=self.toggle_dashboard_sidebar)
        dashboard_btn.pack(side="left", padx=5)
        
        # Updates button  
        updates_btn = tk.Button(nav_frame, text="🔄 Updates",
                               font=('Segoe UI', 10), bg='#10b981', fg='#ffffff', 
                               relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                               command=self.show_updates)
        updates_btn.pack(side="left", padx=5)
        
        # Tools button
        tools_btn = tk.Button(nav_frame, text="⚙️ Tools",
                             font=('Segoe UI', 10), bg='#f59e0b', fg='#ffffff',
                             relief='flat', padx=12, pady=6, cursor='hand2', bd=0, 
                             command=self.toggle_tools_sidebar)
        tools_btn.pack(side="left", padx=5)
        
        return header_frame
    
    def setup_main_layout_with_sidebar(self, parent):
        """Main layout with collapsible sidebar"""
        # Main container
        main_container = tk.Frame(parent, bg='#f8fafc')
        main_container.pack(fill="both", expand=True)
        
        # Content area (existing tabs)
        self.content_frame = tk.Frame(main_container, bg='#f8fafc')
        self.content_frame.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        # Sidebar (initially hidden)
        self.sidebar_frame = tk.Frame(main_container, bg='#ffffff', width=350, 
                                     relief='solid', bd=1)
        # Don't pack initially - will be shown/hidden dynamically
        
        return self.content_frame
    
    def setup_enhanced_rice_tab(self, parent):
        """Enhanced RICE tab with contextual dashboard integration"""
        # Main RICE content (preserve existing layout)
        rice_main = tk.Frame(parent, bg='#ffffff')
        rice_main.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        
        # Quick stats sidebar (right side)
        stats_sidebar = tk.Frame(parent, bg='#f8fafc', width=280, relief='solid', bd=1)
        stats_sidebar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        stats_sidebar.pack_propagate(False)
        
        # Quick stats header
        stats_header = tk.Frame(stats_sidebar, bg='#3b82f6', height=50)
        stats_header.pack(fill="x")
        stats_header.pack_propagate(False)
        
        tk.Label(stats_header, text="📊 Quick Stats", font=('Segoe UI', 12, 'bold'),
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Stats content
        stats_content = tk.Frame(stats_sidebar, bg='#f8fafc', padx=15, pady=15)
        stats_content.pack(fill="both", expand=True)
        
        # Quick metrics
        self._create_quick_metric(stats_content, "Tests Today", "12", "#10b981")
        self._create_quick_metric(stats_content, "Success Rate", "94%", "#3b82f6") 
        self._create_quick_metric(stats_content, "Avg Duration", "45s", "#f59e0b")
        
        # Quick actions
        actions_frame = tk.Frame(stats_content, bg='#f8fafc')
        actions_frame.pack(fill="x", pady=(20, 0))
        
        tk.Button(actions_frame, text="📈 Full Dashboard", font=('Segoe UI', 9, 'bold'),
                 bg='#8b5cf6', fg='#ffffff', relief='flat', padx=10, pady=6,
                 cursor='hand2', bd=0, command=self.show_full_dashboard).pack(fill="x", pady=2)
        
        tk.Button(actions_frame, text="🚀 Batch Run", font=('Segoe UI', 9, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=10, pady=6,
                 cursor='hand2', bd=0, command=self.enhanced_batch_run).pack(fill="x", pady=2)
        
        return rice_main
    
    def _create_quick_metric(self, parent, title, value, color):
        """Create a quick metric card"""
        card = tk.Frame(parent, bg=color, relief='solid', bd=1, height=60)
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)
        
        tk.Label(card, text=title, font=('Segoe UI', 9), bg=color, fg='#ffffff').pack(pady=(8, 2))
        tk.Label(card, text=value, font=('Segoe UI', 14, 'bold'), bg=color, fg='#ffffff').pack()
    
    def toggle_dashboard_sidebar(self):
        """Toggle dashboard sidebar visibility"""
        if self.sidebar_visible:
            self.hide_sidebar()
        else:
            self.show_dashboard_sidebar()
    
    def show_dashboard_sidebar(self):
        """Show dashboard in sidebar"""
        self.sidebar_frame.pack(side="right", fill="y", padx=(0, 30), pady=30)
        self.sidebar_visible = True
        
        # Clear and populate sidebar
        for widget in self.sidebar_frame.winfo_children():
            widget.destroy()
            
        # Sidebar header
        header = tk.Frame(self.sidebar_frame, bg='#1e40af', height=50)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text="🏆 Personal Dashboard", font=('Segoe UI', 12, 'bold'),
                bg='#1e40af', fg='#ffffff').pack(side="left", padx=15, expand=True)
        
        tk.Button(header, text="✕", font=('Segoe UI', 12, 'bold'), bg='#1e40af', fg='#ffffff',
                 relief='flat', bd=0, cursor='hand2', command=self.hide_sidebar).pack(side="right", padx=15)
        
        # Dashboard content (scrollable)
        canvas = tk.Canvas(self.sidebar_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(self.sidebar_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Dashboard widgets
        self._populate_dashboard_sidebar(scrollable_frame)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _populate_dashboard_sidebar(self, parent):
        """Populate dashboard sidebar with key metrics"""
        content = tk.Frame(parent, bg='#ffffff', padx=15, pady=15)
        content.pack(fill="x")
        
        # Today's summary
        tk.Label(content, text="Today's Summary", font=('Segoe UI', 11, 'bold'),
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 10))
        
        metrics = [
            ("Tests Run", "12", "#10b981"),
            ("Success Rate", "94%", "#3b82f6"),
            ("Time Saved", "2.5h", "#f59e0b"),
            ("Scenarios", "8", "#8b5cf6")
        ]
        
        for title, value, color in metrics:
            self._create_sidebar_metric(content, title, value, color)
        
        # Recent activity
        tk.Label(content, text="Recent Activity", font=('Segoe UI', 11, 'bold'),
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(20, 10))
        
        activities = [
            ("✅ Scenario #3 - Passed", "2 min ago"),
            ("✅ Scenario #2 - Passed", "5 min ago"), 
            ("❌ Scenario #1 - Failed", "8 min ago")
        ]
        
        for activity, time in activities:
            activity_frame = tk.Frame(content, bg='#f8fafc', relief='solid', bd=1)
            activity_frame.pack(fill="x", pady=2)
            
            tk.Label(activity_frame, text=activity, font=('Segoe UI', 9),
                    bg='#f8fafc', anchor="w").pack(side="left", padx=8, pady=4)
            tk.Label(activity_frame, text=time, font=('Segoe UI', 8),
                    bg='#f8fafc', fg='#6b7280').pack(side="right", padx=8, pady=4)
        
        # Action buttons
        tk.Button(content, text="📈 View Full Analytics", font=('Segoe UI', 10, 'bold'),
                 bg='#3b82f6', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=self.show_full_dashboard).pack(fill="x", pady=(20, 5))
        
        tk.Button(content, text="🏆 View Achievements", font=('Segoe UI', 10, 'bold'),
                 bg='#8b5cf6', fg='#ffffff', relief='flat', padx=15, pady=8, 
                 cursor='hand2', bd=0, command=self.show_achievements).pack(fill="x", pady=5)
    
    def _create_sidebar_metric(self, parent, title, value, color):
        """Create sidebar metric display"""
        metric_frame = tk.Frame(parent, bg='#ffffff')
        metric_frame.pack(fill="x", pady=2)
        
        tk.Label(metric_frame, text=title, font=('Segoe UI', 9),
                bg='#ffffff', anchor="w").pack(side="left")
        tk.Label(metric_frame, text=value, font=('Segoe UI', 9, 'bold'),
                bg='#ffffff', fg=color).pack(side="right")
    
    def hide_sidebar(self):
        """Hide sidebar"""
        self.sidebar_frame.pack_forget()
        self.sidebar_visible = False
    
    def toggle_tools_sidebar(self):
        """Toggle tools sidebar"""
        if self.sidebar_visible:
            self.hide_sidebar()
        else:
            self.show_tools_sidebar()
    
    def show_tools_sidebar(self):
        """Show tools in sidebar"""
        # Similar implementation to dashboard sidebar but with tools
        pass
    
    def show_full_dashboard(self):
        """Show full dashboard in popup"""
        if 'show_personal_dashboard' in self.callbacks:
            self.callbacks['show_personal_dashboard']()
    
    def show_achievements(self):
        """Show achievements popup"""
        pass
    
    def enhanced_batch_run(self):
        """Enhanced batch execution with live tracking"""
        if 'run_all_scenarios' in self.callbacks:
            self.callbacks['run_all_scenarios']()
    
    def show_updates(self):
        """Show updates dialog"""
        pass

# Usage example:
# enhanced_ui = EnhancedRiceUI(parent, callbacks)
# enhanced_ui.setup_enhanced_header(header_container)
# content_area = enhanced_ui.setup_main_layout_with_sidebar(main_container)
# rice_content = enhanced_ui.setup_enhanced_rice_tab(rice_tab_container)
