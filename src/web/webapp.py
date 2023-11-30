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
import sys
import os
from flask import Flask
from flask_cors import CORS
from web.routes import router
from types import SimpleNamespace

# Default configuration directly as a SimpleNamespace
default = SimpleNamespace(
    PORT=8080,
    OUTDIR='./tmp',
    MT_ANALYSIS=False,
    MT_DOWNLOAD=False
)

def create_web_app(port: int = default.PORT, output_dir: str = default.OUTDIR,
         use_multithreading_analysis: bool = default.MT_ANALYSIS,
         process_via_multithreading: bool = default.MT_DOWNLOAD):
    """Create and configure an instance of the Flask application."""

    if ( (output_dir == default.OUTDIR) and (not os.path.exists(output_dir)) ):
        os.makedirs(output_dir)
        print(f"Created output directory because the default was used: {output_dir}")

    from web.server_mgr import vlm # TODO: this is not ideal, the reason it's called here is because it will initialize a singleton
    # NOTE: When and if a proper user management and sessions for multi-users is implemented this will be handled properly
      
    vlm.use_multithreading_analysis = use_multithreading_analysis
    vlm.process_via_multithreading = process_via_multithreading
    vlm.setDownloadDir(output_dir)

    prefix = " -- Param: "
    print(f"{prefix}Use multithreading analysis set to: [{use_multithreading_analysis}]")
    print(f"{prefix}Use process download and mux via multithreading set to: [{process_via_multithreading}]")
    print(f"{prefix}Port set to: [{port}]")
    print(f"{prefix}Output directory set to [{output_dir}]")

    # Determine if the app is "frozen" (i.e., compiled by PyInstaller)
    application_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    # If the app is run as a PyInstaller bundle, set the base path to sys._MEIPASS
    # Otherwise, set it to the normal location

    # Flask application setup with specified template and static folders
    app = Flask(__name__,
                template_folder=os.path.join(application_path, 'templates'),
                static_folder=os.path.join(application_path, 'static'))
    app.secret_key = 'my_session_secret_key'  # Set a secret key for session management
    app.register_blueprint(router)

    return app

def run_from_dispatcher(port,output_dir,use_multithreading_analysis,process_via_multithreading):
    app = create_web_app(port,output_dir,use_multithreading_analysis,process_via_multithreading)
    debugON = not getattr(sys, 'frozen', False)# If not frozen then the debug mode is on
    CORS(app)
    app.run(debug=debugON, host='0.0.0.0', port=port)

def getEnvironmentalParameters():
    """Retrieve configuration from environment variables and return as a SimpleNamespace."""
    env_params = SimpleNamespace(
        port=int(os.environ.get("PORT", default.PORT)),
        output_dir=os.environ.get("OUTPUT_DIR", default.OUTDIR),
        use_multithreading_analysis=os.environ.get("USE_MULTITHREADING_ANALYSIS", str(default.MT_ANALYSIS)) == "True",
        process_via_multithreading=os.environ.get("PROCESS_VIA_MULTITHREADING", str(default.MT_DOWNLOAD)) == "True"
    )

    # Diagnostic messages
    print(f"PORT: {'Environment variable used' if 'PORT' in os.environ else f'Default used: {env_params.port}'}")
    print(f"OUTPUT_DIR: {'Environment variable used' if 'OUTPUT_DIR' in os.environ else f'Default used: {env_params.output_dir}'}")
    print(f"USE_MULTITHREADING_ANALYSIS: {'Environment variable used' if 'USE_MULTITHREADING_ANALYSIS' in os.environ else f'Default used: {env_params.use_multithreading_analysis}'}")
    print(f"PROCESS_VIA_MULTITHREADING: {'Environment variable used' if 'PROCESS_VIA_MULTITHREADING' in os.environ else f'Default used: {env_params.process_via_multithreading}'}")

    return env_params
