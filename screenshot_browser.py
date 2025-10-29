#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService

class BrowserManager:
    """Browser creation and management functionality"""
    
    def create_driver(self, browser_type, incognito, second_screen):
        """Create browser driver with specified options"""
        try:
            if browser_type.lower() == 'chrome':
                return self._create_chrome_driver(incognito, second_screen)
            elif browser_type.lower() == 'edge':
                return self.create_edge_driver(incognito, second_screen)
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")
        except Exception as e:
            print(f"Browser creation failed: {e}")
            # Fallback to Edge if Chrome fails
            if browser_type.lower() == 'chrome':
                print("Falling back to Edge browser...")
                return self.create_edge_driver(incognito, second_screen)
            return None
    
    def _create_chrome_driver(self, incognito, second_screen):
        """Create Chrome driver with options"""
        chrome_options = ChromeOptions()
        
        if incognito:
            chrome_options.add_argument("--incognito")
        
        # Additional Chrome options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Try system ChromeDriver first, then local
        try:
            service = ChromeService()
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except:
            # Fallback to local ChromeDriver
            chromedriver_path = os.path.join(os.getcwd(), "chromedriver-win64", "chromedriver-win64", "chromedriver.exe")
            if os.path.exists(chromedriver_path):
                service = ChromeService(chromedriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                raise Exception("ChromeDriver not found")
        
        if second_screen:
            driver.set_window_position(1920, 0)
        
        driver.maximize_window()
        return driver
    
    def create_edge_driver(self, incognito, second_screen):
        """Create Edge driver with options"""
        edge_options = EdgeOptions()
        
        if incognito:
            edge_options.add_argument("--inprivate")
        
        # Additional Edge options for stability
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-gpu")
        
        # Try system EdgeDriver first, then local
        try:
            service = EdgeService()
            driver = webdriver.Edge(service=service, options=edge_options)
        except:
            # Fallback to local EdgeDriver
            edgedriver_path = os.path.join(os.getcwd(), "edgedriver", "msedgedriver.exe")
            if os.path.exists(edgedriver_path):
                service = EdgeService(edgedriver_path)
                driver = webdriver.Edge(service=service, options=edge_options)
            else:
                raise Exception("EdgeDriver not found")
        
        if second_screen:
            driver.set_window_position(1920, 0)
        
        driver.maximize_window()
        return driver