import tkinter as tk
from tkinter import ttk, filedialog
import os

class ProcessorView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        
        # Options state (could be moved to app.py)
        self.output_format = tk.StringVar(value="mp3")
        self.quality = tk.StringVar(value="high")
        self.sample_rate = tk.StringVar(value="44100")
        self.channels = tk.StringVar(value="2")
        self.normalize = tk.BooleanVar(value=False)
        self.trim_silence = tk.BooleanVar(value=False)
        self.noise_reduction = tk.BooleanVar(value=False)
        self.fade_in = tk.DoubleVar(value=0.0)
        self.fade_out = tk.DoubleVar(value=0.0)
        self.pitch = tk.DoubleVar(value=1.0)
        self.speed = tk.DoubleVar(value=1.0)
        self.output_dir = tk.StringVar(value=os.path.expanduser("~/Music/MusicForge_Output"))
        
        self._build_ui()

    def _build_ui(self):
        # Header
        ttk.Label(self, text="Audio Processor Settings", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(0, 20))
        
        main_scroll = ttk.Scrollbar(self)
        main_scroll.pack(side="right", fill="y")
        
        canvas = tk.Canvas(self, highlightthickness=0, yscrollcommand=main_scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        main_scroll.config(command=canvas.yview)
        
        container = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=container, anchor="nw")
        
        def _on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        container.bind("<Configure>", _on_frame_configure)

        # --- Format & Quality ---
        fmt_frame = ttk.LabelFrame(container, text="Output Format & Quality", padding=15)
        fmt_frame.pack(fill="x", pady=10)
        
        ttk.Label(fmt_frame, text="Format:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Combobox(fmt_frame, textvariable=self.output_format, values=["mp3", "wav", "flac", "ogg", "m4a"]).grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(fmt_frame, text="Quality:").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Combobox(fmt_frame, textvariable=self.quality, values=["low", "medium", "high", "lossless"]).grid(row=0, column=3, sticky="ew", padx=5)
        
        # --- Audio Parameters ---
        param_frame = ttk.LabelFrame(container, text="Audio Parameters", padding=15)
        param_frame.pack(fill="x", pady=10)
        
        ttk.Label(param_frame, text="Sample Rate:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Combobox(param_frame, textvariable=self.sample_rate, values=["22050", "44100", "48000", "96000"]).grid(row=0, column=1, sticky="ew", padx=5)
        
        ttk.Label(param_frame, text="Channels:").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Combobox(param_frame, textvariable=self.channels, values=["1", "2"]).grid(row=0, column=3, sticky="ew", padx=5)

        # --- Advanced Enhancements ---
        adv_frame = ttk.LabelFrame(container, text="Advanced Enhancements", padding=15)
        adv_frame.pack(fill="x", pady=10)
        
        ttk.Checkbutton(adv_frame, text="Loudness Normalization", variable=self.normalize).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(adv_frame, text="Trim Silence", variable=self.trim_silence).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(adv_frame, text="Noise Reduction", variable=self.noise_reduction).grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # --- Effects (Fade, Pitch, Speed) ---
        fx_frame = ttk.LabelFrame(container, text="Effects", padding=15)
        fx_frame.pack(fill="x", pady=10)
        
        ttk.Label(fx_frame, text="Fade In (s):").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Spinbox(fx_frame, from_=0, to=10, increment=0.5, textvariable=self.fade_in, width=5).grid(row=0, column=1, sticky="w", padx=5)
        
        ttk.Label(fx_frame, text="Fade Out (s):").grid(row=0, column=2, sticky="w", padx=5)
        ttk.Spinbox(fx_frame, from_=0, to=10, increment=0.5, textvariable=self.fade_out, width=5).grid(row=0, column=3, sticky="w", padx=5)
        
        ttk.Label(fx_frame, text="Pitch:").grid(row=1, column=0, sticky="w", padx=5, pady=10)
        ttk.Scale(fx_frame, from_=0.5, to=2.0, variable=self.pitch, orient="horizontal").grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Label(fx_frame, textvariable=self.pitch).grid(row=1, column=2, sticky="w")
        
        ttk.Label(fx_frame, text="Speed:").grid(row=2, column=0, sticky="w", padx=5, pady=10)
        ttk.Scale(fx_frame, from_=0.5, to=2.0, variable=self.speed, orient="horizontal").grid(row=2, column=1, sticky="ew", padx=5)
        ttk.Label(fx_frame, textvariable=self.speed).grid(row=2, column=2, sticky="w")

        # --- Output ---
        out_frame = ttk.LabelFrame(container, text="Output Destination", padding=15)
        out_frame.pack(fill="x", pady=10)
        
        ttk.Entry(out_frame, textvariable=self.output_dir).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(out_frame, text="Browse", command=self._browse_output).pack(side="right")

        # --- Action ---
        action_frame = ttk.Frame(container, padding=20)
        action_frame.pack(fill="x")
        
        self.process_btn = ttk.Button(
            action_frame, 
            text="🚀 Start Batch Processing", 
            style="Accent.TButton",
            command=self._start_processing
        )
        self.process_btn.pack(pady=10)

    def _browse_output(self):
        dir = filedialog.askdirectory(initialdir=self.output_dir.get())
        if dir:
            self.output_dir.set(dir)

    def _start_processing(self):
        if not self.app.file_queue:
            tk.messagebox.showwarning("Empty Queue", "Please add files to the queue first.")
            return
            
        options = {
            "format": self.output_format.get(),
            "quality": self.quality.get(),
            "sample_rate": int(self.sample_rate.get()),
            "channels": int(self.channels.get()),
            "normalize": self.normalize.get(),
            "trim_silence": self.trim_silence.get(),
            "noise_reduction": self.noise_reduction.get(),
            "fade_in": self.fade_in.get(),
            "fade_out": self.fade_out.get(),
            "pitch": self.pitch.get(),
            "speed": self.speed.get(),
            "output_dir": self.output_dir.get()
        }
        
        # Call the app method to start the worker
        self.app.start_batch_processing(options)
        tk.messagebox.showinfo("Started", f"Processing {len(self.app.file_queue)} files in background (Parallel Mode).")
