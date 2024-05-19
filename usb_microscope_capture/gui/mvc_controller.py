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
# controller.py

from .mvc_model import Model
from .mvc_view import View

class tkapp_Controller:
    experiment_state = False
    setup_state = False
    prev_exposure = 0
    prev_gain = 0

    def __init__(self, master, starting_dir):
        self.master = master
        
        # create the model and view for the MVC pattern
        self.model = Model(starting_dir=starting_dir)
        self.view = View(master, starting_dir=starting_dir)

        # register the callbacks
        self.view.tkf_mainFrame.start_button.config(command=self.start_experiment)
        self.view.tkf_mainFrame.stop_button.config(command=self.stop_experiment)
        self.view.tkf_mainFrame.toggle_button.config(command=self.view.toggle_image_window)
        self.view.tkf_mainFrame.toggle_setup_capture_button.config(command=self.toggle_setup_capture)

        # Register observers
        self.model.add_observer(self.view.tkf_mainFrame._tkf_exposure_settings)

    def start_experiment(self):
        cam_dict = self.view.tkf_mainFrame.get_camera_parameters()
        exp_dict = self.view.tkf_mainFrame.get_experiment_parameters()
        self.view.tkTL_image_window.set_size(cam_dict['cam.width'], cam_dict['cam.height'])
        logging.debug(cam_dict)
        logging.debug(exp_dict)
        self.model.set_Experiment(camera_id=cam_dict['cam.id'], 
                                  camera_model=cam_dict['cam.model'],
                                  camera_width=cam_dict['cam.width'], camera_height=cam_dict['cam.height'],
                                  delay_ms=exp_dict['delay_ms'], num_images=exp_dict['no_images'],
                                  image_data_dir=exp_dict['data_folder'],
                                  exp_params=exp_dict)
        self.model.experiment.initialise(wait_for_keypress=False)
        self.experiment_state = True
        self.view.tkf_mainFrame.set_running_status(running_flag=self.experiment_state)
        self.master.after(0, self._check_experiment_state)
    
    def _check_experiment_state(self):
        """this is a function that is performed periodically using the after function
        """        
        next_update_ms = 100 # TODO this is an arbitrary value. It should include a value from the the experiment settings
        FACTOR = 0.75
        if (self.model.experiment.image_counter < self.model.experiment.num_images) and (self.experiment_state):
            curr_time_s = time.time()
            time_since_last_capture_s = curr_time_s - self.model.experiment.last_capture_timestamp
            if time_since_last_capture_s >= self.model.experiment.delay_ms / 1000:
                self.model.experiment.last_capture_timestamp = curr_time_s
                frame = self.model.experiment.capture_image(curr_time_s, record_to_disk=True)
                self.view.update_image(frame)
                next_update_ms = int(self.model.experiment.delay_ms * FACTOR)
                logging.debug(f" - captured: {self.model.experiment.image_counter}, next update: {next_update_ms} ms")
            else:
                next_update_ms = max(1, int((self.model.experiment.delay_ms - time_since_last_capture_s * 1000) * FACTOR))
                logging.debug(f" > next update: {next_update_ms} ms")
            self.master.after(next_update_ms, self._check_experiment_state)
        else:
            logging.debug("Experiment Finished")
            self.model.experiment.finalise()

    def stop_experiment(self):
        logging.info("Stopping capture experiment prematurely!")
        self.experiment_state = False
        self.view.tkf_mainFrame.set_running_status(running_flag=self.experiment_state)

    def toggle_setup_capture(self):
        if not self.setup_state:
            # start setup capture
            cam_dict = self.view.tkf_mainFrame.get_camera_parameters()
            exp_dict = self.view.tkf_mainFrame.get_experiment_parameters(setup_mode=True)
            self.view.tkTL_image_window.set_size(cam_dict['cam.width'], cam_dict['cam.height'])
            logging.debug(cam_dict)
            logging.debug(exp_dict)
            self.model.set_Experiment(camera_id=cam_dict['cam.id'],
                                      camera_model=cam_dict['cam.model'],
                                      camera_width=cam_dict['cam.width'], camera_height=cam_dict['cam.height'],
                                      delay_ms=exp_dict['delay_ms'], num_images=exp_dict['no_images'],
                                      image_data_dir=exp_dict['data_folder'],
                                      exp_params=exp_dict)
            self.model.experiment.initialise(wait_for_keypress=False, setup_capture=True)
            self.setup_state = True
            self.view.tkf_mainFrame.set_running_status(running_flag=self.setup_state)
            self._prev_exposure = self.view.tkf_mainFrame._tkf_exposure_settings.get_exposure() #TODO could also check from camera
            self._prev_gain = self.view.tkf_mainFrame._tkf_exposure_settings.get_gain()
            self.master.after(0, self._check_setup_state)
        else:
            # stop setup capture
            self.setup_state = False
            self.view.tkf_mainFrame.set_running_status(running_flag=self.setup_state)

    def _check_setup_state(self):
        next_update_ms = 100
        _curr_exposure =  self.view.tkf_mainFrame._tkf_exposure_settings.get_exposure()
        _curr_gain =  self.view.tkf_mainFrame._tkf_exposure_settings.get_gain()
        if (_curr_exposure != self.prev_exposure):
            logging.info("Exposure changed from %s to %s", self.prev_exposure, _curr_exposure)
            self.model.camera.set_exposure(_curr_exposure)
        FACTOR = 0.75
        if self.setup_state:
            curr_time_s = time.time()
            time_since_last_capture_s = curr_time_s - self.model.experiment.last_capture_timestamp
            if time_since_last_capture_s >= self.model.experiment.delay_ms / 1000:
                self.model.experiment.last_capture_timestamp = curr_time_s
                frame = self.model.experiment.capture_image(curr_time_s, record_to_disk=False)
                x, y, width, height = self.view.get_roi()
                frame = frame[y:y+height, x:x+width]
                self.view.update_image(frame)
                next_update_ms = int(self.model.experiment.delay_ms * FACTOR)
                logging.debug(f" - captured: {self.model.experiment.image_counter}, next update: {next_update_ms} ms")
            else:
                # not enough time passed wait a few ms
                next_update_ms = max(1, int((self.model.experiment.delay_ms -time_since_last_capture_s*1000)*FACTOR))
                logging.debug(f"               >    next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            
            self.prev_exposure = _curr_exposure
            self.prev_gain = _curr_gain
            self.master.after(next_update_ms, self._check_setup_state)    
        else:
            logging.debug("Experiment Finished")
            self.model.experiment.finalise()
