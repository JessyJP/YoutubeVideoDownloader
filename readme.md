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

## Current State of Development

[//]: # (Add the current state of things section here when content is provided)
- [ ] There are various TODO notes in the coded related to implementation of features and bugfixes.
- [x] First and foremost stable packaging and release mechanism.
The program can work just fine portable but it's good to have a type of installer.
- [x] URL scraping from YouTube Channel URLs
  - [ ] Testing is needed 
- [ ] Per video quality stream selection no yet implemented. (only global limiters available at the moment)
- [x] Finish the "keep file" functionality for separate audio,video, subtitle,etc. data(Easy to implement)
  - [ ] Subtitles download and integration still to be implemented.
  - [ ] Comments download still to be implemented 
- [ ] Better progress reporting and percentage for download progress implementation

- [ ] Improve multithreading and parallel downloads
    - It gets really slow when there is over hundred URLs to analyse, so for now the analyses is set to single thread by default.
- [ ] The settings sub-window needs to be implemented. Currently it is in embryonic state. 
  - In the settings window the user will be able to select, themes languages, paths, shortcut combinations etc.
  - Column order can also be implemented in the Settings and as drag and drop option.
- [ ] Redesign file and functionality separation.
  - It would be necessary to better spread the functionality in the GUI and the core across files. 
  - This will make it easier for proper terminal use implementation. 
  - There should be an option for straight through command user and interactive terminal use.
- [ ] Final file size reporting should be corrected and make more accurate and reflect the latest changes.
- [ ] Better error handling, proper cancellation (and cleanup) and abrupt exit thread handling and cleanup should be implemented (especially for the windowed GUI mode).
- [ ] Speed and GUI responsiveness should also be improved.
- [ ] Bugfix: Sometimes not all videos are properly extracted from a playlist
- [ ] Add a playlist column in the main window
- [ ] There should be a LOG file option in the settings menu

## Potential Features
- [ ] Webpage/Forum or some kind of marketing strategy for outreach to more users
- [ ] Add support for more video platforms
- [ ] Improve error handling and reporting
- [ ] Create a user guide and documentation
- [ ] Optimize performance and resource usage
- [ ] Expand language support
- [ ] Add user customization options (themes, settings, etc.) made more accessible.
- [ ] Implement automatic updates and version checking
- [ ] Resilience for errors/corruption in Theme and config file on startup
- [ ] Error & Bug reporting
- [ ] Use sub-directory for the channels and playlists