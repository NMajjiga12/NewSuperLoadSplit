from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QApplication

from src.Livesplit.livesplit import LivesplitConnection
from src.dashboard.detection_optimizer import DetectionWorker
from src.route_editor.route_editor import RouteEditor  # Import RouteEditor
from src.start_detector import StartDetector  # Import StartDetector class
from src.fadeout_detector import FadeoutDetector  # Import FadeoutDetector class


class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Video Device")
        self.init_ui()
        self.livesplit = LivesplitConnection()  # Assuming the default IP and port
        self.timer_started = False

        self.start_detector = StartDetector()  # Initialize StartDetector
        self.fadeout_detector = FadeoutDetector()  # Initialize FadeoutDetector

        # Create the detection worker thread
        self.detection_worker = DetectionWorker(self.start_detector, self.fadeout_detector)
        self.detection_worker.detection_result.connect(self.handle_detection_result)
        self.detection_worker.start()

        # Frame update timer
        self.timer = QTimer(self)
        self.timer.start(17)  # Targeting ~60 fps

    def init_ui(self):
        main_layout = QVBoxLayout()

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

        main_layout.addWidget(self.split_list_widget)  # Only add the split list widget

        # Initialize RouteEditor and connect signal
        self.route_editor = RouteEditor(self)
        self.route_editor.splits_updated.connect(self.update_split_list)

        self.setLayout(main_layout)

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

    def update_split_list(self, splits):
        self.split_list_widget.clear()
        self.split_list_widget.addItems(splits)

    def closeEvent(self, event):
        if hasattr(self, 'detection_worker'):
            self.detection_worker.stop()
        event.accept()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = VideoWidget()
    widget.show()
    app.exec()
