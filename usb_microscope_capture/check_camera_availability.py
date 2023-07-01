#%%
import cv2

# Iterate through camera IDs starting from 0
for camera_id in range(10):
    # Create a VideoCapture object for this camera
    cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
    
    # Check if the camera was opened successfully
    if cap.isOpened():
        # Read a frame from the camera to check if it is working properly
        ret, frame = cap.read()
        if ret:
            print(f"Camera {camera_id}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}")
        else:
            print(f"Camera {camera_id} is not working properly")
        
        # Release the camera
        cap.release()
    else:
        print(f"Could not open camera {camera_id}")
# %%
