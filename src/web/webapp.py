"""
File: webapp.py

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
# Module imports
from flask import Flask
from web.server_mgr import vlm
from web.routes import router


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

    # Flask application setup
    app = Flask(__name__)
    app.secret_key = 'my_session_secret_key'  # Set a secret key for session management
    app.register_blueprint(router)

    app.run(debug=True, port=port)

if __name__ == '__main__':
    main()
#end