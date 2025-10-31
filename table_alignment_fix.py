#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Shared column configuration for perfect alignment
RICE_COLUMNS = {
    'rice_id': {'start': 0.0, 'width': 0.12, 'title': 'RICE ID'},
    'name': {'start': 0.12, 'width': 0.25, 'title': 'Name'},
    'type': {'start': 0.37, 'width': 0.18, 'title': 'Type'},
    'channel': {'start': 0.55, 'width': 0.12, 'title': 'Channel'},
    'sftp': {'start': 0.67, 'width': 0.13, 'title': 'SFTP'},
    'actions': {'start': 0.80, 'width': 0.20, 'title': 'Actions'}
}

SCENARIOS_COLUMNS = {
    'scenario': {'start': 0.0, 'width': 0.10, 'title': 'Scenario'},
    'description': {'start': 0.10, 'width': 0.35, 'title': 'Description'},
    'result': {'start': 0.45, 'width': 0.08, 'title': 'Result'},
    'steps': {'start': 0.53, 'width': 0.07, 'title': 'Steps'},
    'file': {'start': 0.60, 'width': 0.06, 'title': 'File'},
    'screenshot': {'start': 0.66, 'width': 0.07, 'title': 'Screenshot'},
    'actions': {'start': 0.73, 'width': 0.27, 'title': 'Actions'}
}

def create_aligned_header(parent, columns_config, bg_color='#f3f4f6'):
    """Create perfectly aligned header using shared column config"""
    headers_frame = tk.Frame(parent, bg=bg_color, height=30, relief='solid', bd=1)
    headers_frame.pack(fill="x")
    headers_frame.pack_propagate(False)
    
    for col_id, config in columns_config.items():
        label = tk.Label(headers_frame, text=config['title'], 
                        font=('Segoe UI', 10, 'bold'),
                        bg=bg_color, fg='#1f2937', anchor='w', padx=18)
        label.place(relx=config['start'], y=7, relwidth=config['width'])
        
        # Add separator line (except for last column)
        if col_id != list(columns_config.keys())[-1]:
            separator_x = config['start'] + config['width']
            tk.Frame(headers_frame, bg='#d1d5db', width=1).place(
                relx=separator_x, y=3, height=24)
    
    return headers_frame

def position_data_element(parent, column_id, columns_config, widget, y_offset=8):
    """Position data element using exact same config as headers"""
    config = columns_config[column_id]
    widget.place(relx=config['start'], y=y_offset, relwidth=config['width'])
    return widget