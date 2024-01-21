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
## Imports
# import os
# os.system("title Don't mind the LOG window")
# import gui.splashscreen
# from core.common import isDeployed, os_name
from mobile_kivy_gui.kivy_main_window import main_runGUI
# from YouTubeDownloader import hide_console


## Main function and also a command line parsing tool
def main():
    print("======== YouTube video downloader GUI by JessyJP ========")

    # The gui mode is called
    # if isDeployed and os_name == 'Windows':
    #     hide_console()
    # #end    
    
    # GUI main function
    main_runGUI()
#end


# This block ensures the main function runs only when 
# the script is executed directly, not when imported
if __name__ == "__main__":
    main()
#end