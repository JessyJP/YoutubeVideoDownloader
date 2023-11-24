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
        self.tmpOutputDir = default_tmp_dir # TODO: maybe it shouldn't be assigned but the construction should happen in main
        self.outputExt = ".mkv"

        # Frontend client settings state
        self.clientState = dict()
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

    def setDownloadDir(self, download_dir):
            # Normalize the path to avoid issues with different OS path formats
            normalized_path = os.path.normpath(download_dir)

            # Check if the path exists
            if not os.path.exists(normalized_path):
                raise FileNotFoundError(f"The specified path does not exist: {normalized_path}")

            # Set the download directory
            self.tmpOutputDir = normalized_path

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def getUiDispStatus(self) -> str:
        # Interface provision 
        return self.statusMsg
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def setUiDispStatus(self, msg: str = ""):
        # In the GUI this was used to update the status bar at the bottom,
        # but here it can serve a more comprehensive purpose to update the client.
        self.statusMsg = msg
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        # Call the parent to compute the progress value
        self.statusProgressValue = super().update_progressbar(index_in, total_in, task_level)
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

@app.route('/api/getProgressbarValue', methods=['GET'])
def getProgressbarValue():
    # Assuming you want to keep two decimal places
    return format(vlm.statusProgressValue, '.2f')


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
    return jsonify({"download": "download_path"}) , 202

@app.route('/api/changeStatusForItemsSelectedByID', methods=['POST'])
def changeStatusForItemsSelectedByID():
    if vlm.processState == ProcessRoutine.IDLE:
        data = request.json
        instruction = data.get('instruction')
        video_ids = data.get('videoIds', [])

        # Define the logic for each instruction
        if instruction == "remove":
            # Logic to remove items from the list           
             for id in video_ids:
                item = vlm.getItemByIndexOrVideoID(id)
                if item:
                    vlm.removeItem(item)
                else:
                    print(f"Item with ID {id} not found.")
                    # Handle the case where the item is not found
                    
        elif instruction == "pending":
            # Logic for pending status
            pass
        elif instruction == "skip":
            # Logic for skip status
            pass
        elif instruction == "audio":
            # Logic for toggling audio
            pass
        elif instruction == "video":
            # Logic for toggling video
            pass
        elif instruction == "subtitles":
            # Logic for toggling subtitles
            pass
        elif instruction == "thumbnail":
            # Logic for toggling thumbnail
            pass
        elif instruction == "info":
            # Logic for toggling info
            pass
        elif instruction == "comments":
            # Logic for toggling comments
            pass
        elif instruction == "clear":
            # Logic for clearing all keeps
            pass
        else:
            # Handle unrecognized instruction
            return jsonify({"error": "Unrecognized instruction"}), 400
        #end

        return jsonify({"message": f"Instruction '{instruction}' applied successfully", "affectedItems": video_ids}), 200
    else:
        return jsonify({"message": f"Processing [{vlm.processState}] is currently running!"}), 200
    #end
#end


# @app.route('/api/play_video_preview', methods=['POST'])
# def play_video_preview():
#     data = request.json
#     video_path = data['video_path']
    
#     # Assuming a play_video method exists in the vlm object
#     vlm.play_video(video_path)

#     return jsonify({"message": "Video is playing"})


@app.route('/api/update_client_state', methods=['GET'])
def get_update_client_state():
    # Construct the state to be sent
    state = {
        'uiSettings': {
            # The limiters are handled from the class state
            'audioBitrate': vlm.lastLimits.bitrate,
            'videoResolution': vlm.lastLimits.resolution,
            'fpsValue': vlm.lastLimits.fps,
            # The rest are stored in a dictionary
            'currentTheme': vlm.clientState.get('theme'),
            'viewMode': vlm.clientState.get('viewMode')
        },
        'columnVisibility': vlm.clientState.get('columnVisibility', {})
    }

    # Return the state as a JSON response
    return jsonify(state)


@app.route('/api/update_client_state', methods=['POST'])
def post_update_client_state():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # print(f"Received client state settings: {data}")

    # Extract and store the basic download limit settings
    vlm.lastLimits.bitrate    = data.get('audioBitrate')
    vlm.lastLimits.resolution = data.get('videoResolution')
    vlm.lastLimits.fps        = data.get('fpsValue')

    # Extract and store the UI settings and column visibility in clientState
    uiSettings = data.get('uiSettings', {})
    columnVisibility = data.get('columnVisibility', {})

    vlm.clientState['theme'] = uiSettings.get('currentTheme')
    vlm.clientState['viewMode'] = uiSettings.get('viewMode')
    vlm.clientState['columnVisibility'] = columnVisibility

    # Return a success response
    return jsonify({"message": "Server: Client state settings updated successfully"}), 200


def main(port:int=80, output_dir:str='',
         use_multithreading_analysis:bool = False,
         process_via_multithreading:bool = False ):

    vlm.use_multithreading_analysis = use_multithreading_analysis
    vlm.process_via_multithreading = process_via_multithreading  
    vlm.setDownloadDir(output_dir)

    prefix = " -- Param: "
    print(f"{prefix}Use multithreading analysis set to: [{use_multithreading_analysis}]")
    print(f"{prefix}Use process download and mux via multithreading set to: [{process_via_multithreading}]")
    print(f"{prefix}Port set to: [{port}]")
    print(f"{prefix}Output directory set to [{output_dir}]")

    app.run(debug=True, port=port)

if __name__ == '__main__':
    main()
#end