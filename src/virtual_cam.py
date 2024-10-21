import logging
import time
import cv2
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication

class VideoCapture(QObject):
    instance = None
    initialized = False

    def __new__(cls):
        if VideoCapture.instance is None:
            VideoCapture.instance = super(VideoCapture, cls).__new__(cls)
        return VideoCapture.instance

    def __init__(self):
        super(VideoCapture, self).__init__()

        if not VideoCapture.initialized:
            VideoCapture.initialized = True
            self.device_list = {}
            self.active_devices = []
            self.capture_device = None

    def init_capture_device(self, index):
        if self.capture_device is not None:
            self.capture_device.release()

        if index == -1:
            self.capture_device = None
            return True

        try:
            capture_device = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            capture_device.set(cv2.CAP_PROP_FPS, 60)  # Framerate is set to be 60fps
        except Exception as e:
            logging.exception(e)
            return False

        if capture_device is None or not capture_device.isOpened():
            logging.error(f"Can't open capture device at index {index}")
            return False
        if not capture_device.grab():
            logging.error(f"Capture device at index {index} is already in use")
            return False

        self.capture_device = capture_device
        return True

    def get_frame(self):
        if self.capture_device is None:
            time.sleep(0.01)
            return False, None

        try:
            retval, frame = self.capture_device.read()
        except Exception as e:
            logging.exception(e)
            return False, None

        return retval, frame

    def release(self):
        if self.capture_device is not None:
            self.capture_device.release()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    video_capture = VideoCapture()
    video_capture.init_capture_device(2)
    sys.exit(app.exec())