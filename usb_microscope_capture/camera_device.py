import cv2
import time

class Camera:
    INIT_DELAY_S = 2
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self.camera = None

    def initialise(self):
        self.camera = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        time.sleep(self.INIT_DELAY_S)

    def capture_image(self):
        ret, frame = self.camera.read()
        return frame

    def release(self):
        self.camera.release()
