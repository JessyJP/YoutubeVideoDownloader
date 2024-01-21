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

class BorderedLabel(Label):
    def __init__(self, **kwargs):
        super(BorderedLabel, self).__init__(**kwargs)
        self.text_size = (self.width, None)  # Set text size for proper alignment
        self.halign = "right"  # Horizontal alignment to the right
        self.valign = "middle"  # Vertical alignment to the middle
        with self.canvas.before:
            Color(rgba=(0.8, 0.8, 0.8, 1))  # Light gray background
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_bg_rect, pos=self.update_bg_rect)

    def update_bg_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

# Create Video item card class
class VideoItemTextRow(BoxLayout):
    ''' Class for individual video items '''
    def __init__(self, item, visibility, theme, width_fraction=1, **kwargs):
        super().__init__(**kwargs)

        data = item.as_dict()
        self.labels = {}  # Dictionary to map keys to labels

        self.size_hint_y = None  # Disable vertical size hint
        self.height = 49  # Fixed height for each card

        self.orientation = 'horizontal'  # Set orientation for the row
        self.selection_id = str(uuid.uuid4())  # Unique identifier
        self.is_selected = False
        self.size_hint_x = width_fraction  # Set the width relative to the parent

        self.default_color = hex_to_rgba(theme["container"]["colors"]["tile"])
        self.selected_color = hex_to_rgba(theme["container"]["colors"]["selected"])

        # Generate a random background color
        rand_color = [random.random() for _ in range(3)] + [1]  # RGBA format

        # Set the background color
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
            label = Label(text=str(value), size_hint_x=None, width=Window.width / (self.visColCount if self.visColCount>0 else 1) )
            # label = BorderedLabel(text=str(value), size_hint_x=None, width=Window.width / (self.visColCount if self.visColCount>0 else 1))
            self.labels[key] = label
        #end
        self.update_data_labels(visibility)
    #end

    def update_data_labels(self, new_visibility):
        self.clear_widgets()
        for key, label in self.labels.items():
            if new_visibility[key]:
                label.halign = 'left'  # Horizontal alignment
                label.valign = 'middle'  # Vertical alignment
                label.text_size = (label.width, None)  # Set text size for proper alignment
                self.add_widget(label)
            #end
        #end
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