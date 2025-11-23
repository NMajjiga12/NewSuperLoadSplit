import datetime
import logging
import cv2
import numpy as np
import os
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage

from src.livesplit import Livesplit
from src.vid_capture import VideoCapture
from src.fps_counter import FpsCounter
from src.config import Config
from src.route_handler import RouteHandler
from src.detectors.banner_load_detector import BannerLoadDetector
from src.detectors.fade_load_detector import FadeLoadDetector


class Autosplitter(QThread):
    sig_status_update = pyqtSignal(str, bool, bool)  # message, busy, waiting
    sig_preview_update = pyqtSignal(QPixmap)  # preview image
    sig_preview_clear = pyqtSignal()
    sig_clear_splits = pyqtSignal()
    sig_add_splits = pyqtSignal(list)  # splits list
    sig_component_activated = pyqtSignal(int, int)  # activations, required activations
    sig_load_count_changed = pyqtSignal(int, int)  # load count, required load count
    sig_component_changed = pyqtSignal(int)  # component index
    sig_next_split = pyqtSignal()
    sig_prev_split = pyqtSignal()
    sig_reset_splits = pyqtSignal()

    def __init__(self, parent_process):
        QThread.__init__(self)

        self.alive = True
        self.parent_process = parent_process
        self.running = False

        self.video_capture = VideoCapture()
        self.video_capture.update_device_list()
        
        # Use default value if config key doesn't exist
        capture_device = Config.get_key("capture_device", 0)
        self.video_capture.init_capture_device(capture_device)

        # Initialize detectors
        self.banner_detector = BannerLoadDetector()
        self.fade_detector = FadeLoadDetector()

        self.livesplit = Livesplit()
        self.livesplit.sig_timer_reset.connect(self.reset_run)
        self.livesplit.start()

        self.fps_counter = FpsCounter(1, 60)
        self.fps_counter.start()

        self.current_split_index = 0
        self.current_split = None
        self.current_component_index = 0
        self.prev_component = None

        self.current_component = None
        self.load_count = 0
        self.activations = 0
        self.run_started = False
        self.wait_for_first_split = False
        self.wait_for_reset = False
        self.waiting_for_fadein = False
        
        # New classification state variables
        self.is_in_load_state = False
        self.last_load_time = 0
        self.load_cooldown = 2.0  # seconds between load detections
        self.frames_since_last_load = 0
        self.current_load_type = None
        
        # New settings
        self.starting_detector = Config.get_key("starting_detector", "manual")
        self.ending_detector = Config.get_key("ending_detector", "switch")

    def run(self):
        self.initialize()

        while self.alive:
            if self.running:
                self.update()
                self.fps_counter.update()

    def quit(self):
        self.alive = False
        self.video_capture.release()

        if self.livesplit.isRunning():
            self.livesplit.terminate()
            self.livesplit.wait()

        if self.fps_counter.isRunning():
            self.fps_counter.terminate()
            self.fps_counter.wait()

        if self.video_capture.device_list_worker.isRunning():
            self.video_capture.device_list_worker.terminate()
            self.video_capture.device_list_worker.wait()

    def initialize(self):
        self.sig_status_update.emit("Initializing NSMBW AutoSplit", False, False)
        # Load any ONNX models if needed for future CNN implementation
        self.sig_status_update.emit("Ready", False, False)

    def set_starting_detector(self, detector):
        self.starting_detector = detector
        Config.set_key("starting_detector", detector)

    def set_ending_detector(self, detector):
        self.ending_detector = detector
        Config.set_key("ending_detector", detector)

    def cv2_image_to_pixmap(self, image, width, height):
        if isinstance(image, type(None)) or image.shape[0] == 0 or image.shape[1] == 0 or image.shape[2] != 3:
            logging.warning(f"Image doesn't have correct shape. Expected (>0, >0, 3), got {image.shape}")
            return None

        try:
            # Ensure we have valid dimensions
            if width <= 0 or height <= 0:
                width, height = 320, 240
                
            # Maintain 4:3 aspect ratio (640x480 for NSMBW)
            target_width = width
            target_height = int(target_width * 3 / 4)
            
            # If calculated height exceeds available height, adjust width instead
            if target_height > height:
                target_height = height
                target_width = int(target_height * 4 / 3)
            
            # Ensure minimum dimensions
            target_width = max(target_width, 1)
            target_height = max(target_height, 1)
            
            image = cv2.resize(image, (target_width, target_height), interpolation=cv2.INTER_LINEAR)
            
            # Create a background with the target size using the theme color
            background = np.zeros((height, width, 3), dtype=np.uint8)
            # Set to dark red background color (RGB: 40, 25, 30)
            background[:, :, 0] = 40   # R
            background[:, :, 1] = 25   # G  
            background[:, :, 2] = 30   # B
            
            # Calculate position to center the image
            y_offset = (height - target_height) // 2
            x_offset = (width - target_width) // 2
            
            # Ensure the offsets are within bounds
            y_offset = max(0, min(y_offset, height - target_height))
            x_offset = max(0, min(x_offset, width - target_width))
            
            # Place the resized image on the background
            background[y_offset:y_offset+target_height, x_offset:x_offset+target_width] = image
            
            # Get the final dimensions for the QImage
            final_height, final_width, _ = background.shape
            bytes_per_line = 3 * final_width
            qimg = QImage(background.data, final_width, final_height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            
        except Exception as e:
            logging.exception(e)
            return None

        return pixmap

    def update(self):
        if self.current_component != self.prev_component:
            self.set_activations(self.activations)
            self.set_load_count(self.load_count)
            self.sig_component_changed.emit(self.current_component_index)
            self.prev_component = self.current_component

        retval, frame = self.video_capture.get_frame()
        if not retval or frame is None:
            # If we can't get a frame, clear preview and skip processing
            self.sig_preview_clear.emit()
            return

        try:
            if frame.shape[2] != 3:
                logging.warning(f"Expected frame to have 3 channels, got {frame.shape[2]}")
                return

            if frame.shape[0] != 480 or frame.shape[1] != 640:
                frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)

            width, height = self.parent_process.page_dashboard.get_preview_size()
            
            # Only update preview if we have valid dimensions
            if width > 0 and height > 0:
                preview_pixmap = self.cv2_image_to_pixmap(frame, width, height)

                if preview_pixmap is None:
                    self.sig_preview_clear.emit()
                else:
                    self.sig_preview_update.emit(preview_pixmap)

            if RouteHandler.route is None:
                self.sig_status_update.emit("No route loaded", False, False)
                return
            elif RouteHandler.route.splits is None or len(RouteHandler.route.splits) == 0:
                self.sig_status_update.emit("Route has no splits", False, False)
                return
            else:
                if not self.livesplit.connected:
                    self.sig_status_update.emit("Livesplit not connected", False, False)
                    return
                    
                if not self.run_started and not self.wait_for_first_split:
                    if self.wait_for_reset:
                        self.sig_status_update.emit("Waiting for livesplit to reset", True, False)
                        return

                    if RouteHandler.route.start_condition == "livesplit":
                        self.sig_status_update.emit("Waiting for livesplit to start", False, True)
                        timer = self.livesplit.get_timer()
                        if timer is not None and timer != datetime.timedelta(0, 0, 0, 0, 0, 0):
                            self.start_run()
                            print("Start")
                        return
                    elif RouteHandler.route.start_condition == "first_split":
                        self.current_split_index = 0
                        self.current_component_index = 0
                        self.wait_for_first_split = True

                        try:
                            self.current_split = RouteHandler.route.splits[self.current_split_index]
                        except Exception as e:
                            logging.exception(e)
                            return

                        try:
                            self.current_component = self.current_split.components[self.current_component_index]
                        except Exception as e:
                            logging.exception(e)
                            return

                        self.sig_next_split.emit()

                if self.current_split is None:
                    if len(RouteHandler.route.splits) > 0:
                        try:
                            self.current_split = RouteHandler.route.splits[self.current_split_index]
                        except:
                            pass

                if self.current_split is None:
                    self.sig_status_update.emit("Route has no splits", True, False)

                if self.current_split is not None:
                    if self.current_component is None:
                        try:
                            self.current_component = self.current_split.components[self.current_component_index]
                        except:
                            pass

                    if self.current_component is None:
                        self.sig_status_update.emit("Current split has no components", True, False)

                    if self.current_component is not None:
                        # Handle load detection based on current split's load type
                        self.handle_load_detection(frame)

        except Exception as e:
            logging.exception(f"Error in update loop: {e}")
            self.sig_preview_clear.emit()

    def handle_load_detection(self, frame):
        """Handle load detection using ONNX classifiers"""
        current_time = time.time()
        
        # Cooldown to prevent multiple detections
        if current_time - self.last_load_time < self.load_cooldown:
            return

        # Get the current split's load type
        current_load_type = getattr(self.current_split, 'load_type', 'regular_fade')
        
        # First load in a level is always a banner load
        if self.load_count == 0:
            # Check for banner load
            if self.banner_detector.detect_banners(frame):
                self.handle_load_detected("banner_load")
                return
        else:
            # Subsequent loads use the split's specified load type
            if current_load_type == "banner_load":
                if self.banner_detector.detect_banners(frame):
                    self.handle_load_detected("banner_load")
            elif current_load_type in ["regular_fade", "tower_castle", "ghost_house"]:
                if self.fade_detector.detect_fade_sequence(frame, current_load_type):
                    self.handle_load_detected(current_load_type)

    def handle_load_detected(self, load_type):
        """Process a detected load"""
        current_time = time.time()
        self.last_load_time = current_time
        self.current_load_type = load_type
        
        print(f"Load detected: {load_type}")
        
        # Update load count
        self.load_count += 1
        if hasattr(self.current_split, 'actual_loads'):
            self.current_split.actual_loads = self.load_count
        
        # Update UI
        self.set_load_count(self.load_count)
        
        # Print load count update
        print(f"Load count: {self.load_count}/{self.current_split.expected_loads}")
        
        # Handle timer control based on load state
        self.control_timer_based_on_load_state()
        
        # Check if we've reached the expected number of loads for this split
        if self.load_count >= self.current_split.expected_loads:
            self.handle_final_load()

    def control_timer_based_on_load_state(self):
        """Control LiveSplit timer based on load state"""
        if not self.is_in_load_state:
            # Entering load state - pause timer
            self.is_in_load_state = True
            self.livesplit.pause_timer()
            print("Timer paused - entering load state")
        else:
            # Already in load state, check if we should resume
            self.frames_since_last_load += 1
            
            # Resume timer after 10 frames of being out of load state
            if self.frames_since_last_load > 10:
                self.is_in_load_state = False
                self.livesplit.resume_timer()
                print("Timer resumed - exiting load state")
                self.frames_since_last_load = 0

    def handle_final_load(self):
        """Handle the final load in a split"""
        print("Final load reached for split")
        
        # Wait for fade-in completion
        self.waiting_for_fadein = True
        
        # Split after a short delay (simulating the 10 frames mentioned)
        def delayed_split():
            if self.current_split and self.current_split.split:
                self.livesplit.split_timer()
                print("Split executed")
            self.next_split()
        
        # Use a QTimer or similar for the delay, but for simplicity we'll track frames
        self.frames_until_split = 10

    def update_frame_count(self):
        """Update frame counter for delayed actions"""
        if self.waiting_for_fadein and self.frames_until_split > 0:
            self.frames_until_split -= 1
            if self.frames_until_split <= 0:
                if self.current_split and self.current_split.split:
                    self.livesplit.split_timer()
                    print("Split executed after fade-in")
                self.waiting_for_fadein = False
                self.next_split()

    def start_run(self):
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.livesplit.start_timer()
        self.run_started = True
        self.current_split_index = 0

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        self.current_component_index = 0
        self.load_count = 0
        self.is_in_load_state = False

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_next_split.emit()

    def component_activated(self):
        print("Component Activated")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.set_activations(self.activations + 1)

        if self.activations >= self.current_component.activations:
            self.current_component_index += 1
            self.activations = 0

        if self.current_component_index >= len(self.current_split.components):
            self.next_split()
            return

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

    def next_split(self):
        if not self.run_started and not self.wait_for_first_split:
            return

        print("Next Split")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        if self.current_split.split:
            if self.wait_for_first_split:
                self.run_started = True
                self.wait_for_first_split = False
                self.livesplit.start_timer()
            else:
                self.livesplit.split_timer()

        self.current_split_index += 1

        if self.current_split_index >= len(RouteHandler.route.splits):
            self.sig_next_split.emit()
            self.run_started = False
            self.wait_for_reset = True
            print("Run Finished")
            return

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        if self.current_split.reset_load_count:
            self.load_count = 0

        self.current_component_index = 0
        self.activations = 0
        self.waiting_for_fadein = False
        self.is_in_load_state = False
        self.frames_since_last_load = 0

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_next_split.emit()

    def skip_split(self):
        if not self.run_started:
            return

        print("Skip Split")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.current_split_index += 1

        if self.current_split_index >= len(RouteHandler.route.splits):
            self.current_split_index = len(RouteHandler.route.splits) - 1
            return

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        if self.current_split.reset_load_count:
            self.load_count = 0

        self.current_component_index = 0
        self.activations = 0
        self.waiting_for_fadein = False
        self.is_in_load_state = False

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_next_split.emit()

    def undo_split(self):
        print("Undo Split")
        if RouteHandler.route is None:
            logging.warning("No route is currently loaded")
            return

        self.current_split_index -= 1

        if self.current_split_index < 0:
            self.current_component_index = 0
            return

        try:
            self.current_split = RouteHandler.route.splits[self.current_split_index]
        except Exception as e:
            logging.exception(e)
            return

        self.current_component_index = 0
        self.activations = 0
        self.waiting_for_fadein = False
        self.is_in_load_state = False

        try:
            self.current_component = self.current_split.components[self.current_component_index]
        except Exception as e:
            logging.exception(e)
            return

        self.sig_prev_split.emit()

    def reset_run(self):
        print("Reset")
        self.livesplit.reset_timer()
        self.current_split_index = 0
        self.current_split = None
        self.current_component_index = 0
        self.current_component = None
        self.load_count = 0
        self.activations = 0
        self.run_started = False
        self.wait_for_first_split = False
        self.wait_for_reset = False
        self.waiting_for_fadein = False
        self.is_in_load_state = False
        self.frames_since_last_load = 0
        self.banner_detector.reset()
        self.fade_detector.reset()
        self.sig_reset_splits.emit()

    def set_activations(self, value):
        self.activations = value
        if self.current_component is not None:
            self.sig_component_activated.emit(self.activations, self.current_component.activations)

    def set_load_count(self, value):
        self.load_count = value
        if self.current_split is not None and hasattr(self.current_split, 'expected_loads'):
            self.sig_load_count_changed.emit(self.load_count, self.current_split.expected_loads)