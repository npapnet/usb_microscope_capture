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
from usb_microscope_capture.gui import tkapp_Controller
#%%


if __name__ == "__main__":
    script_dir = pathlib.Path(__file__).resolve().parent
    print(script_dir)
    root = tk.Tk()
    app = tkapp_Controller(root, starting_dir=script_dir)
    root.mainloop()

# %%
