import logging
import time
import cv2
from PyQt5.QtCore import QObject

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
            capture_device.set(cv2.CAP_PROP_FPS, 60) # Framerate is set to be 30fps
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
    if __name__ == "__main__":
        import sys
        from PyQt5.QtWidgets import QApplication

        app = QApplication(sys.argv)
        video_capture = VideoCapture()

        # Initialize capture device (0 refers to the first camera device)
        if not video_capture.init_capture_device(2):
            print("Failed to initialize capture device.")
            sys.exit(1)

        # Create a window for display
        window_name = "Virtual Camera Test"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 640, 480)

        while True:
            ret, frame = video_capture.get_frame()

            if ret:
                # Display the resulting frame
                cv2.imshow(window_name, frame)
            else:
                print("Failed to capture frame")

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the capture device and close the OpenCV window
        video_capture.release()
        cv2.destroyAllWindows()
        sys.exit(app.exec())
