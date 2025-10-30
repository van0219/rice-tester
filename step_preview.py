#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import os
import tempfile
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from PIL import Image, ImageTk
from rice_dialogs import center_dialog

class StepPreview:
    """Step validation and preview system for RICE Tester"""
    
    def __init__(self, selenium_manager, show_popup_callback):
        self.selenium_manager = selenium_manager
        self.show_popup = show_popup_callback
        self.preview_window = None
        
    def validate_and_preview_step(self, step_data, parent_window=None):
        """Validate step and show preview with screenshot"""
        step_type = step_data.get('step_type', '')
        target = step_data.get('target', '')
        value = step_data.get('value', '')
        
        if not self.selenium_manager.driver:
            self.show_popup("Preview Error", "Browser not initialized. Please start browser first.", "error")
            return False
            
        # Create preview window
        self._create_preview_window(step_data, parent_window)
        
        # Validate step in background
        self._validate_step_async(step_type, target, value)
        
        return True
    
    def _create_preview_window(self, step_data, parent_window):
        """Create step preview window"""
        self.preview_window = tk.Toplevel(parent_window) if parent_window else tk.Toplevel()
        self.preview_window.title("🔍 Step Preview & Validation")
        center_dialog(self.preview_window, 600, 500)
        self.preview_window.configure(bg='#ffffff')
        self.preview_window.resizable(False, False)
        
        try:
            self.preview_window.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Header
        header_frame = tk.Frame(self.preview_window, bg='#3b82f6', height=60)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="🔍 Step Preview & Validation", 
                font=('Segoe UI', 14, 'bold'), bg='#3b82f6', fg='#ffffff').pack(expand=True)
        
        # Content
        content_frame = tk.Frame(self.preview_window, bg='#ffffff', padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Step info
        info_frame = tk.Frame(content_frame, bg='#f8fafc', relief='solid', bd=1, padx=15, pady=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        tk.Label(info_frame, text=f"Type: {step_data.get('step_type', '')}", 
                font=('Segoe UI', 10, 'bold'), bg='#f8fafc').pack(anchor="w")
        tk.Label(info_frame, text=f"Target: {step_data.get('target', '')}", 
                font=('Segoe UI', 9), bg='#f8fafc', wraplength=500).pack(anchor="w", pady=(2, 0))
        if step_data.get('value'):
            tk.Label(info_frame, text=f"Value: {step_data.get('value', '')}", 
                    font=('Segoe UI', 9), bg='#f8fafc', wraplength=500).pack(anchor="w", pady=(2, 0))
        
        # Status area
        self.status_frame = tk.Frame(content_frame, bg='#ffffff')
        self.status_frame.pack(fill="x", pady=(0, 15))
        
        # Progress
        self.progress_bar = ttk.Progressbar(self.status_frame, mode='indeterminate', length=400)
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.start(10)
        
        self.status_label = tk.Label(self.status_frame, text="🔍 Validating step...", 
                                   font=('Segoe UI', 10), bg='#ffffff', fg='#6b7280')
        self.status_label.pack()
        
        # Screenshot area
        self.screenshot_frame = tk.Frame(content_frame, bg='#ffffff')
        self.screenshot_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(content_frame, bg='#ffffff')
        button_frame.pack(fill="x")
        
        self.retry_btn = tk.Button(button_frame, text="🔄 Retry", font=('Segoe UI', 10, 'bold'),
                                  bg='#f59e0b', fg='#ffffff', relief='flat', padx=15, pady=8,
                                  cursor='hand2', bd=0, state='disabled',
                                  command=lambda: self._validate_step_async(
                                      step_data.get('step_type'), step_data.get('target'), step_data.get('value')))
        self.retry_btn.pack(side="left", padx=(0, 10))
        
        tk.Button(button_frame, text="Close", font=('Segoe UI', 10, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=15, pady=8,
                 cursor='hand2', bd=0, command=self._close_preview).pack(side="left")
    
    def _validate_step_async(self, step_type, target, value):
        """Validate step asynchronously"""
        import threading
        
        def validate():
            try:
                self._update_status("🔍 Validating step...", "#6b7280")
                self.retry_btn.config(state='disabled')
                
                # Perform validation based on step type
                if step_type == "Navigate":
                    result = self._validate_navigate(target)
                elif step_type == "Element Click":
                    result = self._validate_element_click(target)
                elif step_type == "Text Input":
                    result = self._validate_text_input(target, value)
                elif step_type == "Wait":
                    result = self._validate_wait(target)
                else:
                    result = self._validate_generic_element(target)
                
                if result['success']:
                    self._update_status(f"✅ {result['message']}", "#10b981")
                    if result.get('screenshot'):
                        self._display_screenshot(result['screenshot'])
                else:
                    self._update_status(f"❌ {result['message']}", "#ef4444")
                    
            except Exception as e:
                self._update_status(f"❌ Validation error: {str(e)}", "#ef4444")
            finally:
                self.progress_bar.stop()
                self.retry_btn.config(state='normal')
        
        threading.Thread(target=validate, daemon=True).start()
    
    def _validate_navigate(self, url):
        """Validate navigation step"""
        try:
            current_url = self.selenium_manager.driver.current_url
            if url.startswith('http'):
                return {'success': True, 'message': f"Ready to navigate to: {url}"}
            else:
                return {'success': False, 'message': "Invalid URL format"}
        except Exception as e:
            return {'success': False, 'message': f"Navigation validation failed: {str(e)}"}
    
    def _validate_element_click(self, target):
        """Validate element click step"""
        try:
            # Parse click type
            click_type = "Left"
            clean_target = target
            if '[RIGHT-CLICK]' in target:
                click_type = "Right"
                clean_target = target.replace(' [RIGHT-CLICK]', '')
            elif '[DOUBLE-CLICK]' in target:
                click_type = "Double"
                clean_target = target.replace(' [DOUBLE-CLICK]', '')
            
            # Find element
            element = self._find_element(clean_target)
            if element:
                # Take screenshot of element
                screenshot = self._capture_element_screenshot(element)
                return {
                    'success': True, 
                    'message': f"Element found! Ready for {click_type.lower()} click.",
                    'screenshot': screenshot
                }
            else:
                return {'success': False, 'message': "Element not found on current page"}
                
        except Exception as e:
            return {'success': False, 'message': f"Element validation failed: {str(e)}"}
    
    def _validate_text_input(self, target, value):
        """Validate text input step"""
        try:
            element = self._find_element(target)
            if element:
                if element.is_enabled():
                    screenshot = self._capture_element_screenshot(element)
                    return {
                        'success': True, 
                        'message': f"Input field found! Ready to enter: '{value}'",
                        'screenshot': screenshot
                    }
                else:
                    return {'success': False, 'message': "Input field is disabled"}
            else:
                return {'success': False, 'message': "Input field not found"}
                
        except Exception as e:
            return {'success': False, 'message': f"Input validation failed: {str(e)}"}
    
    def _validate_wait(self, target):
        """Validate wait step"""
        try:
            if ':' in target:
                wait_type, wait_value = target.split(':', 1)
                if wait_type.strip() == "Time" and wait_value.strip().isdigit():
                    return {'success': True, 'message': f"Ready to wait {wait_value.strip()} seconds"}
                else:
                    return {'success': False, 'message': "Invalid wait format"}
            elif target.isdigit():
                return {'success': True, 'message': f"Ready to wait {target} seconds"}
            else:
                return {'success': False, 'message': "Invalid wait value"}
                
        except Exception as e:
            return {'success': False, 'message': f"Wait validation failed: {str(e)}"}
    
    def _validate_generic_element(self, target):
        """Validate generic element step"""
        try:
            element = self._find_element(target)
            if element:
                screenshot = self._capture_element_screenshot(element)
                return {
                    'success': True, 
                    'message': "Element found and ready!",
                    'screenshot': screenshot
                }
            else:
                return {'success': False, 'message': "Element not found"}
                
        except Exception as e:
            return {'success': False, 'message': f"Element validation failed: {str(e)}"}
    
    def _find_element(self, target):
        """Find element using various locator strategies"""
        try:
            wait = WebDriverWait(self.selenium_manager.driver, 3)
            
            # Try different locator strategies
            if target.startswith('#'):
                return wait.until(EC.presence_of_element_located((By.ID, target[1:])))
            elif target.startswith('.'):
                return wait.until(EC.presence_of_element_located((By.CLASS_NAME, target[1:])))
            elif target.startswith('//'):
                return wait.until(EC.presence_of_element_located((By.XPATH, target)))
            elif '[name=' in target or '[id=' in target or '[class=' in target:
                return wait.until(EC.presence_of_element_located((By.XPATH, target)))
            else:
                return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, target)))
                
        except (TimeoutException, NoSuchElementException):
            return None
    
    def _capture_element_screenshot(self, element):
        """Capture screenshot of specific element"""
        try:
            # Get element location and size
            location = element.location
            size = element.size
            
            # Take full page screenshot
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            self.selenium_manager.driver.save_screenshot(temp_file.name)
            
            # Crop to element
            image = Image.open(temp_file.name)
            left = location['x']
            top = location['y']
            right = left + size['width']
            bottom = top + size['height']
            
            # Add padding
            padding = 10
            left = max(0, left - padding)
            top = max(0, top - padding)
            right = min(image.width, right + padding)
            bottom = min(image.height, bottom + padding)
            
            cropped = image.crop((left, top, right, bottom))
            
            # Save cropped image
            cropped_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            cropped.save(cropped_file.name)
            
            # Cleanup
            os.unlink(temp_file.name)
            
            return cropped_file.name
            
        except Exception as e:
            print(f"Screenshot capture failed: {e}")
            return None
    
    def _display_screenshot(self, screenshot_path):
        """Display screenshot in preview window"""
        try:
            if not screenshot_path or not os.path.exists(screenshot_path):
                return
            
            # Clear screenshot frame
            for widget in self.screenshot_frame.winfo_children():
                widget.destroy()
            
            # Load and resize image
            image = Image.open(screenshot_path)
            
            # Resize to fit in preview (max 400x200)
            max_width, max_height = 400, 200
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(image)
            
            # Display image
            tk.Label(self.screenshot_frame, text="📸 Element Preview:", 
                    font=('Segoe UI', 10, 'bold'), bg='#ffffff').pack(pady=(0, 5))
            
            image_label = tk.Label(self.screenshot_frame, image=photo, bg='#ffffff')
            image_label.image = photo  # Keep reference
            image_label.pack()
            
            # Cleanup temp file
            os.unlink(screenshot_path)
            
        except Exception as e:
            tk.Label(self.screenshot_frame, text=f"Screenshot error: {str(e)}", 
                    font=('Segoe UI', 9), bg='#ffffff', fg='#ef4444').pack()
    
    def _update_status(self, message, color):
        """Update status message thread-safe"""
        if hasattr(self, 'status_label') and self.status_label.winfo_exists():
            self.status_label.config(text=message, fg=color)
    
    def _close_preview(self):
        """Close preview window"""
        if self.preview_window:
            self.preview_window.destroy()
            self.preview_window = None

# Integration helper for test_steps_methods.py
def add_preview_button_to_step_form(form_frame, step_data, selenium_manager, show_popup_callback):
    """Add preview button to step creation/edit forms"""
    preview_btn = tk.Button(form_frame, text="🔍 Preview Step", font=('Segoe UI', 10, 'bold'),
                           bg='#8b5cf6', fg='#ffffff', relief='flat', padx=15, pady=8,
                           cursor='hand2', bd=0)
    
    def on_preview():
        previewer = StepPreview(selenium_manager, show_popup_callback)
        previewer.validate_and_preview_step(step_data, form_frame.winfo_toplevel())
    
    preview_btn.config(command=on_preview)
    return preview_btn
