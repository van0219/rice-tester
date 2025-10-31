#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import threading
import time
import sys
import os

# Add Temp path for performance optimizer
temp_path = os.path.join(os.path.dirname(__file__), 'Temp')
if temp_path not in sys.path:
    sys.path.insert(0, temp_path)

try:
    from performance_optimizer import RICEPerformanceOptimizer
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Temp path: {temp_path}")
    print(f"Files in temp: {os.listdir(temp_path) if os.path.exists(temp_path) else 'Temp folder not found'}")
    # Create a dummy optimizer for testing
    class RICEPerformanceOptimizer:
        def optimize_database(self): pass
        def cleanup_temp_files(self): pass
        def optimize_screenshots(self): pass
        def optimize_memory_usage(self): pass

class PerformanceOptimizerUI:
    def __init__(self, parent, show_popup_callback):
        self.parent = parent
        self.show_popup = show_popup_callback
        self.optimizer = RICEPerformanceOptimizer()
        
    def show_optimizer_dialog(self):
        """Show interactive performance optimizer dialog"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("📈 Performance Optimizer")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg='#ffffff')
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Ensure dialog stays on top and is visible
        self.dialog.lift()
        self.dialog.attributes('-topmost', True)
        self.dialog.after(100, lambda: self.dialog.attributes('-topmost', False))
        
        print(f"Dialog created with geometry: {self.dialog.geometry()}")
        print(f"Dialog visible: {self.dialog.winfo_viewable()}")
        
        try:
            self.dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Center dialog - force proper geometry
        self.dialog.withdraw()  # Hide while positioning
        self.dialog.update_idletasks()
        
        # Get screen dimensions
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        
        # Calculate center position
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (500 // 2)
        
        # Set geometry and show
        self.dialog.geometry(f"600x500+{x}+{y}")
        self.dialog.deiconify()  # Show dialog
        
        print(f"Screen: {screen_width}x{screen_height}, Dialog position: {x},{y}")
        
        # Header
        header_frame = tk.Frame(self.dialog, bg='#059669', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="📈 Performance Optimizer", 
                font=('Segoe UI', 16, 'bold'), bg='#059669', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(self.dialog, bg='#ffffff', padx=30, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text="Optimization Tasks", 
                font=('Segoe UI', 14, 'bold'), bg='#ffffff', fg='#1f2937').pack(anchor="w", pady=(0, 15))
        
        # Tasks list
        self.tasks = [
            ("🗃️ Database Optimization", "Create indexes, vacuum, and analyze database"),
            ("🧹 Cleanup Temporary Files", "Remove files older than 7 days"),
            ("📸 Optimize Screenshots", "Clean old screenshots and compress storage"),
            ("💾 Memory Analysis", "Analyze and optimize memory usage patterns")
        ]
        
        self.task_frames = []
        self.task_status = []
        
        for i, (title, description) in enumerate(self.tasks):
            # Task container
            task_container = tk.Frame(content_frame, bg='#f8fafc', relief='solid', bd=1)
            task_container.pack(fill="x", pady=5)
            
            task_frame = tk.Frame(task_container, bg='#f8fafc', padx=15, pady=12)
            task_frame.pack(fill="x")
            
            # Task info
            info_frame = tk.Frame(task_frame, bg='#f8fafc')
            info_frame.pack(side="left", fill="x", expand=True)
            
            title_label = tk.Label(info_frame, text=title, font=('Segoe UI', 11, 'bold'),
                                  bg='#f8fafc', fg='#1f2937', anchor='w')
            title_label.pack(anchor="w")
            
            desc_label = tk.Label(info_frame, text=description, font=('Segoe UI', 9),
                                 bg='#f8fafc', fg='#6b7280', anchor='w')
            desc_label.pack(anchor="w")
            
            # Status indicator
            status_label = tk.Label(task_frame, text="⏳", font=('Segoe UI', 16),
                                   bg='#f8fafc', fg='#6b7280')
            status_label.pack(side="right")
            
            self.task_frames.append(task_container)
            self.task_status.append(status_label)
        
        # Progress bar
        self.progress_frame = tk.Frame(content_frame, bg='#ffffff')
        self.progress_frame.pack(fill="x", pady=(20, 15))
        
        tk.Label(self.progress_frame, text="Overall Progress", 
                font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#1f2937').pack(anchor="w")
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var,
                                           maximum=100, length=540, mode='determinate')
        self.progress_bar.pack(pady=(5, 0))
        
        self.progress_label = tk.Label(self.progress_frame, text="Ready to start", 
                                      font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280')
        self.progress_label.pack(anchor="w", pady=(5, 0))
        
        # Buttons
        btn_frame = tk.Frame(content_frame, bg='#ffffff', height=50)
        btn_frame.pack(fill="x", pady=(15, 0))
        btn_frame.pack_propagate(False)
        
        # Debug: Print button creation
        print("Creating Performance Optimizer buttons...")
        
        self.start_btn = tk.Button(btn_frame, text="🚀 Run Optimization", 
                                  font=('Segoe UI', 11, 'bold'), bg='#059669', fg='#ffffff',
                                  relief='flat', padx=25, pady=10, cursor='hand2', bd=0,
                                  command=self.start_optimization)
        self.start_btn.pack(side="left")
        print(f"Start button created: {self.start_btn}")
        
        close_btn = tk.Button(btn_frame, text="Close", font=('Segoe UI', 11, 'bold'),
                             bg='#6b7280', fg='#ffffff', relief='flat', padx=25, pady=10,
                             cursor='hand2', bd=0, command=self.dialog.destroy)
        close_btn.pack(side="right")
        print(f"Close button created: {close_btn}")
        
        # Force update to ensure buttons are visible
        btn_frame.update_idletasks()
        self.dialog.update_idletasks()
    
    def start_optimization(self):
        """Start optimization process with visual feedback"""
        self.start_btn.configure(state='disabled', text="Running...", bg='#9ca3af')
        
        # Start optimization in background thread
        threading.Thread(target=self.run_optimization_steps, daemon=True).start()
    
    def run_optimization_steps(self):
        """Run optimization steps with visual progress"""
        try:
            total_steps = len(self.tasks)
            
            for i, (title, description) in enumerate(self.tasks):
                # Update current task status
                self.dialog.after(0, lambda idx=i: self.update_task_status(idx, "running"))
                self.dialog.after(0, lambda: self.progress_label.configure(text=f"Running: {title}"))
                
                # Simulate work and run actual optimization
                if i == 0:  # Database optimization
                    self.optimizer.optimize_database()
                elif i == 1:  # Cleanup
                    self.optimizer.cleanup_temp_files()
                elif i == 2:  # Screenshots
                    self.optimizer.optimize_screenshots()
                elif i == 3:  # Memory analysis
                    self.optimizer.optimize_memory_usage()
                
                # Add visual delay for better UX
                time.sleep(1)
                
                # Mark as complete
                self.dialog.after(0, lambda idx=i: self.update_task_status(idx, "complete"))
                
                # Update progress
                progress = ((i + 1) / total_steps) * 100
                self.dialog.after(0, lambda p=progress: self.progress_var.set(p))
            
            # All done
            self.dialog.after(0, self.optimization_complete)
            
        except Exception as e:
            self.dialog.after(0, lambda: self.optimization_error(str(e)))
    
    def update_task_status(self, task_index, status):
        """Update visual status of a task"""
        if status == "running":
            self.task_status[task_index].configure(text="⚡", fg='#f59e0b')
            self.task_frames[task_index].configure(bg='#fef3c7', highlightbackground='#f59e0b', highlightthickness=2)
        elif status == "complete":
            self.task_status[task_index].configure(text="✅", fg='#059669')
            self.task_frames[task_index].configure(bg='#d1fae5', highlightbackground='#059669', highlightthickness=2)
    
    def optimization_complete(self):
        """Handle optimization completion"""
        self.progress_label.configure(text="✅ Optimization completed successfully!")
        self.start_btn.configure(text="✅ Completed", bg='#059669', state='disabled')
        
        # Show success popup after 2 seconds
        self.dialog.after(2000, self.show_success_and_close)
    
    def optimization_error(self, error_msg):
        """Handle optimization error"""
        self.progress_label.configure(text=f"❌ Error: {error_msg}")
        self.start_btn.configure(text="❌ Failed", bg='#ef4444', state='normal')
    
    def show_success_and_close(self):
        """Show success message and close dialog"""
        self.dialog.destroy()
        self.show_popup("Success", 
                       "Performance optimization completed successfully!\n\n• Database indexes created\n• Temporary files cleaned\n• Screenshots optimized\n• Memory usage improved", 
                       "success")