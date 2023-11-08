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

# Imports
import os
import sys
import platform
import subprocess

## ================================= Definitions =================================


## ================================= Runtime Flags =================================

os_name = platform.system()
os_arch = platform.architecture()[0]

isDeployed = getattr(sys, "frozen", False)


## ================================= Logging =================================
import logging
logger = logging.getLogger(__name__)


## ================================= Module management functions =================================
# Ensure all required modules are installed.
def install_missing_modules(modules):
    if isDeployed:# This ensures that this functions is not called once an executable is made
        return
    #end
    try:
        import pkg_resources
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools"])
        import pkg_resources
    #end

    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_modules = [module for module in modules if module not in installed_packages]

    if missing_modules:
        for module in missing_modules:
            print(f"Installing missing module: {module}")# TODO: maybe a logger should be used here instead of a print statement
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
        #end
    #end
#end