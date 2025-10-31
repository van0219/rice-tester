#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk

class EnhancedTable:
    """Professional table widget using ttk.Treeview for perfect alignment"""
    
    def __init__(self, parent, columns, column_widths=None, height=200):
        self.parent = parent
        self.columns = columns
        self.column_widths = column_widths or {}
        self.height = height
        
        # Create main container
        self.container = tk.Frame(parent, bg='#ffffff')
        
        # Create treeview with scrollbars
        self.tree_frame = tk.Frame(self.container, bg='#ffffff')
        self.tree_frame.pack(fill='both', expand=True)
        
        # Create treeview
        self.tree = ttk.Treeview(self.tree_frame, columns=list(columns.keys()), 
                                show='headings', height=height//25)
        
        # Configure columns
        for col_id, col_name in columns.items():
            self.tree.heading(col_id, text=col_name, anchor='w')
            width = self.column_widths.get(col_id, 100)
            self.tree.column(col_id, width=width, anchor='w', stretch=True)
        
        # Create scrollbars
        v_scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.tree_frame, orient='horizontal', command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
        
        # Style configuration
        self.setup_styles()
        
        # Bind events
        self.tree.bind('<Button-1>', self.on_click)
        self.tree.bind('<Double-1>', self.on_double_click)
        
        # Callbacks
        self.row_click_callback = None
        self.row_double_click_callback = None
        
    def setup_styles(self):
        """Setup professional styling for the treeview"""
        style = ttk.Style()
        
        # Configure treeview style
        style.configure("Enhanced.Treeview",
                       background="#ffffff",
                       foreground="#374151",
                       fieldbackground="#ffffff",
                       borderwidth=1,
                       relief="solid")
        
        style.configure("Enhanced.Treeview.Heading",
                       background="#f3f4f6",
                       foreground="#1f2937",
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=1,
                       relief="solid")
        
        # Apply style
        self.tree.configure(style="Enhanced.Treeview")
        
    def pack(self, **kwargs):
        """Pack the table container"""
        self.container.pack(**kwargs)
        
    def insert_row(self, values, tags=None):
        """Insert a row into the table"""
        item = self.tree.insert('', 'end', values=values, tags=tags or [])
        return item
        
    def clear_rows(self):
        """Clear all rows from the table"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def get_selected_item(self):
        """Get the currently selected item"""
        selection = self.tree.selection()
        return selection[0] if selection else None
        
    def get_item_values(self, item):
        """Get values for a specific item"""
        return self.tree.item(item, 'values')
        
    def set_row_click_callback(self, callback):
        """Set callback for row clicks"""
        self.row_click_callback = callback
        
    def set_row_double_click_callback(self, callback):
        """Set callback for row double clicks"""
        self.row_double_click_callback = callback
        
    def on_click(self, event):
        """Handle single click"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item and self.row_click_callback:
            values = self.get_item_values(item)
            self.row_click_callback(item, values)
            
    def on_double_click(self, event):
        """Handle double click"""
        item = self.tree.selection()[0] if self.tree.selection() else None
        if item and self.row_double_click_callback:
            values = self.get_item_values(item)
            self.row_double_click_callback(item, values)
            
    def configure_column_widths(self, widths):
        """Configure column widths"""
        for col_id, width in widths.items():
            if col_id in self.columns:
                self.tree.column(col_id, width=width)

class RiceTable(EnhancedTable):
    """Specialized table for RICE profiles"""
    
    def __init__(self, parent, height=200):
        columns = {
            'rice_id': 'RICE ID',
            'name': 'Name', 
            'type': 'Type',
            'channel': 'Channel',
            'sftp': 'SFTP',
            'actions': 'Actions'
        }
        
        column_widths = {
            'rice_id': 120,
            'name': 250,
            'type': 150,
            'channel': 120,
            'sftp': 120,
            'actions': 150
        }
        
        super().__init__(parent, columns, column_widths, height)
        
        # Configure actions column to not stretch
        self.tree.column('actions', stretch=False)
        
    def add_rice_profile(self, profile_data, profile_id):
        """Add a RICE profile row with action buttons"""
        rice_id, name, client_name, channel_name, sftp_profile_name, type_name, tenant = profile_data
        
        # Insert row
        values = (rice_id or '', name or '', type_name or '', 
                 channel_name or '', sftp_profile_name or '', 'Edit • Delete')
        
        item = self.insert_row(values)
        
        # Store profile_id as item data
        self.tree.set(item, '#1', profile_id)  # Store ID in hidden column
        
        return item

class ScenariosTable(EnhancedTable):
    """Specialized table for test scenarios"""
    
    def __init__(self, parent, height=150):
        columns = {
            'scenario': 'Scenario',
            'description': 'Description',
            'result': 'Result', 
            'steps': 'Steps',
            'file': 'File',
            'screenshot': 'Screenshot',
            'actions': 'Actions'
        }
        
        column_widths = {
            'scenario': 80,
            'description': 300,
            'result': 80,
            'steps': 60,
            'file': 60,
            'screenshot': 80,
            'actions': 150
        }
        
        super().__init__(parent, columns, column_widths, height)
        
        # Configure fixed-width columns
        for col in ['scenario', 'result', 'steps', 'file', 'screenshot', 'actions']:
            self.tree.column(col, stretch=False)
            
    def add_scenario(self, scenario_data, scenario_id):
        """Add a scenario row"""
        scenario_number, description, result, file_path, step_count = scenario_data
        
        # Format values
        result_text = result or 'Not run'
        file_text = '📁' if file_path else ''
        steps_text = str(step_count) if step_count > 0 else '0'
        
        values = (f"#{scenario_number}", description or '', result_text,
                 steps_text, file_text, '📷', 'Run • Edit • Delete')
        
        # Add color tags based on result
        tags = []
        if result == 'Passed':
            tags.append('passed')
        elif result == 'Failed':
            tags.append('failed')
        else:
            tags.append('not_run')
            
        item = self.insert_row(values, tags)
        
        # Store scenario_id as item data
        self.tree.set(item, '#1', scenario_id)
        
        return item
        
    def setup_styles(self):
        """Setup scenario-specific styles"""
        super().setup_styles()
        
        style = ttk.Style()
        
        # Result color tags
        self.tree.tag_configure('passed', foreground='#10b981')
        self.tree.tag_configure('failed', foreground='#ef4444') 
        self.tree.tag_configure('not_run', foreground='#6b7280')

# Example usage and integration helper
def create_rice_table_replacement(parent, callbacks):
    """Create enhanced RICE table to replace current implementation"""
    
    # Container for the table
    table_container = tk.Frame(parent, bg='#ffffff')
    
    # Create the enhanced table
    rice_table = RiceTable(table_container, height=200)
    rice_table.pack(fill='both', expand=True, padx=10, pady=5)
    
    # Set up callbacks
    def on_rice_click(item, values):
        # Extract profile_id from item data
        profile_id = rice_table.tree.set(item, '#1')
        if callbacks.get('select_rice_profile'):
            callbacks['select_rice_profile'](profile_id, values[0])  # rice_id
            
    def on_rice_double_click(item, values):
        profile_id = rice_table.tree.set(item, '#1')
        if callbacks.get('edit_rice_profile'):
            callbacks['edit_rice_profile'](profile_id)
            
    rice_table.set_row_click_callback(on_rice_click)
    rice_table.set_row_double_click_callback(on_rice_double_click)
    
    return table_container, rice_table

def create_scenarios_table_replacement(parent, callbacks):
    """Create enhanced scenarios table to replace current implementation"""
    
    # Container for the table
    table_container = tk.Frame(parent, bg='#ffffff')
    
    # Create the enhanced table
    scenarios_table = ScenariosTable(table_container, height=150)
    scenarios_table.pack(fill='both', expand=True, padx=10, pady=5)
    
    # Set up callbacks
    def on_scenario_click(item, values):
        scenario_id = scenarios_table.tree.set(item, '#1')
        if callbacks.get('select_scenario'):
            callbacks['select_scenario'](scenario_id)
            
    def on_scenario_double_click(item, values):
        scenario_id = scenarios_table.tree.set(item, '#1')
        if callbacks.get('run_scenario'):
            callbacks['run_scenario'](scenario_id)
            
    scenarios_table.set_row_click_callback(on_scenario_click)
    scenarios_table.set_row_double_click_callback(on_scenario_double_click)
    
    return table_container, scenarios_table