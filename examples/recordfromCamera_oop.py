#%%
import pathlib
import time

import cv2

from usb_microscope_capture import Camera, ImageCapturingExperiment

#%%

CAMERA_ID = 1
# Set the resolution of the camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
DELAY_MS = 500
NUM_IMAGES = 150
IMAGE_DATA_DIR = pathlib.Path('captured_images')
IMAGE_DATA_DIR.mkdir(parents=True, exist_ok=True)

camera = Camera(id=CAMERA_ID, width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
experiment = ImageCapturingExperiment(camera, DELAY_MS, NUM_IMAGES, image_folder=IMAGE_DATA_DIR)
experiment.initialise()

while experiment.image_counter < experiment.num_images:
    
    curr_time_s = time.time()
    if curr_time_s - experiment.last_capture_timestamp >= experiment.delay_ms/1000:
        print (experiment.image_counter)
        frame = experiment.capture_image(curr_time_s)
        
        cv2.imshow('Captured Image', frame)        
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
        

experiment.finalise()
