import tkinter as tk

from usb_microscope_capture.camera_devices import AbstractCamera



class TkFrameROISettings(tk.LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, text="Camera Settings", **kwargs)
        
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        
        self._create_widgets()
        self._layout_widgets()
        
    def _create_widgets(self):
        
        # ROI Frame
        self.roi_frame = tk.LabelFrame(self, text="ROI")
        self.roi_frame.columnconfigure(0, weight=4)
        self.roi_frame.columnconfigure(1, weight=1)

        self.x_label = tk.Label(self.roi_frame, text="X:")
        self.x_var = tk.IntVar()
        self.x_entry = tk.Entry(self.roi_frame, textvariable=self.x_var)

        self.y_label = tk.Label(self.roi_frame, text="Y:")
        self.y_var = tk.IntVar()
        self.y_entry = tk.Entry(self.roi_frame, textvariable=self.y_var)

        self.dx_label = tk.Label(self.roi_frame, text="Width (dX):")
        self.dx_var = tk.IntVar()
        self.dx_entry = tk.Entry(self.roi_frame, textvariable=self.dx_var)

        self.dy_label = tk.Label(self.roi_frame, text="Height (dY):")
        self.dy_var = tk.IntVar()
        self.dy_entry = tk.Entry(self.roi_frame, textvariable=self.dy_var)

        self.rotation_label = tk.Label(self.roi_frame, text="Rotation:")
        self.rotation_var = tk.DoubleVar()
        self.rotation_slider = tk.Scale(self.roi_frame, variable=self.rotation_var, from_=-90, to=90, resolution=0.1, orient=tk.HORIZONTAL)

    def _layout_widgets(self):


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


    def get_roi(self):
        try:
            x = self.x_var.get()
        except tk.TclError:
            x = 0

        try:
            y = self.y_var.get()
        except tk.TclError:
            y = 0
        
        try:
            dx = self.dx_var.get()
        except tk.TclError:
            dx = 1

        try:
            dy = self.dy_var.get()
        except tk.TclError:
            dy = 1

        return [x, y, dx, dy]

    def get_rotation(self):
        return self.rotation_var.get()

    def update_settings_upon_device_change(self, camera_device):
        """This is a callback function that is called when the camera device is changed."""
        self.x_var.set(0)
        self.y_var.set(0)
        self.dx_var.set(camera_device.width)
        self.dy_var.set(camera_device.height)


# Usage Example:
if __name__ == "__main__":
    root = tk.Tk()
    frame = TkFrameROISettings(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()
