#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import json
import os

class StepTemplateManager:
    """Advanced step template library for Phase 3"""
    
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.templates_file = "step_templates.json"
        self.load_templates()
    
    def load_templates(self):
        """Load step templates from file"""
        try:
            if os.path.exists(self.templates_file):
                with open(self.templates_file, 'r', encoding='utf-8') as f:
                    self.templates = json.load(f)
            else:
                self.templates = self.get_default_templates()
                self.save_templates()
        except Exception as e:
            print(f"Error loading templates: {e}")
            self.templates = self.get_default_templates()
    
    def save_templates(self):
        """Save templates to file"""
        try:
            with open(self.templates_file, 'w', encoding='utf-8') as f:
                json.dump(self.templates, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving templates: {e}")
    
    def get_default_templates(self):
        """Get default step templates"""
        return {
            "categories": {
                "🌐 Navigation": [
                    {
                        "name": "Navigate to FSM Portal",
                        "description": "Navigate to FSM portal login page",
                        "step_type": "Navigate",
                        "target": "https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1",
                        "icon": "🌐"
                    },
                    {
                        "name": "Navigate to FSM API",
                        "description": "Navigate to FSM API endpoint",
                        "step_type": "Navigate", 
                        "target": "https://mingle-ionapi.inforcloudsuite.com/TAMICS10_AX1/FSM",
                        "icon": "🔗"
                    }
                ],
                "🔐 Authentication": [
                    {
                        "name": "Enter Username",
                        "description": "Enter username in login field",
                        "step_type": "Text Input",
                        "target": "#username",
                        "value": "{username}",
                        "icon": "👤"
                    },
                    {
                        "name": "Enter Password", 
                        "description": "Enter password in login field",
                        "step_type": "Text Input",
                        "target": "#password",
                        "value": "{password}",
                        "icon": "🔒"
                    },
                    {
                        "name": "Click Login Button",
                        "description": "Click the login/sign in button",
                        "step_type": "Element Click",
                        "target": "[type='submit']",
                        "icon": "🚪"
                    }
                ],
                "📋 Forms": [
                    {
                        "name": "Fill Text Field",
                        "description": "Fill a text input field",
                        "step_type": "Text Input",
                        "target": "{selector}",
                        "value": "{text}",
                        "icon": "📝"
                    },
                    {
                        "name": "Select Dropdown Option",
                        "description": "Select option from dropdown",
                        "step_type": "Dropdown Select",
                        "target": "{selector} | By Text: {option}",
                        "icon": "📋"
                    },
                    {
                        "name": "Check Checkbox",
                        "description": "Toggle checkbox selection",
                        "step_type": "Checkbox Toggle",
                        "target": "{selector}",
                        "icon": "☑️"
                    }
                ],
                "🎯 Actions": [
                    {
                        "name": "Click Button",
                        "description": "Click a button element",
                        "step_type": "Element Click",
                        "target": "{selector}",
                        "icon": "🔘"
                    },
                    {
                        "name": "Right Click Menu",
                        "description": "Right click to open context menu",
                        "step_type": "Element Click",
                        "target": "{selector} [RIGHT-CLICK]",
                        "icon": "🖱️"
                    },
                    {
                        "name": "Double Click",
                        "description": "Double click element",
                        "step_type": "Element Click", 
                        "target": "{selector} [DOUBLE-CLICK]",
                        "icon": "⚡"
                    }
                ],
                "⏱️ Waits": [
                    {
                        "name": "Wait 3 Seconds",
                        "description": "Wait for 3 seconds",
                        "step_type": "Wait",
                        "target": "Time (seconds): 3",
                        "icon": "⏰"
                    },
                    {
                        "name": "Wait for Element",
                        "description": "Wait for element to be visible",
                        "step_type": "Wait",
                        "target": "Element Visible: {selector}",
                        "icon": "👁️"
                    },
                    {
                        "name": "Wait for Page Load",
                        "description": "Wait for page to fully load",
                        "step_type": "Wait",
                        "target": "Page Load: complete",
                        "icon": "📄"
                    }
                ],
                "📧 Email": [
                    {
                        "name": "Check Notification Email",
                        "description": "Check for notification email",
                        "step_type": "Email Check",
                        "target": 'SEARCH:subject:"notification" | TIMEOUT:60',
                        "icon": "📧"
                    },
                    {
                        "name": "Check Approval Email",
                        "description": "Check for approval email",
                        "step_type": "Email Check", 
                        "target": 'SEARCH:subject:"approval" | TIMEOUT:120',
                        "icon": "✅"
                    }
                ]
            }
        }
    
    def show_template_library(self, parent, group_id, callback):
        """Show template library dialog"""
        dialog = tk.Toplevel(parent)
        dialog.title("📚 Step Template Library")
        dialog.configure(bg='#ffffff')
        dialog.geometry("900x700")
        dialog.resizable(True, True)
        dialog.minsize(750, 600)
        dialog.transient(parent)
        dialog.grab_set()
        
        try:
            dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced header
        header_frame = tk.Frame(dialog, bg='#8b5cf6', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#8b5cf6')
        header_content.pack(fill='both', expand=True, padx=30, pady=20)
        
        title_frame = tk.Frame(header_content, bg='#8b5cf6')
        title_frame.pack(side='left')
        
        tk.Label(title_frame, text="📚 Step Template Library", 
                font=('Segoe UI', 18, 'bold'), bg='#8b5cf6', fg='#ffffff').pack(anchor='w')
        tk.Label(title_frame, text="Pre-built steps for common testing scenarios", 
                font=('Segoe UI', 10), bg='#8b5cf6', fg='#e9d5ff').pack(anchor='w')
        
        # Template count
        total_templates = sum(len(templates) for templates in self.templates["categories"].values())
        tk.Label(header_content, text=f"{total_templates} Templates", 
                font=('Segoe UI', 12, 'bold'), bg='#8b5cf6', fg='#ffffff').pack(side='right')
        
        # Main content
        main_frame = tk.Frame(dialog, bg='#ffffff')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Left panel - categories
        left_panel = tk.Frame(main_frame, bg='#f8fafc', relief='solid', bd=1, width=250)
        left_panel.pack(side='left', fill='y', padx=(0, 20))
        left_panel.pack_propagate(False)
        
        # Categories header
        cat_header = tk.Frame(left_panel, bg='#e5e7eb', height=40)
        cat_header.pack(fill='x')
        cat_header.pack_propagate(False)
        
        tk.Label(cat_header, text="📂 Categories", font=('Segoe UI', 12, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        # Categories list
        self.categories_frame = tk.Frame(left_panel, bg='#f8fafc')
        self.categories_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Right panel - templates
        right_panel = tk.Frame(main_frame, bg='#ffffff')
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Templates header
        templates_header_frame = tk.Frame(right_panel, bg='#ffffff')
        templates_header_frame.pack(fill='x', pady=(0, 15))
        
        self.templates_title = tk.Label(templates_header_frame, text="Select a category", 
                                       font=('Segoe UI', 14, 'bold'), bg='#ffffff', fg='#374151')
        self.templates_title.pack(side='left')
        
        # Search box
        search_frame = tk.Frame(templates_header_frame, bg='#ffffff')
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="🔍", font=('Segoe UI', 12), bg='#ffffff').pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Segoe UI', 10),
                               width=20, relief='solid', bd=1)
        search_entry.pack(side='left')
        search_entry.bind('<KeyRelease>', lambda e: self.filter_templates())
        
        # Templates container
        self.templates_container = tk.Frame(right_panel, bg='#ffffff')
        self.templates_container.pack(fill='both', expand=True)
        
        # Templates scroll frame
        self.templates_scroll = tk.Frame(self.templates_container, bg='#ffffff')
        self.templates_scroll.pack(fill='both', expand=True)
        
        # Bottom buttons
        bottom_frame = tk.Frame(dialog, bg='#ffffff')
        bottom_frame.pack(fill='x', padx=30, pady=(0, 30))
        
        # Left side - template management
        left_actions = tk.Frame(bottom_frame, bg='#ffffff')
        left_actions.pack(side='left')
        
        tk.Button(left_actions, text="➕ Create Template", font=('Segoe UI', 10, 'bold'),
                 bg='#10b981', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=lambda: self.create_custom_template(dialog)).pack(side='left', padx=(0, 10))
        
        tk.Button(left_actions, text="📁 Import Templates", font=('Segoe UI', 10, 'bold'),
                 bg='#3b82f6', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=self.import_templates).pack(side='left', padx=(0, 10))
        
        # Right side - dialog actions
        right_actions = tk.Frame(bottom_frame, bg='#ffffff')
        right_actions.pack(side='right')
        
        tk.Button(right_actions, text="❌ Close", font=('Segoe UI', 10, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=dialog.destroy).pack()
        
        # Store references
        self.dialog = dialog
        self.group_id = group_id
        self.callback = callback
        self.current_category = None
        
        # Load categories
        self.load_categories()
    
    def load_categories(self):
        """Load template categories"""
        for widget in self.categories_frame.winfo_children():
            widget.destroy()
        
        for i, category in enumerate(self.templates["categories"].keys()):
            template_count = len(self.templates["categories"][category])
            
            cat_frame = tk.Frame(self.categories_frame, bg='#f8fafc', cursor='hand2')
            cat_frame.pack(fill='x', pady=1)
            
            # Category button
            cat_btn = tk.Button(cat_frame, text=f"{category} ({template_count})", 
                               font=('Segoe UI', 10, 'bold'), bg='#ffffff', fg='#374151',
                               relief='flat', anchor='w', padx=15, pady=10, bd=0,
                               command=lambda cat=category: self.select_category(cat))
            cat_btn.pack(fill='x')
            
            # Hover effects
            def on_enter(e, btn=cat_btn):
                btn.configure(bg='#e5e7eb')
            def on_leave(e, btn=cat_btn):
                btn.configure(bg='#ffffff')
            
            cat_btn.bind('<Enter>', on_enter)
            cat_btn.bind('<Leave>', on_leave)
    
    def select_category(self, category):
        """Select and display templates for category"""
        self.current_category = category
        self.templates_title.config(text=category)
        self.load_templates_for_category(category)
    
    def load_templates_for_category(self, category):
        """Load templates for selected category"""
        for widget in self.templates_scroll.winfo_children():
            widget.destroy()
        
        templates = self.templates["categories"].get(category, [])
        
        if not templates:
            tk.Label(self.templates_scroll, text="No templates in this category", 
                    font=('Segoe UI', 12), bg='#ffffff', fg='#6b7280').pack(expand=True)
            return
        
        for template in templates:
            self.create_template_card(template)
    
    def create_template_card(self, template):
        """Create a template card widget"""
        card_frame = tk.Frame(self.templates_scroll, bg='#f8fafc', relief='solid', bd=1)
        card_frame.pack(fill='x', pady=5)
        
        # Card header
        header_frame = tk.Frame(card_frame, bg='#e5e7eb', height=35)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#e5e7eb')
        header_content.pack(fill='both', expand=True, padx=15, pady=8)
        
        tk.Label(header_content, text=f"{template['icon']} {template['name']}", 
                font=('Segoe UI', 11, 'bold'), bg='#e5e7eb', fg='#374151').pack(side='left')
        
        tk.Label(header_content, text=template['step_type'], 
                font=('Segoe UI', 9), bg='#e5e7eb', fg='#6b7280').pack(side='right')
        
        # Card content
        content_frame = tk.Frame(card_frame, bg='#f8fafc')
        content_frame.pack(fill='x', padx=15, pady=10)
        
        tk.Label(content_frame, text=template['description'], 
                font=('Segoe UI', 10), bg='#f8fafc', fg='#374151', 
                wraplength=400, justify='left').pack(anchor='w', pady=(0, 8))
        
        # Template details
        details_frame = tk.Frame(content_frame, bg='#f8fafc')
        details_frame.pack(fill='x', pady=(0, 10))
        
        if 'target' in template:
            tk.Label(details_frame, text=f"Target: {template['target']}", 
                    font=('Segoe UI', 9, 'italic'), bg='#f8fafc', fg='#6b7280').pack(anchor='w')
        
        if 'value' in template:
            tk.Label(details_frame, text=f"Value: {template['value']}", 
                    font=('Segoe UI', 9, 'italic'), bg='#f8fafc', fg='#6b7280').pack(anchor='w')
        
        # Action buttons
        actions_frame = tk.Frame(content_frame, bg='#f8fafc')
        actions_frame.pack(fill='x')
        
        tk.Button(actions_frame, text="✨ Use Template", font=('Segoe UI', 9, 'bold'),
                 bg='#8b5cf6', fg='#ffffff', relief='flat', padx=12, pady=6,
                 cursor='hand2', bd=0, 
                 command=lambda t=template: self.use_template(t)).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text="👁️ Preview", font=('Segoe UI', 9, 'bold'),
                 bg='#3b82f6', fg='#ffffff', relief='flat', padx=12, pady=6,
                 cursor='hand2', bd=0,
                 command=lambda t=template: self.preview_template(t)).pack(side='left', padx=(0, 8))
        
        tk.Button(actions_frame, text="📝 Customize", font=('Segoe UI', 9, 'bold'),
                 bg='#10b981', fg='#ffffff', relief='flat', padx=12, pady=6,
                 cursor='hand2', bd=0,
                 command=lambda t=template: self.customize_template(t)).pack(side='left')
    
    def filter_templates(self):
        """Filter templates based on search"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            if self.current_category:
                self.load_templates_for_category(self.current_category)
            return
        
        # Clear current display
        for widget in self.templates_scroll.winfo_children():
            widget.destroy()
        
        # Search all categories
        found_templates = []
        for category, templates in self.templates["categories"].items():
            for template in templates:
                if (search_term in template['name'].lower() or 
                    search_term in template['description'].lower() or
                    search_term in template['step_type'].lower()):
                    found_templates.append(template)
        
        if found_templates:
            self.templates_title.config(text=f"Search Results ({len(found_templates)})")
            for template in found_templates:
                self.create_template_card(template)
        else:
            tk.Label(self.templates_scroll, text="No templates found", 
                    font=('Segoe UI', 12), bg='#ffffff', fg='#6b7280').pack(expand=True)
    
    def use_template(self, template):
        """Use template to create step"""
        try:
            # Get rice profile
            rice_profiles = self.db_manager.get_rice_profiles()
            rice_profile_id = rice_profiles[0][0] if rice_profiles else 1
            
            # Create step from template
            step_name = template['name']
            step_type = template['step_type']
            target = template.get('target', '')
            description = template.get('description', '')
            
            # Save to database
            self.db_manager.save_test_step(rice_profile_id, step_name, step_type, target, description, self.group_id)
            
            # Close dialog and refresh
            self.dialog.destroy()
            if self.callback:
                self.callback(self.group_id)
            
            self.show_popup("Success", f"✨ Template '{step_name}' added successfully!", "success")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to use template: {str(e)}", "error")
    
    def preview_template(self, template):
        """Preview template details"""
        preview_dialog = tk.Toplevel(self.dialog)
        preview_dialog.title("👁️ Template Preview")
        preview_dialog.configure(bg='#ffffff')
        preview_dialog.geometry("500x400")
        preview_dialog.transient(self.dialog)
        
        try:
            preview_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(preview_dialog, bg='#3b82f6', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"👁️ {template['name']}", 
                font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(preview_dialog, bg='#ffffff', padx=25, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        # Template details
        details = [
            ("Icon", template['icon']),
            ("Name", template['name']),
            ("Type", template['step_type']),
            ("Description", template['description']),
            ("Target", template.get('target', 'N/A')),
            ("Value", template.get('value', 'N/A'))
        ]
        
        for label, value in details:
            row_frame = tk.Frame(content_frame, bg='#ffffff')
            row_frame.pack(fill='x', pady=5)
            
            tk.Label(row_frame, text=f"{label}:", font=('Segoe UI', 10, 'bold'), 
                    bg='#ffffff', fg='#374151', width=12, anchor='w').pack(side='left')
            tk.Label(row_frame, text=str(value), font=('Segoe UI', 10), 
                    bg='#ffffff', fg='#6b7280', wraplength=300, justify='left').pack(side='left', fill='x', expand=True)
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 11, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10,
                 cursor='hand2', bd=0, command=preview_dialog.destroy).pack(pady=(20, 0))
    
    def customize_template(self, template):
        """Customize template before using"""
        # This would open the enhanced step creation wizard with template pre-filled
        self.show_popup("Feature", "Template customization will open the step creation wizard with pre-filled values", "info")
    
    def create_custom_template(self, parent):
        """Create custom template"""
        self.show_popup("Feature", "Custom template creation coming soon!", "info")
    
    def import_templates(self):
        """Import templates from file"""
        self.show_popup("Feature", "Template import/export coming soon!", "info")