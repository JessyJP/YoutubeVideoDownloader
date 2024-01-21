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