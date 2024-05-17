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
from usb_microscope_capture import ImageCapturingExperiment
from usb_microscope_capture.camera_devices  import CameraFactory
#%%

class Model:
    """class to hold the MVC model
    """    
    _tkapp_dir = None
    camera = None
    experiment = None
    _camera_factory = CameraFactory()  # TODO Make this available to view

    def __init__(self, starting_dir:pathlib.Path ): # image_data_dir=pathlib.Path("captured_images")):
        self._tkapp_dir = starting_dir

    def set_camera(self, camera_id:int, camera_model:str , camera_width:int=640, camera_height:int=480):
        try:
            self.camera.release()
        except:
            pass
        # TODO select the correct camera
        self.camera = self._camera_factory.create_camera(camera_type=camera_model)(id=camera_id, width=camera_width, height=camera_height)
        logging.info("Setting width: {camera_width} px")
        logging.info("Setting height: {camera_heigjt} px")
        # self.camera.initialise()

    def set_Experiment(self, camera_id:int, camera_model:str , camera_width:int=640, camera_height:int=480, delay_ms=500, num_images=150, image_data_dir='.'):
        self.set_camera(camera_id=camera_id, camera_model= camera_model, camera_width=camera_width, camera_height=camera_height)
        self.experiment = ImageCapturingExperiment(self.camera, delay_ms, num_images, image_folder=image_data_dir)


