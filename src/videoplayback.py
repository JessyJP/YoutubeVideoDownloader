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
from core import install_missing_modules 

required_modules = ["pafy","youtube-dl","python-vlc"]
install_missing_modules(required_modules)
import pafy
import vlc
import time

def play_youtube_video(url):
    # Get video details and select the best quality stream
    video = pafy.new(url)
    best_stream = video.getbest()

    # Create a VLC instance and set some basic options
    instance = vlc.Instance("--no-xlib")

    # Create a VLC media player object
    player = instance.media_player_new()

    # Set the media for the player
    player.set_media(instance.media_new(best_stream.url))

    # Play the video
    player.play()

    # Keep the video playing until it ends or the user closes the window
    while player.get_state() != vlc.State.Ended:
        time.sleep(0.1)

# Replace the URL with the YouTube video URL you want to play
youtube_url = "https://www.youtube.com/watch?v=ngrBbLTvjN4"
play_youtube_video(youtube_url)
