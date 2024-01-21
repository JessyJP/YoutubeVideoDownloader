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
GUI_SCRIPT_PATH = "./src/YouTubeDownloaderGUI.py"
ICON_PATH = "./images/window_icon.ico"
SPLASH_PATH = "./images/IconProjects/pngaaa.com-4933843.png"
OUTPUT_EXE_NAME = "YouTubeDownloader" + (".exe" if IS_WINDOWS else "")
OUTPUT_GUI_EXE_NAME = "YouTubeDownloaderGUI" + (".exe" if IS_WINDOWS else "")
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

    if os.path.exists(OUTPUT_GUI_EXE_NAME):
        os.remove(OUTPUT_GUI_EXE_NAME)
        print(f"{OUTPUT_GUI_EXE_NAME} file removed.")

    # ============ Step 2: ============
    print("="*73)
    print("Preparing to package the Python script as a standalone executable file...")
    print("="*73)
    
    # Create the executable
    cmd = f'python -m PyInstaller "{MAIN_SCRIPT_PATH}" --onefile --icon "{ICON_PATH}"'
    _separator_ = ";" if IS_WINDOWS else ":"
    cmd += f" --add-data src/web/templates{_separator_}templates --add-data src/web/static{_separator_}static"
    # cmd += ' --noconsole'
    # cmd += ' --splash "./images/IconProjects/pngaaa.com-4933843.png"'
    run_command(cmd)
    
    # Create GUI only executable 
    cmd = f'python -m PyInstaller "{GUI_SCRIPT_PATH}" --onefile --icon "{ICON_PATH}"'
    cmd += ' --noconsole'
    # cmd += ' --splash "./images/IconProjects/pngaaa.com-4933843.png"'
    run_command(cmd)

    # ============ Step 3: ============
    print("="*73)
    print("Moving the executable file from the 'dist' directory to the current directory...")
    shutil.move(os.path.join(DIST_DIR, OUTPUT_EXE_NAME), ".")
    shutil.move(os.path.join(DIST_DIR, OUTPUT_GUI_EXE_NAME), ".")
    print("Done")

    # ============ Step 4: ============
    clean_build_files()

    # ============ Step 5: ============
    print("="*73)
    print(f"Creating a {ZIP_NAME} containing the executable file and other resources...")
    create_zip(ZIP_NAME, [OUTPUT_EXE_NAME, OUTPUT_GUI_EXE_NAME] + RESOURCES)
    print("Done")

    print("="*73)
    print("Packing Completed.")

if __name__ == "__main__":
    main()
