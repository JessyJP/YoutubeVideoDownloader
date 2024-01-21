"""
File: display_container.py

Application Name: Youtube Video Downloader
Description: This application allows users to download videos from YouTube by providing a valid URL.
The user can analyze the video properties and choose the desired quality before downloading the video.

Author: JessyJP
Email: your.email@example.com TODO: add later
Date: April 8, 2023

Copyright (C) 2023 Your Name. All rights reserved.

License:
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
# Core imports
from core.pytube_handler import LimitsAndPriority, VideoInfo
from core.download_options import * # updateOutputKeepsStr, MediaSymbols # NOTE:imports the symbol list as well
# GUI custom imports
# from  mobile_kivy_gui.video_item_card_row import VideoItemRowCard as VideoItemCard
from  mobile_kivy_gui.video_item_card import VideoItemCard as VideoItemCard
# from  mobile_kivy_gui.video_item_text_row import VideoItemTextRow as VideoItemCard
# GUI imports
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner

from kivy.clock import Clock
from core.common import hex_to_rgba

from kivy.graphics import Color, Rectangle

# from gui.settings_window import SettingsWindow # TODO: reimplement the settings window

# TODO: check the imports for redundancy or unused ones

# Refactor the item display container
class VideoItemDisplayContainer():
    def createVideoItemDisplayContainer(self, TC, theme):
        self.theme = theme  # Store the provided theme for later use

        # Get the column headings and visibility settings
        self.colLabelDict = self.theme["container"]["heading"]
        self.columns = self.theme["container"]["heading"].keys()
        self.column_visible = {col: self.theme["container"]["column_visibility"][col] for col in self.columns}
        self.sortColumn = ""

        # ---------- Create a horizontal layout for column headers ----------
        self.headers_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, size_hint_x=1)
        # TODO: check why this was commented out
        # with self.headers_layout.canvas.before:
        #     Color(rgba=hex_to_rgba(self.theme["container"]["colors"]["heading-bg"]))  # Set background color for headers
        #     Rectangle(size=self.headers_layout.size, pos=self.headers_layout.pos)
        # #end

        # Calculate the width for each column
        self.column_width = self.update_column_width(Window.width)

        self.update_headings_visibility()

        # ---------- Create the GridLayout for the scrollable content ----------
        grid_layout = GridLayout(cols=1, size_hint_y=None)  # Single column for vertical stacking
        grid_layout.bind(minimum_height=grid_layout.setter('height'))

        # ---------- Create the ScrollView and add the grid_layout to it ----------
        scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height))
        scroll_view.add_widget(grid_layout)

        # Create the main layout and add the headers and scroll view to it
        container_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        container_layout.add_widget(self.headers_layout)
        container_layout.add_widget(scroll_view)

        # Store references for future use
        self.grid_layout = grid_layout
        self.scroll_view = scroll_view

        # Method to update the container layout
        def update_container_layout_callback(instance, new_size):
            self.update_container_layout(instance, new_size)
        #end
        # Bind the update_container_layout method to window resize event
        Window.bind(size=update_container_layout_callback)

        # Return the main container layout
        return container_layout
    #end

    # Column update method
    def update_headings_visibility(self):
        # Calculate the width for each column
        self.column_width = self.update_column_width(Window.width)

        # Clear all current labels from headers_layout
        self.headers_layout.clear_widgets()
        # Add column headers to the headers_layout
        for col in self.columns:
            if self.column_visible[col]:
                col_label = Label(
                    text=col,
                    size_hint_x=None,
                    width=self.column_width,
                    color=hex_to_rgba(self.theme["container"]["colors"]["heading-text"])
                )
                col_label.halign = 'left'  # Horizontal alignment
                col_label.valign = 'middle'  # Vertical alignment
                col_label.text_size = (col_label.width, None)  # Set text size for proper alignment
                self.headers_layout.add_widget(col_label)
            #end
        #end
    #end

    def update_column_width(self, width):
        visColCount = sum(value for value in self.column_visible.values())
        visColCount = visColCount if visColCount > 0 else 1
        return width / visColCount if visColCount > 0 else 1

    def update_container_layout(self ,instance, new_size):
        # Method to update the container layout size based on the window size
        # Adjust the self.scroll_view's size and the grid and update the headings and content's size    
        # Update the width of each column header
        for label in self.headers_layout.children:
            label.width = self.update_column_width( new_size[0])
            label.text_size = (label.width, None)  # Set text size for proper alignment

        # Update the width of each card in the grid layout
        for card in self.grid_layout.children:
            if isinstance(card, VideoItemCard):
                card.update_width(new_size[0])

        elH = 50 # Element height # TODO: this is currently hardcoded here but should be inserted from the main method or global definition var/const

        # Adjust the height of the scroll_view to fill available space
        remaining_height = Window.height - self.headers_layout.height - sum([elH for _ in range(4+1+1)])
        # self.scroll_view.size_hint_y = None
        self.scroll_view.height = max(remaining_height, self.grid_layout.minimum_height)
    #end

    def find_UI_item_by_id(self,ui_item_id):
        ui_item = None
        if isinstance(ui_item_id, VideoItemCard):
            return ui_item_id # NOTE: directly return the UI item if 
        #end

        # find the UI item by id
        for child in self.grid_layout.children:
            if ui_item_id == child.selection_id:
                ui_item = child
                break;
            #end
        #end
        if ui_item is None:
            raise("UI item was not found by ID!")
        #end
        return ui_item
    #end


    # ------ The basic get/set/add/remove interfacing methods with the container -------
    
    def get_all_items(self):
        # Return only VideoItemCard objects
        return [child for child in self.grid_layout.children if isinstance(child, VideoItemCard)]

    def get_selection(self):
        # Return a list of selection IDs of selected VideoItemCard objects
        return [child.selection_id for child in self.grid_layout.children if isinstance(child, VideoItemCard) and child.is_selected]

    def add(self, item):
        # Assuming 'item' is an instance of VideoInfo
        def scheduled_execution(self, item, dt):  # dt is required as Clock passes the delta time
            card = VideoItemCard(item, self.column_visible, self.theme)
            self.grid_layout.add_widget(card)
        Clock.schedule_once(lambda dt:  scheduled_execution(self, item, dt))

    def remove(self, ui_item):
        # 'item' should be a reference to the VideoItemCard to remove
        Clock.schedule_once(lambda dt:  self.grid_layout.remove_widget(ui_item) )

    def get_UiItmField(self, ui_item_id, field):
        # Get a specific field value from a VideoItemCard
        if isinstance(ui_item_id,VideoItemCard):
            ui_item = ui_item_id
        else:
            ui_item = self.find_UI_item_by_id(ui_item_id)
        #end
        return ui_item.labels[field].text

    def set_UiItmField(self, ui_item_id, field, value):
        # Set a specific field value in a VideoItemCard
        if isinstance(ui_item_id,VideoItemCard):
            ui_item = ui_item_id
        else:
            ui_item = self.find_UI_item_by_id(ui_item_id)
        #end
        ui_item.labels[field].text = value # Setting the Label text

    def get_UiItmField_byColInd(self, ui_item, col_index):
        # TODO: code cleanup will be needed 
        return self.get_UiItmField(ui_item, col_index)


# === Application Stage 4: Youtube Video table Info user manipulation ===
    # ------ Callbacks and companion functions for the tree view columns Context menu -------
    # Add a show popup menu method callback for the header/headings visibility
    def show_tree_popup_menu_callback(self, event):
        if not hasattr(self, 'current_dropdown'):
            # Create a dropdown menu for column visibility
            self.current_dropdown = DropDown()
        #end

        # Check if a dropdown is already open and attached
        if self.current_dropdown.attach_to:
            return  # Do nothing if a dropdown is already open
        else:
            # Clear and reuse the current dropdown, or create a new one if it doesn't exist
            self.current_dropdown.clear_widgets() 
            self.current_dropdown = DropDown()           
        #end       

        # Calculate the width needed for the dropdown
        max_text_length = max(len(col) for col in self.columns)
        dropdown_width = (max_text_length + 4) * 12  # Assuming each character takes up 10 pixels

        for col in self.columns:
            symbol = " ☑  " if self.column_visible[col] else "     "
            btn_text = f"{symbol}{col}"
            btn = Button(text=btn_text, size_hint_y=None, height=44, size_hint_x=None, width=dropdown_width)
            btn.halign = 'left'  # Horizontal alignment
            btn.valign = 'middle'  # Vertical alignment
            btn.text_size = (btn.width, None)  # Set text size for proper alignment
            btn.column_name = col # NOTE: Store the column name in the button object
            btn.bind(on_release=lambda btn: self.current_dropdown.select(btn.column_name))
            self.current_dropdown.add_widget(btn)
        #end

        # Open the dropdown menu
        self.current_dropdown.width = dropdown_width
        # You need to position it correctly based on your app layout
        self.current_dropdown.open(self.headers_layout)

        # Bind on_select event of dropdown
        self.current_dropdown.bind(on_select=lambda instance, x: self.toggle_column_visibility(x))
    #end

    def toggle_column_visibility(self, col):
        self.column_visible[col] = not self.column_visible[col]
        self.update_headings_visibility()
        # Update visibility in all VideoItemCards
        for card in self.grid_layout.children:
            if isinstance(card, VideoItemCard):
                card.update_visibility(self.column_visible, self.grid_layout.width)
            #end
        #end
    #end

    # Add a sort column method
    def sort_column(self, col):
        # Sorting variables
        sortDirections = ["asc", "desc"]
        symbol = ["▲", "▼"]

        # Sorting logic based on column data
        sorted_cards = sorted(self.grid_layout.children, key=lambda x: x.get_value(col))
        self.grid_layout.clear_widgets()
        for card in sorted_cards:
            self.grid_layout.add_widget(card)

        return#TODO: temporary disabled

        # First remove the symbol from the heading
        if self.sortColumn != "":
            self.tree.heading(self.sortColumn, text=self.theme["container"]["heading"][self.sortColumn])#NOTE:_EXTERNAL_METHOD_
        #end

        # If the same column is selected, alternate the sorting direction
        if self.sortColumn == col:
            ind = (sortDirections.index(self.sortDirection) + 1) % len(sortDirections)
        else:
            ind = 0
        #end
        self.sortDirection = sortDirections[ind]
        heading_symbol = symbol[ind]

        # Get the data
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]

        # Try to cast the data as float i.e numerical otherwise keep it as text 
        def try_float(val):
            try:
                return float(val)
            except ValueError:
                return val
            #end
        #end

        # Some entries will be handled specifically
        def sort_key(item):
            value = item[0]
            if col == "download_size":
                value = value.split()[0]
            #end
            return try_float(value)
        #end

        # Do the sorting of the keys
        if self.sortDirection == "asc":
            data.sort(key=sort_key, reverse=False)
        else:
            data.sort(key=sort_key, reverse=True)
        #end

        # Create a mapping between tree view children IDs and their indices in the info table
        # id_to_index = {info.video_id: index for index, info in enumerate(self.getVideoList())}

        # Sort  the info table based on the sorted order of tree view data #TODO: fix error here
        # self.infoList = [x[1] for x in sorted(zip(data, self.getVideoList()), key=lambda x: id_to_index[x[0][1]])]
        # NOTE: Also if this is implemented it will require a sorting function to be implemented in the parent class 

        # Move the sorted data to the correct position in the treeview
        for indx, item in enumerate(data):
            self.tree.move(item[1], '', indx)
        #end

        # Update the status message to indicate the sorting column
        self.setUiDispStatus( f"Sorting by: {col} in "+heading_symbol+" direction")#NOTE:_EXTERNAL_METHOD_

        # Include a sorting direction symbol to the heading
        heading_text = self.theme["container"]["heading"][col]
        self.tree.heading(col,  text=heading_text +" "+ heading_symbol)#NOTE:_EXTERNAL_METHOD_

        # Keep track of the sorting column
        self.sortColumn = col
    #end

    # ------ Callbacks and companion functions for the tree view rows selection and deselection -------

    def select_all_entries(self, event=None):
        items = self.get_all_items()
        for item in items:
            item.update_selection(True)
        #end
        self.on_container_selection()
    #end

    def on_container_selection(self):
        selected_items = self.get_selection()
        total_items = len(self.get_all_items())

        if len(selected_items) == 1:
            item = selected_items[0]
            video_title = self.find_UI_item_by_id(item).title
            msg = f"Selected 1 item: {video_title}"
        else:
            msg = f"Selected {len(selected_items)} of {total_items} items"
        #end

        self.setUiDispStatus( msg)#NOTE:_EXTERNAL_METHOD_
    #end

    def extend_selection(self, event):
        if self.selection_anchor is None:
            return
        #end
        #TODO function needs to be fixed
        cur_selection = self.get_selection()

        if event.keysym == 'Up':
            first_selected = cur_selection[0]
            prev_item = self.tree.prev(first_selected)

            if prev_item:
                if self.selection_direction == 'Up':
                    self.tree.selection_add(prev_item)
                else:
                    self.tree.selection_remove(first_selected)
                    if first_selected == self.selection_anchor:
                        self.selection_direction = 'Up'
                    #end
                #end
            #end
        elif event.keysym == 'Down':
            last_selected = cur_selection[-1]
            next_item = self.tree.next(last_selected)

            if next_item:
                if self.selection_direction == 'Down':
                    self.tree.selection_add(next_item)
                else:
                    self.tree.selection_remove(last_selected)
                    if last_selected == self.selection_anchor:
                        self.selection_direction = 'Down'
                    #end
                #end
            #end
        #end
    #end

    def set_selection_anchor(self, event=None):
        if not hasattr(self, 'selection_anchor'):
            self.selection_anchor = None
        #end

        if not hasattr(self, 'selection_direction'):
            self.selection_direction = None
        #end

        cur_selection = self.get_selection()
        if cur_selection:
            if not self.selection_anchor:
                self.selection_anchor = cur_selection[0]
                self.selection_direction = 'Up' if event.keysym == 'Up' else 'Down'
            #end
        #end
    #end

    def clear_selection_anchor(self, event=None):
        self.selection_anchor = None
        self.selection_direction = None
        self.on_container_selection()
    #end

    def move_selection(self, direction: str, event=None):
        # TODO: this needs to be fixed, it skips one entry
        selected_items = self.get_selection()
        if selected_items:
            if direction == 'up':
                target_item = self.tree.prev(selected_items[0])
            elif direction == 'down':
                target_item = self.tree.next(selected_items[-1])
            else:
                return
            #end
            if target_item:
                self.tree.selection_set(target_item)
                self.tree.focus(target_item)
            #end
        #end
    #end

    def move_selection_up_callback(self, event=None):
        self.move_selection('up', event)
        self.on_container_selection()
    #end

    def move_selection_down_callback(self, event=None):
        self.move_selection('down', event)
        self.on_container_selection()
    #end

#end