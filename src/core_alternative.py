import youtube_dl
import os
import shutil
import requests
from typing import Tuple


class VideoInfo_alternative:
    def __init__(self, url: str, download_status: str = "☑", inputOrderIndex: int = None):
        self.url = url
        self.download_status = download_status
        self.inputOrderIndex = inputOrderIndex
        self.logger = []

        ydl_opts = {'format': 'bestaudio+bestvideo/best'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url, download=False)
            self.info = info_dict
            self.title = info_dict.get('title', None)
            self.author = info_dict.get('uploader', None)
            self.length = info_dict.get('duration', None)
            self.description = info_dict.get('description', None)
            self.publish_date = info_dict.get('upload_date', None)
            self.views = info_dict.get('view_count', None)
            self.thumbnail_url = info_dict.get('thumbnail', None)
            self.rating = info_dict.get('average_rating', None)
            self.video_id = info_dict.get('id', None)

    def as_tuple(self) -> Tuple:
        return (
            self.download_status,
            self.url,
            self.title,
            self.author,
            self.length,
            self.description,
            self.publish_date,
            self.views,
            self.thumbnail_url,
            self.rating,
            self.video_id,
        )

    def download_audio(self, output):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{output}/{self.title}.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def download_video(self, output):
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{output}/{self.title}.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def download_thumbnail(self, output_dir: str, format="jpg") -> str:
        thumbnail_url = self.thumbnail_url
        thumbnail_filename = os.path.join(output_dir, f"{self.title}_thumbnail.{format}")
        thumbnail_data = requests.get(thumbnail_url).content
        with open(thumbnail_filename, 'wb') as f:
            f.write(thumbnail_data)
        return thumbnail_filename

    # More methods to be implemented
