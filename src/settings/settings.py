import sys
import cv2
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QApplication, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
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


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 400)
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # LiveSplit Detection Layout
        livesplit_layout = QVBoxLayout()

        # Title label style for "LiveSplit is not connected."
        livesplit_status_label = QLabel("LiveSplit is not connected.")
        livesplit_status_label.setStyleSheet("""
            color: #FF47FC;
            font-size: 16px;
            font-family: Calibri;
            background-color: #252525;
        """)

        instructions = QLabel(
            "To connect LiveSplit follow the steps here:\n"
            "1. Open LiveSplit, right-click the window and go to edit layout\n"
            "2. Click on the plus button in the top-left corner, and go to controls --> LiveSplit Server\n"
            "3. Click OK to save changes, then enable the server by right-clicking and selecting Control -> Start Server\n"
            "4. Close out of this window and reclick on the connect LiveSplit button"
        )
        instructions.setStyleSheet("color: black; font-size: 12px; font-family: Calibri;")
        instructions.setWordWrap(True)
        livesplit_layout.addWidget(livesplit_status_label)
        livesplit_layout.addWidget(instructions)

        # Virtual Camera Selection Layout
        camera_layout = QHBoxLayout()  # Change to QHBoxLayout
        camera_label = QLabel("Select video device:")
        camera_label.setStyleSheet("""
            color: black;
            font-size: 14px;
            font-family: Calibri;
        """)

        # Apply styles to combo box
        self.camera_combobox = QComboBox()
        self.camera_combobox.setStyleSheet("""
            color: black;
            background-color: #f0f0f0;
            font-family: Calibri;
        """)
        self.camera_combobox.setFixedWidth(200)  # Increase the width of the combo box
        self.camera_combobox.addItems([name for _, name in active_devices])

        # Add label and combobox to the horizontal layout
        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera_combobox)

        # Ensure label and combobox are left-aligned within the row
        camera_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Crop Settings Layout
        crop_layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        crop_params = ["X", "Y", "Width", "Height"]
        self.crop_inputs = {}

        for param in crop_params:
            row_layout = QHBoxLayout()

            # Create a small label
            label = QLabel(param)
            label.setStyleSheet("""
                color: black;
                font-size: 12px;
                font-family: Calibri;
            """)
            label.setFixedWidth(50)  # Reduce the width of the label
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Force label to align left

            # Apply styles to input fields
            input_field = QLineEdit()
            input_field.setStyleSheet("""
                background-color: #f0f0f0;
                color: black;
                font-family: Calibri;
            """)
            input_field.setFixedWidth(60)  # Half-width for the input fields

            row_layout.addWidget(label)
            row_layout.addWidget(input_field)
            row_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)  # Force row to align left
            self.crop_inputs[param] = input_field

            form_layout.addLayout(row_layout)

        # Apply Button Layout (left-aligned)
        apply_button = QPushButton("Apply")

        # Apply styles to button
        apply_button.setStyleSheet("""
            QPushButton {
                color: black;
                background-color: #e0e0e0;
                font-family: Calibri;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #dadada;
                color: black;
            }

            QPushButton:pressed {
                background-color: #00aaff;
                color: white;
            }
        """)
        apply_button.setFixedWidth(115)
        apply_button.clicked.connect(self.apply_crop_settings)

        button_layout = QHBoxLayout()
        button_layout.addWidget(apply_button, alignment=Qt.AlignmentFlag.AlignLeft)  # Align button to the left
        form_layout.addLayout(button_layout)

        crop_layout.addLayout(form_layout)

        # Add sections to main layout
        main_layout.addLayout(livesplit_layout)
        main_layout.addLayout(camera_layout)
        main_layout.addLayout(crop_layout)

        self.setLayout(main_layout)

    def apply_crop_settings(self):
        x = self.crop_inputs["X"].text()
        y = self.crop_inputs["Y"].text()
        width = self.crop_inputs["Width"].text()
        height = self.crop_inputs["Height"].text()
        print(f"Crop Settings Applied: X={x}, Y={y}, Width={width}, Height={height}")


# Main function to run the settings window
def main():
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
