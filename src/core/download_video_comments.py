"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

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
import os
import sys
import json
import csv
import pytchat
# NOTE:TODO: this library is suitable for live streaming but not suitable for downloading comments
from validation_methods import check_for_disallowed_filename_chars
# from core.validation_methods import check_for_disallowed_filename_chars
def download_comments(video_id, base_output_name , output_dir: str, output_format: str = "json") -> str:
    """
    Download the comments for the video.

    :param output_dir: The directory where the output file will be saved.
    :param output_format: The output file format. Supported formats are "json" and "csv". Default is "json".
    :return: The full path of the output file.
    """

    print(f"Download comments for [{base_output_name}] at [{output_dir}] with video id [{video_id}]")

    # Create the output file path
    output_filename = check_for_disallowed_filename_chars(f"{base_output_name}.comments.{output_format}")
    output_file_path = os.path.join(output_dir, output_filename)

    # Download the comments and write them to the output file
    if output_format == "json":
        comments = pytchat.create(video_id=video_id)
        comments_list = []
        for c in comments.sync_items():
            comment = {
                "text": c.message,
                "author": c.author.name,
                "author_channel_url": c.author.channel_url,
                "published_at": c.datetime.isoformat(),
                "likes": c.likecount,
                "replies": c.replycount
            }
            comments_list.append(comment)

        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(comments_list, f, ensure_ascii=False, indent=4)
    elif output_format == "csv":
        comments = pytchat.create(video_id=video_id)
        fieldnames = ["text", "author", "author_channel_url", "published_at", "likes", "replies"]
        with open(output_file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in comments.sync_items():
                writer.writerow({
                    "text": c.message,
                    "author": c.author.name,
                    "author_channel_url": c.author.channel_url,
                    "published_at": c.datetime.isoformat(),
                    "likes": c.likecount,
                    "replies": c.replycount
                })
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    return output_file_path
#end

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python download_video_comments.py <video_id> <base_output_name> <output_dir> <output_format>")
        sys.exit(1)
    
    video_id = sys.argv[1]
    base_output_name = sys.argv[2]
    output_dir = sys.argv[3]
    output_format = sys.argv[4] if len(sys.argv) > 4 else "json"
    
    if not os.path.exists(output_dir):
        print(f"Output directory does not exist: {output_dir}")
        sys.exit(1)

    try:
        download_comments(video_id, base_output_name, output_dir, output_format)
    except Exception as e:
        print(f"Error downloading comments: {e}")
        sys.exit(1)