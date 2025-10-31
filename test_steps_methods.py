#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from selenium_tab_manager import center_dialog

class TestStepsMethods:
    """Additional methods for test steps management"""
    
    def __init__(self):
        self.db_manager = None
        self.show_popup = None
        self._load_group_steps = None
    
    def _add_test_step(self, group_id, parent_popup):
        """Interactive add test step dialog"""
        popup = tk.Toplevel(parent_popup)
        popup.title("Add Test Step")
        center_dialog(popup, 600, 500)
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Step Name
        tk.Label(frame, text="Step Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=50, font=('Segoe UI', 10))
        name_entry.pack(fill="x", pady=(0, 10))
        
        # Step Type
        tk.Label(frame, text="Step Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        type_var = tk.StringVar()
        type_combo = ttk.Combobox(frame, textvariable=type_var, width=57, font=('Segoe UI', 10), state='readonly')
        type_combo['values'] = [
            'Navigate', 'Element Click', 'Text Input', 'JavaScript Execute', 'Wait',
            'File Upload', 'Dropdown Select', 'Checkbox Toggle', 'Radio Button Select',
            'Drag and Drop', 'Mouse Hover', 'Scroll', 'Switch Frame', 'Switch Window',
            'Take Screenshot', 'Get Text', 'Get Attribute', 'Clear Field', 'Refresh Page',
            'Go Back', 'Go Forward', 'Accept Alert', 'Dismiss Alert', 'Send Keys', 'Email Check'
        ]
        type_combo.pack(fill="x", pady=(0, 10))
        
        # Dynamic fields container
        dynamic_frame = tk.Frame(frame, bg='#ffffff')
        dynamic_frame.pack(fill="x", pady=(0, 10))
        
        # Store dynamic widgets
        dynamic_widgets = {}
        
        def update_dynamic_fields(*args):
            # Clear existing dynamic fields
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_widgets.clear()
            
            step_type = type_var.get()
            
            if step_type == 'Navigate':
                tk.Label(dynamic_frame, text="URL:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                url_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                url_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['url'] = url_entry
                
            elif step_type == 'Element Click':
                tk.Label(dynamic_frame, text="Click Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                click_var = tk.StringVar(value='Left Click')
                click_combo = ttk.Combobox(dynamic_frame, textvariable=click_var, width=57, font=('Segoe UI', 10), state='readonly')
                click_combo['values'] = ['Left Click', 'Right Click', 'Double Click']
                click_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['click_type'] = click_var
                
                tk.Label(dynamic_frame, text="Element Selector Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value='ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, width=57, font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['ID', 'Class Name', 'XPath', 'CSS Selector', 'Name', 'Tag Name']
                selector_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="Element Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                element_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['element'] = element_entry
                
            elif step_type == 'Text Input':
                tk.Label(dynamic_frame, text="Element Selector Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value='ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, width=57, font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['ID', 'Class Name', 'XPath', 'CSS Selector', 'Name']
                selector_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="Element Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                element_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['element'] = element_entry
                
                tk.Label(dynamic_frame, text="Text to Input:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                text_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                text_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['text'] = text_entry
                
            elif step_type == 'JavaScript Execute':
                tk.Label(dynamic_frame, text="JavaScript Code:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                js_text = tk.Text(dynamic_frame, width=50, height=4, font=('Segoe UI', 9))
                js_text.pack(fill="x", pady=(0, 5))
                dynamic_widgets['javascript'] = js_text
                
            elif step_type == 'Wait':
                tk.Label(dynamic_frame, text="Wait Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                wait_var = tk.StringVar(value='Time (seconds)')
                wait_combo = ttk.Combobox(dynamic_frame, textvariable=wait_var, width=57, font=('Segoe UI', 10), state='readonly')
                wait_combo['values'] = ['Time (seconds)', 'Element Visible', 'Element Clickable', 'Page Load']
                wait_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['wait_type'] = wait_var
                
                tk.Label(dynamic_frame, text="Wait Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                wait_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                wait_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['wait_value'] = wait_entry
                
            elif step_type == 'File Upload':
                tk.Label(dynamic_frame, text="File Input Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                selector_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector'] = selector_entry
                
                tk.Label(dynamic_frame, text="File Path:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                file_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                file_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['file_path'] = file_entry
                
            elif step_type == 'Dropdown Select':
                tk.Label(dynamic_frame, text="Dropdown Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                selector_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector'] = selector_entry
                
                tk.Label(dynamic_frame, text="Selection Method:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                method_var = tk.StringVar(value='By Text')
                method_combo = ttk.Combobox(dynamic_frame, textvariable=method_var, width=57, font=('Segoe UI', 10), state='readonly')
                method_combo['values'] = ['By Text', 'By Value', 'By Index']
                method_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['method'] = method_var
                
                tk.Label(dynamic_frame, text="Selection Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                value_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                value_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['value'] = value_entry
                
            elif step_type in ['Checkbox Toggle', 'Radio Button Select']:
                tk.Label(dynamic_frame, text="Element Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                selector_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['selector'] = selector_entry
                
            elif step_type == 'Mouse Hover':
                tk.Label(dynamic_frame, text="Element Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                selector_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['selector'] = selector_entry
                
            elif step_type == 'Scroll':
                tk.Label(dynamic_frame, text="Scroll Direction:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                direction_var = tk.StringVar(value='Down')
                direction_combo = ttk.Combobox(dynamic_frame, textvariable=direction_var, width=57, font=('Segoe UI', 10), state='readonly')
                direction_combo['values'] = ['Down', 'Up', 'Left', 'Right', 'To Element']
                direction_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['direction'] = direction_var
                
                tk.Label(dynamic_frame, text="Pixels/Element Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                value_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                value_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['value'] = value_entry
                
            elif step_type in ['Get Text', 'Get Attribute', 'Clear Field']:
                tk.Label(dynamic_frame, text="Element Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                selector_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector'] = selector_entry
                
                if step_type == 'Get Text':
                    tk.Label(dynamic_frame, text="Cache Variable Name (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    cache_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                    cache_entry.pack(fill="x", pady=(0, 5))
                    dynamic_widgets['cache_name'] = cache_entry
                elif step_type == 'Get Attribute':
                    tk.Label(dynamic_frame, text="Attribute Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    attr_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                    attr_entry.pack(fill="x", pady=(0, 10))
                    dynamic_widgets['attribute'] = attr_entry
                    
                    tk.Label(dynamic_frame, text="Cache Variable Name (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    cache_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                    cache_entry.pack(fill="x", pady=(0, 5))
                    dynamic_widgets['cache_name'] = cache_entry
                    
            elif step_type == 'Send Keys':
                tk.Label(dynamic_frame, text="Keys to Send:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                keys_var = tk.StringVar(value='ENTER')
                keys_combo = ttk.Combobox(dynamic_frame, textvariable=keys_var, width=57, font=('Segoe UI', 10))
                keys_combo['values'] = ['ENTER', 'TAB', 'ESCAPE', 'SPACE', 'ARROW_UP', 'ARROW_DOWN', 'ARROW_LEFT', 'ARROW_RIGHT', 'F1', 'F2', 'F3', 'F4', 'F5']
                keys_combo.pack(fill="x", pady=(0, 5))
                dynamic_widgets['keys'] = keys_var
                
            elif step_type == 'Email Check':
                tk.Label(dynamic_frame, text="Search Criteria:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                search_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                search_entry.insert(0, 'subject:"notification"')
                search_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['search_criteria'] = search_entry
                
                tk.Label(dynamic_frame, text="Expected Content (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                content_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                content_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['expected_content'] = content_entry
                
                tk.Label(dynamic_frame, text="Timeout (seconds):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                timeout_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                timeout_entry.insert(0, '60')
                timeout_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['timeout'] = timeout_entry
        
        type_combo.bind('<<ComboboxSelected>>', update_dynamic_fields)
        
        # Description
        tk.Label(frame, text="Description (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(10, 5))
        desc_entry = tk.Entry(frame, width=50, font=('Segoe UI', 10))
        desc_entry.pack(fill="x", pady=(0, 20))
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def build_target_string():
            step_type = type_var.get()
            
            if step_type == 'Navigate':
                return dynamic_widgets.get('url', tk.Entry()).get().strip()
            
            elif step_type in ['Element Click', 'Text Input']:
                selector_type = dynamic_widgets.get('selector_type', tk.StringVar()).get()
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
                    click_type = dynamic_widgets.get('click_type', tk.StringVar()).get()
                    if click_type == 'Right Click':
                        target += " [RIGHT-CLICK]"
                    elif click_type == 'Double Click':
                        target += " [DOUBLE-CLICK]"
                
                return target
            
            elif step_type == 'JavaScript Execute':
                return dynamic_widgets.get('javascript', tk.Text()).get(1.0, tk.END).strip()
            
            elif step_type == 'Wait':
                wait_type = dynamic_widgets.get('wait_type', tk.StringVar()).get()
                wait_value = dynamic_widgets.get('wait_value', tk.Entry()).get().strip()
                return f"{wait_type}: {wait_value}"
            
            elif step_type == 'File Upload':
                selector = dynamic_widgets.get('selector', tk.Entry()).get().strip()
                file_path = dynamic_widgets.get('file_path', tk.Entry()).get().strip()
                return f"{selector} | {file_path}"
            
            elif step_type == 'Dropdown Select':
                selector = dynamic_widgets.get('selector', tk.Entry()).get().strip()
                method = dynamic_widgets.get('method', tk.StringVar()).get()
                value = dynamic_widgets.get('value', tk.Entry()).get().strip()
                return f"{selector} | {method}: {value}"
            
            elif step_type in ['Checkbox Toggle', 'Radio Button Select', 'Mouse Hover', 'Get Text', 'Get Attribute', 'Clear Field']:
                selector = dynamic_widgets.get('selector', tk.Entry()).get().strip()
                if step_type == 'Get Text':
                    cache_name = dynamic_widgets.get('cache_name', tk.Entry()).get().strip()
                    if cache_name:
                        return f"{selector} | CACHE:{cache_name}"
                    return selector
                elif step_type == 'Get Attribute':
                    attribute = dynamic_widgets.get('attribute', tk.Entry()).get().strip()
                    cache_name = dynamic_widgets.get('cache_name', tk.Entry()).get().strip()
                    if cache_name:
                        return f"{selector} | {attribute} | CACHE:{cache_name}"
                    return f"{selector} | {attribute}"
                return selector
            
            elif step_type == 'Scroll':
                direction = dynamic_widgets.get('direction', tk.StringVar()).get()
                value = dynamic_widgets.get('value', tk.Entry()).get().strip()
                return f"{direction}: {value}"
            
            elif step_type == 'Send Keys':
                keys = dynamic_widgets.get('keys', tk.StringVar()).get()
                return keys
            
            elif step_type == 'Email Check':
                search_criteria = dynamic_widgets.get('search_criteria', tk.Entry()).get().strip()
                expected_content = dynamic_widgets.get('expected_content', tk.Entry()).get().strip()
                timeout = dynamic_widgets.get('timeout', tk.Entry()).get().strip()
                
                target_parts = [f"SEARCH:{search_criteria}"]
                if expected_content:
                    target_parts.append(f"CONTENT:{expected_content}")
                if timeout:
                    target_parts.append(f"TIMEOUT:{timeout}")
                
                return " | ".join(target_parts)
            
            elif step_type in ['Take Screenshot', 'Refresh Page', 'Go Back', 'Go Forward', 'Accept Alert', 'Dismiss Alert']:
                return step_type  # These don't need additional parameters
            
            return ""
        
        def save_step():
            name = name_entry.get().strip()
            step_type = type_var.get().strip()
            
            if not all([name, step_type]):
                self.show_popup("Error", "Please fill in Name and Type fields", "error")
                return
            
            target = build_target_string()
            if not target:
                self.show_popup("Error", "Please fill in all required fields for this step type", "error")
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
                self.show_popup("Success", f"Test step '{name}' added successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to add test step: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_step).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
    
    def _edit_test_step(self, step_id, group_id, parent_popup):
        """Interactive edit test step dialog with dynamic fields"""
        cursor = self.db_manager.conn.cursor()
        cursor.execute("SELECT name, step_type, target, description FROM test_steps WHERE id = ? AND user_id = ?", 
                      (step_id, self.db_manager.user_id))
        step_data = cursor.fetchone()
        
        if not step_data:
            self.show_popup("Error", "Test step not found", "error")
            return
        
        name, step_type, target, description = step_data
        
        popup = tk.Toplevel(parent_popup)
        popup.title("Edit Test Step")
        center_dialog(popup, 600, 500)
        popup.configure(bg='#ffffff')
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Step Name
        tk.Label(frame, text="Step Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        name_entry = tk.Entry(frame, width=50, font=('Segoe UI', 10))
        name_entry.insert(0, name)
        name_entry.pack(fill="x", pady=(0, 10))
        
        # Step Type
        tk.Label(frame, text="Step Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
        type_var = tk.StringVar(value=step_type)
        type_combo = ttk.Combobox(frame, textvariable=type_var, width=57, font=('Segoe UI', 10), state='readonly')
        type_combo['values'] = [
            'Navigate', 'Element Click', 'Text Input', 'JavaScript Execute', 'Wait',
            'File Upload', 'Dropdown Select', 'Checkbox Toggle', 'Radio Button Select',
            'Drag and Drop', 'Mouse Hover', 'Scroll', 'Switch Frame', 'Switch Window',
            'Take Screenshot', 'Get Text', 'Get Attribute', 'Clear Field', 'Refresh Page',
            'Go Back', 'Go Forward', 'Accept Alert', 'Dismiss Alert', 'Send Keys', 'Email Check'
        ]
        type_combo.pack(fill="x", pady=(0, 10))
        
        # Dynamic fields container
        dynamic_frame = tk.Frame(frame, bg='#ffffff')
        dynamic_frame.pack(fill="x", pady=(0, 10))
        
        # Store dynamic widgets
        dynamic_widgets = {}
        
        def parse_existing_target():
            """Parse existing target to populate dynamic fields"""
            if step_type == 'Element Click':
                # Check for click type indicators
                if '[RIGHT-CLICK]' in target:
                    return 'Right Click', target.replace(' [RIGHT-CLICK]', '')
                elif '[DOUBLE-CLICK]' in target:
                    return 'Double Click', target.replace(' [DOUBLE-CLICK]', '')
                else:
                    return 'Left Click', target
            return None, target
        
        def update_dynamic_fields(*args):
            # Clear existing dynamic fields
            for widget in dynamic_frame.winfo_children():
                widget.destroy()
            dynamic_widgets.clear()
            
            current_type = type_var.get()
            
            if current_type == 'Navigate':
                tk.Label(dynamic_frame, text="URL:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                url_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                url_entry.insert(0, target if current_type == step_type else '')
                url_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['url'] = url_entry
                
            elif current_type == 'Element Click':
                click_type, clean_target = parse_existing_target() if current_type == step_type else ('Left Click', '')
                
                tk.Label(dynamic_frame, text="Click Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                click_var = tk.StringVar(value=click_type)
                click_combo = ttk.Combobox(dynamic_frame, textvariable=click_var, width=57, font=('Segoe UI', 10), state='readonly')
                click_combo['values'] = ['Left Click', 'Right Click', 'Double Click']
                click_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['click_type'] = click_var
                
                # Detect original selector type
                detected_type = 'CSS Selector'  # Default
                if clean_target.startswith('#'):
                    detected_type = 'ID'
                elif clean_target.startswith('.'):
                    detected_type = 'Class Name'
                elif clean_target.startswith('//'):
                    detected_type = 'XPath'
                elif '[name=' in clean_target:
                    detected_type = 'Name'
                elif clean_target in ['input', 'button', 'div', 'span', 'a', 'img']:
                    detected_type = 'Tag Name'
                
                tk.Label(dynamic_frame, text="Element Selector Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value=detected_type if current_type == step_type else 'ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, width=57, font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['ID', 'Class Name', 'XPath', 'CSS Selector', 'Name', 'Tag Name']
                selector_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="Element Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                element_entry.insert(0, clean_target)
                element_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['element'] = element_entry
                
            elif current_type == 'Text Input':
                # Detect original selector type for Text Input
                detected_type = 'CSS Selector'  # Default
                if target.startswith('#'):
                    detected_type = 'ID'
                elif target.startswith('.'):
                    detected_type = 'Class Name'
                elif target.startswith('//'):
                    detected_type = 'XPath'
                elif '[name=' in target:
                    detected_type = 'Name'
                
                tk.Label(dynamic_frame, text="Element Selector Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_var = tk.StringVar(value=detected_type if current_type == step_type else 'ID')
                selector_combo = ttk.Combobox(dynamic_frame, textvariable=selector_var, width=57, font=('Segoe UI', 10), state='readonly')
                selector_combo['values'] = ['ID', 'Class Name', 'XPath', 'CSS Selector', 'Name']
                selector_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector_type'] = selector_var
                
                tk.Label(dynamic_frame, text="Element Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                element_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                element_entry.insert(0, target if current_type == step_type else '')
                element_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['element'] = element_entry
                
                tk.Label(dynamic_frame, text="Text to Input:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                text_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                text_entry.insert(0, description if current_type == step_type else '')
                text_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['text'] = text_entry
                
            elif current_type == 'JavaScript Execute':
                tk.Label(dynamic_frame, text="JavaScript Code:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                js_text = tk.Text(dynamic_frame, width=50, height=4, font=('Segoe UI', 9))
                js_text.insert(1.0, target if current_type == step_type else '')
                js_text.pack(fill="x", pady=(0, 5))
                dynamic_widgets['javascript'] = js_text
                
            elif current_type == 'Wait':
                # Parse existing wait type from target
                existing_wait_type = 'Time (seconds)'  # Default
                existing_wait_value = ''
                
                if current_type == step_type and target:
                    if target.startswith('Element Visible:'):
                        existing_wait_type = 'Element Visible'
                        existing_wait_value = target.replace('Element Visible:', '').strip()
                    elif target.startswith('Element Clickable:'):
                        existing_wait_type = 'Element Clickable'
                        existing_wait_value = target.replace('Element Clickable:', '').strip()
                    elif target.startswith('Page Load:'):
                        existing_wait_type = 'Page Load'
                        existing_wait_value = target.replace('Page Load:', '').strip()
                    elif ':' in target:
                        parts = target.split(':', 1)
                        existing_wait_type = parts[0].strip()
                        existing_wait_value = parts[1].strip()
                    else:
                        # Time-based wait (just a number)
                        existing_wait_type = 'Time (seconds)'
                        existing_wait_value = target
                
                tk.Label(dynamic_frame, text="Wait Type:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                wait_var = tk.StringVar(value=existing_wait_type)
                wait_combo = ttk.Combobox(dynamic_frame, textvariable=wait_var, width=57, font=('Segoe UI', 10), state='readonly')
                wait_combo['values'] = ['Time (seconds)', 'Element Visible', 'Element Clickable', 'Page Load']
                wait_combo.pack(fill="x", pady=(0, 10))
                dynamic_widgets['wait_type'] = wait_var
                
                tk.Label(dynamic_frame, text="Wait Value:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                wait_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                wait_entry.insert(0, existing_wait_value)
                wait_entry.pack(fill="x", pady=(0, 5))
                dynamic_widgets['wait_value'] = wait_entry
                
            elif current_type in ['Get Text', 'Get Attribute', 'Clear Field']:
                # Parse existing target for Get Text
                existing_selector = target
                existing_cache = ''
                if current_type == step_type and current_type == 'Get Text' and ' | CACHE:' in target:
                    parts = target.split(' | CACHE:')
                    existing_selector = parts[0]
                    existing_cache = parts[1] if len(parts) > 1 else ''
                
                tk.Label(dynamic_frame, text="Element Selector:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                selector_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                selector_entry.insert(0, existing_selector if current_type == step_type else '')
                selector_entry.pack(fill="x", pady=(0, 10))
                dynamic_widgets['selector'] = selector_entry
                
                if current_type == 'Get Text':
                    tk.Label(dynamic_frame, text="Cache Variable Name (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    cache_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                    cache_entry.insert(0, existing_cache if current_type == step_type else '')
                    cache_entry.pack(fill="x", pady=(0, 5))
                    dynamic_widgets['cache_name'] = cache_entry
                elif current_type == 'Get Attribute':
                    # Parse existing target for Get Attribute
                    existing_attr = ''
                    existing_cache = ''
                    if current_type == step_type and ' | ' in target:
                        parts = target.split(' | ')
                        existing_attr = parts[1] if len(parts) > 1 else ''
                        if len(parts) > 2 and parts[2].startswith('CACHE:'):
                            existing_cache = parts[2].replace('CACHE:', '')
                    
                    tk.Label(dynamic_frame, text="Attribute Name:", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    attr_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                    attr_entry.insert(0, existing_attr if current_type == step_type else '')
                    attr_entry.pack(fill="x", pady=(0, 10))
                    dynamic_widgets['attribute'] = attr_entry
                    
                    tk.Label(dynamic_frame, text="Cache Variable Name (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(0, 5))
                    cache_entry = tk.Entry(dynamic_frame, width=50, font=('Segoe UI', 10))
                    cache_entry.insert(0, existing_cache if current_type == step_type else '')
                    cache_entry.pack(fill="x", pady=(0, 5))
                    dynamic_widgets['cache_name'] = cache_entry
        
        type_combo.bind('<<ComboboxSelected>>', update_dynamic_fields)
        
        # Initialize with current step type
        update_dynamic_fields()
        
        # Description
        tk.Label(frame, text="Description (Optional):", font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(anchor="w", pady=(10, 5))
        desc_entry = tk.Entry(frame, width=50, font=('Segoe UI', 10))
        desc_entry.insert(0, description or '')
        desc_entry.pack(fill="x", pady=(0, 20))
        
        btn_frame = tk.Frame(frame, bg='#ffffff')
        btn_frame.pack()
        
        def build_target_string():
            current_type = type_var.get()
            
            if current_type == 'Navigate':
                return dynamic_widgets.get('url', tk.Entry()).get().strip()
            
            elif current_type in ['Element Click', 'Text Input']:
                selector_type = dynamic_widgets.get('selector_type', tk.StringVar()).get()
                element_value = dynamic_widgets.get('element', tk.Entry()).get().strip()
                
                if selector_type == 'ID':
                    target_str = f"#{element_value}"
                elif selector_type == 'Class Name':
                    target_str = f".{element_value}"
                elif selector_type == 'XPath':
                    target_str = element_value
                elif selector_type == 'CSS Selector':
                    target_str = element_value
                elif selector_type == 'Name':
                    target_str = f"[name='{element_value}']"
                elif selector_type == 'Tag Name':
                    target_str = element_value
                else:
                    target_str = element_value
                
                if current_type == 'Element Click':
                    click_type = dynamic_widgets.get('click_type', tk.StringVar()).get()
                    if click_type == 'Right Click':
                        target_str += " [RIGHT-CLICK]"
                    elif click_type == 'Double Click':
                        target_str += " [DOUBLE-CLICK]"
                
                return target_str
            
            elif current_type == 'JavaScript Execute':
                return dynamic_widgets.get('javascript', tk.Text()).get(1.0, tk.END).strip()
            
            elif current_type == 'Wait':
                wait_type = dynamic_widgets.get('wait_type', tk.StringVar()).get()
                wait_value = dynamic_widgets.get('wait_value', tk.Entry()).get().strip()
                return f"{wait_type}: {wait_value}"
            
            elif current_type in ['Get Text', 'Get Attribute', 'Clear Field']:
                selector = dynamic_widgets.get('selector', tk.Entry()).get().strip()
                if current_type == 'Get Text':
                    cache_name = dynamic_widgets.get('cache_name', tk.Entry()).get().strip()
                    if cache_name:
                        return f"{selector} | CACHE:{cache_name}"
                    return selector
                elif current_type == 'Get Attribute':
                    attribute = dynamic_widgets.get('attribute', tk.Entry()).get().strip()
                    cache_name = dynamic_widgets.get('cache_name', tk.Entry()).get().strip()
                    if cache_name:
                        return f"{selector} | {attribute} | CACHE:{cache_name}"
                    return f"{selector} | {attribute}"
                return selector
            
            return target  # Keep original if not handled
        
        def save_changes():
            new_name = name_entry.get().strip()
            new_type = type_var.get().strip()
            
            if not all([new_name, new_type]):
                self.show_popup("Error", "Please fill in Name and Type fields", "error")
                return
            
            new_target = build_target_string()
            if not new_target and new_type in ['Navigate', 'Element Click', 'Text Input', 'JavaScript Execute', 'Wait']:
                self.show_popup("Error", "Please fill in all required fields for this step type", "error")
                return
            
            # Build description
            new_description = desc_entry.get().strip()
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
                self.show_popup("Success", f"Test step '{new_name}' updated successfully!", "success")
            except Exception as e:
                self.show_popup("Error", f"Failed to update test step: {str(e)}", "error")
        
        tk.Button(btn_frame, text="Save Changes", font=('Segoe UI', 10, 'bold'), bg='#10b981', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=save_changes).pack(side="left", padx=(0, 10))
        tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff', 
                 relief='flat', padx=15, pady=8, cursor='hand2', bd=0, command=popup.destroy).pack(side="left")
        
        name_entry.focus()
