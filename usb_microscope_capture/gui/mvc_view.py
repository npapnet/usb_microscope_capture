import pathlib
import tkinter as tk
from tkinter import filedialog, messagebox

import cv2
from PIL import Image, ImageTk

import logging
logging.basicConfig(level=logging.DEBUG)


class TkFrameParameters(tk.Frame):
    _data_directory = None
    def __init__(self, master, starting_dir,**kwargs):
        super().__init__(master, **kwargs)
        self._tk_app_dir = starting_dir

        self.create_widgets()

    def create_widgets(self):
        # =================== camera  frame
        camera_frame = tk.LabelFrame(self, text="Camera Parameters")
        camera_frame.grid(row=0, column=0, padx=5, pady=5)

        self._tkeCamID = self._create_labeled_entry(camera_frame, "Camera ID", 0, 0, "0")
        self._tkeCamWidth = self._create_labeled_entry(camera_frame, "Camera Width", 1, 0, "640")
        self._tkeCamHeight = self._create_labeled_entry(camera_frame, "Camera Height", 2, 0, "480")

        # =================== experiment frame
        experiment_frame = tk.LabelFrame(self, text="Experiment Parameters")
        experiment_frame.grid(row=1, column=0, padx=5, pady=5)

        self.folder_label = tk.Label(experiment_frame, text="Data Folder")
        self.folder_label.grid(row=0, column=0)

        self.browse_button = tk.Button(experiment_frame, text='Browse', command=self.browse_directory)
        self.browse_button.grid(row=0, column=1)


        self._tkeDelay_ms = self._create_labeled_entry(experiment_frame, "Delay [ms]", 1, 0, "500")
        self._tkeNmaxImages = self._create_labeled_entry(experiment_frame, "Num of images", 2, 0, "120")

        # =================== action frame
        action_frame = tk.LabelFrame(self, text="Actions and State")
        action_frame.grid(row=2, column=0, padx=5, pady=5)

        self.start_button = tk.Button(action_frame, text='Start Experiment', font='bold')
        self.start_button.grid(row=0, column=0)

        self.stop_button = tk.Button(action_frame, text='Stop Experiment')
        self.stop_button.grid(row=0, column=1)

        self.toggle_button = tk.Button(action_frame, text='Toggle Image Window')
        self.toggle_button.grid(row=1, column=0, columnspan=2)

        self.status_indicator = tk.Canvas(action_frame, width=20, height=20)
        self.status_indicator.grid(row=2, column=0)
        self.status_indicator.create_oval(2, 2, 18, 18, fill="red")

        self.status_label = tk.Label(action_frame, text="Not running")
        self.status_label.grid(row=2, column=1)


    def get_camera_parameters(self) -> dict:
        """Extracts the camera parameters from the Entry fields and returns them as a dictionary.

        Returns:
            dict: A dictionary where the keys are the parameter names and the values are the parameter values.
        """
        cam_id = int(self._tkeCamID.get())
        cam_width = int(self._tkeCamWidth.get())
        cam_height = int(self._tkeCamHeight.get())

        return {"cam.id": cam_id, "cam.width": cam_width, "cam.height": cam_height}
    
    def get_experiment_parameters(self):
        if not self._data_directory:
            if messagebox.askokcancel("Data Directory Not Set",
                                      "The data directory has not been initialised. "
                                      "Please select a directory to store the images."):
                self.browse_directory()  # prompt the user to select a folder
            else:
                self._data_directory = self._tk_app_dir / "captured_images/"
                self._data_directory.mkdir(parents=True, exist_ok=True)
                # self.folder_label["text"] = str(self._data_directory)

        return {
            "data_folder": self._data_directory,
            "delay_ms": int(self._tkeDelay_ms.get()),
            "no_images": int(self._tkeNmaxImages.get())
        }
    
    def set_running_status(self, running_flag:bool)->None:
        """Changes the color of the status indicator and label text based on the running status of the experiment.
    
        This method changes the color of the status indicator to green if the experiment is running, 
        and to red if it's not running. The text of the label is changed accordingly to "Running" or "Not running".

        Args:
            running_flag (bool): Flag indicating whether the experiment is currently running. 
                                If True, the experiment is running; otherwise, it's not running.

        Returns:
            None
        """
        if running_flag:
            self.status_indicator.itemconfig(1, fill="green")
            self.status_label.config(text="Running")
        else:
            self.status_indicator.itemconfig(1, fill="red")
            self.status_label.config(text="Not running")

    def _create_labeled_entry(self, master, label_text, row, col, default_value):
        """auxilliary function that automated Label, entry process

        Args:
            master (_type_): parent widget
            label_text (_type_): label text
            row (_type_): row on grid layout
            col (_type_): col on grid layout
            default_value (_type_): Initial value 

        Returns:
            tk.Entry: The created object
        """        
        label = tk.Label(master, text=label_text)
        label.grid(row=row, column=col)

        entry = tk.Entry(master)
        entry.insert(0, default_value)
        entry.grid(row=row, column=col+1)
        return entry

    def browse_directory(self):
        self._data_directory = pathlib.Path(filedialog.askdirectory(initialdir=self._tk_app_dir))
        # self.folder_label.configure(text=self._data_directory)


class View:
    _tk_app_dir = None
    def __init__(self, master, starting_dir:pathlib.Path):
        self.master = master
        self._tk_app_dir = starting_dir

        self.master.attributes('-topmost', 1)  # keep the master window always on top
        self.create_view_widgets()
        
        # after initialisation of object set geometry of window (obsolete)
        self.master.after(1,self._set_image_window_init_position) # see comments

    def create_view_widgets(self):
        self.tkFrameParameters = TkFrameParameters(self.master, starting_dir=self._tk_app_dir)
        self.tkFrameParameters.pack()

        self.tkTL_image_window = tk.Toplevel(self.master)
        self.tkTL_image_window.withdraw()
        self.tkTL_image_window.protocol("WM_DELETE_WINDOW", lambda : None)
       
        self.image_canvas = tk.Canvas(self.tkTL_image_window, width=640, height=480)
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
        self.tkTL_image_window.geometry(f"+{x}+{y}")

    def toggle_image_window(self):
        if self.tkTL_image_window.winfo_viewable():
            self.tkTL_image_window.withdraw()
        else:
            self.tkTL_image_window.deiconify()

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
        self.tkTL_image_window.update_idletasks()



