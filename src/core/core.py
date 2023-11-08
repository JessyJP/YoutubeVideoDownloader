

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