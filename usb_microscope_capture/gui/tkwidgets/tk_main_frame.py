"""
View of usb microscope
"""

import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

from usb_microscope_capture.camera_devices.camera_factory import CameraFactory 
from .tk_frame_camera_type import tkFrameCameraType
from .tk_camera_settings import TkFrameCameraSettings


import logging
logging.basicConfig(level=logging.DEBUG)


class TkMainFrame(tk.Frame):
    _data_directory = None
    _camera_factory = CameraFactory()
    
    def __init__(self, master, starting_dir, **kwargs):
        super().__init__(master, **kwargs)
        self._tk_app_dir = starting_dir
        
        self.create_widgets()
        
        # Make the main frame expandable
        self.grid_columnconfigure(0, weight=4)
        self.grid_columnconfigure(1, weight=1)

    def create_widgets(self):
        # =================== camera Setting Labeled Frame frame
        tkLF_camera_frame = tk.LabelFrame(self, text="Camera Parameters")
                # Configure the camera frame to expand proportionally
        tkLF_camera_frame.grid_columnconfigure(0, weight=4)
        tkLF_camera_frame.grid_columnconfigure(1, weight=1)
        tkLF_camera_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self._tkeCamID = self._create_labeled_entry(tkLF_camera_frame, "Camera ID", 0, 0, "0")
        
        # =================== Camera type frame
        self._tkf_camera_type = tkFrameCameraType(tkLF_camera_frame)
        self._tkf_camera_type.set_camera_factory(self._camera_factory)
        self._tkf_camera_type.set_camera_options(self._camera_factory.get_camera_types())
        self._tkf_camera_type.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # =================== experiment frame
        experiment_frame = tk.LabelFrame(self, text="Experiment Parameters")
        experiment_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        experiment_frame.grid_columnconfigure(0, weight=4)
        experiment_frame.grid_columnconfigure(1, weight=1)

        self.folder_label = tk.Label(experiment_frame, text="Data Folder")
        self.folder_label.grid(row=0, column=0, sticky="w")

        self.browse_button = tk.Button(experiment_frame, text='Browse', command=self.browse_directory)
        self.browse_button.grid(row=0, column=1, sticky="e")

        self._tkeDelay_ms = self._create_labeled_entry(experiment_frame, "Delay [ms]", 1, 0, "500")
        self._tkeNmaxImages = self._create_labeled_entry(experiment_frame, "Num of images", 2, 0, "120")
        
        # =================== Camera settings frame
        self.camera_settings_frame = TkFrameCameraSettings(experiment_frame)
        self.camera_settings_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # =================== action frame
        action_frame = tk.LabelFrame(self, text="Actions and State")
        action_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.start_button = tk.Button(action_frame, text='Start Experiment', font='bold')
        self.start_button.grid(row=0, column=0, sticky="ew")

        self.stop_button = tk.Button(action_frame, text='Stop Experiment')
        self.stop_button.grid(row=0, column=1, sticky="ew")

        self.toggle_button = tk.Button(action_frame, text='Toggle Image Window')
        self.toggle_button.grid(row=1, column=0, columnspan=2, sticky="ew")

        self.status_indicator = tk.Canvas(action_frame, width=20, height=20)
        self.status_indicator.grid(row=2, column=0, sticky="w")
        self.status_indicator.create_oval(2, 2, 18, 18, fill="red")

        self.status_label = tk.Label(action_frame, text="Not running")
        self.status_label.grid(row=2, column=1, sticky="e")

        self.toggle_setup_capture_button = tk.Button(action_frame, text='Toggle Image Capture for Setup')
        self.toggle_setup_capture_button.grid(row=3, column=0, columnspan=2, sticky="ew")
        
        # ============== Set callbacks
        self._tkf_camera_type.set_roi_callback(self.camera_settings_frame.update_settings_upon_device_change)
        self._tkf_camera_type._on_camera_selection_change()
        
    def get_camera_parameters(self) -> dict:
        """Extracts the camera parameters from the Entry fields and returns them as a dictionary.

        Returns:
            dict: A dictionary where the keys are the parameter names and the values are the parameter values.
        """
        cam_id = int(self._tkeCamID.get())
        cam_width = int(self._tkf_camera_type.get_max_width())
        cam_height = int(self._tkf_camera_type.get_max_height())
        cam_model = self._tkf_camera_type.camera_type 

        return {"cam.id": cam_id, "cam.model":cam_model, "cam.width": cam_width, "cam.height": cam_height}
    
    def get_experiment_parameters(self):
        if not self._data_directory:
            if messagebox.askokcancel("Data Directory Not Set",
                                      "The data directory has not been initialised. "
                                      "Please select a directory to store the images."):
                self.browse_directory()  # prompt the user to select a folder
            else:
                self._data_directory = self._tk_app_dir / "captured_images/"
                self._data_directory.mkdir(parents=True, exist_ok=True)
                # self.folder_label["text"] = str(self._data_directory)

        return {
            "data_folder": self._data_directory,
            "delay_ms": int(self._tkeDelay_ms.get()),
            "no_images": int(self._tkeNmaxImages.get()),
            "roi": self.camera_settings_frame.get_roi(),
            "exposure": self.camera_settings_frame.get_exposure(),
            "gain": self.camera_settings_frame.get_gain()
        }
    
    def set_running_status(self, running_flag:bool)->None:
        """Changes the color of the status indicator and label text based on the running status of the experiment.
    
        This method changes the color of the status indicator to green if the experiment is running, 
        and to red if it's not running. The text of the label is changed accordingly to "Running" or "Not running".

        Args:
            running_flag (bool): Flag indicating whether the experiment is currently running. 
                                If True, the experiment is running; otherwise, it's not running.

        Returns:
            None
        """
        if running_flag:
            self.status_indicator.itemconfig(1, fill="green")
            self.status_label.config(text="Running")
        else:
            self.status_indicator.itemconfig(1, fill="red")
            self.status_label.config(text="Not running")

    def _create_labeled_entry(self, master, label_text, row, col, default_value):
        """auxilliary function that automated Label, entry process

        Args:
            master (_type_): parent widget
            label_text (_type_): label text
            row (_type_): row on grid layout
            col (_type_): col on grid layout
            default_value (_type_): Initial value 

        Returns:
            tk.Entry: The created object
        """        
        label = tk.Label(master, text=label_text)
        label.grid(row=row, column=col,sticky="nsew")

        entry = tk.Entry(master)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1,sticky="nsew")
        return entry

    def browse_directory(self):
        self._data_directory = pathlib.Path(filedialog.askdirectory(initialdir=self._tk_app_dir))
        # self.folder_label.configure(text=self._data_directory)
