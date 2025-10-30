#!/usr/bin/env python3

import sqlite3

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning"""
    dialog.withdraw()
    dialog.update_idletasks()
    
    # Get dimensions
    if width and height:
        dialog.geometry(f"{width}x{height}")
    
    dialog.update_idletasks()
    w = dialog.winfo_reqwidth() if not width else width
    h = dialog.winfo_reqheight() if not height else height
    
    # CSS-like centering: top 50%, left 50%, transform translate(-50%, -50%)
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.deiconify()
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()
import os
import hashlib
import base64

class DatabaseManager:
    def __init__(self, user_id, password_key="FSM_TESTER_KEY_2024"):
        self.user_id = user_id
        self.password_key = password_key
        self.db_path = os.path.join(os.path.dirname(__file__), 'fsm_tester.db')
        self.conn = sqlite3.connect(self.db_path)
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        cursor = self.conn.cursor()
        
        # Create scenarios table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rice_profile TEXT NOT NULL,
                scenario_number INTEGER NOT NULL,
                description TEXT NOT NULL,
                file_path TEXT,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                executed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, rice_profile, scenario_number)
            )
        """)
        
        # Create fsm_pages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fsm_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create scenario_steps table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenario_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rice_profile TEXT NOT NULL,
                scenario_number INTEGER NOT NULL,
                step_order INTEGER NOT NULL,
                fsm_page_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (fsm_page_id) REFERENCES fsm_pages (id)
            )
        """)
        
        # Create SFTP profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sftp_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                profile_name TEXT NOT NULL,
                host TEXT NOT NULL,
                port INTEGER DEFAULT 22,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                directory TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, profile_name)
            )
        """)
        
        # Create global_config table (removed use_channel and channel_name)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS global_config (
                user_id INTEGER PRIMARY KEY,
                browser_type TEXT,
                second_screen BOOLEAN,
                incognito BOOLEAN,
                fsm_url TEXT,
                fsm_username TEXT,
                fsm_password TEXT,
                sftp_host TEXT,
                sftp_port INTEGER,
                sftp_username TEXT,
                sftp_password TEXT,
                sftp_directory TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create RICE profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rice_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rice_id TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                client_name TEXT NOT NULL,
                channel_name TEXT,
                sftp_profile_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, rice_id)
            )
        """)
        
        # Add sftp_profile_name column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE rice_profiles ADD COLUMN sftp_profile_name TEXT")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # Add tenant column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE rice_profiles ADD COLUMN tenant TEXT")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # Add executed_at column to scenarios table if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE scenarios ADD COLUMN executed_at TIMESTAMP")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # Add auto_login column to scenarios table if it doesn't exist
        try:
            cursor.execute("ALTER TABLE scenarios ADD COLUMN auto_login BOOLEAN DEFAULT 0")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # Add scenario_steps columns if they don't exist
        try:
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN step_name TEXT")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN step_type TEXT")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN step_target TEXT")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN step_description TEXT")
            self.conn.commit()
        except Exception:
            pass  # Columns already exist
        
        # Add screenshot columns if they don't exist
        try:
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN screenshot_before BLOB")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN screenshot_after BLOB")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN screenshot_timestamp TIMESTAMP")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN user_input_required BOOLEAN DEFAULT 0")
            cursor.execute("ALTER TABLE scenario_steps ADD COLUMN execution_status TEXT DEFAULT 'pending'")
            self.conn.commit()
        except Exception:
            pass  # Columns already exist
        
        # Create test step groups table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_step_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                group_name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, group_name)
            )
        """)
        
        # Create test steps table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_steps (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rice_profile_id INTEGER NOT NULL,
                group_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                step_type TEXT NOT NULL,
                target TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (rice_profile_id) REFERENCES rice_profiles (id),
                FOREIGN KEY (group_id) REFERENCES test_step_groups (id)
            )
        """)
        
        # Add group_id column to existing test_steps if it doesn't exist
        try:
            cursor.execute("ALTER TABLE test_steps ADD COLUMN group_id INTEGER")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # Add step_order column to existing test_steps if it doesn't exist
        try:
            cursor.execute("ALTER TABLE test_steps ADD COLUMN step_order INTEGER DEFAULT 1")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # Create default "Generic" group if no groups exist
        cursor.execute("SELECT COUNT(*) FROM test_step_groups WHERE user_id = ?", (self.user_id,))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO test_step_groups (user_id, group_name, description)
                VALUES (?, 'Generic', 'Default group for test steps')
            """, (self.user_id,))
            
            # Get the generic group ID
            generic_group_id = cursor.lastrowid
            
            # Update existing test steps to use generic group
            cursor.execute("""
                UPDATE test_steps SET group_id = ? WHERE user_id = ? AND group_id IS NULL
            """, (generic_group_id, self.user_id))
        
        # Create file channels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                channel_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                UNIQUE(user_id, channel_name)
            )
        """)
        
        # Create rice_types table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rice_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_name TEXT NOT NULL UNIQUE
            )
        """)
        
        # Populate rice_types if empty
        cursor.execute("SELECT COUNT(*) FROM rice_types")
        if cursor.fetchone()[0] == 0:
            types = ['Report', 'Interface - Inbound', 'Interface - Outbound', 'LPL Configuration', 'Approval']
            for type_name in types:
                cursor.execute('INSERT INTO rice_types (type_name) VALUES (?)', (type_name,))
        
        # Create test users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create service accounts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS service_accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_content BLOB,
                date_added TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Create TES-070 versions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tes070_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                rice_profile_id INTEGER NOT NULL,
                version_number INTEGER NOT NULL,
                file_content BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_by TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (rice_profile_id) REFERENCES rice_profiles (id)
            )
        """)
        
        # Migrate existing TES-070 data to use proper rice_profile_id
        try:
            # Check if we need to migrate data
            cursor.execute("SELECT rice_profile_id FROM tes070_versions LIMIT 1")
            sample = cursor.fetchone()
            if sample and not str(sample[0]).isdigit():
                # Migrate text rice_profile_id to integer
                cursor.execute("""
                    UPDATE tes070_versions 
                    SET rice_profile_id = (
                        SELECT rp.id FROM rice_profiles rp 
                        WHERE rp.rice_id = tes070_versions.rice_profile_id 
                        AND rp.user_id = tes070_versions.user_id
                    )
                    WHERE EXISTS (
                        SELECT 1 FROM rice_profiles rp 
                        WHERE rp.rice_id = tes070_versions.rice_profile_id 
                        AND rp.user_id = tes070_versions.user_id
                    )
                """)
                # Delete orphaned records that can't be migrated
                cursor.execute("""
                    DELETE FROM tes070_versions 
                    WHERE NOT EXISTS (
                        SELECT 1 FROM rice_profiles rp 
                        WHERE rp.id = tes070_versions.rice_profile_id
                    )
                """)
        except Exception:
            pass  # Migration already done or not needed
        
        # Create TES-070 templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tes070_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                template_format TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        # Add file_content column if it doesn't exist (for existing databases)
        try:
            cursor.execute("ALTER TABLE service_accounts ADD COLUMN file_content BLOB")
            self.conn.commit()
        except Exception:
            pass  # Column already exists
        
        # 🛡️ SECURITY: Create database trigger to block restricted usernames
        # Recreate trigger every time to prevent tampering
        cursor.execute("DROP TRIGGER IF EXISTS block_restricted_usernames")
        cursor.execute("""
            CREATE TRIGGER block_restricted_usernames
            BEFORE INSERT ON users
            FOR EACH ROW
            WHEN LOWER(NEW.username) IN ('vansilleza_fpi', 'van_silleza', 'admin', 'administrator', 'root', 'system')
            BEGIN
                SELECT RAISE(ABORT, 'Username is reserved for system administrators');
            END
        """)
        
        # 🛡️ SECURITY: Also block updates to restricted usernames  
        # Recreate trigger every time to prevent tampering
        cursor.execute("DROP TRIGGER IF EXISTS block_restricted_username_updates")
        cursor.execute("""
            CREATE TRIGGER block_restricted_username_updates
            BEFORE UPDATE ON users
            FOR EACH ROW
            WHEN LOWER(NEW.username) IN ('vansilleza_fpi', 'van_silleza', 'admin', 'administrator', 'root', 'system')
            AND NEW.id > 3
            BEGIN
                SELECT RAISE(ABORT, 'Username is reserved for system administrators');
            END
        """)
        
        self.conn.commit()
    
    def hash_password_reversible(self, password):
        """Hash password for storage (reversible for SFTP passwords)"""
        if not password:
            return ""
        key_bytes = self.password_key.encode()
        password_bytes = password.encode()
        result = bytearray()
        for i, byte in enumerate(password_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        return base64.b64encode(result).decode()
    
    def decrypt_password(self, hashed_password):
        """Decrypt password for use"""
        if not hashed_password:
            return ""
        try:
            key_bytes = self.password_key.encode()
            encrypted_bytes = base64.b64decode(hashed_password.encode())
            result = bytearray()
            for i, byte in enumerate(encrypted_bytes):
                result.append(byte ^ key_bytes[i % len(key_bytes)])
            return result.decode()
        except:
            return ""
    
    def get_sftp_profiles(self):
        """Get all SFTP profiles for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, profile_name, host, port, username, directory 
            FROM sftp_profiles 
            WHERE user_id = ? 
            ORDER BY profile_name
        """, (self.user_id,))
        return cursor.fetchall()
    
    def save_sftp_profile(self, profile_name, host, port, username, password, directory, profile_id=None):
        """Save SFTP profile"""
        cursor = self.conn.cursor()
        
        if profile_id:
            cursor.execute("""
                UPDATE sftp_profiles 
                SET profile_name = ?, host = ?, port = ?, username = ?, password = ?, directory = ?
                WHERE id = ? AND user_id = ?
            """, (profile_name, host, port, username, 
                  self.hash_password_reversible(password), directory, profile_id, self.user_id))
        else:
            cursor.execute("""
                INSERT INTO sftp_profiles (user_id, profile_name, host, port, username, password, directory)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (self.user_id, profile_name, host, port, username, 
                  self.hash_password_reversible(password), directory))
        
        self.conn.commit()
    
    def delete_sftp_profile(self, profile_id):
        """Delete SFTP profile"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM sftp_profiles WHERE id = ? AND user_id = ?", (profile_id, self.user_id))
        self.conn.commit()
    
    def get_global_config(self):
        """Get global configuration"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM global_config WHERE user_id = ?", (self.user_id,))
        return cursor.fetchone()
    
    def save_global_config(self, config_data):
        """Save global configuration"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO global_config 
            (user_id, browser_type, second_screen, incognito, fsm_url, fsm_username, fsm_password,
             sftp_host, sftp_port, sftp_username, sftp_password, sftp_directory)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.user_id, *config_data))
        self.conn.commit()
    
    def get_rice_profiles(self):
        """Get all RICE profiles for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT rp.id, rp.rice_id, rp.name, rp.client_name, rp.channel_name, rp.sftp_profile_name, rt.type_name, rp.tenant
            FROM rice_profiles rp
            LEFT JOIN rice_types rt ON rp.type = rt.type_name
            WHERE rp.user_id = ? 
            ORDER BY rp.rice_id
        """, (self.user_id,))
        return cursor.fetchall()
    
    def save_rice_profile(self, rice_id, name, profile_type, client_name, channel_name, sftp_profile_name=None, tenant=None, profile_id=None):
        """Save RICE profile"""
        cursor = self.conn.cursor()
        
        if profile_id:
            cursor.execute("""
                UPDATE rice_profiles 
                SET rice_id = ?, name = ?, type = ?, client_name = ?, channel_name = ?, sftp_profile_name = ?, tenant = ?
                WHERE id = ? AND user_id = ?
            """, (rice_id, name, profile_type, client_name, channel_name, sftp_profile_name, tenant, profile_id, self.user_id))
        else:
            cursor.execute("""
                INSERT INTO rice_profiles (user_id, rice_id, name, type, client_name, channel_name, sftp_profile_name, tenant)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.user_id, rice_id, name, profile_type, client_name, channel_name, sftp_profile_name, tenant))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_test_step_groups(self):
        """Get all test step groups for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT tsg.id, tsg.group_name, tsg.description, COUNT(ts.id) as step_count
            FROM test_step_groups tsg
            LEFT JOIN test_steps ts ON tsg.id = ts.group_id
            WHERE tsg.user_id = ?
            GROUP BY tsg.id, tsg.group_name, tsg.description
            ORDER BY tsg.group_name
        """, (self.user_id,))
        return cursor.fetchall()
    
    def save_test_step_group(self, group_name, description, group_id=None):
        """Save test step group"""
        cursor = self.conn.cursor()
        
        if group_id:
            cursor.execute("""
                UPDATE test_step_groups 
                SET group_name = ?, description = ?
                WHERE id = ? AND user_id = ?
            """, (group_name, description, group_id, self.user_id))
        else:
            cursor.execute("""
                INSERT INTO test_step_groups (user_id, group_name, description)
                VALUES (?, ?, ?)
            """, (self.user_id, group_name, description))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def delete_test_step_group(self, group_id):
        """Delete test step group and all its steps"""
        cursor = self.conn.cursor()
        # Delete all steps in this group first
        cursor.execute("DELETE FROM test_steps WHERE group_id = ? AND user_id = ?", (group_id, self.user_id))
        # Delete the group
        cursor.execute("DELETE FROM test_step_groups WHERE id = ? AND user_id = ?", (group_id, self.user_id))
        self.conn.commit()
    
    def get_test_steps(self, rice_profile_id, group_id=None):
        """Get test steps for RICE profile and optionally for specific group"""
        cursor = self.conn.cursor()
        if group_id:
            cursor.execute("""
                SELECT id, name, step_type, target, description
                FROM test_steps 
                WHERE user_id = ? AND rice_profile_id = ? AND group_id = ?
                ORDER BY id
            """, (self.user_id, rice_profile_id, group_id))
        else:
            cursor.execute("""
                SELECT id, name, step_type, target, description
                FROM test_steps 
                WHERE user_id = ? AND rice_profile_id = ?
                ORDER BY id
            """, (self.user_id, rice_profile_id))
        return cursor.fetchall()
    
    def get_test_steps_by_group(self, group_id):
        """Get all test steps for a specific group"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, step_type, target, description
            FROM test_steps 
            WHERE user_id = ? AND group_id = ?
            ORDER BY COALESCE(step_order, id), id
        """, (self.user_id, group_id))
        return cursor.fetchall()
    
    def save_test_step(self, rice_profile_id, name, step_type, target, description, group_id, step_id=None):
        """Save test step"""
        cursor = self.conn.cursor()
        
        if step_id:
            cursor.execute("""
                UPDATE test_steps 
                SET name = ?, step_type = ?, target = ?, description = ?, group_id = ?
                WHERE id = ? AND user_id = ?
            """, (name, step_type, target, description, group_id, step_id, self.user_id))
        else:
            # Get next step_order for this group
            cursor.execute("""
                SELECT COALESCE(MAX(step_order), 0) + 1 FROM test_steps 
                WHERE user_id = ? AND group_id = ?
            """, (self.user_id, group_id))
            next_order = cursor.fetchone()[0]
            
            cursor.execute("""
                INSERT INTO test_steps (user_id, rice_profile_id, name, step_type, target, description, group_id, step_order)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.user_id, rice_profile_id, name, step_type, target, description, group_id, next_order))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def delete_test_step(self, step_id):
        """Delete test step"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM test_steps WHERE id = ? AND user_id = ?", (step_id, self.user_id))
        self.conn.commit()
    
    def get_scenarios(self, rice_profile_id):
        """Get scenarios for RICE profile"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, scenario_number, description, result, file_path
            FROM scenarios 
            WHERE user_id = ? AND rice_profile = ?
            ORDER BY scenario_number
        """, (self.user_id, str(rice_profile_id)))
        return cursor.fetchall()
    
    def get_next_scenario_number(self, rice_profile_id):
        """Get next scenario number for RICE profile"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT MAX(scenario_number) FROM scenarios 
            WHERE user_id = ? AND rice_profile = ?
        """, (self.user_id, str(rice_profile_id)))
        result = cursor.fetchone()
        return (result[0] or 0) + 1
    
    def save_scenario(self, rice_profile_id, scenario_number, description, file_path, auto_login=False):
        """Save scenario"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO scenarios (user_id, rice_profile, scenario_number, description, file_path, auto_login, result)
            VALUES (?, ?, ?, ?, ?, ?, 'Not run')
        """, (self.user_id, str(rice_profile_id), scenario_number, description, file_path, auto_login))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def save_scenario_step(self, rice_profile_id, scenario_number, step_order, fsm_page_id):
        """Save scenario step"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO scenario_steps (user_id, rice_profile, scenario_number, step_order, fsm_page_id)
            VALUES (?, ?, ?, ?, ?)
        """, (self.user_id, str(rice_profile_id), scenario_number, step_order, fsm_page_id))
        
        self.conn.commit()
    
    def save_step_screenshot(self, step_id, screenshot_before=None, screenshot_after=None, status="completed"):
        """Save screenshots for a step"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE scenario_steps 
            SET screenshot_before = ?, screenshot_after = ?, 
                screenshot_timestamp = CURRENT_TIMESTAMP, execution_status = ?
            WHERE id = ?
        """, (screenshot_before, screenshot_after, status, step_id))
        self.conn.commit()
    
    def get_step_screenshots(self, step_id):
        """Get screenshots for a step"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT screenshot_before, screenshot_after, screenshot_timestamp, execution_status
            FROM scenario_steps WHERE id = ?
        """, (step_id,))
        return cursor.fetchone()
    
    def mark_step_user_input_required(self, step_id, required=True):
        """Mark step as requiring user input"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE scenario_steps SET user_input_required = ? WHERE id = ?
        """, (required, step_id))
        self.conn.commit()
    
    def get_file_channels(self):
        """Get all file channels for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, channel_name
            FROM file_channels 
            WHERE user_id = ? 
            ORDER BY channel_name
        """, (self.user_id,))
        return cursor.fetchall()
    
    def save_file_channel(self, channel_name, channel_id=None):
        """Save file channel"""
        cursor = self.conn.cursor()
        
        if channel_id:
            cursor.execute("""
                UPDATE file_channels 
                SET channel_name = ?
                WHERE id = ? AND user_id = ?
            """, (channel_name, channel_id, self.user_id))
        else:
            cursor.execute("""
                INSERT INTO file_channels (user_id, channel_name)
                VALUES (?, ?)
            """, (self.user_id, channel_name))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def update_file_channel(self, channel_id, channel_name):
        """Update file channel"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE file_channels 
            SET channel_name = ?
            WHERE id = ? AND user_id = ?
        """, (channel_name, channel_id, self.user_id))
        self.conn.commit()
    
    def delete_file_channel(self, channel_id):
        """Delete file channel"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM file_channels WHERE id = ? AND user_id = ?", (channel_id, self.user_id))
        self.conn.commit()
    
    def get_rice_types(self):
        """Get all RICE types"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, type_name FROM rice_types ORDER BY id")
        return cursor.fetchall()
    
    def get_test_users(self):
        """Get test users for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, email, password
            FROM test_users 
            WHERE user_id = ?
            ORDER BY name
        """, (self.user_id,))
        return cursor.fetchall()
    
    def save_test_user(self, name, email, password, test_user_id=None):
        """Save test user"""
        cursor = self.conn.cursor()
        encrypted_password = self.hash_password_reversible(password)
        
        if test_user_id:
            cursor.execute("""
                UPDATE test_users 
                SET name = ?, email = ?, password = ?
                WHERE id = ? AND user_id = ?
            """, (name, email, encrypted_password, test_user_id, self.user_id))
        else:
            cursor.execute("""
                INSERT INTO test_users (user_id, name, email, password)
                VALUES (?, ?, ?, ?)
            """, (self.user_id, name, email, encrypted_password))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def delete_test_user(self, test_user_id):
        """Delete test user"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM test_users WHERE id = ? AND user_id = ?", (test_user_id, self.user_id))
        self.conn.commit()
    
    def get_service_accounts(self):
        """Get service accounts for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, file_path, date_added
            FROM service_accounts 
            WHERE user_id = ?
            ORDER BY date_added DESC
        """, (self.user_id,))
        return cursor.fetchall()
    
    def save_service_account(self, name, file_path, date_added, account_id=None):
        """Save service account"""
        cursor = self.conn.cursor()
        
        # Read file content
        file_content = None
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    file_content = f.read()
            except Exception:
                pass
        
        if account_id:
            cursor.execute("""
                UPDATE service_accounts 
                SET name = ?, file_path = ?, file_content = ?, date_added = ?
                WHERE id = ? AND user_id = ?
            """, (name, file_path, file_content, date_added, account_id, self.user_id))
        else:
            cursor.execute("""
                INSERT INTO service_accounts (user_id, name, file_path, file_content, date_added)
                VALUES (?, ?, ?, ?, ?)
            """, (self.user_id, name, file_path, file_content, date_added))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_service_account_content(self, account_id):
        """Get service account file content"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name, file_content FROM service_accounts 
            WHERE id = ? AND user_id = ?
        """, (account_id, self.user_id))
        return cursor.fetchone()
    
    def delete_service_account(self, account_id):
        """Delete service account"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM service_accounts WHERE id = ? AND user_id = ?", (account_id, self.user_id))
        self.conn.commit()
    
    def get_rice_profiles_paginated(self, offset, limit):
        """Get RICE profiles with pagination"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT rp.id, rp.rice_id, rp.name, rp.client_name, rp.channel_name, rp.sftp_profile_name, rt.type_name, rp.tenant
            FROM rice_profiles rp
            LEFT JOIN rice_types rt ON rp.type = rt.type_name
            WHERE rp.user_id = ? 
            ORDER BY rp.rice_id
            LIMIT ? OFFSET ?
        """, (self.user_id, limit, offset))
        return cursor.fetchall()
    
    def get_rice_profiles_count(self):
        """Get total count of RICE profiles"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM rice_profiles WHERE user_id = ?", (self.user_id,))
        return cursor.fetchone()[0]
    
    def get_scenarios_paginated(self, rice_profile_id, offset, limit):
        """Get scenarios with pagination"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, scenario_number, description, result, file_path
            FROM scenarios 
            WHERE user_id = ? AND rice_profile = ?
            ORDER BY scenario_number
            LIMIT ? OFFSET ?
        """, (self.user_id, str(rice_profile_id), limit, offset))
        return cursor.fetchall()
    
    def get_scenarios_count(self, rice_profile_id):
        """Get total count of scenarios for RICE profile"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM scenarios 
            WHERE user_id = ? AND rice_profile = ?
        """, (self.user_id, str(rice_profile_id)))
        return cursor.fetchone()[0]
    
    def save_tes070_version(self, rice_profile_id, file_content, created_by):
        """Save TES-070 version and maintain only latest 5 versions"""
        cursor = self.conn.cursor()
        
        # Convert rice_profile_id to actual database ID if it's a RICE_ID string
        if isinstance(rice_profile_id, str) and not rice_profile_id.isdigit():
            cursor.execute("""
                SELECT id FROM rice_profiles 
                WHERE user_id = ? AND rice_id = ?
            """, (self.user_id, rice_profile_id))
            result = cursor.fetchone()
            if not result:
                raise ValueError(f"RICE profile '{rice_profile_id}' not found")
            rice_profile_id = result[0]
        
        rice_profile_id = int(rice_profile_id)
        
        # Get current version count for this RICE profile
        cursor.execute("""
            SELECT COUNT(*) FROM tes070_versions 
            WHERE user_id = ? AND rice_profile_id = ?
        """, (self.user_id, rice_profile_id))
        version_count = cursor.fetchone()[0]
        
        # If we have 5 versions, delete the oldest one
        if version_count >= 5:
            cursor.execute("""
                DELETE FROM tes070_versions 
                WHERE user_id = ? AND rice_profile_id = ? 
                AND id = (
                    SELECT id FROM tes070_versions 
                    WHERE user_id = ? AND rice_profile_id = ? 
                    ORDER BY created_at ASC LIMIT 1
                )
            """, (self.user_id, rice_profile_id, self.user_id, rice_profile_id))
        
        # Get next version number
        cursor.execute("""
            SELECT COALESCE(MAX(version_number), 0) + 1 FROM tes070_versions 
            WHERE user_id = ? AND rice_profile_id = ?
        """, (self.user_id, rice_profile_id))
        version_number = cursor.fetchone()[0]
        
        # Insert new version
        cursor.execute("""
            INSERT INTO tes070_versions (user_id, rice_profile_id, version_number, file_content, created_by)
            VALUES (?, ?, ?, ?, ?)
        """, (self.user_id, rice_profile_id, version_number, file_content, created_by))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_tes070_versions(self, rice_profile_id):
        """Get all TES-070 versions for a RICE profile (latest 5)"""
        cursor = self.conn.cursor()
        
        # Convert rice_profile_id to actual database ID if it's a RICE_ID string
        if isinstance(rice_profile_id, str) and not rice_profile_id.isdigit():
            cursor.execute("""
                SELECT id FROM rice_profiles 
                WHERE user_id = ? AND rice_id = ?
            """, (self.user_id, rice_profile_id))
            result = cursor.fetchone()
            if not result:
                return []
            rice_profile_id = result[0]
        
        rice_profile_id = int(rice_profile_id)
        
        cursor.execute("""
            SELECT id, version_number, created_at, created_by
            FROM tes070_versions 
            WHERE user_id = ? AND rice_profile_id = ?
            ORDER BY created_at DESC
        """, (self.user_id, rice_profile_id))
        return cursor.fetchall()
    
    def get_tes070_content(self, version_id):
        """Get TES-070 file content by version ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT file_content FROM tes070_versions 
            WHERE id = ? AND user_id = ?
        """, (version_id, self.user_id))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def save_tes070_template(self, template_format):
        """Save TES-070 name format template"""
        cursor = self.conn.cursor()
        
        # Delete existing template for user
        cursor.execute("DELETE FROM tes070_templates WHERE user_id = ?", (self.user_id,))
        
        # Insert new template
        cursor.execute("""
            INSERT INTO tes070_templates (user_id, template_format)
            VALUES (?, ?)
        """, (self.user_id, template_format))
        
        self.conn.commit()
        return cursor.lastrowid
    
    def get_tes070_template(self):
        """Get TES-070 name format template for user"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT template_format FROM tes070_templates 
            WHERE user_id = ? 
            ORDER BY created_at DESC LIMIT 1
        """, (self.user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
