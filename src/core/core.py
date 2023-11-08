

# Main imports
import os
import sys
import platform
import subprocess
import threading



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

