#!/usr/bin/env python3

"""
FSM RICE Tester
Main application entry point that handles authentication and launches the testing interface.
"""

import sys

def center_dialog(dialog, width=None, height=None):
    """Center dialog using CSS-like positioning without blinking"""
    # CSS-like centering: top 50%, left 50%, transform translate(-50%, -50%)
    screen_w = dialog.winfo_screenwidth()
    screen_h = dialog.winfo_screenheight()
    
    # Use provided dimensions or defaults
    w = width if width else 400
    h = height if height else 300
    
    x = (screen_w // 2) - (w // 2)
    y = (screen_h // 2) - (h // 2)
    
    # Set geometry immediately without any hide/show operations
    dialog.geometry(f"{w}x{h}+{x}+{y}")
    dialog.transient()
    dialog.grab_set()
    dialog.focus_set()
import traceback
import os
import tkinter as tk

def main():
    """Main application entry point"""
    try:
        # Import required modules
        try:
            import tkinter as tk
            from AuthSystem import AuthSystem
            from SeleniumInboundTester_Lite import SeleniumInboundTester
        except ImportError as e:
            print(f"ERROR: Failed to import required modules: {e}")
            return
        
        # Launch authentication system
        auth = AuthSystem()
        user = auth.run()
        
        # If user successfully authenticated, launch main interface
        if user:
            root = tk.Tk()
            # Initialize app first
            app = SeleniumInboundTester(root, user)
            # Maximize window after initialization (Windows-specific)
            root.state('zoomed')
            
            # Remove auto-centering to allow proper dragging between monitors
            
            # Handle window close to destroy all popups
            def on_closing():
                try:
                    # Force close all toplevel windows (popups) recursively
                    def destroy_all_toplevels():
                        for widget in root.winfo_children():
                            if isinstance(widget, tk.Toplevel):
                                try:
                                    widget.destroy()
                                except:
                                    pass
                        
                        # Also check for any remaining toplevel windows in the system
                        for widget in root.tk.call('winfo', 'children', '.'):
                            try:
                                widget_obj = root.nametowidget(widget)
                                if isinstance(widget_obj, tk.Toplevel):
                                    widget_obj.destroy()
                            except:
                                pass
                    
                    # Destroy all popups first
                    destroy_all_toplevels()
                    
                    # Clean up any remaining resources
                    try:
                        if hasattr(app, 'selenium_manager'):
                            app.selenium_manager.close()
                    except:
                        pass
                    
                    try:
                        if hasattr(app, 'db_manager'):
                            app.db_manager.close()
                    except:
                        pass
                    
                    # Force quit and destroy main window
                    root.quit()
                    root.destroy()
                    
                    # Force exit if needed
                    import sys
                    sys.exit(0)
                    
                except Exception as e:
                    # Emergency exit
                    import sys
                    try:
                        root.destroy()
                    except:
                        pass
                    sys.exit(0)
            
            root.protocol("WM_DELETE_WINDOW", on_closing)
            
            try:
                root.mainloop()
            except KeyboardInterrupt:
                on_closing()  # Use the same cleanup function
            finally:
                # Force cleanup
                try:
                    root.quit()
                    root.destroy()
                except:
                    pass
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        print(f"ERROR TYPE: {type(e).__name__}")
        print("FULL TRACEBACK:")
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()