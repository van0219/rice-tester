#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import tkinter as tk
from tkinter import ttk, messagebox
import json
import sqlite3
from datetime import datetime
import requests
import base64
from enhanced_popup_system import EnhancedPopupManager

class GitHubTestGroupsManager:
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
    
    def share_test_group(self, test_group_id):
        """Share a test group to GitHub community repository"""
        if not self.load_github_credentials():
            self.popup_manager.show_info("GitHub Authentication Required", 
                                       "Please authenticate with GitHub first using Enterprise Tools.")
            return
        
        # Get test group data
        test_group_data = self.get_test_group_data(test_group_id)
        if not test_group_data:
            self.popup_manager.show_error("Error", "Failed to load test group data.")
            return
        
        # Show sharing dialog
        self.show_sharing_dialog(test_group_data)
    
    def get_test_group_data(self, test_group_id):
        """Get test group data from database"""
        try:
            conn = sqlite3.connect('fsm_tester.db')
            cursor = conn.cursor()
            
            # Get test group info from test_step_groups table
            cursor.execute("SELECT id, group_name, description FROM test_step_groups WHERE id = ?", (test_group_id,))
            group = cursor.fetchone()
            if not group:
                return None
            
            # Get test steps in group from test_steps table
            cursor.execute("""
                SELECT id, name, step_type, target, description
                FROM test_steps 
                WHERE group_id = ?
                ORDER BY COALESCE(step_order, id)
            """, (test_group_id,))
            steps = cursor.fetchall()
            
            conn.close()
            
            # Format data for sharing
            return {
                'name': group[1],  # group_name
                'description': group[2] or '',  # description
                'category': 'General',  # default category
                'created_date': datetime.now().isoformat(),
                'shared_by': self.github_username,
                'steps': [self.format_step_data(step) for step in steps],
                'metadata': {
                    'version': '1.0',
                    'rice_tester_version': '2.0',
                    'step_count': len(steps)
                }
            }
        except Exception as e:
            print(f"Error getting test group data: {e}")
            return None
    
    def format_step_data(self, step):
        """Format step data for JSON export"""
        # step format: (id, name, step_type, target, description)
        return {
            'step_name': step[1] or 'Unnamed Step',
            'step_type': step[2] or 'Unknown',
            'target': step[3] or '',
            'description': step[4] or '',
            'step_order': step[0]  # Use ID as order for now
        }
    
    def show_sharing_dialog(self, test_group_data):
        """Show dialog for sharing test group"""
        dialog = self.popup_manager.create_dynamic_dialog(
            title="🌐 Share Test Group",
            width=500,
            height=400,
            resizable=True
        )
        
        # Header
        header_frame = tk.Frame(dialog, bg='#10b981', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="Share with Community", 
                              font=('Segoe UI', 14, 'bold'), 
                              bg='#10b981', fg='white')
        title_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Test group info
        info_frame = tk.LabelFrame(content_frame, text="Test Group Information", 
                                  font=('Segoe UI', 10, 'bold'), padx=10, pady=10)
        info_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(info_frame, text=f"Name: {test_group_data['name']}", 
                font=('Segoe UI', 9)).pack(anchor='w')
        tk.Label(info_frame, text=f"Steps: {test_group_data['metadata']['step_count']}", 
                font=('Segoe UI', 9)).pack(anchor='w')
        tk.Label(info_frame, text=f"Category: {test_group_data['category']}", 
                font=('Segoe UI', 9)).pack(anchor='w')
        
        # Description
        desc_frame = tk.LabelFrame(content_frame, text="Description (Optional)", 
                                  font=('Segoe UI', 10, 'bold'), padx=10, pady=10)
        desc_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        desc_text = tk.Text(desc_frame, height=4, font=('Segoe UI', 9), wrap='word')
        desc_text.pack(fill='both', expand=True)
        desc_text.insert('1.0', test_group_data['description'])
        
        # Buttons
        button_frame = tk.Frame(content_frame)
        button_frame.pack(fill='x')
        
        cancel_btn = tk.Button(button_frame, text="Cancel", 
                              command=dialog.destroy,
                              font=('Segoe UI', 9), padx=20, pady=8)
        cancel_btn.pack(side='right', padx=(10, 0))
        
        share_btn = tk.Button(button_frame, text="🌐 Share to Community", 
                             bg='#10b981', fg='white', font=('Segoe UI', 9, 'bold'),
                             padx=20, pady=8,
                             command=lambda: self.upload_to_github(test_group_data, desc_text.get('1.0', 'end-1c'), dialog))
        share_btn.pack(side='right')
        
        dialog.focus_set()
    
    def upload_to_github(self, test_group_data, description, dialog):
        """Upload test group to GitHub repository"""
        try:
            # Update description
            test_group_data['description'] = description.strip()
            
            # Create repository if it doesn't exist
            if not self.ensure_repository_exists():
                return
            
            # Create filename
            safe_name = "".join(c for c in test_group_data['name'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
            filename = f"{safe_name.replace(' ', '_')}.json"
            
            # Upload file
            success = self.upload_file_to_repo(filename, json.dumps(test_group_data, indent=2))
            
            if success:
                dialog.destroy()
                self.popup_manager.show_success("Success!", 
                    f"Test group '{test_group_data['name']}' shared successfully!\n\n"
                    f"Repository: {self.github_username}/{self.repo_name}\n"
                    f"File: {filename}")
            else:
                self.popup_manager.show_error("Upload Failed", 
                    "Failed to upload test group. Please check your connection and try again.")
                
        except Exception as e:
            self.popup_manager.show_error("Error", f"Upload failed: {str(e)}")
    
    def ensure_repository_exists(self):
        """Ensure the test groups repository exists"""
        try:
            # Check if repo exists
            url = f"https://api.github.com/repos/{self.github_username}/{self.repo_name}"
            headers = {'Authorization': f'token {self.github_token}'}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                # Create repository
                return self.create_repository()
            else:
                self.popup_manager.show_error("Error", f"Failed to check repository: {response.status_code}")
                return False
                
        except Exception as e:
            self.popup_manager.show_error("Error", f"Repository check failed: {str(e)}")
            return False
    
    def create_repository(self):
        """Create the test groups repository"""
        try:
            url = "https://api.github.com/user/repos"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'name': self.repo_name,
                'description': 'Community shared test groups for RICE Tester - FSM testing patterns',
                'public': True,
                'auto_init': True
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                # Create README
                self.create_readme()
                return True
            else:
                self.popup_manager.show_error("Error", f"Failed to create repository: {response.status_code}")
                return False
                
        except Exception as e:
            self.popup_manager.show_error("Error", f"Repository creation failed: {str(e)}")
            return False
    
    def create_readme(self):
        """Create README for the repository"""
        readme_content = """# RICE Tester - Community Test Groups

This repository contains shared test groups for the RICE Tester application, enabling Infor consultants to share FSM testing patterns across teams.

## About RICE Tester

RICE Tester is an enterprise FSM (Financials and Supply Management) testing suite that automates business process testing in Infor environments.

## Test Group Format

Each test group is stored as a JSON file containing:
- Test group metadata (name, description, category)
- Step definitions with selectors and actions
- Version information for compatibility

## Usage

1. Download test group JSON files
2. Import into your RICE Tester application
3. Customize for your environment
4. Share your own test patterns with the community

## Contributing

Share your test groups by using the "🌐 Share" button in RICE Tester's Test Groups section.

---
*Generated by RICE Tester - Enterprise FSM Testing Suite*
"""
        
        try:
            self.upload_file_to_repo("README.md", readme_content)
        except:
            pass  # README creation is optional
    
    def upload_file_to_repo(self, filename, content):
        """Upload file to GitHub repository"""
        try:
            url = f"https://api.github.com/repos/{self.github_username}/{self.repo_name}/contents/{filename}"
            headers = {
                'Authorization': f'token {self.github_token}',
                'Content-Type': 'application/json'
            }
            
            # Check if file exists
            response = requests.get(url, headers=headers)
            sha = None
            if response.status_code == 200:
                sha = response.json()['sha']
            
            # Upload file
            data = {
                'message': f'Add test group: {filename}',
                'content': base64.b64encode(content.encode()).decode(),
                'branch': 'main'
            }
            
            if sha:
                data['sha'] = sha
            
            response = requests.put(url, headers=headers, json=data)
            return response.status_code in [200, 201]
            
        except Exception as e:
            print(f"Upload error: {e}")
            return False

def main():
    """Test the GitHub Test Groups Manager"""
    root = tk.Tk()
    root.withdraw()
    
    manager = GitHubTestGroupsManager()
    
    # Test with dummy data
    test_data = {
        'name': 'Sample Test Group',
        'description': 'A sample test group for demonstration',
        'category': 'General',
        'steps': [],
        'metadata': {'step_count': 0}
    }
    
    manager.show_sharing_dialog(test_data)
    root.mainloop()

if __name__ == "__main__":
    main()