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
import sys
import os
from flask import Flask
from flask_cors import CORS
from web.routes import router
from types import SimpleNamespace
from web.default_config import default


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
    debugON = False
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
