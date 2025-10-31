#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning"""
    dialog.withdraw()
    dialog.update_idletasks()
    
    # Get dimensions
    if width and height:
        dialog.geometry(f"{width}x{height}")
    
    dialog.update_idletasks()
    w = dialog.winfo_reqwidth() if not width else width
    h = dialog.winfo_reqheight() if not height else height
    
    # CSS-like centering: top 50%, left 50%, transform translate(-50%, -50%)
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.deiconify()
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()
import os
import time

class SeleniumManager:
    def __init__(self):
        self.driver = None
    
    def create_driver(self, browser_type="edge", incognito=False, second_screen=False):
        """Create and configure browser driver"""
        if browser_type == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            if incognito:
                options.add_argument("--incognito")
            if second_screen:
                options.add_argument("--window-position=1920,0")
            
            try:
                if WEBDRIVER_MANAGER_AVAILABLE:
                    # Use WebDriver Manager for automatic version management
                    service = ChromeService(ChromeDriverManager().install())
                    self.driver = webdriver.Chrome(service=service, options=options)
                else:
                    # Try local ChromeDriver first
                    chrome_paths = [
                        os.path.join(os.getcwd(), "chromedriver.exe"),
                        os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver.exe"),
                        os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver-win64", "chromedriver.exe")
                    ]
                    local_driver = next((p for p in chrome_paths if os.path.exists(p)), None)
                    
                    if local_driver:
                        service = ChromeService(local_driver)
                        self.driver = webdriver.Chrome(service=service, options=options)
                    else:
                        # Try system ChromeDriver
                        self.driver = webdriver.Chrome(options=options)
            except Exception as e:
                print(f"Chrome driver failed: {e}")
                # Fallback to Edge
                return self.create_driver("edge", incognito, second_screen)
        else:
            options = webdriver.EdgeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--ignore-certificate-errors")
            if incognito:
                options.add_argument("--inprivate")
            if second_screen:
                options.add_argument("--window-position=1920,0")
            
            try:
                if WEBDRIVER_MANAGER_AVAILABLE:
                    # Use WebDriver Manager for automatic version management
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    self.driver = webdriver.Edge(service=service, options=options)
                else:
                    # Try local EdgeDriver first
                    driver_path = os.path.join(os.getcwd(), "edgedriver", "msedgedriver.exe")
                    if os.path.exists(driver_path):
                        service = EdgeService(driver_path)
                        self.driver = webdriver.Edge(service=service, options=options)
                    else:
                        # Try system EdgeDriver
                        self.driver = webdriver.Edge(options=options)
            except Exception as e:
                print(f"Edge driver failed: {e}")
                # Fallback to Chrome if Edge fails
                return self.create_driver("chrome", incognito, second_screen)
        
        if self.driver:
            self.driver.maximize_window()
        
        return self.driver
    
    def login_to_fsm(self, url, username, password):
        """Perform FSM login"""
        if not self.driver:
            raise Exception("Driver not initialized")
        
        self.driver.set_page_load_timeout(30)
        self.driver.get(url)
        
        wait = WebDriverWait(self.driver, 10)
        time.sleep(3)
        
        # Find and fill username
        username_field = wait.until(EC.presence_of_element_located((By.ID, "username")))
        username_field.clear()
        username_field.send_keys(username)
        
        # Find and fill password
        password_field = self.driver.find_element(By.ID, "pass")
        password_field.clear()
        password_field.send_keys(password)
        
        # Find and click login button
        login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        
        time.sleep(3)
        
        # Check for successful login
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "login" not in driver.current_url.lower()
            )
            return True
        except:
            return False
    
    def navigate_to_page(self, url):
        """Navigate to a specific page"""
        if not self.driver:
            raise Exception("Driver not initialized")
        
        self.driver.get(url)
        self.wait_for_page_stability()
    
    def wait_for_page_stability(self):
        """Wait for page to stabilize"""
        if not self.driver:
            return
        
        try:
            # Wait for document ready state
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            # Additional wait for dynamic content
            time.sleep(2)
            
            # Check for jQuery if available
            try:
                WebDriverWait(self.driver, 5).until(
                    lambda driver: driver.execute_script("return typeof jQuery !== 'undefined' ? jQuery.active == 0 : true")
                )
            except:
                pass  # jQuery not available or timeout
                
        except Exception:
            pass  # Continue even if stability checks fail
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.driver = None
