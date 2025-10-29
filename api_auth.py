#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class APIAuthenticator:
    """Handle API-based authentication for FSM using service account details"""
    
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.service_account_data = None
        
    def load_service_account(self, account_id):
        """Load service account data from database"""
        try:
            account_data = self.db_manager.get_service_account_content(account_id)
            if account_data:
                name, file_content = account_data
                if file_content:
                    # Parse .ionapi file content (JSON format)
                    self.service_account_data = json.loads(file_content.decode('utf-8'))
                    return True
            return False
        except Exception as e:
            print(f"Error loading service account: {e}")
            return False
    
    def get_api_token_url(self):
        """Generate API token URL using service account credentials"""
        if not self.service_account_data:
            return None
            
        try:
            # Extract values from service account: pu + ot + parameters
            pu = self.service_account_data.get('pu', '')  # Base URL
            ot = self.service_account_data.get('ot', '')  # Token endpoint
            saak = self.service_account_data.get('saak', '')  # Username
            sask = self.service_account_data.get('sask', '')  # Password
            ci = self.service_account_data.get('ci', '')  # Client ID
            cs = self.service_account_data.get('cs', '')  # Client Secret
            
            # Build URL: pu + ot + ? + parameters
            base_url = f"{pu}{ot}"
            
            # URL encode the parameters
            params = {
                'username': saak,
                'password': sask,
                'client_id': ci,
                'client_secret': cs,
                'grant_type': 'password'
            }
            
            # Build the complete URL
            url_params = urllib.parse.urlencode(params)
            return f"{base_url}?{url_params}"
            
        except Exception as e:
            print(f"Error generating API token URL: {e}")
            return None
    
    def authenticate_with_api(self, driver):
        """Perform API-based authentication by navigating to token URL"""
        try:
            token_url = self.get_api_token_url()
            if not token_url:
                return False
                
            print(f"Using API authentication...")
            
            # Navigate to the API token URL
            driver.get(token_url)
            time.sleep(3)
            
            # Check if we got a token response or if we're redirected to FSM
            current_url = driver.current_url
            
            if "token" in current_url.lower() or "fsm" in current_url.lower():
                print("API authentication successful!")
                return True
            else:
                print("API authentication failed - unexpected response")
                return False
                
        except Exception as e:
            print(f"API authentication error: {e}")
            return False
    
    def get_available_service_accounts(self):
        """Get list of available service accounts"""
        try:
            accounts = self.db_manager.get_service_accounts()
            return [(acc[0], acc[1]) for acc in accounts]  # (id, name)
        except Exception as e:
            print(f"Error getting service accounts: {e}")
            return []
    
    def authenticate_scenario(self, driver, scenario_data):
        """Authenticate a scenario using API if auto_login is enabled"""
        try:
            # Check if scenario has auto_login enabled
            if not scenario_data.get('auto_login', False):
                return False
                
            # Get the first available service account
            service_accounts = self.get_available_service_accounts()
            if not service_accounts:
                print("No service accounts available for auto-login")
                return False
                
            # Use the first service account
            account_id = service_accounts[0][0]
            if self.load_service_account(account_id):
                return self.authenticate_with_api(driver)
            else:
                print("Failed to load service account for auto-login")
                return False
                
        except Exception as e:
            print(f"Scenario authentication error: {e}")
            return False