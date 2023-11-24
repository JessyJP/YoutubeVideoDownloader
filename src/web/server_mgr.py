"""
File: server_mgr.py

Application Name: Youtube Video Downloader
Description: This application allows users to download videos from YouTube by providing a valid URL.
The user can analyze the video properties and choose the desired quality before downloading the video.

Author: JessyJP
Email: your.email@example.com TODO: add later
Date: April 8, 2023

Copyright (C) 2023 Your Name. All rights reserved.

License:
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
# Module imports
import os
import sys
import threading
from typing import Dict, List, Union, Tuple
from enum import Enum
import datetime


#==============================================================================

# Make and import paths for the custom core components
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
source_dir = os.path.join(project_root, "src")
sys.path.append(project_root)
from src.core.common import add_module_paths
add_module_paths(source_dir)

from src.core.common import audio_bitrate_list, video_resolution_list, fps_value_list
from src.core.video_list_manager import VideoListManager
from src.core.pytube_handler import LimitsAndPriority, VideoInfo

#==============================================================================
# Enum definition for backend current state
class ProcessRoutine(Enum):
    IDLE     = "IDLE"
    ANALYSIS = "ANALYSIS"
    DOWNLOAD = "DOWNLOAD"
#end

# Singleton decorator definitions
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
#end

#==============================================================================
# Wrapper for the manager
@singleton
class WebServerVideoManager(VideoListManager):
    def __init__(self):        
        super().__init__()
        # This status string is for updating the current process status
        self.statusMsg = "Ready!"
        self.statusProgressValue = 100
        # Let's define some variables
        self.processState = ProcessRoutine.IDLE
        # Parameters for Analysis
        self.use_multithreading_analysis = False
        # Parameters for Download
        self.process_via_multithreading = True  
        self.tmpOutputDir = '.' # TODO: maybe it shouldn't be assigned but the construction should happen in main
        self.outputExt = ".mkv"

        # Frontend client settings state
        self.clientState = dict()
        self.lastLimits = LimitsAndPriority()
        print("WebServerVideoManager is initialized")
    #end

    # Intermediate method to run the import operation in a separate thread
    def analyse_button_callback(self, text):
        def analysis_thread(target_func, args):
            # Set state to ANALYSIS at the start
            self.processState = ProcessRoutine.ANALYSIS
            self.setUiDispStatus("Analysis started")

            # Run the analysis
            target_func(*args)

            # Set state back to IDLE and update status when done
            self.processState = ProcessRoutine.IDLE
            self.setUiDispStatus("Analysis completed")
        #end

        if self.processState is ProcessRoutine.IDLE:
            use_analysis_multithreading = self.use_multithreading_analysis
            t = threading.Thread(target=analysis_thread, 
                                 args=(self.import_valid_Youtube_videos_from_textOrURL_list, (text, use_analysis_multithreading)))
            t.start()
        #end
    #end

    def getLimitsDropdownValuesAndLastSelection(self) -> Dict[str, Union[List[str], str]]:

        # # Retrieve or set default last selected values
        # self.lastLimits.bitrate = session.get('last_bitrate', audio_bitrate_list[0])
        # self.lastLimits.resolution = session.get('last_resolution', video_resolution_list[0])
        # self.lastLimits.fps = session.get('last_fps', fps_value_list[0])

        # Get the last selection
        self.lastLimits.bitrate = audio_bitrate_list[0] if  self.lastLimits.bitrate is None else self.lastLimits.bitrate
        self.lastLimits.resolution = video_resolution_list[0] if  self.lastLimits.resolution is None else self.lastLimits.resolution
        self.lastLimits.fps = fps_value_list[0] if  self.lastLimits.fps is None else self.lastLimits.fps

        # Package all render data into a single dictionary
        render_data = {
            'audio_bitrate_list':audio_bitrate_list,
            'video_resolution_list':video_resolution_list,
            'fps_value_list':fps_value_list,
            'last_bitrate':self.lastLimits.bitrate,
            'last_resolution':self.lastLimits.resolution,
            'last_fps':self.lastLimits.fps
        }

        return render_data
    #end

    def getLimitsAndPriorityFromUI(self):
        # TODO: this function should just be integrated or abstracted
        limits_and_priority = LimitsAndPriority()

        # Get the audio bitrate
        limits_and_priority.bitrate = self.lastLimits.bitrate.replace("kbps","").strip()
        # Parse audio format priority into a list
        audio_format_priority_str = "wav, mp3, aac, m4a"
        limits_and_priority.audio_format_priority = [format.strip() for format in audio_format_priority_str.split(",")]

        # Get video resolution 
        limits_and_priority.resolution = self.lastLimits.resolution.replace("p","").strip()
        # Get video fps
        limits_and_priority.fps = self.lastLimits.fps.replace("fps","").strip()
        # Parse video format priority into a list
        video_format_priority_str = "mp4, webm, flv, 3gp, m4a"
        limits_and_priority.video_format_priority = [format.strip() for format in video_format_priority_str.split(",")]
        # TODO here we can just implement the list directly but the input might come from a env variable hance why we parse strings
        limits_and_priority.to_numeric()
        return limits_and_priority
    #end

    def setDownloadDir(self, download_dir):
            # Normalize the path to avoid issues with different OS path formats
            normalized_path = os.path.normpath(download_dir)

            # Check if the path exists
            if not os.path.exists(normalized_path):
                raise FileNotFoundError(f"The specified path does not exist: {normalized_path}")

            # Set the download directory
            self.tmpOutputDir = normalized_path

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def getUiDispStatus(self) -> str:
        # Interface provision 
        return self.statusMsg
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def setUiDispStatus(self, msg: str = ""):
        # In the GUI this was used to update the status bar at the bottom,
        # but here it can serve a more comprehensive purpose to update the client.
        self.statusMsg = msg
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        # Call the parent to compute the progress value
        self.statusProgressValue = super().update_progressbar(index_in, total_in, task_level)
    #end
#end

#============================== Helper functions ==============================
# Function to convert VideoInfo data to JSON
def video_info_to_dict(vItem: VideoInfo) -> dict:
    video_info_tuple = vItem.as_tuple()
    
    video_info_dict = {
        "download_status": video_info_tuple[0],
        "watch_url": video_info_tuple[1],
        "title": video_info_tuple[2],
        "author": video_info_tuple[3],
        "length": video_info_tuple[4],
        "description": video_info_tuple[5],
        "publish_date": video_info_tuple[6],
        "views": video_info_tuple[7],
        "thumbnail_url": video_info_tuple[8],
        "rating": video_info_tuple[9],
        "video_id": video_info_tuple[10],
        "quality_str": video_info_tuple[11],
        "video_size_mb": video_info_tuple[12]
    }

    # Loop over all fields and ensure they can be converted to a string
    for key, value in video_info_dict.items():
        try:
            # Try converting to string, will work for most built-in types
            video_info_dict[key] = str(value)
        except Exception:
            # If there's an error, manually handle the conversion
            # Example for a datetime object, adjust as needed
            if isinstance(value, datetime):
                video_info_dict[key] = value.isoformat()
            else:
                # General fallback, adjust as needed for other types
                video_info_dict[key] = "Unsupported data type"
            #end
        #end
    #end

    return video_info_dict#json.dumps(video_info_dict, indent=4)
#end

#================ Initialize the web server video item manager ================
vlm = WebServerVideoManager()
