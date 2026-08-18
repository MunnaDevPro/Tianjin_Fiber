"""
Utility to convert uploaded factory videos to H.264 MP4 for browser compatibility.
Uses imageio-ffmpeg which bundles its own ffmpeg binary (no system ffmpeg needed).
"""
import os
import subprocess
import tempfile
import imageio_ffmpeg


def convert_video_to_h264(source_path):
    """
    Convert a video file to H.264 MP4 in-place.
    Returns True on success, False on failure.
    """
    if not os.path.isfile(source_path):
        return False

    # Get ffmpeg binary path bundled by imageio_ffmpeg
    ffmpeg_bin = imageio_ffmpeg.get_ffmpeg_exe()

    # Create a temporary output file
    tmp_fd, tmp_path = tempfile.mkstemp(suffix='_converted.mp4')
    os.close(tmp_fd)

    try:
        command = [
            ffmpeg_bin,
            '-y',                         # Overwrite output without prompt
            '-i', source_path,            # Input file
            '-vcodec', 'libx264',         # Encode video as H.264
            '-acodec', 'aac',             # Encode audio as AAC
            '-crf', '23',                 # Quality setting (lower = better quality, 18-28 range)
            '-preset', 'fast',            # Encoding speed (fast is a good balance)
            '-movflags', '+faststart',    # Move MOOV atom to start for web streaming
            '-pix_fmt', 'yuv420p',        # Pixel format compatible with all browsers
            tmp_path                      # Output file
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300  # 5 min max
        )

        if result.returncode == 0 and os.path.getsize(tmp_path) > 0:
            # Replace the original with the converted version
            os.replace(tmp_path, source_path)
            return True
        else:
            return False

    except Exception:
        return False
    finally:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
