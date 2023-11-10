"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Date: April 7, 2023
Description: This script downloads YouTube videos in the specified quality or allows the user to select a quality from the available streams.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Imports
import threading

## ================================= Multithreading functions =================================
class AnalysisThread(threading.Thread):
    threads = []

    def __init__(self, *args, **kwargs):
        super(AnalysisThread, self).__init__(*args, **kwargs)
        self.exception = None
        self.exitcode = 0
        AnalysisThread.threads.append(self)

    def run(self):
        try:
            super(AnalysisThread, self).run()
        except Exception as e:
            self.exception = e
            self.exitcode = 1

    @classmethod
    def get_all_threads(cls, name_contains=""):
        threads = [t for t in cls.threads if name_contains in t.getName()]
        return threads

    @classmethod
    def get_active_threads(cls, thread_list=None):
        if thread_list is None:
            thread_list = cls.threads
        active_threads = [t for t in thread_list if t.is_alive()]
        return active_threads

    @classmethod
    def get_successful_threads(cls, thread_list=None):
        if thread_list is None:
            thread_list = cls.threads
        completed_threads = [t for t in thread_list if not t.is_alive() and t.exception is None]
        return completed_threads

    @classmethod
    def get_errored_threads(cls, thread_list=None):
        if thread_list is None:
            thread_list = cls.threads
        errored_threads = [t for t in thread_list if not t.is_alive() and t.exitcode != 0]
        return errored_threads

    @classmethod
    def get_multithread_stats(cls, name_contains=""):
        thread_list = cls.get_all_threads(name_contains)
        active_threads = cls.get_active_threads(thread_list)
        successful_threads = cls.get_successful_threads(thread_list)
        errored_threads = cls.get_errored_threads(thread_list)

        stats = {
            "total_threads": len(cls.threads),
            "active_threads": len(active_threads),
            "successful_threads": len(successful_threads),
            "errored_threads": len(errored_threads)
        }

        return stats
    #end    

    @classmethod
    def reset_threads(cls):
        cls.threads.clear()
    #end
#end