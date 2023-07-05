import inspect
import pathlib
import tkinter as tk
import logging

from usb_microscope_capture.gui import tkapp_Controller

logging.basicConfig(level=logging.DEBUG)

def _tk_app_capture_starter(script_dir):
    print(script_dir)
    root = tk.Tk()
    app = tkapp_Controller(root, starting_dir=script_dir)
    root.mainloop()

def tkapp_capture_light_stack():
    """starting the Capture only app 
    """    
    # Get the second frame from the top of the stack (the caller of this function)
    caller_frame = inspect.stack()[1]
    script_dir = pathlib.Path(caller_frame.filename).resolve().parent
    _tk_app_capture_starter(script_dir)

def tkapp_capture_light_dummy_func(caller_func):
    """starting the app 
    using a dummy caller func

    Args:
        caller_func (function): dummy function used only to get the script filename 
    """    
    script_dir = pathlib.Path(inspect.getfile(caller_func)).resolve().parent
    _tk_app_capture_starter(script_dir)


