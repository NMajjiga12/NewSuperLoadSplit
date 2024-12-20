# crop_settings.py
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QApplication, QSpacerItem
from src.settings.threshold_output import ThresholdOutputWidget


class CropSettingsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.set_styles()

    def init_ui(self):
        # Main horizontal layout to add the line
        main_h_layout = QHBoxLayout()
        self.setLayout(main_h_layout)

        # Main layout for the widget
        main_layout = QVBoxLayout()

        # Create input fields with labels for X, Y, Width, and Height
        self.x_input = QLineEdit()
        self.x_input.setFixedHeight(20)
        self.x_input.setFixedWidth(100)
        self.x_input.setObjectName("x_input")

        self.y_input = QLineEdit()
        self.y_input.setFixedHeight(20)
        self.y_input.setFixedWidth(100)
        self.y_input.setObjectName("y_input")

        self.width_input = QLineEdit()
        self.width_input.setFixedHeight(20)
        self.width_input.setFixedWidth(100)
        self.width_input.setObjectName("width_input")

        self.height_input = QLineEdit()
        self.height_input.setFixedHeight(20)
        self.height_input.setFixedWidth(100)
        self.height_input.setObjectName("height_input")

        # Arrange input fields and labels vertically
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

        # Add a spacer to push the button down
        spacer = QSpacerItem(0, 5)
        main_layout.addItem(spacer)

        # Create an Apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFixedHeight(35)
        self.apply_button.setFixedWidth(100)
        self.apply_button.setObjectName("apply_button")
        main_layout.addWidget(self.apply_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Create a line widget
        line_widget = QWidget()
        line_widget.setFixedWidth(1)
        line_widget.setStyleSheet("background-color: white;")

        # Add the line and main layout to the horizontal layout
        main_h_layout.addLayout(main_layout)
        main_h_layout.addWidget(line_widget)

        # Add ThresholdOutputWidget to the right of the crop settings, aligned to the top
        self.threshold_output_widget = ThresholdOutputWidget()  # Create an instance of ThresholdOutputWidget
        main_h_layout.addWidget(self.threshold_output_widget, alignment=Qt.AlignmentFlag.AlignTop)  # Add with top alignment

    def set_styles(self):
        """Applies the stylesheet to the widget"""
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
        """Sets the crop values in the input fields"""
        self.x_input.setText(str(x))
        self.y_input.setText(str(y))
        self.width_input.setText(str(width))
        self.height_input.setText(str(height))

    def get_crop_values(self):
        """Gets the crop values from the input fields"""
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
