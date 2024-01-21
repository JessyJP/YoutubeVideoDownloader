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
from PIL import Image, ImageTk
from io import BytesIO
import requests

# Experimental implementation for a different table or card grid look for the table.

class TableRow(tk.Frame):
    def __init__(self, master, image_source, text_fields, button_text):
        super().__init__(master)
        self.image_label = None  # Placeholder for the image label
        
        try:
            self.load_thumbnail(image_source)
        except Exception as e:
            self.display_substitute_text()
        
        self.create_text_fields(text_fields)
        self.create_button(button_text)

    def load_thumbnail(self, image_source):
        # Load the image from different sources
        if image_source.startswith('http'):  # Load from URL
            response = requests.get(image_source)
            response.raise_for_status()  # Check for request errors
            image_data = response.content
        elif image_source.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # Load from file
            with open(image_source, 'rb') as f:
                image_data = f.read()
        else:  # Assume image_source is a data blob
            image_data = image_source

        # Create and place the image
        image = Image.open(BytesIO(image_data))
        image.thumbnail((50, 50))  # Adjust image size as needed
        self.image = ImageTk.PhotoImage(image)
        self.image_label = tk.Label(self, image=self.image)
        self.image_label.pack(side=tk.LEFT)
    
    def display_substitute_text(self):
        # If there's an error, display substitute text
        self.image_label = tk.Label(self, text="No Thumbnail\nAvailable", padx=10, pady=10)
        self.image_label.pack(side=tk.LEFT)
        
    def create_text_fields(self, text_fields):
        # Create and place the text fields
        self.text_entries = []
        for field in text_fields:
            entry = tk.Entry(self)
            entry.insert(tk.END, field)
            entry.pack(side=tk.LEFT)
            self.text_entries.append(entry)
    
    def create_button(self, button_text):
        # Create and place the button
        self.button = tk.Button(self, text=button_text)
        self.button.pack(side=tk.LEFT)

class DynamicTable(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.rows = []  # List to store rows

    def add_row(self, image_source, text_fields, button_text):
        row = TableRow(self, image_source, text_fields, button_text)
        row.pack()
        self.rows.append(row)
    
    def remove_row(self, index):
        if 0 <= index < len(self.rows):
            row = self.rows.pop(index)
            row.pack_forget()
            row.destroy()

# Create the main window
root = tk.Tk()

# Create a dynamic table
table = DynamicTable(root)
table.pack()

# Add initial rows
table.add_row('image1.png', ['Text Field 1', 'Text Field 2'], 'Button 1')
table.add_row('https://example.com/image2.png', ['Text Field 3', 'Text Field 4'], 'Button 2')
table.add_row(b'Invalid Image Data', ['Text Field 5', 'Text Field 6'], 'Button 3')

# Run the application
root.mainloop()
