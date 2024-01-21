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
# Module imports
import os
from types import SimpleNamespace
from flask import Flask, render_template, request, jsonify, send_file, session
from web.server_mgr import vlm, ProcessRoutine, video_info_to_dict
from core.download_options import * # updateOutputKeepsStr, MediaSymbols # NOTE:imports the symbol list as well

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
            vlm.change_download_status(video_ids, COMBINED_SYMBOL,"on")
        elif instruction == "skip":
            # Logic for skip status
            vlm.change_download_status(video_ids, COMBINED_SYMBOL,"off")
        elif instruction == "audio":
            # Logic for toggling audio
            vlm.change_download_status(video_ids, AUDIO_ONLY_SYMBOL)
        elif instruction == "video":
            # Logic for toggling video
            vlm.change_download_status(video_ids, VIDEO_ONLY_SYMBOL)
        elif instruction == "subtitles":
            # Logic for toggling subtitles
            vlm.change_download_status(video_ids, SUBTITLES_ONLY_SYMBOL)
        elif instruction == "thumbnail":
            # Logic for toggling thumbnail
            vlm.change_download_status(video_ids, THUMBNAIL_SYMBOL)
        elif instruction == "info":
            # Logic for toggling info
            vlm.change_download_status(video_ids, INFO_SYMBOL)
        elif instruction == "comments":
            # Logic for toggling comments
            vlm.change_download_status(video_ids, COMMENTS_SYMBOL)
        elif instruction == "clear":
            # Logic for clearing all keeps
            vlm.change_download_status_clearall(video_ids)
        else:
            # Handle unrecognized instruction
            return jsonify({"error": "Unrecognized instruction"}), 400
        #end

        return jsonify({"message": f"Instruction '{instruction}' applied successfully", "affectedItems": video_ids}), 200
    else:
        return jsonify({"message": f"Processing [{vlm.processState}] is currently running!"}), 200
    #end
#end

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
    uiSettings = data.get('uiSettings', {})
    
    vlm.lastLimits.bitrate    = uiSettings.get('audioBitrate')
    vlm.lastLimits.resolution = uiSettings.get('videoResolution')
    vlm.lastLimits.fps        = uiSettings.get('fpsValue')

    # Extract and store the UI settings and column visibility in clientState
    columnVisibility = data.get('columnVisibility', {})

    vlm.clientState['theme'] = uiSettings.get('currentTheme')
    vlm.clientState['viewMode'] = uiSettings.get('viewMode')
    vlm.clientState['columnVisibility'] = columnVisibility

    # Return a success response
    return jsonify({"message": "Server: Client state settings updated successfully"}), 200

@router.route('/api/getFileList', methods=['GET'])
def getFileList():
    if vlm.processState == ProcessRoutine.IDLE:
        # data = request.json
        # video_ids = data.get('videoIds', [])
        # TODO: we could do a selection save but that is not needed now

        symbol_dic = MediaSymbols.get_media_symbols_as_dict()
        videoItemList = vlm.getVideoList()
        listOfOutputs = []
        # Loop over the items
        for item in videoItemList:
            # Iterate over the output types
            for label in symbol_dic:
                symbol = symbol_dic[label]
                # Check if the value is not None
                if item.outputFilepaths[symbol] is not None:
                    # Add the string to the list
                    listOfOutputs.append({
                        "index": len(listOfOutputs),
                        "video_title" : item.title,
                        "video_id" : item.video_id,
                        "label": label,
                        "symbol_key": symbol,
                        "save_output_filename": os.path.basename(item.outputFilepaths[symbol])
                    })
                #end
            #end
        #end
        return jsonify(listOfOutputs), 200
    else:
        return jsonify({"message": f"Processing [{vlm.processState}] is currently running!"}), 200
    #end
#end

@router.route('/api/transferFile', methods=['GET'])
def transferFile():
    if vlm.processState == ProcessRoutine.IDLE:
        video_id = request.args.get('video_id')
        symbol_key = request.args.get('symbol_key')

        item = vlm.getItemByIndexOrVideoID(video_id)
        file_path = item.outputFilepaths[symbol_key]

        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"message": f"Processing [{vlm.processState}] is currently running!"}), 200
    #end
#end

#==============================================================================

# @router.route('/api/play_video_preview', methods=['POST'])
# def play_video_preview():
#     data = request.json
#     video_path = data['video_path']
    
#     # Assuming a play_video method exists in the vlm object
#     vlm.play_video(video_path)

#     return jsonify({"message": "Video is playing"})
