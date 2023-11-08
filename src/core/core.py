

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



from bs4 import BeautifulSoup
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



logger = logging.getLogger(__name__)






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