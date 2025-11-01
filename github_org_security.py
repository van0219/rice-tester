#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import os
from datetime import datetime

class GitHubOrgSecurity:
    """
    GitHub Organization Security Manager
    Validates admin access through GitHub organization membership
    """
    
    def __init__(self, org_name="Infor-FSM"):
        self.org_name = org_name
        self.github_token = None
        self.github_username = None
        
    def load_github_credentials(self):
        """Load GitHub credentials from existing integration"""
        try:
            # Try github_json.config first (test groups format)
            config_path = os.path.join(os.path.dirname(__file__), 'github_json.config')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.github_token = config.get('token')
                    self.github_username = config.get('username')
                    return True
            
            # Try github_config.json (main integration format)
            config_path = os.path.join(os.path.dirname(__file__), 'github_config.json')
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.github_username = config.get('github_username')
                    encoded_token = config.get('github_token')
                    if encoded_token:
                        import base64
                        self.github_token = base64.b64decode(encoded_token.encode()).decode()
                    return True
                    
        except Exception as e:
            print(f"Failed to load GitHub credentials: {e}")
        
        return False
    
    def validate_admin_access(self, username=None):
        """
        Validate if user has admin access through GitHub organization
        Returns: (is_admin: bool, role: str, error: str)
        """
        if not self.load_github_credentials():
            return False, "no_credentials", "GitHub credentials not found"
        
        # Use provided username or loaded username
        check_username = username or self.github_username
        if not check_username:
            return False, "no_username", "Username not available"
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Check organization membership and role
            membership_url = f"https://api.github.com/orgs/{self.org_name}/memberships/{check_username}"
            response = requests.get(membership_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                role = data.get('role', 'member')
                state = data.get('state', 'pending')
                
                # Admin if role is 'admin' or organization owner
                is_admin = role in ['admin', 'owner'] and state == 'active'
                return is_admin, role, None
                
            elif response.status_code == 404:
                return False, "not_member", f"User '{check_username}' is not a member of {self.org_name} organization"
            else:
                return False, "api_error", f"GitHub API error: {response.status_code}"
                
        except Exception as e:
            return False, "network_error", f"Network error: {str(e)}"
    
    def get_organization_members(self):
        """Get all organization members with their roles"""
        if not self.load_github_credentials():
            return []
        
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            # Get organization members
            members_url = f"https://api.github.com/orgs/{self.org_name}/members"
            response = requests.get(members_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                members = response.json()
                member_details = []
                
                for member in members:
                    username = member['login']
                    # Get detailed membership info
                    membership_url = f"https://api.github.com/orgs/{self.org_name}/memberships/{username}"
                    membership_response = requests.get(membership_url, headers=headers, timeout=5)
                    
                    role = "member"  # default
                    if membership_response.status_code == 200:
                        membership_data = membership_response.json()
                        role = membership_data.get('role', 'member')
                    
                    member_details.append({
                        'username': username,
                        'role': role,
                        'avatar_url': member.get('avatar_url', ''),
                        'html_url': member.get('html_url', '')
                    })
                
                return member_details
            else:
                print(f"Failed to get organization members: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error getting organization members: {e}")
            return []
    
    def update_local_admin_status(self, db_manager, user_id, username):
        """Update local database admin status based on GitHub org role"""
        is_admin, role, error = self.validate_admin_access(username)
        
        if error:
            print(f"Admin validation error for {username}: {error}")
            return False
        
        try:
            cursor = db_manager.conn.cursor()
            cursor.execute("""
                UPDATE users SET isAdmin = ? WHERE id = ?
            """, (is_admin, user_id))
            db_manager.conn.commit()
            
            print(f"Updated admin status for {username}: isAdmin={is_admin}, role={role}")
            return is_admin
            
        except Exception as e:
            print(f"Failed to update admin status: {e}")
            return False
    
    def is_user_admin(self, db_manager, user_id):
        """Check if user is admin in local database"""
        try:
            cursor = db_manager.conn.cursor()
            cursor.execute("SELECT isAdmin FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return bool(result[0]) if result else False
        except Exception:
            return False
    
    def sync_all_users_admin_status(self, db_manager):
        """Sync admin status for all users with GitHub usernames"""
        try:
            cursor = db_manager.conn.cursor()
            cursor.execute("SELECT id, username FROM users")
            users = cursor.fetchall()
            
            synced_count = 0
            for user_id, username in users:
                if self.update_local_admin_status(db_manager, user_id, username):
                    synced_count += 1
            
            return synced_count
            
        except Exception as e:
            print(f"Failed to sync admin status: {e}")
            return 0

def test_github_org_security():
    """Test the GitHub organization security system"""
    security = GitHubOrgSecurity()
    
    print("Testing GitHub Organization Security...")
    print(f"Organization: {security.org_name}")
    
    # Test credential loading
    if security.load_github_credentials():
        print(f"✅ Credentials loaded for: {security.github_username}")
        
        # Test admin validation
        is_admin, role, error = security.validate_admin_access()
        if error:
            print(f"❌ Validation error: {error}")
        else:
            print(f"✅ Admin validation: isAdmin={is_admin}, role={role}")
        
        # Test getting organization members
        members = security.get_organization_members()
        print(f"✅ Organization has {len(members)} members:")
        for member in members:
            print(f"  - {member['username']} ({member['role']})")
    else:
        print("❌ Failed to load GitHub credentials")

if __name__ == "__main__":
    test_github_org_security()