from pathlib import Path
from mutagen import File
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC

class MetadataManager:
    """Handles reading and writing audio metadata."""
    
    @staticmethod
    def read_tags(path_str):
        """Read tags from an audio file."""
        p = Path(path_str)
        tags = {
            "title": "", 
            "artist": "", 
            "album": "", 
            "year": "", 
            "genre": "", 
            "tracknumber": ""
        }
        try:
            audio = File(path_str, easy=True)
            if audio:
                for key in tags.keys():
                    if key in audio:
                        tags[key] = audio[key][0]
        except Exception:
            pass
        return tags

    @staticmethod
    def get_cover_art(path_str):
        """Extract cover art from an audio file."""
        try:
            audio = File(path_str)
            if audio and 'APIC:' in audio:
                return audio['APIC:'].data
            elif audio and hasattr(audio, 'pictures') and audio.pictures:
                return audio.pictures[0].data
        except Exception:
            pass
        return None

    @staticmethod
    def write_tags(path_str, tags):
        """Write tags to an audio file."""
        try:
            audio = EasyID3(path_str)
            for key, value in tags.items():
                if key in EasyID3.valid_keys:
                    audio[key] = value
            audio.save()
            return True
        except Exception:
            try:
                audio = File(path_str, easy=True)
                if audio:
                    for key, value in tags.items():
                        audio[key] = value
                    audio.save()
                    return True
            except Exception:
                pass
        return False
