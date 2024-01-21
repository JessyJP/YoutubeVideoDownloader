"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

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
