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
## Imports
import os
os.system("title Don't mind the LOG window")
# import gui.splashscreen
from core.common import isDeployed, os_name
from gui.main_window import main_runGUI
from YouTubeDownloader import hide_console


## Main function and also a command line parsing tool
def main():
    print("======== YouTube video downloader GUI by JessyJP ========")

    # The gui mode is called
    if isDeployed and os_name == 'Windows':
        # hide_console()
        pass
    #end    
    
    # GUI main function
    main_runGUI()
#end


# This block ensures the main function runs only when 
# the script is executed directly, not when imported
if __name__ == "__main__":
    main()
#end