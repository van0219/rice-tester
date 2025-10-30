#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

from screenshot_core import ScreenshotExecutorCore

class ScreenshotExecutor(ScreenshotExecutorCore):
    """Main screenshot executor - modular architecture for memory optimization"""
    
    def __init__(self, user_id, rice_profile_id, scenario_number):
        """Initialize with all modular components"""
        super().__init__(user_id, rice_profile_id, scenario_number)
        self.safe_print(f"ScreenshotExecutor initialized for user {user_id}, profile {rice_profile_id}, scenario {scenario_number}")

if __name__ == "__main__":
    # Test the executor
    try:
        executor = ScreenshotExecutor("test_user", "test_profile", 1)
        print("[SUCCESS] ScreenshotExecutor loaded successfully!")
        methods = [method for method in dir(executor) if not method.startswith('_')]
        print(f"Available methods: {len(methods)} total")
        print("Key methods: execute_scenario, execute_step, capture_screenshot, create_driver")
    except Exception as e:
        print(f"[ERROR] Loading ScreenshotExecutor: {e}")
