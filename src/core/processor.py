import subprocess
from pathlib import Path
from src.utils.helpers import find_ffmpeg

class AudioProcessor:
    """Handles audio processing using FFmpeg."""
    def __init__(self):
        self.ffmpeg_bin = find_ffmpeg()

    def build_command(self, input_file, output_file, options):
        """Build the FFmpeg command based on provided options."""
        fmt = options.get("format", "mp3")
        qual = options.get("quality", "high")
        sr = options.get("sample_rate", 44100)
        ch = options.get("channels", 2)
        
        # Advanced filters
        fade_in = options.get("fade_in", 0)
        fade_out = options.get("fade_out", 0)
        pitch = options.get("pitch", 1.0)
        speed = options.get("speed", 1.0)
        noise_reduction = options.get("noise_reduction", False)
        normalize = options.get("normalize", False)
        trim_silence = options.get("trim_silence", False)
        
        cmd = [self.ffmpeg_bin, "-y", "-i", str(input_file), "-ac", str(ch), "-ar", str(sr)]
        
        afilters = []
        
        # Speed and Pitch
        if speed != 1.0 or pitch != 1.0:
            # atempo filter for speed (0.5 to 2.0)
            # rubberband filter is better for pitch but requires library, 
            # so we use asetrate + atempo for basic pitch shift
            if pitch != 1.0:
                # Adjust sample rate for pitch shift
                new_sr = int(sr * pitch)
                afilters.append(f"asetrate={new_sr}")
                # Then use atempo to bring speed back to normal if needed
                tempo = speed / pitch
                if tempo != 1.0:
                    afilters.append(f"atempo={tempo}")
            elif speed != 1.0:
                afilters.append(f"atempo={speed}")

        if noise_reduction:
            afilters.append("afftdn=nr=12:nf=-25") # Basic noise reduction

        if trim_silence:
            afilters.append("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.4")
            
        if normalize:
            afilters.append("loudnorm=I=-14:TP=-1.5:LRA=11")
            
        if fade_in > 0:
            afilters.append(f"afade=t=in:st=0:d={fade_in}")
            
        if fade_out > 0:
            # Fade out needs duration which we might not have easily without ffprobe
            # For now, we'll assume the user knows the length or we'll skip it 
            # unless we get the duration.
            pass

        if afilters:
            cmd.extend(["-af", ",".join(afilters)])
            
        # Metadata
        tags = options.get("tags", {})
        for key, value in tags.items():
            if value:
                cmd.extend(["-metadata", f"{key}={value}"])
                
        # Format presets
        if fmt == "mp3":
            qmap = {"low":["-b:a","128k"],"medium":["-b:a","192k"],"high":["-b:a","320k"],"lossless":["-b:a","320k"]}
            cmd.extend(qmap.get(qual, ["-b:a", "192k"]))
        elif fmt == "wav":
            cmd.extend(["-acodec", "pcm_s16le"])
        elif fmt == "flac":
            cmd.extend(["-acodec", "flac", "-compression_level", "5"])
        elif fmt == "ogg":
            qmap = {"low":["-q:a","3"],"medium":["-q:a","6"],"high":["-q:a","9"],"lossless":["-q:a","10"]}
            cmd.extend(qmap.get(qual, ["-q:a", "6"]))
        elif fmt == "m4a":
            qmap = {"low":["-c:a","aac","-b:a","128k"],"medium":["-c:a","aac","-b:a","192k"],"high":["-c:a","aac","-b:a","256k"],"lossless":["-c:a","aac","-b:a","320k"]}
            cmd.extend(qmap.get(qual, ["-c:a", "aac", "-b:a", "192k"]))
            
        cmd.append(str(output_file))
        return cmd

    def process(self, input_file, output_file, options):
        """Execute the FFmpeg command."""
        cmd = self.build_command(input_file, output_file, options)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
