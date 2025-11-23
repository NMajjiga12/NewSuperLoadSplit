import numpy as np
import cv2
import onnxruntime

from src.classifiers.classifier import Classifier
from src.classifiers.banner_load_preprocessor import BannerLoadPreprocessor


class BannerLoadDetector:
    def __init__(self):
        self.preprocessor = BannerLoadPreprocessor()
        opts = onnxruntime.SessionOptions()
        opts.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
        self.classifier = Classifier("banner_load.onnx", self.preprocessor, opts, threshold=5)
        self.last_detection_time = 0
        self.detection_cooldown = 2.0  # seconds
        self.is_active = False

    def detect_banners(self, frame):
        """Detect banner loads using the ONNX model"""
        current_time = cv2.getTickCount() / cv2.getTickFrequency()
        
        # Cooldown to prevent multiple detections
        if current_time - self.last_detection_time < self.detection_cooldown:
            return False

        if self.classifier.model is None:
            return False

        try:
            is_load = self.classifier.update(frame)
            
            if is_load and not self.is_active:
                self.is_active = True
                self.last_detection_time = current_time
                print("Banner load detected!")
                return True
            elif not is_load:
                self.is_active = False
                
            return False
        except Exception as e:
            print(f"Error in banner load detection: {e}")
            return False

    def detect_world_label(self, frame):
        """Specifically detect the world label text in top banner"""
        # Crop top region
        height, width = frame.shape[:2]
        top_region = frame[0:int(height*0.15), :]
        
        # Convert to grayscale and threshold
        gray = cv2.cvtColor(top_region, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Look for text-like contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        text_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            
            # Text typically has specific aspect ratios and sizes
            if area > 100 and 0.1 < aspect_ratio < 10:
                text_contours.append(contour)
        
        return len(text_contours) > 2  # Multiple text elements likely present

    def reset(self):
        """Reset detector state"""
        self.is_active = False
        self.last_detection_time = 0