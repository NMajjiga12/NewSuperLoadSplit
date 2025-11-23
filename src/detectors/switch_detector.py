import numpy as np

class SwitchDetector:
    def __init__(self):
        self.switch_pixels = 0
        self.prev_switch_pixel_count = 0
        self.switch_detected = False
        self.switch_checked = False
        
        # Define color thresholds for switch detection
        self.white_threshold = np.array([245, 245, 243])
        self.pale_blue_threshold = np.array([235, 239, 239])
        self.light_cyan_threshold = np.array([216, 231, 232])
        
        # Define the region of interest for switch detection
        self.roi_x1, self.roi_y1 = 494, 278  # Top-left corner
        self.roi_x2, self.roi_y2 = 582, 296  # Bottom-right corner

    def update(self, frame):
        """Update switch detection state"""
        # Reset detection state
        self.switch_detected = False
        
        # Extract the region of interest
        frame_crop = frame[self.roi_y1:self.roi_y2, self.roi_x1:self.roi_x2]
        
        if frame_crop.size == 0:
            return False

        # Count pixels matching our color criteria
        white_pixels = np.sum(np.all(frame_crop >= self.white_threshold - 10, axis=2))
        pale_blue_pixels = np.sum(np.all((frame_crop >= self.pale_blue_threshold - 10) & 
                                        (frame_crop <= self.pale_blue_threshold + 10), axis=2))
        light_cyan_pixels = np.sum(np.all((frame_crop >= self.light_cyan_threshold - 10) & 
                                         (frame_crop <= self.light_cyan_threshold + 10), axis=2))
        
        total_matching_pixels = white_pixels + pale_blue_pixels + light_cyan_pixels
        total_pixels = frame_crop.shape[0] * frame_crop.shape[1]
        
        # Require majority of pixels to match our color criteria
        if total_matching_pixels > total_pixels * 0.6:  # 60% threshold
            self.switch_pixels = total_matching_pixels
            self.switch_detected = True
        else:
            self.switch_pixels = 0
            self.switch_detected = False

    def check_switch_hit(self):
        """Check if switch was hit"""
        if not self.switch_checked and self.switch_detected:
            self.switch_checked = True
            return True
        else:
            return False

    def reset(self):
        """Reset detector state"""
        self.switch_pixels = 0
        self.prev_switch_pixel_count = 0
        self.switch_detected = False
        self.switch_checked = False