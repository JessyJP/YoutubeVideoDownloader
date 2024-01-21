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
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
from core import *

install_missing_modules(["selenium"])

def getHTMLfromURLpage(url, waitForUser=False):
    # Set up the Chrome webdriver with or without headless option
    options = webdriver.ChromeOptions()
    if not waitForUser:
        options.headless = True
    driver = webdriver.Chrome(options=options)
    
    # Navigate to the URL
    driver.get(url)
    
    if waitForUser:
        # Wait for the user to interact with the web page or close the browser window
        while True:
            try:
                # Check if the browser window is still open
                driver.current_url

                # Get the fully-rendered HTML content of the page
                html = driver.page_source
            except WebDriverException:
                # Browser window is closed, exit the loop
                break

            # Add a 10ms delay on every cycle
            time.sleep(0.01)
    else:
        # Wait for the page to load completely
        driver.execute_script("return document.readyState")
        
        # Get the fully-rendered HTML content of the page
        html = driver.page_source
    
    # Quit the webdriver
    driver.quit()
    
    # Return the HTML content of the page as plain text
    return html
#end

def find_watch_in_html(url: str) -> list[str]:
    # Fetch the HTML content from the URL
    html_content = getHTMLfromURLpage(url, True)

    # Split the HTML content into lines
    lines = html_content.splitlines()

    # Search for all lines that contain the string "/watch"
    watch_lines = [line for line in lines if "/watch" in line]

    return watch_lines
#end


################ TEST #################

url = "https://www.youtube.com/@rjpbooks"

answer = is_youtube_url(url)
answer = checkForValidYoutubeURLs(url)
answer = is_valid_youtube_playlist(url)
answer = is_valid_youtube_channel(url)


links = find_watch_in_html(url)

print("\n\n")
for i, link in enumerate(links):
    print(f"{i}: {link}")
# get_channel_videos(channel_id)
print("\n\n")