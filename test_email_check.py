#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

"""
Quick test script for Gmail API Email Check functionality
Run this to verify Gmail integration works before using in RICE Tester
"""

def test_gmail_integration():
    """Test Gmail API integration"""
    try:
        from gmail_email_checker import GmailEmailChecker
        
        print("Testing Gmail API Integration...")
        
        # Initialize checker
        checker = GmailEmailChecker()
        
        # Test setup
        print("Setting up Gmail credentials...")
        if checker.setup_credentials():
            print("SUCCESS: Gmail API setup successful!")
            
            # Test email search
            print("Testing email search...")
            search_criteria = "subject:test"
            
            # Quick check (5 second timeout for testing)
            email_data = checker.check_email_notification(search_criteria, timeout=5)
            
            if email_data:
                print(f"SUCCESS: Email found: {email_data.get('subject', 'No subject')}")
                
                # Test screenshot generation
                print("Testing email screenshot...")
                screenshot_path = checker.capture_email_content(email_data, "test_email_screenshot.png")
                print(f"SUCCESS: Screenshot saved: {screenshot_path}")
                
            else:
                print("INFO: No test emails found (this is normal)")
            
            print("SUCCESS: Gmail integration test completed successfully!")
            return True
            
        else:
            print("ERROR: Gmail API setup failed")
            return False
            
    except ImportError as e:
        print(f"ERROR: Missing dependencies: {e}")
        print("Run: pip install -r gmail_requirements.txt")
        return False
    except Exception as e:
        print(f"ERROR: Test failed: {e}")
        return False

if __name__ == "__main__":
    test_gmail_integration()