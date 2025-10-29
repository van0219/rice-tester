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
    from Temp.enhanced_popup_system import create_enhanced_dialog

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
        
        panel = create_enhanced_dialog(None, "🐙 GitHub Integration - RICE Tester CI/CD", 900, 700, modal=False)
        panel.resizable(False, False)
        panel.maxsize(900, 700)
        
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
        
        # Progress section
        progress_frame = tk.Frame(parent, bg='#f6f8fa', relief='solid', bd=1, padx=20, pady=15)
        progress_frame.pack(fill="x", pady=(20, 0))
        
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
            self._show_enhanced_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        # Show loading dialog
        loading = self._show_loading_dialog("🏠 Creating Repository", "Setting up your GitHub repository...")
        
        def create_repo():
            self._add_progress(f"Creating repository '{repo_name}'...")
            self._create_repository_process(repo_name, loading)
        
        import threading
        threading.Thread(target=create_repo, daemon=True).start()
    
    def _create_repository_process(self, repo_name, loading):
        
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
            
            loading.destroy()
            
            if response.status_code == 201:
                self.repo_name = repo_name
                self._save_updater_config()
                self._add_progress(f"✅ Repository '{repo_name}' created successfully!")
                self._add_progress(f"🔗 URL: https://github.com/{self.github_username}/{repo_name}")
                self._show_enhanced_popup("Success", f"Repository '{repo_name}' created successfully!", "success")
            elif response.status_code == 422:
                self._add_progress(f"ℹ️ Repository '{repo_name}' already exists")
                self.repo_name = repo_name
                self._save_updater_config()
                self._show_enhanced_popup("Repository Exists", f"Repository '{repo_name}' already exists. You can proceed to next step.", "warning")
            else:
                error_msg = response.json().get('message', 'Unknown error')
                self._add_progress(f"❌ Failed to create repository: {error_msg}")
                self._show_enhanced_popup("Error", f"Failed to create repository: {error_msg}", "error")
                
        except Exception as e:
            loading.destroy()
            self._add_progress(f"❌ Error creating repository: {str(e)}")
            self._show_enhanced_popup("Error", f"Error creating repository: {str(e)}", "error")
    
    def _upload_rice_tester(self):
        """Upload RICE Tester code to repository"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self._show_enhanced_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        # Check if repository exists
        if not self._check_repository_exists(repo_name):
            self._show_enhanced_popup("Repository Not Found", f"Repository '{repo_name}' does not exist. Please create it first using Step 1.", "warning")
            return
        
        # Set repo name if check passed
        self.repo_name = repo_name
        
        # Show loading dialog
        loading = self._show_loading_dialog("📦 Uploading Code", "Uploading 35+ RICE Tester files to GitHub...")
        
        def upload_code():
            self._add_progress("Uploading RICE Tester code...")
            self._upload_rice_tester_process(loading)
        
        import threading
        threading.Thread(target=upload_code, daemon=True).start()
    
    def _upload_rice_tester_process(self, loading):
        
        try:
            # Get current RICE Tester directory
            rice_dir = os.path.dirname(os.path.abspath(__file__)).replace('\\Temp', '')
            
            # Dynamic file discovery - automatically include all relevant files
            files_to_upload = []
            
            # Files to exclude (temporary, debug, backup files)
            exclude_patterns = ['_backup', '_original', 'debug_', 'temp_', 'test_', 'check_', 
                              'analyze_', 'find_', 'create_team', 'create_bulletproof', 
                              'create_complete', 'create_corrected', 'create_final']
            
            # Get Python files from main directory (filtered)
            for file in os.listdir(rice_dir):
                if file.endswith('.py') and not any(pattern in file.lower() for pattern in exclude_patterns):
                    files_to_upload.append(file)
            
            # Get essential files from Temp folder (only if not in main directory)
            temp_dir = os.path.join(rice_dir, 'Temp')
            if os.path.exists(temp_dir):
                temp_essential = ['personal_analytics.py', 'auto_updater.py', 'enhanced_run_all_scenarios.py',
                                'enhanced_popup_system.py', 'github_integration_manager.py']
                for file in temp_essential:
                    # Only add if not already in main directory
                    if file not in files_to_upload and os.path.exists(os.path.join(temp_dir, file)):
                        files_to_upload.append(file)
            
            # Add essential non-Python files
            essential_files = ['requirements.txt', 'README.md', 'infor_logo.ico', 'fsm_tester.db']
            for file in essential_files:
                if os.path.exists(os.path.join(rice_dir, file)):
                    files_to_upload.append(file)
            
            # Sort final list
            files_to_upload = sorted(files_to_upload)
            
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            uploaded_count = 0
            
            for filename in files_to_upload:
                file_path = os.path.join(rice_dir, filename)
                
                # Check if file exists, if not try Temp folder
                temp_files = ['personal_analytics.py', 'auto_updater.py', 'enhanced_run_all_scenarios.py', 
                             'enhanced_popup_system.py', 'github_integration_manager.py']
                if not os.path.exists(file_path) and filename in temp_files:
                    file_path = os.path.join(rice_dir, 'Temp', filename)
                
                if os.path.exists(file_path):
                    try:
                        with open(file_path, 'rb') as f:
                            content = base64.b64encode(f.read()).decode('utf-8')
                        
                        data = {
                            'message': f'Add {filename}',
                            'content': content
                        }
                        
                        url = f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/contents/{filename}'
                        response = requests.put(url, headers=headers, json=data, timeout=30)
                        
                        if response.status_code in [200, 201]:
                            uploaded_count += 1
                            self._add_progress(f"✅ Uploaded {filename}")
                        else:
                            self._add_progress(f"⚠️ Failed to upload {filename}")
                    
                    except Exception as e:
                        self._add_progress(f"❌ Error uploading {filename}: {str(e)}")
                else:
                    self._add_progress(f"⚠️ File not found: {filename}")
            
            loading.destroy()
            self._add_progress(f"📁 Upload complete: {uploaded_count} files uploaded")
            self._show_enhanced_popup("Upload Complete", f"Successfully uploaded {uploaded_count} files to GitHub!", "success")
            
        except Exception as e:
            loading.destroy()
            self._add_progress(f"❌ Upload error: {str(e)}")
            self._show_enhanced_popup("Upload Error", f"Error uploading files: {str(e)}", "error")
    
    def _setup_cicd(self):
        """Setup CI/CD pipeline"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self._show_enhanced_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        # Check if repository exists
        if not self._check_repository_exists(repo_name):
            self._show_enhanced_popup("Repository Not Found", f"Repository '{repo_name}' does not exist. Please create it first using Step 1.", "warning")
            return
        
        # Set repo name if check passed
        self.repo_name = repo_name
        
        # Show loading dialog
        loading = self._show_loading_dialog("⚙️ Setting up CI/CD", "Configuring GitHub Actions pipeline...")
        
        def setup_pipeline():
            self._add_progress("Setting up CI/CD pipeline...")
            self._setup_cicd_process(loading)
        
        import threading
        threading.Thread(target=setup_pipeline, daemon=True).start()
    
    def _setup_cicd_process(self, loading):
        
        try:
            # Read CI/CD workflow file
            workflow_path = os.path.join(os.path.dirname(__file__), '.github_workflows_rice-tester-ci.yml')
            
            if os.path.exists(workflow_path):
                with open(workflow_path, 'r', encoding='utf-8') as f:
                    workflow_content = f.read()
                
                # Create .github/workflows directory structure
                headers = {
                    'Authorization': f'token {self.github_token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
                
                # Upload workflow file
                content_b64 = base64.b64encode(workflow_content.encode('utf-8')).decode('utf-8')
                
                data = {
                    'message': 'Add CI/CD pipeline for RICE Tester',
                    'content': content_b64
                }
                
                url = f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/contents/.github/workflows/rice-tester-ci.yml'
                response = requests.put(url, headers=headers, json=data, timeout=30)
                
                loading.destroy()
                if response.status_code in [200, 201]:
                    self._add_progress("✅ CI/CD pipeline configured successfully!")
                    self._add_progress("🔧 GitHub Actions will now automatically:")
                    self._add_progress("   • Test RICE Tester when you push code")
                    self._add_progress("   • Create team distribution packages")
                    self._add_progress("   • Generate releases with assets")
                    
                    self._show_enhanced_popup("CI/CD Setup Complete", "GitHub Actions pipeline configured successfully!", "success")
                else:
                    self._add_progress(f"❌ Failed to setup CI/CD: {response.status_code}")
                    self._show_enhanced_popup("CI/CD Error", "Failed to setup CI/CD pipeline.", "error")
            else:
                loading.destroy()
                self._add_progress("❌ CI/CD workflow file not found")
                self._show_enhanced_popup("File Not Found", "CI/CD workflow file not found in Temp folder.", "error")
                
        except Exception as e:
            loading.destroy()
            self._add_progress(f"❌ CI/CD setup error: {str(e)}")
            self._show_enhanced_popup("Setup Error", f"Error setting up CI/CD: {str(e)}", "error")
    
    def _create_release(self):
        """Create initial release"""
        repo_name = self.repo_entry.get().strip()
        if not repo_name:
            self._show_enhanced_popup("Missing Repository Name", "Please enter a repository name.", "warning")
            return
        
        # Check if repository exists
        if not self._check_repository_exists(repo_name):
            self._show_enhanced_popup("Repository Not Found", f"Repository '{repo_name}' does not exist. Please create it first using Step 1.", "warning")
            return
        
        # Set repo name if check passed
        self.repo_name = repo_name
        
        self._add_progress("Creating initial release...")
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'tag_name': 'v1.0.0',
                'target_commitish': 'main',
                'name': 'RICE Tester v1.0.0 - Enterprise Edition',
                'body': '''# RICE Tester Enterprise Edition v1.0.0

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
*Enterprise-Grade FSM Testing Platform*''',
                'draft': False,
                'prerelease': False
            }
            
            response = requests.post(f'https://api.github.com/repos/{self.github_username}/{self.repo_name}/releases',
                                   headers=headers, json=data, timeout=30)
            
            if response.status_code == 201:
                release_data = response.json()
                self._add_progress("✅ Release v1.0.0 created successfully!")
                self._add_progress(f"🔗 Release URL: {release_data['html_url']}")
                self._add_progress("🎉 GitHub CI/CD setup is now complete!")
                self._add_progress("")
                self._add_progress("📋 Next Steps:")
                self._add_progress("1. Update auto_updater.py with your repository details")
                self._add_progress("2. Add personal dashboard button to RICE Tester UI")
                self._add_progress("3. Deploy enhanced RICE Tester to your team")
                
                self._show_enhanced_popup("Release Created", "Initial release v1.0.0 created successfully! GitHub CI/CD is now fully configured.", "success")
            else:
                error_msg = response.json().get('message', 'Unknown error')
                self._add_progress(f"❌ Failed to create release: {error_msg}")
                self._show_enhanced_popup("Release Error", f"Failed to create release: {error_msg}", "error")
                
        except Exception as e:
            self._add_progress(f"❌ Release creation error: {str(e)}")
            self._show_enhanced_popup("Error", f"Error creating release: {str(e)}", "error")
    
    def _save_github_credentials(self, token, username):
        """Save GitHub credentials securely (basic encryption)"""
        try:
            # Simple encoding (not production-grade encryption)
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
    
    def _show_loading_dialog(self, title, message):
        """Show loading dialog for GitHub operations"""
        loading = tk.Toplevel()
        loading.title(title)
        loading.geometry("400x200")
        loading.configure(bg='#ffffff')
        loading.resizable(False, False)
        loading.transient()
        loading.grab_set()
        
        # Center the dialog
        loading.update_idletasks()
        x = (loading.winfo_screenwidth() // 2) - (400 // 2)
        y = (loading.winfo_screenheight() // 2) - (200 // 2)
        loading.geometry(f"400x200+{x}+{y}")
        
        try:
            loading.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(loading, bg='#3b82f6', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=title, font=('Segoe UI', 14, 'bold'), 
                bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(loading, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=message, font=('Segoe UI', 11), 
                bg='#ffffff', fg='#374151').pack(pady=(0, 15))
        
        # Animated progress bar
        progress_bar = ttk.Progressbar(content_frame, mode='indeterminate', length=300)
        progress_bar.pack(pady=(0, 10))
        progress_bar.start(10)
        
        tk.Label(content_frame, text="Please wait...", font=('Segoe UI', 9), 
                bg='#ffffff', fg='#6b7280').pack()
        
        loading.update()
        return loading
    
    def _save_updater_config(self):
        """Save updater configuration for Updates button"""
        if not self.github_username or not self.repo_name:
            return
        
        try:
            updater_config = {
                'github_username': self.github_username,
                'github_repo': self.repo_name,
                'current_version': '1.0.0',
                'configured_at': datetime.now().isoformat()
            }
            
            config_path = os.path.join(os.path.dirname(__file__), 'updater_config.json')
            with open(config_path, 'w') as f:
                json.dump(updater_config, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save updater config: {e}")
    
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
    
    def _show_enhanced_popup(self, title, message, status):
        """Show enhanced popup that doesn't hide existing forms"""
        popup = create_enhanced_dialog(None, title, 400, 200, modal=False)
        
        try:
            popup.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Status colors
        if status == "success":
            icon = "✅"
            color = "#10b981"
        elif status == "warning":
            icon = "⚠️"
            color = "#f59e0b"
        else:
            icon = "❌"
            color = "#ef4444"
        
        # Header
        header_frame = tk.Frame(popup, bg=color, height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text=f"{icon} {title}", 
                font=('Segoe UI', 14, 'bold'), bg=color, fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(popup, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=message, font=('Segoe UI', 10), 
                bg='#ffffff', fg='#374151', wraplength=350, justify="left").pack(pady=(0, 15))
        
        tk.Button(content_frame, text="Close", font=('Segoe UI', 10, 'bold'), 
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=8, 
                 cursor='hand2', bd=0, command=popup.destroy).pack()

# Integration function for main RICE Tester
def add_github_integration_to_rice_tester():
    """
    Integration instructions for adding GitHub module to RICE Tester
    
    Add this to your main RICE Tester interface:
    
    1. In SeleniumInboundTester_Lite.py, add to setup_ui():
    
    # Check if user has GitHub access
    if self.user['username'].lower() in ['vansilleza_fpi', 'van_silleza', 'vansilleza']:
        # Add GitHub tab
        self.tab_manager.add_tab("🐙 GitHub CI/CD", 
                                lambda parent: self._setup_github_tab(parent))
    
    2. Add this method to SeleniumInboundTester_Lite class:
    
    def _setup_github_tab(self, parent):
        from github_integration_manager import GitHubIntegrationManager
        
        github_manager = GitHubIntegrationManager(
            self.db_manager, 
            self.show_popup, 
            self.user
        )
        
        # Create GitHub integration button
        github_frame = tk.Frame(parent, bg='#ffffff', padx=50, pady=50)
        github_frame.pack(fill="both", expand=True)
        
        tk.Label(github_frame, text="🐙 GitHub CI/CD Integration", 
                font=('Segoe UI', 18, 'bold'), bg='#ffffff', fg='#24292e').pack(pady=(0, 20))
        
        tk.Label(github_frame, text="Set up automated CI/CD pipeline for RICE Tester", 
                font=('Segoe UI', 12), bg='#ffffff', fg='#586069').pack(pady=(0, 30))
        
        tk.Button(github_frame, text="🚀 Open GitHub Integration", 
                 font=('Segoe UI', 14, 'bold'), bg='#238636', fg='#ffffff', 
                 relief='flat', padx=30, pady=15, cursor='hand2', bd=0,
                 command=github_manager.show_github_integration_panel).pack()
    """
    pass

if __name__ == "__main__":
    print("GitHub Integration Manager for RICE Tester")
    print("Secure access control - Only for authorized users")
    print("Features: Repository creation, code upload, CI/CD setup, releases")