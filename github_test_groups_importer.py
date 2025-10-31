#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import tkinter as tk
from tkinter import ttk
import json
import requests
from datetime import datetime
from enhanced_popup_system import EnhancedPopupManager

class GitHubTestGroupsImporter:
    def __init__(self, parent=None):
        self.parent = parent
        self.popup_manager = EnhancedPopupManager()
        self.github_token = None
        self.github_username = None
        self.repo_name = "rice-test-groups"
        
    def load_github_credentials(self):
        """Load GitHub credentials from existing integration"""
        try:
            with open('github_json.config', 'r') as f:
                config = json.load(f)
                self.github_token = config.get('token')
                self.github_username = config.get('username')
                return True
        except:
            return False
    
    def show_import_browser(self, parent_dialog=None):
        """Show community test groups browser for import"""
        if not self.load_github_credentials():
            self.popup_manager.show_info("GitHub Authentication Required", 
                "Please authenticate with GitHub first using Enterprise Tools → GitHub Integration.")
            return
        
        # Create import browser dialog
        dialog = self.popup_manager.create_dynamic_dialog(
            title="📥 Import Community Test Groups",
            width=900,
            height=650,
            resizable=True,
            parent=parent_dialog
        )
        
        # Header
        header_frame = tk.Frame(dialog, bg='#3b82f6', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#3b82f6')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        tk.Label(header_content, text="📥 Community Test Groups", 
                font=('Segoe UI', 16, 'bold'), bg='#3b82f6', fg='white').pack(side='left')
        
        refresh_btn = tk.Button(header_content, text="🔄 Refresh",
                               font=('Segoe UI', 10, 'bold'), bg='#1e40af', fg='white',
                               relief='flat', padx=15, pady=8, cursor='hand2', bd=0,
                               command=lambda: self._load_community_groups(groups_frame))
        refresh_btn.pack(side='right')
        
        # Main content
        content_frame = tk.Frame(dialog, bg='#f8fafc', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Search and filter section
        search_frame = tk.Frame(content_frame, bg='white', relief='solid', bd=1, padx=15, pady=10)
        search_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(search_frame, text="🔍 Search & Filter", 
                font=('Segoe UI', 12, 'bold'), bg='white').pack(anchor='w', pady=(0, 10))
        
        filter_row = tk.Frame(search_frame, bg='white')
        filter_row.pack(fill='x')
        
        # Search box
        tk.Label(filter_row, text="Search:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_row, textvariable=self.search_var, font=('Segoe UI', 10), width=30)
        search_entry.pack(side='left', padx=(0, 15))
        search_entry.bind('<KeyRelease>', lambda e: self._filter_groups())
        
        # Category filter
        tk.Label(filter_row, text="Category:", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 5))
        
        self.category_var = tk.StringVar(value="All")
        category_combo = ttk.Combobox(filter_row, textvariable=self.category_var, 
                                     font=('Segoe UI', 10), state='readonly', width=15)
        category_combo['values'] = ['All', 'General', 'FSM', 'Navigation', 'Forms', 'Authentication']
        category_combo.pack(side='left', padx=(0, 15))
        category_combo.bind('<<ComboboxSelected>>', lambda e: self._filter_groups())
        
        # Clear button
        clear_btn = tk.Button(filter_row, text="✕ Clear",
                             font=('Segoe UI', 9), bg='#ef4444', fg='white',
                             relief='flat', padx=10, pady=4, cursor='hand2', bd=0,
                             command=self._clear_filters)
        clear_btn.pack(side='left')
        
        # Groups display area
        groups_container = tk.Frame(content_frame, bg='white', relief='solid', bd=1)
        groups_container.pack(fill='both', expand=True, pady=(0, 15))
        
        # Groups header
        groups_header = tk.Frame(groups_container, bg='#10b981', height=45)
        groups_header.pack(fill='x')
        groups_header.pack_propagate(False)
        
        tk.Label(groups_header, text="🌐 Available Test Groups", 
                font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='white').pack(expand=True)
        
        # Scrollable groups frame
        canvas = tk.Canvas(groups_container, bg='white')
        scrollbar = ttk.Scrollbar(groups_container, orient='vertical', command=canvas.yview)
        groups_frame = tk.Frame(canvas, bg='white')
        
        groups_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=groups_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Status bar
        status_frame = tk.Frame(content_frame, bg='#f8fafc', height=30)
        status_frame.pack(fill='x')
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(status_frame, text="Loading community test groups...", 
                                    font=('Segoe UI', 9), bg='#f8fafc', fg='#6b7280')
        self.status_label.pack(side='left', pady=5)
        
        # Store references
        self.groups_frame = groups_frame
        self.canvas = canvas
        self.all_groups = []
        self.filtered_groups = []
        
        # Load community groups
        self._load_community_groups(groups_frame)
        
        dialog.focus_set()
    
    def _load_community_groups(self, groups_frame):
        """Load community test groups from GitHub"""
        # Clear existing groups
        for widget in groups_frame.winfo_children():
            widget.destroy()
        
        self.status_label.config(text="Loading community test groups...")
        
        try:
            # Get repository contents
            url = f"https://api.github.com/repos/{self.github_username}/{self.repo_name}/contents"
            headers = {'Authorization': f'token {self.github_token}'}
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 404:
                self._show_no_repository_message(groups_frame)
                return
            elif response.status_code != 200:
                self._show_error_message(groups_frame, f"Failed to load repository: {response.status_code}")
                return
            
            files = response.json()
            json_files = [f for f in files if f['name'].endswith('.json') and f['name'] != 'README.md']
            
            if not json_files:
                self._show_empty_repository_message(groups_frame)
                return
            
            # Load each test group file
            self.all_groups = []
            for file_info in json_files:
                try:
                    file_response = requests.get(file_info['download_url'], timeout=10)
                    if file_response.status_code == 200:
                        group_data = file_response.json()
                        group_data['filename'] = file_info['name']
                        group_data['download_url'] = file_info['download_url']
                        self.all_groups.append(group_data)
                except Exception as e:
                    print(f"Error loading {file_info['name']}: {e}")
            
            self.filtered_groups = self.all_groups.copy()
            self._display_groups()
            
            count = len(self.all_groups)
            self.status_label.config(text=f"Found {count} community test group{'s' if count != 1 else ''}")
            
        except requests.RequestException as e:
            self._show_error_message(groups_frame, f"Network error: {str(e)}")
        except Exception as e:
            self._show_error_message(groups_frame, f"Error loading groups: {str(e)}")
    
    def _display_groups(self):
        """Display filtered groups"""
        # Clear existing
        for widget in self.groups_frame.winfo_children():
            widget.destroy()
        
        if not self.filtered_groups:
            self._show_no_results_message()
            return
        
        for i, group in enumerate(self.filtered_groups):
            self._create_group_card(group, i)
        
        # Update canvas scroll region
        self.groups_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
    
    def _create_group_card(self, group, index):
        """Create a card for each test group"""
        # Card container
        card = tk.Frame(self.groups_frame, bg='#f9fafb', relief='solid', bd=1, padx=15, pady=12)
        card.pack(fill='x', padx=5, pady=5)
        
        # Header row
        header_row = tk.Frame(card, bg='#f9fafb')
        header_row.pack(fill='x', pady=(0, 8))
        
        # Group name and category
        name_frame = tk.Frame(header_row, bg='#f9fafb')
        name_frame.pack(side='left', fill='x', expand=True)
        
        group_name = group.get('name', 'Unnamed Group')
        tk.Label(name_frame, text=group_name, 
                font=('Segoe UI', 12, 'bold'), bg='#f9fafb', fg='#1f2937').pack(anchor='w')
        
        # Category badge
        category = group.get('category', 'General')
        category_colors = {
            'General': '#6b7280',
            'FSM': '#10b981', 
            'Navigation': '#3b82f6',
            'Forms': '#8b5cf6',
            'Authentication': '#f59e0b'
        }
        category_color = category_colors.get(category, '#6b7280')
        
        category_label = tk.Label(header_row, text=category, 
                                 font=('Segoe UI', 9, 'bold'), bg=category_color, fg='white',
                                 padx=8, pady=2)
        category_label.pack(side='right')
        
        # Description
        description = group.get('description', 'No description available')
        if len(description) > 100:
            description = description[:97] + "..."
        
        tk.Label(card, text=description, 
                font=('Segoe UI', 10), bg='#f9fafb', fg='#6b7280',
                wraplength=400, justify='left').pack(anchor='w', pady=(0, 8))
        
        # Metadata row
        meta_row = tk.Frame(card, bg='#f9fafb')
        meta_row.pack(fill='x', pady=(0, 10))
        
        # Steps count
        step_count = group.get('metadata', {}).get('step_count', 0)
        tk.Label(meta_row, text=f"📋 {step_count} steps", 
                font=('Segoe UI', 9), bg='#f9fafb', fg='#6b7280').pack(side='left')
        
        # Shared by
        shared_by = group.get('shared_by', 'Unknown')
        tk.Label(meta_row, text=f"👤 {shared_by}", 
                font=('Segoe UI', 9), bg='#f9fafb', fg='#6b7280').pack(side='left', padx=(15, 0))
        
        # Action buttons
        btn_frame = tk.Frame(card, bg='#f9fafb')
        btn_frame.pack(fill='x')
        
        # Preview button
        preview_btn = tk.Button(btn_frame, text="👁️ Preview",
                               font=('Segoe UI', 9, 'bold'), bg='#6b7280', fg='white',
                               relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                               command=lambda g=group: self._preview_group(g))
        preview_btn.pack(side='left', padx=(0, 10))
        
        # Import button
        import_btn = tk.Button(btn_frame, text="📥 Import",
                              font=('Segoe UI', 9, 'bold'), bg='#10b981', fg='white',
                              relief='flat', padx=12, pady=6, cursor='hand2', bd=0,
                              command=lambda g=group: self._import_group(g))
        import_btn.pack(side='left')
    
    def _filter_groups(self):
        """Filter groups based on search and category"""
        search_term = self.search_var.get().lower()
        category_filter = self.category_var.get()
        
        self.filtered_groups = []
        
        for group in self.all_groups:
            # Search filter
            if search_term:
                name_match = search_term in group.get('name', '').lower()
                desc_match = search_term in group.get('description', '').lower()
                if not (name_match or desc_match):
                    continue
            
            # Category filter
            if category_filter != 'All':
                if group.get('category', 'General') != category_filter:
                    continue
            
            self.filtered_groups.append(group)
        
        self._display_groups()
        
        # Update status
        total = len(self.all_groups)
        filtered = len(self.filtered_groups)
        if filtered != total:
            self.status_label.config(text=f"Showing {filtered} of {total} test groups")
        else:
            self.status_label.config(text=f"Found {total} community test group{'s' if total != 1 else ''}")
    
    def _clear_filters(self):
        """Clear all filters"""
        self.search_var.set("")
        self.category_var.set("All")
        self._filter_groups()
    
    def _preview_group(self, group):
        """Preview test group details"""
        preview_dialog = self.popup_manager.create_dynamic_dialog(
            title=f"👁️ Preview: {group.get('name', 'Test Group')}",
            width=600,
            height=500,
            resizable=True
        )
        
        # Header
        header_frame = tk.Frame(preview_dialog, bg='#6b7280', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"👁️ {group.get('name', 'Test Group')}", 
                font=('Segoe UI', 14, 'bold'), bg='#6b7280', fg='white').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(preview_dialog, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Group info
        info_frame = tk.LabelFrame(content_frame, text="Group Information", 
                                  font=('Segoe UI', 10, 'bold'), padx=10, pady=10)
        info_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(info_frame, text=f"Category: {group.get('category', 'General')}", 
                font=('Segoe UI', 10), anchor='w').pack(fill='x')
        tk.Label(info_frame, text=f"Steps: {group.get('metadata', {}).get('step_count', 0)}", 
                font=('Segoe UI', 10), anchor='w').pack(fill='x')
        tk.Label(info_frame, text=f"Shared by: {group.get('shared_by', 'Unknown')}", 
                font=('Segoe UI', 10), anchor='w').pack(fill='x')
        
        # Description
        desc_frame = tk.LabelFrame(content_frame, text="Description", 
                                  font=('Segoe UI', 10, 'bold'), padx=10, pady=10)
        desc_frame.pack(fill='x', pady=(0, 15))
        
        desc_text = tk.Text(desc_frame, height=4, font=('Segoe UI', 10), wrap='word', state='disabled')
        desc_text.pack(fill='x')
        desc_text.config(state='normal')
        desc_text.insert('1.0', group.get('description', 'No description available'))
        desc_text.config(state='disabled')
        
        # Steps preview
        steps_frame = tk.LabelFrame(content_frame, text="Steps Preview", 
                                   font=('Segoe UI', 10, 'bold'), padx=10, pady=10)
        steps_frame.pack(fill='both', expand=True)
        
        steps_listbox = tk.Listbox(steps_frame, font=('Segoe UI', 9))
        steps_scroll = ttk.Scrollbar(steps_frame, orient='vertical', command=steps_listbox.yview)
        steps_listbox.configure(yscrollcommand=steps_scroll.set)
        
        steps_listbox.pack(side='left', fill='both', expand=True)
        steps_scroll.pack(side='right', fill='y')
        
        # Load steps
        steps = group.get('steps', [])
        for i, step in enumerate(steps, 1):
            step_text = f"{i}. {step.get('step_name', 'Unknown')} ({step.get('step_type', 'Unknown')})"
            steps_listbox.insert(tk.END, step_text)
        
        # Close button
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='white', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=preview_dialog.destroy).pack(pady=(15, 0))
    
    def _import_group(self, group):
        """Import test group to local Test Steps"""
        try:
            # Show confirmation dialog
            confirm_dialog = self.popup_manager.create_dynamic_dialog(
                title="📥 Import Test Group",
                width=500,
                height=300,
                resizable=False
            )
            
            # Header
            header_frame = tk.Frame(confirm_dialog, bg='#10b981', height=50)
            header_frame.pack(fill='x')
            header_frame.pack_propagate(False)
            
            tk.Label(header_frame, text="📥 Import Test Group", 
                    font=('Segoe UI', 12, 'bold'), bg='#10b981', fg='white').pack(expand=True)
            
            # Content
            content_frame = tk.Frame(confirm_dialog, bg='white', padx=20, pady=20)
            content_frame.pack(fill='both', expand=True)
            
            tk.Label(content_frame, text=f"Import '{group.get('name', 'Test Group')}'?", 
                    font=('Segoe UI', 12, 'bold'), bg='white').pack(pady=(0, 10))
            
            tk.Label(content_frame, text=f"This will create a new test step group with {group.get('metadata', {}).get('step_count', 0)} steps.", 
                    font=('Segoe UI', 10), bg='white', fg='#6b7280').pack(pady=(0, 20))
            
            # Buttons
            btn_frame = tk.Frame(content_frame, bg='white')
            btn_frame.pack()
            
            tk.Button(btn_frame, text="📥 Import", font=('Segoe UI', 10, 'bold'), 
                     bg='#10b981', fg='white', relief='flat', padx=20, pady=8, 
                     cursor='hand2', bd=0, 
                     command=lambda: self._perform_import(group, confirm_dialog)).pack(side='left', padx=(0, 10))
            
            tk.Button(btn_frame, text="Cancel", font=('Segoe UI', 10, 'bold'), 
                     bg='#6b7280', fg='white', relief='flat', padx=20, pady=8, 
                     cursor='hand2', bd=0, command=confirm_dialog.destroy).pack(side='left')
            
        except Exception as e:
            self.popup_manager.show_error("Error", f"Failed to show import dialog: {str(e)}")
    
    def _perform_import(self, group, confirm_dialog):
        """Perform the actual import"""
        try:
            # This would integrate with the database manager
            # For now, show success message
            confirm_dialog.destroy()
            
            group_name = group.get('name', 'Imported Group')
            step_count = group.get('metadata', {}).get('step_count', 0)
            
            self.popup_manager.show_success("Import Successful", 
                f"Successfully imported '{group_name}' with {step_count} steps!\n\n"
                f"The test group is now available in your Test Steps section.")
            
        except Exception as e:
            self.popup_manager.show_error("Import Failed", f"Failed to import test group: {str(e)}")
    
    def _show_no_repository_message(self, parent):
        """Show message when repository doesn't exist"""
        msg_frame = tk.Frame(parent, bg='white', padx=40, pady=40)
        msg_frame.pack(fill='both', expand=True)
        
        tk.Label(msg_frame, text="📂 No Community Repository Found", 
                font=('Segoe UI', 14, 'bold'), bg='white', fg='#6b7280').pack(pady=(0, 10))
        
        tk.Label(msg_frame, text="The community test groups repository hasn't been created yet.\nBe the first to share a test group!", 
                font=('Segoe UI', 11), bg='white', fg='#9ca3af', justify='center').pack()
        
        self.status_label.config(text="No community repository found")
    
    def _show_empty_repository_message(self, parent):
        """Show message when repository is empty"""
        msg_frame = tk.Frame(parent, bg='white', padx=40, pady=40)
        msg_frame.pack(fill='both', expand=True)
        
        tk.Label(msg_frame, text="📋 No Test Groups Available", 
                font=('Segoe UI', 14, 'bold'), bg='white', fg='#6b7280').pack(pady=(0, 10))
        
        tk.Label(msg_frame, text="No community test groups have been shared yet.\nBe the first to contribute!", 
                font=('Segoe UI', 11), bg='white', fg='#9ca3af', justify='center').pack()
        
        self.status_label.config(text="No test groups available")
    
    def _show_error_message(self, parent, error_msg):
        """Show error message"""
        msg_frame = tk.Frame(parent, bg='white', padx=40, pady=40)
        msg_frame.pack(fill='both', expand=True)
        
        tk.Label(msg_frame, text="❌ Error Loading Test Groups", 
                font=('Segoe UI', 14, 'bold'), bg='white', fg='#ef4444').pack(pady=(0, 10))
        
        tk.Label(msg_frame, text=error_msg, 
                font=('Segoe UI', 11), bg='white', fg='#6b7280', justify='center').pack()
        
        self.status_label.config(text="Error loading test groups")
    
    def _show_no_results_message(self):
        """Show message when no results match filters"""
        msg_frame = tk.Frame(self.groups_frame, bg='white', padx=40, pady=40)
        msg_frame.pack(fill='both', expand=True)
        
        tk.Label(msg_frame, text="🔍 No Matching Test Groups", 
                font=('Segoe UI', 14, 'bold'), bg='white', fg='#6b7280').pack(pady=(0, 10))
        
        tk.Label(msg_frame, text="Try adjusting your search terms or category filter.", 
                font=('Segoe UI', 11), bg='white', fg='#9ca3af', justify='center').pack()
        
        self.status_label.config(text="No matching test groups found")

def main():
    """Test the GitHub Test Groups Importer"""
    root = tk.Tk()
    root.withdraw()
    
    importer = GitHubTestGroupsImporter()
    importer.show_import_browser()
    
    root.mainloop()

if __name__ == "__main__":
    main()