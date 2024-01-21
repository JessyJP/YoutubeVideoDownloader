"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

MIT License

Copyright (c) 2024 JessyJP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Imports
import os
import sys
import platform
import subprocess

## ================================= Definitions =================================


## ================================= Runtime Flags =================================

os_name = platform.system()
os_arch = platform.architecture()[0]

isDeployed = getattr(sys, "frozen", False)


## ================================= Logging =================================
import logging
logger = logging.getLogger(__name__)

## ================================= Quality definitions =================================

# Define base values
base_audio_bitrates = ["max", 384, 320, 256, 192, 160, 128, 96, 64]
base_video_resolutions = ["max", 15360, 7680, 4320, 2160, 1440, 1080, 720, 480, 360, 240, 144]
base_fps_values = ["max", 240, 120, 60, 50, 48, 30, 25, 24, 15]

# Generate lists with units
audio_bitrate_list = [f"{bitrate} kbps" if bitrate != "max" else "max kbps" for bitrate in base_audio_bitrates]
video_resolution_list = [f"{resolution}p" if resolution != "max" else "max p" for resolution in base_video_resolutions]
fps_value_list = [f"{fps} fps" if fps != "max" else "max fps" for fps in base_fps_values]

## ================================= Module management functions =================================
# Ensure all required modules are installed.
def install_missing_modules(modules):
    if isDeployed:# This ensures that this functions is not called once an executable is made
        return
    #end
    try:
        import pkg_resources
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
        import pkg_resources
    #end

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_modules = [module for module in modules if module not in installed_packages]

    if missing_modules:
        for module in missing_modules:
            print(f"Installing missing module: {module}")# TODO: maybe a logger should be used here instead of a print statement
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        #end
    #end
#end

def add_module_paths(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                sys.path.insert(0, subdir)
                print(f"Added {subdir} to sys.path")
                break
            #end
        #end
    #end
#end

## ================================= Conversion  functions =================================
def hex_to_rgba(color, default_alpha=1.0):
    if color.startswith("rgba"):
        # Extract numbers from rgba string
        rgba = color.strip("rgba()").replace(" ", "").split(",")
        r, g, b = [int(x) for x in rgba[:3]]
        a = float(rgba[3]) if len(rgba) > 3 else default_alpha
    elif color.startswith("#"):
        # Strip the '#' character if it's there
        color = color.lstrip('#')

        # Convert the hex values to RGB
        r, g, b = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        a = default_alpha
    else:
        # Handle invalid input format
        raise ValueError("Invalid color format")

    # Normalize RGB values to [0.0, 1.0] and return with alpha
    return r / 255.0, g / 255.0, b / 255.0, a

