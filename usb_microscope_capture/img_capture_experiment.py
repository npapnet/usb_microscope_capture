import pathlib
import time
from datetime import datetime

import cv2


class ImageCapturingExperiment:
    GRAYSCALE=True
    def __init__(self, camera, delay_ms:int, num_images:int, image_folder:pathlib.Path):
        self.camera = camera
        self.delay_ms = delay_ms
        self.num_images = num_images
        self.image_folder = image_folder
        
        self.metadata_fobj = None
        
    def initialise(self, wait_for_keypress:bool=True):
        self.camera.initialise()
        if wait_for_keypress: # this is for compatibility with the console application
            input(" >> Press ENTER key to proceed. <<")
        
        self._init_test_folder() 
        # initialise timestamps
        self.start_timestamp = time.time()
        self.last_capture_timestamp = self.start_timestamp 
        self.image_counter = 0

    def _init_test_folder(self):
        self.test_start_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.test_folder =self.image_folder / f"test-{self.test_start_timestamp}"
        self.test_folder.mkdir(parents=True, exist_ok=True)
        print(self.test_folder)
        self.test_metadata_fname = self.test_folder / f"metadata_{self.test_start_timestamp}.txt"
        self.metadata_fobj = open(self.test_metadata_fname, "w")
        self.metadata_fobj.write('ID \t elapsed\n')

        

    def capture_image(self, curr_time_s:float):
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
        filename = self.test_folder / f"img_{self.image_counter:05d}.png"
        cv2.imwrite(str(filename.absolute()), frame)


    def finalise(self) -> None:
        cv2.destroyAllWindows()
        self.camera.release()
        self.metadata_fobj.close()

