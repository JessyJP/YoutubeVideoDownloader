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
from tkinter import ttk

# TODO: Might not be useful at all
class AutoHideScrollbar(ttk.Scrollbar):
    def __init__(self, master=None, **kwargs):
        ttk.Scrollbar.__init__(self, master, **kwargs)
        self.bind('<Enter>', self.on_mouse_enter)
        self.bind('<Leave>', self.on_mouse_leave)
        self.grid_remove()

    def on_mouse_enter(self, event):
        self.grid()

    def on_mouse_leave(self, event):
        if not self.identify(event.x, event.y) == 'slider':
            self.grid_remove()