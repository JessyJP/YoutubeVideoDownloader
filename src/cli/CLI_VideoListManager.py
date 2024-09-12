"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This is a python source script part of the YouTube Video Downloader Suit.

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

from cli.ConsoleProgressbar import ConsoleProgressbarChecker, make_progress_bar_str
from core.video_list_manager import VideoListManager
from core.limiters import LimitsAndPriority

class VideoListManagerCLI(VideoListManager):
    def __init__(self):        
        super().__init__()
        # This status string is for updating the current process status
        self.statusMsg = "Ready!"
        self._consoleProgressbarChecker = ConsoleProgressbarChecker()
    
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
        self._consoleProgressbarChecker.log_output(msg)
        print(msg)
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        # Call the parent to compute the progress value
        progressValue = super().update_progressbar(index_in, total_in, task_level)
        progress_bar_str = make_progress_bar_str(progressValue,64)
        # NOTE: we can simply print the progress_bar_str but it's more fancy to replace it
        if progressValue == 100:
            print(progress_bar_str)
        else:
            self._consoleProgressbarChecker.update_progress(progress_bar_str)
        #end
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