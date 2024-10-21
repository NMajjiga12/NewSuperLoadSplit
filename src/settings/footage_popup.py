import sys
import cv2
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QComboBox
from PyQt6.QtCore import pyqtSignal, Qt
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

# GUI Code using PyQt6
class FootagePopup(QWidget):  # Changed from QMainWindow to QWidget
    device_selected = pyqtSignal(int)  # Changed Signal to pyqtSignal

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Select Video Device")
        self.setFixedSize(500, 100)  # Adjust size as needed

        main_layout = QVBoxLayout()

        # Add a label above the device selection for settings title
        settings_label = QLabel("                                Video Capture Device Settings                                ")
        settings_label.setStyleSheet("color: white; font-size: 18px; font-family: Calibri; border: 1px solid #828790;")
        main_layout.addWidget(settings_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create a horizontal layout for the label and combobox
        device_selection_layout = QHBoxLayout()

        device_label = QLabel("   Select Video Capture    ")
        device_selection_layout.addWidget(device_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.device_combobox = QComboBox()
        self.device_combobox.addItem("Select Device")  # Add default prompt option
        self.device_combobox.addItems([name for _, name in active_devices])
        self.device_combobox.setObjectName("device_combobox")
        self.device_combobox.setFixedWidth(300)  # Set the width to 200 pixels (or your desired width)
        self.device_combobox.currentIndexChanged.connect(self.on_ok)  # Connect signal to on_ok method
        device_selection_layout.addWidget(self.device_combobox)

        # Add the horizontal layout to the main layout
        main_layout.addLayout(device_selection_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

        self.set_styles()

    def set_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #303030;
            }

            QLabel {
                background-color: #252525;
                color: white;
                font-size: 16px;
                font-family: Calibri;
                border: 1px solid #828790;
            }

            QComboBox {
                color: white;
                background-color: #252525;
                border: 1px solid #828790;
                font-size: 16px;
                font-family: Calibri;
                padding: 4px;
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
        """)

    def on_ok(self):
        selected_index = self.device_combobox.currentIndex()
        if selected_index == 0:  # If "Select Device" is selected, do nothing
            return
        device_index = active_devices[selected_index - 1][0]  # Adjust index because of "Select Device" option
        print(f"Selected Device: {device_index}")
        self.device_selected.emit(device_index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FootagePopup()
    window.show()
    app.exec()
