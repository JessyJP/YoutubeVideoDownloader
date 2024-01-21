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
# Core imports
from core.download_options import * # updateOutputKeepsStr, MediaSymbols # NOTE:imports the symbol list as well
from core.common import audio_bitrate_list as BitrateList, video_resolution_list as ResolutionList, fps_value_list as FPSList
# GUI imports
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
import uuid
from core.common import hex_to_rgba
import random

from kivy.uix.image import AsyncImage  # Import for asynchronous image loading

# Create Video item card class
class VideoItemCard(BoxLayout):
    ''' Class for individual video items '''
    def __init__(self, item, visibility, theme, width_fraction=1, **kwargs):
        super().__init__(**kwargs)

        data = item.as_dict()
        self.labels = {}  # Dictionary to map keys to labels

        self.size_hint_y = None  # Disable vertical size hint
        self.height = 350  # Fixed height for each card
        self.vpad = 10
        self.padding = 10

        # Set orientation to horizontal to place the image and labels side by side
        self.orientation = 'horizontal'
        self.selection_id = str(uuid.uuid4())  # Unique identifier
        self.is_selected = False
        self.size_hint_x = width_fraction  # Set the width relative to the parent

        # Create an AsyncImage widget for the thumbnail
        self.thumbnail = AsyncImage(source=item.thumbnail_url, size_hint=(None, None), 
                                    size=(self.height - self.vpad, self.height - self.vpad), 
                                    allow_stretch=True)

        # Create a BoxLayout for labels (to the right of the image)
        self.labels_layout = BoxLayout(orientation='vertical', padding=[self.vpad, self.vpad])

        self.default_color = hex_to_rgba(theme["container"]["colors"]["tile"])
        self.selected_color = hex_to_rgba(theme["container"]["colors"]["selected"])

        # Background color setup
        rand_color = [random.random() for _ in range(3)] + [1]  # RGBA format
        with self.canvas.before:
            Color(rgba=self.default_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        #end

        # Update the size and position of the background rectangle
        def update_bg_rect(instance, value):
            instance.bg_rect.pos = instance.pos
            instance.bg_rect.size = instance.size
        #end
        self.bind(pos=update_bg_rect, size=update_bg_rect)


        self.visColCount = sum(value for value in visibility.values())
        # Add UI elements (labels) for each piece of data in the dictionary
        for key, value in data.items():
            label = Label(text=str(value))
            label.width = abs(Window.width - (self.height  + self.vpad * 3))
            self.labels[key] = label
        #end
        self.update_data_labels(visibility)
    #end

    def update_data_labels(self, new_visibility):
        self.labels_layout.clear_widgets()
        self.clear_widgets()

        # Set the size and position of the image
        image_width = self.height - self.vpad * 2  # Adjust width to maintain aspect ratio
        self.thumbnail.size_hint = (None, None)
        self.thumbnail.size = (image_width, image_width)
        self.thumbnail.pos_hint = {'center_x': 0.5}

        # Calculate the height for each label based on the number of visible labels
        visible_labels_count = sum(new_visibility.values())
        label_height = max((self.height - self.vpad * 2) / visible_labels_count, 20)  # Minimum height of 20
        label_width = abs(self.width - (image_width + self.vpad * 3))
        
        for key, label in self.labels.items():
            if new_visibility[key]:
                label.halign = 'left'  # Horizontal alignment
                label.valign = 'center'  # Vertical alignment
                label.text_size = (label_width, label_height)
                label.size_hint_y = None  # Disable vertical size hint
                label.height = label_height  # Set fixed height for each label
                self.labels_layout.add_widget(label)
            #end
        #end

        # Add the image and labels layout to the main layout
        self.add_widget(self.thumbnail)
        self.add_widget(self.labels_layout)
        self.last_visibility = new_visibility    
    #end

    def update_visibility(self, new_visibility, width):
        # Remove all widgets and re-add them based on updated visibility
        self.visColCount = sum(value for value in new_visibility.values())
        self.update_width(width)
        self.update_data_labels(new_visibility)
    #end

    def update_width(self, new_width):
        # Update the width of each label in the card
        for label in self.labels.values():
            label.width = new_width / (self.visColCount if self.visColCount>0 else 1)
        #end
        self.update_data_labels(self.last_visibility)
    #end

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.update_selection()
            return True
        #end
        return super(BoxLayout, self).on_touch_down(touch)
    #end

    def update_selection(self, selectionVal=None):
        if selectionVal is None:
            self.is_selected = not self.is_selected
        else:
            self.is_selected = selectionVal
        #end
        
        # Update the background color based on selection
        bg_color = self.selected_color if self.is_selected else self.default_color
        with self.canvas.before:
            Color(rgba=bg_color)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        #end
    #end

    # ---- GET/SET methods ----
    def get_value(self, key):
        return self.labels[key].text if key in self.labels else None
    #end

    def set_value(self, key, value):
        if key in self.labels:
            self.labels[key].text = str(value)
        #end
    #end
#end