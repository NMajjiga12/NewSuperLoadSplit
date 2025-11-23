import numpy as np
import time
import cv2
import onnxruntime

from src.classifiers.classifier import Classifier
from src.classifiers.banner_load_preprocessor import BannerLoadPreprocessor


class BannerLoadDetector:
    def __init__(self):
        # Classifier
        self.banner_classifier = None
        
        # Model Path
        self.banner_model_path = 'models/banner_load.onnx'
        
        # Parameters
        self.banner_thresh = 5
        self.banner_detected = False
        self.banner_checked = False
        self.last_detection_time = 0
        self.detection_cooldown = 2.0

    def load_model(self, opts):
        """Load the banner load ONNX model"""
        self.banner_classifier = Classifier(self.banner_model_path, BannerLoadPreprocessor(), opts, self.banner_thresh)

    def update(self, frame):
        """Update banner detection state"""
        current_time = time.time()
        
        # Cooldown to prevent multiple detections
        if current_time - self.last_detection_time < self.detection_cooldown:
            return False

        if self.banner_classifier and self.banner_classifier.update(frame):
            self.banner_detected = True
            self.last_detection_time = current_time
            return True
        
        # Reset if classifier indicates no banner
        if self.banner_classifier and self.banner_classifier.check_reset():
            self.banner_detected = False
            self.banner_checked = False
            
        return False

    def check_banner_load(self):
        """Check if banner load was detected"""
        if not self.banner_checked and self.banner_detected:
            self.banner_checked = True
            self.banner_detected = False  # Reset for next detection
            return True
        else:
            return False

    def reset(self):
        """Reset detector state"""
        self.banner_detected = False
        self.banner_checked = False
        self.last_detection_time = 0