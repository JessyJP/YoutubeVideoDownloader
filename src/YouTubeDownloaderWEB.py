"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Date: April 7, 2023
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

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

# This starter file name: YouTubeDownloaderWEB.py
from web.webapp import create_web_app, getEnvironmentalParameters

from dotenv import load_dotenv
import os

# Load the .env file from a specific path
env_file_path = os.path.join(os.path.dirname(__file__), "../webapp.env")
load_dotenv(env_file_path)
# Print message indicating the path of the .env file
print(f"The environmental parameters were loaded from: {env_file_path}")

# TODO: note the arrangement the way the parameters are passed with defaults etc. could be simplified
envParam = getEnvironmentalParameters()
app = create_web_app(port=envParam.port,
                        output_dir=envParam.output_dir,
                        use_multithreading_analysis=envParam.use_multithreading_analysis,
                        process_via_multithreading=envParam.process_via_multithreading)

if __name__ == '__main__':
    pass
#end