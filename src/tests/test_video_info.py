import unittest
import os
import sys
# Add the 'src' directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
from core.yt_dlp_handler import VideoInfo

class TestVideoInfo(unittest.TestCase):

    # You can use a sample YouTube video for testing purposes.
    TEST_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    OUTPUT_DIR = "./test_output"

    def setUp(self):
        """ Set up for test, instantiate VideoInfo class """
        # Create an instance of VideoInfo for testing
        self.video_info = VideoInfo(url=self.TEST_VIDEO_URL)

        # Create output directory for downloading files
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)

    def tearDown(self):
        """ Clean up any files downloaded during the tests """
        if os.path.exists(self.OUTPUT_DIR):
            for file in os.listdir(self.OUTPUT_DIR):
                os.remove(os.path.join(self.OUTPUT_DIR, file))
            os.rmdir(self.OUTPUT_DIR)

    def test_metadata_extraction(self):
        """ Test extraction of video metadata """
        metadata = self.video_info.as_dict()
        self.assertIn("title", metadata)
        self.assertIn("author", metadata)
        self.assertIn("length", metadata)
        print(f"Metadata: {metadata}")

    def test_select_audio_stream(self):
        """ Test selection of the best audio stream """
        audio_stream = self.video_info.select_audio_stream(max_audio_bitrate="max")
        self.assertIsNotNone(audio_stream)
        print(f"Audio Stream: {audio_stream}")

    def test_select_video_stream(self):
        """ Test selection of the best video stream """
        video_stream = self.video_info.select_video_stream(max_resolution="max", max_fps="max")
        self.assertIsNotNone(video_stream)
        print(f"Video Stream: {video_stream}")

    def test_download_thumbnail(self):
        """ Test downloading the thumbnail image """
        thumbnail_file = self.video_info.download_thumbnail(self.OUTPUT_DIR, format="jpg")
        self.assertTrue(os.path.exists(thumbnail_file))
        print(f"Thumbnail File: {thumbnail_file}")

    def test_download_audio(self):
        """ Test downloading the audio stream """
        audio_stream = self.video_info.select_audio_stream(max_audio_bitrate="max")
        audio_file = self.video_info.download_audio(audio_stream, self.OUTPUT_DIR)
        self.assertTrue(os.path.exists(audio_file))
        print(f"Audio File: {audio_file}")

    def test_download_video(self):
        """ Test downloading the video stream """
        video_stream = self.video_info.select_video_stream(max_resolution="max", max_fps="max")
        video_file = self.video_info.download_video(video_stream, self.OUTPUT_DIR)
        self.assertTrue(os.path.exists(video_file))
        print(f"Video File: {video_file}")

    def test_download_info(self):
        """ Test downloading video info to a file """
        info_file = self.video_info.download_video_info(self.OUTPUT_DIR)
        self.assertTrue(os.path.exists(info_file))
        print(f"Info File: {info_file}")

    def test_checkIfDownloadIsPending(self):
        """ Test the checkIfDownloadIsPending method """
        is_pending = self.video_info.checkIfDownloadIsPending()
        self.assertIsInstance(is_pending, bool)
        print(f"Download Pending: {is_pending}")

if __name__ == '__main__':
    unittest.main()
