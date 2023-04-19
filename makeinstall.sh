#!/bin/bash
echo "=========================================================================="
echo "Preparing to package the Python script as a standalone executable file..."
echo "=========================================================================="
pyinstaller "./src/YouTubeDownloader.py" --onefile --icon "./images/window_icon.ico"
# --noconsole
# --splash "./images/IconProjects/pngaaa.com-4933843.png"

echo "=========================================================================="
echo "Moving the executable file from the 'dist' directory to the current directory..."
mv "./dist/YouTubeDownloader" "./"
echo "Done"

echo "=========================================================================="
echo "Removing the 'dist' directory..."
rm -r dist
echo "Done"

echo "=========================================================================="
echo "Removing the 'build' directory..."
rm -r build
echo "Done"

echo "Removing the .spec file..."
rm YouTubeDownloader.spec

echo "=========================================================================="
echo "Creating a tar.gz file containing the executable file and other resources..."
tar -czvf YouTubeDownloader.tar.gz YouTubeDownloader images/ themes/ config.ini
echo "Done"

echo "=========================================================================="
echo "Packing Completed."
