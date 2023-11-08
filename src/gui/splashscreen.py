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
import tkinter as tk
import time

def show_splash_screen():
    splash_root = tk.Tk()
    splash_root.overrideredirect(True)

    screen_width = splash_root.winfo_screenwidth()
    screen_height = splash_root.winfo_screenheight()

    splash_image = tk.PhotoImage(file="./images/IconProjects/pngaaa.com-4933843.png")
    splash_label = tk.Label(splash_root, image=splash_image)
    splash_label.pack()

    splash_root.geometry(f"+{screen_width//2 - splash_image.width()//2}+{screen_height//2 - splash_image.height()//2}")

    splash_root.after(2000, splash_root.destroy)  # Close splash screen after 3 seconds (3000 milliseconds)
    splash_root.mainloop()
#end


show_splash_screen()# Run the splash screen