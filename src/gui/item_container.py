"""
File: item_container.py

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
from core.download_options import * # updateOutputKeepsStr, MediaSymbols # NOTE:imports the symbol list as well
# GUI imports
import tkinter as tk
from tkinter import ttk

# Refactor the item display container
class VideoItemDisplayContainer():

    def createVideoItemDisplayContainer(self, frame,TC):
        # Get tree view column headings
        self.columns = tuple(self.theme["container"]["heading"].keys())

        # Custom style for the tree view widget
        style = ttk.Style()
        style.configure("Treeview", background=self.theme["container"]["colors"]["background"])
        style.map("Treeview", background=[("selected", self.theme["container"]["colors"]["selected"])])
        style.configure("Treeview", foreground=self.theme["global"]["colors"]["button_text"])
        style.map("Treeview", foreground=[("selected", self.theme["container"]["colors"]["selected_text"])])

        # Creating the Tree view widget (table)
        self.tree = ttk.Treeview(frame, columns=self.columns, show="headings", height=25, style="Treeview")
        self.tree.grid(row=0, column=0, columnspan=TC, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.tree.bind('<<TreeviewSelect>>', self.on_treeview_selection)

        # Assign labels and widths to the tree view columns
        for col in self.columns:
            self.tree.heading(col, text=self.theme["container"]["heading"][col],anchor="center")#,anchor=self.theme["container"]["alignment"][col]
            self.tree.column(col, width=self.theme["container"]["column_width"][col],anchor=self.theme["container"]["alignment"][col])# stretch=tk.NO
        #end

        # Add the right-click binding
        self.tree.bind("<Button-3>", self.show_tree_popup_menu_callback)

        # Create the column visibility variables
        self.column_visible = {col: tk.BooleanVar(value=self.theme["container"]["column_visibility"][col]) for col in self.columns}

        # Load default visibility settings for columns from configuration
        for col in self.tree["columns"]:
            self.column_visible[col] = tk.BooleanVar(value=self.config.getboolean('ColumnsVisibility', col))
            self.toggle_column_visibility(col)# Update the columns
        #end

        # Column Sorting
        for col in self.columns:
            self.tree.heading(col, text=self.theme["container"]["heading"][col], command=lambda col=col: self.sort_column(col))
        #end
        self.sortColumn = ""
        self.sortDirection = ""

        # Vertical scrollbar column -----------------
        # Create a scrollbar for the tree view widget (table) :TODO make it automatic
        self.tree_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree_scrollbar.grid(row=0, column=TC, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=self.tree_scrollbar.set)

        return self.tree
    #end

    # ------ The basic get/set/add/remove interfacing methods with the container -------
    def get_all_items(self):
        return self.tree.get_children()
    #end

    def get_selection(self):
        return self.tree.selection()
    #end

    def add(self,item):
        self.tree.insert("", "end", values=item.as_tuple())
        

    def remove(self, items):
        self.tree.delete(items)
    #end

    def get_UiItmField(self, ui_item_id, field):
        return self.tree.set(ui_item_id, field)
    #end
    
    def set_UiItmField(self, ui_item_id, field, value):
        self.tree.set(ui_item_id, field, value)
    #end

    def get_UiItmField_byColInd(self, ui_item, col_index):
        return self.tree.item(ui_item)["values"][col_index]
    #end
        
# === Application Stage 4: Youtube Video table Info user manipulation ===
    # ------ Callbacks and companion functions for the tree view columns Context menu -------
    # Add a show popup menu method callback
    def show_tree_popup_menu_callback(self, event):
        # Get the height of the header
        header_height = abs(self.tree.winfo_height() - self.tree.winfo_reqheight())
        header_height = 25  # TODO: will be hardcoded for now!

        # Check if the click event is above the column labels
        if event.y < header_height:
            popup = tk.Menu(self, tearoff=0)

            for col in self.tree["columns"]:
                text = self.tree.heading(col)["text"]
                popup.add_checkbutton(label=text, variable=self.column_visible[col], command=lambda col=col: self.toggle_column_visibility(col))
            #end
        else:
            popup = self.show_container_item_context_menu()#NOTE:_EXTERNAL_METHOD_
        #end

        popup.tk_popup(event.x_root, event.y_root)
    #end

    # A method to toggle the column visibility
    def toggle_column_visibility(self, col):
        visibility = self.column_visible[col].get()

        if visibility:
            width_ = self.theme["container"]["column_width"][col]#NOTE:_EXTERNAL_METHOD_
            stretch_ = True
        else:
            width_ = 0
            stretch_ = False
        #end

        self.tree.column(col, width=width_, minwidth=0,stretch=stretch_)
    #end

    # Add a sort column method
    def sort_column(self, col):
        # Sorting variables
        sortDirections = ["asc", "desc"]
        symbol = ["▲", "▼"]

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
            self.tree.selection_add(item)
        #end
    #end

    def on_treeview_selection(self, event):
        selected_items = self.get_selection()
        total_items = len(self.get_all_items())

        if len(selected_items) == 1:
            item = selected_items[0]
            video_title = self.tree.item(item)["values"][2]
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
    #end

    def move_selection_down_callback(self, event=None):
        self.move_selection('down', event)
    #end

#end