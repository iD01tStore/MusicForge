import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.core.processor import AudioProcessor
from src.core.metadata import MetadataManager
from src.utils.helpers import find_ffmpeg

def test_discovery():
    print("Testing Discovery...")
    ffmpeg = find_ffmpeg()
    print(f"FFmpeg found at: {ffmpeg}")
    return ffmpeg is not None

def test_metadata():
    print("Testing Metadata...")
    # Since we don't have a real audio file easily available that we know of,
    # we'll just check if the class can be instantiated.
    mm = MetadataManager()
    print("MetadataManager instantiated successfully.")
    return True

def test_processor():
    print("Testing Processor...")
    ap = AudioProcessor()
    options = {
        "format": "mp3",
        "quality": "high",
        "sample_rate": 44100,
        "channels": 2,
        "normalize": True,
        "fade_in": 2.0,
        "tags": {"title": "Test Title"}
    }
    cmd = ap.build_command("input.wav", "output.mp3", options)
    print(f"Generated command: {' '.join(cmd)}")
    return "loudnorm" in ' '.join(cmd) and "afade" in ' '.join(cmd)

if __name__ == "__main__":
    s1 = test_discovery()
    s2 = test_metadata()
    s3 = test_processor()
    
    if all([s1, s2, s3]):
        print("\nCore tests PASSED!")
    else:
        print("\nCore tests FAILED!")
        sys.exit(1)
