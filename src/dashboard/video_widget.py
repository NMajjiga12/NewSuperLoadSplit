import cv2
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, \
    QApplication, QListWidget

from src.Livesplit.livesplit import LivesplitConnection
from src.Livesplit.livesplit_detector import LiveSplitDialog
from src.dashboard.crop_settings import CropSettingsWidget
from src.dashboard.detection_optimizer import DetectionWorker
from src.dashboard.footage_popup import FootagePopup
from src.fadeout_detector import FadeoutDetector
from src.route_editor.route_editor import RouteEditor  # Import RouteEditor
from src.start_detector import StartDetector
from src.virtual_cam import VideoCapture


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Video Device")
        self.init_ui()
        self.crop_settings = None
        self.crop_params = (0, 20, 640, 460)  # Default crop parameters
        self.livesplit = LivesplitConnection()  # Assuming the default IP and port
        self.livesplit.sig_connection_status.connect(self.update_livesplit_status)
        self.video_capture = VideoCapture()  # Initialize VideoCapture
        self.fadeout_detector = FadeoutDetector()  # Initialize FadeoutDetector
        self.start_detector = StartDetector()
        self.timer_started = False

        # Create the detection worker thread
        self.detection_worker = DetectionWorker(self.start_detector, self.fadeout_detector)
        self.detection_worker.detection_result.connect(self.handle_detection_result)
        self.detection_worker.start()

        # Frame update timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(17)  # Targeting ~60 fps


    def init_ui(self):
        main_layout = QVBoxLayout()  # Changed from QHBoxLayout to QVBoxLayout
        top_layout = QHBoxLayout()  # Added to separate top and bottom sections
        video_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.split_list_widget = QListWidget()
        self.split_list_widget.setFixedWidth(200)  # Set fixed width for the list widget
        self.split_list_widget.setFixedHeight(400)  # Set fixed width for the list widget
        self.split_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #252525;
                color: white;
                padding: 5px;
                font-size: 18px;
                font-family: Calibri;
            }
            QListWidget::item:selected {
                background-color: black;
                color: white;
            }
        """)

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        video_layout.addWidget(self.video_label)

        # Add a spacer below the video widget
        spacer_above_button = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        # Detect Virtual Camera button
        self.detect_camera_button = QPushButton("Detect Virtual Camera")
        self.detect_camera_button.setObjectName("detect_camera_button")
        self.detect_camera_button.setStyleSheet("""
            #detect_camera_button {
                color: white;
                background-color: #252525;
                border: none;
                padding: 8px 65px;
                border-radius: 2px;
                font-size: 16px;
            }
            #detect_camera_button:hover {
                background-color: #dadada;
            }
            #detect_camera_button:pressed {
                background-color: #00aaff;
            }
        """)
        self.detect_camera_button.clicked.connect(self.detect_virtual_camera)

        # Connect LiveSplit button
        self.connect_livesplit_button = QPushButton("Connect LiveSplit")
        self.connect_livesplit_button.setObjectName("connect_livesplit_button")
        self.connect_livesplit_button.setStyleSheet("""
            #connect_livesplit_button {
                color: white;
                background-color: #252525;
                border: none;
                padding: 8px 20px;
                border-radius: 2px;
                font-size: 16px;
            }
            #connect_livesplit_button:hover {
                background-color: #dadada;
            }
            #connect_livesplit_button:pressed {
                background-color: #00aaff;
            }
        """)
        self.connect_livesplit_button.clicked.connect(self.check_livesplit_status)

        # Crop Video Footage button
        self.crop_button = QPushButton("Crop Video Footage")
        self.crop_button.setObjectName("crop_button")
        self.crop_button.setStyleSheet("""
            #crop_button {
                color: white;
                background-color: #252525;
                border: none;
                padding: 8px 20px;
                border-radius: 2px;
                font-size: 16px;
            }
            #crop_button:hover {
                background-color: #dadada;
            }
            #crop_button:pressed {
                background-color: #00aaff;
            }
        """)
        self.crop_button.clicked.connect(self.open_crop_settings)

        button_layout.addStretch()
        button_layout.addWidget(self.detect_camera_button)
        button_layout.addWidget(self.connect_livesplit_button)
        button_layout.addWidget(self.crop_button)
        button_layout.setAlignment(self.crop_button, Qt.AlignmentFlag.AlignRight)

        top_layout.addWidget(self.split_list_widget)  # Add the list widget to the top layout
        top_layout.addLayout(video_layout)

        main_layout.addLayout(top_layout)
        main_layout.addItem(spacer_above_button)  # Add the spacer to the main layout below the video widget
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Initialize RouteEditor and connect signal
        self.route_editor = RouteEditor(self)
        self.route_editor.splits_updated.connect(self.update_split_list)

    def open_crop_settings(self):
        if self.crop_settings is None:
            self.crop_settings_widget = CropSettingsWidget()
            self.crop_settings_widget.apply_button.clicked.connect(self.apply_crop_settings)
        self.crop_settings_widget.set_crop_values(*self.crop_params)
        self.crop_settings_widget.show()

    def apply_crop_settings(self):
        # Retrieve values from crop settings and apply to video stream
        self.crop_params = self.crop_settings_widget.get_crop_values()
        self.crop_settings_widget.close()

    def check_livesplit_status(self):
        # Manually check LiveSplit connection status
        self.livesplit.connect()

    def update_livesplit_status(self, connected):
        dialog = LiveSplitDialog(connected, self.livesplit, self)
        dialog.exec()

    def detect_virtual_camera(self):
        self.footage_popup = FootagePopup()  # Create the FootagePopup window
        self.footage_popup.device_selected.connect(self.init_camera)  # Connect signal
        self.footage_popup.show()

    def init_camera(self, device_index):
        print(f"Initializing camera with index {device_index}")
        if self.video_capture.init_capture_device(device_index):
            self.video_capture.capture_device.set(cv2.CAP_PROP_FPS, 60)  # Set frame rate to 60fps
            print("Camera initialized successfully")
        else:
            print("Failed to initialize camera")

    def update_frame(self):
        ret, frame = self.video_capture.get_frame() if self.video_capture else (False, None)
        if ret:
            # Crop the frame if needed
            x, y, width, height = self.crop_params
            frame_height, frame_width, _ = frame.shape
            x = min(max(x, 0), frame_width)
            y = min(max(y, 0), frame_height)
            width = min(width, frame_width - x)
            height = min(height, frame_height - y)
            frame = frame[y:y + height, x:x + width]

            # Convert the frame to RGB format
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Send frame to detection worker for processing
            self.detection_worker.add_frame(rgb_frame)

            # Resize the frame to match the QLabel size if needed
            label_width = self.video_label.width()
            label_height = self.video_label.height()
            if (rgb_frame.shape[1], rgb_frame.shape[0]) != (label_width, label_height):
                rgb_frame = cv2.resize(rgb_frame, (label_width, label_height), interpolation=cv2.INTER_LINEAR)

            # Convert to QImage and display in QLabel
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)

        else:
            # Display a black screen if frame retrieval fails
            self.display_black_screen()

    def handle_detection_result(self, detection_type):
        if detection_type == 'start' and not self.timer_started:
            print('Found needle. Start timer detected.')
            self.livesplit.start_timer()
            self.timer_started = True
        elif detection_type == 'fadeout' and self.timer_started:
            print('Fadeout detected (black screen).')
            self.livesplit.pause_timer()
        elif detection_type == 'fadein' and self.timer_started:
            print('Fadein detected.')
            self.livesplit.unpause_timer()

    def display_black_screen(self):
        # Load a "no signal" image to display
        no_signal_image_path = "../../img/nosignal.png"  # Update with the correct path to the image
        no_signal_pixmap = QPixmap(no_signal_image_path)
        # Resize the pixmap to match the video label size if necessary
        no_signal_pixmap = no_signal_pixmap.scaled(self.video_label.width(), self.video_label.height(),
                                                   Qt.AspectRatioMode.KeepAspectRatio)
        # Set the pixmap to the video label
        self.video_label.setPixmap(no_signal_pixmap)
    def update_split_list(self, splits):
        self.split_list_widget.clear()
        self.split_list_widget.addItems(splits)

    def closeEvent(self, event):
        if self.video_capture:
            self.video_capture.release()
        if hasattr(self, 'detection_worker'):
            self.detection_worker.stop()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = VideoWidget()
    widget.show()
    sys.exit(app.exec())