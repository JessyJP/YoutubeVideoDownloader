from src.core.post_download_mux import combine_via_ffmpeg

try:
    import ffmpeg
    print("ffmpeg module is importable.")
except ImportError:
    print("ffmpeg module is not importable. Please make sure ffmpeg-python is installed.")

combine_via_ffmpeg

video = ffmpeg.input("r:/test/NixOS is Mindblowing.mp4")
audio = ffmpeg.input("r:/test/NixOS is Mindblowing.aac")

print("done")