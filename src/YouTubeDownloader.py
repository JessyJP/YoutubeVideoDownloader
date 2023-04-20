"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Date: April 7, 2023
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import splashscreen
## Import Modules
import os
import argparse
from core import *
from gui_main import *


## Command line parsing tool
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube video downloader")

    # Condition to check if there are no input arguments or if "-gui" is specified
    parser.add_argument("--gui", action="store_true", help="Run GUI")
    
    args = parser.parse_args()
    if args.gui or (len(sys.argv)-1) == 0:        
        main_runGUI()
    else:
        parser.add_argument("-c", action="store_true", help="Combine audio and video (default)")
        parser.add_argument("-a", action="store_true", help="Download audio only")
        parser.add_argument("-v", action="store_true", help="Download video only")
        parser.add_argument("-s", action="store_true", help="Add subtitles")
        parser.add_argument("-i", action="store_true", help="Keep info")
        parser.add_argument("-t", action="store_true", help="Download the thumbnails")
        parser.add_argument("-q", choices=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p", "max"], help="Video quality specifier")
        parser.add_argument("--fps", type=int, help="Specify the fps (frames per second)")
        parser.add_argument("--abr", type=int, help="Specify the audio bitrate in kbps")
        parser.add_argument("output", nargs="?", default=".", help="Output directory (default: current directory)")
        parser.add_argument("urls", nargs="+", help="One or more YouTube video URLs")

        args = parser.parse_args()

        if not (args.a or args.v):
            args.c = True

        limits = LimitsAndPriority()

        for url in args.urls:
            info = get_url_info_entry(url)
            info.download_and_combine(args.output, limits)
        #end
    #end
#end
