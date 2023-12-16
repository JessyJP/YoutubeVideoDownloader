"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This is a python source script part of the YouTube Video Downloader Suit.

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
# import googleapiclient.discovery
# from googleapiclient.errors import HttpError
from validation_methods import check_for_disallowed_filename_chars

def download_comments(video_id, base_output_name, output_dir, api_key, output_format="json"):
    youtube = ""#googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Create the output file path
    output_filename = check_for_disallowed_filename_chars(f"{base_output_name}.comments.{output_format}")
    output_file_path = os.path.join(output_dir, output_filename)

    comments_list = []
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100  # Adjust as needed
        )
        response = request.execute()

        for item in response.get("items", []):
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments_list.append({
                "text": comment["textDisplay"],
                "author": comment["authorDisplayName"],
                "author_channel_url": comment["authorChannelUrl"],
                "published_at": comment["publishedAt"],
                "likes": comment["likeCount"],
            })

        # Write to output file
        if output_format == "json":
            with open(output_file_path, "w", encoding="utf-8") as f:
                json.dump(comments_list, f, ensure_ascii=False, indent=4)
        elif output_format == "csv":
            import csv
            fieldnames = ["text", "author", "author_channel_url", "published_at", "likes"]
            with open(output_file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for comment in comments_list:
                    writer.writerow(comment)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

    except:# HttpError as e:
        print(f"An HTTP error occurred: {e.resp.status} {e.content}")
        sys.exit(1)

    return output_file_path

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python download_video_comments.py <video_id> <base_output_name> <output_dir> <api_key> <output_format>")
        sys.exit(1)

    video_id = sys.argv[1]
    base_output_name = sys.argv[2]
    output_dir = sys.argv[3]
    api_key = sys.argv[4]
    output_format = sys.argv[5] if len(sys.argv) > 5 else "json"

    if not os.path.exists(output_dir):
        print(f"Output directory does not exist: {output_dir}")
        sys.exit(1)

    try:
        download_comments(video_id, base_output_name, output_dir, api_key, output_format)
    except Exception as e:
        print(f"Error downloading comments: {e}")
        sys.exit(1)
