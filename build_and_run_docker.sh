#!/bin/bash

# Check if the container exists and remove it
if [ $(sudo docker ps -a -q -f name=youtube-downloader-container) ]; then
    sudo docker rm -f youtube-downloader-container
fi

# Build the Docker image
sudo docker build -t youtube-downloader .

# Run the Docker container
sudo docker run -p 8080:8080 -v /home/jp/youtube_download_tmp:/app/tmp --name youtube-downloader-container youtube-downloader
