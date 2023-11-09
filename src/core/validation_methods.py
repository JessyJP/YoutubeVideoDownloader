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
# from typing import List, Union, Set, Any,  Optional
import re

## ================================= Check & Validation functions =================================

def is_youtube_url(url):
    youtube_domain_pattern = re.compile(
        r"(https?://)?(www\.)?(m\.)?(youtube\.com|youtu\.be|youtube-nocookie\.com|youtube.googleapis.com)/?([\w\-]*)"
    )
    match = youtube_domain_pattern.search(url)
    return bool(match)
#end

def checkForValidYoutubeURLs(list_Of_URLs):
    youtube_urls = []

    # Regular expression to match valid YouTube URLs
    youtube_url_pattern = re.compile(
        r"(https?://)?(www\.)?(m\.)?(youtube\.com|youtu\.be|youtube-nocookie\.com|youtube.googleapis.com)/((watch\?v=[a-zA-Z0-9_-]{11})|(embed/[a-zA-Z0-9_-]{11})|(v/[a-zA-Z0-9_-]{11}))(\S+)?"
    )

    # Check each if each url is a valid YouTube URL
    for url in list_Of_URLs:
        matches = youtube_url_pattern.findall(url)
        for match in matches:
            youtube_urls.append("".join(match))

    return youtube_urls
#end

def is_valid_youtube_playlist(url_to_check):
    # Check if the input is a string
    if not isinstance(url_to_check, str):
        return False
    #end

    # Define the YouTube playlist pattern
    pattern = r"\/playlist\?(?:list=)([-_a-zA-Z0-9]+)"

    # Check if the given URL matches the pattern
    match = re.search(pattern, url_to_check)

    # Return True if there's a match, False otherwise
    return bool(match)
#end

def check_for_disallowed_filename_chars(filepath):
    # Disallowed characters for Windows, macOS, and Linux file systems
    disallowed_chars = r'[<>:"/\\|?*]'

    # Substitute disallowed characters with an underscore
    sanitized_filepath = re.sub(disallowed_chars, '_', filepath)

    return sanitized_filepath
#end

def is_valid_youtube_channel(url: str) -> bool:
    # Check for all YouTube channel URL formats:
    # https://www.youtube.com/channel/UCXXXXXXXXXXXXXXXXXXXXX
    # https://www.youtube.com/c/ChannelName
    # https://www.youtube.com/@Username
    pattern = r'(https?://)?(www\.)?youtube\.com/(channel/UC[\w-]{22}|c/[\w-]+|@[\w-]+)'
    match = re.match(pattern, url)
    return match is not None
#end