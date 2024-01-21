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