import sys
import cv2
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Signal, Qt
from pygrabber.dshow_graph import FilterGraph

# Function to get the names of video devices using pygrabber
def get_video_device_names():
    graph = FilterGraph()
    return graph.get_input_devices()

# Function to check if a device index is valid
def is_device_active(val_index):
    cap = cv2.VideoCapture(val_index)
    if cap.isOpened():
        ret, _ = cap.read()
        cap.release()
        return ret
    return False

# Get the device names
device_names = get_video_device_names()

# Check the first 10 indexes or the number of devices available
max_checks = min(10, len(device_names))
active_devices = []

for index in range(max_checks):
    if is_device_active(index):
        active_devices.append((index, device_names[index]))

# GUI Code using PySide6
class FootagePopup(QMainWindow):
    device_selected = Signal(int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Video Device")
        self.setFixedSize(300, 150)  # Adjust size as needed

        layout = QVBoxLayout()

        device_label = QLabel("Select an active video device:")
        layout.addWidget(device_label)

        self.device_combobox = QComboBox()
        self.device_combobox.addItems([name for _, name in active_devices])
        self.device_combobox.setObjectName("device_combobox")
        layout.addWidget(self.device_combobox)

        self.ok_button = QPushButton("OK")
        self.ok_button.setObjectName("ok_button")
        self.ok_button.clicked.connect(self.on_ok)
        layout.addWidget(self.ok_button, 0, Qt.AlignmentFlag.AlignCenter)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)
        self.set_styles()

    def set_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #303030;
            }

            QLabel {
                color: white;
                font-size: 16px;
                font-family: Calibri;
            }

            QComboBox {
                color: white;
                background-color: #252525;
                border: 1px solid #828790;
                font-size: 16px;
                font-family: Calibri;
                padding: 5px;
            }

            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #828790;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }

            QComboBox::down-arrow {
                image: url(noimage);
            }

            QComboBox QListView {
                background-color: #252525;
                color: white;
                border: 1px solid #828790;
                selection-background-color: #00aaff;
            }

            QPushButton#ok_button {
                color: white;
                background-color: #252525;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }

            QPushButton#ok_button:hover {
                background-color: #dadada;
            }

            QPushButton#ok_button:pressed {
                background-color: #00aaff;
            }
        """)

    def on_ok(self):
        selected_index = self.device_combobox.currentIndex()
        device_index = active_devices[selected_index][0]
        print(f"Selected Device: {device_index}")
        self.device_selected.emit(device_index)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FootagePopup()
    window.show()
    app.exec()
