<p align="center">
  <img src="images\IconProjects\pngaaa.com-4933843.png" alt="Logo" width="100" height="73">
  <h1 align="center">Youtube Downloader Deluxe</h1>
</p>

**Youtube Downloader Deluxe** is a powerful and feature-rich software that allows you to easily download your favorite YouTube videos. With its user-friendly interface and advanced capabilities, it stands out as one of the best YouTube downloaders available today.

![Screenshot](images/Preview.png)

## Features

- Intuitive and easy-to-use graphical interface
- Supports downloading videos in various formats (MP4, WebM, etc.) and outputs in matroska MKV
- Allows downloading as a separate file: audio streams (MP3, OGG, etc.), the video streams(MP4, WebM, etc.)
- Also Supports downloading  subtitles, thumbnails, comments, info and description metadata as separate files
- Preview a selection of videos before downloading via your local video player (feature supported by Global Potplayer - Daum  https://potplayer.daum.net/)
- Multithreaded video analysis and download procedures
- Compatible with YouTube watch links, playlists, YouTube channel URLs and extraction of sub-links from non-YouTube webpages.
- Integration with the Google API for additional functionality
- Progress tracking and cancellation options, ability to sort the YouTube video info(s) according to the information columns which can be hidden as well
- Shortcut key combinations available, and ability to copy the table meta data as pain text
- Global quality limiters and per-video download quality selection
- Regular updates and improvements
- Can work in Windowed GUI mode and non-gui mode from the command line
- Can integrate with external software for stream muxing and transcoding and editing

## Setup and Execution Guide

This guide walks you through the steps to set up and run the project. It is recommended to use a virtual environment for this setup to ensure that the dependencies of the project do not interfere with other Python projects or system-wide Python packages.

### Step 1: Creating a Virtual Environment

A virtual environment is an isolated Python environment that allows you to manage dependencies for different projects separately. To create a virtual environment, follow these steps or use a tool such as your IDE:

1. **Navigate to your project's root directory**:
   ```bash
   cd download/path/to/YoutubeVideoDownloader
   ```

2. **Create a Virtual Environment**:
   - For **Windows**, use:
     ```bash
     python -m venv .venv
     ```
   - For **macOS and Linux**, use:
     ```bash
     python3 -m venv .venv
     ```

3. **Activate the Virtual Environment**:
   - On **Windows**, run:
     ```bash
     .\.venv\Scripts\activate
     ```
   - On **macOS and Linux**, run:
     ```bash
     source .venv/bin/activate
     ```
   You will know that the virtual environment is activated as the name of the virtual environment (.venv) will appear on your terminal prompt.

### Step 2: Installing Dependencies
With the virtual environment activated, install all the required dependencies listed in `versioned_requirements.txt`:

```bash
pip install -r versioned_requirements.txt
```
This command will install the exact versions of the dependencies required for the project.

### Step 3: Making an executable package on your platform
Once all dependencies are installed, you can run the `make.py` script:

```bash
python make.py
```
Or on some systems, you might need to use:

```bash
python3 make.py
```
This will execute the script and perform the make and packaging tasks defined in `make.py`.

### Step 4: Running the Script
* If you have ran "Step 3" then you can use the produced executable:
  *  YouTubeDownloader.exe for Windows
  *  YouTubeDownloader for Linux.
* A zip package is also produced for portable use with all necessary files.
* You can open it graphically or from the terminal. 
  * From the terminal you can start it as a command line tool or in GUI mode with a flag. 
  * You can also use it as a web application or cloud application and serve it via a webpage.
* You can also run all those options directly from python without "Step 3" from terminal or IDE. For easy quick start run:
  ```bash
  python run_app.py # will run the GUI by default.
  ```
  You can also run the actual starting point from inside src.
  ```bash
  cd src
  python YouTubeDownloader.py
  ```
### Additional Notes

- **Deactivating the Virtual Environment**: To exit the virtual environment, simply run `deactivate` in your terminal. This will revert to your global Python environment.
- **Reactivating**: To work on your project again after deactivating, navigate to your project directory and activate the virtual environment as shown in Step 1.


## Current State of Development TODO(s)

[//]: # (Add the current state of things section here when content is provided)
- [ ] There are various TODO notes in the coded related to implementation of features and bugfixes.

The program can work just fine portable but it's good to have a type of installer.
- [x] URL scraping from YouTube Channel URLs
  - [ ] Testing is needed, meaning automated testing procedures during build time.
- [ ] Per video quality stream selection no yet implemented. (only global limiters available at the moment)
This could be with a selection and a button to transfer the limits.
- [x] Finish the "keep file" functionality for separate audio,video, subtitle,etc. data.
  - [ ] Subtitles download and integration still to be implemented.
  - [ ] Comments download still to be implemented 
- [ ] Better progress reporting and percentage for download progress implementation.
This is relevant when there are a lot of links/text/channels inserted at the same time.
	- Download reporting is ok but not too detailed.
	- Analysis reporting could do much better. 

- [x] Improve multithreading and parallel downloads
    - It gets really slow when there is over hundred URLs to analyse, so for now the analyses is set to single thread by default.
- [ ] The settings sub-window needs to be implemented. Currently it is in embryonic state. 
  - In the settings window the user will be able to select, themes languages, paths, shortcut combinations etc.
  - Column order can also be implemented in the Settings and as drag and drop option.
- [x] Redesign file and functionality separation.
  - It would be necessary to better spread the functionality in the GUI and the core across files. 
  - This will make it easier for proper terminal use implementation. 
  - There should be an option for straight through command user and interactive terminal use.
- [ ] Final file size reporting should be corrected and make more accurate and reflect the latest changes.
- [ ] Better error handling, proper cancellation (and clean-up) and abrupt exit thread handling and clean-up should be implemented (especially for the windowed GUI mode).
- [ ] Speed and GUI responsiveness should also be improved.
- [ ] Bugfix: Sometimes not all videos are properly extracted from a playlist
- [ ] Add a playlist column in the main window
- [ ] There should be a LOG file option in the settings menu
- [ ] The cancel operation should be revaluated. Any bugs should be fixed for both download and analysis.

## Potential Features
- [ ] Webpage/Forum or some kind of marketing strategy for outreach to more users
- [ ] Add support for more video platforms
- [ ] Improve error handling and reporting
- [ ] Create a user guide and documentation
- [ ] Optimize performance and resource usage
	- [x] Some parts about startup were optimized. But still not the best
- [ ] Expand language support
- [ ] Add user customization options (themes, settings, etc.) made more accessible.
- [ ] Implement automatic updates and version checking
- [ ] Resilience for errors/corruption in Theme and config file on startup
- [ ] Error & Bug reporting
- [ ] Use sub-directory for the channels and playlists