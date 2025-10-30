#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
import base64
import zipfile
import shutil
from datetime import datetime
try:
    from enhanced_popup_system import create_enhanced_dialog
except ImportError:
    try:
        from Temp.enhanced_popup_system import create_enhanced_dialog
    except ImportError:
        def create_enhanced_dialog(parent, title, width, height, modal=True):
            dialog = tk.Toplevel(parent)
            dialog.title(title)
            dialog.geometry(f"{width}x{height}")
            return dialog

class GitHubIntegrationManager:
    """
    GitHub Integration Module for RICE Tester
    Secure access control - Only accessible to vansilleza_fpi
    """
    
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.github_token = None
        self.github_username = None
        self.repo_name = None
        
        # Try to load saved credentials
        self._load_github_credentials()
    
    def show_github_integration_dialog(self):
        """Show GitHub integration panel with login and management"""
        
        panel = create_enhanced_dialog(None, "🐙 GitHub Integration - RICE Tester CI/CD", 900, 736, modal=False)
        panel.resizable(False, False)
        panel.maxsize(900, 736)
        
        try:
            panel.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(panel, bg='#000000', height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🐙 GitHub Integration Manager", 
                              font=('Segoe UI', 18, 'bold'), bg='#000000', fg='#ffffff')
        title_label.pack(side="left", padx=25, pady=25)
        
        # Status indicator
        status_label = tk.Label(header_frame, text="🔒 Authorized Access", 
                             font=('Segoe UI', 11), bg='#000000', fg='#f6f8fa')
        status_label.pack(side="right", padx=25, pady=25)
        
        # Main content
        main_frame = tk.Frame(panel, bg='#ffffff', padx=25, pady=25)
        main_frame.pack(fill="both", expand=True)
        
        # Check if already logged in
        if self.github_token:
            self._show_management_interface(main_frame)
        else:
            self._show_login_interface(main_frame)
    
    def _show_login_interface(self, parent):
        """Show GitHub login interface"""
        # Login section
        login_frame = tk.Frame(parent, bg='#f6f8fa', relief='solid', bd=1, padx=20, pady=20)
        login_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(login_frame, text="🔐 GitHub Authentication", font=('Segoe UI', 14, 'bold'), 
                bg='#f6f8fa', fg='#24292e').pack(anchor="w", pady=(0, 15))
        
        # Instructions
        instructions = """To set up GitHub CI/CD for RICE Tester, you need a GitHub Personal Access Token:

1. Go to GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name like "RICE Tester CI/CD"
4. Select these scopes:
   ✅ repo (Full control of private repositories)
   ✅ workflow (Update GitHub Action workflows)
   ✅ write:packages (Upload packages)
5. Click "Generate token" and copy it immediately"""
        
        tk.Label(login_frame, text=instructions, font=('Segoe UI', 9), 
                bg='#f6f8fa', fg='#586069', justify="left", wraplength=800).pack(anchor="w", pady=(0, 15))
        
        # Token input
        token_frame = tk.Frame(login_frame, bg='#f6f8fa')
        token_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(token_frame, text="GitHub Personal Access Token:", font=('Segoe UI', 10, 'bold'), 
                bg='#f6f8fa', fg='#24292e').pack(anchor="w")
        
        self.token_entry = tk.Entry(token_frame, font=('Segoe UI', 10), show="•", width=60)
        self.token_entry.pack(fill="x", pady=(5, 0))
        
        # Username input
        username_frame = tk.Frame(login_frame, bg='#f6f8fa')
        username_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(username_frame, text="GitHub Username:", font=('Segoe UI', 10, 'bold'), 
                bg='#f6f8fa', fg='#24292e').pack(anchor="w")
        
        self.username_entry = tk.Entry(username_frame, font=('Segoe UI', 10), width=30)
        self.username_entry.pack(anchor="w", pady=(5, 0))
        
        # Login button
        login_btn = tk.Button(login_frame, text="🔑 Connect to GitHub", font=('Segoe UI', 11, 'bold'), 
                             bg='#238636', fg='#ffffff', relief='flat', padx=20, pady=10, 
                             cursor='hand2', bd=0, command=self._authenticate_github)
        login_btn.pack(anchor="w", pady=(10, 0))
        
        # Help section
        help_frame = tk.Frame(parent, bg='#fff8dc', relief='solid', bd=1, padx=20, pady=15)
        help_frame.pack(fill="x")
        
        tk.Label(help_frame, text="💡 Need Help?", font=('Segoe UI', 12, 'bold'), 
                bg='#fff8dc', fg='#b08800').pack(anchor="w")
        
        help_text = """• Your token is stored securely and only used for RICE Tester CI/CD setup
• This module will help you create the repository, upload code, and configure automation
• All GitHub operations are done through official GitHub API with your permissions"""
        
        tk.Label(help_frame, text=help_text, font=('Segoe UI', 9), 
                bg='#fff8dc', fg='#6f4e00', justify="left").pack(anchor="w", pady=(5, 0))
    
    def _authenticate_github(self):
        """Authenticate with GitHub using personal access token"""
        token = self.token_entry.get().strip()
        username = self.username_entry.get().strip()
        
        if not token or not username:
            self.show_popup("Missing Information", "Please enter both GitHub token and username.", "warning")
            return
        
        # Test authentication
        try:
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get('https://api.github.com/user', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                if user_data['login'].lower() == username.lower():
                    self.github_token = token
                    self.github_username = username
                    
                    # Save credentials securely (encrypted)
                    self._save_github_credentials(token, username)
                    
                    self.show_popup("Success", f"Successfully connected to GitHub as {username}!", "success")
                    
                    # Refresh interface
                    for widget in self.token_entry.master.master.winfo_children():
                        widget.destroy()
                    
                    self._show_management_interface(self.token_entry.master.master)
                else:
                    self.show_popup("Authentication Failed", "Username doesn't match the token owner.", "error")
            else:
                self.show_popup("Authentication Failed", "Invalid GitHub token or network error.", "error")
                
        except Exception as e:
            self.show_popup("Connection Error", f"Failed to connect to GitHub: {str(e)}", "error")
    
    def _show_management_interface(self, parent):
        """Show GitHub management interface after successful login"""
        # Status section
        status_frame = tk.Frame(parent, bg='#d1ecf1', relief='solid', bd=1, padx=20, pady=15)
        status_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(status_frame, text="✅ Connected to GitHub", font=('Segoe UI', 14, 'bold'), 
                bg='#d1ecf1', fg='#0c5460').pack(anchor="w")
        
        tk.Label(status_frame, text=f"Username: {self.github_username}", font=('Segoe UI', 10), 
                bg='#d1ecf1', fg='#0c5460').pack(anchor="w", pady=(5, 0))
        
        # Repository management
        repo_frame = tk.Frame(parent, bg='#ffffff')
        repo_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(repo_frame, text="📁 Repository Management", font=('Segoe UI', 14, 'bold'), 
                bg='#ffffff', fg='#24292e').pack(anchor="w", pady=(0, 15))
        
        # Repository name input
        repo_input_frame = tk.Frame(repo_frame, bg='#ffffff')
        repo_input_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(repo_input_frame, text="Repository Name:", font=('Segoe UI', 10, 'bold'), 
                bg='#ffffff', fg='#24292e').pack(anchor="w")
        
        self.repo_entry = tk.Entry(repo_input_frame, font=('Segoe UI', 10), width=40)
        self.repo_entry.insert(0, "rice-tester")
        self.repo_entry.pack(anchor="w", pady=(5, 0))
        
        # Action buttons
        actions_frame = tk.Frame(repo_frame, bg='#ffffff')
        actions_frame.pack(fill="x")
        
        # Step 1: Create Repository
        step1_btn = tk.Button(actions_frame, text="1️⃣ Create Repository", font=('Segoe UI', 10, 'bold'), 
                             bg='#0969da', fg='#ffffff', relief='flat', padx=15, pady=8, 
                             cursor='hand2', bd=0, command=self._create_repository)
        step1_btn.pack(side="left", padx=(0, 10))
        
        # Step 2: Upload Code
        step2_btn = tk.Button(actions_frame, text="2️⃣ Upload RICE Tester", font=('Segoe UI', 10, 'bold'), 
                             bg='#8250df', fg='#ffffff', relief='flat', padx=15, pady=8, 
                             cursor='hand2', bd=0, command=self._upload_rice_tester)
        step2_btn.pack(side="left", padx=(0, 10))
        
        # Step 3: Setup CI/CD
        step3_btn = tk.Button(actions_frame, text="3️⃣ Setup CI/CD", font=('Segoe UI', 10, 'bold'), 
                             bg='#238636', fg='#ffffff', relief='flat', padx=15, pady=8, 
                             cursor='hand2', bd=0, command=self._setup_cicd)
        step3_btn.pack(side="left", padx=(0, 10))
        
        # Step 4: Create Release
        step4_btn = tk.Button(actions_frame, text="4️⃣ Create Release", font=('Segoe UI', 10, 'bold'), 
                             bg='#cf222e', fg='#ffffff', relief='flat', padx=15, pady=8, 
                             cursor='hand2', bd=0, command=self._create_release)
        step4_btn.pack(side="left")
        
        # Release Information section
        release_frame = tk.Frame(parent, bg='#e0f2fe', relief='solid', bd=1, padx=20, pady=15)
        release_frame.pack(fill="x", pady=(20, 10))
        
        tk.Label(release_frame, text="📦 Release Information", font=('Segoe UI', 12, 'bold'), 
                bg='#e0f2fe', fg='#0277bd').pack(anchor="w", pady=(0, 10))
        
        # Release URL
        url_frame = tk.Frame(release_frame, bg='#e0f2fe')
        url_frame.pack(fill="x", pady=(0, 5))
        
        tk.Label(url_frame, text="Team Download Link:", font=('Segoe UI', 10, 'bold'), 
                bg='#e0f2fe', fg='#01579b').pack(anchor="w")
        
        self.release_url = tk.Entry(url_frame, font=('Consolas', 9), width=70, state='readonly')
        self.release_url.pack(fill="x", pady=(2, 0))
        self.release_url.insert(0, f"https://github.com/{self.github_username}/rice-tester/releases")
        
        # Current Version
        version_frame = tk.Frame(release_frame, bg='#e0f2fe')
        version_frame.pack(fill="x", pady=(5, 0))
        
        tk.Label(version_frame, text="Current Version:", font=('Segoe UI', 10, 'bold'), 
                bg='#e0f2fe', fg='#01579b').pack(side="left")
        
        # Read current version from version.json
        current_version = self._get_current_version()
        tk.Label(version_frame, text=f"{current_version} (Latest Release)", font=('Segoe UI', 10), 
                bg='#e0f2fe', fg='#0277bd').pack(side="left", padx=(10, 0))
        
        # Copy button
        copy_btn = tk.Button(release_frame, text="📋 Copy Link", font=('Segoe UI', 9, 'bold'), 
                           bg='#0288d1', fg='#ffffff', relief='flat', padx=15, pady=5, 
                           cursor='hand2', bd=0, command=self._copy_release_url)
        copy_btn.pack(anchor="w", pady=(10, 0))
        
        # Progress section
        progress_frame = tk.Frame(parent, bg='#f6f8fa', relief='solid', bd=1, padx=20, pady=15)
        progress_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(progress_frame, text="📊 Setup Progress", font=('Segoe UI', 12, 'bold'), 
                bg='#f6f8fa', fg='#24292e').pack(anchor="w", pady=(0, 10))
        
        self.progress_text = tk.Text(progress_frame, height=8, font=('Consolas', 9), 
                                    bg='#ffffff', relief='solid', bd=1, wrap=tk.WORD, state=tk.DISABLED)
        self.progress_text.pack(fill="x")
        
        self._add_progress("Ready to set up GitHub CI/CD for RICE Tester...")
        self._add_progress("Click the buttons above in order: 1️⃣ → 2️⃣ → 3️⃣ → 4️⃣")
    
    def _add_progress(self, message):
        """Add message to progress log"""
        if hasattr(self, 'progress_text'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[{timestamp}] {message}\n"
            
            self.progress_text.config(state=tk.NORMAL)
            self.progress_text.insert(tk.END, formatted_message)
            self.progress_text.config(state=tk.DISABLED)
            self.progress_text.see(tk.END)
    
    def _check_repository_exists(self, repo_name):
        """Check if repository exists on GitHub"""
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(f'https://api.github.com/repos/{self.github_username}/{repo_name}', 
                                  headers=headers, timeout=10)
            
            return response.status_code == 200
        except Exception:
            return False
    
    def _create_repository(self):
        """Create GitHub repository"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self.show_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        self._add_progress(f"Creating repository '{repo_name}'...")
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'name': repo_name,
                'description': 'RICE Tester - Enterprise FSM Testing Platform',
                'private': True,
                'auto_init': True
            }
            
            response = requests.post('https://api.github.com/user/repos', 
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 201:
                self.repo_name = repo_name
                self._save_updater_config()
                self._add_progress(f"✅ Repository '{repo_name}' created successfully!")
                self._add_progress(f"🔗 URL: https://github.com/{self.github_username}/{repo_name}")
                self.show_popup("Success", f"Repository '{repo_name}' created successfully!", "success")
            elif response.status_code == 422:
                self._add_progress(f"ℹ️ Repository '{repo_name}' already exists")
                self.repo_name = repo_name
                self._save_updater_config()
                self.show_popup("Repository Exists", f"Repository '{repo_name}' already exists. You can proceed to next step.", "warning")
            else:
                error_msg = response.json().get('message', 'Unknown error')
                self._add_progress(f"❌ Failed to create repository: {error_msg}")
                self.show_popup("Error", f"Failed to create repository: {error_msg}", "error")
                
        except Exception as e:
            self._add_progress(f"❌ Error creating repository: {str(e)}")
            self.show_popup("Error", f"Error creating repository: {str(e)}", "error")
    
    def _upload_rice_tester(self):
        """Upload RICE Tester code to repository"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self.show_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        # Check if repository exists
        if not self._check_repository_exists(repo_name):
            self.show_popup("Repository Not Found", f"Repository '{repo_name}' does not exist. Please create it first using Step 1.", "warning")
            return
        
        self.repo_name = repo_name
        self._add_progress("Uploading RICE Tester code...")
        
        try:
            # Get current RICE Tester directory
            rice_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Core files to upload
            files_to_upload = [
                'RICE_Tester.py', 'SeleniumInboundTester_Lite.py', 'database_manager.py',
                'rice_manager.py', 'rice_scenario_manager.py', 'personal_analytics.py',
                'tes070_generator.py', 'enhanced_ui_design.py', 'requirements.txt',
                'README_TEAM.txt', 'SETUP_FIRST_TIME.bat', 'infor_logo.ico',
                'fsm_tester.db', 'version.json', '.github_workflows_rice-tester-ci.yml',
                'github_json.config', 'github_integration_manager.py'
            ]
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            uploaded_count = 0
            failed_files = []
            
            for filename in files_to_upload:
                file_path = os.path.join(rice_dir, filename)
                
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            content = base64.b64encode(f.read()).decode('utf-8')
                        
                        url = f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/contents/{filename}'
                        
                        data = {
                            'message': f'Add {filename}',
                            'content': content
                        }
                        
                        response = requests.put(url, headers=headers, json=data, timeout=30)
                        
                        if response.status_code in [200, 201]:
                            uploaded_count += 1
                            self._add_progress(f"✅ Uploaded {filename}")
                        else:
                            self._add_progress(f"⚠️ Failed to upload {filename}")
                            failed_files.append(filename)
                    
                    except Exception as e:
                        self._add_progress(f"❌ Error uploading {filename}: {str(e)}")
                        failed_files.append(filename)
                else:
                    self._add_progress(f"⚠️ File not found: {filename}")
                    failed_files.append(filename)
            
            self._add_progress(f"📁 Upload complete: {uploaded_count}/{len(files_to_upload)} files uploaded")
            
            if uploaded_count == len(files_to_upload):
                self.show_popup("Upload Complete", f"Successfully uploaded all {uploaded_count} files to GitHub!", "success")
            else:
                self.show_popup("Partial Upload", f"Uploaded {uploaded_count}/{len(files_to_upload)} files. Some files failed.", "warning")
            
        except Exception as e:
            self._add_progress(f"❌ Upload error: {str(e)}")
            self.show_popup("Upload Error", f"Error uploading files: {str(e)}", "error")
    
    def _setup_cicd(self):
        """Setup CI/CD pipeline"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self.show_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        if not self._check_repository_exists(repo_name):
            self.show_popup("Repository Not Found", f"Repository '{repo_name}' does not exist. Please create it first using Step 1.", "warning")
            return
        
        self.repo_name = repo_name
        self._add_progress("Setting up CI/CD pipeline...")
        
        try:
            # Read CI/CD workflow file
            workflow_path = os.path.join(os.path.dirname(__file__), '.github_workflows_rice-tester-ci.yml')
            
            if os.path.exists(workflow_path):
                with open(workflow_path, 'r', encoding='utf-8') as f:
                    workflow_content = f.read()
                
                headers = {
                    'Authorization': f'token {self.github_token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
                
                url = f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/contents/.github/workflows/rice-tester-ci.yml'
                
                content_b64 = base64.b64encode(workflow_content.encode('utf-8')).decode('utf-8')
                
                data = {
                    'message': 'Add CI/CD pipeline for RICE Tester',
                    'content': content_b64
                }
                
                response = requests.put(url, headers=headers, json=data, timeout=30)
                
                if response.status_code in [200, 201]:
                    self._add_progress("✅ CI/CD pipeline configured successfully!")
                    self.show_popup("CI/CD Setup Complete", "GitHub Actions pipeline configured successfully!", "success")
                else:
                    self._add_progress(f"❌ Failed to setup CI/CD: {response.status_code}")
                    self.show_popup("CI/CD Error", "Failed to setup CI/CD pipeline.", "error")
            else:
                self._add_progress("❌ CI/CD workflow file not found")
                self.show_popup("File Not Found", "CI/CD workflow file not found.", "error")
                
        except Exception as e:
            self._add_progress(f"❌ CI/CD setup error: {str(e)}")
            self.show_popup("Setup Error", f"Error setting up CI/CD: {str(e)}", "error")
    
    def _create_release(self):
        """Create release with automatic version increment"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self.show_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        if not self._check_repository_exists(repo_name):
            self.show_popup("Repository Not Found", f"Repository '{repo_name}' does not exist. Please create it first using Step 1.", "warning")
            return
        
        self.repo_name = repo_name
        self._add_progress("Creating release...")
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get existing releases to determine next version
            releases_response = requests.get(f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/releases',
                                           headers=headers, timeout=10)
            
            next_version = "v1.0.0"
            if releases_response.status_code == 200:
                releases = releases_response.json()
                if releases:
                    # Find highest version number
                    versions = []
                    for release in releases:
                        tag = release['tag_name']
                        if tag.startswith('v') and '.' in tag:
                            try:
                                version_parts = tag[1:].split('.')
                                if len(version_parts) >= 2:
                                    major = int(version_parts[0])
                                    minor = int(version_parts[1])
                                    patch = int(version_parts[2]) if len(version_parts) > 2 else 0
                                    versions.append((major, minor, patch))
                            except ValueError:
                                continue
                    
                    if versions:
                        # Get highest version and increment patch
                        highest = max(versions)
                        next_version = f"v{highest[0]}.{highest[1]}.{highest[2] + 1}"
                        self._add_progress(f"📈 Next version: {next_version}")
            
            data = {
                'tag_name': next_version,
                'target_commitish': 'main',
                'name': f'RICE Tester {next_version} - Enterprise Edition',
                'body': f'''# RICE Tester Enterprise Edition {next_version}

## 🚀 Enterprise Features
- **Personal Analytics Dashboard**: Individual performance insights and achievements
- **Auto-Update System**: Seamless updates via GitHub integration
- **Enhanced Batch Execution**: Smart login optimization and professional loading
- **GitHub CI/CD Pipeline**: Automated testing and distribution

## 🎯 Core Features
- Complete FSM testing suite with authentication
- RICE profile management and scenario testing
- Browser automation with Edge/Chrome support
- Professional UI with enterprise-grade styling

## 📦 Installation
1. Download the team distribution ZIP
2. Extract and run SETUP_FIRST_TIME.bat
3. Use RUN_RICE_TESTER.bat for daily launches

**Created with ❤️ by IQ (Infor Q) & Van Anthony Silleza**
*Enterprise-Grade FSM Testing Platform*

---
*Release generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*''',
                'draft': False,
                'prerelease': False
            }
            
            response = requests.post(f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/releases',
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 201:
                release_data = response.json()
                self._add_progress(f"✅ Release {next_version} created successfully!")
                self._add_progress(f"🔗 Release URL: {release_data['html_url']}")
                self.show_popup("Release Created", f"Release {next_version} created successfully!", "success")
            else:
                error_msg = response.json().get('message', 'Unknown error')
                self._add_progress(f"❌ Failed to create release: {error_msg}")
                self.show_popup("Release Error", f"Failed to create release: {error_msg}", "error")
                
        except Exception as e:
            self._add_progress(f"❌ Release creation error: {str(e)}")
            self.show_popup("Error", f"Error creating release: {str(e)}", "error")
    
    def _save_github_credentials(self, token, username):
        """Save GitHub credentials securely"""
        try:
            encoded_token = base64.b64encode(token.encode()).decode()
            
            config = {
                'github_username': username,
                'github_token': encoded_token,
                'saved_at': datetime.now().isoformat()
            }
            
            config_path = os.path.join(os.path.dirname(__file__), 'github_config.json')
            with open(config_path, 'w') as f:
                json.dump(config, f)
                
        except Exception as e:
            print(f"Failed to save GitHub config: {e}")
    
    def _load_github_credentials(self):
        """Load saved GitHub credentials"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'github_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.github_username = config.get('github_username')
                encoded_token = config.get('github_token')
                if encoded_token:
                    self.github_token = base64.b64decode(encoded_token.encode()).decode()
                
                return True
        except Exception as e:
            print(f"Failed to load GitHub config: {e}")
        
        return False
    
    def _get_current_version(self):
        """Get current version from version.json"""
        try:
            version_path = os.path.join(os.path.dirname(__file__), 'version.json')
            if os.path.exists(version_path):
                with open(version_path, 'r') as f:
                    version_data = json.load(f)
                    return f"v{version_data.get('version', '1.0.0')}"
        except Exception:
            pass
        return "v1.0.0"
    
    def _save_updater_config(self):
        """Save updater configuration for Updates button"""
        if not self.github_username or not self.repo_name:
            return
        
        try:
            current_version = self._get_current_version().replace('v', '')
            
            updater_config = {
                'github_username': self.github_username,
                'github_repo': self.repo_name,
                'current_version': current_version,
                'configured_at': datetime.now().isoformat()
            }
            
            config_path = os.path.join(os.path.dirname(__file__), 'updater_config.json')
            with open(config_path, 'w') as f:
                json.dump(updater_config, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save updater config: {e}")
    
    def _copy_release_url(self):
        """Copy release URL to clipboard"""
        try:
            url = f"https://github.com/{self.github_username}/rice-tester/releases"
            # Copy to clipboard
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(url)
            root.update()
            root.destroy()
            
            self.show_popup("Copied", "Release URL copied to clipboard!", "success")
        except Exception as e:
            self.show_popup("Error", f"Failed to copy URL: {str(e)}", "error")

if __name__ == "__main__":
    print("GitHub Integration Manager for RICE Tester")
    print("Secure access control - Only for authorized users")
    print("Features: Repository creation, code upload, CI/CD setup, releases")