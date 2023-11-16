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
import shutil
import subprocess
import platform
import zipfile

# ===================== Definitions Section =====================
PLATFORM = platform.system()
IS_WINDOWS = PLATFORM == "Windows"
IS_LINUX_OR_MAC = PLATFORM in ["Linux", "Darwin"]

# Specify all the directories, filenames, and other constants here
MAIN_SCRIPT_PATH = "./src/YouTubeDownloader.py"
ICON_PATH = "./images/window_icon.ico"
SPLASH_PATH = "./images/IconProjects/pngaaa.com-4933843.png"
OUTPUT_EXE_NAME = "YouTubeDownloader" + (".exe" if IS_WINDOWS else "")
SPEC_NAME = "YouTubeDownloader.spec"
ZIP_NAME = "YouTubeDownloader.zip"
DIST_DIR = "dist"
BUILD_DIR = "build"
RESOURCES = ['images/', 'themes/', 'config.ini']
# ===============================================================

def run_command(cmd):
    """Helper function to run a shell command and display its output."""
    process = subprocess.Popen(cmd, shell=True)
    process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {cmd}.")

def clean_build_files():
    """Remove the build artifacts: 'dist' and 'build' directories and .spec file."""
    print("="*73)
    
    shutil.rmtree(DIST_DIR, ignore_errors=True)
    print(f'Dist directory [{DIST_DIR}] removed.')
    
    shutil.rmtree(BUILD_DIR, ignore_errors=True)
    print(f'Build directory [{BUILD_DIR}] removed.')

    if os.path.exists(SPEC_NAME):
        os.remove(SPEC_NAME)
        print(f'.spec [{SPEC_NAME}] file removed.')    
        
    if os.path.exists(ZIP_NAME):
        os.remove(ZIP_NAME)
        print(f'Zip archive [{ZIP_NAME}] file removed.')  

def create_zip(archive_name, files):
    """Create a zip archive from the list of files and directories."""
    with zipfile.ZipFile(archive_name, 'w') as zipf:
        for file in files:
            if os.path.isdir(file):
                for foldername, subfolders, filenames in os.walk(file):
                    for filename in filenames:
                        zipf.write(os.path.join(foldername, filename), os.path.join(foldername, filename))
            else:
                zipf.write(file)

def main():
    # ============ Step 1: ============
    clean_build_files()
    if os.path.exists(OUTPUT_EXE_NAME):
        os.remove(OUTPUT_EXE_NAME)
        print(f"{OUTPUT_EXE_NAME} file removed.")

    # ============ Step 2: ============
    print("="*73)
    print("Preparing to package the Python script as a standalone executable file...")
    print("="*73)
    
    # Create the executable
    cmd = f'python -m PyInstaller "{MAIN_SCRIPT_PATH}" --onefile --icon "{ICON_PATH}"'
    cmd += ' --noconsole'
    # cmd += ' --splash "./images/IconProjects/pngaaa.com-4933843.png"'
    run_command(cmd)
    
    # ============ Step 3: ============
    print("="*73)
    print("Moving the executable file from the 'dist' directory to the current directory...")
    shutil.move(os.path.join(DIST_DIR, OUTPUT_EXE_NAME), ".")
    print("Done")

    # ============ Step 4: ============
    clean_build_files()

    # ============ Step 5: ============
    print("="*73)
    print(f"Creating a {ZIP_NAME} containing the executable file and other resources...")
    create_zip(ZIP_NAME, [OUTPUT_EXE_NAME] + RESOURCES)
    print("Done")

    print("="*73)
    print("Packing Completed.")

if __name__ == "__main__":
    main()
