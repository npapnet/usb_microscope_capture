import cv2
import time

from abc import ABC, abstractmethod
import logging

class AbstractCamera(ABC):
    """
    Abstract Camera class that defines the basic interface for a camera.

    """

    @abstractmethod
    def initialise(self):
        pass

    @abstractmethod
    def check_operation(self):
        pass

    @abstractmethod
    def capture_image(self):
        pass

    @abstractmethod
    def release(self):
        pass

class Camera(AbstractCamera):
    
    def __init__(self, id, width, height, init=False):
        self.id = id
        self.width = width
        self.height = height
        self._camera_device = None
        if init:
            self.initialise()

    def initialise(self, initial_delay_s:int = 2)->None:
        logging.debug(f"initialising camera with id:{self.id}, width x height :( {self.width}x{self.height})")
        self._camera_device = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        self._camera_device.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._camera_device.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        time.sleep(initial_delay_s)

    def capture_image(self):
        ret, frame = self._camera_device.read()
        return frame

    def release(self)->None:
        logging.debug("releasing previous camera...")
        self._camera_device.release()
        logging.debug("Camera released")

    def check_operation(self)-> bool:
        ret, _ = self._camera_device.read()
        return ret
