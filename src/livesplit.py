import socket
from PyQt6.QtCore import QThread, pyqtSignal

class LivesplitConnection(QThread):
    sig_connection_status = pyqtSignal(bool)  # connected

    def __init__(self, ip="127.0.0.1", port=16834):
        QThread.__init__(self)
        self.ip = ip
        self.port = port
        self.connected = False
        self.socket = None

    def run(self):
        pass  # No continuous checking in the background

    def connect(self):
        if self.check_server():
            try:
                self.socket = socket.create_connection((self.ip, self.port))
                self.connected = True
                self.sig_connection_status.emit(True)
            except Exception as e:
                self.connected = False
                self.sig_connection_status.emit(False)
                print(f"Connection error: {e}")
        else:
            self.connected = False
            self.sig_connection_status.emit(False)

    def check_server(self):
        try:
            with socket.create_connection((self.ip, self.port), timeout=0.1):
                return True
        except Exception:
            return False

    def send_command(self, command):
        if self.connected and self.socket:
            try:
                self.socket.sendall(f"{command}\r\n".encode())
            except Exception as e:
                print(f"Error sending command '{command}': {e}")

    def start_timer(self):
        self.send_command("starttimer")

    def split_timer(self):
        self.send_command("split")

    def reset_timer(self):
        self.send_command("reset")

    def pause_timer(self):
        self.send_command("pausegametime")

    def unpause_timer(self):
        self.send_command("unpausegametime")

    def close_connection(self):
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
            finally:
                self.connected = False
                self.sig_connection_status.emit(False)
