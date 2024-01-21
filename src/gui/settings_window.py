"""
YouTube Video Downloader
Copyright (C) 2023 JessyJP

Author: JessyJP
Year: 2024
Description: This is a python source script part of the YouTube Video Downloader Suit.

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
from tkinter import ttk
from configparser import ConfigParser

class SettingsWindow(tk.Toplevel):
    def __init__(self, master=None, config_file="config.ini"):
        super().__init__(master)
        self.master = master  # The master is the main window
        self.title("Settings")
        self.geometry("600x400")
        self.config_file = config_file
        self.load_config(self.config_file)
        self.create_widgets()
        self.bind("<Escape>", self.close)

    def load_config(self, config_file: str) -> None:
        self.config = ConfigParser()
        self.config.read(config_file)

    def save_config(self) -> None:
        # Save the modified settings to the ini file
        with open(self.config_file, "w") as configfile:
            self.config.write(configfile)

    def create_general_panel(self, parent) -> None:
        general_frame = ttk.Frame(parent)
        parent.add(general_frame, text="General")

        # Create widgets for the "General" panel
        theme_directory_label = ttk.Label(general_frame, text="Theme Directory:")
        theme_directory_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        theme_directory_entry = ttk.Entry(general_frame)
        theme_directory_entry.insert(0, self.config.get("General", "theme_directory"))
        theme_directory_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add more widgets for other entries in the General section

    def create_download_settings_panel(self, parent) -> None:
        download_settings_frame = ttk.Frame(parent)
        parent.add(download_settings_frame, text="Download Settings")

        # Create widgets for the "DownloadSettings" panel
        audio_bitrate_label = ttk.Label(download_settings_frame, text="Audio Bitrate:")
        audio_bitrate_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        audio_bitrate_entry = ttk.Entry(download_settings_frame)
        audio_bitrate_entry.insert(0, self.config.get("DownloadSettings", "audio_bitrate"))
        audio_bitrate_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add more widgets for other entries in the DownloadSettings section

    def create_key_bindings_panel(self, parent) -> None:
        key_bindings_frame = ttk.Frame(parent)
        parent.add(key_bindings_frame, text="Key Bindings")

        # Create widgets for the "KeyBindings" panel
        # Iterate over the key bindings in the ini file
        for index, key_binding in enumerate(self.config.options("KeyBindings")):
            key_binding_label = ttk.Label(key_bindings_frame, text=f"{key_binding}:")
            key_binding_label.grid(row=index, column=0, sticky=tk.W, padx=10, pady=10)
            key_binding_entry = ttk.Entry(key_bindings_frame)
            key_binding_entry.insert(0, self.config.get("KeyBindings", key_binding))
            key_binding_entry.grid(row=index, column=1, padx=10, pady=10)

    def create_columns_visibility_panel(self, parent) -> None:
        columns_visibility_frame = ttk.Frame(parent)
        parent.add(columns_visibility_frame, text="Columns Visibility")

        # Create widgets for the "ColumnsVisibility" panel
        # Iterate over the column visibility settings in the ini file
        for index, column in enumerate(self.config.options("ColumnsVisibility")):
            column_visibility_label = ttk.Label(columns_visibility_frame, text=f"{column}:")
            column_visibility_label.grid(row=index, column=0, sticky=tk.W, padx=10, pady=10)
            column_visibility_var = tk.BooleanVar()
            column_visibility_var.set(self.config.getboolean("ColumnsVisibility", column))
            column_visibility_checkbox = ttk.Checkbutton(columns_visibility_frame, variable=column_visibility_var)
            column_visibility_checkbox.grid(row=index, column=1, padx=10, pady=10)

    def create_help_panel(self, parent) -> None:
        help_frame = ttk.Frame(parent)
        parent.add(help_frame, text="Help")

        # Create the "About" section
        about_label = ttk.Label(help_frame, text="About")
        about_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

        about_text = tk.Text(help_frame, height=5, width=60, state=tk.DISABLED)
        about_text.insert(tk.END, "This is a settings window for a Python application.\n")
        about_text.insert(tk.END, "Version: 1.0\n")
        about_text.insert(tk.END, "Author: Your Name\n")
        about_text.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Create the "Help" section
        help_label = ttk.Label(help_frame, text="Help")
        help_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

        help_text = tk.Text(help_frame, height=10, width=60, state=tk.DISABLED)
        help_text.insert(tk.END, "TODO:Help will be implemented later")
        help_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def validate_input(self) -> bool:
        # TODO:Validate input values in each panel
        pass

    def display_error_message(self, message: str) -> None:
        # TODO:Display an error message if there are issues with input values
        pass

    def create_widgets(self):
        # Create a Notebook widget for managing the tabs
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill=tk.BOTH)

        # Create and display panels for each section of the ini file
        self.create_general_panel(notebook)
        self.create_download_settings_panel(notebook)
        self.create_key_bindings_panel(notebook)
        self.create_columns_visibility_panel(notebook)
        self.create_help_panel(notebook)

        # Create the "Save" button
        save_button = ttk.Button(self, text="Save", command=self.save_config)
        save_button.pack(side=tk.BOTTOM, pady=10)

    def close(self, event=None):
        self.destroy()
