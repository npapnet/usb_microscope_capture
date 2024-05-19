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
from usb_microscope_capture.camera_devices  import CameraFactory, AbstractCamera
from usb_microscope_capture.gui.observer import Observer

class Model:
    """class to hold the MVC model
    """
    _tkapp_dir: pathlib.Path = None  # application dir
    camera: AbstractCamera = None    # camera object
    experiment: ImageCapturingExperiment = None
    _camera_factory: CameraFactory = CameraFactory()  # TODO Make this available to view
    _observers = []

    def __init__(self, starting_dir: pathlib.Path):  # image_data_dir=pathlib.Path("captured_images")):
        self._tkapp_dir = starting_dir

    def set_camera(self, camera_id: int, camera_model: str, camera_width: int = 640, camera_height: int = 480):
        try:
            self.camera.release()
        except:
            pass
        # TODO select the correct camera
        self.camera = self._camera_factory.create_camera(camera_type=camera_model)(
            id=camera_id, width=camera_width, height=camera_height)
        logging.info(f"Setting width: {camera_width} px")
        logging.info(f"Setting height: {camera_height} px")
        # self.camera.initialise()
        self.notify_observers()

    def set_Experiment(self, camera_id: int, camera_model: str,
                       camera_width: int = 640, camera_height: int = 480,
                       delay_ms=500, num_images=150, image_data_dir='.',
                       exp_params: dict = None):
        self.set_camera(camera_id=camera_id, camera_model=camera_model,
                        camera_width=camera_width, camera_height=camera_height)
        self.experiment = ImageCapturingExperiment(self.camera, delay_ms=delay_ms, num_images=num_images,
                                                   image_folder=image_data_dir, exp_params=exp_params)

    def add_observer(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def remove_observer(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self):
        for observer in self._observers:
            observer.update(self.camera)
