import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
from tkinterdnd2 import DND_FILES

class QueueView(ttk.Frame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, **kwargs)
        self.app = app
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="File Queue", font=("Segoe UI", 18, "bold")).pack(side="left")
        
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side="right")
        
        ttk.Button(btn_frame, text="Add Files", command=self._add_files).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Add Folder", command=self._add_folder).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self._clear_queue).pack(side="left", padx=5)

        # Treeview
        columns = ("filename", "title", "artist", "album", "format", "size")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        
        self.tree.heading("filename", text="Filename")
        self.tree.heading("title", text="Title")
        self.tree.heading("artist", text="Artist")
        self.tree.heading("album", text="Album")
        self.tree.heading("format", text="Format")
        self.tree.heading("size", text="Size")
        
        self.tree.column("filename", width=200)
        self.tree.column("title", width=150)
        self.tree.column("artist", width=150)
        self.tree.column("album", width=150)
        self.tree.column("format", width=80)
        self.tree.column("size", width=100)
        
        self.tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        # Drag and Drop
        self.tree.drop_target_register(DND_FILES)
        self.tree.dnd_bind('<<Drop>>', self._on_drop)
        
        # Populate if there are files
        self._refresh_tree()

    def _refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for file_item in self.app.file_queue:
            self._insert_row(file_item)

    def _insert_row(self, file_item):
        p = Path(file_item["path"])
        size_mb = f"{p.stat().st_size / (1024*1024):.2f} MB" if p.exists() else "N/A"
        tags = file_item["tags"]
        
        self.tree.insert("", "end", values=(
            p.name,
            tags.get("title", ""),
            tags.get("artist", ""),
            tags.get("album", ""),
            p.suffix.upper()[1:],
            size_mb
        ))

    def _add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Audio Files",
            filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg *.m4a *.aac *.wma"), ("All Files", "*.*")]
        )
        if files:
            self._process_new_paths(files)

    def _add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            audio_ext = {'.mp3','.wav','.flac','.ogg','.m4a','.aac','.wma'}
            files = [str(p) for p in Path(folder).rglob('*') if p.suffix.lower() in audio_ext]
            self._process_new_paths(files)

    def _on_drop(self, event):
        paths = self.app.root.splitlist(event.data.replace("{", "").replace("}", ""))
        self._process_new_paths(paths)

    def _process_new_paths(self, paths):
        existing_paths = {item["path"] for item in self.app.file_queue}
        for path in paths:
            if path not in existing_paths:
                tags = self.app.metadata.read_tags(path)
                file_item = {"path": path, "tags": tags}
                self.app.file_queue.append(file_item)
                self._insert_row(file_item)

    def _clear_queue(self):
        self.app.file_queue.clear()
        self._refresh_tree()
