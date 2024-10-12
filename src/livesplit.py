import livesplit
import socket
from PyQt6.QtCore import QThread, pyqtSignal

class LivesplitConnection(QThread):
    sig_connection_status = pyqtSignal(bool)  # connected

    def __init__(self, ip="127.0.0.1", port=16834):
        QThread.__init__(self)
        self.ip = ip
        self.port = port
        self.connected = False
        self.ls = None

    def run(self):
        pass  # No continuous checking in the background

    def connect(self):
        if self.check_server():
            try:
                self.ls = livesplit.Livesplit(ip=self.ip, port=self.port)
                self.connected = True
                self.sig_connection_status.emit(True)
            except Exception as e:
                self.connected = False
                self.sig_connection_status.emit(False)
        else:
            self.connected = False
            self.sig_connection_status.emit(False)

    def check_server(self):
        try:
            with socket.create_connection((self.ip, self.port), timeout=2):
                return True
        except Exception:
            return False

    def start_timer(self):
        if self.connected:
            try:
                self.ls.startTimer()
            except Exception as e:
                print(f"Error starting timer: {e}")

    def split_timer(self):
        if self.connected:
            try:
                self.ls.split()
            except Exception as e:
                print(f"Error splitting timer: {e}")

    def reset_timer(self):
        if self.connected:
            try:
                self.ls.reset()
            except Exception as e:
                print(f"Error resetting timer: {e}")
