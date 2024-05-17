from . import *

class CameraFactory:
    _cameras = {
        'Generic (640x480)': Camera_Generic,
        'GL USB2 (640x480)': Camera_GL_USB2_UVC,
        'WTM W1 (1280x720)': Camera_WTM_W1,
    }

    @staticmethod
    def create_camera(camera_type)->AbstractCamera:
        if camera_type in CameraFactory._cameras:
            return CameraFactory._cameras[camera_type]()
        else:
            raise ValueError(f"Unknown camera type: {camera_type}")

    @staticmethod
    def get_camera_types()-> list[str]:
        return list(CameraFactory._cameras.keys())
