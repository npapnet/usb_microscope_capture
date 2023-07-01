import os
import pathlib
import time

import cv2

from usb_microscope_capture import Camera, ImageCapturingExperiment

def run_experiment(camera_id: int, camera_width: int, camera_height: int, delay_ms: int, num_images: int, image_data_dir: str) -> None:
    """ Run an image capturing experiment with the specified parameters.
    
    This function initialises a camera and an image capturing experiment, captures the 
    specified number of images with the specified delay between captures, and then finalises the experiment.
    
    Args:
        camera_id (int): The ID of the camera to use.
        camera_width (int): The width of the camera resolution.
        camera_height (int): The height of the camera resolution.
        delay_ms (int): The delay between image captures in milliseconds.
        num_images (int): The number of images to capture.
        image_data_dir (str): The directory where the captured images should be saved.

    Returns:
        None
    """  

    image_data_dir_path = pathlib.Path(image_data_dir)
    image_data_dir_path.mkdir(parents=True, exist_ok=True)

    camera = Camera(id=camera_id, width=camera_width, height=camera_height)
    experiment = ImageCapturingExperiment(camera, delay_ms, num_images, image_folder=image_data_dir_path)
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
    print("Experiment finished.")