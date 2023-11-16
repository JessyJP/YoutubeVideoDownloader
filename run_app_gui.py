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
import os, sys
from src.core.common import add_module_paths

# Determine the root of your project (one level up from this script)
project_root = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.join(project_root, "src")

# Add to the system path
# sys.path.insert(0, project_root)
# print(f"Added project root {project_root} to sys.path")
add_module_paths(source_dir)

# Change the working directory to the 'src' directory

from src.YouTubeDownloader import main  

if __name__ == '__main__':
    sys.argv = [__file__, '--gui']
    main()

# NOTE: if running this script returns an error, just run "YouTubeDownloader.py" directly