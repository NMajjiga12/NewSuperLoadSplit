# threshold_output.py
import sys
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QGridLayout, QApplication
from PyQt6.QtCore import Qt

class ThresholdOutputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Create the main layout
        main_layout = QVBoxLayout()

        # Create a grid layout to organize the labels and line edits into separate columns
        grid_layout = QGridLayout()

        # Add headers for each column
        output_header = QLabel("Output Val")
        highest_value_header = QLabel("Highest Val")
        threshold_header = QLabel("Threshold")

        # Apply styles to headers
        output_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        highest_value_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        threshold_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add headers to the grid layout
        grid_layout.addWidget(output_header, 0, 1, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)  # Centered above output QLineEdits
        grid_layout.addWidget(highest_value_header, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignCenter)  # Centered above highest value QLineEdits
        grid_layout.addWidget(threshold_header, 0, 3, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)  # Centered above threshold QLineEdits

        # Create pairs of line edits for outputs, highest values, and thresholds
        output_elements = [
            ("Start Output", False),  # Output fields (not editable)
            ("Banner Output", False),
            ("Reset Output", False),
            ("End Output", False),
        ]

        highest_value_elements = [
            (False),  # Highest Value fields (not editable)
            (False),
            (False),
            (False),
        ]

        threshold_elements = [
            (True),  # Threshold fields (editable)
            (True),
            (True),
            (True),
        ]

        # Set fixed widths for the output, highest value, and threshold line edits
        line_edit_width = 80

        # Add output elements to the first column (starting from row 1)
        for i, (label_text, is_editable) in enumerate(output_elements, start=1):
            output_label = QLabel(label_text)
            output_line_edit = QLineEdit()
            output_line_edit.setReadOnly(not is_editable)
            output_line_edit.setFixedHeight(25)
            output_line_edit.setFixedWidth(line_edit_width)  # Set fixed width for output values

            # Add output label and line edit to the grid layout
            grid_layout.addWidget(output_label, i, 0, alignment=Qt.AlignmentFlag.AlignLeft)
            grid_layout.addWidget(output_line_edit, i, 1)

        # Add highest value line edits to the second column (without labels, starting from row 1)
        for i, is_editable in enumerate(highest_value_elements, start=1):
            highest_value_line_edit = QLineEdit()
            highest_value_line_edit.setReadOnly(not is_editable)
            highest_value_line_edit.setFixedHeight(25)
            highest_value_line_edit.setFixedWidth(line_edit_width)  # Set fixed width for highest value fields

            # Add highest value line edit to the grid layout
            grid_layout.addWidget(highest_value_line_edit, i, 2)

        # Add threshold line edits to the third column (without labels, starting from row 1)
        for i, is_editable in enumerate(threshold_elements, start=1):
            threshold_line_edit = QLineEdit()
            threshold_line_edit.setReadOnly(not is_editable)
            threshold_line_edit.setFixedHeight(25)
            threshold_line_edit.setFixedWidth(line_edit_width)  # Set fixed width for threshold values

            # Add threshold line edit to the grid layout
            grid_layout.addWidget(threshold_line_edit, i, 3, 1, 2)

        # Add the grid layout to the main layout
        main_layout.addLayout(grid_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)
        self.setWindowTitle("Threshold and Output Settings")
        self.resize(600, 150)

        # Apply the stylesheet to the widget
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThresholdOutputWidget()
    window.show()
    sys.exit(app.exec())
