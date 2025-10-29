#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LocatorFallback:
    """Enhanced locator system with fallback strategies for robust element finding"""
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.fallback_strategies = [
            self._find_by_primary_locator,
            self._find_by_id_fallback,
            self._find_by_xpath_fallback,
            self._find_by_text_fallback,
            self._find_by_partial_text_fallback,
            self._find_by_class_fallback,
            self._find_by_tag_fallback
        ]
    
    def find_element_with_fallback(self, target, step_name="Unknown Step"):
        """Find element using fallback strategies"""
        logger.info(f"Attempting to find element for step: {step_name}")
        logger.info(f"Primary target: {target}")
        
        for i, strategy in enumerate(self.fallback_strategies):
            try:
                element = strategy(target)
                if element:
                    if i > 0:
                        logger.warning(f"Primary locator failed for '{step_name}'. Found using fallback strategy #{i}")
                    else:
                        logger.info(f"Element found using primary locator for '{step_name}'")
                    return element
            except Exception as e:
                logger.debug(f"Strategy #{i} failed: {str(e)}")
                continue
        
        # All strategies failed
        error_msg = f"Element not found: {step_name} (possible UI change). Target: {target}"
        logger.error(error_msg)
        raise NoSuchElementException(error_msg)
    
    def _find_by_primary_locator(self, target):
        """Find using the original locator strategy"""
        wait = WebDriverWait(self.driver, self.timeout)
        
        # Parse click type modifiers
        clean_target = self._clean_target(target)
        
        # Determine locator strategy
        if clean_target.startswith('#'):
            return wait.until(EC.presence_of_element_located((By.ID, clean_target[1:])))
        elif clean_target.startswith('.'):
            return wait.until(EC.presence_of_element_located((By.CLASS_NAME, clean_target[1:])))
        elif clean_target.startswith('//'):
            return wait.until(EC.presence_of_element_located((By.XPATH, clean_target)))
        elif '[name=' in clean_target or '[id=' in clean_target or '[class=' in clean_target:
            return wait.until(EC.presence_of_element_located((By.XPATH, clean_target)))
        else:
            return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, clean_target)))
    
    def _find_by_id_fallback(self, target):
        """Fallback: Try to find by ID if target contains ID-like patterns"""
        clean_target = self._clean_target(target)
        
        # Extract potential ID from various formats
        potential_ids = []
        
        if 'id=' in clean_target:
            # Extract from xpath: //input[@id='username'] -> username
            import re
            id_match = re.search(r"id=['\"]([^'\"]+)['\"]", clean_target)
            if id_match:
                potential_ids.append(id_match.group(1))
        
        if clean_target.startswith('.') or clean_target.startswith('#'):
            # Try the selector value as ID
            potential_ids.append(clean_target[1:])
        
        # Try common ID patterns based on target
        base_name = clean_target.lower().replace(' ', '').replace('-', '').replace('_', '')
        potential_ids.extend([
            base_name,
            f"{base_name}Btn",
            f"{base_name}Button",
            f"btn{base_name.title()}",
            f"{base_name}Input",
            f"{base_name}Field"
        ])
        
        wait = WebDriverWait(self.driver, 2)  # Shorter timeout for fallbacks
        
        for potential_id in potential_ids:
            try:
                return wait.until(EC.presence_of_element_located((By.ID, potential_id)))
            except TimeoutException:
                continue
        
        return None
    
    def _find_by_xpath_fallback(self, target):
        """Fallback: Generate XPath alternatives"""
        clean_target = self._clean_target(target)
        wait = WebDriverWait(self.driver, 2)
        
        # Generate XPath alternatives
        xpath_alternatives = []
        
        if clean_target.startswith('#'):
            # ID to XPath
            id_value = clean_target[1:]
            xpath_alternatives.extend([
                f"//*[@id='{id_value}']",
                f"//input[@id='{id_value}']",
                f"//button[@id='{id_value}']",
                f"//div[@id='{id_value}']"
            ])
        
        elif clean_target.startswith('.'):
            # Class to XPath
            class_value = clean_target[1:]
            xpath_alternatives.extend([
                f"//*[@class='{class_value}']",
                f"//*[contains(@class, '{class_value}')]",
                f"//button[contains(@class, '{class_value}')]",
                f"//input[contains(@class, '{class_value}')]"
            ])
        
        elif not clean_target.startswith('//'):
            # CSS to XPath approximation
            xpath_alternatives.extend([
                f"//*[@name='{clean_target}']",
                f"//*[@id='{clean_target}']",
                f"//*[contains(@class, '{clean_target}')]"
            ])
        
        for xpath in xpath_alternatives:
            try:
                return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                continue
        
        return None
    
    def _find_by_text_fallback(self, target):
        """Fallback: Find by text content"""
        clean_target = self._clean_target(target)
        wait = WebDriverWait(self.driver, 2)
        
        # Extract potential text from target
        potential_texts = []
        
        # If target looks like text
        if not any(char in clean_target for char in ['#', '.', '/', '[', '@']):
            potential_texts.append(clean_target)
        
        # Common button/link texts
        common_texts = ['Submit', 'Login', 'Save', 'Cancel', 'OK', 'Next', 'Previous', 'Search']
        for text in common_texts:
            if text.lower() in clean_target.lower():
                potential_texts.append(text)
        
        # Try finding by exact text
        for text in potential_texts:
            try:
                # Try button first, then any element
                xpath_options = [
                    f"//button[text()='{text}']",
                    f"//input[@value='{text}']",
                    f"//*[text()='{text}']",
                    f"//a[text()='{text}']"
                ]
                
                for xpath in xpath_options:
                    try:
                        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    except TimeoutException:
                        continue
                        
            except TimeoutException:
                continue
        
        return None
    
    def _find_by_partial_text_fallback(self, target):
        """Fallback: Find by partial text content"""
        clean_target = self._clean_target(target)
        wait = WebDriverWait(self.driver, 2)
        
        # Extract keywords from target
        keywords = []
        if not any(char in clean_target for char in ['#', '.', '/', '[', '@']):
            # Split target into words
            words = clean_target.replace('-', ' ').replace('_', ' ').split()
            keywords.extend([word for word in words if len(word) > 2])
        
        for keyword in keywords:
            try:
                xpath_options = [
                    f"//button[contains(text(), '{keyword}')]",
                    f"//input[contains(@value, '{keyword}')]",
                    f"//*[contains(text(), '{keyword}')]",
                    f"//a[contains(text(), '{keyword}')]"
                ]
                
                for xpath in xpath_options:
                    try:
                        return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                    except TimeoutException:
                        continue
                        
            except TimeoutException:
                continue
        
        return None
    
    def _find_by_class_fallback(self, target):
        """Fallback: Try common class patterns"""
        clean_target = self._clean_target(target)
        wait = WebDriverWait(self.driver, 2)
        
        # Generate potential class names
        potential_classes = []
        
        if not clean_target.startswith('.') and not any(char in clean_target for char in ['#', '/', '[', '@']):
            base_name = clean_target.lower().replace(' ', '-')
            potential_classes.extend([
                base_name,
                f"{base_name}-btn",
                f"{base_name}-button",
                f"btn-{base_name}",
                f"{base_name}-input",
                f"{base_name}-field"
            ])
        
        for class_name in potential_classes:
            try:
                return wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            except TimeoutException:
                continue
        
        return None
    
    def _find_by_tag_fallback(self, target):
        """Fallback: Find by common tag types"""
        clean_target = self._clean_target(target)
        wait = WebDriverWait(self.driver, 1)  # Very short timeout
        
        # If target suggests a specific element type
        tag_hints = {
            'button': ['button', 'input[type="button"]', 'input[type="submit"]'],
            'input': ['input', 'textarea'],
            'link': ['a'],
            'submit': ['input[type="submit"]', 'button[type="submit"]']
        }
        
        target_lower = clean_target.lower()
        for hint, tags in tag_hints.items():
            if hint in target_lower:
                for tag in tags:
                    try:
                        if '[' in tag:
                            # CSS selector
                            return wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, tag)))
                        else:
                            # Tag name
                            elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, tag)))
                            if elements:
                                return elements[0]  # Return first match
                    except TimeoutException:
                        continue
        
        return None
    
    def _clean_target(self, target):
        """Remove click type modifiers from target"""
        clean_target = target
        for modifier in [' [RIGHT-CLICK]', ' [DOUBLE-CLICK]', ' [LEFT-CLICK]']:
            clean_target = clean_target.replace(modifier, '')
        return clean_target.strip()
    
    def get_fallback_report(self):
        """Get report of fallback usage for analytics"""
        # This could be expanded to track fallback usage statistics
        return {
            'total_attempts': getattr(self, '_total_attempts', 0),
            'fallback_used': getattr(self, '_fallback_used', 0),
            'success_rate': getattr(self, '_success_rate', 100.0)
        }

# Integration helper for selenium_manager.py
def enhance_selenium_manager_with_fallback(selenium_manager):
    """Enhance existing selenium manager with fallback capabilities"""
    
    def find_element_enhanced(target, step_name="Unknown Step"):
        """Enhanced element finding with fallback"""
        if not selenium_manager.driver:
            raise WebDriverException("WebDriver not initialized")
        
        fallback_finder = LocatorFallback(selenium_manager.driver)
        return fallback_finder.find_element_with_fallback(target, step_name)
    
    # Add enhanced method to selenium manager
    selenium_manager.find_element_with_fallback = find_element_enhanced
    
    return selenium_manager