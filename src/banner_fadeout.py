import cv2
import numpy as np


class BannerFadeout:
    def __init__(self):
        pass  # No need for image templates, detecting using color now

    def detect(self, frame):
        # Convert to HSV color space to detect yellow
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for yellow color in HSV
        lower_yellow = np.array([15, 80, 80])
        upper_yellow = np.array([35, 255, 255])

        # Create a mask for yellow regions
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Apply morphological operations to close gaps in the mask
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # Create a copy of the original image and apply the mask
        detected_image = cv2.bitwise_and(frame, frame, mask=mask)

        # Use OpenCV's built-in PSNR function to calculate PSNR between original and detected image
        psnr_value = cv2.PSNR(frame, detected_image)
        print('PSNR value:', psnr_value)

        # Define PSNR threshold for detection (adjust as needed)
        threshold = 30.0

        # Return True if yellow banner detected, otherwise False
        if psnr_value >= threshold:
            print("Yellow banner detected.")
        else:
            print("No yellow banner detected.")

        return psnr_value >= threshold