# Module imports
from flask import Flask, render_template, request, jsonify, session
from web.server_mgr import vlm, ProcessRoutine, video_info_to_dict

#==============================================================================
## ---------- Router api calls ----------
from flask import Blueprint # , render_template
# Create a Blueprint for your routes
router = Blueprint('router', __name__)

@router.route('/')
def index():
    return render_template('index.html', title="YouTubeDownloader",
                            **vlm.getLimitsDropdownValuesAndLastSelection())
#end

@router.route('/api/getState', methods=['GET'])
def getState():
    return vlm.processState.value  # Assuming this is a string

@router.route('/api/getStatusMsg', methods=['GET'])
def getStatusMsg():
    return vlm.statusMsg  # Assuming this is a string

@router.route('/api/getProgressbarValue', methods=['GET'])
def getProgressbarValue():
    # Assuming you want to keep two decimal places
    return format(vlm.statusProgressValue, '.2f')


@router.route('/api/getVideoItemList', methods=['GET'])
def getVideoItemList():
    jsonList = []
    for item in vlm.getVideoList():
        jsonList.append(video_info_to_dict(item))
    #end
    return jsonify(jsonList)
#end

@router.route('/api/analyzeURLtext', methods=['POST'])
def analyzeURLtext():
    # vlm = WebServerVideoManager()
    data = request.json
    url_text_data = data['url']
    vlm.analyse_button_callback(url_text_data)

    # Return a response indicating that the analysis process has started
    return jsonify({"message": "Analysis process started"}), 202
#end

@router.route('/api/downloadVideoList', methods=['POST'])
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

@router.route('/api/changeStatusForItemsSelectedByID', methods=['POST'])
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


# @router.route('/api/play_video_preview', methods=['POST'])
# def play_video_preview():
#     data = request.json
#     video_path = data['video_path']
    
#     # Assuming a play_video method exists in the vlm object
#     vlm.play_video(video_path)

#     return jsonify({"message": "Video is playing"})


@router.route('/api/update_client_state', methods=['GET'])
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


@router.route('/api/update_client_state', methods=['POST'])
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

#==============================================================================

# Flask application setup
app = Flask(__name__)
app.secret_key = 'my_session_secret_key'  # Set a secret key for session management
app.register_blueprint(router)

#==============================================================================

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