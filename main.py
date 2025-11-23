import logging
import sys
import os

from PyQt5.QtCore import QObject, QSize, Qt
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QFontDatabase, QFont

from src.config import Config
from ui.colors import Color
from ui.main_window_ui import MainWindowUi
from ui.styles import Style
from src.autosplitter import Autosplitter
from src.cpu_monitor import CpuMonitor
from src.route_handler import RouteHandler

from src.main_window_pages.page_dashboard import PageDashboard
from src.main_window_pages.page_route import PageRoute
from src.main_window_pages.page_settings import PageSettings


class MainWindow(QObject):
    def __init__(self):
        QObject.__init__(self)

        self.page_title = "Dashboard"

        # Set up ui
        self.ui = MainWindowUi()
        self.ui.close_callback = self.exit
        self.ui.setup_ui()
        
        # Use default window decorations
        self.ui.setWindowTitle("NSMBW AutoSplit")

        # Set up required classes
        self.autosplitter = Autosplitter(self)

        self.page_dashboard = PageDashboard(self.ui, self.autosplitter)
        self.page_route = PageRoute(self.ui)
        self.page_settings = PageSettings(self.ui)

        # Initialize device list after page_settings is created
        self.autosplitter.video_capture.sig_device_list_updated.connect(self.page_settings.device_list_updated)
        self.autosplitter.video_capture.update_device_list()

        self.cpu_monitor = CpuMonitor(1)
        self.cpu_monitor.sig_cpu_usage_update.connect(self.set_cpu_usage)
        self.cpu_monitor.start()

        # Connect Signals
        self.ui.page_dashboard_close_route_btn.clicked.connect(RouteHandler.close_route_btn)
        self.ui.page_dashboard_load_route_btn.clicked.connect(RouteHandler.load_route_btn)
        self.ui.page_dashboard_save_route_btn.clicked.connect(RouteHandler.save_route_btn)
        self.ui.page_dashboard_save_route_as_btn.clicked.connect(RouteHandler.save_route_as_btn)

        self.ui.page_route_close_route_btn.clicked.connect(RouteHandler.close_route_btn)
        self.ui.page_route_load_route_btn.clicked.connect(RouteHandler.load_route_btn)
        self.ui.page_route_save_route_btn.clicked.connect(RouteHandler.save_route_btn)
        self.ui.page_route_save_route_as_btn.clicked.connect(RouteHandler.save_route_as_btn)

        self.page_route.sig_route_modified.connect(self.page_dashboard.route_updated)

        self.autosplitter.sig_status_update.connect(self.set_status)
        self.autosplitter.sig_preview_update.connect(self.page_dashboard.update_preview)
        self.autosplitter.sig_preview_clear.connect(self.page_dashboard.clear_preview)
        self.autosplitter.sig_clear_splits.connect(self.page_dashboard.clear_splits)
        self.autosplitter.sig_add_splits.connect(self.page_dashboard.add_splits)
        self.autosplitter.sig_component_activated.connect(self.page_dashboard.component_activated)
        self.autosplitter.sig_load_count_changed.connect(self.page_dashboard.load_count_changed)
        self.autosplitter.sig_component_changed.connect(self.page_dashboard.component_changed)
        self.autosplitter.sig_next_split.connect(self.page_dashboard.next_split)
        self.autosplitter.sig_prev_split.connect(self.page_dashboard.prev_split)
        self.autosplitter.sig_reset_splits.connect(self.page_dashboard.reset_splits)
        self.autosplitter.livesplit.sig_connection_status.connect(self.set_livesplit_status)
        self.autosplitter.fps_counter.sig_fps_update.connect(self.set_fps)
        self.autosplitter.video_capture.sig_device_list_updated.connect(self.page_settings.device_list_updated)
        self.page_settings.sig_livesplit_port_changed.connect(self.autosplitter.livesplit.reconnect_port)
        self.page_settings.sig_capture_device_changed.connect(self.autosplitter.video_capture.init_capture_device)
        # Removed the starting and ending detector connections since they were moved to PageRoute
        self.page_settings.sig_font_size_changed.connect(self.update_font_size)

        # Add menus with new icons
        self.add_menu("🖥️", "btn_dashboard", "Dashboard", is_top_menu=True)
        self.add_menu("📕", "btn_route", "Route", is_top_menu=True)
        self.add_menu("⚙️", "btn_settings", "Settings", is_top_menu=False)
        self.ui.layout_menu_bottom.addWidget(self.ui.frame_menu_spacer)

        self.select_standard_menu("btn_dashboard")

        # Load version
        self.ui.label_version.setText("v1.0.0")
        if hasattr(self.ui, 'label_beta') and self.ui.label_beta:
            self.ui.label_beta.parent().layout().removeWidget(self.ui.label_beta)
            self.ui.label_beta.deleteLater()

        # Load window position
        window_pos = Config.get_key("window_position", [100, 100])
        if window_pos is not None:
            self.ui.move(window_pos[0], window_pos[1])

        # Load window size
        try:
            window_size = Config.get_key("window_size", [1000, 724])
            if window_size is not None:
                self.ui.resize(window_size[0], window_size[1])
            else:
                self.ui.resize(1000, 724)
        except Exception as e:
            logging.exception(e)
            self.ui.resize(1000, 724)

        # Load current route
        def update_routes():
            self.page_dashboard.route_updated()
            self.page_route.route_updated()
            self.set_title()

        RouteHandler.route_updated = update_routes

        # Get the current route from config - no default route
        current_route = Config.get_key("current_route", "")
        if current_route and os.path.exists(current_route):
            RouteHandler.load_route(current_route)

        # Start autosplitter
        self.autosplitter.start()
        self.autosplitter.running = True

        # Set current page
        self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_dashboard)

        self.set_title()

        self.ui.show()

        self.recenter_ui()

    def button(self):
        btn_widget = self.sender()

        if btn_widget.objectName() == "btn_dashboard":
            self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_dashboard)
            self.page_title = "Dashboard"

        if btn_widget.objectName() == "btn_route":
            self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_route)
            self.page_title = "Route"

        if btn_widget.objectName() == "btn_settings":
            self.ui.stacked_widget_pages.setCurrentWidget(self.ui.page_settings)
            self.page_title = "Settings"

        self.reset_style(btn_widget.objectName())
        self.set_title()
        btn_widget.setStyleSheet(self.select_menu(btn_widget.styleSheet()))

    def add_menu(self, icon, obj_name, tooltip, is_top_menu):
        button = QPushButton(self.ui)
        button.setObjectName(obj_name)
        button.setFixedSize(QSize(55, 55))
        button.setStyleSheet(Style.btn_tabs)
        button.setToolTip(tooltip)
        button.setText(icon)  # Use emoji as button text
        button.clicked.connect(self.button)

        if is_top_menu:
            self.ui.layout_menus.addWidget(button)
        else:
            self.ui.layout_menu_bottom.addWidget(button)

    @staticmethod
    def select_menu(get_style):
        select = get_style + "QPushButton { border-right: 7px solid rgb(44, 49, 60); }"
        return select

    @staticmethod
    def deselect_menu(get_style):
        deselect = get_style.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
        return deselect

    def select_standard_menu(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(self.select_menu(w.styleSheet()))

    def reset_style(self, widget):
        for w in self.ui.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(self.deselect_menu(w.styleSheet()))

    def set_title(self):
        if RouteHandler.route is not None:
            self.ui.setWindowTitle(f"NSMBW AutoSplit - {self.page_title} - {RouteHandler.route.name}")
        else:
            self.ui.setWindowTitle(f"NSMBW AutoSplit - {self.page_title}")

    def set_status(self, msg, busy=False, waiting=False):
        self.ui.label_status.setText(msg)
        self.ui.label_status.adjustSize()
        
        # Update status indicator color
        if not self.autosplitter.livesplit.connected:
            # Grey when LiveSplit not connected
            self.ui.label_status_busy_anim.setStyleSheet(f"color: {Color.text_dark_gray};")
        elif waiting:
            # Yellow when waiting for LiveSplit to start
            self.ui.label_status_busy_anim.setStyleSheet("color: rgb(255, 255, 0);")
        elif busy:
            # Green when started/running
            self.ui.label_status_busy_anim.setStyleSheet("color: rgb(0, 255, 0);")
        else:
            # Default light gray
            self.ui.label_status_busy_anim.setStyleSheet(f"color: {Color.text_light_gray};")

    def set_livesplit_status(self, connected):
        if connected:
            self.ui.label_livesplit_status.setText("Connected")
            self.ui.label_livesplit_status.adjustSize()
            self.ui.label_livesplit_status.setStyleSheet("color: rgb(91, 153, 61);")
        else:
            self.ui.label_livesplit_status.setText("Disconnected")
            self.ui.label_livesplit_status.adjustSize()
            self.ui.label_livesplit_status.setStyleSheet("color: rgb(153, 61, 61);")

    def set_cpu_usage(self, usage):
        self.ui.label_cpu_usage_percent.setText(f"{usage:.1f}%")
        self.ui.label_cpu_usage_percent.adjustSize()

    def set_fps(self, fps):
        self.ui.label_fps_value.setText(f"{fps:.1f}")
        self.ui.label_fps_value.adjustSize()

    def update_font_size(self, font_size):
        """Update font size across the application"""
        app = QApplication.instance()
        font = QFont("Montserrat", font_size)
        app.setFont(font)
        
        # Update specific fonts in pages
        self.page_dashboard.update_font_size(font_size)
        self.page_route.update_font_size(font_size)
        self.page_settings.update_font_size(font_size)

    def exit(self):
        self.ui.close()

        if self.cpu_monitor.isRunning():
            self.cpu_monitor.terminate()
            self.cpu_monitor.wait()

        self.autosplitter.quit()

        if self.autosplitter.isRunning():
            self.autosplitter.terminate()
            self.autosplitter.wait()

        import time
        time.sleep(0.1)

    def recenter_ui(self):
        # Simple centering function
        frame_geometry = self.ui.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.ui.move(frame_geometry.topLeft())


def load_fonts():
    # Load Montserrat font for all text elements
    font_paths = [
        os.path.join(os.path.dirname(__file__), "resources", "fonts"),
        os.path.join(os.path.dirname(__file__), "fonts"),
        "C:/Windows/Fonts",
        "/usr/share/fonts/truetype",
        "/Library/Fonts"
    ]
    
    montserrat_variants = {
        "Montserrat-Bold": QFont.Bold,
        "Montserrat-SemiBold": QFont.DemiBold, 
        "Montserrat-Medium": QFont.Medium,
        "Montserrat-Regular": QFont.Normal
    }
    
    fonts_loaded = {}
    
    for font_dir in font_paths:
        if os.path.exists(font_dir):
            for font_file in os.listdir(font_dir):
                if font_file.endswith(('.ttf', '.otf')):
                    try:
                        font_path = os.path.join(font_dir, font_file)
                        font_id = QFontDatabase.addApplicationFont(font_path)
                        if font_id != -1:
                            font_families = QFontDatabase.applicationFontFamilies(font_id)
                            if font_families:
                                font_name = font_families[0]
                                # Map file name to weight
                                for variant, weight in montserrat_variants.items():
                                    if variant.lower() in font_file.lower():
                                        fonts_loaded[variant] = font_name
                                        print(f"Loaded font: {font_file} as {font_name}")
                    except Exception as e:
                        print(f"Failed to load font {font_file}: {e}")
    
    # Set as default application font
    if fonts_loaded:
        app = QApplication.instance()
        default_font = QFont(fonts_loaded.get("Montserrat-Regular", "Montserrat"), 9)
        app.setFont(default_font)
        print("Montserrat font family set as default")
    else:
        print("Montserrat fonts not found, using system default")


if __name__ == "__main__":
    print("Starting NSMBW AutoSplit...")

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Clear log
    appdata = os.path.join(os.path.expandvars(r'%LOCALAPPDATA%'), "NSMBW AutoSplit")
    log_path = os.path.join(appdata, "application.log")
    os.makedirs(appdata, exist_ok=True)
    try:
        with open(log_path, 'w'):
            pass
    except:
        pass

    logging.basicConfig(filename=log_path,
                        format="\n%(asctime)s %(levelname)s %(filename)s:%(lineno)d - %(message)s\n\n",
                        level=logging.DEBUG)

    Config.init()

    app = QApplication(sys.argv)
    load_fonts()
    print("Fonts loaded")
    window = MainWindow()
    print("MainWindow constructed")
    exit_code = app.exec_()
    print(f"Exit Code: {exit_code}")
    sys.exit(exit_code)