# settings.py
import sys
import cv2
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QGridLayout, QHBoxLayout

# Import from other files
from src.Livesplit.livesplit_detector import LiveSplitDialog
from src.settings.crop_settings import CropSettingsWidget
from src.settings.footage_popup import FootagePopup
from src.settings.footage_popup import active_devices
from src.virtual_cam import VideoCapture  # Import the VideoCapture class


class SettingsWindow(QWidget):
    device_selected = pyqtSignal(int)  # Emit only the selected index
    settings_updated = pyqtSignal(dict)
    crop_settings_updated = pyqtSignal(tuple)  # Signal to emit updated crop settings
    livesplit_status_checked = pyqtSignal()  # Signal to check LiveSplit status

    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)
        self.selected_device_index = None
        self.init_ui()
        self.live_split_thread = None
        self.crop_params = (0, 0, 640, 480)  # Default crop parameters matching the preview size

        # Create and initialize VideoCapture instance
        self.video_capture = VideoCapture()

        # Create a timer to periodically update the video feed
        self.frame_timer = QTimer(self)
        self.frame_timer.timeout.connect(self.update_frame)

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Title label style for "LiveSplit is not connected."
        self.livesplit_dialog = LiveSplitDialog(connected=False)
        self.livesplit_dialog.setFixedHeight(150)
        self.livesplit_dialog.setFixedWidth(810)
        self.livesplit_dialog.connection_status_changed.connect(self.handle_livesplit_connection_status)
        main_layout.addWidget(self.livesplit_dialog)

        # Create a grid layout for the main content
        content_layout = QGridLayout()
        main_layout.addLayout(content_layout)

        # Virtual Camera Selection Layout
        self.footage_popup = FootagePopup()
        self.footage_popup.device_selected.connect(self.handle_device_selection)
        content_layout.addWidget(self.footage_popup, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)

        # Create and configure the CropSettingsWidget on the left (in a separate row)
        self.crop_widget = CropSettingsWidget()
        self.crop_widget.apply_button.clicked.connect(self.apply_crop_settings)
        content_layout.addWidget(self.crop_widget, 1, 0,
                                 alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Add a QLabel to display the video feed from the virtual camera on the right
        self.video_display_label = QLabel(self)
        self.video_display_label.setFixedSize(300, 225)  # Adjusted size to match the requirement
        self.video_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.video_display_label, 0, 1, 2, 1,
                                 alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def open_crop_settings(self):
        self.crop_widget.set_crop_values(*self.crop_params)
        self.crop_widget.show()

    def apply_crop_settings(self):
        self.crop_params = self.crop_widget.get_crop_values()
        self.crop_settings_updated.emit(self.crop_params)
        print(f"Applied crop settings: {self.crop_params}")

    def check_livesplit_status(self):
        self.livesplit_status_checked.emit()

    def handle_livesplit_connection_status(self, connected):
        if connected:
            print("LiveSplit is now connected.")
        else:
            print("LiveSplit is not connected.")

    def handle_device_selection(self, device_index):
        selected_index = next((index for index, (idx, _) in enumerate(active_devices) if idx == device_index), -1)
        self.selected_device_index = selected_index
        self.device_selected.emit(selected_index)
        self.init_camera(selected_index)  # Initialize the camera based on the selected device

    def init_camera(self, selected_index):
        device_index = active_devices[selected_index][0]
        print(f"Initializing camera with device index {device_index}")
        if self.video_capture.init_capture_device(device_index):
            print("Camera initialized successfully")
            self.frame_timer.start(30)  # Start the timer with an interval of 30ms (~33 FPS)
        else:
            print("Failed to initialize camera")
            self.frame_timer.stop()

    def update_frame(self):
        ret, frame = self.video_capture.get_frame() if self.video_capture else (False, None)
        if ret:
            # Apply crop settings to the frame
            x, y, width, height = self.crop_params
            frame_height, frame_width, _ = frame.shape

            # Ensure the crop parameters are within frame boundaries
            x = min(max(x, 0), frame_width)
            y = min(max(y, 0), frame_height)
            width = min(width, frame_width - x)
            height = min(height, frame_height - y)
            cropped_frame = frame[y:y + height, x:x + width]

            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to fit the QLabel size (300x225)
            label_width, label_height = 300, 225
            if (rgb_frame.shape[1], rgb_frame.shape[0]) != (label_width, label_height):
                rgb_frame = cv2.resize(rgb_frame, (label_width, label_height), interpolation=cv2.INTER_LINEAR)

            # Convert to QImage and display in QLabel
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_display_label.setPixmap(pixmap)
        else:
            # Display a black screen if frame retrieval fails
            self.display_black_screen()

    def display_black_screen(self):
        # Set a black pixmap as the placeholder when there's no valid frame
        black_pixmap = QPixmap(self.video_display_label.size())
        black_pixmap.fill(Qt.GlobalColor.black)
        self.video_display_label.setPixmap(black_pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())
