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
from typing import List, Union, Set, Any,  Optional
# from typing import *
from urlextract import URLExtract
import re
from pytube import Playlist, Channel # py/Youtube Classes
import requests
from bs4 import BeautifulSoup
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
# Core Imports
from core.pytube_handler import VideoInfo as VideoInfoPyTube
from core.youtube_dl_handler import VideoInfo as VideoInfoDL
from core.yt_dlp_handler import VideoInfo as VideoInfoYTDLP

# from core.common import logger
import logging
# Logging
logger = logging.getLogger(__name__)

## ================================= Get the video info from the URL function =================================

def get_video_info_item_from_url(url: str, use_alternative=False) -> Union[VideoInfoPyTube, VideoInfoYTDLP, None]:
    try:
        video_info = VideoInfoYTDLP(url=url)
        return video_info
    except Exception as e:
        print(f"An error occurred while fetching the video information using {VideoInfoPyTube} for {url}: {e}")
        if use_alternative:
            try:
                video_info_alt = VideoInfoPyTube(url)
                return video_info_alt
            except Exception as e_alt:
                print(f"An error occurred while fetching the video information using {VideoInfoPyTube} for {url}: {e_alt}")
            #end
        #end
        return None
    #end
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
#end


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
        #end

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
        #end
    #end

    return videos
#end