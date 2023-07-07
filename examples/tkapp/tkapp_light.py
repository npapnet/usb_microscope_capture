#%%
import pathlib
import tkinter as tk

import logging
logging.basicConfig(level=logging.DEBUG)
# Assuming the Camera and ImageCapturingExperiment classes are defined elsewhere
from usb_microscope_capture.gui import tkapp_Controller
from usb_microscope_capture.tkapps import tkapp_capture_light_stack
#%%


# if __name__ == "__main__": # Original way to call the app
#     script_dir = pathlib.Path(__file__).resolve().parent
#     print(script_dir)
        
#     root = tk.Tk()
#     app = tkapp_Controller(root, starting_dir=script_dir)
#     root.mainloop()

# %%   using the  tkapps
if __name__ == "__main__": 
        tkapp_capture_light_stack()

# %%
