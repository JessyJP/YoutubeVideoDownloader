"""
File: main.py

Application Name: Youtube Video Downloader
Description: This application allows users to download videos from YouTube by providing a valid URL.
The user can analyze the video properties and choose the desired quality before downloading the video.

Author: JessyJP
Email: your.email@example.com TODO: add later
Date: April 8, 2023

Copyright (C) 2023 Your Name. All rights reserved.

License:
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

import threading
from typing import List, Union
from core.download_options import DownloadProgress
from core.pytube_handler import LimitsAndPriority, VideoInfo
import shutil


class VideoListManager:
    def __init__(self):        
        # Video Info list
        self.infoList: List[VideoInfo] = []

    def getVideoList(self):
        return self.infoList;

    def getItem(self,rowIndex):
        return self.infoList[rowIndex]
    
    def getItemIndex(self, video_info):
        index = self.infoList.index(video_info)
        return index
    
    def removeItem(self, video_info):        
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

        # If the index is not valid or the video_id doesn't match, search exhaustively
        for video_info in self.infoList:
            if video_info.video_id == video_id:
                return video_info
            #end
        #end

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
            current_url_entries.add(item.url)
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

    ## Process methods
    def downloadAllVideoItems(self, process_via_multithreading, limits, outputDir, outputExt):
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

    ## -------------------------- Abstract/Template UI functions -----------------------------
    # These functions are provisioned to be overwritten by the child classes for UI updates.
    # They are not compulsory to implement.
    def updateVideoItemUIDownloadState(self, videoItem, download_status=None):
        pass

