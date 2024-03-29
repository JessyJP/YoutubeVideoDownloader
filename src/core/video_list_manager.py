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

import threading
from typing import List, Union
from core.download_options import DownloadProgress
from core.pytube_handler import LimitsAndPriority, VideoInfo
import shutil
from time import sleep
import warnings

from core.custom_thread import CustomThread # TODO:NOTE could be named "CustomThreading" too
from core.validation_methods import checkForValidYoutubeURLs, is_valid_youtube_channel, is_valid_youtube_playlist
from core.url_text_processor import extract_URL_list_from_text, get_html_content, get_video_urls_from_playlist, get_videos_and_playlists_from_Channel
from core.url_text_processor import get_video_info_item_from_url

# TODO: some functions could be expanded with a union of various video info classes if other library interfaces are implemented
class VideoListManager:
    # This function handles the diagnostic update in a separate thread
    diagnostics_thread = None;# Static variable
    # Class constructor
    def __init__(self):        
        # Video Info list
        self.infoList: List[VideoInfo] = []
        self.diagnostic_refresh_interval = 0.25# TODO a moderate value to be adjusted

    def getVideoList(self):
        return self.infoList;

    def getItem(self,rowIndex):
        return self.infoList[rowIndex]
    
    def getItemIndex(self, video_info):
        index = self.infoList.index(video_info)
        return index
    
    def addItem(self, video_info: VideoInfo):
        self.infoList.append(video_info)

    def removeItem(self, video_info: VideoInfo):        
        if video_info is not None:
            # Remove the VideoInfo object from the infoList
            index_to_remove = self.infoList.index(video_info)
            self.infoList.pop(index_to_remove)

    # This method is used to locate a video info from a list
    def getItemByIndexOrVideoID(self, video_id: str, index: int = -1) -> Union[VideoInfo, None]:
        # Check if the input index is valid and if the video_id at that index matches the input video_id
        if 0 <= index < len(self.infoList) and self.infoList[index].video_id == video_id:
            return self.infoList[index]
        #end

        # Warning if the first check fails
        warnings.warn(f"Initial search by index {index} failed, performing exhaustive search.", RuntimeWarning)

        # If the index is not valid or the video_id doesn't match, search exhaustively
        for idx, video_info in enumerate(self.infoList):
            if video_info.video_id == video_id:
                warnings.warn(f"Found video at index {idx} instead of {index}.", RuntimeWarning)
                return video_info
            #end
        #end

        # Warning if the first check fails
        warnings.warn("Initial search by index failed, performing exhaustive search.", RuntimeWarning)

        # If no match is found, return None
        return None
    #end

    def getItemProp(index,property):
        pass
    #TODO: not implemented

    def setRowProp(index,property):
        pass
    #TODO: not implemented

    # Get the current URLs in the tree view and video IDs
    def getURL_videoIDList(self):
        current_url_entries = set()
        current_video_ids = set()
        for item in self.getVideoList():
            current_url_entries.add(item.watch_url)
            current_video_ids.add(item.video_id)
        #end
        return current_url_entries, current_video_ids
    #end

    def remove_duplicate_items(self):
        # Get the current video IDs in the tree view
        current_video_ids = set()
        for item in self.getVideoList():
            current_video_ids.add(item.video_id)
        #end
        
        # Check each row in the tree view and remove duplicates
        for item in self.getVideoList():
            video_id = item.video_id
            if video_id in current_video_ids:
                current_video_ids.remove(video_id)
            else:
                self.removeItem(item)
            #end
        #end
    #end

    ## --------------------------- URL/Text Analysis methods ----------------------------------------
    
    # Process Text and URLs
    def import_valid_Youtube_videos_from_textOrURL_list(self, text, use_analysis_multithreading, recursiveCheckOfURLcontent_mode=0):

        # Make sure to clean up the download list and simplify it from duplicates
        self.remove_duplicate_items()

        numYT_vidMSG = "- YouTube Video URL(s)"
        # Check the recursion level and check the input type. At the end the output should be a URL list.
        if recursiveCheckOfURLcontent_mode == 1:
            dispPrefix = self.getUiDispStatus().split(numYT_vidMSG)[0] + " - playlist videos"
            URLs_toCheck = text
        elif recursiveCheckOfURLcontent_mode == 3:
            dispPrefix = self.getUiDispStatus().split(numYT_vidMSG)[0] + " - sub-links"
            URLs_toCheck = extract_URL_list_from_text(text)
            URLs_toCheck = checkForValidYoutubeURLs(URLs_toCheck)  # TODO: needs to be improved
        else:  # recursiveCheckOfURLcontent_mode == 0# i.e. default
            global topLevelAnalyzeRunning
            topLevelAnalyzeRunning = True  # Could be used to regulate how many simultaneous Analyse operations there can be
            dispPrefix = "Import Youtube URLs : Currently Processing URL(s)"
            URLs_toCheck = extract_URL_list_from_text(text)
        #end

        # Remove duplicate URLs by converting to set and back to list
        URLs_toCheck = set(URLs_toCheck)
        N = len(URLs_toCheck)
        n = 0
        analysisThreads = []# This is used in the multithreading case only
        self.setUiDispStatus(f"{dispPrefix} found {N}")
        self.update_progressbar(n, N, recursiveCheckOfURLcontent_mode)

        # Process the URLs one at a time and add only unique ones
        for url in URLs_toCheck:
            # Run in Single thread or multithread mode
            if use_analysis_multithreading: 
                self.updateUiDistStatus_in_multithread_mode(self.diagnostic_refresh_interval);               
                t = CustomThread(target=self.process_url, args=(url, use_analysis_multithreading, recursiveCheckOfURLcontent_mode))
                t.start()
                analysisThreads.append(t)                
            else:
                n=n+1;
                self.setUiDispStatus(f"{dispPrefix} {n} of {N} {numYT_vidMSG} {len(self.getVideoList())} ")
                self.process_url(url, use_analysis_multithreading, recursiveCheckOfURLcontent_mode)
                self.update_progressbar(n, N, recursiveCheckOfURLcontent_mode)
            #end
        #end

        # In the multithread case wait for the analysis threads to first join
        if use_analysis_multithreading:
            # Wait for all threads to complete
            for t in analysisThreads:
                t.join()
            #end
        #end

        # To finish up the analysis
        if recursiveCheckOfURLcontent_mode == 0:  # This checks the recursion mode
            # Make sure to clean up the download list and simplify it from duplicates
            self.remove_duplicate_items()
            # Update the UI elements
            self.setUiDispStatus("URL import and Analysis is Complete!")  # Clear the diagnostic output
            # self.setUiDispStatus("");# Clear the diagnostic output #TODO: select one
            self.update_progressbar(N, N, recursiveCheckOfURLcontent_mode)
        #end
    #end

    def process_url(self, url, use_analysis_multithreading, recursiveCheckOfURLcontent_mode):  
        # Get the latest list of URL(s) and VideoID(s)
        current_url_entries, current_video_ids = self.getURL_videoIDList()

        if url not in current_url_entries:
            vi_item = get_video_info_item_from_url(url)

            if vi_item is None:
                if recursiveCheckOfURLcontent_mode == 0 or recursiveCheckOfURLcontent_mode == 2:  # This checks the recursion mode
                    try:
                        if is_valid_youtube_playlist(url):
                            recursiveCheckOfURLcontent_mode = 1  # This controls the recursion mode for playlists
                            urlsFromPlaylist = get_video_urls_from_playlist(url)
                            self.import_valid_Youtube_videos_from_textOrURL_list(urlsFromPlaylist, use_analysis_multithreading, recursiveCheckOfURLcontent_mode)
                        elif is_valid_youtube_channel(url):
                            recursiveCheckOfURLcontent_mode = 2  # This controls the recursion mode for channels
                            urlsFromChannel = get_videos_and_playlists_from_Channel(url)
                            self.import_valid_Youtube_videos_from_textOrURL_list(urlsFromChannel, use_analysis_multithreading, recursiveCheckOfURLcontent_mode)
                        else:
                            recursiveCheckOfURLcontent_mode = 3  # This controls the recursion mode for other urls
                            web_page_html = get_html_content(url)
                            self.import_valid_Youtube_videos_from_textOrURL_list(web_page_html, use_analysis_multithreading, recursiveCheckOfURLcontent_mode)
                        #end
                    #end
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        recursiveCheckOfURLcontent_mode = 0  # This controls the recursion mode
                    #end
                #end
                return
            #end
  
            # Check if the video ID already exists and insert a new row in the table with the URL and an empty checkbox and videoProperties
            if vi_item.video_id not in current_video_ids:
                self.addItem(vi_item)
            #end
        #end
    #end
    
    def updateUiDistStatus_in_multithread_mode(self, interval=0.01):# TODO: Could add this as a class variable so that it can be controlled
        # TODO: This could be redesigned such that it gets diagnostic message function which takes the relevant numbers. 
        # Only if the thread is not running
        if self.diagnostics_thread is None or not self.diagnostics_thread.is_alive():
            def diagnostic_message(stats):
                message = (
                    f"URL thread check(s) Total: {stats['total_threads']}    "
                    f"Active: {stats['active_threads']}    "
                    f"Completed: {stats['successful_threads']}    "
                    f"Errors: {stats['errored_threads']}    "
                )
                return message
            #end
            def display_diagnostics_thread(interval):
                while True:
                    stats = CustomThread.get_multithread_stats()
                    self.update_progressbar(
                            index_in=stats['successful_threads']+stats['errored_threads'],
                            total_in=stats['total_threads'], 
                            task_level=0)
                    self.setUiDispStatus(diagnostic_message(stats))
                    sleep(interval)

                    # Break condition: All threads from CustomThread are finished
                    if len(CustomThread.get_active_threads(CustomThread.threads)) == 0:
                        break
                    #end
                #end

                # Set self.diagnostics_thread to None when it's done
                self.diagnostics_thread = None
                CustomThread.reset_threads()
            #end

            self.diagnostics_thread = threading.Thread(target=display_diagnostics_thread, args=(interval,), daemon=True)
            self.diagnostics_thread.start()
        #end
    #end

    ## --------------------------- Video info download ----------------------------------------

    def video_item_process_download(self, item: VideoInfo, limits: LimitsAndPriority, outputdir: str, outputExt: str):
        # TODO: get local limits here maybe. And if they exists apply them here. If not use global
        
        # Start 
        self.updateVideoItemUIDownloadState(item, DownloadProgress.IN_PROGRESS)
        try:
            item.process_downloads_combine_keep(limits, outputdir, outputExt)                
            item.download_status = DownloadProgress.DONE
            item.log("Download and Combine is complete!")
        except Exception as e:
            item.download_status = DownloadProgress.ERROR
            item.log(f"File not finished. Error: {e}")
            print(f"File not finished. Error: {e}")
            temp_path = item.make_tmp_dir(outputdir)
            shutil.rmtree(temp_path)
        #end
        # Finish
        self.updateVideoItemUIDownloadState(item)
    #end

    ## Process the download entries method
    def downloadAllVideoItems(self, process_via_multithreading: bool, limits: LimitsAndPriority, outputDir: str, outputExt: str):
        # Create a list to hold thread objects
        download_threads = []
        # Get lengths
        n = 0; N = len(self.infoList);
        # Loop over all entries in the tree view
        # for info in self.infoList:
        for n in range(N):

            self.infoList[n].log(f"Process Entry Download {n+1} of {N}: ");

            # Run in Single thread or multithread mode
            if process_via_multithreading:
                t = threading.Thread(target=self.video_item_process_download, args=(self.infoList[n], limits, outputDir, outputExt))
                t.start()
                download_threads.append(t)            
            else:
                self.video_item_process_download(self.infoList[n], limits, outputDir, outputExt)
            #end
        #end

        if process_via_multithreading:
            # Wait for all threads to complete
            for t in download_threads:
                t.join()
            #end
        #end

    def update_download_progress(self):
        # Global GUI update while downloading
        N = len(self.getVideoList())
        count_done          = sum(1 for video_info in self.getVideoList() if video_info.download_status == DownloadProgress.DONE)
        count_in_progress   = sum(1 for video_info in self.getVideoList() if video_info.download_status == DownloadProgress.IN_PROGRESS)# TODO: this could be implemented different, so that percentage is included, basically this has to be ignored and calculated as total - the other 2
        count_error         = sum(1 for video_info in self.getVideoList() if video_info.download_status == DownloadProgress.ERROR)
        self.update_progressbar(count_done+count_error,N,0)
        self.setUiDispStatus(f"Processing {N} item(s): Completed downloads {count_done} of {N}      Still in progress = {count_in_progress}, Errors = {count_error}!")
    #end

    ## -------------------------- Abstract/Template UI functions -----------------------------
    # These functions are provisioned to be overwritten by the child classes for UI updates.
    # They are not compulsory to implement. They are not necessary for this class but serve as insertion points for the child classes.

    # NOTE: This is the value compute part of the function. 
    # The display part needs to be implemented by overwriting this function 
    # and first calling (this) the parent function.
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        global index, total
        if total_in == 0:
            return 0;# Default value
        #end
        if task_level == 0:
            index = index_in
            total = total_in
            # Update the progress bar for the main task
            progressValue = (index / total) * 100
        else:
            progressValue = 100 * ( index +  (index_in/total_in) )/ total 
        #end
        return progressValue
    #end

    def getUiDispStatus(self):
        # Interface provision 
        return ""

    def setUiDispStatus(self, msg: str = ""):
        # Interface provision 
        pass

    # TODO: this function could be renamed and somewhat reimplemented. 
    def updateVideoItemUIDownloadState(self, videoItem, download_status=None):
        # Interface provision but by default: 
        # Also update the global download progress
        self.update_download_progress()
        pass