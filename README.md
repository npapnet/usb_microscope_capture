# 1. usb_microscope_capture

Author: N. Papadakis

Repository for a small package used for the development of  a USB Microscope capture  device.

# 2. Requirements

## 2.1. Hardware requirements

This is written and tested for an OEM digital Microscope with 500x zoom (probably other microscopes can use the same architecture). 

![OEM](OEM-usb-digital-microscope-500x-zoom.jpg)

## 2.2. Installation 

- clone the repository
- navivate to the repository and to install use the following :
```{bash}
python setup.py install
```

# 3. Example code


After installing you can use, the following code in python to capture the data

```{python}
import cv2
import pathlib 
from datetime import datetime
import time 
from usb_microscope_capture import Camera, ImageCapturingExperiment

CAMERA_ID = 1
# Set the resolution of the camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
DELAY_MS = 500
NUM_IMAGES = 150
IMAGE_DATA_DIR = pathlib.Path('captured_images')
IMAGE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# initialise the camera
camera = Camera(id=CAMERA_ID, width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
experiment = ImageCapturingExperiment(camera, DELAY_MS, NUM_IMAGES, image_folder=IMAGE_DATA_DIR)

# experiment.GRAYSCALE = False ## uncomment the line to save grayscale images


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
```