#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class VisualElementPicker:
    """Visual element picker for Phase 3 advanced features"""
    
    def __init__(self, db_manager, show_popup_callback):
        self.db_manager = db_manager
        self.show_popup = show_popup_callback
        self.driver = None
        self.picking = False
        self.selected_element = None
        self.picker_dialog = None
    
    def show_element_picker(self, parent, callback):
        """Show visual element picker interface"""
        self.callback = callback
        
        dialog = tk.Toplevel(parent)
        dialog.title("🎯 Visual Element Picker")
        dialog.configure(bg='#ffffff')
        dialog.geometry("600x500")
        dialog.resizable(True, True)
        dialog.minsize(500, 400)
        dialog.transient(parent)
        dialog.grab_set()
        
        try:
            dialog.iconbitmap("infor_logo.ico")
        except:
            pass
        
        # Enhanced header
        header_frame = tk.Frame(dialog, bg='#f59e0b', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#f59e0b')
        header_content.pack(fill='both', expand=True, padx=25, pady=20)
        
        title_frame = tk.Frame(header_content, bg='#f59e0b')
        title_frame.pack(side='left')
        
        tk.Label(title_frame, text="🎯 Visual Element Picker", 
                font=('Segoe UI', 16, 'bold'), bg='#f59e0b', fg='#ffffff').pack(anchor='w')
        tk.Label(title_frame, text="Click elements in browser to capture selectors", 
                font=('Segoe UI', 10), bg='#f59e0b', fg='#fef3c7').pack(anchor='w')
        
        # Status indicator
        self.picker_status = tk.Label(header_content, text="● Ready", 
                                     font=('Segoe UI', 12, 'bold'), bg='#f59e0b', fg='#ffffff')
        self.picker_status.pack(side='right')
        
        # Main content
        content_frame = tk.Frame(dialog, bg='#ffffff', padx=25, pady=25)
        content_frame.pack(fill='both', expand=True)
        
        # Instructions
        instructions_frame = tk.Frame(content_frame, bg='#fef3c7', relief='solid', bd=1)
        instructions_frame.pack(fill='x', pady=(0, 20))
        
        inst_header = tk.Frame(instructions_frame, bg='#f59e0b', height=35)
        inst_header.pack(fill='x')
        inst_header.pack_propagate(False)
        
        tk.Label(inst_header, text="📋 How to Use", font=('Segoe UI', 11, 'bold'), 
                bg='#f59e0b', fg='#ffffff').pack(expand=True)
        
        inst_content = tk.Frame(instructions_frame, bg='#fef3c7')
        inst_content.pack(fill='x', padx=15, pady=12)
        
        instructions = [
            "1️⃣ Enter the URL of the page you want to pick elements from",
            "2️⃣ Click 'Launch Browser' to open the page",
            "3️⃣ Click 'Start Picking' to enable element selection mode",
            "4️⃣ Click any element in the browser to capture its selector",
            "5️⃣ Review and use the captured selector information"
        ]
        
        for instruction in instructions:
            tk.Label(inst_content, text=instruction, font=('Segoe UI', 9), 
                    bg='#fef3c7', fg='#92400e', anchor='w').pack(fill='x', pady=1)
        
        # URL Configuration
        url_frame = tk.Frame(content_frame, bg='#ffffff')
        url_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(url_frame, text="🌐 Target URL:", font=('Segoe UI', 11, 'bold'), 
                bg='#ffffff', fg='#374151').pack(anchor='w', pady=(0, 5))
        
        self.url_var = tk.StringVar()
        url_entry = tk.Entry(url_frame, textvariable=self.url_var, font=('Segoe UI', 10),
                            relief='solid', bd=1, highlightthickness=1, highlightcolor='#f59e0b')
        url_entry.pack(fill='x', ipady=6)
        
        # Set default URL from browser config
        browser_config = self.get_browser_config()
        if browser_config and browser_config.get('base_url'):
            self.url_var.set(browser_config['base_url'])
        else:
            self.url_var.set("https://mingle-portal.inforcloudsuite.com/TAMICS10_AX1")
        
        # Controls
        controls_frame = tk.Frame(content_frame, bg='#ffffff')
        controls_frame.pack(fill='x', pady=(0, 20))
        
        self.launch_btn = tk.Button(controls_frame, text="🚀 Launch Browser", 
                                   font=('Segoe UI', 11, 'bold'), bg='#10b981', fg='#ffffff',
                                   relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                                   command=self.launch_browser)\n        self.launch_btn.pack(side='left', padx=(0, 10))
        
        self.pick_btn = tk.Button(controls_frame, text="🎯 Start Picking", 
                                 font=('Segoe UI', 11, 'bold'), bg='#f59e0b', fg='#ffffff',
                                 relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                                 command=self.start_picking, state='disabled')
        self.pick_btn.pack(side='left', padx=(0, 10))
        
        self.stop_btn = tk.Button(controls_frame, text="⏹️ Stop Picking", 
                                 font=('Segoe UI', 11, 'bold'), bg='#ef4444', fg='#ffffff',
                                 relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                                 command=self.stop_picking, state='disabled')
        self.stop_btn.pack(side='left')
        
        # Element Information Display
        info_frame = tk.Frame(content_frame, bg='#f8fafc', relief='solid', bd=1)
        info_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        info_header = tk.Frame(info_frame, bg='#e5e7eb', height=35)
        info_header.pack(fill='x')
        info_header.pack_propagate(False)
        
        tk.Label(info_header, text="🔍 Selected Element", font=('Segoe UI', 11, 'bold'), 
                bg='#e5e7eb', fg='#374151').pack(expand=True)
        
        self.info_content = tk.Frame(info_frame, bg='#f8fafc')
        self.info_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Initial message
        self.info_label = tk.Label(self.info_content, text="No element selected", 
                                  font=('Segoe UI', 10), bg='#f8fafc', fg='#6b7280')
        self.info_label.pack(expand=True)
        
        # Bottom buttons
        bottom_frame = tk.Frame(content_frame, bg='#ffffff')
        bottom_frame.pack(fill='x')
        
        self.use_btn = tk.Button(bottom_frame, text="✨ Use Element", 
                                font=('Segoe UI', 11, 'bold'), bg='#8b5cf6', fg='#ffffff',
                                relief='flat', padx=20, pady=10, cursor='hand2', bd=0,
                                command=self.use_selected_element, state='disabled')
        self.use_btn.pack(side='left', padx=(0, 10))
        
        tk.Button(bottom_frame, text="❌ Close", font=('Segoe UI', 11, 'bold'),
                 bg='#6b7280', fg='#ffffff', relief='flat', padx=20, pady=10,
                 cursor='hand2', bd=0, command=self.close_picker).pack(side='right')
        
        self.picker_dialog = dialog
    
    def get_browser_config(self):
        """Get browser configuration"""
        try:
            config = self.db_manager.get_global_config()
            if config:
                return {
                    'browser_type': config[1],
                    'base_url': config[4],
                    'incognito_mode': config[3]
                }
        except:
            pass
        return None
    
    def launch_browser(self):
        """Launch browser for element picking"""
        try:
            url = self.url_var.get().strip()
            if not url:
                self.show_popup("Error", "Please enter a URL", "error")
                return
            
            # Get browser config
            browser_config = self.get_browser_config()
            browser_type = browser_config.get('browser_type', 'chrome').lower() if browser_config else 'chrome'
            
            # Setup browser options
            if browser_type == 'edge':
                from selenium.webdriver.edge.options import Options
                options = Options()
            else:
                from selenium.webdriver.chrome.options import Options
                options = Options()
            
            # Common options
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            if browser_config and browser_config.get('incognito_mode'):
                if browser_type == 'edge':
                    options.add_argument("--inprivate")
                else:
                    options.add_argument("--incognito")
            
            # Launch browser
            if browser_type == 'edge':
                self.driver = webdriver.Edge(options=options)
            else:
                self.driver = webdriver.Chrome(options=options)
            
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.driver.get(url)
            
            # Update UI
            self.launch_btn.config(state='disabled', text="🌐 Browser Launched")
            self.pick_btn.config(state='normal')
            self.picker_status.config(text="● Browser Ready")
            
        except Exception as e:
            self.show_popup("Error", f"Failed to launch browser: {str(e)}", "error")
    
    def start_picking(self):
        """Start element picking mode"""
        if not self.driver:
            return
        
        try:
            # Inject element picker JavaScript
            self.driver.execute_script("""
                if (!window.elementPickerActive) {
                    window.elementPickerActive = true;
                    window.selectedElementInfo = null;
                    
                    // Create overlay
                    const overlay = document.createElement('div');
                    overlay.id = 'element-picker-overlay';
                    overlay.style.cssText = `
                        position: fixed;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        background: rgba(245, 158, 11, 0.1);
                        z-index: 999999;
                        pointer-events: none;
                        border: 3px solid #f59e0b;
                        box-sizing: border-box;
                    `;
                    document.body.appendChild(overlay);
                    
                    // Create info tooltip
                    const tooltip = document.createElement('div');
                    tooltip.id = 'element-picker-tooltip';
                    tooltip.style.cssText = `
                        position: fixed;
                        background: #1f2937;
                        color: white;
                        padding: 8px 12px;
                        border-radius: 6px;
                        font-family: monospace;
                        font-size: 12px;
                        z-index: 1000000;
                        pointer-events: none;
                        display: none;
                        max-width: 300px;
                        word-wrap: break-word;
                    `;
                    document.body.appendChild(tooltip);
                    
                    let lastHighlighted = null;
                    
                    function generateSelector(element) {
                        const selectors = [];
                        
                        // ID selector (highest priority)
                        if (element.id) {
                            selectors.push({
                                type: 'ID',
                                value: '#' + element.id,
                                priority: 1
                            });
                        }
                        
                        // Name attribute
                        if (element.name) {
                            selectors.push({
                                type: 'Name',
                                value: `[name="${element.name}"]`,
                                priority: 2
                            });
                        }
                        
                        // Data attributes
                        for (let attr of element.attributes) {
                            if (attr.name.startsWith('data-')) {
                                selectors.push({
                                    type: 'Data Attribute',
                                    value: `[${attr.name}="${attr.value}"]`,
                                    priority: 3
                                });
                            }
                        }
                        
                        // Class selector
                        if (element.className && typeof element.className === 'string') {
                            const classes = element.className.trim().split(/\\s+/);
                            if (classes.length > 0 && classes[0]) {
                                selectors.push({
                                    type: 'Class',
                                    value: '.' + classes.join('.'),
                                    priority: 4
                                });
                            }
                        }
                        
                        // Tag selector
                        selectors.push({
                            type: 'Tag',
                            value: element.tagName.toLowerCase(),
                            priority: 5
                        });
                        
                        // XPath
                        function getXPath(element) {
                            if (element.id) {
                                return `//*[@id="${element.id}"]`;
                            }
                            
                            const parts = [];
                            while (element && element.nodeType === Node.ELEMENT_NODE) {
                                let index = 0;
                                let sibling = element.previousSibling;
                                while (sibling) {
                                    if (sibling.nodeType === Node.ELEMENT_NODE && sibling.tagName === element.tagName) {
                                        index++;
                                    }
                                    sibling = sibling.previousSibling;
                                }
                                
                                const tagName = element.tagName.toLowerCase();
                                const pathIndex = index > 0 ? `[${index + 1}]` : '';
                                parts.unshift(tagName + pathIndex);
                                element = element.parentNode;
                            }
                            
                            return '/' + parts.join('/');
                        }
                        
                        selectors.push({
                            type: 'XPath',
                            value: getXPath(element),
                            priority: 6
                        });
                        
                        return selectors.sort((a, b) => a.priority - b.priority);
                    }
                    
                    function highlightElement(element) {
                        if (lastHighlighted) {
                            lastHighlighted.style.outline = '';
                        }
                        
                        element.style.outline = '3px solid #f59e0b';
                        element.style.outlineOffset = '2px';
                        lastHighlighted = element;
                    }
                    
                    function showTooltip(event, element) {
                        const selectors = generateSelector(element);
                        const primary = selectors[0];
                        
                        tooltip.innerHTML = `
                            <div><strong>${element.tagName}</strong></div>
                            <div>${primary.type}: ${primary.value}</div>
                            <div style="font-size: 10px; opacity: 0.8;">Click to select</div>
                        `;
                        
                        tooltip.style.display = 'block';
                        tooltip.style.left = (event.clientX + 10) + 'px';
                        tooltip.style.top = (event.clientY - 10) + 'px';
                    }
                    
                    function hideTooltip() {
                        tooltip.style.display = 'none';
                    }
                    
                    // Mouse move handler
                    document.addEventListener('mousemove', function(e) {
                        if (!window.elementPickerActive) return;
                        
                        const element = e.target;
                        if (element.id === 'element-picker-overlay' || element.id === 'element-picker-tooltip') {
                            return;
                        }
                        
                        highlightElement(element);
                        showTooltip(e, element);
                    });
                    
                    // Click handler
                    document.addEventListener('click', function(e) {
                        if (!window.elementPickerActive) return;
                        
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const element = e.target;
                        if (element.id === 'element-picker-overlay' || element.id === 'element-picker-tooltip') {
                            return;
                        }
                        
                        const selectors = generateSelector(element);
                        
                        window.selectedElementInfo = {
                            tagName: element.tagName,
                            text: element.innerText || element.textContent || '',
                            selectors: selectors,
                            attributes: Array.from(element.attributes).map(attr => ({
                                name: attr.name,
                                value: attr.value
                            }))
                        };
                        
                        // Visual feedback
                        element.style.outline = '3px solid #10b981';
                        element.style.outlineOffset = '2px';
                        
                        hideTooltip();
                        
                        // Stop picking
                        window.elementPickerActive = false;
                        overlay.remove();
                        tooltip.remove();
                        
                        return false;
                    }, true);
                    
                    // Mouse leave handler
                    document.addEventListener('mouseleave', hideTooltip);
                }
            """)
            
            # Update UI
            self.picking = True
            self.pick_btn.config(state='disabled', text="🎯 Picking Active")
            self.stop_btn.config(state='normal')
            self.picker_status.config(text="● Picking Mode")
            
            # Start monitoring for selected element
            self.monitor_selection()
            
        except Exception as e:
            self.show_popup("Error", f"Failed to start picking: {str(e)}", "error")
    
    def monitor_selection(self):
        """Monitor for element selection"""
        if not self.driver or not self.picking:
            return
        
        try:
            # Check if element was selected
            selected_info = self.driver.execute_script("return window.selectedElementInfo;")
            
            if selected_info:
                self.selected_element = selected_info
                self.display_element_info(selected_info)
                self.stop_picking()
                return
            
            # Continue monitoring
            if self.picking and hasattr(self, 'picker_dialog') and self.picker_dialog.winfo_exists():
                self.picker_dialog.after(500, self.monitor_selection)
                
        except Exception as e:
            print(f"Monitoring error: {e}")
            if self.picking:
                self.picker_dialog.after(1000, self.monitor_selection)
    
    def stop_picking(self):
        """Stop element picking mode"""
        self.picking = False
        
        if self.driver:
            try:
                self.driver.execute_script("""
                    window.elementPickerActive = false;
                    const overlay = document.getElementById('element-picker-overlay');
                    const tooltip = document.getElementById('element-picker-tooltip');
                    if (overlay) overlay.remove();
                    if (tooltip) tooltip.remove();
                """)
            except:
                pass
        
        # Update UI
        self.pick_btn.config(state='normal', text="🎯 Start Picking")
        self.stop_btn.config(state='disabled')
        self.picker_status.config(text="● Ready")
    
    def display_element_info(self, element_info):
        """Display selected element information"""
        # Clear existing info
        for widget in self.info_content.winfo_children():
            widget.destroy()
        
        # Element details
        details_frame = tk.Frame(self.info_content, bg='#f8fafc')
        details_frame.pack(fill='both', expand=True)
        
        # Tag name
        tag_frame = tk.Frame(details_frame, bg='#f8fafc')
        tag_frame.pack(fill='x', pady=2)
        tk.Label(tag_frame, text="Tag:", font=('Segoe UI', 9, 'bold'), 
                bg='#f8fafc', fg='#374151', width=12, anchor='w').pack(side='left')
        tk.Label(tag_frame, text=element_info['tagName'], font=('Segoe UI', 9), 
                bg='#f8fafc', fg='#6b7280').pack(side='left')
        
        # Text content
        if element_info.get('text'):
            text_frame = tk.Frame(details_frame, bg='#f8fafc')
            text_frame.pack(fill='x', pady=2)
            tk.Label(text_frame, text="Text:", font=('Segoe UI', 9, 'bold'), 
                    bg='#f8fafc', fg='#374151', width=12, anchor='w').pack(side='left')
            text_content = element_info['text'][:50] + "..." if len(element_info['text']) > 50 else element_info['text']
            tk.Label(text_frame, text=text_content, font=('Segoe UI', 9), 
                    bg='#f8fafc', fg='#6b7280').pack(side='left')
        
        # Selectors
        tk.Label(details_frame, text="Available Selectors:", font=('Segoe UI', 10, 'bold'), 
                bg='#f8fafc', fg='#374151').pack(anchor='w', pady=(10, 5))
        
        # Selector list
        selector_frame = tk.Frame(details_frame, bg='#ffffff', relief='solid', bd=1)
        selector_frame.pack(fill='both', expand=True)
        
        for i, selector in enumerate(element_info['selectors'][:5]):  # Show top 5
            sel_row = tk.Frame(selector_frame, bg='#ffffff' if i % 2 == 0 else '#f9fafb')
            sel_row.pack(fill='x', padx=5, pady=2)
            
            tk.Label(sel_row, text=f"{selector['type']}:", font=('Segoe UI', 8, 'bold'), 
                    bg=sel_row['bg'], fg='#374151', width=15, anchor='w').pack(side='left')
            
            value_label = tk.Label(sel_row, text=selector['value'], font=('Segoe UI', 8), 
                                  bg=sel_row['bg'], fg='#6b7280', anchor='w')
            value_label.pack(side='left', fill='x', expand=True)
            
            # Copy button
            copy_btn = tk.Button(sel_row, text="📋", font=('Segoe UI', 8), 
                               bg='#3b82f6', fg='#ffffff', relief='flat', 
                               padx=4, pady=1, cursor='hand2', bd=0,
                               command=lambda v=selector['value']: self.copy_to_clipboard(v))
            copy_btn.pack(side='right', padx=(5, 0))
        
        # Enable use button
        self.use_btn.config(state='normal')
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            self.picker_dialog.clipboard_clear()
            self.picker_dialog.clipboard_append(text)
            self.show_popup("Copied", f"Selector copied to clipboard", "success")
        except Exception as e:
            self.show_popup("Error", f"Failed to copy: {str(e)}", "error")
    
    def use_selected_element(self):
        """Use selected element in callback"""
        if self.selected_element and self.callback:
            # Get the best selector
            best_selector = self.selected_element['selectors'][0]
            
            element_data = {
                'selector_type': best_selector['type'],
                'selector_value': best_selector['value'],
                'element_text': self.selected_element.get('text', ''),
                'tag_name': self.selected_element['tagName'],
                'all_selectors': self.selected_element['selectors']
            }
            
            self.callback(element_data)
            self.close_picker()
    
    def close_picker(self):
        """Close element picker"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
        
        if self.picker_dialog:
            self.picker_dialog.destroy()