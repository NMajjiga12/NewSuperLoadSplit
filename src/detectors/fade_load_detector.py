import numpy as np
import time
import cv2
import onnxruntime

from src.classifiers.classifier import Classifier
from src.classifiers.fade_load_preprocessor import FadeLoadPreprocessor
from src.classifiers.ghost_house_preprocessor import GhostHousePreprocessor
from src.classifiers.tower_castle_preprocessor import TowerCastlePreprocessor


class FadeLoadDetector:
    def __init__(self):
        # Classifiers for different load types
        self.fade_classifier = None
        self.ghost_house_classifier = None
        self.tower_castle_classifier = None
        
        # Model Paths
        self.fade_model_path = 'models/fade_load.onnx'
        
        # Parameters
        self.fade_thresh = 5
        self.ghost_house_thresh = 5
        self.tower_castle_thresh = 5
        
        self.fade_detected = False
        self.fade_checked = False
        self.current_load_type = "regular_fade"
        
        self.last_detection_time = 0
        self.detection_cooldown = 2.0

    def load_models(self, opts):
        """Load all fade load ONNX models"""
        self.fade_classifier = Classifier(self.fade_model_path, FadeLoadPreprocessor(), opts, self.fade_thresh)
        self.ghost_house_classifier = Classifier(self.fade_model_path, GhostHousePreprocessor(), opts, self.ghost_house_thresh)
        self.tower_castle_classifier = Classifier(self.fade_model_path, TowerCastlePreprocessor(), opts, self.tower_castle_thresh)

    def update(self, frame, load_type="regular_fade"):
        """Update fade detection state based on load type"""
        current_time = time.time()
        self.current_load_type = load_type
        
        # Cooldown to prevent multiple detections
        if current_time - self.last_detection_time < self.detection_cooldown:
            return False

        # Select appropriate classifier based on load type
        classifier = self.fade_classifier
        if load_type == "ghost_house" and self.ghost_house_classifier:
            classifier = self.ghost_house_classifier
        elif load_type == "tower_castle" and self.tower_castle_classifier:
            classifier = self.tower_castle_classifier

        if classifier and classifier.update(frame):
            self.fade_detected = True
            self.last_detection_time = current_time
            return True
        
        # Reset if classifier indicates no fade
        if classifier and classifier.check_reset():
            self.fade_detected = False
            self.fade_checked = False
            
        return False

    def check_fade_load(self):
        """Check if fade load was detected"""
        if not self.fade_checked and self.fade_detected:
            self.fade_checked = True
            self.fade_detected = False  # Reset for next detection
            return True
        else:
            return False

    def reset(self):
        """Reset detector state"""
        self.fade_detected = False
        self.fade_checked = False
        self.last_detection_time = 0
        self.current_load_type = "regular_fade"