#%%[markdown]
#  ** OBSOLETE**
# these is one of the initial scripts which are now obsolete
#
#%%
import cv2
import pathlib 
from datetime import datetime
import time 


#%%

IMAGE_DATA_DIR = pathlib.Path('captured_images')
IMAGE_DATA_DIR.mkdir(parents=True, exist_ok=True)
now = datetime.now() # current date and time

def now_as_str()->str:
    return  now.strftime("%Y%m%d-%H%M%S")
TEST_TIMESTAMP = now_as_str()
TEST_FOLDER =IMAGE_DATA_DIR / f"test-{TEST_TIMESTAMP}"
TEST_FOLDER.mkdir(parents=True, exist_ok=True)
print(TEST_FOLDER)
TEST_METADATA_FNAME = TEST_FOLDER/ f"metadata_{TEST_TIMESTAMP}.txt"

#%%
# Set the camera ID (usually 0 or 1)
CAMERA_ID = 1

# Set the resolution of the camera
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
# CAMERA_WIDTH = 800
# CAMERA_HEIGHT = 600
# CAMERA_WIDTH = 1600
# CAMERA_HEIGHT = 1200
# Set the number of images to capture
DELAY_MS = 500

NUM_IMAGES = 150

# initialise Metadata file
metadata_fobj = open(TEST_METADATA_FNAME, "w")
metadata_fobj.write('ID \t elapsed\n')

# Initialize the camera
camera = cv2.VideoCapture(CAMERA_ID, cv2.CAP_DSHOW)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
time.sleep(2) # this is to start the camera
input(" >> Press ENTER key to proceed. <<")
#%%
START_TIMESTAMP = time.time()
LAST_TIMESTAMP = START_TIMESTAMP 
LAST_CAPTURE_TIMESTAMP = START_TIMESTAMP 
k=0

# Capture the specified number of images
while k <NUM_IMAGES:
    curr_time = time.time()
    if curr_time - LAST_CAPTURE_TIMESTAMP>=DELAY_MS/1000:
        time_delta = curr_time-LAST_CAPTURE_TIMESTAMP
        elapsed_time = curr_time-START_TIMESTAMP
        # Read a frame from the camera
        ret, frame = camera.read()

        # Save the image to file
        filename = TEST_FOLDER / f"img_{k:05d}.png"
        print(f"{k}: {time_delta} - {filename}")
        cv2.imwrite(str(filename.absolute()), frame)
        metadata_fobj.write(f"{k}\t {elapsed_time:010.3f}\n")
        
        # Display the captured image
        cv2.imshow('Captured Image', frame)
                
        LAST_CAPTURE_TIMESTAMP = curr_time
        k = k+1
    LAST_TIMESTAMP = curr_time
    # check to close 
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
# Release the camera
camera.release()
# close file
metadata_fobj.close()