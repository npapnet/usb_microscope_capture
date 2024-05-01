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
from usb_microscope_capture import Camera, ImageCapturingExperiment
from .mvc_model import Model
from .mvc_view import View 

class tkapp_Controller:
    experiment_state = False
    setup_state = False
    def __init__(self, master, starting_dir):
        self.master = master
        
        self.model = Model(starting_dir = starting_dir)
        self.view = View(master, starting_dir = starting_dir)

        self.view.tkFrameParameters.start_button.config(command=self.start_experiment)
        self.view.tkFrameParameters.stop_button.config(command=self.stop_experiment)
        self.view.tkFrameParameters.toggle_button.config(command=self.view.toggle_image_window)
        self.view.tkFrameParameters.toggle_setup_capture_button.config(command=self.toggle_setup_capture)

    def start_experiment(self):
        # 
        cam_dict = self.view.tkFrameParameters.get_camera_parameters()
        exp_dict = self.view.tkFrameParameters.get_experiment_parameters()
        logging.debug(cam_dict)
        logging.debug(exp_dict)
        self.model.set_Experiment(camera_id=cam_dict['cam.id'], camera_width=cam_dict['cam.width'], camera_height=cam_dict['cam.height'],
                                 delay_ms=exp_dict['delay_ms'], num_images=exp_dict['no_images'] ,
                                 image_data_dir=exp_dict['data_folder'] 
                                 #pathlib.Path("captured_images")
                                )
        self.model.experiment.initialise(wait_for_keypress=False)
        self.experiment_state = True
        self.view.tkFrameParameters.set_running_status(running_flag= self.experiment_state)
        self.master.after(0, self._check_experiment_state)
    
    def _check_experiment_state(self):
        """this is a function that is performed periodically using the after function
        """        
        next_update_ms = 100 # TODO this is an arbitrary value. It should include a value from the the experiment settings
        FACTOR = 0.75
        if (self.model.experiment.image_counter < self.model.experiment.num_images) and (self.experiment_state==True):
            curr_time_s = time.time()
            time_since_last_capture_s = curr_time_s - self.model.experiment.last_capture_timestamp 
            if time_since_last_capture_s >= self.model.experiment.delay_ms/1000:
                # perform capture
                self.model.experiment.last_capture_timestamp = curr_time_s
                frame = self.model.experiment.capture_image(curr_time_s)
                self.view.update_image(frame) 
                next_update_ms = int(self.model.experiment.delay_ms*FACTOR)
                logging.debug(f"    - captured: {self.model.experiment.image_counter }, next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            else:
                # not enough time passed wait a few ms
                next_update_ms = max(1, int((self.model.experiment.delay_ms -time_since_last_capture_s*1000)*FACTOR))
                logging.debug(f"               >    next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            self.master.after(next_update_ms, self._check_experiment_state)    
        else:
            # the experiment has finished or stopped
            logging.debug("Experiment Finished (image counter = num images)")

            self.model.experiment.finalise()

    def stop_experiment(self):
        print ("Stopping capture experiment prematurely!")
        logging.info("Stopping capture experiment prematurely!")
        self.experiment_state = False
        self.view.tkFrameParameters.set_running_status(running_flag=self.experiment_state)

    def toggle_setup_capture(self):
        """this function will toggle the setup in order to facilitate proper  configuration without saving to disk
        """
        if self.setup_state is False:

            cam_dict = self.view.tkFrameParameters.get_camera_parameters()
            exp_dict = self.view.tkFrameParameters.get_experiment_parameters()
            logging.debug(cam_dict)
            logging.debug(exp_dict)
            self.model.set_Experiment(camera_id=cam_dict['cam.id'], camera_width=cam_dict['cam.width'], camera_height=cam_dict['cam.height'],
                                    delay_ms=exp_dict['delay_ms'], num_images=exp_dict['no_images'] ,
                                    image_data_dir=exp_dict['data_folder'] 
                                    #pathlib.Path("captured_images")
                                    )
            self.model.experiment.initialise(wait_for_keypress=False, setup_capture=True)
            self.setup_state = True
            self.view.tkFrameParameters.set_running_status(running_flag= self.setup_state)
            self.master.after(0, self._check_setup_state)
        else:
            self.setup_state = False
            self.view.tkFrameParameters.set_running_status(running_flag=self.setup_state)


    def _check_setup_state(self):
        """this is a function that is performed periodically using the after function
        """  
        #TODO there is a lot of replication with the check_experiment state. I could create a generic function that can 
        # handle both cases and create wrappers for both.     
        next_update_ms = 100
        FACTOR = 0.75
        if (self.setup_state==True):
            curr_time_s = time.time()
            time_since_last_capture_s = curr_time_s - self.model.experiment.last_capture_timestamp 
            if time_since_last_capture_s >= self.model.experiment.delay_ms/1000:
                # perform capture
                self.model.experiment.last_capture_timestamp = curr_time_s
                frame = self.model.experiment.capture_image(curr_time_s, record_to_disk=False)
                self.view.update_image(frame) 
                next_update_ms = int(self.model.experiment.delay_ms*FACTOR)
                logging.debug(f"    - captured: {self.model.experiment.image_counter }, next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            else:
                # not enough time passed wait a few ms
                next_update_ms = max(1, int((self.model.experiment.delay_ms -time_since_last_capture_s*1000)*FACTOR))
                logging.debug(f"               >    next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            self.master.after(next_update_ms, self._check_setup_state)    
        else:
            # the experiment has finished or stopped
            logging.debug("Experiment Finished (image counter = num images)")

            self.model.experiment.finalise()