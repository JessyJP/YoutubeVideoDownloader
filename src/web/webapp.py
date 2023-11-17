# Module imports
import os
import sys
import threading
from typing import Dict, List, Union, Tuple
from enum import Enum
from flask import Flask, render_template, request, jsonify, session
import json
import datetime
import atexit


#==============================================================================

# Make and import paths for the custom core components
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
source_dir = os.path.join(project_root, "src")
sys.path.append(project_root)
from src.core.common import add_module_paths
add_module_paths(source_dir)

from src.core.common import audio_bitrate_list, video_resolution_list, fps_value_list
from src.core.video_list_manager import VideoListManager
from src.core.pytube_handler import LimitsAndPriority, VideoInfo

#==============================================================================
# Enum definition for backend current state
class ProcessRoutine(Enum):
    IDLE     = "IDLE"
    ANALYSIS = "ANALYSIS"
    DOWNLOAD = "DOWNLOAD"
#end

# Singleton decorator definitions
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
#end

#==============================================================================
# Wrapper for the manager
@singleton
class WebWrapper(VideoListManager):
    def __init__(self, default_tmp_dir):        
        super().__init__()
        # This status string is for updating the current process status
        self.statusMsg = "Ready!"
        self.statusProgressValue = 100
        # Let's define some variables
        self.processState = ProcessRoutine.IDLE
        # Parameters for Analysis
        self.use_multithreading_analysis = False
        # Parameters for Download
        self.process_via_multithreading = True  
        self.tmpOutputDir = default_tmp_dir 
        self.outputExt = ".mkv"

        # Frontend client settings state
        self.theme = "dark"
        self.localSaveDir = ""
        self.lastLimits = LimitsAndPriority()
        print("WebWrapper is initialized")
    #end

    # Intermediate method to run the import operation in a separate thread
    def analyse_button_callback(self, text):
        def analysis_thread(target_func, args):
            # Set state to ANALYSIS at the start
            self.processState = ProcessRoutine.ANALYSIS
            self.setUiDispStatus("Analysis started")

            # Run the analysis
            target_func(*args)

            # Set state back to IDLE and update status when done
            self.processState = ProcessRoutine.IDLE
            self.setUiDispStatus("Analysis completed")
        #end

        if self.processState is ProcessRoutine.IDLE:
            use_analysis_multithreading = self.use_multithreading_analysis
            t = threading.Thread(target=analysis_thread, 
                                 args=(self.import_valid_Youtube_videos_from_textOrURL_list, (text, use_analysis_multithreading)))
            t.start()
        #end
    #end

    # NOTE:Overwrite this function from the parent class interface
    def getUiDispStatus(self) -> str:
        # Interface provision 
        return self.statusMsg
    #end

    # NOTE:Overwrite this function from the parent class interface
    def setUiDispStatus(self, msg: str = ""):
        # In the GUI this was used to update the status bar at the bottom,
        # but here it can serve a more comprehensive purpose to update the client.
        self.statusMsg = msg
    #end

    # NOTE:Overwrite this function from the parent class interface
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        # Call the parent to compute the progress value
        self.statusProgressValue = super().update_progressbar(index_in, total_in, task_level)

    def getLimitsDropdownValuesAndLastSelection(self) -> Dict[str, Union[List[str], str]]:

        # # Retrieve or set default last selected values
        # self.lastLimits.bitrate = session.get('last_bitrate', audio_bitrate_list[0])
        # self.lastLimits.resolution = session.get('last_resolution', video_resolution_list[0])
        # self.lastLimits.fps = session.get('last_fps', fps_value_list[0])

        # Get the last selection
        self.lastLimits.bitrate = audio_bitrate_list[0] if  self.lastLimits.bitrate is None else self.lastLimits.bitrate
        self.lastLimits.resolution = video_resolution_list[0] if  self.lastLimits.resolution is None else self.lastLimits.resolution
        self.lastLimits.fps = fps_value_list[0] if  self.lastLimits.fps is None else self.lastLimits.fps

        # Package all render data into a single dictionary
        render_data = {
            'audio_bitrate_list':audio_bitrate_list,
            'video_resolution_list':video_resolution_list,
            'fps_value_list':fps_value_list,
            'last_bitrate':self.lastLimits.bitrate,
            'last_resolution':self.lastLimits.resolution,
            'last_fps':self.lastLimits.fps
        }

        return render_data
    #end

    def getLimitsAndPriorityFromUI(self):
        # TODO: this function should just be integrated or abstracted
        limits_and_priority = LimitsAndPriority()

        # Get the audio bitrate
        limits_and_priority.bitrate = self.lastLimits.bitrate.replace("kbps","").strip()
        # Parse audio format priority into a list
        audio_format_priority_str = "wav, mp3, aac, m4a"
        limits_and_priority.audio_format_priority = [format.strip() for format in audio_format_priority_str.split(",")]

        # Get video resolution 
        limits_and_priority.resolution = self.lastLimits.resolution.replace("p","").strip()
        # Get video fps
        limits_and_priority.fps = self.lastLimits.fps.replace("fps","").strip()
        # Parse video format priority into a list
        video_format_priority_str = "mp4, webm, flv, 3gp, m4a"
        limits_and_priority.video_format_priority = [format.strip() for format in video_format_priority_str.split(",")]
        # TODO here we can just implement the list directly but the input might come from a env variable hance why we parse strings
        limits_and_priority.to_numeric()
        return limits_and_priority
    #end
