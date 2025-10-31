#!/usr/bin/env python3
import sqlite3
import os

# Simulate the load_rice_profiles method
class MockDatabaseManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db_path = os.path.join(os.path.dirname(__file__), 'fsm_tester.db')
        self.conn = sqlite3.connect(self.db_path)
    
    def get_rice_profiles_filtered(self, offset, limit, search_term="", type_filter="", client_filter=""):
        """Get RICE profiles with search and filter"""
        cursor = self.conn.cursor()
        
        # Build WHERE clause
        where_conditions = ["rp.user_id = ?"]
        params = [self.user_id]
        
        if search_term:
            where_conditions.append("(rp.rice_id LIKE ? OR rp.name LIKE ? OR rp.client_name LIKE ?)")
            search_param = f"%{search_term}%"
            params.extend([search_param, search_param, search_param])
        
        if type_filter:
            where_conditions.append("rt.type_name = ?")
            params.append(type_filter)
        
        if client_filter:
            where_conditions.append("rp.client_name = ?")
            params.append(client_filter)
        
        where_clause = " AND ".join(where_conditions)
        
        query = f"""
            SELECT rp.id, rp.rice_id, rp.name, rp.client_name, rp.channel_name, rp.sftp_profile_name, rt.type_name, rp.tenant
            FROM rice_profiles rp
            LEFT JOIN rice_types rt ON rp.type = rt.type_name
            WHERE {where_clause}
            ORDER BY rp.rice_id
            LIMIT ? OFFSET ?
        """
        
        print(f"Query: {query}")
        print(f"Params: {params + [limit, offset]}")
        
        cursor.execute(query, params + [limit, offset])
        results = cursor.fetchall()
        
        print(f"Results: {results}")
        return results

# Test with different user IDs
print("=== TESTING RICE PROFILE LOADING ===")

for user_id in [1, 2, 3, 4]:
    print(f"\n--- Testing User ID: {user_id} ---")
    db_manager = MockDatabaseManager(user_id)
    profiles = db_manager.get_rice_profiles_filtered(0, 5)  # offset=0, limit=5
    print(f"Found {len(profiles)} profiles for user {user_id}")
    for profile in profiles:
        print(f"  {profile}")
    db_manager.conn.close()