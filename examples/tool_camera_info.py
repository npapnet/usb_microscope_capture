#%%
import cv2

# Initialize the camera
camera = cv2.VideoCapture(  0)

if not camera.isOpened():
    print("Error: Could not open camera.")
else:
    # Fetch camera properties
    
    try:
        camera_name = camera.get(cv2.CAP_PROP_BACKEND_NAME)
    except:
        camera_name = camera.get(cv2.CAP_PROP_BACKEND)
        pass
    print(f"Camera Backend Name: {camera_name}")
    frame_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
    exposure = camera.get(cv2.CAP_PROP_EXPOSURE)
    gain = camera.get(cv2.CAP_PROP_GAIN)
    
    # Print camera properties

    
    print(f"Frame Width: {frame_width}")
    print(f"Frame Height: {frame_height}")
    print(f"Exposure: {exposure}")
    print(f"Gain: {gain}")

# Release the camera
camera.release()

# %%
