@echo off
cls

echo ==========================================================================
echo Preparing to package the Python script as a standalone executable file...
echo ==========================================================================
pyinstaller "./src/YouTubeDownloader.py" --onefile ^
			--icon "./images/window_icon.ico" 
			::^
			REM --noconsole
			:: --splash "./images/IconProjects/pngaaa.com-4933843.png"

echo ==========================================================================
echo Moving the executable file from the "dist" directory to the current directory...
move ".\dist\YouTubeDownloader.exe" ".\"
echo Done

echo ==========================================================================
echo Removing the "dist" directory...
rmdir /S /Q dist
echo Done

echo ==========================================================================
echo Removing the "build" directory...
rmdir /S /Q build
echo Done

echo Removing the .spec file...
del /Q /F YouTubeDownloader.spec

echo ==========================================================================
echo Creating a zip file containing the executable file and other resources...
powershell -Command "Compress-Archive -Force -Path 'YouTubeDownloader.exe', 'images/', 'themes/', 'config.ini' -DestinationPath 'YouTubeDownloader.zip'"
echo Done

echo ==========================================================================
echo Packing Completed.
