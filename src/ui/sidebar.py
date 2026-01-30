import tkinter as tk
from tkinter import ttk

class Sidebar(ttk.Frame):
    """A sidebar navigation component."""
    def __init__(self, parent, on_change_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_change = on_change_callback
        self.current_selection = None
        self.buttons = {}
        
        self._build_ui()

    def _build_ui(self):
        # Logo or Title area
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")
        ttk.Label(header, text="MF", font=("Segoe UI", 24, "bold")).pack()
        
        # Navigation buttons
        nav_frame = ttk.Frame(self, padding=5)
        nav_frame.pack(fill="both", expand=True)
        
        self._add_nav_button(nav_frame, "Queue", "queue")
        self._add_nav_button(nav_frame, "Processor", "processor")
        self._add_nav_button(nav_frame, "Player", "player")
        self._add_nav_button(nav_frame, "Settings", "settings")
        
        # Footer
        footer = ttk.Frame(self, padding=10)
        footer.pack(side="bottom", fill="x")
        ttk.Label(footer, text="v1.2.0", font=("Segoe UI", 8)).pack()

    def _add_nav_button(self, parent, text, view_id):
        btn = ttk.Button(
            parent, 
            text=text, 
            command=lambda: self._select_view(view_id),
            style="Sidebar.TButton"
        )
        btn.pack(fill="x", pady=2, padx=5)
        self.buttons[view_id] = btn
        
        if not self.current_selection:
            self._select_view(view_id)

    def _select_view(self, view_id):
        if self.current_selection == view_id:
            return
            
        self.current_selection = view_id
        self.on_change(view_id)
        
        # Update button styles (conceptually, depends on theme)
        for vid, btn in self.buttons.items():
            if vid == view_id:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])
