#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
try:
    from enhanced_popup_system import create_enhanced_dialog
except ImportError:
    from Temp.enhanced_popup_system import create_enhanced_dialog

class PersonalAnalytics:
    """
    Personal Analytics Dashboard - Privacy-First Design
    Shows individual insights and trends to make users feel like testing superheroes!
    """
    
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.user_id = db_manager.user_id
    
    def show_full_analytics(self):
        """Show full analytics dashboard with trends and charts"""
        dashboard = create_enhanced_dialog(None, "📊 Full Analytics Dashboard", 1000, 700, modal=False)
        dashboard.resizable(True, True)  # Enable maximize for trends charts
        dashboard.state('zoomed')  # Start maximized for better chart viewing
        
        try:
            dashboard.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(dashboard, bg='#1e40af', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="📊 Full Analytics Dashboard", 
                              font=('Segoe UI', 18, 'bold'), bg='#1e40af', fg='#ffffff')
        title_label.pack(side="left", padx=25, pady=25)
        
        # Main content with tabs
        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Overview & Trends tabs only
        self._create_overview_tab(notebook)
        self._create_trends_tab(notebook)
        
        # Close button
        close_frame = tk.Frame(dashboard, bg='#ffffff', pady=15)
        close_frame.pack(fill="x")
        
        tk.Button(close_frame, text="Close Dashboard", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=25, pady=10, 
                 cursor='hand2', bd=0, command=dashboard.destroy).pack()
    
    def show_achievements(self):
        """Show achievements dashboard"""
        dashboard = create_enhanced_dialog(None, "🏆 Achievements Dashboard", 800, 600, modal=False)
        dashboard.resizable(True, True)  # Enable maximize
        
        try:
            dashboard.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(dashboard, bg='#1e40af', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🏆 Your Achievements", 
                              font=('Segoe UI', 18, 'bold'), bg='#1e40af', fg='#ffffff')
        title_label.pack(side="left", padx=25, pady=25)
        
        # Main content with tabs
        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Achievements & Optimization tabs only
        self._create_achievements_tab(notebook)
        self._create_optimization_tab(notebook)
        
        # Close button
        close_frame = tk.Frame(dashboard, bg='#ffffff', pady=15)
        close_frame.pack(fill="x")
        
        tk.Button(close_frame, text="Close Dashboard", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=25, pady=10, 
                 cursor='hand2', bd=0, command=dashboard.destroy).pack()
    
    def show_personal_dashboard(self):
        """Show comprehensive personal analytics dashboard"""
        dashboard = create_enhanced_dialog(None, "🏆 Your Personal Testing Dashboard", 1000, 700, modal=False)
        
        try:
            dashboard.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(dashboard, bg='#1e40af', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🏆 Your Personal Testing Dashboard", 
                              font=('Segoe UI', 18, 'bold'), bg='#1e40af', fg='#ffffff')
        title_label.pack(side="left", padx=25, pady=25)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, text="Your journey to testing excellence!", 
                                 font=('Segoe UI', 11), bg='#1e40af', fg='#bfdbfe')
        subtitle_label.pack(side="right", padx=25, pady=25)
        
        # Main content with tabs
        notebook = ttk.Notebook(dashboard)
        notebook.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tab 1: Overview & Stats
        self._create_overview_tab(notebook)
        
        # Tab 2: Performance Trends
        self._create_trends_tab(notebook)
        
        # Tab 3: Achievements & Insights
        self._create_achievements_tab(notebook)
        
        # Tab 4: Optimization Suggestions
        self._create_optimization_tab(notebook)
        
        # Close button
        close_frame = tk.Frame(dashboard, bg='#ffffff', pady=15)
        close_frame.pack(fill="x")
        
        tk.Button(close_frame, text="Close Dashboard", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=25, pady=10, 
                 cursor='hand2', bd=0, command=dashboard.destroy).pack()
    
    def _create_overview_tab(self, notebook):
        """Create overview statistics tab"""
        overview_frame = tk.Frame(notebook, bg='#ffffff')
        notebook.add(overview_frame, text="📊 Overview")
        
        # Scrollable content
        canvas = tk.Canvas(overview_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(overview_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get personal statistics
        stats = self._get_personal_statistics()
        
        # Stats cards
        cards_frame = tk.Frame(scrollable_frame, bg='#ffffff', padx=20, pady=20)
        cards_frame.pack(fill="x")
        
        # Row 1: Core metrics
        row1 = tk.Frame(cards_frame, bg='#ffffff')
        row1.pack(fill="x", pady=(0, 15))
        
        self._create_stat_card(row1, "🎯 Total Tests", str(stats['total_tests']), "#3b82f6", 0)
        self._create_stat_card(row1, "✅ Success Rate", f"{stats['success_rate']:.1f}%", "#10b981", 1)
        self._create_stat_card(row1, "⚡ Avg Duration", f"{stats['avg_duration']:.1f}s", "#f59e0b", 2)
        self._create_stat_card(row1, "🔥 Current Streak", f"{stats['current_streak']} days", "#ef4444", 3)
        
        # Row 2: Recent activity
        row2 = tk.Frame(cards_frame, bg='#ffffff')
        row2.pack(fill="x", pady=(0, 15))
        
        self._create_stat_card(row2, "📅 Tests Today", str(stats['tests_today']), "#8b5cf6", 0)
        self._create_stat_card(row2, "✅ Passed Today", str(stats['passed_today']), "#10b981", 1)
        self._create_stat_card(row2, "❌ Failed Today", str(stats['failed_today']), "#ef4444", 2)
        self._create_stat_card(row2, "📈 Today's Rate", f"{stats['success_rate_today']:.1f}%" if stats['tests_today'] > 0 else "0.0%", "#06b6d4", 3)
        
        # Recent activity section
        activity_frame = tk.Frame(scrollable_frame, bg='#f8fafc', relief='solid', bd=1)
        activity_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        tk.Label(activity_frame, text="📋 Recent Activity", font=('Segoe UI', 14, 'bold'), 
                bg='#f8fafc', fg='#1e40af').pack(anchor="w", padx=15, pady=(15, 10))
        
        recent_tests = self._get_recent_tests()
        for test in recent_tests[:5]:  # Show last 5 tests
            test_frame = tk.Frame(activity_frame, bg='#ffffff', relief='solid', bd=1)
            test_frame.pack(fill="x", padx=15, pady=2)
            
            # Test info
            info_frame = tk.Frame(test_frame, bg='#ffffff')
            info_frame.pack(fill="x", padx=10, pady=8)
            
            # Status icon and scenario
            status_icon = "✅" if test['result'] == 'Passed' else "❌" if test['result'] == 'Failed' else "⏸️"
            tk.Label(info_frame, text=f"{status_icon} Scenario #{test['scenario_number']}", 
                    font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(side="left")
            
            # Timestamp
            tk.Label(info_frame, text=test['executed_at'], font=('Segoe UI', 9), 
                    bg='#ffffff', fg='#6b7280').pack(side="right")
        
        # Enable mouse wheel scrolling for overview
        def _on_mousewheel_overview(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scroll events to canvas and scrollable frame
        canvas.bind("<MouseWheel>", _on_mousewheel_overview)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel_overview)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_trends_tab(self, notebook):
        """Create performance trends tab with charts"""
        trends_frame = tk.Frame(notebook, bg='#ffffff')
        notebook.add(trends_frame, text="📈 Trends")
        
        # Scrollable content with both vertical and horizontal scrolling
        canvas = tk.Canvas(trends_frame, bg='#ffffff')
        v_scrollbar = ttk.Scrollbar(trends_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(trends_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Chart container
        chart_frame = tk.Frame(scrollable_frame, bg='#ffffff', padx=20, pady=20)
        chart_frame.pack(fill="both", expand=True)
        
        # Create matplotlib figure with optimal size for dashboard viewing
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        fig.patch.set_facecolor('#ffffff')
        
        # Chart 1: Success rate over time
        trend_data = self._get_trend_data()
        if trend_data:
            dates = [item['date'] for item in trend_data]
            success_rates = [item['success_rate'] for item in trend_data]
            
            ax1.plot(dates, success_rates, color='#10b981', linewidth=2, marker='o')
            ax1.set_title('Success Rate Trend', fontsize=12, fontweight='bold')
            ax1.set_ylabel('Success Rate (%)')
            ax1.grid(True, alpha=0.3)
        
        # Chart 2: Test duration trends
        if trend_data:
            durations = [item['avg_duration'] for item in trend_data]
            ax2.plot(dates, durations, color='#f59e0b', linewidth=2, marker='s')
            ax2.set_title('Average Duration Trend', fontsize=12, fontweight='bold')
            ax2.set_ylabel('Duration (seconds)')
            ax2.grid(True, alpha=0.3)
        
        # Chart 3: Tests per day
        if trend_data:
            test_counts = [item['test_count'] for item in trend_data]
            ax3.bar(dates, test_counts, color='#3b82f6', alpha=0.7)
            ax3.set_title('Daily Test Activity', fontsize=12, fontweight='bold')
            ax3.set_ylabel('Number of Tests')
        
        # Chart 4: Scenario success rates
        scenario_stats = self._get_scenario_statistics()
        if scenario_stats:
            scenarios = [f"#{item['scenario_number']}" for item in scenario_stats]
            rates = [item['success_rate'] for item in scenario_stats]
            colors = ['#10b981' if rate >= 90 else '#f59e0b' if rate >= 70 else '#ef4444' for rate in rates]
            
            ax4.bar(scenarios, rates, color=colors, alpha=0.7)
            ax4.set_title('Scenario Success Rates', fontsize=12, fontweight='bold')
            ax4.set_ylabel('Success Rate (%)')
            ax4.set_ylim(0, 100)
        
        plt.tight_layout(pad=2.0)  # Add padding for better readability
        
        # Embed chart in tkinter
        canvas_widget = FigureCanvasTkAgg(fig, chart_frame)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(fill="both", expand=True)
        
        # Enable mouse wheel scrolling for trends (both vertical and horizontal)
        def _on_mousewheel_trends(event):
            # Vertical scrolling with mouse wheel
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _on_shift_mousewheel_trends(event):
            # Horizontal scrolling with Shift+mouse wheel
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scroll events to canvas and all child widgets
        canvas.bind("<MouseWheel>", _on_mousewheel_trends)
        canvas.bind("<Shift-MouseWheel>", _on_shift_mousewheel_trends)
        canvas_widget.get_tk_widget().bind("<MouseWheel>", _on_mousewheel_trends)
        canvas_widget.get_tk_widget().bind("<Shift-MouseWheel>", _on_shift_mousewheel_trends)
        
        # Also bind to the scrollable frame
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel_trends)
        scrollable_frame.bind("<Shift-MouseWheel>", _on_shift_mousewheel_trends)
        
        # Pack scrollbars and canvas
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
    
    def _create_achievements_tab(self, notebook):
        """Create achievements and insights tab"""
        achievements_frame = tk.Frame(notebook, bg='#ffffff')
        notebook.add(achievements_frame, text="🏆 Achievements")
        
        # Scrollable content
        canvas = tk.Canvas(achievements_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(achievements_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Achievements section
        achievements = self._get_personal_achievements()
        
        # Unlocked achievements
        unlocked_frame = tk.Frame(scrollable_frame, bg='#ffffff', padx=20, pady=20)
        unlocked_frame.pack(fill="x")
        
        tk.Label(unlocked_frame, text="🏆 Unlocked Achievements", font=('Segoe UI', 16, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 15))
        
        for achievement in achievements['unlocked']:
            self._create_achievement_card(unlocked_frame, achievement, True)
        
        # Progress towards next achievements
        progress_frame = tk.Frame(scrollable_frame, bg='#ffffff', padx=20, pady=20)
        progress_frame.pack(fill="x")
        
        tk.Label(progress_frame, text="🎯 Progress Towards Next", font=('Segoe UI', 16, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 15))
        
        for achievement in achievements['in_progress']:
            self._create_achievement_card(progress_frame, achievement, False)
        
        # Enable mouse wheel scrolling for achievements
        def _on_mousewheel_achievements(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scroll events to canvas and scrollable frame
        canvas.bind("<MouseWheel>", _on_mousewheel_achievements)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel_achievements)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_optimization_tab(self, notebook):
        """Create optimization suggestions tab"""
        optimization_frame = tk.Frame(notebook, bg='#ffffff')
        notebook.add(optimization_frame, text="💡 Suggestions")
        
        # Scrollable content
        canvas = tk.Canvas(optimization_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(optimization_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Content
        content_frame = tk.Frame(scrollable_frame, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="💡 Personalized Optimization Suggestions", 
                font=('Segoe UI', 16, 'bold'), bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 20))
        
        suggestions = self._get_optimization_suggestions()
        
        for suggestion in suggestions:
            self._create_suggestion_card(content_frame, suggestion)
        
        # Enable mouse wheel scrolling for optimization
        def _on_mousewheel_optimization(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind scroll events to canvas and scrollable frame
        canvas.bind("<MouseWheel>", _on_mousewheel_optimization)
        scrollable_frame.bind("<MouseWheel>", _on_mousewheel_optimization)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _create_stat_card(self, parent, title, value, color, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief='solid', bd=1, width=200, height=100)
        card.grid(row=0, column=column, padx=10, sticky="ew")
        card.grid_propagate(False)
        parent.grid_columnconfigure(column, weight=1)
        
        # Title
        tk.Label(card, text=title, font=('Segoe UI', 10, 'bold'), 
                bg=color, fg='#ffffff').pack(pady=(15, 5))
        
        # Value
        tk.Label(card, text=value, font=('Segoe UI', 18, 'bold'), 
                bg=color, fg='#ffffff').pack()
    
    def _create_achievement_card(self, parent, achievement, unlocked):
        """Create an achievement card"""
        bg_color = '#10b981' if unlocked else '#f3f4f6'
        text_color = '#ffffff' if unlocked else '#6b7280'
        
        card = tk.Frame(parent, bg=bg_color, relief='solid', bd=1, height=80)
        card.pack(fill="x", pady=5)
        card.pack_propagate(False)
        
        # Icon and title
        info_frame = tk.Frame(card, bg=bg_color)
        info_frame.pack(fill="x", padx=15, pady=15)
        
        icon_label = tk.Label(info_frame, text=achievement['icon'], font=('Segoe UI', 20), 
                bg=bg_color)
        icon_label.pack(side="left", padx=(0, 10))
        
        text_frame = tk.Frame(info_frame, bg=bg_color)
        text_frame.pack(side="left", fill="x", expand=True)
        
        title_label = tk.Label(text_frame, text=achievement['title'], font=('Segoe UI', 12, 'bold'), 
                bg=bg_color, fg=text_color, anchor="w")
        title_label.pack(fill="x")
        
        desc_label = tk.Label(text_frame, text=achievement['description'], font=('Segoe UI', 9), 
                bg=bg_color, fg=text_color, anchor="w")
        desc_label.pack(fill="x")
        
        # Bind scroll events to all card elements
        def bind_scroll_to_widget(widget):
            def scroll_handler(event):
                # Find the canvas by traversing up the widget hierarchy
                current = widget
                while current and not hasattr(current, 'yview_scroll'):
                    current = current.master
                if current and hasattr(current, 'yview_scroll'):
                    current.yview_scroll(int(-1*(event.delta/120)), "units")
            widget.bind("<MouseWheel>", scroll_handler)
        
        bind_scroll_to_widget(card)
        bind_scroll_to_widget(info_frame)
        bind_scroll_to_widget(icon_label)
        bind_scroll_to_widget(text_frame)
        bind_scroll_to_widget(title_label)
        bind_scroll_to_widget(desc_label)
        
        if not unlocked and 'progress' in achievement:
            # Progress bar
            progress_frame = tk.Frame(card, bg=bg_color)
            progress_frame.pack(fill="x", padx=15, pady=(0, 10))
            
            progress_bar = tk.Frame(progress_frame, bg='#d1d5db', height=6)
            progress_bar.pack(fill="x")
            
            progress_fill = tk.Frame(progress_bar, bg='#3b82f6', height=6)
            progress_fill.place(relwidth=achievement['progress']/100, relheight=1)
            
            tk.Label(progress_frame, text=f"{achievement['progress']:.0f}% complete", 
                    font=('Segoe UI', 8), bg=bg_color, fg=text_color).pack(anchor="e")
    
    def _create_suggestion_card(self, parent, suggestion):
        """Create an optimization suggestion card"""
        card = tk.Frame(parent, bg='#fef3c7', relief='solid', bd=1)
        card.pack(fill="x", pady=10)
        
        # Content
        content_frame = tk.Frame(card, bg='#fef3c7', padx=15, pady=15)
        content_frame.pack(fill="x")
        
        # Icon and title
        header_frame = tk.Frame(content_frame, bg='#fef3c7')
        header_frame.pack(fill="x", pady=(0, 10))
        
        icon_label = tk.Label(header_frame, text=suggestion['icon'], font=('Segoe UI', 16), 
                bg='#fef3c7')
        icon_label.pack(side="left", padx=(0, 10))
        
        title_label = tk.Label(header_frame, text=suggestion['title'], font=('Segoe UI', 12, 'bold'), 
                bg='#fef3c7', fg='#92400e')
        title_label.pack(side="left")
        
        # Description
        desc_label = tk.Label(content_frame, text=suggestion['description'], font=('Segoe UI', 10), 
                bg='#fef3c7', fg='#451a03', wraplength=800, justify="left")
        desc_label.pack(fill="x")
        
        # Action button
        action_btn = None
        if 'action' in suggestion:
            action_btn = tk.Button(content_frame, text=suggestion['action'], font=('Segoe UI', 9, 'bold'), 
                     bg='#f59e0b', fg='#ffffff', relief='flat', padx=15, pady=5, 
                     cursor='hand2', bd=0)
            action_btn.pack(anchor="w", pady=(10, 0))
        
        # Bind scroll events to all card elements
        def bind_scroll_to_widget(widget):
            def scroll_handler(event):
                # Find the canvas by traversing up the widget hierarchy
                current = widget
                while current and not hasattr(current, 'yview_scroll'):
                    current = current.master
                if current and hasattr(current, 'yview_scroll'):
                    current.yview_scroll(int(-1*(event.delta/120)), "units")
            widget.bind("<MouseWheel>", scroll_handler)
        
        bind_scroll_to_widget(card)
        bind_scroll_to_widget(content_frame)
        bind_scroll_to_widget(header_frame)
        bind_scroll_to_widget(icon_label)
        bind_scroll_to_widget(title_label)
        bind_scroll_to_widget(desc_label)
        if action_btn:
            bind_scroll_to_widget(action_btn)
    
    def _get_personal_statistics(self):
        """Get personal testing statistics"""
        cursor = self.db_manager.conn.cursor()
        
        # Basic stats
        cursor.execute("""
            SELECT COUNT(*) as total_tests,
                   AVG(CASE WHEN result = 'Passed' THEN 1.0 ELSE 0.0 END) * 100 as success_rate,
                   COUNT(CASE WHEN DATE(executed_at) >= DATE('now', '-7 days') THEN 1 END) as tests_this_week
            FROM scenarios 
            WHERE user_id = ? AND executed_at IS NOT NULL
        """, (self.user_id,))
        
        basic_stats = cursor.fetchone()
        
        # Today's actual data
        cursor.execute("""
            SELECT COUNT(*) as tests_today,
                   AVG(CASE WHEN result = 'Passed' THEN 1.0 ELSE 0.0 END) * 100 as success_rate_today,
                   COUNT(CASE WHEN result = 'Passed' THEN 1 END) as passed_today,
                   COUNT(CASE WHEN result = 'Failed' THEN 1 END) as failed_today
            FROM scenarios 
            WHERE user_id = ? AND DATE(executed_at) = DATE('now') AND executed_at IS NOT NULL
        """, (self.user_id,))
        
        today_stats = cursor.fetchone()
        
        # Calculate additional metrics
        stats = {
            'total_tests': basic_stats[0] if basic_stats[0] else 0,
            'success_rate': basic_stats[1] if basic_stats[1] else 0,
            'tests_this_week': basic_stats[2] if basic_stats[2] else 0,
            'tests_today': today_stats[0] if today_stats[0] else 0,
            'success_rate_today': today_stats[1] if today_stats[1] else 0,
            'passed_today': today_stats[2] if today_stats[2] else 0,
            'failed_today': today_stats[3] if today_stats[3] else 0,
            'avg_duration': 45.5,  # Placeholder - would calculate from execution logs
            'current_streak': 3,   # Placeholder - consecutive days with tests
            'best_day': 'Monday',  # Placeholder - day with highest success rate
            'improvement': 12.5,   # Placeholder - improvement over last month
            'quality_score': 8.5   # Placeholder - overall quality score
        }
        
        return stats
    
    def _get_recent_tests(self):
        """Get recent test executions"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT scenario_number, result, executed_at, description
            FROM scenarios 
            WHERE user_id = ? AND executed_at IS NOT NULL
            ORDER BY executed_at DESC
            LIMIT 10
        """, (self.user_id,))
        
        tests = []
        for row in cursor.fetchall():
            tests.append({
                'scenario_number': row[0],
                'result': row[1],
                'executed_at': row[2],
                'description': row[3]
            })
        
        return tests
    
    def _get_trend_data(self):
        """Get trend data for charts"""
        # Placeholder data - would calculate from actual test history
        return [
            {'date': '2025-01-22', 'success_rate': 85, 'avg_duration': 67, 'test_count': 5},
            {'date': '2025-01-23', 'success_rate': 92, 'avg_duration': 62, 'test_count': 8},
            {'date': '2025-01-24', 'success_rate': 88, 'avg_duration': 59, 'test_count': 6},
            {'date': '2025-01-25', 'success_rate': 95, 'avg_duration': 55, 'test_count': 7},
            {'date': '2025-01-26', 'success_rate': 90, 'avg_duration': 58, 'test_count': 9},
            {'date': '2025-01-27', 'success_rate': 94, 'avg_duration': 52, 'test_count': 4},
            {'date': '2025-01-28', 'success_rate': 97, 'avg_duration': 48, 'test_count': 6}
        ]
    
    def _get_scenario_statistics(self):
        """Get statistics by scenario"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("""
            SELECT scenario_number,
                   AVG(CASE WHEN result = 'Passed' THEN 1.0 ELSE 0.0 END) * 100 as success_rate,
                   COUNT(*) as total_runs
            FROM scenarios 
            WHERE user_id = ? AND executed_at IS NOT NULL
            GROUP BY scenario_number
            ORDER BY scenario_number
        """, (self.user_id,))
        
        scenarios = []
        for row in cursor.fetchall():
            scenarios.append({
                'scenario_number': row[0],
                'success_rate': row[1] if row[1] else 0,
                'total_runs': row[2]
            })
        
        return scenarios
    
    def _get_personal_achievements(self):
        """Get personal achievements"""
        stats = self._get_personal_statistics()
        
        achievements = {
            'unlocked': [],
            'in_progress': []
        }
        
        # Check various achievement criteria
        if stats['total_tests'] >= 10:
            achievements['unlocked'].append({
                'icon': '🎯',
                'title': 'Getting Started',
                'description': 'Completed your first 10 tests'
            })
        
        if stats['success_rate'] >= 90:
            achievements['unlocked'].append({
                'icon': '🏆',
                'title': 'Excellence',
                'description': 'Achieved 90%+ success rate'
            })
        
        if stats['tests_this_week'] >= 5:
            achievements['unlocked'].append({
                'icon': '🔥',
                'title': 'Active Tester',
                'description': 'Ran 5+ tests this week'
            })
        
        # Progress towards next achievements
        if stats['total_tests'] < 50:
            achievements['in_progress'].append({
                'icon': '🚀',
                'title': 'Power User',
                'description': 'Complete 50 total tests',
                'progress': (stats['total_tests'] / 50) * 100
            })
        
        if stats['success_rate'] < 95:
            achievements['in_progress'].append({
                'icon': '💎',
                'title': 'Perfectionist',
                'description': 'Achieve 95%+ success rate',
                'progress': (stats['success_rate'] / 95) * 100
            })
        
        return achievements
    
    def _get_optimization_suggestions(self):
        """Get personalized optimization suggestions"""
        stats = self._get_personal_statistics()
        suggestions = []
        
        if stats['success_rate'] < 85:
            suggestions.append({
                'icon': '🎯',
                'title': 'Improve Test Reliability',
                'description': 'Your success rate could be improved. Consider reviewing failed scenarios and updating test steps for better reliability.',
                'action': 'Review Failed Tests'
            })
        
        if stats['tests_this_week'] < 3:
            suggestions.append({
                'icon': '📅',
                'title': 'Increase Testing Frequency',
                'description': 'Regular testing helps catch issues early. Try to run tests at least 3 times per week for optimal coverage.',
                'action': 'Set Testing Schedule'
            })
        
        suggestions.append({
            'icon': '⚡',
            'title': 'Speed Up Your Tests',
            'description': 'Use the batch execution feature to run multiple scenarios efficiently. This saves time and provides better coverage.',
            'action': 'Try Batch Execution'
        })
        
        suggestions.append({
            'icon': '📊',
            'title': 'Track Your Progress',
            'description': 'Check your personal dashboard regularly to identify patterns and celebrate improvements in your testing journey.',
            'action': 'View Trends'
        })
        
        return suggestions

if __name__ == "__main__":
    print("Personal Analytics Dashboard - Privacy-First Design")
    print("Making every user feel like a testing superhero! 🦸‍♂️")