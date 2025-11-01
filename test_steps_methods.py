#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from selenium_tab_manager import center_dialog

class TestStepsMethods:
    """Enhanced methods for test steps management with Phase 2 UX improvements"""
    
    def __init__(self):
        self.db_manager = None
        self.show_popup = None
        self._load_group_steps = None
    
    def _add_test_step(self, group_id, parent_popup):
        """Enhanced step creation wizard with visual previews"""
        popup = tk.Toplevel(parent_popup)
        popup.title("✨ Step Creation Wizard")
        
        # Dynamic height calculation to ensure Save button is always visible
        screen_height = popup.winfo_screenheight()
        # Use 85% of screen height, with reasonable min/max bounds
        dynamic_height = min(max(int(screen_height * 0.85), 600), screen_height - 100)
        
        center_dialog(popup, 750, dynamic_height)
        popup.configure(bg='#ffffff')
        popup.resizable(True, True)
        popup.minsize(650, 600)
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced header with wizard styling
        header_frame = tk.Frame(popup, bg='#3b82f6', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#3b82f6')
        header_content.pack(fill='both', expand=True, padx=25, pady=15)
        
        tk.Label(header_content, text="✨ Step Creation Wizard", 
                font=('Segoe UI', 16, 'bold'), bg='#3b82f6', fg='#ffffff').pack(side='left')
        
        # Step counter in header
        self.step_counter_label = tk.Label(header_content, text="Step 1 of 4", 
                                          font=('Segoe UI', 10, 'bold'), bg='#3b82f6', fg='#ffffff')
        self.step_counter_label.pack(side='right')
        
        # Main content with enhanced layout
        main_frame = tk.Frame(popup, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Left panel for form with scrollable canvas
        left_panel = tk.Frame(main_frame, bg='#ffffff')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 15))
        
        # Create scrollable canvas for form
        canvas = tk.Canvas(left_panel, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind mousewheel to canvas with error handling
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget was destroyed
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Clean up mousewheel binding when popup is destroyed
        def cleanup_bindings():
            try:
                canvas.unbind_all("<MouseWheel>")
            except:
                pass
        popup.protocol("WM_DELETE_WINDOW", lambda: (cleanup_bindings(), popup.destroy()))
        
        # Right panel for preview
        right_panel = tk.Frame(main_frame, bg='#f8fafc', relief='solid', bd=1, width=250)
        right_panel.pack(side='right', fill='y', padx=(15, 0))
        right_panel.pack_propagate(False)
        
        # Step summary header
        preview_header = tk.Frame(right_panel, bg='#e5e7eb', height=40)
        preview_header.pack(fill='x')
        preview_header.pack_propagate(False)
        
        tk.Label(preview_header, text="📝 Step Summary", font=('Segoe UI', 11, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        # Step summary content
        self.preview_frame = tk.Frame(right_panel, bg='#f8fafc')
        self.preview_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Initial summary message
        self.preview_label = tk.Label(self.preview_frame, 
                                     text="Select step type to see summary", 
                                     font=('Segoe UI', 10), bg='#f8fafc', fg='#6b7280', 
                                     wraplength=200, justify='center')
        self.preview_label.pack(expand=True)
        
        frame = scrollable_frame
        
        # Enhanced step name with validation
        name_frame = tk.Frame(frame, bg='#ffffff')
        name_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(name_frame, text="1️⃣ Step Name:", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        name_entry = tk.Entry(name_frame, font=('Segoe UI', 11), relief='solid', bd=1,
                             highlightthickness=2, highlightcolor='#3b82f6')
        name_entry.pack(fill="x", ipady=8)
        
        # Validation label
        self.name_validation = tk.Label(name_frame, text="", font=('Segoe UI', 9), 
                                       bg='#ffffff', fg='#ef4444')
        self.name_validation.pack(anchor='w', pady=(2, 0))
        
        # Enhanced step type with categories
        type_frame = tk.Frame(frame, bg='#ffffff')
        type_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(type_frame, text="2️⃣ Step Type:", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(type_frame, textvariable=type_var, font=('Segoe UI', 11), 
                                 state='readonly', height=12)
        
        # Categorized step types with icons
        step_types = [
            '🌐 Navigate', '👆 Element Click', '⌨️ Text Input', '📋 Dropdown Select',
            '☑️ Checkbox Toggle', '🔘 Radio Button Select', '📁 File Upload',
            '🖱️ Mouse Hover', '📜 Scroll', '⏱️ Wait', '📸 Take Screenshot',
            '📝 Get Text', '🔍 Get Attribute', '🧹 Clear Field', '🔄 Refresh Page',
            '⬅️ Go Back', '➡️ Go Forward', '⚠️ Accept Alert', '❌ Dismiss Alert',
            '⌨️ Send Keys', '🖼️ Switch Frame', '🪟 Switch Window', '📧 Email Check',
            '🔧 JavaScript Execute', '🎯 Drag and Drop'
        ]
        type_combo['values'] = step_types
        type_combo.pack(fill="x", ipady=6)
        
        # Helper text
        tk.Label(type_frame, text="Choose the action this step will perform", 
                font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(anchor='w', pady=(4, 0))
        
        # Enhanced dynamic fields with better organization
        config_frame = tk.Frame(frame, bg='#ffffff')
        config_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(config_frame, text="3️⃣ Step Configuration:", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        # Dynamic fields container with enhanced styling
        dynamic_frame = tk.Frame(config_frame, bg='#ffffff')
        dynamic_frame.pack(fill="x", pady=(0, 10))
        
        # Store dynamic widgets
        dynamic_widgets = {}
        
        def update_dynamic_fields(*args):
            # Clear existing dynamic fields
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_widgets.clear()
            
            # Update step counter
            self.step_counter_label.config(text="Step 3 of 4")
            
            # Get clean step type (remove emoji)
            raw_type = type_var.get()
            if not raw_type:
                self.update_preview("Select a step type to continue")
                return
                
            step_type = raw_type.split(' ', 1)[1] if ' ' in raw_type else raw_type
            
            # Update summary immediately
            self.update_preview(f"Configuring: {step_type}")
            
            if step_type == 'Navigate':
                tk.Label(dynamic_frame, text="🌐 Target URL:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                url_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                    highlightthickness=1, highlightcolor='#10b981')
                url_entry.pack(fill="x", ipady=6, pady=(0, 5))
                url_entry.insert(0, "https://")
                dynamic_widgets['url'] = url_entry
                
                # URL validation
                def validate_url(*args):
                    url = url_entry.get()
                    if url and (url.startswith('http://') or url.startswith('https://')):
                        self.update_preview(f"Navigate to: {url}")
                    else:
                        self.update_preview("Enter a valid URL (http:// or https://)")
                
                url_entry.bind('<KeyRelease>', validate_url)
                
            elif step_type == 'Element Click':
                tk.Label(dynamic_frame, text="👆 Click Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                click_var = tk.StringVar(value='👆 Left Click')
                click_combo = ttk.Combobox(dynamic_frame, textvariable=click_var, 
                                         font=('Segoe UI', 10), state='readonly')
                click_combo['values'] = ['👆 Left Click', '🖱️ Right Click', '⚡ Double Click']
                click_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['click_type'] = click_var
                
                tk.Label(dynamic_frame, text="🎯 Element Selector Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value='🆔 ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, 
                                            font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['🆔 ID', '🏷️ Class Name', '🛤️ XPath', '🎨 CSS Selector', '📛 Name', '🏷️ Tag Name']
                selector_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="🔍 Element Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                element_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['element'] = element_entry
                
                # Element validation and preview
                def validate_element(*args):
                    selector_type = selector_var.get().split(' ', 1)[1] if ' ' in selector_var.get() else selector_var.get()
                    element_val = element_entry.get()
                    click_type = click_var.get().split(' ', 1)[1] if ' ' in click_var.get() else click_var.get()
                    
                    if element_val:
                        preview_text = f"{click_type} on element:\n{selector_type}: {element_val}"
                        self.update_preview(preview_text)
                    else:
                        self.update_preview("Enter element selector value")
                
                element_entry.bind('<KeyRelease>', validate_element)
                selector_combo.bind('<<ComboboxSelected>>', validate_element)
                click_combo.bind('<<ComboboxSelected>>', validate_element)
                
            elif step_type == 'Text Input':
                tk.Label(dynamic_frame, text="🎯 Element Selector Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value='🆔 ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, 
                                            font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['🆔 ID', '🏷️ Class Name', '🛤️ XPath', '🎨 CSS Selector', '📛 Name']
                selector_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="🔍 Element Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                element_entry.pack(fill="x", ipady=6, pady=(0, 10))
                dynamic_widgets['element'] = element_entry
                
                tk.Label(dynamic_frame, text="⌨️ Text to Input:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                text_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                    highlightthickness=1, highlightcolor='#10b981')
                text_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['text'] = text_entry
                
                # Text input validation and preview
                def validate_text_input(*args):
                    selector_type = selector_var.get().split(' ', 1)[1] if ' ' in selector_var.get() else selector_var.get()
                    element_val = element_entry.get()
                    text_val = text_entry.get()
                    
                    if element_val and text_val:
                        preview_text = f"Type text into element:\n{selector_type}: {element_val}\nText: '{text_val}'"
                        self.update_preview(preview_text)
                    elif element_val:
                        self.update_preview(f"Element: {selector_type}: {element_val}\nEnter text to input")
                    else:
                        self.update_preview("Enter element selector and text")
                
                element_entry.bind('<KeyRelease>', validate_text_input)
                text_entry.bind('<KeyRelease>', validate_text_input)
                selector_combo.bind('<<ComboboxSelected>>', validate_text_input)
                
            elif step_type == 'Wait':
                tk.Label(dynamic_frame, text="⏱️ Wait Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                wait_var = tk.StringVar(value='⏰ Time (seconds)')
                wait_combo = ttk.Combobox(dynamic_frame, textvariable=wait_var, 
                                        font=('Segoe UI', 10), state='readonly')
                wait_combo['values'] = ['⏰ Time (seconds)', '👁️ Element Visible', '👆 Element Clickable', '📄 Page Load']
                wait_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['wait_type'] = wait_var
                
                tk.Label(dynamic_frame, text="🔢 Wait Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                wait_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                    highlightthickness=1, highlightcolor='#10b981')
                wait_entry.pack(fill="x", ipady=6, pady=(0, 5))
                wait_entry.insert(0, "5")
                dynamic_widgets['wait_value'] = wait_entry
                
                # Wait validation and preview
                def validate_wait(*args):
                    wait_type = wait_var.get().split(' ', 1)[1] if ' ' in wait_var.get() else wait_var.get()
                    wait_val = wait_entry.get()
                    
                    if wait_val:
                        if wait_type == 'Time (seconds)':
                            try:
                                seconds = float(wait_val)
                                preview_text = f"Wait for {seconds} seconds"
                            except:
                                preview_text = "Enter valid number of seconds"
                        else:
                            preview_text = f"Wait for: {wait_type}\nCondition: {wait_val}"
                        self.update_preview(preview_text)
                    else:
                        self.update_preview("Enter wait value")
                
                wait_entry.bind('<KeyRelease>', validate_wait)
                wait_combo.bind('<<ComboboxSelected>>', validate_wait)
            
            elif step_type in ['Dropdown Select', 'File Upload']:
                tk.Label(dynamic_frame, text="🎯 Element Selector Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value='🆔 ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, 
                                            font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['🆔 ID', '🏷️ Class Name', '🛤️ XPath', '🎨 CSS Selector', '📛 Name']
                selector_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="🔍 Element Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                element_entry.pack(fill="x", ipady=6, pady=(0, 10))
                dynamic_widgets['element'] = element_entry
                
                if step_type == 'Dropdown Select':
                    tk.Label(dynamic_frame, text="📋 Selection Value:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    value_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                         highlightthickness=1, highlightcolor='#10b981')
                    value_entry.pack(fill="x", ipady=6, pady=(0, 5))
                    dynamic_widgets['value'] = value_entry
                elif step_type == 'File Upload':
                    tk.Label(dynamic_frame, text="📁 File Path:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    file_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                         highlightthickness=1, highlightcolor='#10b981')
                    file_entry.pack(fill="x", ipady=6, pady=(0, 5))
                    dynamic_widgets['file_path'] = file_entry
            
            elif step_type in ['Checkbox Toggle', 'Radio Button Select', 'Mouse Hover', 'Get Text', 'Get Attribute', 'Clear Field']:
                tk.Label(dynamic_frame, text="🎯 Element Selector Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value='🆔 ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, 
                                            font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['🆔 ID', '🏷️ Class Name', '🛤️ XPath', '🎨 CSS Selector', '📛 Name']
                selector_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="🔍 Element Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                element_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['element'] = element_entry
            
            elif step_type == 'JavaScript Execute':
                tk.Label(dynamic_frame, text="🔧 JavaScript Code:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                js_text = tk.Text(dynamic_frame, width=50, height=4, font=('Segoe UI', 9))
                js_text.pack(fill="x", pady=(0, 5))
                dynamic_widgets['javascript'] = js_text
            
            elif step_type == 'Send Keys':
                tk.Label(dynamic_frame, text="⌨️ Keys to Send:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                keys_var = tk.StringVar(value='ENTER')
                keys_combo = ttk.Combobox(dynamic_frame, textvariable=keys_var, font=('Segoe UI', 10))
                keys_combo['values'] = ['ENTER', 'TAB', 'ESCAPE', 'SPACE', 'ARROW_UP', 'ARROW_DOWN']
                keys_combo.pack(fill="x", ipady=4, pady=(0, 5))
                dynamic_widgets['keys'] = keys_var
            
            elif step_type in ['Scroll', 'Drag and Drop']:
                if step_type == 'Scroll':
                    tk.Label(dynamic_frame, text="📜 Scroll Direction:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    direction_var = tk.StringVar(value='Down')
                    direction_combo = ttk.Combobox(dynamic_frame, textvariable=direction_var, 
                                                 font=('Segoe UI', 10), state='readonly')
                    direction_combo['values'] = ['Down', 'Up', 'Left', 'Right']
                    direction_combo.pack(fill="x", ipady=4, pady=(0, 10))
                    dynamic_widgets['direction'] = direction_var
                    
                    tk.Label(dynamic_frame, text="🔢 Pixels:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    pixels_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                          highlightthickness=1, highlightcolor='#10b981')
                    pixels_entry.insert(0, "300")
                    pixels_entry.pack(fill="x", ipady=6, pady=(0, 5))
                    dynamic_widgets['pixels'] = pixels_entry
                
                elif step_type == 'Drag and Drop':
                    tk.Label(dynamic_frame, text="🎯 Source Element:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    source_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                           highlightthickness=1, highlightcolor='#10b981')
                    source_entry.pack(fill="x", ipady=6, pady=(0, 10))
                    dynamic_widgets['source'] = source_entry
                    
                    tk.Label(dynamic_frame, text="🎯 Target Element:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    target_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                           highlightthickness=1, highlightcolor='#10b981')
                    target_entry.pack(fill="x", ipady=6, pady=(0, 5))
                    dynamic_widgets['target'] = target_entry
            
            elif step_type in ['Switch Frame', 'Switch Window', 'Email Check']:
                if step_type in ['Switch Frame', 'Switch Window']:
                    tk.Label(dynamic_frame, text="🆔 Frame/Window ID:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    id_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                    id_entry.pack(fill="x", ipady=6, pady=(0, 5))
                    dynamic_widgets['identifier'] = id_entry
                
                elif step_type == 'Email Check':
                    tk.Label(dynamic_frame, text="📧 Search Criteria:", font=('Segoe UI', 11, 'bold'), 
                            bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                    search_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                           highlightthickness=1, highlightcolor='#10b981')
                    search_entry.insert(0, 'subject:"notification"')
                    search_entry.pack(fill="x", ipady=6, pady=(0, 5))
                    dynamic_widgets['search'] = search_entry
            
            elif step_type in ['Take Screenshot', 'Refresh Page', 'Go Back', 'Go Forward', 'Accept Alert', 'Dismiss Alert']:
                tk.Label(dynamic_frame, text="✅ No additional configuration required", 
                        font=('Segoe UI', 11), bg='#ffffff', fg='#10b981').pack(anchor="w", pady=(10, 5))
                dynamic_widgets['no_config'] = True
                self.update_preview(f"Ready to create {step_type} step")
        
        type_combo.bind('<<ComboboxSelected>>', update_dynamic_fields)
        
        # Store reference for validation triggering
        self.current_dynamic_widgets = dynamic_widgets
        
        # Enhanced description section
        desc_frame = tk.Frame(frame, bg='#ffffff')
        desc_frame.pack(fill='x', pady=(15, 20))
        
        tk.Label(desc_frame, text="4️⃣ Description (Optional):", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        desc_entry = tk.Entry(desc_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                             highlightthickness=1, highlightcolor='#3b82f6')
        desc_entry.pack(fill="x", ipady=6)
        
        tk.Label(desc_frame, text="Add notes or comments about this step", 
                font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280').pack(anchor='w', pady=(4, 0))
        
        # Update step counter when description is focused
        def on_desc_focus(*args):
            self.step_counter_label.config(text="Step 4 of 4")
        desc_entry.bind('<FocusIn>', on_desc_focus)
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def build_target_string():
            raw_type = type_var.get()
            step_type = raw_type.split(' ', 1)[1] if ' ' in raw_type else raw_type
            
            if step_type == 'Navigate':
                return dynamic_widgets.get('url', tk.Entry()).get().strip()
            
            elif step_type in ['Element Click', 'Text Input']:
                raw_selector = dynamic_widgets.get('selector_type', tk.StringVar()).get()
                selector_type = raw_selector.split(' ', 1)[1] if ' ' in raw_selector else raw_selector
                element_value = dynamic_widgets.get('element', tk.Entry()).get().strip()
                
                if selector_type == 'ID':
                    target = f"#{element_value}"
                elif selector_type == 'Class Name':
                    target = f".{element_value}"
                elif selector_type == 'XPath':
                    target = element_value
                elif selector_type == 'CSS Selector':
                    target = element_value
                elif selector_type == 'Name':
                    target = f"[name='{element_value}']"
                elif selector_type == 'Tag Name':
                    target = element_value
                else:
                    target = element_value
                
                if step_type == 'Element Click':
                    raw_click = dynamic_widgets.get('click_type', tk.StringVar()).get()
                    click_type = raw_click.split(' ', 1)[1] if ' ' in raw_click else raw_click
                    if click_type == 'Right Click':
                        target += " [RIGHT-CLICK]"
                    elif click_type == 'Double Click':
                        target += " [DOUBLE-CLICK]"
                
                return target
            
            elif step_type == 'Wait':
                raw_wait = dynamic_widgets.get('wait_type', tk.StringVar()).get()
                wait_type = raw_wait.split(' ', 1)[1] if ' ' in raw_wait else raw_wait
                wait_value = dynamic_widgets.get('wait_value', tk.Entry()).get().strip()
                return f"{wait_type}: {wait_value}"
            
            elif step_type in ['Dropdown Select', 'File Upload']:
                raw_selector = dynamic_widgets.get('selector_type', tk.StringVar()).get()
                selector_type = raw_selector.split(' ', 1)[1] if ' ' in raw_selector else raw_selector
                element_value = dynamic_widgets.get('element', tk.Entry()).get().strip()
                
                if selector_type == 'ID':
                    target = f"#{element_value}"
                elif selector_type == 'Class Name':
                    target = f".{element_value}"
                else:
                    target = element_value
                
                if step_type == 'Dropdown Select':
                    value = dynamic_widgets.get('value', tk.Entry()).get().strip()
                    return f"{target} | {value}"
                elif step_type == 'File Upload':
                    file_path = dynamic_widgets.get('file_path', tk.Entry()).get().strip()
                    return f"{target} | {file_path}"
            
            elif step_type in ['Checkbox Toggle', 'Radio Button Select', 'Mouse Hover', 'Get Text', 'Get Attribute', 'Clear Field']:
                raw_selector = dynamic_widgets.get('selector_type', tk.StringVar()).get()
                selector_type = raw_selector.split(' ', 1)[1] if ' ' in raw_selector else raw_selector
                element_value = dynamic_widgets.get('element', tk.Entry()).get().strip()
                
                if selector_type == 'ID':
                    return f"#{element_value}"
                elif selector_type == 'Class Name':
                    return f".{element_value}"
                else:
                    return element_value
            
            elif step_type == 'JavaScript Execute':
                return dynamic_widgets.get('javascript', tk.Text()).get(1.0, tk.END).strip()
            
            elif step_type == 'Send Keys':
                return dynamic_widgets.get('keys', tk.StringVar()).get()
            
            elif step_type == 'Scroll':
                direction = dynamic_widgets.get('direction', tk.StringVar()).get()
                pixels = dynamic_widgets.get('pixels', tk.Entry()).get().strip()
                return f"{direction}: {pixels}"
            
            elif step_type == 'Drag and Drop':
                source = dynamic_widgets.get('source', tk.Entry()).get().strip()
                target = dynamic_widgets.get('target', tk.Entry()).get().strip()
                return f"{source} | {target}"
            
            elif step_type in ['Switch Frame', 'Switch Window']:
                return dynamic_widgets.get('identifier', tk.Entry()).get().strip()
            
            elif step_type == 'Email Check':
                return dynamic_widgets.get('search', tk.Entry()).get().strip()
            
            # For step types that don't need configuration
            return step_type
        
        def validate_form():
            """Enhanced form validation with visual feedback"""
            errors = []
            
            # Validate name
            name = name_entry.get().strip()
            if not name:
                errors.append("Step name is required")
                self.name_validation.config(text="❌ Step name is required")
            elif len(name) < 3:
                errors.append("Step name must be at least 3 characters")
                self.name_validation.config(text="❌ Name too short (min 3 chars)", fg='#ef4444')
            else:
                self.name_validation.config(text="✅ Valid name", fg='#10b981')
            
            # Validate step type
            raw_type = type_var.get().strip()
            if not raw_type:
                errors.append("Step type is required")
            
            return errors
        
        def save_step():
            # Validate form first
            errors = validate_form()
            if errors:
                self.show_popup("Validation Error", "\n".join(errors), "error")
                return
            
            name = name_entry.get().strip()
            raw_type = type_var.get().strip()
            step_type = raw_type.split(' ', 1)[1] if ' ' in raw_type else raw_type
            
            target = build_target_string()
            if not target and step_type not in ['Take Screenshot', 'Refresh Page', 'Go Back', 'Go Forward', 'Accept Alert', 'Dismiss Alert']:
                self.show_popup("Configuration Error", "Please complete the step configuration", "error")
                return
            
            # Build description
            description = desc_entry.get().strip()
            if step_type == 'Text Input' and 'text' in dynamic_widgets:
                text_input = dynamic_widgets['text'].get().strip()
                if text_input:
                    description = text_input
            
            try:
                rice_profiles = self.db_manager.get_rice_profiles()
                rice_profile_id = rice_profiles[0][0] if rice_profiles else 1
                
                self.db_manager.save_test_step(rice_profile_id, name, step_type, target, description, group_id)
                popup.destroy()
                self._load_group_steps(group_id)
                self.show_popup("Success", f"✨ Test step '{name}' created successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to add test step: {str(e)}", "error")
        
        # Enhanced action buttons
        tk.Button(btn_frame, text="💾 Create Step", font=('Segoe UI', 11, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0, command=save_step).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="❌ Cancel", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        # Add validation on name entry
        name_entry.bind('<KeyRelease>', lambda e: validate_form())
        
        name_entry.focus()
        
        # Initialize step summary
        self.update_preview("Welcome to Step Creation Wizard!\n\nStart by entering a step name.")
    
    def update_preview(self, text):
        """Update the step summary panel"""
        if hasattr(self, 'preview_label'):
            self.preview_label.config(text=text)
            
            # Add visual styling based on content
            if "✅" in text or "success" in text.lower():
                self.preview_label.config(fg='#10b981')
            elif "❌" in text or "error" in text.lower() or "Enter" in text:
                self.preview_label.config(fg='#ef4444')
            elif "Configuring" in text or "Ready to configure" in text:
                self.preview_label.config(fg='#3b82f6')
            else:
                self.preview_label.config(fg='#374151')
    
    def _edit_test_step(self, step_id, group_id, parent_popup):
        """Enhanced edit test step dialog matching Step Creation Wizard"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT name, step_type, target, description FROM test_steps WHERE id = ? AND user_id = ?", 
                      (step_id, self.db_manager.user_id))
        step_data = cursor.fetchone()
        
        if not step_data:
            self.show_popup("Error", "Test step not found", "error")
            return
        
        name, step_type, target, description = step_data
        
        popup = tk.Toplevel(parent_popup)
        popup.title("✏️ Edit Test Step")
        
        # Dynamic height like Step Creation Wizard
        screen_height = popup.winfo_screenheight()
        dynamic_height = min(max(int(screen_height * 0.85), 600), screen_height - 100)
        
        center_dialog(popup, 750, dynamic_height)
        popup.configure(bg='#ffffff')
        popup.resizable(True, True)
        popup.minsize(650, 600)
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced header matching wizard
        header_frame = tk.Frame(popup, bg='#10b981', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#10b981')
        header_content.pack(fill='both', expand=True, padx=25, pady=15)
        
        tk.Label(header_content, text="✏️ Edit Test Step", 
                font=('Segoe UI', 16, 'bold'), bg='#10b981', fg='#ffffff').pack(side='left')
        
        # Main content with scrollable form
        main_frame = tk.Frame(popup, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Scrollable canvas for form
        canvas = tk.Canvas(main_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Bind mousewheel with error handling
        def _on_mousewheel(event):
            try:
                if canvas.winfo_exists():
                    canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Widget was destroyed
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Clean up mousewheel binding when popup is destroyed
        def cleanup_bindings():
            try:
                canvas.unbind_all("<MouseWheel>")
            except:
                pass
        popup.protocol("WM_DELETE_WINDOW", lambda: (cleanup_bindings(), popup.destroy()))
        
        frame = scrollable_frame
        
        # Step name
        name_frame = tk.Frame(frame, bg='#ffffff')
        name_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(name_frame, text="📝 Step Name:", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        name_entry = tk.Entry(name_frame, font=('Segoe UI', 11), relief='solid', bd=1,
                             highlightthickness=2, highlightcolor='#3b82f6')
        name_entry.insert(0, name)
        name_entry.pack(fill="x", ipady=8)
        
        # Step type with emoji matching
        type_frame = tk.Frame(frame, bg='#ffffff')
        type_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(type_frame, text="🎯 Step Type:", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        # Convert plain step_type to emoji version for display
        step_type_map = {
            'Navigate': '🌐 Navigate', 'Element Click': '👆 Element Click', 'Text Input': '⌨️ Text Input',
            'Dropdown Select': '📋 Dropdown Select', 'Checkbox Toggle': '☑️ Checkbox Toggle',
            'Radio Button Select': '🔘 Radio Button Select', 'File Upload': '📁 File Upload',
            'Mouse Hover': '🖱️ Mouse Hover', 'Scroll': '📜 Scroll', 'Wait': '⏱️ Wait',
            'Take Screenshot': '📸 Take Screenshot', 'Get Text': '📝 Get Text',
            'Get Attribute': '🔍 Get Attribute', 'Clear Field': '🧹 Clear Field',
            'Refresh Page': '🔄 Refresh Page', 'Go Back': '⬅️ Go Back', 'Go Forward': '➡️ Go Forward',
            'Accept Alert': '⚠️ Accept Alert', 'Dismiss Alert': '❌ Dismiss Alert',
            'Send Keys': '⌨️ Send Keys', 'Switch Frame': '🖼️ Switch Frame',
            'Switch Window': '🪟 Switch Window', 'Email Check': '📧 Email Check',
            'JavaScript Execute': '🔧 JavaScript Execute', 'Drag and Drop': '🎯 Drag and Drop'
        }
        
        type_var = tk.StringVar(value=step_type_map.get(step_type, step_type))
        type_combo = ttk.Combobox(type_frame, textvariable=type_var, font=('Segoe UI', 11), 
                                 state='readonly', height=12)
        
        step_types = [
            '🌐 Navigate', '👆 Element Click', '⌨️ Text Input', '📋 Dropdown Select',
            '☑️ Checkbox Toggle', '🔘 Radio Button Select', '📁 File Upload',
            '🖱️ Mouse Hover', '📜 Scroll', '⏱️ Wait', '📸 Take Screenshot',
            '📝 Get Text', '🔍 Get Attribute', '🧹 Clear Field', '🔄 Refresh Page',
            '⬅️ Go Back', '➡️ Go Forward', '⚠️ Accept Alert', '❌ Dismiss Alert',
            '⌨️ Send Keys', '🖼️ Switch Frame', '🪟 Switch Window', '📧 Email Check',
            '🔧 JavaScript Execute', '🎯 Drag and Drop'
        ]
        type_combo['values'] = step_types
        type_combo.pack(fill="x", ipady=6)
        
        # Dynamic configuration fields
        config_frame = tk.Frame(frame, bg='#ffffff')
        config_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(config_frame, text="⚙️ Step Configuration:", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        dynamic_frame = tk.Frame(config_frame, bg='#ffffff')
        dynamic_frame.pack(fill="x", pady=(0, 10))
        
        dynamic_widgets = {}
        
        def parse_existing_data():
            """Parse existing target data into components"""
            parsed = {}
            
            if step_type == 'Navigate':
                parsed['url'] = target
            elif step_type == 'Element Click':
                if '[RIGHT-CLICK]' in target:
                    parsed['click_type'] = '🖱️ Right Click'
                    clean_target = target.replace(' [RIGHT-CLICK]', '')
                elif '[DOUBLE-CLICK]' in target:
                    parsed['click_type'] = '⚡ Double Click'
                    clean_target = target.replace(' [DOUBLE-CLICK]', '')
                else:
                    parsed['click_type'] = '👆 Left Click'
                    clean_target = target
                
                if clean_target.startswith('#'):
                    parsed['selector_type'] = '🆔 ID'
                    parsed['element'] = clean_target[1:]
                elif clean_target.startswith('.'):
                    parsed['selector_type'] = '🏷️ Class Name'
                    parsed['element'] = clean_target[1:]
                elif clean_target.startswith('//'):
                    parsed['selector_type'] = '🛤️ XPath'
                    parsed['element'] = clean_target
                elif '[name=' in clean_target:
                    parsed['selector_type'] = '📛 Name'
                    parsed['element'] = clean_target
                else:
                    parsed['selector_type'] = '🎨 CSS Selector'
                    parsed['element'] = clean_target
                    
            elif step_type == 'Text Input':
                if target.startswith('#'):
                    parsed['selector_type'] = '🆔 ID'
                    parsed['element'] = target[1:]
                elif target.startswith('.'):
                    parsed['selector_type'] = '🏷️ Class Name'
                    parsed['element'] = target[1:]
                else:
                    parsed['selector_type'] = '🎨 CSS Selector'
                    parsed['element'] = target
                parsed['text'] = description
                
            elif step_type == 'Wait':
                if ':' in target:
                    wait_parts = target.split(':', 1)
                    wait_type = wait_parts[0].strip()
                    if wait_type == 'Time (seconds)':
                        parsed['wait_type'] = '⏰ Time (seconds)'
                    elif wait_type == 'Element Visible':
                        parsed['wait_type'] = '👁️ Element Visible'
                    elif wait_type == 'Element Clickable':
                        parsed['wait_type'] = '👆 Element Clickable'
                    elif wait_type == 'Page Load':
                        parsed['wait_type'] = '📄 Page Load'
                    else:
                        parsed['wait_type'] = '⏰ Time (seconds)'
                    parsed['wait_value'] = wait_parts[1].strip()
                else:
                    parsed['wait_type'] = '⏰ Time (seconds)'
                    parsed['wait_value'] = target
                    
            elif step_type in ['Dropdown Select', 'File Upload'] and '|' in target:
                parts = target.split('|', 1)
                element_part = parts[0].strip()
                value_part = parts[1].strip()
                
                if element_part.startswith('#'):
                    parsed['selector_type'] = '🆔 ID'
                    parsed['element'] = element_part[1:]
                elif element_part.startswith('.'):
                    parsed['selector_type'] = '🏷️ Class Name'
                    parsed['element'] = element_part[1:]
                else:
                    parsed['selector_type'] = '🎨 CSS Selector'
                    parsed['element'] = element_part
                    
                if step_type == 'Dropdown Select':
                    parsed['value'] = value_part
                else:
                    parsed['file_path'] = value_part
                    
            elif step_type == 'Scroll' and ':' in target:
                parts = target.split(':', 1)
                parsed['direction'] = parts[0].strip()
                parsed['pixels'] = parts[1].strip()
                
            elif step_type == 'Drag and Drop' and '|' in target:
                parts = target.split('|', 1)
                parsed['source'] = parts[0].strip()
                parsed['target'] = parts[1].strip()
                
            elif step_type == 'JavaScript Execute':
                parsed['javascript'] = target
                
            elif step_type == 'Send Keys':
                parsed['keys'] = target
                
            elif step_type in ['Switch Frame', 'Switch Window']:
                parsed['identifier'] = target
                
            elif step_type == 'Email Check':
                parsed['search'] = target
                
            elif step_type in ['Checkbox Toggle', 'Radio Button Select', 'Mouse Hover', 'Get Text', 'Get Attribute', 'Clear Field']:
                if target.startswith('#'):
                    parsed['selector_type'] = '🆔 ID'
                    parsed['element'] = target[1:]
                elif target.startswith('.'):
                    parsed['selector_type'] = '🏷️ Class Name'
                    parsed['element'] = target[1:]
                else:
                    parsed['selector_type'] = '🎨 CSS Selector'
                    parsed['element'] = target
            
            return parsed
        
        def update_dynamic_fields(*args):
            # Clear existing fields
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_widgets.clear()
            
            raw_type = type_var.get()
            current_step_type = raw_type.split(' ', 1)[1] if ' ' in raw_type else raw_type
            
            # Get parsed data for current step type
            parsed_data = parse_existing_data() if current_step_type == step_type else {}
            
            # Use same dynamic field creation as Step Creation Wizard
            if current_step_type == 'Navigate':
                tk.Label(dynamic_frame, text="🌐 Target URL:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                url_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                    highlightthickness=1, highlightcolor='#10b981')
                url_entry.insert(0, parsed_data.get('url', 'https://'))
                url_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['url'] = url_entry
                
            elif current_step_type == 'Element Click':
                tk.Label(dynamic_frame, text="👆 Click Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                click_var = tk.StringVar(value=parsed_data.get('click_type', '👆 Left Click'))
                click_combo = ttk.Combobox(dynamic_frame, textvariable=click_var, 
                                         font=('Segoe UI', 10), state='readonly')
                click_combo['values'] = ['👆 Left Click', '🖱️ Right Click', '⚡ Double Click']
                click_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['click_type'] = click_var
                
                tk.Label(dynamic_frame, text="🎯 Element Selector Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value=parsed_data.get('selector_type', '🆔 ID'))
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, 
                                            font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['🆔 ID', '🏷️ Class Name', '🛤️ XPath', '🎨 CSS Selector', '📛 Name', '🏷️ Tag Name']
                selector_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="🔍 Element Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                element_entry.insert(0, parsed_data.get('element', ''))
                element_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['element'] = element_entry
                
            elif current_step_type == 'Text Input':
                tk.Label(dynamic_frame, text="🎯 Element Selector Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value=parsed_data.get('selector_type', '🆔 ID'))
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, 
                                            font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['🆔 ID', '🏷️ Class Name', '🛤️ XPath', '🎨 CSS Selector', '📛 Name']
                selector_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="🔍 Element Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                element_entry.insert(0, parsed_data.get('element', ''))
                element_entry.pack(fill="x", ipady=6, pady=(0, 10))
                dynamic_widgets['element'] = element_entry
                
                tk.Label(dynamic_frame, text="⌨️ Text to Input:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                text_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                    highlightthickness=1, highlightcolor='#10b981')
                text_entry.insert(0, parsed_data.get('text', ''))
                text_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['text'] = text_entry
                
            elif current_step_type == 'Wait':
                tk.Label(dynamic_frame, text="⏱️ Wait Type:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                wait_var = tk.StringVar(value=parsed_data.get('wait_type', '⏰ Time (seconds)'))
                wait_combo = ttk.Combobox(dynamic_frame, textvariable=wait_var, 
                                        font=('Segoe UI', 10), state='readonly')
                wait_combo['values'] = ['⏰ Time (seconds)', '👁️ Element Visible', '👆 Element Clickable', '📄 Page Load']
                wait_combo.pack(fill="x", ipady=4, pady=(0, 10))
                dynamic_widgets['wait_type'] = wait_var
                
                tk.Label(dynamic_frame, text="🔢 Wait Value:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                wait_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                    highlightthickness=1, highlightcolor='#10b981')
                wait_entry.insert(0, parsed_data.get('wait_value', '5'))
                wait_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['wait_value'] = wait_entry
                
            # Add other step types with same pattern...
            elif current_step_type in ['Take Screenshot', 'Refresh Page', 'Go Back', 'Go Forward', 'Accept Alert', 'Dismiss Alert']:
                tk.Label(dynamic_frame, text="✅ No additional configuration required", 
                        font=('Segoe UI', 11), bg='#ffffff', fg='#10b981').pack(anchor="w", pady=(10, 5))
                dynamic_widgets['no_config'] = True
            else:
                # Generic target field for other types
                tk.Label(dynamic_frame, text="🎯 Target/Configuration:", font=('Segoe UI', 11, 'bold'), 
                        bg='#ffffff', fg='#059669').pack(anchor="w", pady=(0, 5))
                target_entry = tk.Entry(dynamic_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                                       highlightthickness=1, highlightcolor='#10b981')
                target_entry.insert(0, target)
                target_entry.pack(fill="x", ipady=6, pady=(0, 5))
                dynamic_widgets['target'] = target_entry
        
        type_combo.bind('<<ComboboxSelected>>', update_dynamic_fields)
        
        # Initialize with current step type
        update_dynamic_fields()
        
        # Description
        desc_frame = tk.Frame(frame, bg='#ffffff')
        desc_frame.pack(fill='x', pady=(15, 20))
        
        tk.Label(desc_frame, text="📄 Description (Optional):", font=('Segoe UI', 12, 'bold'), 
                bg='#ffffff', fg='#1e40af').pack(anchor="w", pady=(0, 8))
        
        desc_entry = tk.Entry(desc_frame, font=('Segoe UI', 10), relief='solid', bd=1,
                             highlightthickness=1, highlightcolor='#3b82f6')
        desc_entry.insert(0, description or '')
        desc_entry.pack(fill="x", ipady=6)
        
        # Buttons
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def save_changes():
            new_name = name_entry.get().strip()
            raw_type = type_var.get().strip()
            new_type = raw_type.split(' ', 1)[1] if ' ' in raw_type else raw_type
            new_description = desc_entry.get().strip()
            
            # Build target using same logic as Step Creation Wizard
            new_target = self.build_target_from_widgets(new_type, dynamic_widgets)
            
            if not all([new_name, new_type]):
                self.show_popup("Error", "Please fill in Name and Type fields", "error")
                return
            
            # Handle Text Input description
            if new_type == 'Text Input' and 'text' in dynamic_widgets:
                text_input = dynamic_widgets['text'].get().strip()
                if text_input:
                    new_description = text_input
            
            try:
                cursor.execute("""UPDATE test_steps 
                                 SET name = ?, step_type = ?, target = ?, description = ? 
                                 WHERE id = ? AND user_id = ?""",
                              (new_name, new_type, new_target, new_description, step_id, self.db_manager.user_id))
                self.db_manager.conn.commit()
                popup.destroy()
                self._load_group_steps(group_id)
                self.show_popup("Success", f"✨ Test step '{new_name}' updated successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update test step: {str(e)}", "error")
        
        tk.Button(btn_frame, text="💾 Save Changes", font=('Segoe UI', 11, 'bold'), 
                 bg='#10b981', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="❌ Cancel", font=('Segoe UI', 11, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10, 
                 cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
    def build_target_from_widgets(self, step_type, dynamic_widgets):
        """Build target string from dynamic widgets (shared with Step Creation Wizard)"""
        if step_type == 'Navigate':
            return dynamic_widgets.get('url', tk.Entry()).get().strip()
        
        elif step_type in ['Element Click', 'Text Input']:
            raw_selector = dynamic_widgets.get('selector_type', tk.StringVar()).get()
            selector_type = raw_selector.split(' ', 1)[1] if ' ' in raw_selector else raw_selector
            element_value = dynamic_widgets.get('element', tk.Entry()).get().strip()
            
            if selector_type == 'ID':
                target = f"#{element_value}"
            elif selector_type == 'Class Name':
                target = f".{element_value}"
            elif selector_type == 'XPath':
                target = element_value
            elif selector_type == 'CSS Selector':
                target = element_value
            elif selector_type == 'Name':
                target = f"[name='{element_value}']"
            elif selector_type == 'Tag Name':
                target = element_value
            else:
                target = element_value
            
            if step_type == 'Element Click':
                raw_click = dynamic_widgets.get('click_type', tk.StringVar()).get()
                click_type = raw_click.split(' ', 1)[1] if ' ' in raw_click else raw_click
                if click_type == 'Right Click':
                    target += " [RIGHT-CLICK]"
                elif click_type == 'Double Click':
                    target += " [DOUBLE-CLICK]"
            
            return target
        
        elif step_type == 'Wait':
            raw_wait = dynamic_widgets.get('wait_type', tk.StringVar()).get()
            wait_type = raw_wait.split(' ', 1)[1] if ' ' in raw_wait else raw_wait
            wait_value = dynamic_widgets.get('wait_value', tk.Entry()).get().strip()
            return f"{wait_type}: {wait_value}"
        
        # For other types, return existing target or step_type
        return dynamic_widgets.get('target', tk.Entry()).get().strip() if 'target' in dynamic_widgets else step_type