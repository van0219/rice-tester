#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8
sys.path.append(r'd:\AmazonQ\InforQ\RICE_Tester')

# Test the TES-070 generator
try:
    from tes070_generator import generate_tes070_report
    from database_manager import DatabaseManager
    
    print("Testing TES-070 generator...")
    
    # Create a mock database manager with user_id
    db_manager = DatabaseManager(user_id=1)
    
    # Test with a simple rice profile
    generate_tes070_report(
        rice_profile="TEST001", 
        show_popup=None,  # No popup for testing
        current_user={'full_name': 'Test User'},
        db_manager=db_manager
    )
    
    print("SUCCESS: TES-070 generator test completed successfully!")
    
except Exception as e:
    print(f"ERROR in TES-070 generator: {str(e)}")
    import traceback
    traceback.print_exc()