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

class RiceUI:
    def __init__(self, parent, callbacks):
        self.parent = parent
        self.callbacks = callbacks
        
    def setup_rice_tab_content(self, parent):
        """Setup RICE profiles tab content"""
        
        # Original layout (preserves table formatting)
        rice_frame = tk.Frame(parent, bg='#ffffff', padx=20, pady=20)
        rice_frame.pack(fill="both", expand=True)
        
        # RICE profiles section
        rice_header_frame = tk.Frame(rice_frame, bg='#ffffff')
        rice_header_frame.pack(fill="x", pady=(0, 10))
        
        rice_label = tk.Label(rice_header_frame, text="RICE List", font=('Segoe UI', 12, 'bold'), bg='#ffffff')
        rice_label.pack(side="left")
        
        # Pagination info
        self.rice_page_label = tk.Label(rice_header_frame, text="Page 1 of 1", font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280')
        self.rice_page_label.pack(side="right")
        
        # RICE profiles container
        rice_container = tk.Frame(rice_frame, bg='#ffffff')
        rice_container.pack(fill="x", pady=(0, 5))
        
        # Headers
        headers_frame = tk.Frame(rice_container, bg='#e5e7eb', height=25)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        # Static headers with relative positioning and padding
        rice_id_label = tk.Label(headers_frame, text="RICE ID", font=('Segoe UI', 10, 'bold'), 
                                bg='#e5e7eb', fg='#374151', anchor='w')
        rice_id_label.place(relx=0, y=5, relwidth=0.12)
        rice_id_label.config(padx=18)  # 1/4 inch left padding
        
        name_label = tk.Label(headers_frame, text="Name", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w')
        name_label.place(relx=0.12, y=5, relwidth=0.25)
        name_label.config(padx=18)  # 1/4 inch left padding
        
        type_label = tk.Label(headers_frame, text="Type", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w')
        type_label.place(relx=0.37, y=5, relwidth=0.18)
        type_label.config(padx=18)  # 1/4 inch left padding
        
        channel_label = tk.Label(headers_frame, text="Channel", font=('Segoe UI', 10, 'bold'), 
                                bg='#e5e7eb', fg='#374151', anchor='w')
        channel_label.place(relx=0.55, y=5, relwidth=0.12)
        channel_label.config(padx=18)  # 1/4 inch left padding
        
        sftp_label = tk.Label(headers_frame, text="SFTP", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w')
        sftp_label.place(relx=0.67, y=5, relwidth=0.13)
        sftp_label.config(padx=18)  # 1/4 inch left padding
        
        actions_label = tk.Label(headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                                bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        actions_label.place(relx=0.80, y=5, relwidth=0.2)
        
        # Column separators for RICE headers
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.12, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.37, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.55, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.67, y=2, height=21)
        tk.Frame(headers_frame, bg='#d1d5db', width=1).place(relx=0.80, y=2, height=21)
        
        # Fixed frame for RICE profiles
        self.rice_scroll_frame = tk.Frame(rice_container, bg='#ffffff')
        self.rice_scroll_frame.pack(fill="x")
        
        # Pagination controls
        rice_nav_frame = tk.Frame(rice_frame, bg='#ffffff')
        rice_nav_frame.pack(fill="x", pady=(0, 10))
        
        # Center frame for pagination buttons
        nav_center_frame = tk.Frame(rice_nav_frame, bg='#ffffff')
        nav_center_frame.pack(expand=True)
        
        # Records per page selector (right side)
        rice_per_page_frame = tk.Frame(rice_nav_frame, bg='#ffffff')
        rice_per_page_frame.pack(side="right")
        
        tk.Label(rice_per_page_frame, text="Show:", font=('Segoe UI', 9), 
                 bg='#ffffff', fg='#6b7280').pack(side="left", padx=(0, 5))
        
        self.rice_per_page_var = tk.StringVar(value="5")
        rice_per_page_combo = ttk.Combobox(rice_per_page_frame, textvariable=self.rice_per_page_var,
                                           values=["5", "10", "20", "50", "100"],
                                           width=5, state="readonly", font=('Segoe UI', 9))
        rice_per_page_combo.pack(side="left", padx=(0, 5))
        rice_per_page_combo.bind('<<ComboboxSelected>>', 
                                lambda e: self.callbacks['change_rice_per_page'](int(self.rice_per_page_var.get())))
        
        tk.Label(rice_per_page_frame, text="records", font=('Segoe UI', 9), 
                 bg='#ffffff', fg='#6b7280').pack(side="left")
        
        self.rice_prev_btn = tk.Button(nav_center_frame, text="◀ Prev", font=('Segoe UI', 9), 
                                      bg='#e5e7eb', fg='#374151', relief='flat', padx=10, pady=4, 
                                      cursor='hand2', bd=0, highlightthickness=0, state='disabled',
                                      command=self.callbacks['rice_prev_page'])
        self.rice_prev_btn.pack(side="left", padx=(0, 5))
        
        self.rice_next_btn = tk.Button(nav_center_frame, text="Next ▶", font=('Segoe UI', 9), 
                                      bg='#e5e7eb', fg='#374151', relief='flat', padx=10, pady=4, 
                                      cursor='hand2', bd=0, highlightthickness=0, state='disabled',
                                      command=self.callbacks['rice_next_page'])
        self.rice_next_btn.pack(side="left")
        
        # RICE buttons
        rice_btn_frame = tk.Frame(rice_frame, bg='#ffffff')
        rice_btn_frame.pack(fill="x", pady=(0, 20))
        
        add_rice_btn = ttk.Button(rice_btn_frame, text="➕ Add RICE", style='Primary.TButton',
                                 command=self.callbacks['add_rice_profile'])
        add_rice_btn.pack(side="left", padx=(0, 10))
        add_rice_btn.configure(cursor='hand2')
        
        refresh_rice_btn = ttk.Button(rice_btn_frame, text="Refresh", style='Secondary.TButton',
                                     command=self.callbacks['load_rice_profiles'])
        refresh_rice_btn.pack(side="left")
        refresh_rice_btn.configure(cursor='hand2')
        
        # Scenarios section
        self.scenarios_label = tk.Label(rice_frame, text="Scenarios", font=('Segoe UI', 12, 'bold'), bg='#ffffff')
        self.scenarios_label.pack(anchor="w", pady=(10, 5))
        
        # Generate TES-070 button (between title and table)
        tes_btn_frame = tk.Frame(rice_frame, bg='#ffffff')
        tes_btn_frame.pack(fill="x", pady=(0, 5))
        
        generate_tes_btn = tk.Button(tes_btn_frame, text="📋 Generate TES-070", 
                                    font=('Segoe UI', 10, 'bold'), bg='#3b82f6', fg='#ffffff',
                                    relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                                    command=self.callbacks['generate_tes_070'])
        generate_tes_btn.pack(side="left", padx=(0, 5))
        generate_tes_btn.configure(cursor='hand2')
        
        history_tes_btn = tk.Button(tes_btn_frame, text="📚 TES-070 History", 
                                   font=('Segoe UI', 10, 'bold'), bg='#6366f1', fg='#ffffff',
                                   relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                                   command=self.callbacks['show_tes070_history'])
        history_tes_btn.pack(side="left")
        history_tes_btn.configure(cursor='hand2')
        
        # Scenarios container with pagination
        scenarios_container = tk.Frame(rice_frame, bg='#ffffff')
        scenarios_container.pack(fill="both", expand=True, pady=(0, 10))
        
        # Scenarios header with pagination info
        scenarios_header_frame = tk.Frame(scenarios_container, bg='#ffffff')
        scenarios_header_frame.pack(fill="x", pady=(0, 5))
        
        # Pagination info for scenarios
        self.scenarios_page_label = tk.Label(scenarios_header_frame, text="Page 1 of 1", font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280')
        self.scenarios_page_label.pack(side="right")
        
        # Scenario headers
        scenario_headers_frame = tk.Frame(scenarios_container, bg='#e5e7eb', height=25)
        scenario_headers_frame.pack(fill="x")
        scenario_headers_frame.pack_propagate(False)
        
        scenario_label = tk.Label(scenario_headers_frame, text="Scenario", font=('Segoe UI', 10, 'bold'), 
                                 bg='#e5e7eb', fg='#374151', anchor='w')
        scenario_label.place(x=10, y=5, width=100)
        scenario_label.config(padx=18)  # 1/4 inch left padding
        
        desc_label = tk.Label(scenario_headers_frame, text="Description", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w')
        desc_label.place(x=120, y=5, relwidth=0.4)
        desc_label.config(padx=18)  # 1/4 inch left padding
        
        result_label = tk.Label(scenario_headers_frame, text="Result", font=('Segoe UI', 10, 'bold'), 
                               bg='#e5e7eb', fg='#374151', anchor='w')
        result_label.place(relx=0.45, y=5, relwidth=0.08)
        result_label.config(padx=18)  # 1/4 inch left padding
        
        steps_label = tk.Label(scenario_headers_frame, text="Steps", font=('Segoe UI', 10, 'bold'), 
                              bg='#e5e7eb', fg='#374151', anchor='w')
        steps_label.place(relx=0.53, y=5, relwidth=0.07)
        steps_label.config(padx=18)  # 1/4 inch left padding
        
        file_label = tk.Label(scenario_headers_frame, text="File", font=('Segoe UI', 10, 'bold'), 
                             bg='#e5e7eb', fg='#374151', anchor='w')
        file_label.place(relx=0.60, y=5, relwidth=0.09)
        file_label.config(padx=18)  # 1/4 inch left padding
        
        screenshot_label = tk.Label(scenario_headers_frame, text="Screenshot", font=('Segoe UI', 10, 'bold'), 
                                   bg='#e5e7eb', fg='#374151', anchor='w')
        screenshot_label.place(relx=0.69, y=5, relwidth=0.09)
        screenshot_label.config(padx=18)  # 1/4 inch left padding
        
        actions_label = tk.Label(scenario_headers_frame, text="Actions", font=('Segoe UI', 10, 'bold'), 
                                bg='#e5e7eb', fg='#374151', anchor='w', padx=18)
        actions_label.place(relx=0.78, y=5, relwidth=0.22)
        
        # Column separators for scenario headers
        tk.Frame(scenario_headers_frame, bg='#d1d5db', width=1).place(x=115, y=2, height=21)
        tk.Frame(scenario_headers_frame, bg='#d1d5db', width=1).place(relx=0.45, y=2, height=21)
        tk.Frame(scenario_headers_frame, bg='#d1d5db', width=1).place(relx=0.53, y=2, height=21)
        tk.Frame(scenario_headers_frame, bg='#d1d5db', width=1).place(relx=0.60, y=2, height=21)
        tk.Frame(scenario_headers_frame, bg='#d1d5db', width=1).place(relx=0.69, y=2, height=21)
        tk.Frame(scenario_headers_frame, bg='#d1d5db', width=1).place(relx=0.78, y=2, height=21)
        
        # Fixed frame for scenarios
        self.scenarios_scroll_frame = tk.Frame(scenarios_container, bg='#ffffff')
        self.scenarios_scroll_frame.pack(fill="x")
        
        # Scenarios pagination controls
        scenarios_nav_frame = tk.Frame(scenarios_container, bg='#ffffff')
        scenarios_nav_frame.pack(fill="x", pady=(5, 0))
        
        # Center frame for pagination buttons
        scenarios_nav_center_frame = tk.Frame(scenarios_nav_frame, bg='#ffffff')
        scenarios_nav_center_frame.pack(expand=True)
        
        # Records per page selector for scenarios (right side)
        scenarios_per_page_frame = tk.Frame(scenarios_nav_frame, bg='#ffffff')
        scenarios_per_page_frame.pack(side="right")
        
        tk.Label(scenarios_per_page_frame, text="Show:", font=('Segoe UI', 9), 
                 bg='#ffffff', fg='#6b7280').pack(side="left", padx=(0, 5))
        
        self.scenarios_per_page_var = tk.StringVar(value="5")
        scenarios_per_page_combo = ttk.Combobox(scenarios_per_page_frame, textvariable=self.scenarios_per_page_var,
                                               values=["5", "10", "20", "50", "100"],
                                               width=5, state="readonly", font=('Segoe UI', 9))
        scenarios_per_page_combo.pack(side="left", padx=(0, 5))
        scenarios_per_page_combo.bind('<<ComboboxSelected>>', 
                                     lambda e: self.callbacks['change_scenarios_per_page'](int(self.scenarios_per_page_var.get())))
        
        tk.Label(scenarios_per_page_frame, text="records", font=('Segoe UI', 9), 
                 bg='#ffffff', fg='#6b7280').pack(side="left")
        
        self.scenarios_prev_btn = tk.Button(scenarios_nav_center_frame, text="◀ Prev", font=('Segoe UI', 9), 
                                          bg='#e5e7eb', fg='#374151', relief='flat', padx=10, pady=4, 
                                          cursor='hand2', bd=0, highlightthickness=0, state='disabled',
                                          command=self.callbacks['scenarios_prev_page'])
        self.scenarios_prev_btn.pack(side="left", padx=(0, 5))
        
        self.scenarios_next_btn = tk.Button(scenarios_nav_center_frame, text="Next ▶", font=('Segoe UI', 9), 
                                          bg='#e5e7eb', fg='#374151', relief='flat', padx=10, pady=4, 
                                          cursor='hand2', bd=0, highlightthickness=0, state='disabled',
                                          command=self.callbacks['scenarios_next_page'])
        self.scenarios_next_btn.pack(side="left")
        
        # Scenario buttons
        scenario_btn_frame = tk.Frame(rice_frame, bg='#ffffff')
        scenario_btn_frame.pack(fill="x")
        
        add_scenario_btn = ttk.Button(scenario_btn_frame, text="➕ Add Scenario", style='Primary.TButton',
                                     command=self.callbacks['add_scenario'])
        add_scenario_btn.pack(side="left", padx=(0, 10))
        add_scenario_btn.configure(cursor='hand2')
        

        run_all_btn = ttk.Button(scenario_btn_frame, text="Run All Scenarios", style='Success.TButton',
                                command=self.callbacks['run_all_scenarios'])
        run_all_btn.pack(side="left")
        run_all_btn.configure(cursor='hand2')
