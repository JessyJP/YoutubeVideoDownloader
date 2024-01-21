"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

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