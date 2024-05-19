import tkinter as tk

from usb_microscope_capture.camera_devices import AbstractCamera

class TKFrameGainExposureSettings(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Exposure & Gain Settings", **kwargs)
        
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self):
        # Exposure time
        self.exposure_label = tk.Label(self, text="Exposure time:")
        self.exposure_var = tk.DoubleVar()
        self.exposure_entry = tk.Entry(self, textvariable=self.exposure_var)
        
        # Gain
        self.gain_label = tk.Label(self, text="Gain:")
        self.gain_var = tk.DoubleVar()
        self.gain_entry = tk.Entry(self, textvariable=self.gain_var)
        
        # Auto Settings checkbox
        self.auto_var = tk.BooleanVar()
        self.auto_checkbox = tk.Checkbutton(self, text="Auto", variable=self.auto_var, command=self._toggle_auto_settings)
        
    def _layout_widgets(self):
        self.auto_checkbox.grid(row=0, column=0, columnspan=2, sticky='we')
        

        self.gain_label.grid(row=1, column=0, sticky='e')
        self.gain_entry.grid(row=1, column=1, sticky='we')

        self.exposure_label.grid(row=2, column=0, sticky='e')
        self.exposure_entry.grid(row=2, column=1, sticky='we')
        
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

    def _toggle_auto_settings(self):
        if self.auto_var.get():
            self.exposure_entry.config(state='disabled')
            self.gain_entry.config(state='disabled')
            # Enable auto-exposure and auto-gain using OpenCV
            self._set_auto_exposure_gain(True)
        else:
            self.exposure_entry.config(state='normal')
            self.gain_entry.config(state='normal')
            # Disable auto-exposure and auto-gain and set values manually using OpenCV
            self._set_auto_exposure_gain(False)
            self._set_manual_exposure_gain()

    def _set_auto_exposure_gain(self, auto):
        # This function will use OpenCV to enable/disable auto-exposure and auto-gain
        # cap = cv2.VideoCapture(0)
        pass
        # cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1 if auto else 0.25) # Assuming the camera supports this
        # cap.set(cv2.CAP_PROP_AUTO_WB, 1 if auto else 0) # Example for auto white balance if needed
        # cap.release()

    def _set_manual_exposure_gain(self):
        # This function will set the manual exposure and gain using OpenCV
        # cap = cv2.VideoCapture(0)
        pass
        # cap.set(cv2.CAP_PROP_EXPOSURE, self.get_exposure())
        # cap.set(cv2.CAP_PROP_GAIN, self.get_gain())
        # cap.release()


