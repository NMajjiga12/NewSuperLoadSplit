import cv2
import os

class StartDetector:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.needle_img_path = os.path.join(script_dir, '..', 'img', 'image.png')
        self.needle_img = cv2.imread(self.needle_img_path, cv2.IMREAD_UNCHANGED)
        assert self.needle_img is not None, f"{self.needle_img_path} could not be read, check with os.path.exists()"
        self.needle_img_gray = cv2.cvtColor(self.needle_img, cv2.COLOR_BGR2GRAY)

    def detect(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(frame_gray, self.needle_img_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        print('Best match top left position: %s' % str(max_loc))
        print('Best match confidence: %s' % max_val)
        return max_val >= 0.85
