import cv2
import os

class StartDetector:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Path to the template image
        self.needle_img_path = os.path.join(script_dir, '..', 'img', 'image.png')
        self.needle_img = cv2.imread(self.needle_img_path, cv2.IMREAD_UNCHANGED)
        assert self.needle_img is not None, f"{self.needle_img_path} could not be read, check with os.path.exists()"
        self.needle_img_gray = cv2.cvtColor(self.needle_img, cv2.COLOR_BGR2RGB)

    def detect(self, frame):
        # Convert frame to grayscale to match the template
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform template matching
        result = cv2.matchTemplate(frame_gray, self.needle_img_gray, cv2.TM_CCOEFF_NORMED)

        # Define a threshold for detection
        threshold = 0.7  # Adjust based on testing and template quality

        # Get the max value from the match result
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Print out the threshold and match value for debugging
        # print(f"Threshold: {threshold}, Max Match Value: {max_val}")

        # Return True if the match value exceeds the threshold
        return max_val >= threshold