#%%
import cv2
import pathlib 
from datetime import datetime
import time 

class Camera:
    INIT_DELAY_S = 2
    def __init__(self, id, width, height):
        self.id = id
        self.width = width
        self.height = height
        self.camera = None

    def initialise(self):
        self.camera = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        time.sleep(self.INIT_DELAY_S)

    def capture_image(self):
        ret, frame = self.camera.read()
        return frame

    def release(self):
        self.camera.release()

class ImageCapturingExperiment:
    GRAYSCALE=True
    def __init__(self, camera, delay_ms:int, num_images:int, image_folder:pathlib.Path):
        self.camera = camera
        self.delay_ms = delay_ms
        self.num_images = num_images
        self.image_folder = image_folder
        
        self.metadata_fobj = None
        
    def initialise(self):
        self.camera.initialise()
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


#%%

CAMERA_ID = 1
# Set the resolution of the camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
DELAY_MS = 500
NUM_IMAGES = 150
IMAGE_DATA_DIR = pathlib.Path('captured_images')
IMAGE_DATA_DIR.mkdir(parents=True, exist_ok=True)

# def now_as_str()->str:
#     return  datetime.now().strftime("%Y%m%d-%H%M%S")

camera = Camera(id=CAMERA_ID, width=CAMERA_WIDTH, height=CAMERA_HEIGHT)
experiment = ImageCapturingExperiment(camera, DELAY_MS, NUM_IMAGES, image_folder=IMAGE_DATA_DIR)
experiment.initialise()

while experiment.image_counter < experiment.num_images:
    
    curr_time_s = time.time()
    if curr_time_s - experiment.last_capture_timestamp >= experiment.delay_ms/1000:
        print (experiment.image_counter)
        frame = experiment.capture_image(curr_time_s)
        
        cv2.imshow('Captured Image', frame)        
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
        

experiment.finalise()
