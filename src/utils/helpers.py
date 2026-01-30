import os
import sys
import subprocess
import shutil
from pathlib import Path

def get_base_dir() -> Path:
    """Get the base directory of the application."""
    return Path(getattr(sys, "_MEIPASS", Path(__file__).parent.parent.parent)).resolve()

def find_ffmpeg() -> str:
    """Discover the FFmpeg binary path."""
    base_dir = get_base_dir()
    assets_dir = base_dir / "assets_music_forge"
    env = os.environ.get("FFMPEG_PATH")
    
    if env and Path(env).is_file():
        return str(Path(env).resolve())
        
    exe_names = ["ffmpeg.exe", "ffmpeg"]
    candidates = []
    for name in exe_names:
        candidates += [base_dir / name, base_dir / "bin" / name, assets_dir / name]
        
    for c in candidates:
        if c.is_file():
            return str(c.resolve())
            
    which = shutil.which("ffmpeg")
    return which if which else "ffmpeg"

def enable_windows_dpi_awareness():
    """Enable HiDPI awareness on Windows."""
    try:
        if sys.platform.startswith("win"):
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

def set_taskbar_appid(app_id: str):
    """Set the Windows taskbar AppUserModelID for correct icon grouping."""
    try:
        if sys.platform.startswith("win"):
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass

def sanitize_filename(name: str) -> str:
    """Sanitize a string to be a valid filename."""
    import re
    return re.sub(r'[\\/*?:"<>|]', "_", name)
