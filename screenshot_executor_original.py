#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
os.system('chcp 65001 >nul 2>&1')  # Set Windows console to UTF-8

from screenshot_core import ScreenshotExecutorCore

class ScreenshotExecutor(ScreenshotExecutorCore):
    """Main screenshot executor - imports all functionality from modular components"""
    pass

if __name__ == "__main__":
    # Test the executor
    executor = ScreenshotExecutor("test_user", "test_profile", 1)
    print("ScreenshotExecutor loaded successfully!")
