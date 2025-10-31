#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import traceback

def test_add_scenario():
    """Test the add scenario form in isolation"""
    try:
        print("Testing Add Scenario form...")
        
        # Mock database manager
        class MockDB:
            user_id = 1
            conn = None
            def get_next_scenario_number(self, profile):
                return 1
            def get_test_users(self):
                return [(1, "Test User", "test@example.com", "encrypted_pass")]
            def get_test_step_groups(self):
                return [(1, "Login", "Login steps", 4)]
            def get_test_steps_by_group(self, group_id):
                return [(1, "Navigate", "Navigate", "url", "")]
            def decrypt_password(self, encrypted):
                return "test_password"
        
        def mock_popup(title, message, type):
            print(f"{type}: {title} - {message}")
        
        print("Importing ModernScenarioAddForm...")
        from scenario_add_form_modern import ModernScenarioAddForm
        
        print("Creating form instance...")
        form = ModernScenarioAddForm(MockDB(), mock_popup)
        
        print("Calling add_scenario...")
        form.add_scenario(1, lambda: print("Refreshed"))
        
        print("Form created successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide root window
    
    # Test the form
    test_add_scenario()
    
    # Keep window alive for testing
    root.mainloop()