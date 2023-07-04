#%%
import pathlib
import time
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

import logging
logging.basicConfig(level=logging.DEBUG)
# Assuming the Camera and ImageCapturingExperiment classes are defined elsewhere
from usb_microscope_capture import Camera, ImageCapturingExperiment
#%%

class Model:
    """class to hold the MVC model
    """    
    _tkapp_dir = None
    camera = None
    experiment = None
    def __init__(self, starting_dir:pathlib.Path ): # image_data_dir=pathlib.Path("captured_images")):
        self._tkapp_dir = starting_dir

    def set_camera(self, camera_id:int, camera_width:int=640, camera_height:int=480):
        try:
            self.camera.release()
        except:
            pass
        self.camera = Camera(id=camera_id, width=camera_width, height=camera_height)
        # self.camera.initialise()

    def set_Experiment(self, camera_id:int, camera_width:int=640, camera_height:int=480, delay_ms=500, num_images=150, image_data_dir='.'):
        self.set_camera(camera_id=camera_id, camera_width=camera_width, camera_height=camera_height)
        self.experiment = ImageCapturingExperiment(self.camera, delay_ms, num_images, image_folder=image_data_dir)


