import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

class SettingsView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        ttk.Label(self, text="Settings", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Appearance
        app_frame = ttk.LabelFrame(self, text="Appearance", padding=15)
        app_frame.pack(fill="x", pady=10)
        
        ttk.Label(app_frame, text="Theme:").grid(row=0, column=0, sticky="w", padx=5)
        self.theme_var = tk.StringVar(value=self.app.style.theme.name)
        themes = self.app.style.theme_names()
        theme_cb = ttk.Combobox(app_frame, textvariable=self.theme_var, values=themes)
        theme_cb.grid(row=0, column=1, sticky="ew", padx=5)
        theme_cb.bind("<<ComboboxSelected>>", self._on_theme_change)
        
        # System
        sys_frame = ttk.LabelFrame(self, text="System", padding=15)
        sys_frame.pack(fill="x", pady=10)
        
        self.max_workers = tk.IntVar(value=4)
        ttk.Label(sys_frame, text="Max Parallel Workers:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Spinbox(sys_frame, from_=1, to=16, textvariable=self.max_workers, width=5).grid(row=0, column=1, sticky="w", padx=5)
        
        # About
        about_frame = ttk.LabelFrame(self, text="About", padding=15)
        about_frame.pack(fill="x", pady=10)
        
        ttk.Label(about_frame, text="Music Forge Pro", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(about_frame, text="Version 1.2.0 (Manus Upgrade Edition)").pack(anchor="w")
        ttk.Label(about_frame, text="© 2026 iD01t Productions & Manus AI").pack(anchor="w")

    def _on_theme_change(self, event):
        theme = self.theme_var.get()
        self.app.style.theme_use(theme)
