#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from enhanced_table_system import RiceTable, ScenariosTable

def demo_enhanced_tables():
    """Demo the enhanced table system"""
    
    # Create main window
    root = tk.Tk()
    root.title("Enhanced Table Demo - RICE Tester")
    root.geometry("1200x800")
    root.configure(bg='#f8fafc')
    
    try:
        root.iconbitmap("infor_logo.ico")
    except:
        pass
    
    # Main container
    main_frame = tk.Frame(root, bg='#f8fafc', padx=20, pady=20)
    main_frame.pack(fill='both', expand=True)
    
    # Title
    title_label = tk.Label(main_frame, text="🚀 Enhanced Table System Demo", 
                          font=('Segoe UI', 16, 'bold'), bg='#f8fafc', fg='#1f2937')
    title_label.pack(pady=(0, 20))
    
    # RICE Table Section
    rice_section = tk.Frame(main_frame, bg='#ffffff', relief='solid', bd=1)
    rice_section.pack(fill='x', pady=(0, 20))
    
    rice_header = tk.Frame(rice_section, bg='#ffffff', padx=15, pady=10)
    rice_header.pack(fill='x')
    
    tk.Label(rice_header, text="📋 RICE Profiles Table", font=('Segoe UI', 14, 'bold'), 
             bg='#ffffff', fg='#1f2937').pack(side='left')
    
    # Create RICE table
    rice_table = RiceTable(rice_section, height=200)
    rice_table.pack(fill='x', padx=15, pady=(0, 15))
    
    # Add sample RICE data
    sample_rice_data = [
        ("RICE001", "Purchase Order Processing", "Client A", "Web", "SFTP_PO", "Inbound", "TENANT1"),
        ("RICE002", "Invoice Validation", "Client B", "API", "SFTP_INV", "Outbound", "TENANT2"),
        ("RICE003", "Payment Processing", "Client A", "Web", "SFTP_PAY", "Inbound", "TENANT1"),
        ("RICE004", "Vendor Management", "Client C", "File", "SFTP_VEN", "Interface", "TENANT3"),
        ("RICE005", "GL Journal Entry", "Client B", "Web", "SFTP_GL", "Inbound", "TENANT2")
    ]
    
    for i, data in enumerate(sample_rice_data):
        rice_table.add_rice_profile(data, i+1)
    
    # Scenarios Table Section
    scenarios_section = tk.Frame(main_frame, bg='#ffffff', relief='solid', bd=1)
    scenarios_section.pack(fill='both', expand=True)
    
    scenarios_header = tk.Frame(scenarios_section, bg='#ffffff', padx=15, pady=10)
    scenarios_header.pack(fill='x')
    
    tk.Label(scenarios_header, text="🎯 Test Scenarios Table", font=('Segoe UI', 14, 'bold'), 
             bg='#ffffff', fg='#1f2937').pack(side='left')
    
    # Create Scenarios table
    scenarios_table = ScenariosTable(scenarios_section, height=250)
    scenarios_table.pack(fill='both', expand=True, padx=15, pady=(0, 15))
    
    # Add sample scenarios data
    sample_scenarios_data = [
        (1, "Login to FSM Portal", "Passed", "/path/to/file1.xlsx", 5),
        (2, "Navigate to Purchase Orders", "Passed", "/path/to/file2.xlsx", 3),
        (3, "Create New Purchase Order", "Failed", None, 8),
        (4, "Validate PO Details", "Not run", "/path/to/file4.xlsx", 4),
        (5, "Submit for Approval", "Not run", None, 2),
        (6, "Check Approval Status", "Passed", "/path/to/file6.xlsx", 6),
        (7, "Generate PO Report", "Not run", "/path/to/file7.xlsx", 7)
    ]
    
    for i, data in enumerate(sample_scenarios_data):
        scenarios_table.add_scenario(data, i+1)
    
    # Add click handlers for demo
    def on_rice_click(item, values):
        print(f"RICE clicked: {values[0]} - {values[1]}")
        
    def on_scenario_click(item, values):
        print(f"Scenario clicked: {values[0]} - {values[1]} - Status: {values[2]}")
    
    rice_table.set_row_click_callback(on_rice_click)
    scenarios_table.set_row_click_callback(on_scenario_click)
    
    # Instructions
    instructions = tk.Label(main_frame, 
                           text="✨ Features: Perfect column alignment • Click to select • Scroll with mouse wheel • Resize columns by dragging", 
                           font=('Segoe UI', 10), bg='#f8fafc', fg='#6b7280')
    instructions.pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    demo_enhanced_tables()