#end

#============================== Helper functions ==============================
# Function to convert VideoInfo data to JSON
def video_info_to_dict(vItem: VideoInfo) -> dict:
    video_info_tuple = vItem.as_tuple()
    
    video_info_dict = {
        "download_status": video_info_tuple[0],
        "watch_url": video_info_tuple[1],
        "title": video_info_tuple[2],
        "author": video_info_tuple[3],
        "length": video_info_tuple[4],
        "description": video_info_tuple[5],
        "publish_date": video_info_tuple[6],
        "views": video_info_tuple[7],
        "thumbnail_url": video_info_tuple[8],
        "rating": video_info_tuple[9],
        "video_id": video_info_tuple[10],
        "quality_str": video_info_tuple[11],
        "video_size_mb": video_info_tuple[12]
    }

    # Loop over all fields and ensure they can be converted to a string
    for key, value in video_info_dict.items():
        try:
            # Try converting to string, will work for most built-in types
            video_info_dict[key] = str(value)
        except Exception:
            # If there's an error, manually handle the conversion
            # Example for a datetime object, adjust as needed
            if isinstance(value, datetime):
                video_info_dict[key] = value.isoformat()
            else:
                # General fallback, adjust as needed for other types
                video_info_dict[key] = "Unsupported data type"
            #end
        #end
    #end

    return video_info_dict#json.dumps(video_info_dict, indent=4)
#end

#==============================================================================

# Flask application setup
vlm = WebWrapper("R:/")
app = Flask(__name__)
app.secret_key = 'my_session_secret_key'  # Set a secret key for session management

#==============================================================================
## ---------- Router api calls ----------

@app.route('/')
def index():
    return render_template('index.html', title="YouTubeDownloader",
                            **vlm.getLimitsDropdownValuesAndLastSelection())
#end

@app.route('/api/getState', methods=['GET'])
def getState():
    return vlm.processState.value  # Assuming this is a string

@app.route('/api/getStatusMsg', methods=['GET'])
def getStatusMsg():
    return vlm.statusMsg  # Assuming this is a string

@app.route('/api/getVideoItemList', methods=['GET'])
def getVideoItemList():
    jsonList = []
    for item in vlm.getVideoList():
        jsonList.append(video_info_to_dict(item))
    #end
    return jsonify(jsonList)
#end

@app.route('/api/analyzeURLtext', methods=['POST'])
def analyzeURLtext():
    # vlm = WebWrapper()
    data = request.json
    url_text_data = data['url']
    vlm.analyse_button_callback(url_text_data)

    # Return a response indicating that the analysis process has started
    return jsonify({"message": "Analysis process started"}), 202
#end

@app.route('/api/downloadVideoList', methods=['POST'])
def downloadVideoList():
    # Set state to ANALYSIS at the start
    vlm.processState = ProcessRoutine.DOWNLOAD
    # TODO: we could do a try-except here because we don't know what might happen and the flag might get stuck
    # TODO: Similar approach should probably be taken for the analysis. I could do when i am not feeling lazy. 
    # data = request.json
    numericLimits = vlm.getLimitsAndPriorityFromUI()
    
    vlm.downloadAllVideoItems(
                        process_via_multithreading=vlm.process_via_multithreading,
                        limits=numericLimits,
                        outputDir=vlm.tmpOutputDir,
                        outputExt=vlm.outputExt)
    
    vlm.processState = ProcessRoutine.IDLE
    return jsonify({"download": "download_path"})

@app.route('/api/clearItemSelectionByID', methods=['POST'])
def clearItemSelectionByID():
    data = request.json
    video_ids = data.get('videoIds', [])
    
    # Logic to clear items using the video IDs
    for id in video_ids:
        item = vlm.getItemByIndexOrVideoID(id)
        if item:
            vlm.removeItem(item)
        else:
            print(f"Item with ID {id} not found.")
            # Handle the case where the item is not found

    return jsonify({"message": "Items cleared successfully"})


# @app.route('/api/play_video_preview', methods=['POST'])
# def play_video_preview():
#     data = request.json
#     video_path = data['video_path']
    
#     # Assuming a play_video method exists in the vlm object
#     vlm.play_video(video_path)

#     return jsonify({"message": "Video is playing"})


@app.route('/api/update_client_state', methods=['GET'])
def update_client_state():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    print(f"Received client state settings: {data}")

    # Extract the data, Process and store the settings
    vlm.lastLimits.bitrate    = data.get('audioBitrate')
    vlm.lastLimits.resolution = data.get('videoResolution')
    vlm.lastLimits.fps        = data.get('fpsValue')
    vlm.theme                 = data.get('currentTheme')
    vlm.localSaveDir          = data.get('downloadLocation')

    # Return a success response
    return jsonify({"message": "Client state settings updated successfully"}), 200


def main():
    app.run(debug=True, port=80)

if __name__ == '__main__':
    main()
#end