from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QApplication
from PyQt6.QtCore import Qt

class CropSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.set_styles()

    def init_ui(self):
        self.setWindowTitle("Crop Settings")
        self.setFixedSize(250, 350)  # Adjust height for larger input boxes

        main_layout = QVBoxLayout()

        self.x_input = QLineEdit()
        self.x_input.setFixedHeight(30)  # Increase the height of the input box
        self.x_input.setObjectName("x_input")

        self.y_input = QLineEdit()
        self.y_input.setFixedHeight(30)  # Increase the height of the input box
        self.y_input.setObjectName("y_input")

        self.width_input = QLineEdit()
        self.width_input.setFixedHeight(30)  # Increase the height of the input box
        self.width_input.setObjectName("width_input")

        self.height_input = QLineEdit()
        self.height_input.setFixedHeight(30)  # Increase the height of the input box
        self.height_input.setObjectName("height_input")

        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("X"))
        input_layout.addWidget(self.x_input)
        input_layout.addWidget(QLabel("Y"))
        input_layout.addWidget(self.y_input)
        input_layout.addWidget(QLabel("Width"))
        input_layout.addWidget(self.width_input)
        input_layout.addWidget(QLabel("Height"))
        input_layout.addWidget(self.height_input)

        main_layout.addLayout(input_layout)

        self.apply_button = QPushButton("Apply")
        self.apply_button.setObjectName("apply_button")
        main_layout.addWidget(self.apply_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

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

            QLineEdit {
                color: white;
                background-color: #252525;
                border: 1px solid #828790;
                font-size: 16px;
                font-family: Calibri;
            }

            QPushButton#apply_button {
                color: white;
                background-color: #252525;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }

            QPushButton#apply_button:hover {
                background-color: #dadada;
            }

            QPushButton#apply_button:pressed {
                background-color: #00aaff;
            }
        """)

    def set_crop_values(self, x, y, width, height):
        self.x_input.setText(str(x))
        self.y_input.setText(str(y))
        self.width_input.setText(str(width))
        self.height_input.setText(str(height))

    def get_crop_values(self):
        return (
            int(self.x_input.text()),
            int(self.y_input.text()),
            int(self.width_input.text()),
            int(self.height_input.text())
        )

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    widget = CropSettingsWidget()
    widget.show()
    sys.exit(app.exec())
