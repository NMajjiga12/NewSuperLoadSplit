import numpy as np
import cv2
import onnxruntime
import time

from src.classifiers.classifier import Classifier
from src.classifiers.fade_load_preprocessor import FadeLoadPreprocessor
from src.classifiers.tower_castle_preprocessor import TowerCastlePreprocessor
from src.classifiers.ghost_house_preprocessor import GhostHousePreprocessor


class FadeLoadDetector:
    def __init__(self):
        self.preprocessor = FadeLoadPreprocessor()
        self.tower_castle_preprocessor = TowerCastlePreprocessor()
        self.ghost_house_preprocessor = GhostHousePreprocessor()
        
        opts = onnxruntime.SessionOptions()
        opts.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        
        self.fade_classifier = Classifier("fade_load.onnx", self.preprocessor, opts, threshold=5)
        self.tower_castle_classifier = Classifier("fade_load.onnx", self.tower_castle_preprocessor, opts, threshold=5)
        self.ghost_house_classifier = Classifier("fade_load.onnx", self.ghost_house_preprocessor, opts, threshold=5)
        
        self.brightness_history = []
        self.fade_threshold = 0.7
        self.black_screen_threshold = 20
        self.max_history_size = 15
        self.last_detection_time = 0
        self.detection_cooldown = 2.0
        self.is_active = False
        self.current_load_type = "regular_fade"

    def detect_fade_sequence(self, frame, load_type="regular_fade"):
        """Detect fade loads using the ONNX model"""
        current_time = time.time()
        
        # Cooldown to prevent multiple detections
        if current_time - self.last_detection_time < self.detection_cooldown:
            return False

        self.current_load_type = load_type
        
        # Select the appropriate classifier based on load type
        if load_type == "tower_castle" and self.tower_castle_classifier.model is not None:
            classifier = self.tower_castle_classifier
        elif load_type == "ghost_house" and self.ghost_house_classifier.model is not None:
            classifier = self.ghost_house_classifier
        elif self.fade_classifier.model is not None:
            classifier = self.fade_classifier
        else:
            return False

        try:
            is_load = classifier.update(frame)
            
            if is_load and not self.is_active:
                self.is_active = True
                self.last_detection_time = current_time
                print(f"{load_type} load detected!")
                return True
            elif not is_load:
                self.is_active = False
                
            return False
        except Exception as e:
            print(f"Error in fade load detection: {e}")
            return False

    def detect_tower_markers(self, frame):
        """Detect tower/castle specific markers during fade loads"""
        # Tower/castle loads often have specific center markers or patterns
        center_x, center_y = frame.shape[1] // 2, frame.shape[0] // 2
        center_region = frame[center_y-50:center_y+50, center_x-50:center_x+50]
        
        if center_region.size == 0:
            return False
            
        gray_center = cv2.cvtColor(center_region, cv2.COLOR_RGB2GRAY)
        
        # Look for circular patterns
        circles = cv2.HoughCircles(gray_center, cv2.HOUGH_GRADIENT, 1, 20,
                                 param1=50, param2=30, minRadius=10, maxRadius=40)
        
        return circles is not None and len(circles) > 0

    def check_black_screen(self, frame):
        """Check if screen is predominantly black"""
        avg_brightness = np.mean(cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY))
        return avg_brightness < self.black_screen_threshold

    def reset(self):
        """Reset detector state"""
        self.is_active = False
        self.last_detection_time = 0
        self.brightness_history.clear()