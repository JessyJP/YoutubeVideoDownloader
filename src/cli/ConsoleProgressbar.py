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
import sys
import re
from time import sleep

class ConsoleProgressbarChecker:
    def __init__(self):
        # Log list
        self._logged_lines = []

    def log_output(self, line):
        """
        Log a line that is printed to the console.
        """
        self._logged_lines.append(line)

    def update_progress(self, progress_bar_str):
        """
        Update the console with the progress bar string.
        If the logged lines match a pattern, overwrite them.
        """
        if self.__should_overwrite():
            self.__overwrite_logged_output()
        print(progress_bar_str, end='\n')
        sys.stdout.flush()
        self._logged_lines = [progress_bar_str]  # Keep only the latest progress bar in the log

    def __should_overwrite(self):
        """
        Check if the logged lines contain the expected strings and there are exactly two strings in the log.
        """
        if len(self._logged_lines) != 2:
            return False

        return ("Progress:" in self._logged_lines[0]) and ("URL thread check" in self._logged_lines[1])

    def __overwrite_logged_output(self):
        """
        Overwrite the logged output with blank space.
        """
        # Overwrite the last two lines (message and progress bar)
        sys.stdout.write('\x1b[1A')  # Move the cursor up one line
        sys.stdout.write('\x1b[2K')  # Clear the current line
        sys.stdout.write('\x1b[1A')  # Move the cursor up one line
        sys.stdout.write('\x1b[2K')  # Clear the current line

# ================================= Progress bar string maker =================================
def make_progress_bar_str(progress, width=72):
    """
    Make a text-based progress bar for the terminal.

    :param progress: The progress percentage (0 to 100).
    :param width: The width of the progress bar in characters.
    """
    filled_length = int(width * progress // 100)
    bar = '█' * filled_length + '-' * (width - filled_length)
    if progress >= 100:
        bar+= '\n'
    return f'\rProgress: |{bar}| {progress:.2f}%'

## ================================= TESTING SECTION ===========================
def test():
    # --- ASSUME NO DIRECT ACCESS --- Mock STATS function begin---
    def diagnostic_message(stats):
        message = (
            f"URL thread check(s) Total: {stats['total_threads']}    "
            f"Active: {stats['active_threads']}    "
            f"Completed: {stats['successful_threads']}    "
            f"Errors: {stats['errored_threads']}    "
        )
        return message
    # --- ASSUME NO DIRECT ACCESS --- Mock STATS function end ---

    # Example usage
    console_updater = ConsoleProgressbarChecker()

    # Simulate updating the console
    total_time = 3
    total_range = 1000
    for i in range(total_range + 1):
        # --- ASSUME NO DIRECT ACCESS --- Mock STATS begin ---
        stats = {
            'total_threads': total_range,
            'active_threads': total_range - i,
            'successful_threads': i,
            'errored_threads': 0
        }
        message = diagnostic_message(stats)
        # --- ASSUME NO DIRECT ACCESS --- Mock STATS end ---

        progress_percent = (i / total_range) * 100
        progress_bar_str = make_progress_bar_str(progress_percent)

        # Printing and logging diagnostic messages
        console_updater.update_progress(progress_bar_str)
        print(message)
        console_updater.log_output(message)
        sleep(total_time / total_range)

if __name__ == "__main__":
    test()
#end