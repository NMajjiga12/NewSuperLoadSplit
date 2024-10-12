from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout

class LiveSplitDialog(QDialog):
    def __init__(self, connected, livesplit, parent=None):
        super().__init__(parent)
        self.livesplit = livesplit
        self.setWindowTitle("LiveSplit Status")
        self.init_ui(connected)
        self.set_styles()

    def init_ui(self, connected):
        layout = QVBoxLayout()

        status_label = QLabel("LiveSplit is connected." if connected else "LiveSplit is not connected.")
        status_label.setObjectName("title_label")
        if connected:
            status_label.setStyleSheet("color: #00dbdb; font-size: 20px;")
        else:
            status_label.setStyleSheet("color: #FF47FC; font-size: 24px;")  # Increased font size for "not connected" text
        layout.addWidget(status_label)

        if not connected:
            instruction_label = QLabel(
                "To connect LiveSplit follow the steps here:\n"
                "1. Open LiveSplit, right-click the window and go to edit layout\n"
                "2. Click on the plus button in the top-left corner, and go to controls --> LiveSplit Server and add it to your layout\n"
                "3. Click OK to save changes, then enable the server by right-clicking and selecting Control -> Start Server.\n"
                "4. Close out of this window and reclick on the connect LiveSplit button"
            )
            instruction_label.setObjectName("instruction_label")
            layout.addWidget(instruction_label)

        button_layout = QHBoxLayout()

        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("popup_button")
        self.close_button.clicked.connect(self.close)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def set_styles(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #252525;
                border: 1px solid #828790;
                border-radius: 5px;
            }

            QLabel#title_label {
                font-size: 16px;
                font-family: Calibri;
                padding: 10px;
                border-bottom: 1px solid #828790;
            }

            QLabel#instruction_label {
                color: white;
                font-size: 14px;
                font-family: Calibri;
                padding: 10px;
            }

            QPushButton#popup_button {
                color: white;
                background-color: #252525;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }

            QPushButton#popup_button:hover {
                background-color: #dadada;
            }

            QPushButton#popup_button:pressed {
                background-color: #00aaff;
            }
        """)

# Example usage:
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = LiveSplitDialog(connected=False, livesplit=None)
    dialog.show()
    sys.exit(app.exec())
