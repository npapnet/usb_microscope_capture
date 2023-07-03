
import pathlib
import time
import tkinter as tk
from tkinter import filedialog, ttk

import cv2
from PIL import Image, ImageTk

import logging
logging.basicConfig(level=logging.DEBUG)
# Assuming the Camera and ImageCapturingExperiment classes are defined elsewhere
from usb_microscope_capture import Camera, ImageCapturingExperiment


class Model:
    def __init__(self, camera_id=1, camera_width=640, camera_height=480, delay_ms=500, num_images=50, image_data_dir=pathlib.Path("captured_images")):
        self.camera = Camera(id=camera_id, width=camera_width, height=camera_height)
        self.experiment = ImageCapturingExperiment(self.camera, delay_ms, num_images, image_folder=image_data_dir)

    def set_Experiment(self, camera_id=1, camera_width=640, camera_height=480, delay_ms=500, num_images=150, image_data_dir='.'):
        # TODO use this METHOD to initialise the experiment
        self.experiment = ImageCapturingExperiment(self.camera, delay_ms, num_images, image_folder=image_data_dir)

class TkFrameParameters(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.create_widgets()

    def create_widgets(self):
        # =================== camera  frame
        camera_frame = tk.LabelFrame(self, text="Camera Parameters")
        camera_frame.grid(row=0, column=0, padx=5, pady=5)

        self.create_labeled_entry(camera_frame, "Camera ID", 0, 0, "0")
        self.create_labeled_entry(camera_frame, "Camera Width", 1, 0, "640")
        self.create_labeled_entry(camera_frame, "Camera Height", 2, 0, "480")

        # =================== experiment frame
        experiment_frame = tk.LabelFrame(self, text="Experiment Parameters")
        experiment_frame.grid(row=1, column=0, padx=5, pady=5)

        self.browse_button = tk.Button(experiment_frame, text='Browse', command=self.browse_directory)
        self.browse_button.grid(row=0, column=0)

        self.folder_label = tk.Label(experiment_frame, text="No directory selected")
        self.folder_label.grid(row=0, column=1)

        self.create_labeled_entry(experiment_frame, "Delay [ms]", 1, 0, "500")
        self.create_labeled_entry(experiment_frame, "Num of images", 2, 0, "120")

        # =================== action frame
        action_frame = tk.LabelFrame(self, text="Actions and State")
        action_frame.grid(row=2, column=0, padx=5, pady=5)

        self.start_button = tk.Button(action_frame, text='Start Experiment', font='bold')
        self.start_button.grid(row=0, column=0)

        self.stop_button = tk.Button(action_frame, text='Stop Experiment')
        self.stop_button.grid(row=0, column=1)

        self.toggle_button = tk.Button(action_frame, text='Toggle Image Window')
        self.toggle_button.grid(row=1, column=0, columnspan=2)

    def create_labeled_entry(self, master, label_text, row, col, default_value):
        label = tk.Label(master, text=label_text)
        label.grid(row=row, column=col)

        entry = tk.Entry(master)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1)

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir="captured_images")
        self.folder_label.configure(text=directory)


class View:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-topmost', 1)  # keep the master window always on top
        self.create_view_widgets()
        
        # after initialisation of object set geometry of window (obsolete)
        self.master.after(1,self._set_image_window_init_position) # see comments

    def create_view_widgets(self):
        self.frame = TkFrameParameters(self.master)
        self.frame.pack()

        self.image_window = tk.Toplevel(self.master)
        self.image_window.withdraw()
        self.image_window.protocol("WM_DELETE_WINDOW", lambda : None)
       
        self.image_canvas = tk.Canvas(self.image_window, width=640, height=480)
        self.image_canvas.pack()

    def _set_image_window_init_position(self):
        """auxilliary function because initialisation 
        
        this is run only once during the lifetime of the object. 
        I could also do it with a lambda fucntion
        This is not necessary after setting master as topmost.
        """        
        x = self.master.winfo_x() + self.master.winfo_width()
        y = self.master.winfo_y()
        # Set the position of the image window
        self.image_window.geometry(f"+{x}+{y}")

    def toggle_image_window(self):
        if self.image_window.winfo_viewable():
            self.image_window.withdraw()
        else:
            self.image_window.deiconify()

    def update_image(self, image_frame):
        # Convert the image frame to a format suitable for Tkinter
        image = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        # If there isn't an image on the canvas yet, create one
        if not hasattr(self, 'image_on_canvas'):
            self.image_on_canvas = self.image_canvas.create_image(0, 0, image=image, anchor='nw')
        # Otherwise, update the existing image
        else:
            self.image_canvas.itemconfig(self.image_on_canvas, image=image)

        # Keep a reference to the image object to prevent it from being garbage collected
        self.current_image = image
        self.image_window.update_idletasks()


class Controller:
    experiment_state = False
    def __init__(self, master):
        self.master = master
        self.model = Model()
        self.view = View(master)

        self.view.frame.start_button.config(command=self.start_experiment)
        self.view.frame.stop_button.config(command=self.stop_experiment)
        self.view.frame.toggle_button.config(command=self.view.toggle_image_window)

    def start_experiment(self):
        # 
        self.model.experiment.initialise(wait_for_keypress=False)
        self.experiment_state = True
        self.master.after(0, self._check_experiment_state)
    
    def _check_experiment_state(self):
        """this is a function that is performed periodically using the after function
        """        
        next_update_ms = 100
        if (self.model.experiment.image_counter < self.model.experiment.num_images) and (self.experiment_state==True):
            curr_time_s = time.time()
            time_since_last_capture_s = curr_time_s - self.model.experiment.last_capture_timestamp 
            if time_since_last_capture_s >= self.model.experiment.delay_ms/1000:
                # perform capture
                self.model.experiment.last_capture_timestamp = curr_time_s
                frame = self.model.experiment.capture_image(curr_time_s)
                self.view.update_image(frame) 
                next_update_ms = int(self.model.experiment.delay_ms/2)
                logging.debug(f"    - captured: {self.model.experiment.image_counter }, next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            else:
                # not enough time passed wait a few ms
                next_update_ms = max(1, int((self.model.experiment.delay_ms -time_since_last_capture_s*1000)/2))
                logging.debug(f"               >    next update : {next_update_ms} ms ({self.model.experiment.delay_ms},{time_since_last_capture_s*1000:.2f}) ")
            self.master.after(next_update_ms, self._check_experiment_state)    
        else:
            # the experiment has finished or stopped
            logging.debug("Experiment Finished (image counter = num images)")
            self.model.experiment.finalise()

    def stop_experiment(self):
        # TODO add functionality
        print ("Stopping capture experiment prematurely!")
        logging.info("Stopping capture experiment prematurely!")
        self.experiment_state = False


if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
