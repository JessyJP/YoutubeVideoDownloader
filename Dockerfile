# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files and directories into the container
COPY ./src /app/src
COPY ./data /app/data
COPY ./images /app/images
COPY ./themes /app/themes
COPY ./.gitignore /app/.gitignore
# COPY ./Dockerfile /app/Dockerfile
COPY ./webapp.env /app/webapp.env
COPY ./config.ini /app/config.ini
COPY ./readme.md /app/readme.md
COPY ./make.py /app/make.py
COPY ./run_app_gui.py /app/run_app_gui.py
COPY ./versioned_requirements.txt /app/versioned_requirements.txt
# We could have a dockerignore file, but this is also fine.

RUN mkdir /app/tmp

# Install Gunicorn and any other needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/versioned_requirements.txt
RUN pip install --no-cache-dir gunicorn

# Make port 8080 available to the world outside this container
EXPOSE 8080
ENV PYTHONUNBUFFERED=1

WORKDIR /app/src

# Production server
# Define command to start the application using Gunicorn
# CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8080", "YouTubeDownloaderWEB:app"]

#  Development server
# RUN python ./make.py

# WORKDIR /app/src
CMD ["python","./YouTubeDownloader.py", "--web", "--enable-analysis-threading","--enable-download-threading","--output","/app/tmp"]
