#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from urllib.parse import urlparse

class StepExecutor:
    """Step execution functionality"""
    
    def __init__(self):
        # Initialize step cache for storing values
        self.step_cache = {}
    
    def execute_step(self, step_data, current_step=1, total_steps=1):
        """Execute a single step with screenshots and progress updates"""
        step_order, step_name, step_type, step_target, step_description, user_input_required = step_data
        
        print(f"[STEP DEBUG] Raw step data: {step_data}")
        print(f"[STEP DEBUG] Step {current_step}: name='{step_name}', type='{step_type}', target='{step_target}', desc='{step_description}'")
        
        # Force step type detection if None
        if step_type is None:
            step_type = self._detect_step_type(step_name, step_target, step_description)
            print(f"[STEP DEBUG] Detected step type: '{step_type}'")
        
        self.safe_print(f"Executing Step {current_step}/{total_steps}: {step_name}")
        
        # Update progress if callback is available
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, "Starting...")
        
        # Capture before screenshot (skip for Wait steps)
        screenshot_before = None if step_type == "Wait" else self.capture_screenshot()
        
        try:
            # Handle user input steps
            if user_input_required:
                if not self.wait_for_user_input(step_name, step_description):
                    return False
                screenshot_after = self.capture_screenshot()
                self.save_screenshot_to_db(step_order, screenshot_before, screenshot_after, "completed")
                return True
            
            # Execute step based on type
            print(f"[STEP EXECUTION] About to execute step type: '{step_type}'")
            success = self._execute_step_by_type(step_type, step_target, step_description, step_name, current_step, total_steps)
            
            # Capture after screenshot with proper timing (skip for Wait steps)
            if step_type == "Wait":
                screenshot_after = None
            else:
                # Add step-specific wait before capturing after screenshot
                if step_type == 'Text Input':
                    time.sleep(0.5)  # Allow text entry to complete
                elif step_type == 'Element Click':
                    time.sleep(0.8)  # Allow click effects to manifest
                elif step_type == 'Navigate':
                    time.sleep(1)  # Additional buffer for dynamic content
                elif step_type == 'JavaScript Execute':
                    time.sleep(1.5)  # Allow script execution
                elif step_type == 'Get Text':
                    time.sleep(0.3)  # Allow text extraction to complete
                else:
                    time.sleep(0.5)  # General wait
                
                screenshot_after = self.capture_screenshot()
            
            # Save to database
            status = "completed" if success else "failed"
            self.save_screenshot_to_db(step_order, screenshot_before, screenshot_after, status)
            
            # Update progress
            if self.progress_callback:
                if success:
                    self.progress_callback(current_step, total_steps, step_name, "[SUCCESS] Completed")
                else:
                    self.progress_callback(current_step, total_steps, step_name, "[FAILED] Failed")
            
            return success
            
        except Exception as e:
            self.safe_print(f"Step execution failed: {e}")
            screenshot_after = self.capture_screenshot()
            self.save_screenshot_to_db(step_order, screenshot_before, screenshot_after, "failed")
            
            if self.progress_callback:
                self.progress_callback(current_step, total_steps, step_name, f"[FAILED] Failed: {str(e)}")
            
            return False
    
    def _execute_step_by_type(self, step_type, step_target, step_description, step_name, current_step, total_steps):
        """Execute step based on its type"""
        try:
            if step_type in ["Navigate", "Web Navigation"]:
                return self._execute_navigate(step_target, step_name, current_step, total_steps)
            elif step_type == "Element Click":
                return self._execute_element_click(step_target, step_name, current_step, total_steps)
            elif step_type == "Text Input":
                return self._execute_text_input(step_target, step_description, step_name, current_step, total_steps)
            elif step_type == "JavaScript Execute":
                return self._execute_javascript(step_target, step_name, current_step, total_steps)
            elif step_type == "Wait":
                # For Wait steps, the wait time is in step_description (from custom_value)
                return self._execute_wait(step_description)
            elif step_type == "Get Text":
                return self._execute_get_text(step_target, step_name, current_step, total_steps)
            elif step_type == "Get Attribute":
                return self._execute_get_attribute(step_target, step_name, current_step, total_steps)
            elif step_type == "Email Check":
                return self._execute_email_check(step_target, step_name, current_step, total_steps)
            else:
                self.safe_print(f"Unknown step type: {step_type}")
                return False
        except Exception as e:
            self.safe_print(f"Step type execution failed: {e}")
            return False
    
    def _execute_navigate(self, url, step_name, current_step, total_steps):
        """Execute navigation step"""
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, f"Navigating to {url}")
        
        try:
            # Check if driver exists
            if not self.driver:
                self.safe_print("No browser driver available")
                return False
            
            # Check if already on the same page
            try:
                current_url = self.driver.current_url
                if self._urls_match(current_url, url):
                    self.safe_print(f"Already on target page: {url}")
                    return True
            except:
                # If we can't get current URL, continue with navigation
                pass
            
            self.safe_print(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page load with timeout
            try:
                WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.execute_script("return document.readyState") == "complete"
                )
                self.safe_print(f"Navigation successful to: {url}")
                return True
            except TimeoutException:
                self.safe_print(f"Navigation timeout for: {url}, but continuing...")
                return True  # Continue execution even if timeout
                
        except Exception as e:
            self.safe_print(f"Navigation failed for {url}: {str(e)}")
            import traceback
            self.safe_print(f"Navigation traceback: {traceback.format_exc()}")
            return False
    
    def _execute_element_click(self, selector, step_name, current_step, total_steps):
        """Execute element click step"""
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, "Clicking element...")
        
        try:
            # Check for right-click
            is_right_click = "right-click" in step_name.lower() or "right click" in step_name.lower()
            
            if is_right_click:
                return self._execute_right_click(selector, step_name, current_step, total_steps)
            else:
                return self._execute_left_click(selector)
        except Exception as e:
            self.safe_print(f"Element click failed: {e}")
            return False
    
    def _execute_left_click(self, selector):
        """Execute left click on element"""
        # Handle both comma and pipe separated selectors
        if '|' in selector:
            selectors = [s.strip() for s in selector.split('|')]
        else:
            selectors = [s.strip() for s in selector.split(',')]
        
        for sel in selectors:
            try:
                # Determine selector type and use appropriate locator
                if sel.startswith('//'):
                    # XPath selector
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    )
                else:
                    # CSS selector
                    element = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                    )
                element.click()
                time.sleep(1)
                return True
            except:
                continue
        
        return False
    
    def _execute_right_click(self, selector, step_name, current_step, total_steps):
        """Execute right-click on element"""
        # Handle both comma and pipe separated selectors
        if '|' in selector:
            selectors = [s.strip() for s in selector.split('|')]
        else:
            selectors = [s.strip() for s in selector.split(',')]
        
        for sel in selectors:
            try:
                # Determine selector type and use appropriate locator
                if sel.startswith('//'):
                    # XPath selector
                    element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, sel))
                    )
                else:
                    # CSS selector
                    element = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, sel))
                    )
                
                # First left-click to select
                element.click()
                time.sleep(0.5)
                
                # Then right-click
                actions = ActionChains(self.driver)
                actions.context_click(element).perform()
                time.sleep(1)
                return True
            except:
                continue
        
        return False
    
    def _execute_text_input(self, selector, text_value, step_name, current_step, total_steps):
        """Execute text input step"""
        # Replace any cached values in the text
        processed_text = self._replace_cached_values(text_value)
        
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, f"Entering: '{processed_text}'")
        
        try:
            if selector.startswith('#'):
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
            else:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
            
            element.click()
            time.sleep(0.5)
            element.clear()
            print(f"[VARIABLE USAGE] Original text: '{text_value}' -> Processed text: '{processed_text}'")
            print(f"[CACHE STATUS] Available variables: {list(self.step_cache.keys())}")
            element.send_keys(processed_text)
            return True
                
        except Exception as e:
            self.safe_print(f"Text input failed: {e}")
            return False
    
    def _execute_javascript(self, script, step_name, current_step, total_steps):
        """Execute JavaScript step"""
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, "Executing JavaScript...")
        
        try:
            # Handle Enter key simulation with multiple methods
            if "enter" in script.lower() or "keydown" in script.lower():
                return self._execute_enter_key()
            
            # Execute the JavaScript
            self.driver.execute_script(script)
            time.sleep(2)
            
            # Wait for any loading indicators
            self._wait_for_loading()
            
            return True
        except Exception as e:
            self.safe_print(f"JavaScript execution failed: {e}")
            return False
    
    def _execute_enter_key(self):
        """Execute Enter key with multiple fallback methods"""
        try:
            # Method 1: Direct Selenium Keys.ENTER
            active_element = self.driver.switch_to.active_element
            active_element.send_keys(Keys.ENTER)
            time.sleep(1)
            return True
        except:
            try:
                # Method 2: JavaScript dispatchEvent
                script = """
                var event = new KeyboardEvent('keydown', {
                    key: 'Enter',
                    code: 'Enter',
                    keyCode: 13,
                    which: 13,
                    bubbles: true
                });
                document.activeElement.dispatchEvent(event);
                """
                self.driver.execute_script(script)
                time.sleep(1)
                return True
            except:
                try:
                    # Method 3: Form submission
                    script = """
                    var forms = document.forms;
                    for (var i = 0; i < forms.length; i++) {
                        if (forms[i].contains(document.activeElement)) {
                            forms[i].submit();
                            break;
                        }
                    }
                    """
                    self.driver.execute_script(script)
                    time.sleep(1)
                    return True
                except:
                    return False
    
    def _execute_wait(self, duration):
        """Execute wait step - duration should be the actual wait time from custom_value"""
        try:
            # For Wait steps, duration parameter contains the actual wait time (from custom_value)
            if isinstance(duration, str) and duration.startswith('Time (seconds):'):
                # Handle old format "Time (seconds): 3"
                wait_time = float(duration.split(':')[1].strip())
            else:
                # Handle new format - direct value "3"
                wait_time = float(duration)
            
            print(f"[WAIT DEBUG] Waiting for {wait_time} seconds...")
            time.sleep(wait_time)
            return True
        except Exception as e:
            print(f"[WAIT ERROR] Failed to parse wait time '{duration}': {e}")
            time.sleep(2)  # Default wait
            return True
    
    def _execute_get_text(self, selector, step_name, current_step, total_steps):
        """Execute get text step and cache the value"""
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, "Getting text...")
        
        try:
            # Parse selector and cache name
            cache_name = None
            actual_selector = selector
            
            if ' | CACHE:' in selector:
                parts = selector.split(' | CACHE:')
                actual_selector = parts[0].strip()
                cache_name = parts[1].strip() if len(parts) > 1 else None
                self.safe_print(f"[CACHE CONFIG] Custom cache name specified: '{cache_name}'")
            else:
                self.safe_print(f"[CACHE CONFIG] No custom cache name, will use default pattern")
            
            # Handle both comma and pipe separated selectors
            if '|' in actual_selector and ' | CACHE:' not in selector:
                selectors = [s.strip() for s in actual_selector.split('|')]
            elif ',' in actual_selector:
                selectors = [s.strip() for s in actual_selector.split(',')]
            else:
                selectors = [actual_selector.strip()]
            
            for sel in selectors:
                try:
                    # Determine selector type and use appropriate locator
                    if sel.startswith('//'):
                        # XPath selector
                        element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, sel))
                        )
                    else:
                        # CSS selector
                        element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                        )
                    
                    # Get the text content
                    text_value = element.text.strip()
                    self.safe_print(f"[GET TEXT] Extracted: '{text_value or '[EMPTY]'}' from: {sel}")
                    
                    # Log the extracted value (especially for work unit)
                    if "work unit" in step_name.lower() or "workunit" in step_name.lower():
                        self.safe_print(f"EXTRACTED WORK UNIT: '{text_value or '[BLANK]'}'")
                    
                    # Cache the value with custom name or default
                    if cache_name:
                        cache_key = cache_name
                        self.safe_print(f"[CACHE KEY] Using custom cache key: '{cache_key}'")
                    else:
                        cache_key = f"step_{current_step}_{step_name.replace(' ', '_')}"
                        self.safe_print(f"[CACHE KEY] Generated default cache key: '{cache_key}'")
                    
                    self.step_cache[cache_key] = text_value
                    
                    print(f"[VARIABLE CAPTURE] Text retrieved: '{text_value}' -> cached as '{cache_key}'")
                    print(f"[CACHE STATUS] Current cache contents: {self.step_cache}")
                    
                    # Update progress with captured value
                    if self.progress_callback:
                        self.progress_callback(current_step, total_steps, step_name, f"Captured: '{text_value}'")
                    
                    # Special logging for workunit capture
                    if 'workunit' in step_name.lower():
                        print(f"[WORKUNIT CAPTURE] *** WORKUNIT CAPTURED: '{text_value}' as key '{cache_key}' ***")
                        print(f"[WORKUNIT CACHE] Available for variable replacement: ${{{cache_key}}}")
                    return True
                    
                except Exception as e:
                    self.safe_print(f"Selector '{sel}' failed: {e}")
                    continue
            
            self.safe_print("All selectors failed for Get Text step")
            return False
            
        except Exception as e:
            self.safe_print(f"Get Text execution failed: {e}")
            return False
    
    def _execute_get_attribute(self, selector, step_name, current_step, total_steps):
        """Execute get attribute step and cache the value"""
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, "Getting attribute...")
        
        try:
            # Parse selector, attribute, and cache name
            parts = selector.split(' | ')
            actual_selector = parts[0].strip()
            attribute_name = parts[1].strip() if len(parts) > 1 else 'href'
            
            cache_name = None
            if len(parts) > 2 and parts[2].startswith('CACHE:'):
                cache_name = parts[2].replace('CACHE:', '').strip()
                print(f"[CACHE CONFIG] Custom cache name specified: '{cache_name}'")
            
            # Handle multiple selectors
            if ',' in actual_selector:
                selectors = [s.strip() for s in actual_selector.split(',')]
            else:
                selectors = [actual_selector.strip()]
            
            for sel in selectors:
                try:
                    # Determine selector type and use appropriate locator
                    if sel.startswith('//'):
                        element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, sel))
                        )
                    else:
                        element = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, sel))
                        )
                    
                    # Get the attribute value
                    attr_value = element.get_attribute(attribute_name)
                    if attr_value:
                        attr_value = attr_value.strip()
                    
                    # Cache the value if cache name provided
                    if cache_name:
                        cache_key = cache_name
                        print(f"[CACHE KEY] Using custom cache key: '{cache_key}'")
                    else:
                        cache_key = f"step_{current_step}_{step_name.replace(' ', '_')}"
                        print(f"[CACHE KEY] Generated default cache key: '{cache_key}'")
                    
                    self.step_cache[cache_key] = attr_value or ''
                    
                    print(f"[ATTRIBUTE CAPTURE] Attribute '{attribute_name}' retrieved: '{attr_value}' -> cached as '{cache_key}'")
                    print(f"[CACHE STATUS] Current cache contents: {self.step_cache}")
                    return True
                    
                except Exception as e:
                    self.safe_print(f"Selector '{sel}' failed: {e}")
                    continue
            
            self.safe_print("All selectors failed for Get Attribute step")
            return False
            
        except Exception as e:
            self.safe_print(f"Get Attribute execution failed: {e}")
            return False
    
    def _replace_cached_values(self, text):
        """Replace cached value references in text with actual values"""
        if not text or not self.step_cache:
            print(f"[VARIABLE DEBUG] No text or empty cache - text: '{text}', cache: {self.step_cache}")
            return text
        
        # Replace patterns like ${step_3_Get_Column_Value} with cached values
        import re
        pattern = r'\$\{([^}]+)\}'
        
        def replace_match(match):
            cache_key = match.group(1)
            cached_value = self.step_cache.get(cache_key, match.group(0))
            print(f"[VARIABLE REPLACE] Looking for '{cache_key}' -> Found: '{cached_value}'")
            
            # Special logging for workunit replacement
            if 'workunit' in cache_key.lower():
                print(f"[WORKUNIT REPLACE] *** REPLACING WORKUNIT VARIABLE ***")
                print(f"[WORKUNIT REPLACE] Variable: ${{{cache_key}}} -> Value: '{cached_value}'")
                if cached_value == match.group(0):  # No replacement happened
                    print(f"[WORKUNIT ERROR] Variable not found in cache! Available keys: {list(self.step_cache.keys())}")
            
            return cached_value
        
        result = re.sub(pattern, replace_match, text)
        print(f"[VARIABLE FINAL] '{text}' -> '{result}'")
        return result
    
    def _wait_for_loading(self):
        """Wait for loading indicators to disappear"""
        try:
            # Wait for common loading indicators
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'loading')]"))
            )
        except:
            pass
        
        try:
            # Wait for table rows to appear (for search results)
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//tr[position()>1]"))
            )
        except:
            pass
    
    def _urls_match(self, url1, url2):
        """Check if two URLs point to the same page"""
        try:
            parsed1 = urlparse(url1)
            parsed2 = urlparse(url2)
            return (parsed1.netloc == parsed2.netloc and 
                    parsed1.path == parsed2.path)
        except:
            return False
    
    def _detect_step_type(self, step_name, step_target, step_description):
        """Detect step type based on step name and content"""
        if not step_name:
            return "Unknown"
        
        step_name_lower = step_name.lower()
        
        # Navigation steps
        if any(keyword in step_name_lower for keyword in ["navigate", "page", "go to"]):
            return "Navigate"
        
        # Click steps
        if any(keyword in step_name_lower for keyword in ["click", "button", "select"]):
            return "Element Click"
        
        # Text input steps
        if any(keyword in step_name_lower for keyword in ["enter", "input", "type", "search"]) and "${" in str(step_description):
            return "Text Input"
        
        # Get text steps
        if any(keyword in step_name_lower for keyword in ["get", "capture", "extract", "workunit", "work unit"]):
            return "Get Text"
        
        # Wait steps
        if any(keyword in step_name_lower for keyword in ["wait", "pause"]):
            return "Wait"
        
        # JavaScript steps
        if any(keyword in step_name_lower for keyword in ["press enter", "javascript", "script"]):
            return "JavaScript Execute"
        
        # Default based on content
        if step_target and ("http" in str(step_target) or "://" in str(step_target)):
            return "Navigate"
        
        return "Element Click"  # Default fallback
    
    def _execute_email_check(self, step_target, step_name, current_step, total_steps):
        """Execute email check step using Gmail API"""
        if self.progress_callback:
            self.progress_callback(current_step, total_steps, step_name, "Checking email...")
        
        try:
            # Parse step target: "SEARCH:criteria | CONTENT:expected | TIMEOUT:60"
            search_criteria = ""
            expected_content = []
            timeout = 60
            
            if step_target:
                parts = step_target.split(" | ")
                for part in parts:
                    if part.startswith("SEARCH:"):
                        search_criteria = part.replace("SEARCH:", "").strip()
                    elif part.startswith("CONTENT:"):
                        content_str = part.replace("CONTENT:", "").strip()
                        if content_str:
                            expected_content = [c.strip() for c in content_str.split(",")]
                    elif part.startswith("TIMEOUT:"):
                        try:
                            timeout = int(part.replace("TIMEOUT:", "").strip())
                        except:
                            timeout = 60
            
            if not search_criteria:
                self.safe_print("No search criteria provided for email check")
                return False
            
            # Initialize Gmail checker
            from gmail_email_checker import GmailEmailChecker
            gmail_checker = GmailEmailChecker()
            
            # Update progress
            if self.progress_callback:
                self.progress_callback(current_step, total_steps, step_name, f"Searching: {search_criteria}")
            
            # Check for email
            if expected_content:
                # Verify email with content
                success = gmail_checker.verify_email_content(search_criteria, expected_content, timeout)
                if success:
                    self.safe_print(f"Email found with expected content: {expected_content}")
                else:
                    self.safe_print(f"Email not found or missing expected content: {expected_content}")
            else:
                # Just check for email existence
                email_data = gmail_checker.check_email_notification(search_criteria, timeout)
                success = email_data is not None
                if success:
                    self.safe_print(f"Email found: {email_data.get('subject', 'No subject')}")
                    
                    # Create email screenshot for documentation
                    try:
                        screenshot_path = f"email_screenshot_step_{current_step}.png"
                        gmail_checker.capture_email_content(email_data, screenshot_path)
                        self.safe_print(f"Email screenshot saved: {screenshot_path}")
                    except Exception as e:
                        self.safe_print(f"Email screenshot failed: {e}")
                else:
                    self.safe_print(f"No email found matching criteria: {search_criteria}")
            
            # Update progress with result
            if self.progress_callback:
                if success:
                    self.progress_callback(current_step, total_steps, step_name, "✅ Email verified")
                else:
                    self.progress_callback(current_step, total_steps, step_name, "❌ Email not found")
            
            return success
            
        except Exception as e:
            self.safe_print(f"Email check failed: {e}")
            if self.progress_callback:
                self.progress_callback(current_step, total_steps, step_name, f"❌ Error: {str(e)}")
            return False
