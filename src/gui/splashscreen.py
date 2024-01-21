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