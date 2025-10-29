#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

import sqlite3
from urllib.parse import urlparse

class ScreenshotUtils:
    """Utility functions for screenshot executor"""
    
    def step_contains_url(self, step_type, step_target):
        """Check if step contains URL for tenant extraction"""
        if step_type == "Navigate":
            return True
        
        # Check if step_target looks like a URL
        if step_target and ("http" in step_target or "://" in step_target):
            return True
        
        return False
    
    def extract_tenant_from_url(self, url):
        """Extract tenant ID from FSM URL"""
        try:
            if not url:
                return None
            
            # Common FSM URL patterns
            patterns = [
                "mingle-ionapi.inforcloudsuite.com/",
                "mingle-portal.inforcloudsuite.com/",
                "mingle.inforcloudsuite.com/"
            ]
            
            for pattern in patterns:
                if pattern in url:
                    # Extract tenant after the pattern
                    parts = url.split(pattern)
                    if len(parts) > 1:
                        tenant_part = parts[1].split('/')[0]
                        if tenant_part and tenant_part != "":
                            return tenant_part
            
            # Fallback: try to extract from path
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')
            if path_parts and path_parts[0]:
                return path_parts[0]
            
            return None
        except Exception as e:
            print(f"Tenant extraction failed: {e}")
            return None
    
    def is_login_step(self, step_name, step_type):
        """Check if step is a login-related step"""
        login_keywords = [
            "login", "sign in", "username", "password", 
            "authenticate", "credentials", "log in"
        ]
        
        step_name_lower = step_name.lower()
        return any(keyword in step_name_lower for keyword in login_keywords)
    
    def get_scenario_steps(self, user_id, rice_profile, scenario_number):
        """Get steps for a scenario from database - uses proper custom_value field for step values"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT 
                    ss.step_order,
                    COALESCE(ts.name, ss.step_name) as step_name,
                    COALESCE(ts.step_type, ss.step_type) as step_type,
                    COALESCE(ts.target, ss.step_target) as step_target,
                    CASE 
                        WHEN COALESCE(ts.step_type, ss.step_type) IN ('Text Input', 'Wait') 
                        THEN COALESCE(NULLIF(ss.step_description, ''), NULLIF(ss.custom_value, 'None'), ts.default_value)
                        ELSE COALESCE(ss.step_description, ts.description)
                    END as step_description,
                    COALESCE(ss.user_input_required, 0) as user_input_required
                FROM scenario_steps ss
                LEFT JOIN test_steps ts ON ss.test_step_id = ts.id
                WHERE ss.user_id = ? AND ss.rice_profile = ? AND ss.scenario_number = ?
                ORDER BY ss.step_order
            ''', (user_id, rice_profile, scenario_number))
            
            return cursor.fetchall()
        except Exception as e:
            self.safe_print(f"Failed to get scenario steps: {e}")
            return []
        finally:
            conn.close()
    
    def get_browser_config(self, user_id, rice_profile):
        """Get browser configuration from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT browser_type, second_screen, incognito
                FROM global_config 
                WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if result:
                return {
                    'browser_type': result[0] or 'chrome',
                    'incognito': bool(result[2]),
                    'second_screen': bool(result[1])
                }
            else:
                return {
                    'browser_type': 'chrome',
                    'incognito': False,
                    'second_screen': False
                }
        except Exception as e:
            self.safe_print(f"Failed to get browser config: {e}")
            return {
                'browser_type': 'chrome',
                'incognito': False,
                'second_screen': False
            }
        finally:
            conn.close()
    
    def update_scenario_status(self, user_id, rice_profile, scenario_number, status):
        """Update scenario execution status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE scenarios 
                SET execution_status = ?, last_executed = datetime('now')
                WHERE user_id = ? AND rice_profile = ? AND scenario_number = ?
            ''', (status, user_id, rice_profile, scenario_number))
            conn.commit()
        except Exception as e:
            self.safe_print(f"Failed to update scenario status: {e}")
        finally:
            conn.close()