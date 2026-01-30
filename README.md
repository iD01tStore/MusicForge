# 🎵 Music Forge Pro

**Professional Audio Suite & Batch Processor**

**Version:** 1.2.0 (Manus Upgrade Edition)
**Developer:** Guillaume Lessard — iD01t Productions & Manus AI
**Website:** [https://www.id01t.ca](https://www.id01t.ca)

Music Forge Pro is a major upgrade to the original Music Forge app, featuring a completely modernized UI, parallel processing engine, and advanced audio manipulation tools.

---

## ✨ New in Version 1.2.0

*   **Modern Sidebar UI** — Streamlined navigation between Queue, Processor, Player, and Settings.
*   **Parallel Processing Engine** — Utilize all your CPU cores for lightning-fast batch audio conversion.
*   **Advanced Audio Filters**:
    *   **Fade In/Out** — Customizable durations for smooth transitions.
    *   **Pitch & Speed Control** — Adjust audio tempo and pitch independently.
    *   **Noise Reduction** — Intelligent FFmpeg-based noise floor reduction.
    *   **Loudness Normalization** — Broadcast-standard (EBU R128) normalization.
*   **Enhanced Metadata** — Support for extended tags including Year, Genre, and Track Number.
*   **Real-time Waveform** — Visual feedback in the built-in audio player.
*   **Modular Architecture** — Clean, maintainable codebase for future expansions.

---

## 📦 Requirements

*   **Python 3.8+**
*   **FFmpeg** (Auto-detected or via `FFMPEG_PATH`)
*   **Dependencies:** `pillow`, `ttkbootstrap`, `mutagen`, `tkinterdnd2`, `pygame`

---

## 🚀 Quick Start

1.  **Launch** Music Forge Pro: `python main.py`.
2.  **Queue**: Drag and drop your audio files into the Queue view.
3.  **Processor**: Configure your output format, quality, and advanced effects.
4.  **Settings**: Customize the theme (Cyborg, Darkly, Solar, etc.) and parallel worker count.
5.  **Compile**: Click `🚀 Start Batch Processing` to begin.

---

## 🛠 Building From Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run directly
python main.py
```

---

## 📄 License

MIT License © 2026 iD01t Productions & Manus AI
