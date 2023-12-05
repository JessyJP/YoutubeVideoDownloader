"""
File: main.py

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
## Import modules
import os
import sys
import threading
import subprocess
import shlex
# Core imports
from core.pytube_handler import LimitsAndPriority, VideoInfo
from core.video_list_manager import VideoListManager
from core.download_options import * # updateOutputKeepsStr, MediaSymbols # NOTE:imports the symbol list as well
from core.common import audio_bitrate_list as BitrateList, video_resolution_list as ResolutionList, fps_value_list as FPSList
# GUI imports
import tkinter as tk
from tkinter import ttk, filedialog
from gui.settings_window import SettingsWindow
# Other imports
from typing import Union
import json
import shutil
import pyperclip
import configparser
import inspect
# TODO: check the imports for redundancy or unused ones

# ---------------------------------------------------------------------------
# Refactor the item display container
class VideoItemDisplayContainer():

    def createVideoItemDisplayContainer(self, frame,TC):
        # Get tree view column headings
        self.columns = tuple(self.theme["tree_view"]["heading"].keys())

        # Custom style for the tree view widget
        style = ttk.Style()
        style.configure("Treeview", background=self.theme["tree_view"]["colors"]["background"])
        style.map("Treeview", background=[("selected", self.theme["tree_view"]["colors"]["selected"])])
        style.configure("Treeview", foreground=self.theme["global"]["colors"]["button_text"])
        style.map("Treeview", foreground=[("selected", self.theme["tree_view"]["colors"]["selected_text"])])

        # Creating the Tree view widget (table)
        self.tree = ttk.Treeview(frame, columns=self.columns, show="headings", height=25, style="Treeview")
        self.tree.grid(row=0, column=0, columnspan=TC, sticky=(tk.N, tk.S, tk.E, tk.W))
        self.tree.bind('<<TreeviewSelect>>', self.on_treeview_selection)

        # Assign labels and widths to the tree view columns
        for col in self.columns:
            self.tree.heading(col, text=self.theme["tree_view"]["heading"][col],anchor="center")#,anchor=self.theme["tree_view"]["alignment"][col]
            self.tree.column(col, width=self.theme["tree_view"]["column_width"][col],anchor=self.theme["tree_view"]["alignment"][col])# stretch=tk.NO
        #end

        # Add the right-click binding
        self.tree.bind("<Button-3>", self.show_tree_popup_menu_callback)

        # Create the column visibility variables
        self.column_visible = {col: tk.BooleanVar(value=self.theme["tree_view"]["column_visibility"][col]) for col in self.columns}

        # Load default visibility settings for columns from configuration
        for col in self.tree["columns"]:
            self.column_visible[col] = tk.BooleanVar(value=self.config.getboolean('ColumnsVisibility', col))
            self.toggle_column_visibility(col)# Update the columns
        #end

        # Column Sorting
        for col in self.columns:
            self.tree.heading(col, text=self.theme["tree_view"]["heading"][col], command=lambda col=col: self.sort_column(col))
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
            # Get the number of selected items
            selected_items_count = len(self.get_selection())

            # Create the popup menu
            popup = tk.Menu(self, tearoff=0)

            # Add the message about the selected items count
            popup.add_command(label=f"{selected_items_count} item(s) selected", state='disabled')
            popup.add_separator()

            if self.active_process_flag:
                _state="disabled"
            else:
                _state="normal"
            #end
            # Add download status options
            popup.add_command(label="Download Status: Pending "+COMBINED_SYMBOL, command=lambda: self.change_download_status(COMBINED_SYMBOL,"on"), state=_state)
            popup.add_command(label="Download Status: Skip ", command=lambda: self.change_download_status(COMBINED_SYMBOL,"off"), state=_state)
            popup.add_separator()
            popup.add_command(label="Keep Audio Only: Toggle Add/Remove "+AUDIO_ONLY_SYMBOL,  command=lambda: self.change_download_status(AUDIO_ONLY_SYMBOL), state=_state)
            popup.add_command(label="Keep Video Only: Toggle Add/Remove "+VIDEO_ONLY_SYMBOL,  command=lambda: self.change_download_status(VIDEO_ONLY_SYMBOL), state=_state)
            popup.add_command(label="Keep All Subtitles Only: Toggle Add/Remove "+SUBTITLES_ONLY_SYMBOL,  command=lambda: self.change_download_status(SUBTITLES_ONLY_SYMBOL), state=_state)
            popup.add_command(label="Keep Thumbnail:   Toggle Add/Remove "+THUMBNAIL_SYMBOL,   command=lambda: self.change_download_status(THUMBNAIL_SYMBOL), state=_state)
            popup.add_command(label="Keep Info:       Toggle Add/Remove "+INFO_SYMBOL,        command=lambda: self.change_download_status(INFO_SYMBOL), state=_state)
            popup.add_command(label="Keep Comments:   Toggle Add/Remove "+COMMENTS_SYMBOL,    command=lambda: self.change_download_status(COMMENTS_SYMBOL), state=_state)
            popup.add_command(label="Clear All Keeps",   command=lambda: self.change_download_status_clearall(), state=_state)
            popup.add_separator()
            popup.add_command(label="Remove Selected Entries",   command=lambda: self.remove_table_entry_selection(), state=_state)

            # Add a separator and the copy_selected_entries_to_text_callback section
            popup.add_separator()
            popup.add_command(label="Copy Selected Entries as text", command=self.copy_selected_entries_to_text_callback)
            popup.add_command(label=f"Play Preview {selected_items_count} item(s) in Local player", command=self.play_selected_watch_urls_locally)
            popup.add_command(label=f"Show preview selected thumbnails", command=self.open_selected_thumbnails_urls_locally)
        #end

        popup.tk_popup(event.x_root, event.y_root)
    #end

    # A method to toggle the column visibility
    def toggle_column_visibility(self, col):
        visibility = self.column_visible[col].get()

        if visibility:
            width_ = self.theme["tree_view"]["column_width"][col]#NOTE:_EXTERNAL_METHOD_
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
            self.tree.heading(self.sortColumn, text=self.theme["tree_view"]["heading"][self.sortColumn])#NOTE:_EXTERNAL_METHOD_
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
        heading_text = self.theme["tree_view"]["heading"][col]
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
# ---------------------------------------------------------------------------

## Main Application window
class YouTubeDownloaderGUI(tk.Tk, VideoListManager, VideoItemDisplayContainer):
# === Application Stage 1: Initialization functions ===

    # Class Constructor: Creates the application, loads theme and configuration also adds global keybindings
    def __init__(self):
        # Call parent constructor
        # super().__init__()
        # print(YouTubeDownloaderGUI.__mro__)

        tk.Tk.__init__(self)
        VideoListManager.__init__(self)

        # First Load configuration file 
        self.config_file = 'config.ini'
        self.load_config()

        # Do further configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Load the theme from the configuration file 
        self.load_theme()
        # Create the main window
        self.create_widgets()

        # Bind various key combinations
        self.bind_keys_from_config()

        # At the end also add main window closing callback
        self.protocol("WM_DELETE_WINDOW", self.close_application_window)

        # Flagging variable
        self.cancel_flag = False #TODO: check if this is needed in the download manager
        self.active_process_flag = False# TODO: maybe have to rename this flag to process_running flag instead

        # Some settings
        self.COLUMN_INDEX_URL = 1  # Assuming the URL is the 2nd -1 column in the tree view
        self.COLUMN_INDEX_VIDEO_ID = 10  # Assuming the video ID is the 11th -1 column in the tree view
    #end

    # Handle window closing
    def close_application_window(self):
        # Stop all threads before closing the window
        self.cancel_flag = True
        for thread in threading.enumerate():
            if thread is not threading.main_thread():
                pass
                # thread.terminate() #TODO: more work needed here
                # thread.join()
                # TODO: reevaluate the abrupt or normal shutdown procedure
            #end
        #end

        # Save configuration and close the window
        self.save_config()
        self.destroy()
    #end

    # Load configuration which is used to preserve and import configuration variables
    def load_config(self):
        if not self.config_file:
            raise ValueError("Configuration file not defined")
        #end

        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
    #end

    # Save the configuration file is used to preserve and import configuration variables
    def save_config(self):
        # Check if config has been loaded, otherwise create a new one with defaults
        if not hasattr(self, "config"):
            raise ValueError(f"Configuration file has not been loaded yet of there is a problem with the {self.config_file}!")
        #end

        # Save theme
        section = "General"
        theme_directory = self.config.get(section, 'theme_directory')
        self.config.set(section, 'theme_directory', theme_directory)
        self.config.set(section, 'theme', self.theme["filename"])
        self.config.set(section, "last_download_location",self.download_location_entry.get())
    
        # Save default and current settings
        section =  "DownloadSettings"
        options = ["audio_bitrate","video_bitrate","fps", 
                   "video_format_priority",
                   "audio_format_priority"]
        defaultValues = ["max","max","max",
                        "mp4, webm, flv, 3gp, m4a",
                        "wav, mp3, aac, m4a"]
        for option, value in zip(options, defaultValues):
            if not self.config.has_option(section, option):
                self.config.set(section, option, value)
            #end
        #end

        # Save column visibility settings
        for col, var in self.column_visible.items():
            self.config.set('ColumnsVisibility', col, str(var.get()))
        #end

        with open(self.config_file, 'w') as file:
            self.config.write(file)
        #end
    #end

    # Load theme
    def load_theme(self):
        theme_directory = self.config.get('General', 'theme_directory')
        theme_file = self.config.get('General', 'theme')
        language_file = self.config.get('General', 'language')
        
        # Load theme file
        with open(f"{theme_directory}/{theme_file}", "r") as file:
            theme = json.load(file)
        #end
        
        # Load language file
        with open(f"{theme_directory}/{language_file}", "r") as file:
            language = json.load(file)
        #end

        def merge_dict(d1, d2):
            for k, v in d1.items():
                if k in d2:
                    if isinstance(v, dict) and isinstance(d2[k], dict):
                        merge_dict(v, d2[k])
                    else:
                        d2[k] = v
                    #end
                else:
                    d2[k] = v
                #end
            #end
            return d2
        #end
        
        # Merge theme and language dictionaries
        self.theme = merge_dict(theme, language)
        
        # Add the filename to the theme dictionary
        self.theme["filename"] = theme_file

        application_window_icon_path = f"{self.theme['global']['directories']['icons']}{self.theme['icons']['application_window']}"
        if sys.platform != "win32":
            img = tk.PhotoImage(file=application_window_icon_path.replace(".ico", ".png"))
            self.tk.call('wm', 'iconphoto', self._w, img)
        else:
            self.iconbitmap(application_window_icon_path)
        #end

        self.title(self.theme["window_title"])
        self.configure(bg=self.theme["global"]["colors"]["background"])
        self.geometry(f"{self.theme['global']['window']['width']}x{self.theme['global']['window']['height']}")  
    #end

    # Bind keys according to the configuration file
    def bind_keys_from_config(self):
        # Check if config has been loaded
        if not hasattr(self, "config"):
            self.load_config()
        #end

        # Load key bindings from config file
        keybindings = self.config["KeyBindings"]
        for key, value in keybindings.items():
            if value:
                # Parse keybinding and command from config value
                callbackName, keybindingCombo = [val.strip() for val in value.split(":")]
                # Check if callbackName is a valid function name
                if not hasattr(self, callbackName.strip()):
                    raise AttributeError(f"{callbackName.strip()} is not a valid callback function name in {self.config_file}.")
                #end
                # Add key binding to application
                self.bind(keybindingCombo, getattr(self, callbackName))
            #end
        #end
    #end

    # Create the window and all widgets
    def create_widgets(self):
        window_padding = self.theme['global']['window']['padding']
        TC = 50;# Total number of columns

        # Create the window frame
        frame = ttk.Frame(self)
        frame.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W), padx=window_padding, pady=window_padding)

        # First row -----------------
        # Pre-initialize display container inherited fields that are used here and potentially in the sub-window(s)
        self.column_visible = {}
        self.dispTable = self.createVideoItemDisplayContainer(frame,TC)
        # Self-reference because instead of inheritance the container may be instantiated instead # TODO: check
        self.container = self

        # Second row -----------------
        # Add a label for the input text field
        url_label = ttk.Label(frame,  text=self.theme["texts"]["url_label"])
        url_label.grid(column=0, row=1, sticky=tk.W, pady=10)

        # Create an input text field
        self.url_entry = tk.Entry(frame)
        self.url_entry.grid(column=1, row=1,columnspan=TC-2, sticky=(tk.W, tk.E), padx=(0, 0), pady=10)
        self.url_entry.bind("<Button-3>", self.show_text_edit_context_menu)


        # Create buttons
        self.analyse_button = ttk.Button(frame, text=self.theme["texts"]["analyse_button"], command=self.process_input_text_callback)
        self.analyse_button.grid(column=TC-1, row=1, sticky=tk.E, padx=(0, 0))

        # Third row -----------------
        # Create settings button with a gear icon (existing code)
        icon_path = f"{self.theme['global']['directories']['icons']}{self.theme['icons']['settings_button']}"
        self.settings_icon = tk.PhotoImage(file=icon_path)
        self.settings_button = ttk.Button(frame, image=self.settings_icon)
        self.settings_button.grid(column=0, row=2, sticky=tk.W)

        # Create a play item selection locally button. This sends the items to the local video player.
        # NOTE: this currently works only with PotPlayer installed
        self.playSelectionLocal_button = ttk.Button(frame, text="   Play Preview \n Selection Locally",command=self.play_selected_watch_urls_locally)
        self.playSelectionLocal_button.grid(column=0, row=2, sticky=tk.W, padx=(45, 0))

        # Add dropdown boxes for quality limiters

        # self.download_limiter_label = ttk.Label(frame, text="Download limiters:")
        # self.download_limiter_label.grid(column=0, row=2, sticky=(tk.W, tk.E), padx=(60, 0))

        audio_bitrate_list = [self.config.get("DownloadSettings", "audio_bitrate")]+ BitrateList
        video_resolution_list = [self.config.get("DownloadSettings", "video_bitrate")] + ResolutionList
        fps_value_list = [self.config.get("DownloadSettings", "fps")] + FPSList

        self.dropdown_audio_limiter_selection = tk.StringVar(value=audio_bitrate_list[0])
        self.dropdown_video_limiter_selection = tk.StringVar(value=video_resolution_list[0])
        self.dropdown_fps_limiter_selection = tk.StringVar(value=fps_value_list[0])

        self.dropdown_audio_limiter = ttk.OptionMenu(frame, self.dropdown_audio_limiter_selection, *audio_bitrate_list)
        self.dropdown_video_limiter = ttk.OptionMenu(frame, self.dropdown_video_limiter_selection, *video_resolution_list)
        self.dropdown_fps_limiter = ttk.OptionMenu(frame, self.dropdown_fps_limiter_selection, *fps_value_list)

        self.dropdown_audio_limiter.grid(row=2, column=1, padx=(0, 0), pady=5, sticky="w")
        self.dropdown_video_limiter.grid(row=2, column=2, padx=(0, 0), pady=5, sticky="w")
        self.dropdown_fps_limiter.grid(row=2, column=3, padx=(0, 0), pady=5, sticky="w")
        # TODO:NOTE: on change callbacks could be implemented for the dropdowns. Thus updating the and correctly showing the actual download size. 

        # Create the "Select Download Location" button
        self.select_location_button = ttk.Button(frame, text=self.theme["texts"]["select_location_button"], command=self.open_select_location_dialog)
        self.select_location_button.grid(column=4, row=2, sticky=tk.W, padx=(0, 0))

        # Create the "Selected Download Location" text field
        self.download_location_entry = tk.Entry(frame)
        self.download_location_entry.grid(column=5, row=2,columnspan=TC-6, sticky=(tk.W, tk.E), padx=(0, 0))
        self.download_location_entry.insert(0, self.config.get("General", "last_download_location"))
        self.download_location_entry.bind("<Button-3>", self.show_text_edit_context_menu)

        # Bind the events to the button
        self.settings_button.bind("<Enter>", self.on_settings_button_hover)
        self.settings_button.bind("<Leave>", self.on_settings_button_leave)
        self.settings_button.bind("<Button-1>", self.on_settings_button_click)

        # Create the "Download" button
        self.download_button = ttk.Button(frame, text=self.theme["texts"]["download_button"], command=self.download_all_entries_callback)
        self.download_button.grid(column=TC-1, row=2, sticky=tk.E, padx=(0, 0))

        # Forth row -----------------
        # Create a progress bar widget
        self.progress_bar_msg = tk.StringVar()#TODO: may be redundant
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate",variable=self.progress_bar_msg)
        self.progress_bar.grid(column=0, row=3, columnspan=TC, sticky=(tk.W, tk.E))

        # Create the "Diagnostic out label" label and text field
        self.status_bar_label = ttk.Label(frame, text="")
        self.status_bar_label.grid(column=0, row=3, columnspan=TC, sticky=(tk.W, tk.E))

        # self.view_button = ttk.Button(self, text="Switch View", command=self.toggle_view)
        # self.view_button.grid(column=1, row=2, sticky=tk.E, padx=(0, 0))
        # TODO: experimental option to change the viewing table to a card based or alternative

        # Configure column and row weights
        for i in range(TC):
            frame.columnconfigure(i, weight=1)
        #end
        frame.rowconfigure(0, weight=1)
    #end

# === Application Stage 2: Settings & Configuration setup window functions & dialogs  ===
    # ------ Callbacks and companion functions configuration/settings window button  -------

    # Configuration window button Icon callbacks
    def on_settings_button_hover(self, event):
        icon_path = f"{self.theme['global']['directories']['icons']}{self.theme['icons']['settings_button_hover']}"
        hover_icon = tk.PhotoImage(file=icon_path)
        self.settings_button.config(image=hover_icon)
        self.settings_button.image = hover_icon
    #end

    def on_settings_button_leave(self, event):
        icon_path = f"{self.theme['global']['directories']['icons']}{self.theme['icons']['settings_button']}"
        normal_icon = tk.PhotoImage(file=icon_path)
        self.settings_button.config(image=normal_icon)
        self.settings_button.image = normal_icon
    #end

    def on_settings_button_click(self, event):
        if self.active_process_flag:
            return
        #end
        icon_path = f"{self.theme['global']['directories']['icons']}{self.theme['icons']['settings_button_click']}"
        click_icon = tk.PhotoImage(file=icon_path)
        self.settings_button.config(image=click_icon)
        self.settings_button.image = click_icon
        self.open_settings_window()
        self.save_config()  # Add this line to save the config when the settings button is clicked
    #end

    # Settings window behavior companion function for the callback
    def open_settings_window(self):
        if hasattr(self, "settings_window") and self.settings_window.winfo_exists():
            self.settings_window.destroy()
            del self.settings_window
        else:
            self.settings_window = SettingsWindow(self)
        #end
    #end

    # Add the function to open a dialog for location selection
    def open_select_location_dialog(self, event=None):
        download_location_here = filedialog.askdirectory()
        if download_location_here:
            self.download_location_entry.delete(0, tk.END)
            self.download_location_entry.insert(0, download_location_here)
            self.update_idletasks()
        #end
    #end

    # ------ Callback for handling hotkey press callbacks -------
    def number_key_context_menu_shortcut_callback(self, event):
        # Only use the shortcut key if no process is running
        if self.active_process_flag:
            return
        #end
        from functools import partial
        # Extract the key symbol (number) from the event
        pressed_number = event.keysym

        def dummy_case():
            pass
        #end
        def call_switch_case(switch_group, case):
            return switch_group.get(case, dummy_case)()
        #end

        # Check for modifier keys
        modifiers = ""
        switch_group = {}
        if event.state & 0x0001:  # Shift key
            modifiers += "Shift+"
        #end

        if event.state & 0x0004:  # Control key
            modifiers += "Ctrl+"
        #end

        if (event.state & 0x0008 or event.state & 0x0080 or 
            event.state & 0x20000 or event.state & 0x20004 ):  # Alt key (different codes on different systems)
            modifiers += "Alt+"
        #end

        if modifiers == '':  # No modifier case
            switch_group = {
                '1': partial(self.change_download_status, COMBINED_SYMBOL, "on"),
                '2': partial(self.change_download_status, COMBINED_SYMBOL, "off"),
                '3': partial(self.change_download_status, AUDIO_ONLY_SYMBOL),
                '4': partial(self.change_download_status, VIDEO_ONLY_SYMBOL),
                '5': partial(self.change_download_status, SUBTITLES_ONLY_SYMBOL),
                '6': partial(self.change_download_status, THUMBNAIL_SYMBOL),
                '7': partial(self.change_download_status, INFO_SYMBOL),
                '8': partial(self.change_download_status, COMMENTS_SYMBOL),
                '0': partial(self.change_download_status_clearall)
            }
        #end

        call_switch_case(switch_group,pressed_number)

        # def print_hex(value):
        #     hex_value = hex(value)
        #     print(f"The hexadecimal representation of {value} is: {hex_value}")
        # #end

        # print_hex(event.state)
        print(f"{modifiers}Number {pressed_number} pressed")
    #end

    def show_text_edit_context_menu(self, event):
        widget = event.widget
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label="Undo", command=lambda: widget.event_generate("<<Undo>>"))
        context_menu.add_command(label="Redo", command=lambda: widget.event_generate("<<Redo>>"))
        context_menu.add_separator()
        context_menu.add_command(label="Cut", command=lambda: widget.event_generate("<<Cut>>"))
        context_menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
        context_menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
        context_menu.add_separator()
        context_menu.add_command(label="Select All", command=lambda: widget.select_range(0, tk.END))
        context_menu.tk.call("tk_popup", context_menu, event.x_root, event.y_root)
    #end

    # --- get methods for the association between the GUI table and the info list

    def get_video_info_by_entry(self, ui_item_id) -> Union[VideoInfo, None]:
        # Get the video_id associated with the selected tree view container index
        video_id = self.container.get_UiItmField(ui_item_id, 'video_id')
        # Get the video item list index of the selected tree container item index
        item_container_index = self.dispTable.index(ui_item_id)

        # Use the getItemByIndexOrVideoID function to find the VideoInfo object
        video_info = self.getItemByIndexOrVideoID(video_id, item_container_index)

        return video_info
    #end

    def get_tree_view_UI_item_by_video_info(self, video_info: VideoInfo) -> Union[str, None]:
        # Check if the input video_info is valid
        if video_info is None:
            return None
        #end

        # Try to find the tree view UI item by index first
        index = self.getItemIndex(video_info)
        if index != -1:
            ui_item = self.container.get_all_items()[index]
            # Check if the video_id matches
            if self.container.get_UiItmField(ui_item, 'video_id') == video_info.video_id:
                return ui_item
            #end
        #end

        # If the index method fails or video_id doesn't match, search exhaustively
        for ui_item in self.container.get_all_items():
            if self.container.get_UiItmField(ui_item, 'video_id') == video_info.video_id:
                return ui_item
            #end
        #end

        # If no match is found, return None
        return None
    #end

    # ------ Callbacks and companion functions for the tree view rows operations Context menu or Key Bindings -------
    def updateTreeViewFromVideoInfoTable(self):
        # Clear the tree view
        self.container.remove(*self.container.get_all_items())

        # Re-insert all entries from the table
        for videoInfoItem in self.getVideoList():
            self.container.add(videoInfoItem)
        #end
    #end

    def remove_table_entry_selection(self, event=None):
        if self.active_process_flag:
            return
        #end
        selected_items = self.container.get_selection()

        for sel_id in selected_items:
            # Find the corresponding VideoInfo object
            video_info = self.get_video_info_by_entry(sel_id)

            if video_info is not None:
                self.removeItem(video_info)
            else:
                raise ValueError("VideoInfo not found for the selected tree view item!")
            #end
        #end

        for sel_id in selected_items:
            self.container.remove(sel_id)
        #end
    #end

    def change_download_status(self, symbol, state="toggle"):
        selected_items = self.container.get_selection()

        for ui_item in selected_items:
            new_status = updateOutputKeepsStr(self.container.get_UiItmField(ui_item, 'download_status'), symbol, state)

            # Find the corresponding VideoInfo object (handle) and update its download state
            video_info = self.get_video_info_by_entry(ui_item)
            if video_info is None:
                raise(f"Error: VideoInfo object not found for UI item '{ui_item}'")
            #end

            # Update download state of the video info in the handle table entry 
            video_info.download_status = new_status

            # Update the download status of the selected UI item in the tree view
            self.container.set_UiItmField(ui_item, 'download_status', new_status)
        #end
    #end

    def change_download_status_clearall(self):
        selected_items = self.container.get_selection()
        symbol_list = MediaSymbols.get_all_symbol_values_as_list()
        state = "off"

        for ui_item in selected_items:
            for symbol in symbol_list:
                new_status = updateOutputKeepsStr(self.container.get_UiItmField(ui_item, 'download_status'), symbol, state)

                # Find the corresponding VideoInfo object (handle) and update its download state
                video_info = self.get_video_info_by_entry(ui_item)
                if video_info is None:
                    raise(f"Error: VideoInfo object not found for UI item '{ui_item}'")
                #end

                # Update download state of the video info in the handle table entry 
                video_info.download_status = new_status

                # Update the download status of the selected UI item in the tree view
                self.container.set_UiItmField(ui_item, 'download_status', new_status)
            #end
        #end
    #end


    def copy_selected_entries_to_text_callback(self, event=None):
        selected_items = self.tree.selection()
        text_to_copy = []

        # Get the list of visible columns
        visible_columns = [col for col in self.tree["columns"] if self.tree.column(col, "width") > 0]

        for item in selected_items:
            item_values = self.tree.item(item)['values']
            visible_item_values = [str(item_values[i]) for i, col in enumerate(self.tree["columns"]) if col in visible_columns]
            item_text = "\t".join(visible_item_values)
            text_to_copy.append(item_text)
        #end

        if text_to_copy:
            text_to_copy = "\n".join(text_to_copy)
            pyperclip.copy(text_to_copy)
        #end
    #end

    # ------ Callback for calling external player to open the selected watch URLs -------
    def play_selected_watch_urls_locally(self, event=None) -> None:
        # Get the currently selected items
        selected_items = self.container.get_selection()

        # Get the list of watch URLs from the selected items
        watch_urls = [self.get_video_info_by_entry(item).watch_url for item in selected_items]

        # Get the external player filepath from the ini file
        external_player = self.config.get("General", "playback_player")

        # Ensure the watch URLs are properly quoted for shell execution
        quoted_urls = [shlex.quote(url) for url in watch_urls]

        # Combine all the watch URLs into a single command
        command = f"{external_player} {'  '.join(watch_urls)}"

        # Call the external process with the command
        subprocess.Popen(command, shell=True)
    #end

    def open_selected_thumbnails_urls_locally(self, event=None) -> None:
        # Get the currently selected items
        selected_items = self.container.get_selection()

        # Get the list of watch URLs from the selected items
        thumbnail_url = [self.get_video_info_by_entry(item).thumbnail_url for item in selected_items]

        # Get the external player filepath from the ini file
        external_player = self.config.get("General", "playback_player")

        # Ensure the watch URLs are properly quoted for shell execution
        quoted_urls = [shlex.quote(url) for url in thumbnail_url]

        # Combine all the watch URLs into a single command
        command = f"{external_player} {'  '.join(thumbnail_url)}"

        # Call the external process with the command
        subprocess.Popen(command, shell=True)
    #end

# === Application Stage 3: Youtube URL Video Input functions ===
    # ------ Callbacks and companion functions for URL insertion and analysis  -------

    # User Actions Callbacks
    def paste_input_text_callback(self, event):
        clipboard_data = self.clipboard_get()
        self.import_youtube_videos_threaded(clipboard_data)
    #end

    def process_input_text_callback(self, event=None):
        input_text = self.url_entry.get()
        self.import_youtube_videos_threaded(input_text)
        self.url_entry.delete(0, tk.END)
    #end

    # Intermediate method to run the import operation in a separate thread
    def import_youtube_videos_threaded(self, text):
        if self.active_process_flag == False:
            # Reset just in case
            self.reset_cancel_flag()  
            # Disable the download button if it's not already disabled
            # TODO: overall the disable/enable configuration should be rechecked and tested for consistency
            self.download_button.config(state='disabled')# TODO: may be redundant here.
            self.disable_UI_elements_during_download()# TODO: this is for download but also works, but will give incorrect label, i.e. "cancel download"
            # Get the threading mode flag
            use_analysis_multithreading = self.config.getboolean("General", "multithread_analyse_procedure")
            # Make and start an analysis thread
            t = threading.Thread(target=self.import_valid_Youtube_videos_from_textOrURL_list, args=(text, use_analysis_multithreading))
            t.start()
        #end
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def import_valid_Youtube_videos_from_textOrURL_list(self, text, use_analysis_multithreading, recursiveCheckOfURLcontent_mode=0):
        VideoListManager.import_valid_Youtube_videos_from_textOrURL_list(self, text, use_analysis_multithreading, recursiveCheckOfURLcontent_mode)
        # To finish up, enable the UIelements after the analysis
        if recursiveCheckOfURLcontent_mode == 0:  # This checks the recursion mode
            # Enable any ui elements
            self.download_button.config(state='normal')# TODO: if this is removed from this class and only implemented in the child
            self.enable_UI_elements_after_download()
        #end
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def process_url(self, url, use_analysis_multithreading, recursiveCheckOfURLcontent_mode):
        # Add this an interrupt that can be activated from the gui
        if self.cancel_flag:
            self.download_button.config(state='normal')
            return
        #end
        
        # Call the parent after checking the interrupt
        VideoListManager.process_url(self, url, use_analysis_multithreading, recursiveCheckOfURLcontent_mode)
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    # Get the current URLs in the tree view and video IDs
    def getURL_videoIDList(self):# TODO it's best to extract that from the self.getVideoList()
        current_url_entries = set()
        current_video_ids = set()
        for ui_item in self.container.get_all_items():  # Update the urls and the entries
            current_url_entries.add(self.container.get_UiItmField_byColInd(ui_item,self.COLUMN_INDEX_URL))
            current_video_ids.add(self.container.get_UiItmField_byColInd(ui_item,self.COLUMN_INDEX_VIDEO_ID))
        #end
        return current_url_entries, current_video_ids
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def addItem(self, video_info_item):
        super().addItem(video_info_item)
        self.container.add(video_info_item)
        # # Add the URL and video ID to the current_url_entries and current_video_ids sets
        # current_url_entries.add(video_info_item.watch_url) # NOTE: effective placeholder because it's not inserted or  returned
        # current_video_ids.add(video_info_item.video_id) # NOTE: effective placeholder because it's not inserted or  returned
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def remove_duplicate_items(self):
        super().remove_duplicate_items()
        # Get the current video IDs in the tree view
        current_video_ids = set()
        for item in self.container.get_all_items():
            current_video_ids.add(self.container.get_UiItmField_byColInd(item, self.COLUMN_INDEX_VIDEO_ID))
        #end
        
        # Check each row in the tree view and remove duplicates
        for item in self.container.get_all_items():
            video_id = self.container.get_UiItmField_byColInd(item,self.COLUMN_INDEX_VIDEO_ID)
            if video_id in current_video_ids:
                current_video_ids.remove(video_id)
            else:
                self.container.remove(item)
            #end
        #end
    #end

# === Application Stage 5: Youtube URL Video Download functions ===
    # ------ Callbacks and companion functions for Download, location and properties handling   -------

    def get_download_location(self):
        outputdir = os.path.abspath( self.download_location_entry.get() )
        if not os.path.isdir(outputdir):
            self.open_select_location_dialog()
            outputdir = os.path.abspath( self.download_location_entry.get() )
            if outputdir == "":
                self.setUiDispStatus("Please select download location!")
                return None
            #end
            if not os.path.isdir(outputdir):
                self.setUiDispStatus("Invalid download location! Please select a valid download location!")
                return None        
            #end
        #end
        return outputdir
    #end

    def getLimitsAndPriorityFromUI(self):
        limits_and_priority = LimitsAndPriority()

        # Get the audio bitrate
        limits_and_priority.bitrate = self.dropdown_audio_limiter_selection.get().replace("kbps","").strip()
        # Parse audio format priority into a list
        audio_format_priority_str = self.config.get("DownloadSettings", "audio_format_priority")
        limits_and_priority.audio_format_priority = [format.strip() for format in audio_format_priority_str.split(",")]

        # Get video resolution 
        limits_and_priority.resolution = self.dropdown_video_limiter_selection.get().replace("p","").strip()
        # Get video fps
        limits_and_priority.fps = self.dropdown_fps_limiter_selection.get().replace("fps","").strip()
        # Parse video format priority into a list
        video_format_priority_str = self.config.get("DownloadSettings", "video_format_priority")
        limits_and_priority.video_format_priority = [format.strip() for format in video_format_priority_str.split(",")]
        
        limits_and_priority.to_numeric()
        return limits_and_priority
    #end

    def download_all_entries_callback(self):
        if self.active_process_flag == False:
            t = threading.Thread(target=self.download_all_entries_thread, args=())
            t.start()
        else:
            # If a second time is pressed the cancel flag should be called 
            # Assume the text label has been changed
            self.cancel_operation_flagON()
        #end
    #end

    def download_all_entries_thread(self):
        # Disable relevant UI elements during download
        self.disable_UI_elements_during_download()

        # Get valid download location
        outputDir = self.get_download_location()
        if outputDir is None:
            # Re-enable relevant UI elements after download
            self.enable_UI_elements_after_download()
            return
        #end

        # Get Limits
        limits = self.getLimitsAndPriorityFromUI()

        # Get output extension
        outputExt = self.config.get("General", "output_file_ext")

        # Get the process threading run configuration
        process_via_multithreading = self.config.getboolean("General", "multithread_download_procedure")

        # Call the download manager processing function with all arguments
        self.downloadAllVideoItems( process_via_multithreading, limits, outputDir, outputExt)

        # Re-enable relevant UI elements after download
        self.enable_UI_elements_after_download()
    #end

# === Application Stage ANY: Functions to handle long operation states, status and diagnostic information ===
    # ------ Procedural Functions & Callbacks for extended processes  -------
    # With time consuming procedures such as analysis and download,
    # there is need to regulate the UI behavior as well as provide the ability
    # to update status & progress as well as cancel the procedure

    # Set/get pair functions for diagnostic output in above the progress bar
    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def getUiDispStatus(self):
        return self.status_bar_label.cget("text")
    #end
    
    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def setUiDispStatus(self, msg: str = ""):# TODO: funcCall may be obsolete in the future
        self.status_bar_label.config(text=msg)
        self.progress_bar_msg.set(msg)# TODO: may be redundant 
        self.update_idletasks();# Update the GUI
        self.container.update_idletasks();#NOTE: Update the GUI with a specific for the implementation method
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def update_progressbar(self, index_in: int, total_in :int, task_level):
        # Call the parent to compute the progress value
        progressValue = super().update_progressbar(index_in, total_in, task_level)
        # Assign the value
        self.progress_bar["value"]  = progressValue

        # TODO: a bit redundant
        self.progress_bar.update()  # Refresh the window to show the progress
        self.progress_bar.update_idletasks()  # Refresh the window to show the progress
        self.update()  # Refresh the window to show the progress
    #end

    # NOTE: @OVERWRITE This function overwrites/overrides the parent implementation
    def updateVideoItemUIDownloadState(self, videoItem,  download_status=None):        
        # Get the associated item
        ui_item = self.get_tree_view_UI_item_by_video_info(videoItem)
        # Update the download status. Sometimes the download status contains download flags.
        # Therefore, in some situations the download status is updated only for the UI. 
        if download_status is None:
            self.container.set_UiItmField(ui_item, 'download_status', videoItem.download_status)
        else:
            self.container.set_UiItmField(ui_item, 'download_status', download_status)

        # Also update the global download progress
        self.update_download_progress()
    #end

    def cancel_operation_flagON(self, event=None):
        self.cancel_flag = True
        msg = "Cancel the currently running operation!";
        self.setUiDispStatus(msg)
    #end

    def reset_cancel_flag(self):
        self.cancel_flag = False
    #end

    def disable_UI_elements_during_download(self):
        self.active_process_flag = True
        self.update_progressbar(0,len(self.getVideoList()),0)
        self.setUiDispStatus(f"Starting Download of {len(self.getVideoList())} item(s) now!")

        # Disable the input URL text field
        self.url_entry.config(state='disabled')

        # Disable the analyze button
        self.analyse_button.config(state='disabled')

        # Disable the select download location button
        self.select_location_button.config(state='disabled')

        # Disable the download location text field
        self.download_location_entry.config(state='disabled')

        # Disable the limiter dropdowns
        self.dropdown_audio_limiter.config(state='disabled')
        self.dropdown_video_limiter.config(state='disabled')
        self.dropdown_fps_limiter.config(state='disabled')

        # Disable the settings button
        self.settings_button.config(state='disabled')

        # Change the download button text to cancel
        self.download_button.config(text=self.theme["texts"]["download_cancel_button"])
        #TODO:NOTE: maybe it would be good for this pair of functions to be more general and have a 3rd button that will be the cancel button
        # ... this way the cancel, analysis and download button will always have easy and predictable enable/disable switching pattern 
    #end

    def enable_UI_elements_after_download(self):
        self.active_process_flag = False
        self.reset_cancel_flag()

        # Enable the input URL text field
        self.url_entry.config(state='normal')

        # Enable the analyze button
        self.analyse_button.config(state='normal')

        # Enable the select download location button
        self.select_location_button.config(state='normal')

        # Enable the download location text field
        self.download_location_entry.config(state='normal')

        # Enable the limiter dropdowns
        self.dropdown_audio_limiter.config(state='normal')
        self.dropdown_video_limiter.config(state='normal')
        self.dropdown_fps_limiter.config(state='normal')

        # Enable the settings button
        self.settings_button.config(state='normal')

        # Revert the download button text to the original
        self.download_button.config(text=self.theme["texts"]["download_button"])
    #end

#end:class

def main_runGUI():
    app = YouTubeDownloaderGUI()
    app.mainloop()
#end

# === Application run Main window GUI  ===
if __name__ == "__main__":
    main_runGUI()
#end