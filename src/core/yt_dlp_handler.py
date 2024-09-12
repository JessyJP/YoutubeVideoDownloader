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

import os
import subprocess
from yt_dlp import YoutubeDL
from typing import Tuple
import requests
import shutil
from datetime import datetime
from PIL import Image
from io import BytesIO

from core.validation_methods import check_for_disallowed_filename_chars
from core.download_options import setOutputKeepsStr
from core.post_download_mux import combine_via_auto_selection


## ================================= Video Info class =================================
class VideoInfo:
    def __init__(
        self,
        url: str,
        download_status: str = setOutputKeepsStr(combined=True),
        inputOrderIndex: int = None,
    ):
        self.url = url
        self.download_status = download_status
        self.inputOrderIndex = inputOrderIndex
        self.logger = []

        ydl_opts = {'format': 'bestaudio+bestvideo/best'}
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.info = info_dict
            self.title = info_dict.get('title', None)
            self.author = info_dict.get('uploader', None)
            self.length = info_dict.get('duration', None)
            self.description = info_dict.get('description', None)
            self.publish_date = info_dict.get('upload_date', None)
            self.views = info_dict.get('view_count', None)
            self.thumbnail_url = info_dict.get('thumbnail', None)
            self.rating = info_dict.get('average_rating', None)
            self.video_id = info_dict.get('id', None)

            # Extract video and audio information
            audio_stream = self.get_best_audio_stream(info_dict['formats'])
            video_stream = self.get_best_video_stream(info_dict['formats'])

            # Quality string
            if audio_stream and video_stream:
                self.quality_str = f"{video_stream['height']}p@{video_stream.get('fps', 0)}fps/{audio_stream['abr']}kbps"
            else:
                self.quality_str = "Unknown"

            self.audio_bitrate = audio_stream.get('abr', 0) if audio_stream else None
            self.video_resolution = video_stream.get('height', None) if video_stream else None
            self.video_fps = video_stream.get('fps', 0) if video_stream else None

            # Filesize
            self.video_size_bytes = (video_stream.get('filesize', 0) or 0) + (audio_stream.get('filesize', 0) or 0) if video_stream and audio_stream else 0
            self.video_size_mb = round(self.video_size_bytes / (1024 * 1024), 2) if self.video_size_bytes else 0

            self.base_output_name = check_for_disallowed_filename_chars(self.title)

            self.creationTimestamp = datetime.now()

    def get_best_audio_stream(self, formats):
        """ Get the best audio stream from the list of formats. """
        try:
            audio_streams = [f for f in formats if f.get('acodec') != 'none' and f.get('abr') is not None]
            if audio_streams:
                best_audio_stream = max(audio_streams, key=lambda f: f['abr'], default=None)
                self.log(f"Best audio stream found: {best_audio_stream}")
                return best_audio_stream
            else:
                self.log("No valid audio streams found.")
                return None
        except Exception as e:
            self.log(f"Error selecting best audio stream: {e}")
            return None

    def get_best_video_stream(self, formats):
        """ Get the best video stream from the list of formats. """
        try:
            video_streams = [f for f in formats if f.get('vcodec') != 'none' and f.get('height') is not None]
            if video_streams:
                best_video_stream = max(video_streams, key=lambda f: f['height'], default=None)
                self.log(f"Best video stream found: {best_video_stream}")
                return best_video_stream
            else:
                self.log("No valid video streams found.")
                return None
        except Exception as e:
            self.log(f"Error selecting best video stream: {e}")
            return None

    def as_tuple(self) -> Tuple:
        return (
            self.download_status,
            self.url,
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
            str(self.video_size_mb) + " MB",
        )

    def as_dict(self) -> dict:
        return {
            "download_status": self.download_status,
            "watch_url": self.url,
            "title": self.title,
            "author": self.author,
            "length": self.length,
            "description": self.description,
            "publish_date": self.publish_date,
            "views": self.views,
            "thumbnail_url": self.thumbnail_url,
            "rating": self.rating,
            "video_id": self.video_id,
            "quality_str": self.quality_str,
            "download_size": str(self.video_size_mb) + " MB",
        }

    # ----- Stream Selection functions and download from stream -----
    def select_audio_stream(self, max_audio_bitrate, formatPriority=[]):
        audio_streams = self.info['formats']
        audio_streams_to_check = [f for f in audio_streams if f['acodec'] != 'none']
        audio_streams_to_check.sort(key=lambda x: x['abr'], reverse=True)

        if max_audio_bitrate != "max":
            audio_streams_to_check = [s for s in audio_streams_to_check if int(s['abr']) <= max_audio_bitrate]

        return audio_streams_to_check[0]

    def select_video_stream(self, max_resolution, max_fps, formatPriority=[]):
        video_streams = self.info['formats']
        video_streams_to_check = [f for f in video_streams if f['vcodec'] != 'none']
        video_streams_to_check.sort(key=lambda x: x['height'], reverse=True)

        if max_resolution != "max":
            video_streams_to_check = [s for s in video_streams_to_check if int(s['height']) <= max_resolution]

        if max_fps != "max":
            video_streams_to_check = [s for s in video_streams_to_check if s['fps'] <= max_fps]

        return video_streams_to_check[0]

    def wget_thumbnail(self, format='pil'):
        """
        Download the thumbnail and return it in the specified format.
        format: 'blob' (return binary data), 'pil' (return PIL image), 'raw' (return raw response content)
        """
        try:
            response = requests.get(self.thumbnail_url)
            response.raise_for_status()

            if format == 'blob':
                return response.content  # Binary blob (byte data)
            elif format == 'raw':
                return BytesIO(response.content)  # Raw data as a BytesIO object
            elif format == 'pil':
                image = Image.open(BytesIO(response.content))  # PIL Image object
                return image
            else:
                raise ValueError("Invalid format specified")
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    def download_audio(self, audio_stream, output):
        """ Download the audio stream. """
        audio_filename = f"{self.base_output_name}.aac"
        audio_filename = check_for_disallowed_filename_chars(audio_filename)
        print(f"Downloading audio for [{self.title}] ...")

        ydl_opts = {
            'format': audio_stream['format_id'],
            'outtmpl': os.path.join(output, audio_filename),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        audio_file = os.path.join(output, audio_filename)
        print(f"Download complete: {audio_file}")
        return audio_file

    def download_video(self, video_stream, output):
        """ Download the video stream. """
        video_filename = f"{self.base_output_name}.mp4"
        video_filename = check_for_disallowed_filename_chars(video_filename)
        print(f"Downloading video ({video_stream['height']}p) for [{self.title}] ...")

        ydl_opts = {
            'format': video_stream['format_id'],
            'outtmpl': os.path.join(output, video_filename),
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

        video_file = os.path.join(output, video_filename)
        print(f"Download complete: {video_file}")
        return video_file

    def process_downloads_combine_keep(self, limits, output_dir, outputExt=".mkv"):
        """ Process audio and video downloads and combine them. """
        output_dir = os.path.abspath(output_dir)
        temp_path = self.make_tmp_dir(output_dir)

        # Download audio and video
        audio_stream = self.select_audio_stream(limits.bitrate, limits.audio_format_priority)
        video_stream = self.select_video_stream(limits.resolution, limits.fps, limits.video_format_priority)

        audio_filename = self.download_audio(audio_stream, temp_path)
        video_filename = self.download_video(video_stream, temp_path)

        output_filename = f"{self.base_output_name}{outputExt}"
        output_filename = check_for_disallowed_filename_chars(output_filename)
        output_filepath = os.path.join(output_dir, output_filename)

        combine_via_auto_selection(output_filepath, video_filename, [audio_filename], [])

        shutil.rmtree(temp_path)
        return output_filepath

    def download_thumbnail(self, output_dir: str, format="jpg") -> str:
        """ Download the thumbnail image. """
        thumbnail_url = self.thumbnail_url
        thumbnail_filename = os.path.join(output_dir, f"{self.base_output_name}_thumbnail.{format}")
        thumbnail_data = requests.get(thumbnail_url).content
        with open(thumbnail_filename, 'wb') as f:
            f.write(thumbnail_data)
        return thumbnail_filename

    def download_video_info(self, output_dir: str) -> str:
        """ Download video information into a text file. """
        video_info_filename = os.path.join(output_dir, f"{self.base_output_name}_info.txt")
        with open(video_info_filename, 'w') as f:
            f.write(f"Title: {self.title}\n")
            f.write(f"Author: {self.author}\n")
            f.write(f"Video Length: {self.length}\n")
            f.write(f"Description: {self.description}\n")
            f.write(f"Publish Date: {self.publish_date}\n")
            f.write(f"Views: {self.views}\n")
            f.write(f"Thumbnail URL: {self.thumbnail_url}\n")
            f.write(f"Rating: {self.rating}\n")
            f.write(f"Video ID: {self.video_id}\n")
            f.write(f"Video URL: {self.url}\n")

        return video_info_filename

    def download_comments(self, output_dir: str, output_format: str = "json") -> str:
        """ Download the comments for the video (to be implemented). """
        output_filename = check_for_disallowed_filename_chars(f"{self.base_output_name}.comments.{output_format}")
        output_file_path = os.path.join(output_dir, output_filename)

        # For now, we'll simulate the download process with a placeholder
        try:
            subprocess.run(['python', './src/core/download_video_comments2.py',
                            self.video_id, self.base_output_name, output_dir, output_format], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred in subprocess: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        return output_file_path

    # Helper methods
    def log(self, message: str) -> None:
        """ Log a message by appending it to the logger list. """
        self.logger.append(message)

    def make_tmp_dir(self, output_dir):
        """ Create a temporary directory for download storage. """
        dir_prefix = "."
        temp_dir = check_for_disallowed_filename_chars(self.video_id)
        temp_path = os.path.join(output_dir, f"{dir_prefix}{temp_dir}")
        os.makedirs(temp_path, exist_ok=True)
        return temp_path

    def checkIfDownloadIsPending(self) -> bool:
        """ Check if the download is pending. """
        return "☑" in self.download_status
