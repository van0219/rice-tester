#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_add_scenario():
    """Test the Add Scenario form"""
    try:
        from scenario_add_form_modern import ModernScenarioAddForm
        
        # Mock database manager
        class MockDB:
            user_id = 1
            def get_next_scenario_number(self, profile):
                return 1
            def get_test_users(self):
                return [(1, "Test User", "test@example.com", "encrypted_pass")]
            def get_test_step_groups(self):
                return [(1, "Login", "Login steps", 4), (2, "Navigation", "Nav steps", 3)]
            def get_test_steps_by_group(self, group_id):
                return [(1, "Navigate", "Navigate", "url", ""), (2, "Click", "Element Click", "button", "")]
        
        def mock_popup(title, message, type):
            print(f"{type}: {title} - {message}")
        
        root = tk.Tk()
        root.withdraw()
        
        form = ModernScenarioAddForm(MockDB(), mock_popup)
        form.add_scenario(1, lambda: print("Refreshed"))
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error testing Add Scenario: {e}")
        import traceback
        traceback.print_exc()

def test_edit_scenario():
    """Test the Edit Scenario form"""
    try:
        from scenario_edit_form_modern import ModernScenarioEditForm
        
        # Mock database manager
        class MockDB:
            user_id = 1
            conn = None
            def get_test_users(self):
                return [(1, "Test User", "test@example.com", "encrypted_pass")]
            def get_test_step_groups(self):
                return [(1, "Login", "Login steps", 4), (2, "Navigation", "Nav steps", 3)]
            def get_test_steps_by_group(self, group_id):
                return [(1, "Navigate", "Navigate", "url", ""), (2, "Click", "Element Click", "button", "")]
            def decrypt_password(self, encrypted):
                return "decrypted_password"
        
        def mock_popup(title, message, type):
            print(f"{type}: {title} - {message}")
        
        root = tk.Tk()
        root.withdraw()
        
        form = ModernScenarioEditForm(MockDB(), mock_popup)
        # Mock scenario data would be loaded here
        print("Edit Scenario form created successfully")
        
        root.mainloop()
        
    except Exception as e:
        print(f"Error testing Edit Scenario: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Testing Add Scenario form...")
    test_add_scenario()
    
    print("\nTesting Edit Scenario form...")
    test_edit_scenario()