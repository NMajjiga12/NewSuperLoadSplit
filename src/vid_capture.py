import logging
import time

import cv2

from PyQt5.QtMultimedia import QCameraInfo
from PyQt5.QtCore import QObject, QThread, pyqtSignal


class VideoCapture(QObject):
    sig_device_list_updated = pyqtSignal()

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
            self.capture_device = None
            self.device_list_worker = None
            self.current_device_index = -1

    def get_device_list(self):
        return self.device_list

    def update_device_list(self):
        self.device_list_worker = DeviceListWorker()
        self.device_list_worker.sig_device_list_updated.connect(self.device_list_updated)
        self.device_list_worker.start()

    def device_list_updated(self, device_list):
        self.device_list = device_list
        self.sig_device_list_updated.emit()
        print(self.device_list)

    def init_capture_device(self, index):
        # If trying to initialize the same device, do nothing
        if self.current_device_index == index and self.capture_device is not None:
            if self.capture_device.isOpened():
                return True
        
        # Release previous device
        if self.capture_device is not None:
            self.capture_device.release()
            self.capture_device = None

        try:
            # Try different backends if DSHOW fails
            capture_device = cv2.VideoCapture(index, cv2.CAP_DSHOW)
            
            # If DSHOW fails, try default backend
            if not capture_device.isOpened():
                capture_device = cv2.VideoCapture(index)
                
            if capture_device is None or not capture_device.isOpened():
                logging.error(f"Can't open capture device at index {index}")
                return False
                
            # Test if we can actually read a frame
            retval, test_frame = capture_device.read()
            if not retval or test_frame is None:
                logging.error(f"Capture device at index {index} is not providing frames")
                capture_device.release()
                return False

        except Exception as e:
            logging.exception(f"Error initializing capture device at index {index}: {e}")
            return False

        try:
            # Set frame width to 640 (4:3 aspect ratio for NSMBW)
            capture_device.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            # Set frame height to 480
            capture_device.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            # Set framerate to 30fps for NSMBW (minimum) and allow up to 60fps
            capture_device.set(cv2.CAP_PROP_FPS, 60)
            # Set buffer size to minimize latency
            capture_device.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            # Set fourcc codec for better compatibility
            capture_device.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        except Exception as e:
            logging.exception(f"Error setting capture device properties: {e}")
            # Continue even if properties can't be set

        self.capture_device = capture_device
        self.current_device_index = index
        return True

    def get_frame(self):
        if self.capture_device is None or not self.capture_device.isOpened():
            time.sleep(0.033)  # ~30fps delay
            return False, None

        try:
            retval, frame = self.capture_device.read()
            if not retval or frame is None or frame.size == 0:
                return False, None

            # Ensure frame has valid dimensions
            if frame.shape[0] == 0 or frame.shape[1] == 0:
                return False, None

            # Convert from BGR to RGB for display
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        except Exception as e:
            logging.exception(f"Error reading frame from capture device: {e}")
            return False, None

        return retval, frame

    def release(self):
        if self.capture_device is not None:
            self.capture_device.release()
            self.capture_device = None
            self.current_device_index = -1


class DeviceListWorker(QThread):
    sig_device_list_updated = pyqtSignal(dict)

    def __init__(self):
        QThread.__init__(self)

        self.device_list = {}

    def run(self):
        self.update_device_list()
        self.sig_device_list_updated.emit(self.device_list)

    def update_device_list(self):
        try:
            self.device_list.clear()
            index = 0
            for camera_info in QCameraInfo.availableCameras():
                self.device_list[str(index)] = camera_info.description()
                index += 1
        except Exception as e:
            logging.exception(e)