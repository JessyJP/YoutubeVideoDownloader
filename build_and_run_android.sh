#!/bin/bash

# Define the source and destination directories
SEPARARATOR="----------------------------------------------------"
SRC_DIR="src"
DEST_DIR="build_android" # Replace with your actual destination directory
APK_NAME="yddapp"

RSYNC_OPTS="-av --exclude='*.pyc' --exclude='__pycache__/'"

echo "Current user [$USER]."

## ===============================================================
# Your build and run commands go here
echo $SEPARARATOR
echo "Remove previous directory [$DEST_DIR] if it exists."
echo $SEPARARATOR
# rm -vr $DEST_DIR


echo $SEPARARATOR
echo "Create the anroid build subset."
echo $SEPARARATOR
# Create destination directory if it doesn't exist
mkdir -p "$DEST_DIR"

# Use rsync to copy specific directories and exclude .pyc files
rsync -av --exclude='*.pyc' --exclude='__pycache__/' "$SRC_DIR/core" "$DEST_DIR/"
rsync -av --exclude='*.pyc' --exclude='__pycache__/' "$SRC_DIR/mobile_kivy_gui" "$DEST_DIR/"
rsync -av --exclude='*.pyc' --exclude='__pycache__/' "themes" "$DEST_DIR/"
rsync -av --exclude='*.pyc' --exclude='__pycache__/' "images" "$DEST_DIR/"
rsync -av --exclude='*.pyc' --exclude='__pycache__/' "data" "$DEST_DIR/"

# Copy the main file. Rename the file to main because buldozer expects that as a starting point
cp -v "$SRC_DIR/YouTubeDownloaderKIVY.py"     "$DEST_DIR/main.py"
# Copy specific files
cp -v "buildozer.spec" "$DEST_DIR/" #
cp -v "config.ini"     "$DEST_DIR/"

# Add any other specific files or directories you need to copy here

## ===============================================================
# Your build and run commands go here
echo $SEPARARATOR
echo "Apply the local python virtual environment"
source .venv/bin/activate

echo "Change working directory to [$DEST_DIR]."
cd $DEST_DIR
echo "Current working directory [${PWD}]."

chown -R jp:jp ${PWD}
echo "Change ownership of [${PWD}]."

# Your build and run commands go here
echo "Build and run via buildozer."
echo $SEPARARATOR
# buildozer -v android debug
# buildozer -v android debug deploy run logcat > log
# buildozer -v android debug deploy run logcat | grep "python"
# adb install $APK_NAME.apk

# View python only logs
# cat log | grep "python" > plog; kwrite plog

echo $SEPARARATOR
echo "Build and run script done."
echo $SEPARARATOR
