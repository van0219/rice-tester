#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class PaginationManager:
    def __init__(self):
        # Pagination for RICE and scenarios
        self.rice_current_page = 1
        self.rice_per_page = 5
        self.rice_total_records = 0
        self.rice_per_page_options = [5, 10, 20, 50, 100]
        
        # Scenarios pagination
        self.scenarios_current_page = 1
        self.scenarios_per_page = 5
        self.scenarios_total_records = 0
        self.scenarios_per_page_options = [5, 10, 20, 50, 100]
    
    def rice_prev_page(self, ui_components, load_callback):
        """Go to previous page of RICE profiles"""
        if self.rice_current_page > 1:
            self.rice_current_page -= 1
            load_callback(ui_components)
    
    def rice_next_page(self, ui_components, load_callback):
        """Go to next page of RICE profiles"""
        total_pages = max(1, (self.rice_total_records + self.rice_per_page - 1) // self.rice_per_page)
        if self.rice_current_page < total_pages:
            self.rice_current_page += 1
            load_callback(ui_components)
    
    def scenarios_prev_page(self, ui_components, load_callback):
        """Go to previous page of scenarios"""
        if self.scenarios_current_page > 1:
            self.scenarios_current_page -= 1
            load_callback(ui_components)
    
    def scenarios_next_page(self, ui_components, load_callback):
        """Go to next page of scenarios"""
        total_pages = max(1, (self.scenarios_total_records + self.scenarios_per_page - 1) // self.scenarios_per_page)
        if self.scenarios_current_page < total_pages:
            self.scenarios_current_page += 1
            load_callback(ui_components)
    
    def change_rice_per_page(self, new_per_page, ui_components, load_callback, clear_callback):
        """Change RICE records per page and refresh"""
        self.rice_per_page = new_per_page
        # Adjust current page to stay within bounds
        max_page = max(1, (self.rice_total_records + self.rice_per_page - 1) // self.rice_per_page)
        if self.rice_current_page > max_page:
            self.rice_current_page = max_page
        load_callback(ui_components)
        clear_callback(ui_components)
    
    def change_scenarios_per_page(self, new_per_page, ui_components, load_callback):
        """Change scenarios records per page and refresh"""
        self.scenarios_per_page = new_per_page
        # Adjust current page to stay within bounds
        max_page = max(1, (self.scenarios_total_records + self.scenarios_per_page - 1) // self.scenarios_per_page)
        if self.scenarios_current_page > max_page:
            self.scenarios_current_page = max_page
        load_callback(ui_components)
