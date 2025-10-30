#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import sqlite3
import base64
import time
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from api_auth import APIAuthenticator
from screenshot_browser import BrowserManager
from screenshot_steps import StepExecutor
from screenshot_utils import ScreenshotUtils

class ScreenshotExecutorCore(BrowserManager, StepExecutor, ScreenshotUtils):
    """Core screenshot executor functionality"""
    
    def __init__(self, user_id, rice_profile_id, scenario_number):
        self.user_id = user_id
        self.rice_profile_id = str(rice_profile_id)
        self.scenario_number = scenario_number
        self.driver = None
        self.db_path = 'fsm_tester.db'
        self.progress_callback = None
        
        # Initialize parent classes
        StepExecutor.__init__(self)
        
        # Initialize API authenticator
        from database_manager import DatabaseManager
        self.db_manager = DatabaseManager(user_id)
        self.api_auth = APIAuthenticator(self.db_manager)
    
    def set_progress_callback(self, callback):
        """Set callback function for progress updates"""
        self.progress_callback = callback
    
    def safe_print(self, message):
        """Safely print messages with Unicode handling"""
        try:
            safe_message = message.encode('ascii', 'replace').decode('ascii')
            print(safe_message)
        except Exception as e:
            print(f"[UNICODE ERROR] {str(e)}")
        
    def capture_screenshot(self):
        """Capture screenshot and return as base64"""
        if not self.driver:
            return None
        try:
            screenshot = self.driver.get_screenshot_as_png()
            return base64.b64encode(screenshot).decode('utf-8')
        except Exception as e:
            self.safe_print(f"Screenshot capture failed: {e}")
            return None
    
    def save_screenshot_to_db(self, step_order, screenshot_before=None, screenshot_after=None, status="completed"):
        """Save screenshots to database using composite key"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE scenario_steps 
                SET screenshot_before = ?, screenshot_after = ?, 
                    screenshot_timestamp = ?, execution_status = ?
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ? AND step_order = ?
            ''', (screenshot_before, screenshot_after, datetime.now(), status, 
                  self.user_id, self.rice_profile_id, self.scenario_number, step_order))
            conn.commit()
            self.safe_print(f"Screenshots saved for step {step_order}")
        except Exception as e:
            self.safe_print(f"Database save failed: {e}")
        finally:
            conn.close()
    
    def wait_for_user_input(self, step_name, step_description):
        """Show dialog and wait for user input"""
        root = tk.Tk()
        root.withdraw()
        
        result = messagebox.askokcancel(
            "User Input Required",
            f"Step: {step_name}\n\n"
            f"Description: {step_description}\n\n"
            f"Please complete this step manually, then click OK to continue.\n"
            f"Click Cancel to stop execution."
        )
        
        root.destroy()
        return result
    
    def execute_scenario_with_shared_browser(self, shared_driver=None):
        """Execute scenario with shared browser session"""
        if shared_driver:
            self.driver = shared_driver
        
        # Get scenario steps
        steps = self.get_scenario_steps(self.user_id, self.rice_profile_id, self.scenario_number)
        if not steps:
            self.safe_print("No steps found for scenario")
            return False
        
        total_steps = len(steps)
        self.safe_print(f"Executing {total_steps} steps...")
        
        # Update progress
        if self.progress_callback:
            self.progress_callback(0, total_steps, "Starting", "Launching browser and starting execution...")
        
        success = True
        for i, step_data in enumerate(steps, 1):
            if not self.execute_step(step_data, i, total_steps):
                success = False
                break
        
        # Update scenario status
        status = "completed" if success else "failed"
        self.update_scenario_status(self.user_id, self.rice_profile_id, self.scenario_number, status)
        
        # Final progress update
        if self.progress_callback:
            if success:
                self.progress_callback(total_steps, total_steps, "Complete", "[SUCCESS] All steps completed successfully!")
            else:
                self.progress_callback(i-1, total_steps, "Failed", "[FAILED] Execution stopped due to error")
        
        return success
    
    def execute_scenario(self):
        """Execute scenario with new browser instance"""
        # Get browser configuration
        config = self.get_browser_config(self.user_id, self.rice_profile_id)
        
        # Create browser driver
        self.driver = self.create_driver(
            config['browser_type'], 
            config['incognito'], 
            config['second_screen']
        )
        
        if not self.driver:
            self.safe_print("Failed to create browser driver")
            return False
        
        try:
            return self.execute_scenario_with_shared_browser(self.driver)
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
    
    def execute_scenario_with_steps(self, custom_steps):
        """Execute scenario with custom filtered steps (for batch execution)"""
        # Get browser configuration
        config = self.get_browser_config(self.user_id, self.rice_profile_id)
        
        # Create browser driver
        self.driver = self.create_driver(
            config['browser_type'], 
            config['incognito'], 
            config['second_screen']
        )
        
        if not self.driver:
            self.safe_print("Failed to create browser driver")
            return False
        
        try:
            total_steps = len(custom_steps)
            self.safe_print(f"Executing {total_steps} custom steps...")
            
            # Update progress
            if self.progress_callback:
                self.progress_callback(0, total_steps, "Starting", "Launching browser and starting execution...")
            
            success = True
            for i, step_data in enumerate(custom_steps, 1):
                # Convert step data to expected format if needed
                if len(step_data) >= 6:
                    step_order, step_name, step_type, step_target, step_description, user_input_required = step_data
                    
                    # Create step data in expected format
                    formatted_step = {
                        'step_order': step_order,
                        'step_name': step_name,
                        'step_type': step_type,
                        'step_target': step_target,
                        'step_description': step_description,
                        'user_input_required': user_input_required
                    }
                    
                    if not self.execute_step(formatted_step, i, total_steps):
                        success = False
                        break
                else:
                    self.safe_print(f"Invalid step data format: {step_data}")
                    success = False
                    break
            
            # Update scenario status
            status = "completed" if success else "failed"
            self.update_scenario_status(self.user_id, self.rice_profile_id, self.scenario_number, status)
            
            # Final progress update
            if self.progress_callback:
                if success:
                    self.progress_callback(total_steps, total_steps, "Complete", "[SUCCESS] All steps completed successfully!")
                else:
                    self.progress_callback(i-1, total_steps, "Failed", "[FAILED] Execution stopped due to error")
            
            return success
            
        finally:
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
