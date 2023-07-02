import cv2
import time

class Camera:
    INIT_DELAY_S = 2
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self._camera_device = None

    def initialise(self):
        self._camera_device = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        self._camera_device.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._camera_device.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        time.sleep(self.INIT_DELAY_S)

    def capture_image(self):
        ret, frame = self._camera_device.read()
        return frame

    def release(self):
        self._camera_device.release()

    def check_operation(self):
        ret, _ = self._camera_device.read()
        return ret
