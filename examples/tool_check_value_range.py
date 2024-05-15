#%%
import cv2

# Initialize the camera
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

def test_property_range(camera, property_id, test_values):
    results = {}
    for value in test_values:
        camera.set(property_id, value)
        actual_value = camera.get(property_id)
        results[value] = actual_value
        print(f"Attempted to set {value}, actual value: {actual_value} \t: {'Success' if actual_value == value else 'X'}")
    return results

# Define a range of test values for exposure and gain
exposure_test_values = [-13, -11, -9, -7, -5, -3, -1, 0, 1, 3, 5, 7, 9, 11, 13]
gain_test_values = [-1.0, 0, 0.25, 0.75,  1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

print("Testing Exposure Range:")
exposure_results = test_property_range(camera, cv2.CAP_PROP_EXPOSURE, exposure_test_values)

print("\nTesting Gain Range:")
gain_results = test_property_range(camera, cv2.CAP_PROP_GAIN, gain_test_values)

# Release the camera
camera.release()
# %%
