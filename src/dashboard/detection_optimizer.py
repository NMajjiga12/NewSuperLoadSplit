from PyQt6.QtCore import QThread, pyqtSignal
import queue

class DetectionWorker(QThread):
    detection_result = pyqtSignal(str, bool)

    def __init__(self, start_detector, fadeout_detector):
        super().__init__()
        self.start_detector = start_detector
        self.fadeout_detector = fadeout_detector
        self.running = True
        self.frame_queue = queue.Queue(maxsize=10)  # Limit queue size to avoid overloading memory

    def add_frame(self, frame):
        if not self.frame_queue.full():
            self.frame_queue.put(frame)

    def run(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=1)  # Get frame from queue
                if frame is not None:
                    # Start detection logic
                    if self.start_detector.detect(frame):
                        self.detection_result.emit('start', True)

                    # Fadeout detection logic
                    status = self.fadeout_detector.detect_fadeout(frame)
                    if status:
                        self.detection_result.emit(status, False)

            except queue.Empty:
                continue

    def stop(self):
        self.running = False
        self.wait()
