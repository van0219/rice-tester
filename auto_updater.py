#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
import zipfile
import shutil
import tempfile
from datetime import datetime, timedelta
import threading
from rice_dialogs import center_dialog

class RiceAutoUpdater:
    """
    Auto-Update System for RICE Tester
    Checks GitHub releases and provides seamless updates
    """
    
    def __init__(self, current_version="1.0.0", github_repo="rice-tester"):
        self.current_version = current_version
        self.github_repo = github_repo
        self.github_username = "vansilleza"  # Will be configurable
        self.update_check_interval = 24  # hours
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load updater configuration"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'updater_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                self.github_username = config.get('github_username', 'vansilleza')
                self.github_repo = config.get('github_repo', 'rice-tester')
                self.current_version = config.get('current_version', '1.0.0')
        except Exception as e:
            print(f"Failed to load updater config: {e}")
    
    def _save_config(self):
        """Save updater configuration"""
        try:
            config = {
                'github_username': self.github_username,
                'github_repo': self.github_repo,
                'current_version': self.current_version,
                'last_check': datetime.now().isoformat()
            }
            
            config_path = os.path.join(os.path.dirname(__file__), 'updater_config.json')
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Failed to save updater config: {e}")
    
    def should_check_for_updates(self):
        """Check if it's time to check for updates"""
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'updater_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                last_check = config.get('last_check')
                if last_check:
                    last_check_time = datetime.fromisoformat(last_check)
                    if datetime.now() - last_check_time < timedelta(hours=self.update_check_interval):
                        return False
            
            return True
        except Exception:
            return True
    
    def check_for_updates(self, show_ui=True, callback=None):
        """Check for updates from GitHub releases"""
        if show_ui:
            self._show_update_dialog()
        else:
            # Background check
            threading.Thread(target=self._background_check, args=(callback,), daemon=True).start()
    
    def _show_update_dialog(self):
        """Show update check dialog"""
        dialog = tk.Toplevel()
        dialog.title("🔄 RICE Tester Updates")
        center_dialog(dialog, 500, 400)
        dialog.configure(bg='#ffffff')
        dialog.resizable(False, False)
        
        try:
            dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(dialog, bg='#10b981', height=70)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(header_frame, text="🔄 RICE Tester Updates", 
                              font=('Segoe UI', 16, 'bold'), bg='#10b981', fg='#ffffff')
        title_label.pack(expand=True)
        
        # Content
        content_frame = tk.Frame(dialog, bg='#ffffff', padx=25, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        # Current version
        current_frame = tk.Frame(content_frame, bg='#f3f4f6', relief='solid', bd=1, padx=15, pady=10)
        current_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(current_frame, text="📦 Current Version", font=('Segoe UI', 12, 'bold'), 
                bg='#f3f4f6', fg='#374151').pack(anchor="w")
        tk.Label(current_frame, text=f"RICE Tester v{self.current_version}", font=('Segoe UI', 10), 
                bg='#f3f4f6', fg='#6b7280').pack(anchor="w", pady=(5, 0))
        
        # Status area
        self.status_frame = tk.Frame(content_frame, bg='#ffffff')
        self.status_frame.pack(fill="x", pady=(0, 20))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(content_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(fill="x", pady=(0, 15))
        
        # Status label
        self.status_label = tk.Label(content_frame, text="Checking for updates...", 
                                    font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        self.status_label.pack(pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='#ffffff')
        button_frame.pack(fill="x")
        
        self.update_button = tk.Button(button_frame, text="📥 Download Update", 
                                      font=('Segoe UI', 10, 'bold'), bg='#3b82f6', fg='#ffffff',
                                      relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                                      state='disabled', command=self._start_update)
        self.update_button.pack(side="left", padx=(0, 10))
        
        close_button = tk.Button(button_frame, text="Close", 
                                font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff',
                                relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                                command=dialog.destroy)
        close_button.pack(side="left")
        
        # Start checking
        self.dialog = dialog
        self.latest_release = None
        threading.Thread(target=self._check_github_releases, daemon=True).start()
    
    def _check_github_releases(self):
        """Check GitHub for latest release"""
        try:
            self._update_status("Connecting to GitHub...")
            self.progress_var.set(25)
            
            url = f"https://api.github.com/repos/{self.github_username}/{self.github_repo}/releases/latest"
            response = requests.get(url, timeout=10)
            
            self.progress_var.set(50)
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name'].lstrip('v')
                
                self.progress_var.set(75)
                self._update_status("Comparing versions...")
                
                if self._is_newer_version(latest_version, self.current_version):
                    self.latest_release = release_data
                    self.progress_var.set(100)
                    self._update_status(f"✅ Update available: v{latest_version}")
                    self._show_update_available(release_data)
                else:
                    self.progress_var.set(100)
                    self._update_status("✅ You have the latest version!")
                    self._show_up_to_date()
            else:
                self.progress_var.set(100)
                self._update_status("❌ Failed to check for updates")
                self._show_check_failed()
                
        except Exception as e:
            self.progress_var.set(100)
            self._update_status(f"❌ Error: {str(e)}")
            self._show_check_failed()
        
        # Save last check time
        self._save_config()
    
    def _update_status(self, message):
        """Update status label thread-safe"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def _is_newer_version(self, latest, current):
        """Compare version strings"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        except:
            return False
    
    def _show_update_available(self, release_data):
        """Show update available UI"""
        # Clear status frame
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Update info
        update_frame = tk.Frame(self.status_frame, bg='#dbeafe', relief='solid', bd=1, padx=15, pady=10)
        update_frame.pack(fill="x")
        
        tk.Label(update_frame, text="🎉 Update Available!", font=('Segoe UI', 12, 'bold'), 
                bg='#dbeafe', fg='#1e40af').pack(anchor="w")
        
        version_text = f"New Version: {release_data['tag_name']}"
        tk.Label(update_frame, text=version_text, font=('Segoe UI', 10), 
                bg='#dbeafe', fg='#1e3a8a').pack(anchor="w", pady=(5, 0))
        
        # Release notes (truncated)
        notes = release_data.get('body', '')[:200]
        if len(notes) == 200:
            notes += "..."
        
        if notes:
            tk.Label(update_frame, text=f"What's New: {notes}", font=('Segoe UI', 9), 
                    bg='#dbeafe', fg='#1e3a8a', wraplength=400, justify="left").pack(anchor="w", pady=(5, 0))
        
        # Enable update button
        self.update_button.config(state='normal')
    
    def _show_up_to_date(self):
        """Show up to date UI"""
        # Clear status frame
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Up to date info
        uptodate_frame = tk.Frame(self.status_frame, bg='#d1fae5', relief='solid', bd=1, padx=15, pady=10)
        uptodate_frame.pack(fill="x")
        
        tk.Label(uptodate_frame, text="✅ You're Up to Date!", font=('Segoe UI', 12, 'bold'), 
                bg='#d1fae5', fg='#065f46').pack(anchor="w")
        
        tk.Label(uptodate_frame, text="You have the latest version of RICE Tester.", font=('Segoe UI', 10), 
                bg='#d1fae5', fg='#047857').pack(anchor="w", pady=(5, 0))
    
    def _show_check_failed(self):
        """Show check failed UI"""
        # Clear status frame
        for widget in self.status_frame.winfo_children():
            widget.destroy()
        
        # Error info
        error_frame = tk.Frame(self.status_frame, bg='#fee2e2', relief='solid', bd=1, padx=15, pady=10)
        error_frame.pack(fill="x")
        
        tk.Label(error_frame, text="❌ Update Check Failed", font=('Segoe UI', 12, 'bold'), 
                bg='#fee2e2', fg='#991b1b').pack(anchor="w")
        
        tk.Label(error_frame, text="Unable to check for updates. Please try again later.", font=('Segoe UI', 10), 
                bg='#fee2e2', fg='#b91c1c').pack(anchor="w", pady=(5, 0))
    
    def _start_update(self):
        """Start the update process"""
        if not self.latest_release:
            return
        
        # Disable update button
        self.update_button.config(state='disabled', text="Downloading...")
        
        # Start download in background
        threading.Thread(target=self._download_and_install, daemon=True).start()
    
    def _download_and_install(self):
        """Download and install update"""
        try:
            # Find download URL
            download_url = None
            for asset in self.latest_release.get('assets', []):
                if asset['name'].endswith('.zip') and 'RICE_Tester' in asset['name']:
                    download_url = asset['browser_download_url']
                    break
            
            if not download_url:
                self._update_status("❌ No download package found")
                return
            
            self._update_status("📥 Downloading update...")
            self.progress_var.set(0)
            
            # Download file
            response = requests.get(download_url, stream=True, timeout=30)
            total_size = int(response.headers.get('content-length', 0))
            
            # Create temp file
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, 'rice_tester_update.zip')
            
            downloaded = 0
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 80  # 80% for download
                            self.progress_var.set(progress)
            
            self._update_status("📦 Installing update...")
            self.progress_var.set(85)
            
            # Create backup
            rice_dir = os.path.dirname(os.path.dirname(__file__))  # Go up from Temp
            backup_dir = os.path.join(rice_dir, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # Backup critical files
            critical_files = ['fsm_tester.db', 'github_config.json', 'updater_config.json']
            os.makedirs(backup_dir, exist_ok=True)
            
            for file in critical_files:
                src = os.path.join(rice_dir, file)
                if os.path.exists(src):
                    shutil.copy2(src, backup_dir)
                # Also check Temp folder
                src_temp = os.path.join(rice_dir, 'Temp', file)
                if os.path.exists(src_temp):
                    shutil.copy2(src_temp, os.path.join(backup_dir, file))
            
            self.progress_var.set(90)
            
            # Extract update
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find extracted folder
            extracted_folder = None
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                if os.path.isdir(item_path) and item != '__pycache__':
                    extracted_folder = item_path
                    break
            
            if extracted_folder:
                # Copy files (excluding database and config files)
                for root, dirs, files in os.walk(extracted_folder):
                    for file in files:
                        if file not in critical_files and not file.endswith('.db'):
                            src_file = os.path.join(root, file)
                            rel_path = os.path.relpath(src_file, extracted_folder)
                            dst_file = os.path.join(rice_dir, rel_path)
                            
                            # Create directory if needed
                            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                            shutil.copy2(src_file, dst_file)
            
            self.progress_var.set(95)
            
            # Update version
            new_version = self.latest_release['tag_name'].lstrip('v')
            self.current_version = new_version
            self._save_config()
            
            self.progress_var.set(100)
            self._update_status("✅ Update completed successfully!")
            
            # Show completion dialog
            self._show_update_complete(new_version, backup_dir)
            
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        except Exception as e:
            self._update_status(f"❌ Update failed: {str(e)}")
            self.update_button.config(state='normal', text="📥 Download Update")
    
    def _show_update_complete(self, new_version, backup_dir):
        """Show update completion dialog"""
        completion_dialog = tk.Toplevel(self.dialog)
        completion_dialog.title("✅ Update Complete")
        center_dialog(completion_dialog, 450, 300)
        completion_dialog.configure(bg='#ffffff')
        completion_dialog.grab_set()
        
        try:
            completion_dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(completion_dialog, bg='#10b981', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="✅ Update Complete!", 
                font=('Segoe UI', 16, 'bold'), bg='#10b981', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(completion_dialog, bg='#ffffff', padx=25, pady=25)
        content_frame.pack(fill="both", expand=True)
        
        tk.Label(content_frame, text=f"RICE Tester has been updated to v{new_version}", 
                font=('Segoe UI', 12, 'bold'), bg='#ffffff', fg='#065f46').pack(pady=(0, 15))
        
        tk.Label(content_frame, text="✅ Application files updated\n✅ Database and settings preserved\n✅ Backup created", 
                font=('Segoe UI', 10), bg='#ffffff', fg='#047857', justify="left").pack(pady=(0, 15))
        
        tk.Label(content_frame, text=f"Backup location:\n{backup_dir}", 
                font=('Segoe UI', 9), bg='#ffffff', fg='#6b7280', justify="left").pack(pady=(0, 20))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='#ffffff')
        button_frame.pack()
        
        restart_btn = tk.Button(button_frame, text="🔄 Restart RICE Tester", 
                               font=('Segoe UI', 10, 'bold'), bg='#3b82f6', fg='#ffffff',
                               relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                               command=self._restart_application)
        restart_btn.pack(side="left", padx=(0, 10))
        
        later_btn = tk.Button(button_frame, text="Later", 
                             font=('Segoe UI', 10, 'bold'), bg='#6b7280', fg='#ffffff',
                             relief='flat', padx=20, pady=8, cursor='hand2', bd=0,
                             command=completion_dialog.destroy)
        later_btn.pack(side="left")
    
    def _restart_application(self):
        """Restart the application"""
        try:
            import sys
            import subprocess
            
            # Close all dialogs
            if hasattr(self, 'dialog'):
                self.dialog.destroy()
            
            # Restart application
            rice_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'RICE_Tester.py')
            if os.path.exists(rice_path):
                subprocess.Popen([sys.executable, rice_path])
                sys.exit(0)
            else:
                messagebox.showinfo("Restart Required", "Please restart RICE Tester manually to complete the update.")
                
        except Exception as e:
            messagebox.showerror("Restart Failed", f"Please restart RICE Tester manually: {str(e)}")
    
    def _background_check(self, callback=None):
        """Background update check"""
        try:
            url = f"https://api.github.com/repos/{self.github_username}/{self.github_repo}/releases/latest"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data['tag_name'].lstrip('v')
                
                if self._is_newer_version(latest_version, self.current_version):
                    if callback:
                        callback(True, release_data)
                    return True
            
            if callback:
                callback(False, None)
            return False
            
        except Exception:
            if callback:
                callback(False, None)
            return False

# Configuration helper
def configure_updater(github_username, github_repo, current_version):
    """Configure the auto-updater with repository details"""
    config = {
        'github_username': github_username,
        'github_repo': github_repo,
        'current_version': current_version,
        'configured_at': datetime.now().isoformat()
    }
    
    config_path = os.path.join(os.path.dirname(__file__), 'updater_config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Auto-updater configured for {github_username}/{github_repo} v{current_version}")

if __name__ == "__main__":
    # Test the updater
    root = tk.Tk()
    root.withdraw()  # Hide main window
    
    updater = RiceAutoUpdater()
    updater.check_for_updates(show_ui=True)
    
    root.mainloop()