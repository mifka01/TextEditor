import tkinter as tk
from tkinter import ttk
import os


class FileButton(ttk.Button):
    def __init__(self, app, raw_file):
        displayed_name = os.path.basename(raw_file.name)
        super().__init__(
            app.button_frame,
            style="File.TButton",
            text=displayed_name,
            command=lambda: app.switch_tabs(raw_file)
        )
        self.raw_file = raw_file
        self.pack(side=tk.LEFT, fill=tk.Y)
        self.config(width=len(displayed_name))
        self.bind(
            '<Button-2>',  # Right click for Mac / Wheel click for Windows
            lambda event: app.close_file(self.raw_file)
        )
