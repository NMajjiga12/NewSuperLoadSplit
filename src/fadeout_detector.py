import cv2
import numpy as np

class FadeoutDetector:
    def __init__(self):
        self.is_fadeout = False

    def detect_fadeout(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Check if most pixels are dark (to differentiate from dark levels)
        dark_pixel_threshold = 10  # Pixel value below which we consider it "dark"
        dark_pixel_ratio_threshold = 0.98  # Ratio of pixels that need to be dark to consider it a fadeout
        num_dark_pixels = np.sum(gray_frame < dark_pixel_threshold)
        total_pixels = gray_frame.size
        dark_pixel_ratio = num_dark_pixels / total_pixels

        fadeout_detected = dark_pixel_ratio >= dark_pixel_ratio_threshold

        if fadeout_detected and not self.is_fadeout:
            self.is_fadeout = True
            return 'fadeout'
        elif not fadeout_detected and self.is_fadeout:
            self.is_fadeout = False
            return 'fadein'

        return None