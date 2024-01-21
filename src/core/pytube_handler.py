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

## Imports
import os
import subprocess
from pytube import YouTube # py/Youtube Classes
from typing import Tuple

import requests
import shutil
from datetime import datetime

# For image handling
from PIL import Image
from io import BytesIO

from core.validation_methods import check_for_disallowed_filename_chars
from core.download_options import setOutputKeepsStr
from core.download_options import * # TODO: list them one by one
from core.post_download_mux import combine_via_auto_selection

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

        # Get the default file name for the various files
        self.base_output_name = os.path.splitext(video_stream.default_filename)[0]
        # NOTE: alternatively we can use the title

        # Internal limiter which can allow limits per video
        self.internalLimiter = LimitsAndPriority()# TODO: will be currently unused
        # Output filepaths dictionary which stores the paths for each download symbol 
        self.outputFilepaths = {symbol: None for symbol in MediaSymbols.get_all_symbol_values_as_list()}
        # self.outputFilepaths = SimpleNamespace(**self.outputFilepaths)
        # Creation timestamp, which can be used for sorting
        self.creationTimestamp = datetime.now()
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

    def as_dict(self) -> dict:
        return {
            "download_status": self.download_status,
            "watch_url": self.watch_url,
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
            "download_size": str(self.video_size_mb) + " MB"
        }

    # ----- Steam Selection functions and download from stream
    def select_audio_stream(self, max_audio_bitrate, formatPriority=[]):
        audio_streams_to_check = self.streams.filter(only_audio=True).order_by('abr').desc()
        if not max_audio_bitrate == "max":
            audio_streams_to_check = [s for s in audio_streams_to_check if propToInt(s.abr,"kbps") <= max_audio_bitrate]
        #end

        # TODO:NOTE for now disable format priority. It may not be useful. 
        # Also there is a bug that here. 
        # Format priority only works if we additionally filter by ony the above criteria and then check
        # if formatPriority != []:
        #     for format in formatPriority:
        #         for stream in audio_streams_to_check:
        #             if stream.mime_type.startswith(f'audio/{format}'):
        #                 return stream
        #             #end
        #         #end
        #     #end
        # #end

        # Fallback to the first available stream if none match the format priority
        return audio_streams_to_check[0]
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

        # TODO:NOTE for now disable format priority. It may not be useful. 
        # Also there is a bug that here. 
        # Format priority only works if we additionally filter by ony the above criteria and then check
        # # Select stream based on format priority
        # if formatPriority != []:
        #     for format in formatPriority:
        #         for stream in video_streams_to_check:
        #             if stream.mime_type.startswith(f'video/{format}'):
        #                 return stream
        #             #end
        #         #end
        #     #end
        # #end

        # Fallback to the first available stream if none match the format priority
        return video_streams_to_check[0]
    #end
    
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
            #end
            
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None
        #end
    #end

    def download_audio(self,audio_stream, output):
        # Download the highest quality audio
        # TODO: we need to think a bit more about the naming and potential file format conflicts
        audio_filename = f"{self.base_output_name}.mp3"
        audio_filename = self.base_output_name+".aac"
        audio_filename = check_for_disallowed_filename_chars(audio_filename)
        print(f"Downloading audio for [{self.title}] ...")

        audio_stream.download(output, filename=audio_filename)

        audio_file = os.path.join(output, audio_filename)

        print(f"Download complete: {audio_file}")

        return audio_file
    #end

    def download_video(self,video_stream, output):
        # Download the video file
        video_filename = f"{self.base_output_name}.mp4"
        video_filename = check_for_disallowed_filename_chars(video_filename)
        print(f"Downloading video ({video_stream.resolution}) for [{self.title}] ...")

        video_stream.download(output, filename=video_filename)
        video_file = os.path.join(output, video_filename);
        print(f"Download complete: {video_file}")
        return video_file
    #end

    def process_downloads_combine_keep(self, limits, output_dir, outputExt=".mkv"):
        strOut = f"Process Entry Download: ";
        output_dir = os.path.abspath(output_dir)
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
            outputFilename = self.base_output_name+outputExt
            outputFilename = os.path.join(output_dir,check_for_disallowed_filename_chars(outputFilename))
            audio_filenames = [audio_filename]
            subtitle_filenames = []  # Assuming no subtitles for now
            self.log(strOut+"Combining Audio and Video: "+outputFilename)
            combine_via_auto_selection(outputFilename,video_filename, audio_filenames, subtitle_filenames)

            # There are multiple options for merging
            # NOTE: FFMPEG    (implemented)
            # NOTE: mkvmerge  (implemented)
            # TODO: VLC

            self.outputFilepaths[COMBINED_SYMBOL] = outputFilename
        #end

        if AUDIO_ONLY_SYMBOL in self.download_status:
            self.outputFilepaths[AUDIO_ONLY_SYMBOL] = shutil.move(audio_filename,output_dir)
        #end        
        if VIDEO_ONLY_SYMBOL in self.download_status:
            self.outputFilepaths[VIDEO_ONLY_SYMBOL] = shutil.move(video_filename,output_dir)
        #end
        if SUBTITLES_ONLY_SYMBOL in self.download_status:
            self.download_subtitles(output_dir,any)# TODO: will have to download them in advance and move them later
        #end
        if THUMBNAIL_SYMBOL in self.download_status:
            self.outputFilepaths[THUMBNAIL_SYMBOL]  = self.download_thumbnail(output_dir)
        #end

        if INFO_SYMBOL in self.download_status:
            self.outputFilepaths[INFO_SYMBOL]       = self.download_video_info(output_dir)
        #end

        if COMMENTS_SYMBOL in self.download_status:
            self.outputFilepaths[COMMENTS_SYMBOL]   = self.download_comments(output_dir)
        #end

        # Clean up the temporary directory and delete it
        self.log("Clean :"+temp_path)
        shutil.rmtree(temp_path)
    #end

    # ----- More download methods -----
    def download_subtitles(self,output_dir, languages):
        pass
        #TODO:NOTE note implemented
    #end

    # Function to download thumbnail
    def download_thumbnail(self, output_dir: str, format="jpg") -> str:
        thumbnail_url = self.thumbnail_url
        thumbnail_filename = os.path.join(output_dir, f"{self.base_output_name}.{format}")
        thumbnail_data = requests.get(thumbnail_url).content
        with open(thumbnail_filename, 'wb') as f:
            f.write(thumbnail_data)
        return thumbnail_filename
    #end

    # Function to download video info in a text file
    def download_video_info(self, output_dir: str) -> str:
        video_info_filename = os.path.join(output_dir, f"{self.base_output_name}_info.txt")
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
        output_filename = check_for_disallowed_filename_chars(f"{self.base_output_name}.comments.{output_format}")
        output_file_path = os.path.join(output_dir, output_filename)
        # NOTE: TODO the functionality for downloading the comments has to be revised in detail
        # NOTE: TODO currently this is unavailable
        
        try:
            subprocess.run(['python', './src/core/download_video_comments2.py', 
                            self.video_id, self.base_output_name, output_dir, output_format], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred in subprocess: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        #end

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
        temp_dir = check_for_disallowed_filename_chars(self.video_id)
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
        # Internal conversion method
        self.bitrate = "max kbps"
        self.resolution = "max p"
        self.fps = propToInt(self.fps,"max fps")
    #end

    def to_numeric(self):
        # Internal conversion method
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