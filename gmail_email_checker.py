#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import base64
import time
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from PIL import Image, ImageDraw, ImageFont
import textwrap
import html

class GmailEmailChecker:
    """Gmail API email checking for RICE Tester automation"""
    
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    
    def __init__(self):
        self.service = None
        self.credentials_file = "gmail_credentials.json"
        self.token_file = "gmail_token.json"
    
    def setup_credentials(self):
        """Setup Gmail API credentials"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(f"Gmail credentials file '{self.credentials_file}' not found")
                
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('gmail', 'v1', credentials=creds)
        return True
    
    def check_email_notification(self, search_criteria, timeout=60):
        """
        Check for email notification based on search criteria
        
        Args:
            search_criteria (str): Gmail search query (e.g., "subject:notification from:noreply@example.com")
            timeout (int): Maximum wait time in seconds
        
        Returns:
            dict: Email details if found, None if not found
        """
        if not self.service:
            if not self.setup_credentials():
                return None
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Search for emails
                results = self.service.users().messages().list(
                    userId='me', 
                    q=search_criteria,
                    maxResults=10
                ).execute()
                
                messages = results.get('messages', [])
                
                if messages:
                    # Get the most recent message
                    message_id = messages[0]['id']
                    message = self.service.users().messages().get(
                        userId='me', 
                        id=message_id
                    ).execute()
                    
                    # Extract email details
                    email_data = self._parse_email(message)
                    
                    # Check if email is recent (within last 5 minutes)
                    if self._is_recent_email(email_data['timestamp']):
                        return email_data
                
                # Wait before checking again
                time.sleep(5)
                
            except HttpError as error:
                print(f"Gmail API error: {error}")
                time.sleep(10)
            except Exception as e:
                print(f"Email check error: {e}")
                time.sleep(5)
        
        return None
    
    def verify_email_content(self, search_criteria, expected_content, timeout=60):
        """
        Verify email contains expected content
        
        Args:
            search_criteria (str): Gmail search query
            expected_content (list): List of strings that should be in email body
            timeout (int): Maximum wait time in seconds
        
        Returns:
            bool: True if email found with expected content
        """
        email_data = self.check_email_notification(search_criteria, timeout)
        
        if not email_data:
            return False
        
        email_body = email_data.get('body', '').lower()
        
        # Check if all expected content is present
        for content in expected_content:
            if content.lower() not in email_body:
                return False
        
        return True
    
    def _parse_email(self, message):
        """Parse Gmail message to extract useful information"""
        headers = message['payload'].get('headers', [])
        
        # Extract headers
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        
        # Extract body
        body = self._extract_body(message['payload'])
        
        # Convert timestamp
        timestamp = int(message['internalDate']) / 1000
        
        return {
            'id': message['id'],
            'subject': subject,
            'sender': sender,
            'date': date_str,
            'timestamp': timestamp,
            'body': body,
            'snippet': message.get('snippet', '')
        }
    
    def _extract_body(self, payload):
        """Extract email body from payload"""
        body = ""
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    data = part['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            if payload['mimeType'] == 'text/plain':
                data = payload['body']['data']
                body = base64.urlsafe_b64decode(data).decode('utf-8')
        
        return body
    
    def _is_recent_email(self, timestamp):
        """Check if email is recent (within last 5 minutes)"""
        current_time = time.time()
        return (current_time - timestamp) <= 300  # 5 minutes
    
    def capture_email_content(self, email_data, output_path="email_screenshot.png"):
        """Create visual representation of email for TES-070 documentation"""
        try:
            # Create image canvas
            width, height = 800, 600
            img = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(img)
            
            # Try to load font, fallback to default
            try:
                font_header = ImageFont.truetype("arial.ttf", 16)
                font_body = ImageFont.truetype("arial.ttf", 12)
                font_small = ImageFont.truetype("arial.ttf", 10)
            except:
                font_header = ImageFont.load_default()
                font_body = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            y_pos = 20
            
            # Email header background
            draw.rectangle([10, 10, width-10, 120], fill='#f8f9fa', outline='#dee2e6')
            
            # Subject
            subject = email_data.get('subject', 'No Subject')[:60]
            draw.text((20, y_pos), f"Subject: {subject}", fill='black', font=font_header)
            y_pos += 25
            
            # From
            sender = email_data.get('sender', 'Unknown Sender')[:50]
            draw.text((20, y_pos), f"From: {sender}", fill='#666666', font=font_body)
            y_pos += 20
            
            # Date
            date_str = email_data.get('date', 'Unknown Date')[:30]
            draw.text((20, y_pos), f"Date: {date_str}", fill='#666666', font=font_body)
            y_pos += 20
            
            # Status
            draw.text((20, y_pos), "Status: ✅ Email Verified", fill='#28a745', font=font_body)
            y_pos += 40
            
            # Email body background
            draw.rectangle([10, 130, width-10, height-20], fill='white', outline='#dee2e6')
            
            # Email body content
            body = email_data.get('body', email_data.get('snippet', 'No content available'))
            
            # Clean HTML if present
            if '<' in body and '>' in body:
                body = html.unescape(body)
                # Simple HTML tag removal
                import re
                body = re.sub('<[^<]+?>', '', body)
            
            # Wrap text and draw
            wrapped_lines = textwrap.wrap(body[:500], width=80)
            y_pos = 150
            
            for line in wrapped_lines[:15]:  # Limit to 15 lines
                if y_pos > height - 50:
                    draw.text((20, y_pos), "... (content truncated)", fill='#999999', font=font_small)
                    break
                draw.text((20, y_pos), line, fill='black', font=font_body)
                y_pos += 18
            
            # Footer
            draw.text((20, height-30), f"Email ID: {email_data.get('id', 'N/A')[:20]}...", 
                     fill='#999999', font=font_small)
            
            # Save image
            img.save(output_path)
            return output_path
            
        except Exception as e:
            print(f"Error creating email screenshot: {e}")
            # Create simple error image
            img = Image.new('RGB', (400, 200), color='white')
            draw = ImageDraw.Draw(img)
            draw.text((20, 80), "Email Content Screenshot", fill='black')
            draw.text((20, 100), f"Subject: {email_data.get('subject', 'N/A')}", fill='black')
            draw.text((20, 120), "✅ Email Verification Complete", fill='green')
            img.save(output_path)
            return output_path
    
    def get_setup_instructions(self):
        """Return setup instructions for Gmail API"""
        return """
Gmail API Setup Instructions:

1. Go to Google Cloud Console (console.cloud.google.com)
2. Create a new project or select existing one
3. Enable Gmail API for your project
4. Create credentials (OAuth 2.0 Client ID)
5. Download credentials as 'gmail_credentials.json'
6. Place file in RICE Tester directory
7. First run will open browser for authorization

Required file: gmail_credentials.json
Generated file: gmail_token.json (auto-created)
"""

# Example usage for RICE Tester integration
def create_email_check_step_data(search_criteria, expected_content=None, timeout=60):
    """Create step data for email checking"""
    step_data = {
        'step_type': 'Email Check',
        'search_criteria': search_criteria,
        'expected_content': expected_content or [],
        'timeout': timeout,
        'service': 'gmail'
    }
    return step_data

# Common email check patterns
EMAIL_PATTERNS = {
    'password_reset': 'subject:"Password Reset" OR subject:"Reset Password"',
    'account_verification': 'subject:"Verify" OR subject:"Confirmation"',
    'notification': 'subject:"Notification" OR subject:"Alert"',
    'order_confirmation': 'subject:"Order" OR subject:"Purchase"',
    'welcome_email': 'subject:"Welcome" OR subject:"Getting Started"'
}