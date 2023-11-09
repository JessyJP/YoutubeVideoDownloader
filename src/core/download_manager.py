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
from typing import Union
from core.pytube_handler import VideoInfo
from core.youtube_dl_handler import VideoInfo_alternative
import shutil


# -------- Get the video info from the URL --------
def get_url_info_entry(url: str, use_alternative=False) -> Union[VideoInfo, VideoInfo_alternative, None]:
    try:
        video_info = VideoInfo(url=url)
        return video_info
    except Exception as e:
        print(f"An error occurred while fetching the video information using VideoInfo for {url}: {e}")
        if use_alternative:
            try:
                video_info_alt = VideoInfo_alternative(url)
                return video_info_alt
            except Exception as e_alt:
                print(f"An error occurred while fetching the video information using VideoInfo_alternative for {url}: {e_alt}")
            #end
        #end
        return None
    #end
#end

class DownloadManager():
    def __init__(self):        
        # Video Info list
        self.infoList = [];

    def getTBL(self):
        return self.infoList;

    def getRow(self,rowIndex):
        return self.infoList[rowIndex]
    
    def getRowIndex(self, video_info):
        index = self.infoList.index(video_info)
        return index
    
    def removeRow(self, video_info):        
        if video_info is not None:
            # Remove the VideoInfo object from the infoList
            index_to_remove = self.infoList.index(video_info)
            self.infoList.pop(index_to_remove)

    # This method is used to locate a video info from a list
    def get_video_info_by_index_or_video_id(self, video_id: str, index: int = -1) -> Union[VideoInfo, None]:
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

    def getRowProp(index,property):
        pass

    def setRowProp(index,property):
        pass


    ## Process methods
    def download_all_entries(self, process_via_multithreading, limits, outputDir, outputExt):
        # Create a list to hold thread objects
        download_threads = []
        # Get lengths
        n = 0; N = len(self.infoList);
        # Loop over all entries in the tree view
        # for info in self.infoList:
        for n in range(N):

            def download_by_info(n, limits, outputdir, outputExt):
                # Define variables
                N = len(self.infoList)
                self.infoList[n].log(f"Process Entry Download {n+1} of {N}: ");
                _DONE_ = "Done!"
                _ERROR_ = "Error!"
                _IN_PROGRESS_ = "Downloading Now..."

                # Get the associated item
                item = self.get_tree_view_item_by_video_info(self.infoList[n])
                # initial_download_keep_str = self.tree.set(item, 'download_status')
                def setItemStatus(item,new_status=None):
                    self.tree.set(item, 'download_status', new_status)
                #end
                
                # TODO: get local limits here maybe. And if they exists apply them here. If not use global

                # Start 
                setItemStatus(item,_IN_PROGRESS_)
                try:
                    self.infoList[n].process_downloads_combine_keep(limits, outputdir, outputExt)                
                    self.infoList[n].download_status = _DONE_
                except Exception as e:
                    print(f"File not finished. Error: {e}")
                    self.infoList[n].download_status = _ERROR_
                    temp_path = self.infoList[n].make_tmp_dir(outputdir)
                    shutil.rmtree(temp_path)
                #end

                # Global Update GUI
                setItemStatus(item, self.infoList[n].download_status)
                count_done          = sum(1 for video_info in self.infoList if video_info.download_status == _DONE_)
                count_in_progress   = sum(1 for video_info in self.infoList if video_info.download_status == _IN_PROGRESS_)
                count_error         = sum(1 for video_info in self.infoList if video_info.download_status == _ERROR_)
                self.update_progress(count_done+count_error,N,0)
                self.dispStatus(f"Processing {N} item(s): Completed downloads {count_done} of {N}      Still in progress = {count_in_progress}, Errors = {count_error}!")
            #end

            # Run in Single thread or multithread mode
            if process_via_multithreading:
                t = threading.Thread(target=download_by_info, args=(n, limits, outputDir, outputExt))
                t.start()
                download_threads.append(t)            
            else:
                download_by_info(n, limits, outputDir, outputExt)
            #end
        #end

        if process_via_multithreading:
            # Wait for all threads to complete
            for t in download_threads:
                t.join()
            #end
        #end