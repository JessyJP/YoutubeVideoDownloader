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
# Imports
from enum import Enum

## ================================= Download Keep Options =================================

class DownloadProgress():# TODO: enum would be better, more rewriting is needed
    DONE = "Done!"
    ERROR = "Error!"
    IN_PROGRESS = "Downloading Now..."

class MediaSymbols(Enum):
    COMBINED       = "☑"
    AUDIO_ONLY     = "Ⓐ"
    VIDEO_ONLY     = "Ⓥ"
    SUBTITLES_ONLY = "Ⓢ"
    THUMBNAIL      = "Ⓣ"
    INFO           = "ⓘ"
    COMMENTS       = "ⓒ"

    @classmethod
    def get_all_symbol_values_as_list(cls):
        return [symbol.value for symbol in cls]
    
    @staticmethod
    def get_media_symbols_as_dict():
        return {f"{symbol.name}_SYMBOL": symbol.value for symbol in MediaSymbols}


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