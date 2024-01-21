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
# Imports
import threading

## ================================= Multithreading functions =================================
class CustomThread(threading.Thread):
    threads = []# TODO: this could potentially be implemented with a tag/label to indicate the groups
    # TODO:NOTE: or it could be implemented such that this stores the threads for a specific period of time.
    #... and is not using a static variable (list) to hold the thread handles.

    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self.exception = None
        self.exitcode = 0
        CustomThread.threads.append(self)

    def run(self):
        try:
            super(CustomThread, self).run()
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