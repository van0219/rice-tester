#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import sqlite3
import os

# Simple test to verify RICE records display
class TestRiceDisplay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Test RICE Display")
        self.root.geometry("800x600")
        
        # Connect to database
        self.db_path = os.path.join(os.path.dirname(__file__), 'fsm_tester.db')
        self.conn = sqlite3.connect(self.db_path)
        
        self.setup_ui()
        self.load_rice_records()
    
    def setup_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg='#ffffff')
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="RICE Records Test", font=('Segoe UI', 16, 'bold'), 
                bg='#ffffff').pack(pady=(0, 20))
        
        # Headers
        headers_frame = tk.Frame(main_frame, bg='#f3f4f6', height=30)
        headers_frame.pack(fill="x")
        headers_frame.pack_propagate(False)
        
        tk.Label(headers_frame, text="RICE ID", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6').place(x=10, y=5, width=100)
        tk.Label(headers_frame, text="Name", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6').place(x=120, y=5, width=200)
        tk.Label(headers_frame, text="Client", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6').place(x=330, y=5, width=150)
        tk.Label(headers_frame, text="Type", font=('Segoe UI', 10, 'bold'), 
                bg='#f3f4f6').place(x=490, y=5, width=150)
        
        # Scrollable content
        canvas_frame = tk.Frame(main_frame, bg='#ffffff')
        canvas_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        self.canvas = tk.Canvas(canvas_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg='#ffffff')
        
        self.scroll_frame.bind('<Configure>', 
                              lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def load_rice_records(self):
        cursor = self.conn.cursor()
        
        # Test with user_id = 1 (has most records)
        cursor.execute("""
            SELECT rp.id, rp.rice_id, rp.name, rp.client_name, rt.type_name
            FROM rice_profiles rp
            LEFT JOIN rice_types rt ON rp.type = rt.type_name
            WHERE rp.user_id = ?
            ORDER BY rp.rice_id
        """, (1,))
        
        records = cursor.fetchall()
        print(f"Loading {len(records)} records for user_id=1")
        
        for i, (profile_id, rice_id, name, client_name, type_name) in enumerate(records):
            bg_color = '#ffffff' if i % 2 == 0 else '#f9fafb'
            
            row_frame = tk.Frame(self.scroll_frame, bg=bg_color, height=35)
            row_frame.pack(fill='x')
            row_frame.pack_propagate(False)
            
            # RICE ID
            tk.Label(row_frame, text=rice_id or '', font=('Segoe UI', 9), 
                    bg=bg_color, anchor='w').place(x=10, y=8, width=100)
            
            # Name
            tk.Label(row_frame, text=name or '', font=('Segoe UI', 9), 
                    bg=bg_color, anchor='w').place(x=120, y=8, width=200)
            
            # Client
            tk.Label(row_frame, text=client_name or '', font=('Segoe UI', 9), 
                    bg=bg_color, anchor='w').place(x=330, y=8, width=150)
            
            # Type
            tk.Label(row_frame, text=type_name or '', font=('Segoe UI', 9), 
                    bg=bg_color, anchor='w').place(x=490, y=8, width=150)
            
            print(f"Created row {i}: {rice_id} - {name}")
        
        # Update canvas scroll region
        self.root.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        print("Canvas scroll region updated")
    
    def run(self):
        self.root.mainloop()
        self.conn.close()

if __name__ == "__main__":
    app = TestRiceDisplay()
    app.run()