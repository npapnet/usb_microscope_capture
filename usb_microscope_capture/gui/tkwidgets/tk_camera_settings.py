import tkinter as tk

class CameraSettingsFrame(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Camera Settings", **kwargs)
        
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
        self.exposure_label = tk.Label(self, text="Exposure time:")
        self.exposure_var = tk.DoubleVar()
        self.exposure_entry = tk.Entry(self, textvariable=self.exposure_var)

        # Gain
        self.gain_label = tk.Label(self, text="Gain:")
        self.gain_var = tk.DoubleVar()
        self.gain_entry = tk.Entry(self, textvariable=self.gain_var)

        # ROI Frame
        self.roi_frame = tk.LabelFrame(self, text="ROI")
        self.roi_frame.columnconfigure(0, weight=4)
        self.roi_frame.columnconfigure(1, weight=1)

        self.x_label = tk.Label(self.roi_frame, text="X:")
        self.x_var = tk.DoubleVar()
        self.x_entry = tk.Entry(self.roi_frame, textvariable=self.x_var)

        self.y_label = tk.Label(self.roi_frame, text="Y:")
        self.y_var = tk.DoubleVar()
        self.y_entry = tk.Entry(self.roi_frame, textvariable=self.y_var)

        self.dx_label = tk.Label(self.roi_frame, text="Width (dX):")
        self.dx_var = tk.DoubleVar()
        self.dx_entry = tk.Entry(self.roi_frame, textvariable=self.dx_var)

        self.dy_label = tk.Label(self.roi_frame, text="Height (dY):")
        self.dy_var = tk.DoubleVar()
        self.dy_entry = tk.Entry(self.roi_frame, textvariable=self.dy_var)

        self.rotation_label = tk.Label(self.roi_frame, text="Rotation:")
        self.rotation_var = tk.DoubleVar()
        self.rotation_slider = tk.Scale(self.roi_frame, variable=self.rotation_var, from_=-90, to=90, resolution=0.1, orient=tk.HORIZONTAL)

    def _layout_widgets(self):
        self.camera_label.grid(row=0, column=0, sticky='e')
        self.camera_dropdown.grid(row=0, column=1, sticky='we')

        self.exposure_label.grid(row=1, column=0, sticky='e')
        self.exposure_entry.grid(row=1, column=1, sticky='we')

        self.gain_label.grid(row=2, column=0, sticky='e')
        self.gain_entry.grid(row=2, column=1, sticky='we')

        self.roi_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='we')

        self.x_label.grid(row=0, column=0, sticky='e')
        self.x_entry.grid(row=0, column=1, sticky='we')

        self.y_label.grid(row=1, column=0, sticky='e')
        self.y_entry.grid(row=1, column=1, sticky='we')

        self.dx_label.grid(row=2, column=0, sticky='e')
        self.dx_entry.grid(row=2, column=1, sticky='we')

        self.dy_label.grid(row=3, column=0, sticky='e')
        self.dy_entry.grid(row=3, column=1, sticky='we')

        self.rotation_label.grid(row=4, column=0, sticky='e')
        self.rotation_slider.grid(row=4, column=1, sticky='we')

    def set_camera_options(self, camera_list):
        menu = self.camera_dropdown['menu']
        menu.delete(0, 'end')
        for camera in camera_list:
            menu.add_command(label=camera, command=lambda value=camera: self.camera_var.set(value))

    def set_exposure_range(self, min_val, max_val):
        self.exposure_entry.config(validate='key', validatecommand=(self.register(self._validate_exposure), '%P'))
        self.exposure_min = min_val
        self.exposure_max = max_val

    def set_gain_range(self, min_val, max_val):
        self.gain_entry.config(validate='key', validatecommand=(self.register(self._validate_gain), '%P'))
        self.gain_min = min_val
        self.gain_max = max_val

    def _validate_exposure(self, value_if_allowed):
        if value_if_allowed:
            try:
                value = float(value_if_allowed)
                if self.exposure_min <= value <= self.exposure_max:
                    return True
            except ValueError:
                return False
        return False

    def _validate_gain(self, value_if_allowed):
        if value_if_allowed:
            try:
                value = float(value_if_allowed)
                if self.gain_min <= value <= self.gain_max:
                    return True
            except ValueError:
                return False
        return False

    def get_exposure(self):
        return self.exposure_var.get()

    def get_gain(self):
        return self.gain_var.get()

    def get_roi(self):
        return [self.x_var.get(), self.y_var.get(), self.dx_var.get(), self.dy_var.get()]

    def get_rotation(self):
        return self.rotation_var.get()
