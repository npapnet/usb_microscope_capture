import pathlib
import time
from datetime import datetime

import cv2


class ImageCapturingExperiment:
    """
    A class to represent an image capturing experiment.
    
    Attributes
    ----------
    camera : Camera
        A Camera object representing the camera to be used in the experiment.
    delay_ms : int
        The delay in milliseconds between capturing each image.
    num_images : int
        The total number of images to be captured in the experiment.
    image_folder : pathlib.Path
        The directory path where the images will be stored.
    metadata_fobj : _io.TextIOWrapper
        File object for storing the metadata of captured images.
    """
    GRAYSCALE=True
    def __init__(self, camera, delay_ms:int, num_images:int, image_folder:pathlib.Path=pathlib.Path("captured_images")):
        """
        Constructs all the necessary attributes for the image capturing experiment.

        Parameters
        ----------
        camera : Camera
            A Camera object representing the camera to be used in the experiment.
        delay_ms : int
            The delay in milliseconds between capturing each image.
        num_images : int
            The total number of images to be captured in the experiment.
        image_folder : pathlib.Path
            The directory path where the images will be stored.
        """
        self.camera = camera
        self.delay_ms = delay_ms
        self.num_images = num_images
        self.image_folder = image_folder
        
        self.metadata_fobj = None
        
    def initialise(self, wait_for_keypress:bool=True):
        """_summary_

        Args:
            wait_for_keypress (bool, optional): _description_. Defaults to True.
        """        
        self.camera.initialise()
        assert self.camera.check_operation() , "Camera not working or not connected. Exiting...." 
        if wait_for_keypress: # this is for compatibility with the console application
            input(" >> Press ENTER key to proceed. <<")
        
        self._init_test_folder() 
        # initialise timestamps
        self.start_timestamp = time.time()
        self.last_capture_timestamp = self.start_timestamp 
        self.image_counter = 0

    def _init_test_folder(self):
        """
        Initialises the test folder where images will be stored and creates a metadata file.
        """
        self.test_start_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.test_folder =self.image_folder / f"test-{self.test_start_timestamp}"
        self.test_folder.mkdir(parents=True, exist_ok=True)
        print(self.test_folder)
        self.test_metadata_fname = self.test_folder / f"metadata_{self.test_start_timestamp}.txt"
        self.metadata_fobj = open(self.test_metadata_fname, "w")
        self.metadata_fobj.write('ID \t elapsed\n')

    def capture_image(self, curr_time_s:float):
        """ Captures an image, converts it to grayscale if required, and saves it along with its metadata.

        Parameters
        ----------
        curr_time_s : float
            The current timestamp.

        Returns
        -------
        numpy.ndarray
            The captured image.
        """
        elapsed_time = curr_time_s - self.start_timestamp
        frame = self.camera.capture_image()
        
        if self.GRAYSCALE:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        self._write_img_file(frame)

        # write metadata file
        self.metadata_fobj.write(f"{self.image_counter}\t {elapsed_time:010.3f}\n")

        self.last_capture_timestamp = curr_time_s
        self.image_counter += 1
            
        return frame

    def _write_img_file(self, frame) -> None:
        """
        Writes the captured image to the file.

        Parameters
        ----------
        frame : numpy.ndarray
            The captured image.
        """
        filename = self.test_folder / f"img_{self.image_counter:05d}.png"
        cv2.imwrite(str(filename.absolute()), frame)


    def finalise(self) -> None:
        """
        Finalises the experiment by releasing the camera and closing the metadata file.
        """
        cv2.destroyAllWindows()
        self.camera.release()
        self.metadata_fobj.close()

