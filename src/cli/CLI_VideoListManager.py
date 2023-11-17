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

from core.video_list_manager import VideoListManager
from core.pytube_handler import LimitsAndPriority

class VideoListManagerCLI(VideoListManager):
    def __init__(self):        
        super().__init__()
        # This status string is for updating the current process status
        self.statusMsg = "Ready!"
    
        self.lastLimits = LimitsAndPriority() # TODO: might not be needed
        print("Video List Manager CLI is initialized!")
    #end

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
        print(msg)
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        # Call the parent to compute the progress value
        progressValue = super().update_progressbar(index_in, total_in, task_level)

        def display_progress_bar(progress, width=72):
            """
            Displays a text-based progress bar in the terminal.

            :param progress: The progress percentage (0 to 100).
            :param width: The width of the progress bar in characters.
            """
            filled_length = int(width * progress // 100)
            bar = '█' * filled_length + '-' * (width - filled_length)
            print(f'\rProgress: |{bar}| {progress:.2f}%\n', end='\r')

            # Print a new line when the progress is complete
            if progress >= 100:
                print()

        display_progress_bar(progressValue)
    #end

    def getLimitsAndPriorityFromInputArguments(self, args) -> LimitsAndPriority:
        # TODO: this function should just be integrated or abstracted
        limits_and_priority = LimitsAndPriority()

        # Get the audio bitrate
        limits_and_priority.bitrate = args.bitrate.replace("kbps","").strip()
        # Parse audio format priority into a list
        audio_format_priority_str = "wav, mp3, aac, m4a"
        limits_and_priority.audio_format_priority = [format.strip() for format in audio_format_priority_str.split(",")]

        # Get video resolution 
        limits_and_priority.resolution = args.resolution.replace("p","").strip()
        # Get video fps
        limits_and_priority.fps = args.fps.replace("fps","").strip()
        # Parse video format priority into a list
        video_format_priority_str = "mp4, webm, flv, 3gp, m4a"
        limits_and_priority.video_format_priority = [format.strip() for format in video_format_priority_str.split(",")]
        # TODO here we can just implement the list directly but the input might come from a env variable hance why we parse strings
        limits_and_priority.to_numeric()
        return limits_and_priority
    #end
#end