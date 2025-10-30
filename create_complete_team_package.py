#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
from datetime import datetime

def create_complete_team_package():
    """Create complete RICE Tester team package with all essential files"""
    
    # Get current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Dynamically get all Python files (exclude backup, temp, debug files)
    exclude_patterns = ['_backup', '_original', 'debug_', 'temp_', 'check_', 
                       'analyze_', 'find_', 'create_team', 'create_bulletproof', 
                       'create_complete', 'create_corrected', 'create_final']
    
    # Don't exclude essential manager files
    essential_managers = ['test_steps_manager.py', 'test_users_manager.py']
    
    essential_files = []
    for file in os.listdir(current_dir):
        if file.endswith('.py'):
            # Include essential managers or files not matching exclude patterns
            if file in essential_managers or not any(pattern in file.lower() for pattern in exclude_patterns):
                essential_files.append(file)
    
    # Dynamically get essential Temp files (excluding personal_analytics.py - now in main dir)
    temp_essential = ['enhanced_popup_system.py', 'auto_updater.py', 'github_config.json', 'updater_config.json']
    temp_files = []
    temp_dir = os.path.join(current_dir, 'Temp')
    if os.path.exists(temp_dir):
        for file in temp_essential:
            if os.path.exists(os.path.join(temp_dir, file)):
                temp_files.append(file)
    
    # Other essential files
    other_files = [
        'infor_logo.ico',
        'infor_logo.png',
        'fsm_tester.db',
        'requirements.txt'
    ]
    
    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"RICE_Tester_COMPLETE_TEAM_{timestamp}.zip"
    
    print("Creating COMPLETE RICE Tester Team Package...")
    
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add Python files
        for file in essential_files:
            file_path = os.path.join(current_dir, file)
            if os.path.exists(file_path):
                zipf.write(file_path, file)
                print(f"   OK {file}")
            else:
                print(f"   MISSING: {file}")
        
        # Add Temp files (maintain Temp folder structure)
        temp_dir = os.path.join(current_dir, 'Temp')
        for file in temp_files:
            if file not in essential_files:  # Avoid duplicates
                file_path = os.path.join(temp_dir, file)
                if os.path.exists(file_path):
                    zipf.write(file_path, f"Temp/{file}")
                    print(f"   OK Temp/{file}")
        
        # Add other files
        for file in other_files:
            file_path = os.path.join(current_dir, file)
            if os.path.exists(file_path):
                zipf.write(file_path, file)
                print(f"   OK {file}")
        
        # Add setup scripts
        setup_content = '''@echo off
echo Installing RICE Tester dependencies...
pip install selenium tkinter pillow requests python-docx openpyxl matplotlib pandas
echo Setup complete!
pause
'''
        zipf.writestr('SETUP_FIRST_TIME.bat', setup_content)
        
        run_content = '''@echo off
echo Starting RICE Tester...
python RICE_Tester.py
pause
'''
        zipf.writestr('RUN_RICE_TESTER.bat', run_content)
        
        readme_content = '''# RICE Tester Team Package

## Setup Instructions:
1. Extract all files to a folder
2. Run SETUP_FIRST_TIME.bat as Administrator (one time only)
3. Use RUN_RICE_TESTER.bat for daily launches

## Requirements:
- Python 3.8+
- Internet connection for initial setup
'''
        zipf.writestr('README_TEAM.txt', readme_content)
    
    file_size = os.path.getsize(package_name) / (1024 * 1024)
    print(f"\nCOMPLETE Team Package Created!")
    print(f"Package: {package_name}")
    print(f"Size: {file_size:.1f} MB")
    
    return package_name

if __name__ == "__main__":
    create_complete_team_package()
