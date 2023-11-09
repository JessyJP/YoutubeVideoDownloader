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

# Imports
import subprocess
from typing import Union
import ffmpeg as ffmpeg # Video Editing Module

# from core.common import isDeployed
import sys
isDeployed = getattr(sys, "frozen", False)


## ================================= Progress & Other function =================================

def on_progress(stream, chunk, bytes_remaining):
    global progress_bar
    progress_bar.update(progress_bar.total - bytes_remaining)

## ================================= Combine audio-video functions =================================
def combine_via_auto_selection(output_file, video_filename, audio_filenames, subtitle_filenames):

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