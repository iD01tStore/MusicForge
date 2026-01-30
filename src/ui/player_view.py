import tkinter as tk
from tkinter import ttk
import pygame
from pathlib import Path
import threading
import time

class PlayerView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        
        self.is_playing = False
        self.current_track = tk.StringVar(value="No track selected")
        self.time_info = tk.StringVar(value="00:00 / 00:00")
        self.progress = tk.DoubleVar(value=0.0)
        
        try:
            pygame.mixer.init()
        except Exception:
            pass
            
        self._build_ui()
        self._update_loop()

    def _build_ui(self):
        ttk.Label(self, text="Audio Player", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 20))
        
        # Track Info
        info_frame = ttk.Frame(self, padding=20)
        info_frame.pack(fill="x")
        
        ttk.Label(info_frame, textvariable=self.current_track, font=("Segoe UI", 14)).pack()
        ttk.Label(info_frame, textvariable=self.time_info).pack(pady=5)
        
        # Waveform Placeholder
        self.canvas = tk.Canvas(self, height=150, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(fill="x", pady=20, padx=20)
        self._draw_waveform_placeholder()
        
        # Controls
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(pady=20)
        
        ttk.Button(ctrl_frame, text="⏮", width=5, command=self._prev_track).pack(side="left", padx=5)
        self.play_btn = ttk.Button(ctrl_frame, text="▶", width=8, command=self._toggle_play)
        self.play_btn.pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="⏭", width=5, command=self._next_track).pack(side="left", padx=5)
        
        # Progress Bar
        self.slider = ttk.Scale(self, from_=0, to=100, variable=self.progress, orient="horizontal", command=self._seek)
        self.slider.pack(fill="x", padx=40, pady=10)

    def _draw_waveform_placeholder(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 150
        mid = h / 2
        import random
        for i in range(0, w, 4):
            val = random.randint(10, 60)
            self.canvas.create_line(i, mid-val, i, mid+val, fill="#3498db", width=2)

    def _toggle_play(self):
        if not self.app.file_queue:
            return
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.play_btn.configure(text="▶")
            self.is_playing = False
        else:
            if not pygame.mixer.music.get_busy():
                # Start first track if nothing playing
                track_path = self.app.file_queue[0]["path"]
                pygame.mixer.music.load(track_path)
                pygame.mixer.music.play()
                self.current_track.set(Path(track_path).name)
            else:
                pygame.mixer.music.unpause()
            
            self.play_btn.configure(text="⏸")
            self.is_playing = True

    def _next_track(self):
        pass # Implement logic to find next in queue

    def _prev_track(self):
        pass

    def _seek(self, val):
        pass

    def _update_loop(self):
        if self.is_playing:
            # Update progress and time
            pass
        self.after(500, self._update_loop)
