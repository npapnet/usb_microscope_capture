"""
camera_device.py

This module contains the definition of an abstract base class (ABC) for a camera device and a concrete implementation of the ABC.

Classes:
    - AbstractCamera: This is an abstract base class that defines the basic interface for a camera device. It declares the following methods:
        - initialise: This method is intended to set up the camera for operation.
        - check_operation: This method is intended to verify if the camera is functioning correctly.
        - capture_image: This method is intended to capture an image using the camera.
        - release: This method is intended to release the resources held by the camera.

Dependencies:
    - time: This module is used for time-related tasks.
    - abc: This module provides the infrastructure for defining abstract base classes (ABCs).
    - logging: This module is used for logging.
    - cv2: This is an OpenCV module for working with images and videos.
"""
import time
from abc import ABC, abstractmethod
import logging
import numpy as np
import cv2


class AbstractCamera(ABC):
    """
    Abstract Camera class that defines the basic interface for a camera.
    """
    model_name = ""

    @abstractmethod
    def initialise(self):
        """
        This method is intended to set up the camera for operation.
        """
        pass

    @abstractmethod
    def check_operation(self):
        """
        This method is intended to verify if the camera is functioning correctly.
        """
        pass

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

    @abstractmethod
    def capture_image(self, roi:list = None):
        """
        This method is intended to capture an image using the camera.
        """
        pass

    @abstractmethod
    def release(self):
        """
        This method is intended to release the resources held by the camera.
        """
        pass




