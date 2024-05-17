import tkinter as tk
from usb_microscope_capture.camera_devices.camera_factory import CameraFactory

class tkFrameCameraType(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Camera type", **kwargs)
        
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self):
        # Camera dropdown
        self.camera_label = tk.Label(self, text="Camera Model:")
        self.camera_var = tk.StringVar()
        self.camera_dropdown = tk.OptionMenu(self, self.camera_var, "")

        # Exposure time
        self.max_width = tk.Label(self, text="Widht [px]:")
        self.max_width_var = tk.DoubleVar()
        self.tb_max_width = tk.Entry(self, textvariable=self.max_width_var)

        # Gain
        self.max_height = tk.Label(self, text="Height [px]:")
        self.max_height_var = tk.DoubleVar()
        self.tb_max_height = tk.Entry(self, textvariable=self.max_height_var)

    def _layout_widgets(self):
        self.camera_label.grid(row=0, column=0, sticky='e')
        self.camera_dropdown.grid(row=0, column=1, sticky='we')

        self.max_width.grid(row=1, column=0, sticky='e')
        self.tb_max_width.grid(row=1, column=1, sticky='we')

        self.max_height.grid(row=2, column=0, sticky='e')
        self.tb_max_height.grid(row=2, column=1, sticky='we')


    def set_camera_options(self, camera_list:list = None)->None:
        """Populate the combo box

        Args:
            camera_list (list, optional): _description_. Defaults to None.
        """
        menu = self.camera_dropdown['menu']
        menu.delete(0, 'end')
        for camera in camera_list:
            menu.add_command(label=camera, command=lambda value=camera: self.camera_var.set(value))
        self.camera_var.set(camera_list[0])  # Set the default value to the first value in camera_list

    def set_camera_factory(self, camera_factory: CameraFactory):
        """Set the camera factory 

        # TODO implement properly this function. It would give access to the camera factory and would simplify changes in the code. 
        # i.e. getting max width and height from the camera factory, or validating exposure and gain values from a specific camera. 

        Args:
            camera_factory (CameraFactory): _description_
        """
        self.camera_factory = camera_factory

    def get_max_width(self):
        return self.max_width_var.get()

    def get_max_height(self):
        return self.max_height_var.get()
