import tkinter as tk

class TKTLImageWindow(tk.Toplevel):
    def __init__(self, master, width=1280, height=720, **kwargs):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # initialize canvas for displaying images
        self.image_canvas = tk.Canvas(self, width=width, height=height)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

    def set_size(self, width, height):
        """
        Sets the size of the top-level window and the canvas.

        Args:
            width (int): The width to set for the window and canvas.
            height (int): The height to set for the window and canvas.
        """
        self.geometry(f"{width}x{height}")
        self.image_canvas.config(width=width, height=height)

    def get_canvas(self):
        """
        Provides access to the canvas.

        Returns:
            tk.Canvas: The canvas widget.
        """
        return self.image_canvas
