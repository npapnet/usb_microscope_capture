import tkinter as tk
from usb_microscope_capture.camera_devices import CameraFactory, AbstractCamera

class tkFrameCameraType(tk.LabelFrame):
    camera_factory: CameraFactory = None
    _camera_device: AbstractCamera = None
    _reinitialise_roi_upon_camera_change  = None

    def __init__(self, master, camera_factory:CameraFactory= None,**kwargs):
        super().__init__(master, text="Camera type", **kwargs)
        
        self.camera_factory = camera_factory
        
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        
        self._create_widgets()
        self._layout_widgets()
        

    def _create_widgets(self):
        # Camera dropdown
        self.camera_label = tk.Label(self, text="Camera Model:")
        self.camera_var = tk.StringVar()
        self.camera_var.trace_add('write', self._on_camera_selection_change)
        self.camera_dropdown = tk.OptionMenu(self, self.camera_var, "")

        # Width
        self.max_width = tk.Label(self, text="Width [px]:")
        self.max_width_var = tk.DoubleVar()
        self.tb_max_width = tk.Entry(self, textvariable=self.max_width_var)

        # Height
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

    def set_camera_options(self, camera_list:list = None) -> None:
        """Populate the combo box

        Args:
            camera_list (list, optional): List of camera models. Defaults to None.
        """
        menu = self.camera_dropdown['menu']
        menu.delete(0, 'end')
        for camera in camera_list:
            menu.add_command(label=camera, command=lambda value=camera: self.camera_var.set(value))
        self.camera_var.set(camera_list[0])  # Set the default value to the first value in camera_list
        self._on_camera_selection_change()

    def set_camera_factory(self, camera_factory: CameraFactory):
        """Set the camera factory and update dimensions

        Args:
            camera_factory (CameraFactory): CameraFactory instance
        """
        self.camera_factory = camera_factory


    def _on_camera_selection_change(self, *args):
        """Callback when the camera selection changes"""
        selected_camera = self.camera_var.get()
        try:
            if self.camera_factory:
                self._camera_device = self.camera_factory._cameras.get(selected_camera)
                if self._camera_device:
                    self.update_dimensions_from_device()
                    self._reinitialise_roi_upon_camera_change(self._camera_device)
        except Exception as e:
            print(f"Error: {e}")
            pass

    def set_roi_callback(self, callback):  
        self._reinitialise_roi_upon_camera_change = callback

    def update_dimensions_from_device(self):
        """Update the max width and height from the selected camera device"""
        self.max_width_var.set(self._camera_device.width)
        self.max_height_var.set(self._camera_device.height)

    def get_max_width(self):
        return self.max_width_var.get()

    def get_max_height(self):
        return self.max_height_var.get()
