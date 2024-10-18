import socket
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal

class LiveSplitConnectionThread(QThread):
    connection_status_changed = pyqtSignal(bool)  # Signal to update connection status

    def __init__(self, ip="127.0.0.1", port=16834, check_interval=1000):
        super().__init__()
        self.ip = ip
        self.port = port
        self.check_interval = check_interval  # Interval to check the server status (milliseconds)
        self.running = True
        self.connected = False

    def run(self):
        """ Continuously check the server status in the background. """
        while self.running:
            current_status = self.check_server()
            if current_status != self.connected:  # Only emit signal if status has changed
                self.connected = current_status
                self.connection_status_changed.emit(self.connected)
            self.msleep(self.check_interval)  # Sleep for a while before checking again

    def check_server(self):
        """Try to establish a connection to the LiveSplit server to see if it's running."""
        try:
            with socket.create_connection((self.ip, self.port), timeout=0.1):
                return True
        except Exception:
            return False

    def stop(self):
        """Stop the background thread."""
        self.running = False
        self.quit()
        self.wait()


class LiveSplitDialog(QDialog):
    def __init__(self, connected=False, livesplit=None, parent=None):
        super().__init__(parent)
        self.livesplit = livesplit
        self.setWindowTitle("LiveSplit Status")
        self.init_ui(connected)
        self.set_styles()

        # Start LiveSplit connection thread to listen for server status
        self.ls_thread = LiveSplitConnectionThread()
        self.ls_thread.connection_status_changed.connect(self.update_status)
        self.ls_thread.start()

    def init_ui(self, connected):
        layout = QVBoxLayout()

        self.status_label = QLabel("LiveSplit is connected." if connected else "LiveSplit is not connected.")
        self.status_label.setObjectName("title_label")
        if connected:
            self.status_label.setStyleSheet("color: #00dbdb; font-size: 20px;")
        else:
            self.status_label.setStyleSheet("color: #FF47FC; font-size: 24px;")
        layout.addWidget(self.status_label)

        self.instruction_label = QLabel(
            "To connect LiveSplit follow the steps here:\n"
            "1. Open LiveSplit, right-click the window and go to edit layout\n"
            "2. Click on the plus button in the top-left corner, and go to controls --> LiveSplit Server and add it to your layout\n"
            "3. Click OK to save changes, then enable the server by right-clicking and selecting Control -> Start Server.\n"
            "4. Close out of this window and reclick on the connect LiveSplit button"
        )
        self.instruction_label.setObjectName("instruction_label")
        layout.addWidget(self.instruction_label)

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

    def update_status(self, connected):
        """Update the UI based on the connection status."""
        if connected:
            self.status_label.setText("LiveSplit is connected.")
            self.status_label.setStyleSheet("color: #00dbdb; font-size: 20px;")
        else:
            self.status_label.setText("LiveSplit is not connected.")
            self.status_label.setStyleSheet("color: #FF47FC; font-size: 24px;")

    def closeEvent(self, event):
        """Stop the connection thread when the window is closed."""
        self.ls_thread.stop()
        event.accept()


# Example usage:
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = LiveSplitDialog(connected=False, livesplit=None)
    dialog.show()
    sys.exit(app.exec())
