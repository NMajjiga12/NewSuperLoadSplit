from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QMessageBox
from src.vid_capture import VideoCapture
from src.config import Config
from ui.styles import Style
from ui.fonts import *


class PageSettings(QObject):
    sig_capture_device_changed = pyqtSignal(object)
    sig_livesplit_port_changed = pyqtSignal()
    sig_font_size_changed = pyqtSignal(int)

    def __init__(self, ui):
        QObject.__init__(self)
        self.ui = ui
        self.vid_cap = VideoCapture()

        # Widgets
        self.livesplit_port_input = self.ui.page_settings_livesplit_input_port
        self.capture_device_dropdown = self.ui.page_settings_dropdown_capture_device
        self.update_capture_device_btn = self.ui.page_settings_update_capture_device_btn
        self.font_size_dropdown = self.ui.page_settings_font_size

        # Connect signals
        self.livesplit_port_input.textEdited.connect(self.port_edited)
        self.update_capture_device_btn.clicked.connect(self.update_capture_device)
        self.font_size_dropdown.currentTextChanged.connect(self.font_size_changed)

        # Load States From Config with proper defaults
        self.livesplit_port_input.setText(str(Config.get_key("livesplit_port", 16834)))
            
        # Load font size
        font_size = Config.get_key("font_size", 9)
        self.font_size_dropdown.setCurrentText(str(font_size))

    def device_list_updated(self):
        self.capture_device_dropdown.clear()
        device_list = self.vid_cap.get_device_list()
        for index, name in device_list.items():
            self.capture_device_dropdown.addItem(name, int(index))

        current_device = Config.get_key("capture_device", 0)
        index = self.capture_device_dropdown.findData(current_device)
        if index >= 0:
            self.capture_device_dropdown.setCurrentIndex(index)

        self.capture_device_dropdown.currentIndexChanged.connect(self.capture_device_changed)

    def port_edited(self):
        try:
            port_value = int(self.livesplit_port_input.text())
            Config.set_key("livesplit_port", port_value)
            self.sig_livesplit_port_changed.emit()
        except ValueError:
            # Reset to default if invalid input
            self.livesplit_port_input.setText("16834")
            Config.set_key("livesplit_port", 16834)
            self.sig_livesplit_port_changed.emit()

    def capture_device_changed(self):
        current_index = self.capture_device_dropdown.currentIndex()
        if current_index >= 0:
            device_id = self.capture_device_dropdown.itemData(current_index)
            Config.set_key("capture_device", device_id)

    def font_size_changed(self, text):
        try:
            font_size = int(text)
            Config.set_key("font_size", font_size)
            self.sig_font_size_changed.emit(font_size)
        except ValueError:
            pass

    def update_capture_device(self):
        """Update capture device without restarting program"""
        current_index = self.capture_device_dropdown.currentIndex()
        if current_index >= 0:
            device_id = self.capture_device_dropdown.itemData(current_index)
            Config.set_key("capture_device", device_id)
            
            # Emit signal to update capture device
            self.sig_capture_device_changed.emit(device_id)
            
            # Show feedback to user
            QMessageBox.information(self.ui, "Success", f"Capture device updated to: {self.capture_device_dropdown.currentText()}")

    def update_font_size(self, font_size):
        """Update font size for settings page elements"""
        small_font = QFont("Montserrat", font_size - 1)
        regular_font = QFont("Montserrat", font_size)
        title_font = QFont("Montserrat", font_size)
        title_font.setBold(True)
        
        self.ui.page_settings_title_livesplit.setFont(title_font)
        self.ui.page_settings_title_video_capture.setFont(title_font)
        self.ui.page_settings_title_appearance.setFont(title_font)
        
        self.livesplit_port_input.setFont(small_font)
        self.capture_device_dropdown.setFont(small_font)
        self.update_capture_device_btn.setFont(regular_font)
        self.font_size_dropdown.setFont(small_font)
        self.ui.page_settings_restart_label.setFont(small_font)