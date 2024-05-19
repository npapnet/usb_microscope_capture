"""
View of usb microscope
"""

import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from usb_microscope_capture.gui.tkwidgets.tk_main_frame import TkMainFrame
from usb_microscope_capture.gui.tkwidgets.tktl_image_window import TKTLImageWindow

import logging
logging.basicConfig(level=logging.DEBUG)



class View:
    _tk_app_dir = None
    def __init__(self, master, starting_dir:pathlib.Path):
        self.master = master
        self._tk_app_dir = starting_dir

        self.master.attributes('-topmost', 1)  # keep the master window always on top
        self.create_view_widgets()
        
        # after initialisation of object set geometry of window (obsolete)
        self.master.after(1,self._set_image_window_init_position) # see comments

    def create_view_widgets(self):
        # initialise the main frame
        self.tkf_mainFrame = TkMainFrame(self.master, starting_dir=self._tk_app_dir)
        self.tkf_mainFrame.pack(fill=tk.BOTH, expand=True)

        # initialise the image window
        self.tkTL_image_window = TKTLImageWindow(self.master)
        # give access to the canvas of the image winodw
        self.image_canvas = self.tkTL_image_window.get_canvas()

    def _set_image_window_init_position(self):
        """auxilliary function because initialisation 
        
        this is run only once during the lifetime of the object. 
        I could also do it with a lambda fucntion
        This is not necessary after setting master as topmost.
        """        
        x = self.master.winfo_x() + self.master.winfo_width()
        y = self.master.winfo_y()
        # Set the position of the image window
        self.tkTL_image_window.geometry(f"+{x}+{y}")

    def toggle_image_window(self):
        if self.tkTL_image_window.winfo_viewable():
            self.tkTL_image_window.withdraw()
        else:
            self.tkTL_image_window.deiconify()

    def update_image(self, image_frame):
        # Convert the image frame to a format suitable for Tkinter
        image = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        # If there isn't an image on the canvas yet, create one
        if not hasattr(self, 'image_on_canvas'):
            self.image_on_canvas = self.image_canvas.create_image(0, 0, image=image, anchor='nw')
        # Otherwise, update the existing image
        else:
            self.image_canvas.itemconfig(self.image_on_canvas, image=image)

        # Keep a reference to the image object to prevent it from being garbage collected
        self.current_image = image
        self.tkTL_image_window.update_idletasks()

    def get_roi(self)->list:
        return self.tkf_mainFrame._tkf_roi_settings.get_roi()


