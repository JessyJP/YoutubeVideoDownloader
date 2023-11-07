import threading
import atexit
from flask import Flask, render_template, request, jsonify
from gui_main import YouTubeDownloaderGUI

app = Flask(__name__)
gui = YouTubeDownloaderGUI() 
thread = None

def call_main_loop():
    global gui
    try:
        gui.mainloop()
    except:
        pass

def start_gui():
    global thread
    if thread is None:
        # Notice the comma after gui, which makes args a tuple with one element.
        thread = threading.Thread(target=call_main_loop)
        thread.start()

def stop_gui():
    # Add any necessary cleanup logic here
    # If the GUI has a method to shut it down gracefully, call it here
    # e.g., gui.shutdown()
    if thread and thread.is_alive():
        thread.join()  # This will wait for the thread to complete



# @app.before_request
# def initialize():
#     start_gui()

# @atexit.register
# def cleanup():
#     stop_gui()

@app.route('/')
def index():
    return render_template('index.html', infoList=gui.infoList)

@app.route('/api/analyze_video', methods=['POST'])
def analyze_video():
    data = request.json
    url = data['url']

    # Extract the data using the gui object. Assuming the YouTubeDownloaderGUI class has methods to do this
    video_info = gui.analyze_video(url)
    
    return jsonify(video_info)

@app.route('/api/audio_bitrate_list', methods=['GET'])
def audio_bitrate_list():
    # Again, we're assuming the YouTubeDownloaderGUI class has a method to get this list
    bitrate_list = gui.get_audio_bitrate_list()
    
    return jsonify(bitrate_list)

@app.route('/api/video_resolution_list', methods=['GET'])
def video_resolution_list():
    resolution_list = gui.get_video_resolution_list()
    
    return jsonify(resolution_list)

@app.route('/api/fps_value_list', methods=['GET'])
def fps_value_list():
    fps_list = gui.get_fps_value_list()
    
    return jsonify(fps_list)

@app.route('/api/download_video', methods=['POST'])
def download_video():
    data = request.json
    download_path = gui.download_video(data)
    
    return jsonify({"download_path": download_path})

@app.route('/api/play_video_preview', methods=['POST'])
def play_video_preview():
    data = request.json
    video_path = data['video_path']
    
    # Assuming a play_video method exists in the gui object
    gui.play_video(video_path)

    return jsonify({"message": "Video is playing"})

@app.route('/api/select_download_location', methods=['POST'])
def select_download_location():
    # This might involve server-side handling of file system interactions. 
    # For now, we'll just return a static path as an example.
    return jsonify({"download_location": "/path/to/download/folder"})

if __name__ == '__main__':
    start_gui()
    app.run(debug=True)
    stop_gui()