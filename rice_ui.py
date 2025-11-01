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
        
        # Perfect RICE table columns (balanced proportions)
        self.RICE_COLUMNS = {
            'rice_id': {'start': 0.0, 'width': 0.10, 'title': 'RICE ID'},
            'name': {'start': 0.10, 'width': 0.35, 'title': 'Name'},
            'type': {'start': 0.45, 'width': 0.15, 'title': 'Type'},
            'channel': {'start': 0.60, 'width': 0.15, 'title': 'Channel'},
            'sftp': {'start': 0.75, 'width': 0.10, 'title': 'SFTP'},
            'actions': {'start': 0.85, 'width': 0.15, 'title': 'Actions'}
        }
        
        # Perfect Scenarios table columns (balanced proportions)
        self.SCENARIOS_COLUMNS = {
            'scenario': {'start': 0.0, 'width': 0.10, 'title': 'Scenario'},
            'description': {'start': 0.10, 'width': 0.35, 'title': 'Description'},
            'result': {'start': 0.45, 'width': 0.10, 'title': 'Result'},
            'steps': {'start': 0.55, 'width': 0.10, 'title': 'Steps'},
            'file': {'start': 0.65, 'width': 0.10, 'title': 'File'},
            'screenshot': {'start': 0.75, 'width': 0.10, 'title': 'Screenshot'},
            'actions': {'start': 0.85, 'width': 0.15, 'title': 'Actions'}
        }
        
    def setup_rice_tab_content(self, parent):
        """Setup RICE profiles tab content"""
        
        # Main container with light background (matching SFTP)
        self.main_container = tk.Frame(parent, bg='#f8fafc')
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Modern card container (matching SFTP)
        self.card_frame = tk.Frame(self.main_container, bg='#ffffff', relief='solid', bd=1,
                                  highlightbackground='#e5e7eb', highlightthickness=1)
        self.card_frame.pack(fill="both", expand=True)
        
        # RICE profiles section - Primary card
        rice_card = tk.Frame(self.card_frame, bg='#ffffff')
        rice_card.pack(fill="x", pady=(0, 20), padx=20)
        
        rice_frame = tk.Frame(rice_card, bg='#ffffff', padx=20, pady=15)
        rice_frame.pack(fill="x")
        
        # Pagination info removed - using scroll approach
        
        # RICE List header with buttons
        rice_header_main = tk.Frame(rice_frame, bg='#ffffff')
        rice_header_main.pack(fill="x", pady=(0, 10))
        
        rice_list_label = tk.Label(rice_header_main, text="📋 RICE Items", font=('Segoe UI', 14, 'bold'), bg='#ffffff', fg='#1f2937')
        rice_list_label.pack(side="left")
        
        # Compact buttons in header
        header_btn_frame = tk.Frame(rice_header_main, bg='#ffffff')
        header_btn_frame.pack(side="right")
        
        add_rice_btn = tk.Button(header_btn_frame, text="＋ Add", font=('Segoe UI', 9), 
                                bg='#10b981', fg='#ffffff', relief='flat', padx=12, pady=6, 
                                cursor='hand2', bd=0, highlightthickness=0,
                                command=self.callbacks['add_rice_profile'])
        add_rice_btn.pack(side="left", padx=(0, 5))
        
        refresh_rice_btn = tk.Button(header_btn_frame, text="⟲ Refresh", font=('Segoe UI', 9), 
                                    bg='#6b7280', fg='#ffffff', relief='flat', padx=12, pady=6, 
                                    cursor='hand2', bd=0, highlightthickness=0,
                                    command=self.callbacks['load_rice_profiles'])
        refresh_rice_btn.pack(side="left")
        
        # Compact search and filter row
        search_frame = tk.Frame(rice_frame, bg='#ffffff')
        search_frame.pack(fill="x", pady=(0, 10))
        
        # Search box with clear button
        search_input_frame = tk.Frame(search_frame, bg='#ffffff')
        search_input_frame.pack(side="left", padx=(0, 15))
        
        tk.Label(search_input_frame, text="🔍", font=('Segoe UI', 12), bg='#ffffff', fg='#6b7280').pack(side="left", padx=(0, 5))
        
        self.rice_search_var = tk.StringVar()
        self.rice_search_entry = tk.Entry(search_input_frame, textvariable=self.rice_search_var, font=('Segoe UI', 10),
                                         bg='#f9fafb', relief='solid', bd=1, width=25)
        self.rice_search_entry.pack(side="left")
        self.rice_search_entry.insert(0, "Search RICE items...")
        self.rice_search_entry.config(fg='#9ca3af')
        self.rice_search_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.rice_search_entry.bind('<FocusOut>', self._on_search_focus_out)
        self.rice_search_entry.bind('<Button-1>', self._on_search_click)
        self.rice_search_entry.bind('<KeyRelease>', self._on_search_change)
        
        # Clear search button
        self.clear_search_btn = tk.Button(search_input_frame, text="✕", font=('Segoe UI', 8), 
                                         bg='#ef4444', fg='#ffffff', relief='flat', padx=4, pady=2, 
                                         cursor='hand2', bd=0, highlightthickness=0,
                                         command=self._clear_search)
        self.clear_search_btn.pack(side="left", padx=(2, 0))
        
        # Search results count
        self.search_results_label = tk.Label(search_frame, text="", font=('Segoe UI', 9), 
                                            bg='#ffffff', fg='#6b7280')
        self.search_results_label.pack(side="left", padx=(10, 0))
        
        # Loading indicator (initially hidden)
        self.loading_label = tk.Label(search_frame, text="⏳ Loading...", font=('Segoe UI', 9), 
                                     bg='#ffffff', fg='#3b82f6')
        # Don't pack initially - will be shown/hidden as needed
        
        # Type filter next to search
        tk.Label(search_frame, text="Type:", font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(side="left", padx=(0, 5))
        self.rice_type_filter_var = tk.StringVar(value="All")
        self.rice_type_filter = ttk.Combobox(search_frame, textvariable=self.rice_type_filter_var,
                                           width=20, font=('Segoe UI', 9), state='readonly')
        self.rice_type_filter['values'] = ["All"]
        self.rice_type_filter.pack(side="left")
        self.rice_type_filter.bind('<<ComboboxSelected>>', self._on_filter_change)
        
        # RICE profiles container with modern styling
        rice_container = tk.Frame(rice_frame, bg='#ffffff', relief='solid', bd=1)
        rice_container.pack(fill="x", pady=(0, 5))
        
        # Modern table headers with SFTP styling
        headers_frame = tk.Frame(rice_container, bg='#f3f4f6', height=35, relief='solid', bd=1)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        # Header labels with icons and better spacing
        tk.Label(headers_frame, text="🆔 RICE ID", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0, y=8, relwidth=0.10)
        
        tk.Label(headers_frame, text="📝 Name", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.10, y=8, relwidth=0.35)
        
        tk.Label(headers_frame, text="🏷️ Type", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.45, y=8, relwidth=0.15)
        
        tk.Label(headers_frame, text="📡 Channel", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.60, y=8, relwidth=0.15)
        
        tk.Label(headers_frame, text="📁 SFTP", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.75, y=8, relwidth=0.10)
        
        tk.Label(headers_frame, text="⚙️ Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='center', padx=10).place(relx=0.85, y=8, relwidth=0.15)
        
        # Column separators
        tk.Frame(headers_frame, bg='#9ca3af', width=1).place(relx=0.10, y=4, height=27)
        tk.Frame(headers_frame, bg='#9ca3af', width=1).place(relx=0.45, y=4, height=27)
        tk.Frame(headers_frame, bg='#9ca3af', width=1).place(relx=0.60, y=4, height=27)
        tk.Frame(headers_frame, bg='#9ca3af', width=1).place(relx=0.75, y=4, height=27)
        tk.Frame(headers_frame, bg='#9ca3af', width=1).place(relx=0.85, y=4, height=27)
        
        # Responsive scrollable frame for RICE profiles
        rice_scroll_container = tk.Frame(rice_container, bg='#ffffff')
        rice_scroll_container.pack(fill="x", padx=1, pady=(0, 1))
        
        # Canvas and scrollbar for RICE profiles with initial height
        self.rice_canvas = tk.Canvas(rice_scroll_container, bg='#ffffff', highlightthickness=0, height=200)
        rice_scrollbar = ttk.Scrollbar(rice_scroll_container, orient="vertical", command=self.rice_canvas.yview)
        self.rice_scroll_frame = tk.Frame(self.rice_canvas, bg='#ffffff')
        
        # Configure scrolling
        def _configure_scroll_region(event):
            # Update scroll region when frame content changes
            self.rice_canvas.configure(scrollregion=self.rice_canvas.bbox("all"))
        
        def _configure_canvas(event):
            # Update canvas window width when canvas is resized
            canvas_width = event.width
            self.rice_canvas.itemconfig(self.rice_canvas_window, width=canvas_width)
        
        self.rice_scroll_frame.bind('<Configure>', _configure_scroll_region)
        self.rice_canvas.bind('<Configure>', _configure_canvas)
        self.rice_canvas_window = self.rice_canvas.create_window((0, 0), window=self.rice_scroll_frame, anchor="nw")
        self.rice_canvas.configure(yscrollcommand=rice_scrollbar.set)
        
        # Force initial canvas width update
        def _update_canvas_width():
            canvas_width = self.rice_canvas.winfo_width()
            if canvas_width > 1:  # Only update if canvas has been rendered
                self.rice_canvas.itemconfig(self.rice_canvas_window, width=canvas_width)
        
        # Schedule width update after canvas is rendered
        self.rice_canvas.after_idle(_update_canvas_width)
        
        # Pack canvas and scrollbar
        self.rice_canvas.pack(side="left", fill="both", expand=True)
        rice_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas and frame
        def _on_rice_mousewheel(event):
            self.rice_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.rice_canvas.bind("<MouseWheel>", _on_rice_mousewheel)
        self.rice_scroll_frame.bind("<MouseWheel>", _on_rice_mousewheel)
        
        # Store canvas for later height adjustment
        self.rice_scroll_container = rice_scroll_container
        
        # Pagination controls removed - using scrollbar approach
        
        # Buttons moved to header - this section removed to save vertical space
        
        # Scenarios section - Secondary card within main card
        scenarios_card = tk.Frame(self.card_frame, bg='#ffffff')
        scenarios_card.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scenarios_frame = tk.Frame(scenarios_card, bg='#ffffff', padx=20, pady=15)
        scenarios_frame.pack(fill="both", expand=True)
        
        # Scenarios header with all buttons
        scenarios_header_main = tk.Frame(scenarios_frame, bg='#ffffff')
        scenarios_header_main.pack(fill="x", pady=(0, 15))
        
        self.scenarios_label = tk.Label(scenarios_header_main, text="🎯 Test Scenarios", font=('Segoe UI', 14, 'bold'), bg='#ffffff', fg='#1f2937')
        self.scenarios_label.pack(side="left")
        
        # All buttons in header - following IT standards for compact UI
        header_btn_frame = tk.Frame(scenarios_header_main, bg='#ffffff')
        header_btn_frame.pack(side="right")
        
        # TES-070 buttons (document actions)
        generate_tes_btn = tk.Button(header_btn_frame, text="◉ Generate TES-070", 
                                    font=('Segoe UI', 9), bg='#3b82f6', fg='#ffffff',
                                    relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                                    command=self.callbacks['generate_tes_070'])
        generate_tes_btn.pack(side="left", padx=(0, 3))
        
        history_tes_btn = tk.Button(header_btn_frame, text="⧉ History", 
                                   font=('Segoe UI', 9), bg='#6366f1', fg='#ffffff',
                                   relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                                   command=self.callbacks['show_tes070_history'])
        history_tes_btn.pack(side="left", padx=(0, 8))
        
        # Scenario action buttons
        add_scenario_btn = tk.Button(header_btn_frame, text="＋ Add", 
                                    font=('Segoe UI', 9), bg='#10b981', fg='#ffffff',
                                    relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                                    command=self.callbacks['add_scenario'])
        add_scenario_btn.pack(side="left", padx=(0, 3))
        
        run_all_btn = tk.Button(header_btn_frame, text="▷ Run All", 
                               font=('Segoe UI', 9), bg='#3b82f6', fg='#ffffff',
                               relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                               command=self.callbacks['run_all_scenarios'])
        run_all_btn.pack(side="left")
        
        # Scenarios container with modern styling
        scenarios_container = tk.Frame(scenarios_frame, bg='#ffffff', relief='solid', bd=1)
        scenarios_container.pack(fill="both", expand=True)
        
        # Scenarios header - pagination info removed
        scenarios_header_frame = tk.Frame(scenarios_container, bg='#ffffff')
        scenarios_header_frame.pack(fill="x", pady=(0, 5))
        
        # Modern scenario headers with SFTP styling
        scenario_headers_frame = tk.Frame(scenarios_container, bg='#f3f4f6', height=35, relief='solid', bd=1)
        scenario_headers_frame.pack(fill="x")
        scenario_headers_frame.pack_propagate(False)
        
        # Header labels with icons and better spacing
        tk.Label(scenario_headers_frame, text="#️⃣ Scenario", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0, y=8, relwidth=0.10)
        
        tk.Label(scenario_headers_frame, text="📝 Description", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.10, y=8, relwidth=0.35)
        
        tk.Label(scenario_headers_frame, text="✅ Result", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.45, y=8, relwidth=0.10)
        
        tk.Label(scenario_headers_frame, text="📋 Steps", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.55, y=8, relwidth=0.10)
        
        tk.Label(scenario_headers_frame, text="📁 File", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.65, y=8, relwidth=0.10)
        
        tk.Label(scenario_headers_frame, text="📷 Screenshot", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='w').place(relx=0.75, y=8, relwidth=0.10)
        
        tk.Label(scenario_headers_frame, text="⚙️ Actions", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6', fg='#374151', anchor='center', padx=10).place(relx=0.85, y=8, relwidth=0.15)
        
        # Column separators
        tk.Frame(scenario_headers_frame, bg='#9ca3af', width=1).place(relx=0.10, y=4, height=27)
        tk.Frame(scenario_headers_frame, bg='#9ca3af', width=1).place(relx=0.45, y=4, height=27)
        tk.Frame(scenario_headers_frame, bg='#9ca3af', width=1).place(relx=0.55, y=4, height=27)
        tk.Frame(scenario_headers_frame, bg='#9ca3af', width=1).place(relx=0.65, y=4, height=27)
        tk.Frame(scenario_headers_frame, bg='#9ca3af', width=1).place(relx=0.75, y=4, height=27)
        tk.Frame(scenario_headers_frame, bg='#9ca3af', width=1).place(relx=0.85, y=4, height=27)
        
        # Responsive scrollable frame for scenarios
        scenarios_scroll_container = tk.Frame(scenarios_container, bg='#ffffff')
        scenarios_scroll_container.pack(fill="both", expand=True, padx=1, pady=(0, 1))
        
        # Canvas and scrollbar for scenarios
        self.scenarios_canvas = tk.Canvas(scenarios_scroll_container, bg='#ffffff', highlightthickness=0, height=150)
        scenarios_scrollbar = ttk.Scrollbar(scenarios_scroll_container, orient="vertical", command=self.scenarios_canvas.yview)
        self.scenarios_scroll_frame = tk.Frame(self.scenarios_canvas, bg='#ffffff')
        
        # Configure scrolling
        def _configure_scenarios_scroll(event):
            self.scenarios_canvas.configure(scrollregion=self.scenarios_canvas.bbox("all"))
        
        def _configure_scenarios_canvas(event):
            canvas_width = event.width
            self.scenarios_canvas.itemconfig(self.scenarios_canvas_window, width=canvas_width)
        
        self.scenarios_scroll_frame.bind('<Configure>', _configure_scenarios_scroll)
        self.scenarios_canvas.bind('<Configure>', _configure_scenarios_canvas)
        self.scenarios_canvas_window = self.scenarios_canvas.create_window((0, 0), window=self.scenarios_scroll_frame, anchor="nw")
        self.scenarios_canvas.configure(yscrollcommand=scenarios_scrollbar.set)
        
        # Pack canvas and scrollbar
        self.scenarios_canvas.pack(side="left", fill="both", expand=True)
        scenarios_scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scenarios canvas and frame
        def _on_scenarios_mousewheel(event):
            self.scenarios_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.scenarios_canvas.bind("<MouseWheel>", _on_scenarios_mousewheel)
        self.scenarios_scroll_frame.bind("<MouseWheel>", _on_scenarios_mousewheel)
        
        # Pagination controls removed - using scrollbar approach
        
        # Buttons moved to header - this section removed to save vertical space
    
    def _on_search_focus_in(self, event):
        """Handle search box focus in"""
        if self.rice_search_entry.get() == "Search RICE items...":
            self.rice_search_entry.delete(0, tk.END)
            self.rice_search_entry.config(fg='#374151')
    
    def _on_search_click(self, event):
        """Handle search box click - clear placeholder immediately"""
        if self.rice_search_entry.get() == "Search RICE items...":
            self.rice_search_entry.delete(0, tk.END)
            self.rice_search_entry.config(fg='#374151')
    
    def _on_search_focus_out(self, event):
        """Handle search box focus out"""
        if not self.rice_search_entry.get().strip():
            self.rice_search_entry.delete(0, tk.END)
            self.rice_search_entry.insert(0, "Search RICE items...")
            self.rice_search_entry.config(fg='#9ca3af')
    
    def _on_search_change(self, event):
        """Handle search text change"""
        if hasattr(self, 'callbacks') and 'load_rice_profiles' in self.callbacks:
            self.callbacks['load_rice_profiles']()
    
    def _on_filter_change(self, event):
        """Handle filter dropdown change"""
        if hasattr(self, 'callbacks') and 'load_rice_profiles' in self.callbacks:
            self.callbacks['load_rice_profiles']()
    
    def _clear_search(self):
        """Clear search box and refresh results"""
        self.rice_search_entry.delete(0, tk.END)
        self.rice_search_entry.insert(0, "Search RICE items...")
        self.rice_search_entry.config(fg='#9ca3af')
        if hasattr(self, 'callbacks') and 'load_rice_profiles' in self.callbacks:
            self.callbacks['load_rice_profiles']()
    
    def show_loading(self):
        """Show loading indicator"""
        if hasattr(self, 'loading_label'):
            self.search_results_label.pack_forget()
            self.loading_label.pack(side="left", padx=(10, 0))
    
    def hide_loading(self):
        """Hide loading indicator"""
        if hasattr(self, 'loading_label'):
            self.loading_label.pack_forget()
            self.search_results_label.pack(side="left", padx=(10, 0))
    
    def update_search_results_count(self, count, total):
        """Update search results count display"""
        if hasattr(self, 'search_results_label'):
            if count == total:
                self.search_results_label.config(text=f"Showing all {total} items")
            else:
                self.search_results_label.config(text=f"Showing {count} of {total} items")
    
    def _update_filter_options(self):
        """Update filter dropdown options"""
        # This will be called from rice_data_core.py
        pass
    
    def adjust_rice_canvas_height(self, content_height):
        """Dynamically adjust RICE canvas height based on content and available window space"""
        if hasattr(self, 'rice_canvas'):
            try:
                # Get the main application window
                root = self.rice_canvas.winfo_toplevel()
                root.update_idletasks()  # Ensure window is properly rendered
                
                # Get available window height (excluding title bar, etc.)
                window_height = root.winfo_height()
                
                # Account for UI elements that take up space:
                # - Main app header: ~80px
                # - Search section: ~50px
                # - Table headers: ~30px
                # - Padding and margins: ~40px
                # - Scenarios section minimum: ~200px (to keep it visible)
                reserved_space = 80 + 50 + 30 + 40 + 200  # ~400px (110px more space gained)
                
                # Calculate available space for RICE list
                available_height = window_height - reserved_space
                
                # Use 50% of available space as maximum (equal split with scenarios)
                max_rice_height = max(150, int(available_height * 0.5))
                
                # Calculate optimal height: content height or max height, whichever is smaller
                # Minimum height of 150px to show at least a few rows
                # Add 20px padding for better appearance
                optimal_height = max(150, min(content_height + 20, max_rice_height))
                
                # Apply the height
                self.rice_canvas.configure(height=optimal_height)
                
                # Debug output
                print(f"DEBUG: Window height: {window_height}px")
                print(f"DEBUG: Available height: {available_height}px")
                print(f"DEBUG: Max RICE height: {max_rice_height}px")
                print(f"DEBUG: Content height: {content_height}px")
                print(f"DEBUG: Optimal height: {optimal_height}px")
                
                # Force update of canvas width and scroll region
                def _final_update():
                    canvas_width = self.rice_canvas.winfo_width()
                    if canvas_width > 1:
                        self.rice_canvas.itemconfig(self.rice_canvas_window, width=canvas_width)
                    self.rice_canvas.configure(scrollregion=self.rice_canvas.bbox("all"))
                
                self.rice_canvas.after_idle(_final_update)
                
            except Exception as e:
                print(f"DEBUG: Height calculation error: {e}")
                # Fallback to reasonable default if calculation fails
                self.rice_canvas.configure(height=300)
                # Still try to update canvas width
                try:
                    canvas_width = self.rice_canvas.winfo_width()
                    if canvas_width > 1:
                        self.rice_canvas.itemconfig(self.rice_canvas_window, width=canvas_width)
                except:
                    pass
    
    def adjust_scenarios_canvas_height(self, content_height):
        """Dynamically adjust scenarios canvas height"""
        if hasattr(self, 'scenarios_canvas'):
            try:
                root = self.scenarios_canvas.winfo_toplevel()
                window_height = root.winfo_height()
                available_height = window_height - 400  # Updated reserved space calculation
                max_scenarios_height = max(150, int(available_height * 0.5))  # 50% for scenarios
                optimal_height = max(150, min(content_height + 20, max_scenarios_height))
                self.scenarios_canvas.configure(height=optimal_height)
                
                def _final_scenarios_update():
                    canvas_width = self.scenarios_canvas.winfo_width()
                    if canvas_width > 1:
                        self.scenarios_canvas.itemconfig(self.scenarios_canvas_window, width=canvas_width)
                    self.scenarios_canvas.configure(scrollregion=self.scenarios_canvas.bbox("all"))
                
                self.scenarios_canvas.after_idle(_final_scenarios_update)
            except:
                self.scenarios_canvas.configure(height=200)
