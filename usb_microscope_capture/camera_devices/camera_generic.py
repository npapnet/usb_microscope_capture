"""
camera_device.py

This module contains the definition of an abstract base class (ABC) for a camera device and a concrete implementation of the ABC.

Classes:
    - AbstractCamera: This is an abstract base class that defines the basic interface for a camera device. It declares the following methods:
        - initialise: This method is intended to set up the camera for operation.
        - check_operation: This method is intended to verify if the camera is functioning correctly.
        - capture_image: This method is intended to capture an image using the camera.
        - release: This method is intended to release the resources held by the camera.
    - Camera: This is a concrete class that inherits from AbstractCamera. It is expected to provide implementations for the methods declared in AbstractCamera.

Dependencies:
    - time: This module is used for time-related tasks.
    - abc: This module provides the infrastructure for defining abstract base classes (ABCs).
    - logging: This module is used for logging.
    - cv2: This is an OpenCV module for working with images and videos.
"""
import time
import logging
import numpy as np
import cv2

from .camera_device_abstract import AbstractCamera
logging.basicConfig(level=logging.DEBUG)

class Camera_Generic(AbstractCamera):
    """
    Concrete implementation of the AbstractCamera class.
    """
    _max_height = 480
    _max_width = 640
    
    def __init__(self, id, width:int=None, height:int=None, init=False):
        """
        Initializes the Camera object.

        Args:
            id (int): The ID of the camera device.
            width (int): The width of the captured image.
            height (int): The height of the captured image.
            init (bool, optional): Whether to initialize the camera during object creation. Defaults to False.
        """
        self.model_name = "Generic Camera"
        self.id = id
        self.width = width if width <= self._max_width else self._max_width
        self.height = height if height <= self._max_height else self._max_height
        self._camera_device = None
        if init:
            self.initialise()

    def initialise(self, initial_delay_s:int = 2) -> None:
        """
        Sets up the camera for operation.

        Args:
            initial_delay_s (int, optional): The initial delay in seconds before capturing the first image. Defaults to 2.
        """
        logging.debug(f"initialising camera with id:{self.id}, width x height :( {self.width}x{self.height})")
        self._camera_device = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        self._camera_device.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._camera_device.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        #TODO look at https://github.com/opencv/opencv/issues/9738 and https://answers.opencv.org/question/112/autogain-how-to-disable-autogain-and-set-a-fixed-value/
        #    for removing autoexposure
        # self._camera_device.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        # self._camera_device.set(cv2.CAP_PROP_EXPOSURE, -7.0)
        time.sleep(initial_delay_s)

    def set_exposure(self, exposure_value: float) -> None:
        """
        Sets the exposure for the camera.

        Args:
            exposure_value (float): The exposure value to be set.
        """
        if self._camera_device is not None:
            logging.debug(f"Setting camera exposure to {exposure_value}")
            self._camera_device.set(cv2.CAP_PROP_EXPOSURE, exposure_value)
        else:
            logging.error("Camera device is not initialized.")

    def set_gain(self, gain_value: float) -> None:
        """
        Sets the gain for the camera.

        Args:
            gain_value (float): The gain value to be set.
        """
        if self._camera_device is not None:
            logging.debug(f"Setting camera gain to {gain_value}")
            self._camera_device.set(cv2.CAP_PROP_GAIN, gain_value)
        else:
            logging.error("Camera device is not initialized.")

    def capture_image(self, roi:list = None) -> np.ndarray:
        """
        Captures an image using the camera.

        Returns:
            numpy.ndarray: The captured image.
        """
        ret, frame = self._camera_device.read()
        if roi is not None:
            x, y, w, h = roi
            try:
                assert x>=0 and y>=0 and w>0 and h>0
                assert x+w <= self.width and y+h <= self.height
                frame = frame[y:y+h, x:x+w]
            except AssertionError:
                logging.error(f"Invalid ROI: {roi}")

        return frame

    def release(self) -> None:
        """
        Releases the resources held by the camera.
        """
        logging.debug("releasing previous camera...")
        self._camera_device.release()
        logging.debug("Camera released")

    def check_operation(self) -> bool:
        """
        Verifies if the camera is functioning correctly.

        Returns:
            bool: True if the camera is functioning correctly, False otherwise.
        """
        ret, _ = self._camera_device.read()
        return ret
