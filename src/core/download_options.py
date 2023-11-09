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
# Imports
from enum import Enum

## ================================= Download Keep Options =================================


class MediaSymbols(Enum):
    COMBINED       = "☑"
    AUDIO_ONLY     = "Ⓐ"
    VIDEO_ONLY     = "Ⓥ"
    SUBTITLES_ONLY = "Ⓢ"
    THUMBNAIL      = "Ⓣ"
    INFO           = "ⓘ"
    COMMENTS       = "ⓒ"


## Unpack the options to strings
COMBINED_SYMBOL         = MediaSymbols.COMBINED.value        
AUDIO_ONLY_SYMBOL       = MediaSymbols.AUDIO_ONLY.value      
VIDEO_ONLY_SYMBOL       = MediaSymbols.VIDEO_ONLY.value      
SUBTITLES_ONLY_SYMBOL   = MediaSymbols.SUBTITLES_ONLY.value  
THUMBNAIL_SYMBOL        = MediaSymbols.THUMBNAIL.value       
INFO_SYMBOL             = MediaSymbols.INFO.value            
COMMENTS_SYMBOL         = MediaSymbols.COMMENTS.value        

def setOutputKeepsStr(combined: bool = False, spacing: int = 2, audio_only: bool = False, video_only: bool = False,  
                      subtitles_only: bool = False, thumbnail: bool = False, info: bool = False, comments: bool = False) -> str:
    """
    Converts boolean flags for output types to a string representation.

    :param combined: Flag to include combined video and audio output.
    :param spacing: The number of spaces between each output type in the resulting string.
    :param video_only: Flag to include video-only output.
    :param audio_only: Flag to include audio-only output.
    :param subtitles_only: Flag to include subtitles-only output.
    :param thumbnail: Flag to include thumbnail output.
    :param info: Flag to include info output.
    :param comments: Flag to include comments output.

    :return: A string representation of the output types to keep.
    """
    output_types = []

    # version 1
    # if combined:       output_types.append(COMBINED_SYMBOL)
    # if audio_only:     output_types.append(AUDIO_ONLY_SYMBOL)
    # if video_only:     output_types.append(VIDEO_ONLY_SYMBOL)
    # if subtitles_only: output_types.append(SUBTITLES_ONLY_SYMBOL)
    # if thumbnail:      output_types.append(THUMBNAIL_SYMBOL)
    # if info:           output_types.append(INFO_SYMBOL)
    # if comments:       output_types.append(COMMENTS_SYMBOL)

    # version 2
    output_types.append(COMBINED_SYMBOL if combined else " ")
    output_types.append(AUDIO_ONLY_SYMBOL if audio_only else " ")
    output_types.append(VIDEO_ONLY_SYMBOL if video_only else " ")
    output_types.append(SUBTITLES_ONLY_SYMBOL if subtitles_only else " ")
    output_types.append(THUMBNAIL_SYMBOL if thumbnail else " ")
    output_types.append(INFO_SYMBOL if info else " ")
    output_types.append(COMMENTS_SYMBOL if comments else " ")

    return (" " * spacing).join(output_types)
#end

def updateOutputKeepsStr(current_str: str, symbol: str, action: str) -> str:
    symbol_flags = {
        COMBINED_SYMBOL: "combined",
        AUDIO_ONLY_SYMBOL: "audio_only",
        VIDEO_ONLY_SYMBOL: "video_only",
        SUBTITLES_ONLY_SYMBOL: "subtitles_only",
        THUMBNAIL_SYMBOL: "thumbnail",
        INFO_SYMBOL: "info",
        COMMENTS_SYMBOL: "comments"
    }

    if symbol not in symbol_flags:
        raise ValueError("Invalid symbol")

    if action not in ('on', 'off', 'toggle'):
        raise ValueError("Invalid action")

    current_flags = {
        "combined":         COMBINED_SYMBOL in current_str,
        "audio_only":       AUDIO_ONLY_SYMBOL in current_str,
        "video_only":       VIDEO_ONLY_SYMBOL in current_str,
        "subtitles_only":   SUBTITLES_ONLY_SYMBOL in current_str,
        "thumbnail":        THUMBNAIL_SYMBOL in current_str,
        "info":             INFO_SYMBOL in current_str,
        "comments":         COMMENTS_SYMBOL in current_str,
    }

    flag_to_update = symbol_flags[symbol]

    if action == 'on':
        current_flags[flag_to_update] = True
    elif action == 'off':
        current_flags[flag_to_update] = False
    elif action == 'toggle':
        current_flags[flag_to_update] = not current_flags[flag_to_update]

    return setOutputKeepsStr(**current_flags)
#end