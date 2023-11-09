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

## Imports
import os
from pytube import YouTube # py/Youtube Classes
from typing import Tuple

import requests
import shutil
import json
import csv
import pytchat

from core.validation_methods import check_for_disallowed_filename_chars
from core.download_manager import combine_via_auto_selection
from core.download_options import setOutputKeepsStr
from core.download_options import * # TODO: list them one by one

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

    def process_downloads_combine_keep(self, limits, output_dir, outputExt=".mkv"):
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

## ================================= Limit and Priority class =================================
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


## ================================= Helper functions =================================

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