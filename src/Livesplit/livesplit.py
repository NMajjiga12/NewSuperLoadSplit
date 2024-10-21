import socket

from PyQt6.QtCore import QThread, pyqtSignal

class LivesplitConnection(QThread):
    sig_connection_status = pyqtSignal(bool)  # connected

    def __init__(self, ip="127.0.0.1", port=16834, check_interval=1000):
        super().__init__()
        self.ip = ip
        self.port = port
        self.connected = False
        self.socket = None
        self.check_interval = check_interval  # Interval to check the server status (milliseconds)
        self.running = True

    def run(self):
        """ Continuously check the server status in the background. """
        while self.running:
            self.check_connection_status()
            self.msleep(self.check_interval)  # Sleep for a while before checking again

    def check_connection_status(self):
        """Check if the LiveSplit server is running and emit the status."""
        if self.check_server():
            if not self.connected:  # If it's not marked as connected, mark it as connected
                self.connected = True
                self.sig_connection_status.emit(True)
        else:
            if self.connected:  # If it's marked as connected, mark it as disconnected
                self.connected = False
                self.sig_connection_status.emit(False)

    def check_server(self):
        """Try to establish a connection to the LiveSplit server to see if it's running."""
        try:
            with socket.create_connection((self.ip, self.port), timeout=0.1):
                return True
        except Exception:
            return False

    def send_command(self, command):
        """Send a command to the LiveSplit server."""
        if self.connected and self.socket:
            try:
                self.socket.sendall(f"{command}\r\n".encode())
            except Exception as e:
                print(f"Error sending command '{command}': {e}")

    def start_timer(self):
        """Start the timer."""
        self.send_command("starttimer")

    def split_timer(self):
        """Split the timer."""
        self.send_command("split")

    def reset_timer(self):
        """Reset the timer."""
        self.send_command("reset")

    def pause_timer(self):
        """Pause the game timer."""
        self.send_command("pausegametime")

    def unpause_timer(self):
        """Unpause the game timer."""
        self.send_command("unpausegametime")

    def stop(self):
        """Stop the connection check."""
        self.running = False
        self.quit()
        self.wait()

    def close_connection(self):
        """Close the socket connection."""
        if self.socket:
            try:
                self.socket.close()
            except Exception as e:
                print(f"Error closing socket: {e}")
            finally:
                self.connected = False
                self.sig_connection_status.emit(False)