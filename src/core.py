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
## ================================= Module management functions =================================
# Main imports
import os
import sys
import platform
import subprocess
import threading

isDeployed = getattr(sys, "frozen", False)

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
            print(f"Installing missing module: {module}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        #end
    #end
#end

## Check & Install packages
install_missing_modules(["urlextract","pandas","requests"])
install_missing_modules(["pytube","pytchat","tqdm","ffmpeg-python"])

## Add the core functionality  modules
import pandas as pd
from pytube import YouTube, Playlist, Channel # py/Youtube Classes
import ffmpeg as ffmpeg # Video Editing Module
from tqdm import tqdm

# Text and URL string data handling
import logging
from typing import List, Set
from urlextract import URLExtract
import requests
import re

from typing import List, Union, Tuple, Any,  Optional
from typing import *
from dataclasses import dataclass, field
from typing import NamedTuple
import shutil



import json
import csv
import datetime
import pytz
import pytchat


install_missing_modules(["beautifulsoup4"])
install_missing_modules(["google-api-python-client","google_auth_oauthlib"])
from bs4 import BeautifulSoup
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

install_missing_modules(["youtube_dl"])
from core_alternative import *

logger = logging.getLogger(__name__)

## ================================= Download Keep Options =================================
COMBINED_SYMBOL = "☑"
AUDIO_ONLY_SYMBOL = "Ⓐ"
VIDEO_ONLY_SYMBOL = "Ⓥ"
SUBTITLES_ONLY_SYMBOL = "Ⓢ"
THUMBNAIL_SYMBOL = "Ⓣ"
INFO_SYMBOL = "ⓘ"
COMMENTS_SYMBOL = "ⓒ"

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
        "combined": COMBINED_SYMBOL in current_str,
        "audio_only": AUDIO_ONLY_SYMBOL in current_str,
        "video_only": VIDEO_ONLY_SYMBOL in current_str,
        "subtitles_only": SUBTITLES_ONLY_SYMBOL in current_str,
        "thumbnail": THUMBNAIL_SYMBOL in current_str,
        "info": INFO_SYMBOL in current_str,
        "comments": COMMENTS_SYMBOL in current_str,
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

## ================================= Video Info class =================================
class VideoInfo(YouTube):
    def __init__(
        self,
        url: str,
        download_status: str = setOutputKeepsStr(combined=True),#"   ☑   "
        inputOrderIndex: int = None,
    ):
        super().__init__(url)

        self.download_status = download_status
        self.inputOrderIndex = inputOrderIndex
        self.logger = []

        # Get the best audio and video streams
        audio_stream = self.streams.filter(type="audio").order_by("abr").last()
        video_stream = self.streams.filter(type="video").order_by("resolution").last()

        # Get the best fps
        fps = max(video_stream.fps, 0)

        # Quality
        self.quality_str = f"{video_stream.resolution}@{fps}fps/{audio_stream.abr}kbps"
        self.audio_bitrate = audio_stream.abr
        self.video_resolution = video_stream.resolution
        self.video_fps = fps

        # Filesize
        self.video_size_bytes = video_stream.filesize + audio_stream.filesize# TODO:
        self.video_size_mb = round(self.video_size_bytes / (1024 * 1024))# TODO:Better and updatable calculation is needed
    #end

    def as_tuple(self) -> Tuple:
        return (
            self.download_status,
            self.watch_url,
            self.title,
            self.author,
            self.length,
            self.description,
            self.publish_date,
            self.views,
            self.thumbnail_url,
            self.rating,
            self.video_id,
            self.quality_str,
            str(self.video_size_mb)+ " MB",
        )
    #end

    # ----- Steam Selection functions and download from stream
    def select_audio_stream(self, max_audio_bitrate, formatPriority=[]):
        audio_streams_to_check = self.streams.filter(only_audio=True).order_by('abr').desc()
        if not max_audio_bitrate == "max":
            audio_streams_to_check = [s for s in audio_streams_to_check if propToInt(s.abr,"kbps") <= max_audio_bitrate]
        #end

        if formatPriority == []:
            return audio_streams_to_check[0]
        else:
            for format in formatPriority:
                for stream in audio_streams_to_check:
                    if stream.mime_type.startswith(f'audio/{format}'):
                        return stream
                    #end
                #end
            #end
            return audio_streams_to_check[0]
        #end
    #end

    def select_video_stream(self, max_resolution, max_fps, formatPriority=[]):
        video_streams_to_check = self.streams.filter(only_video=True).order_by('resolution').desc()

        # Filter by max resolution
        if max_resolution != "max":
            video_streams_to_check = [s for s in video_streams_to_check if propToInt(s.resolution, "p") <= max_resolution]
        #end

        # Filter by max fps
        if max_fps != "max":
            video_streams_to_check = [s for s in video_streams_to_check if s.fps <= max_fps]
        #end

        # Select stream based on format priority
        if formatPriority == []:
            return video_streams_to_check[0]
        else:
            for format in formatPriority:
                for stream in video_streams_to_check:
                    if stream.mime_type.startswith(f'video/{format}'):
                        return stream
                    #end
                #end
            #end
        # Fallback to the first available stream if none match the format priority
        return video_streams_to_check[0]
        #end
    #end

    def download_audio(self,audio_stream, output):
        # Download the highest quality audio
        audio_filename = f"{self.title}.mp3"
        audio_filename = check_for_disallowed_filename_chars(audio_filename)
        print(f"Downloading audio for {self.title}...")

        audio_stream.download(output, filename=audio_filename)

        audio_file = os.path.join(output, audio_filename)

        print(f"Download complete: {audio_file}")

        return audio_file
    #end

    def download_video(self,video_stream, output):
        # Download the video file
        video_filename = f"{self.title}.mp4"
        video_filename = check_for_disallowed_filename_chars(video_filename)
        print(f"Downloading video ({video_stream.resolution}) for {self.title}...")

        video_stream.download(output, filename=video_filename)
        video_file = os.path.join(output, video_filename);
        print(f"Download complete: {video_file}")
        return video_file
    #end

    def process_downloads_combine_keep(self, output_dir, limits, outputExt=".mkv"):
        strOut = f"Process Entry Download: ";
        temp_path = self.make_tmp_dir(output_dir)
        self.log("Create temporary directory: "+temp_path)

        if COMBINED_SYMBOL in self.download_status or  AUDIO_ONLY_SYMBOL in self.download_status:  
            # Download the audio files with the relevant quality settings
            audioStream = self.select_audio_stream(limits.bitrate, limits.audio_format_priority)
            audio_filename = self.download_audio(audioStream,temp_path)
            self.log(strOut+"Audio: "+audio_filename+" ...")
        #end

        if COMBINED_SYMBOL in self.download_status or  VIDEO_ONLY_SYMBOL in self.download_status:
            # Download the video file with the relevant quality settings
            videoStream = self.select_video_stream(limits.resolution,limits.fps,limits.video_format_priority)
            video_filename = self.download_video(videoStream,temp_path)
            self.log(strOut+"Video: "+video_filename+" ...")
        #end

        #TODO: download all subtitles and integrate them

        if COMBINED_SYMBOL in self.download_status:
            # Call the combine function
            outputFilename = os.path.join(output_dir,check_for_disallowed_filename_chars(self.title)+outputExt)
            audio_filenames = [audio_filename]
            subtitle_filenames = []  # Assuming no subtitles for now
            self.log(strOut+"Combining Audio and Video: "+outputFilename)
            combine_via_auto_selection(outputFilename,video_filename, audio_filenames, subtitle_filenames)

            # There are multiple options for merging
            # NOTE: FFMPEG    (implemented)
            # NOTE: mkvmerge  (implemented)
            # TODO: VLC
        #end

        if AUDIO_ONLY_SYMBOL in self.download_status:
            shutil.move(audio_filename,output_dir)
        #end        
        if VIDEO_ONLY_SYMBOL in self.download_status:
            shutil.move(video_filename,output_dir)
        #end
        if SUBTITLES_ONLY_SYMBOL in self.download_status:
            self.download_subtitles(output_dir,any)# TODO: will have to download them in advance and move them later
        #end
        if THUMBNAIL_SYMBOL in self.download_status:
            self.download_thumbnail(output_dir)
        #end

        if INFO_SYMBOL in self.download_status:
            self.download_video_info(output_dir)
        #end

        if COMMENTS_SYMBOL in self.download_status:
            self.download_comments(output_dir)
        #end

        # Clean up the temporary directory and delete it
        self.log("Clean :"+temp_path)
        shutil.rmtree(temp_path)
    #end

    # ----- More download methods -----
    def download_subtitles(self,output_dir, languages):
        pass
    #end

    # Function to download thumbnail
    def download_thumbnail(self, output_dir: str, format="jpg") -> str:
        thumbnail_url = self.thumbnail_url
        thumbnail_filename = os.path.join(output_dir, f"{self.title}_thumbnail.{format}")
        thumbnail_data = requests.get(thumbnail_url).content
        with open(thumbnail_filename, 'wb') as f:
            f.write(thumbnail_data)
        return thumbnail_filename
    #end

    # Function to download video info in a text file
    def download_video_info(self, output_dir: str) -> str:
        video_info_filename = os.path.join(output_dir, f"{self.title}_info.txt")
        with open(video_info_filename, 'w') as f:
            f.write(f"Title: {self.title}\n")
            f.write(f"Author: {self.author}\n")
            f.write(f"Video Length: {self.length}\n") # Adding video length in seconds
            f.write(f"Description: {self.description}\n")
            f.write(f"Publish Date: {self.publish_date}\n")
            f.write(f"Views: {self.views}\n")
            f.write(f"Thumbnail URL: {self.thumbnail_url}\n")
            f.write(f"Rating: {self.rating}\n")
            f.write(f"Video ID: {self.video_id}\n")
            f.write(f"Video URL: {self.watch_url}\n") # Adding video URL
            f.write(f"Video Embed URL: {self.embed_url}\n") # Adding embed URL
            f.write(f"Video Age Restricted: {self.age_restricted}\n") # Adding age restriction info
            f.write(f"Video Keywords: {', '.join(self.keywords)}\n") # Adding video keywords
            audio_stream = self.streams.filter(type="audio").order_by("abr").last()
            video_stream = self.streams.filter(type="video").order_by("resolution").last()
            fps = max(video_stream.fps, 0)
            quality_str = f"{video_stream.resolution}@{fps}fps/{audio_stream.abr}kbps"
            f.write(f"Quality: {quality_str}\n")
        return video_info_filename
    #end

    def download_comments(self, output_dir: str, output_format: str = "json") -> str:
        """
        Download the comments for the video.

        :param output_dir: The directory where the output file will be saved.
        :param output_format: The output file format. Supported formats are "json" and "csv". Default is "json".
        :return: The full path of the output file.
        """
        # Create the output file path
        output_filename = check_for_disallowed_filename_chars(f"{self.title}_comments.{output_format}")
        output_file_path = os.path.join(output_dir, output_filename)

        # Download the comments and write them to the output file
        if output_format == "json":
            comments = pytchat.create(video_id=self.video_id)
            comments_list = []
            for c in comments.sync_items():
                comment = {
                    "text": c.message,
                    "author": c.author.name,
                    "author_channel_url": c.author.channel_url,
                    "published_at": c.datetime.isoformat(),
                    "likes": c.likecount,
                    "replies": c.replycount
                }
                comments_list.append(comment)

            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(comments_list, f, ensure_ascii=False, indent=4)
        elif output_format == "csv":
            comments = pytchat.create(video_id=self.video_id)
            fieldnames = ["text", "author", "author_channel_url", "published_at", "likes", "replies"]
            with open(output_file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for c in comments.sync_items():
                    writer.writerow({
                        "text": c.message,
                        "author": c.author.name,
                        "author_channel_url": c.author.channel_url,
                        "published_at": c.datetime.isoformat(),
                        "likes": c.likecount,
                        "replies": c.replycount
                    })
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        return output_file_path
    #end

    # ---- Extra functions ----
    def log(self, message: str) -> None:
        """
        Log a message by appending it to the logger list.

        :param message: The message to be logged.
        """
        self.logger.append(message)
    #end

    def make_tmp_dir(self,output_dir):
        # Create a hidden subdirectory in the user-selected download location
        dir_prefix = "." # For hidden directory
        temp_dir = check_for_disallowed_filename_chars(self.title)
        temp_path = os.path.join(output_dir, f"{dir_prefix}{temp_dir}")
        os.makedirs(temp_path, exist_ok=True)
        return temp_path
    #end

    def checkIfDownloadIsPending(self) -> bool:
        """
        Check if the video download is pending or completed.

        :return: True if the download is pending (checkbox is checked), False otherwise.
        """
        return "☑" in self.download_status
    #end
#end

class LimitsAndPriority:
    def __init__(self):
        self.bitrate = None
        self.audio_format_priority = None
        self.resolution = None
        self.fps = None
        self.video_format_priority = None
    #end

    def setLimitsToMax(self):
        self.bitrate = "max kbps"
        self.resolution = "max p"
        self.fps = propToInt(self.fps,"max fps")
    #end

    def to_numeric(self):
        self.bitrate = propToInt(self.bitrate,"kbps")
        self.resolution = propToInt(self.resolution,"p")
        self.fps = propToInt(self.fps,"fps")
    #end
#end

def propToInt(prop,str):
    intProp = prop.split(str)[0].strip()
    try:
        intProp = int(intProp)
        return intProp
    except (TypeError, ValueError):
        pass
    #end
    return prop
#end

def get_variable_names(cls):
    return list(cls.__annotations__.keys())
#end

def get_variable_types(cls):
    return list(cls.__annotations__.values())
#end

## ================================= Input Pre-Download get/select functions =================================

def extract_URL_list_from_text(text: str) -> List[str]:
    """
    Extracts a list of URLs from a given text string.

    Args:
        text (str): The input text string.

    Returns:
        List[str]: A list of URLs extracted from the input text string.
    """
    url_list = []

    try:
        # Create an instance of the urlextract library
        custom_cache_path = "./data/tlds-alpha-by-domain.txt"
        url_extractor = URLExtract()
        url_extractor.cache_file = custom_cache_path
        url_extractor.update()

        # Extract URLs from the input text string
        url_list = list(set(url_extractor.find_urls(text)))

    except Exception as e:
        print(f"Error using URLExtract: {e}")
        print("Using fallback method (regular expression) for URL extraction.")

        # Fallback method: use a regular expression for URL extraction
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        url_list = list(set(url_pattern.findall(text)))
    #end

    return url_list
#end

def get_video_urls_from_playlist(playlist_url: str) -> Set[str]:
    """
    Extracts a set of video URLs from a given YouTube playlist URL.

    Args:
        playlist_url (str): The URL of the YouTube playlist.

    Returns:
        Set[str]: A set of video URLs extracted from the YouTube playlist.
    """
    try:
        # Initialize the Playlist object with the given URL
        playlist = Playlist(playlist_url)
    except Exception as e:
        print(f"Error fetching playlist: {e}")
        return set()
    #end

    # Extract all video URLs from the playlist
    video_urls = set(playlist.video_urls)

    return video_urls
#end

def get_videos_and_playlists_from_Channel(channel_url: str) -> Set[str]:
    channel = Channel(channel_url)
    return set(channel.video_urls + channel.playlist_urls)
#end

def get_html_content(url: str, timeout: int = 10) -> Optional[Union[str, Exception]]:
    """
    Fetches the HTML content from the specified URL.

    Args:
        url (str): The URL to fetch the HTML content from.
        timeout (int): The number of seconds to wait for the server to respond (default is 10 seconds).

    Returns:
        Optional[Union[str, Exception]]: The HTML content as a string if the request was successful,
        otherwise an exception object describing the error.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {url}: {e}")
        return e
    #end
#end



def extract_video_urls_from_page(youtube_url):#TODO doesn't work 
    # Send a GET request to the YouTube page
    response = requests.get(youtube_url)

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the <a> tags with a class of "yt-simple-endpoint style-scope ytd-video-renderer"
    video_links = soup.find_all('a', class_='yt-simple-endpoint style-scope ytd-video-renderer')

    # Extract the href attribute from each <a> tag
    video_urls = [link['href'] for link in video_links]

    # Prepend "https://www.youtube.com" to each URL
    video_urls = ['https://www.youtube.com' + url for url in video_urls]

    return video_urls


def get_channel_videos(channel_id): #TODO not tested THIS is alternative channel video extraction
    # Set up the YouTube Data API client
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json" # Replace with your client secrets file path
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Authenticate and construct the service object
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # Get the playlist ID for the channel's uploads playlist
    request = youtube.channels().list(part="contentDetails", id=channel_id)
    response = request.execute()
    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    # Get all the video IDs from the uploads playlist
    videos = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(part="contentDetails", playlistId=playlist_id, maxResults=50, pageToken=next_page_token)
        response = request.execute()

        for item in response["items"]:
            video_id = item["contentDetails"]["videoId"]
            videos.append(f'https://www.youtube.com/watch?v={video_id}')

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return videos
#end

# -------- Get the video info from the URL --------
def get_url_info_entry(url: str, use_alternative=False) -> Union[VideoInfo, VideoInfo_alternative, None]:
    try:
        video_info = VideoInfo(url=url)
        return video_info
    except Exception as e:
        print(f"An error occurred while fetching the video information using VideoInfo for {url}: {e}")
        if use_alternative:
            try:
                video_info_alt = VideoInfo_alternative(url)
                return video_info_alt
            except Exception as e_alt:
                print(f"An error occurred while fetching the video information using VideoInfo_alternative for {url}: {e_alt}")
            #end
        #end
        return None
    #end
#end

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

## ================================= Progress & Other function =================================

def on_progress(stream, chunk, bytes_remaining):
    global progress_bar
    progress_bar.update(progress_bar.total - bytes_remaining)

## ================================= Combine audio-video functions =================================
def combine_via_auto_selection(output_file, video_filename, audio_filenames, subtitle_filenames):
    os_name = platform.system()
    os_arch = platform.architecture()[0]

    # if os_name == 'Windows' and os_arch == '64bit':
    #     combine_via_mkvmerge(output_file, video_filename, audio_filenames, subtitle_filenames)
    # else:
    combine_via_ffmpeg(output_file, video_filename, audio_filenames, subtitle_filenames)
    #end
#end

def combine_via_ffmpeg(output_file, video_filename, audio_filenames, subtitle_filenames):
    video = ffmpeg.input(video_filename)
    audio = ffmpeg.input(audio_filenames[0])

    # Combine video and audio streams using the 'copy' codec to avoid transcoding
    output = ffmpeg.output(video, audio, output_file, format='matroska', vcodec='copy', acodec='copy')

    if isDeployed:
        # Run the ffmpeg command
        process = output.run_async(pipe_stdout=True, pipe_stderr=True, overwrite_output=True)
        stdout, stderr = process.communicate()

        # stdout and stderr are bytes, decode them to strings if needed
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        # do something with stdout and stderr
        print(stdout, stderr)
    else:
        # Run the ffmpeg command
         output.run(overwrite_output=True)
    #end
#end

def combine_via_mkvmerge(output_file, video_filename, audio_filenames, subtitle_filenames):
    executable = r"./mkvtoolnix/mkvmerge.exe"#TODO: this has to be edited, maybe add the c\program files\-path
    # Prepare the arguments for mkvmerge
    args = [executable, "-o", output_file, video_filename]
    for audio in audio_filenames:
        args += ["--language", "0:und", audio]
    #end
    for subtitle in subtitle_filenames:
        args += ["--language", "0:und", subtitle]
    #end

    # Call mkvmerge via the command line
    subprocess.run(args, check=True)
#end

## ================================= Multithreading functions =================================
class MyThread(threading.Thread):
    threads = []

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self.exception = None
        self.exitcode = 0
        MyThread.threads.append(self)

    def run(self):
        try:
            super(MyThread, self).run()
        except Exception as e:
            self.exception = e
            self.exitcode = 1

    @classmethod
    def get_all_threads(cls, name_contains=""):
        threads = [t for t in cls.threads if name_contains in t.getName()]
        return threads

    @classmethod
    def get_active_threads(cls, thread_list=None):
        if thread_list is None:
            thread_list = cls.threads
        active_threads = [t for t in thread_list if t.is_alive()]
        return active_threads

    @classmethod
    def get_successful_threads(cls, thread_list=None):
        if thread_list is None:
            thread_list = cls.threads
        completed_threads = [t for t in thread_list if not t.is_alive() and t.exception is None]
        return completed_threads

    @classmethod
    def get_errored_threads(cls, thread_list=None):
        if thread_list is None:
            thread_list = cls.threads
        errored_threads = [t for t in thread_list if not t.is_alive() and t.exitcode != 0]
        return errored_threads

    @classmethod
    def get_multithread_stats(cls, name_contains=""):
        thread_list = cls.get_all_threads(name_contains)
        active_threads = cls.get_active_threads(thread_list)
        successful_threads = cls.get_successful_threads(thread_list)
        errored_threads = cls.get_errored_threads(thread_list)

        stats = {
            "total_threads": len(cls.threads),
            "active_threads": len(active_threads),
            "successful_threads": len(successful_threads),
            "errored_threads": len(errored_threads)
        }

        return stats
    #end    

    @classmethod
    def reset_threads(cls):
        cls.threads.clear()
    #end
#end