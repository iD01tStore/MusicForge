import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from tkinterdnd2 import TkinterDnD
from pathlib import Path

from src.ui.sidebar import Sidebar
from src.ui.queue_view import QueueView
from src.ui.processor_view import ProcessorView
from src.ui.settings_view import SettingsView
from src.ui.player_view import PlayerView
from src.core.worker import SerialWorker, ParallelWorker
from src.core.processor import AudioProcessor
from src.core.metadata import MetadataManager
from src.utils.helpers import (
    enable_windows_dpi_awareness, 
    set_taskbar_appid, 
    get_base_dir,
    find_ffmpeg
)

class MusicForgeApp:
    def __init__(self):
        enable_windows_dpi_awareness()
        
        self.root = TkinterDnD.Tk()
        self.style = tb.Style(theme="darkly")
        
        self.root.title("Music Forge — Pro Audio Suite")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        set_taskbar_appid("iD01tProductions.MusicForge.v1.2")
        
        # State
        self.file_queue = []
        self.current_view = None
        
        # Workers
        self.ui_worker = SerialWorker(error_callback=self._on_worker_error)
        self.ui_worker.start()
        self.process_worker = ParallelWorker()
        
        # Core components
        self.processor = AudioProcessor()
        self.metadata = MetadataManager()
        
        self._build_layout()
        self._check_ffmpeg()

    def _build_layout(self):
        # Main container
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill="both", expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(self.main_container, self._on_view_change, width=150)
        self.sidebar.pack(side="left", fill="y")
        
        # Content Area
        self.content_area = ttk.Frame(self.main_container, padding=20)
        self.content_area.pack(side="right", fill="both", expand=True)
        
        # Initialize views (placeholders for now)
        self.views = {
            "queue": self._build_queue_view,
            "processor": self._build_processor_view,
            "player": self._build_player_view,
            "settings": self._build_settings_view
        }

    def _on_view_change(self, view_id):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
        # Build new view
        if view_id in self.views:
            self.views[view_id]()

    def _build_queue_view(self):
        view = QueueView(self.content_area, self)
        view.pack(fill="both", expand=True)
        
    def _build_processor_view(self):
        view = ProcessorView(self.content_area, self)
        view.pack(fill="both", expand=True)

    def _build_player_view(self):
        view = PlayerView(self.content_area, self)
        view.pack(fill="both", expand=True)

    def _build_settings_view(self):
        view = SettingsView(self.content_area, self)
        view.pack(fill="both", expand=True)

    def _check_ffmpeg(self):
        ffmpeg_path = find_ffmpeg()
        if not ffmpeg_path or ffmpeg_path == "ffmpeg":
            # Check if it's actually in path
            try:
                import subprocess
                subprocess.run(["ffmpeg", "-version"], capture_output=True)
            except Exception:
                messagebox.showwarning("FFmpeg Not Found", "FFmpeg is required for processing. Please install it or place it in the app directory.")

    def _on_worker_error(self, error):
        self.root.after(0, lambda: messagebox.showerror("Worker Error", str(error)))

    def start_batch_processing(self, options):
        """Start the parallel batch processing."""
        output_dir = Path(options["output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for file_item in self.file_queue:
            input_path = Path(file_item["path"])
            output_path = output_dir / f"{input_path.stem}.{options['format']}"
            
            # Create a task for each file
            self.process_worker.submit(
                self._process_single_file,
                input_path,
                output_path,
                options,
                file_item["tags"]
            )
            
    def _process_single_file(self, input_path, output_path, options, tags):
        """Worker task for a single file."""
        # Merge tags into options
        task_options = options.copy()
        task_options["tags"] = tags
        
        result = self.processor.process(input_path, output_path, task_options)
        
        if result.returncode == 0:
            print(f"Processed: {input_path.name} -> {output_path.name}")
        else:
            print(f"Error processing {input_path.name}: {result.stderr}")

    def run(self):
        self.root.mainloop()
        self.ui_worker.stop()
        self.process_worker.shutdown(wait=False)

if __name__ == "__main__":
    app = MusicForgeApp()
    app.run()
