import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

# Import the UI class from the 'main_ui' module
from ui.main_ui import Ui_MainWindow
from src.dashboard.video_widget import VideoWidget
from src.route_editor.route_editor import RouteEditor
from src.settings.settings import SettingsWindow


class MainWindow(QMainWindow):
    settings_requested = pyqtSignal()  # Define a custom signal for settings requests

    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated 'main_ui' class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Initialize sidebar (side_menu)
        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Main content stack widget
        self.main_content = self.ui.stackedWidget

        # Define a list of menu items with names and icons
        self.menu_list = [
            {"name": "Dashboard", "icon": "./icon/dashboard-white.svg"},
            {"name": "Routes", "icon": "./icon/map.svg"},
            {"name": "Settings", "icon": "./icon/settings-white.svg"}
        ]

        # Initialize UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()

    def init_list_widget(self):
        # Initialize the side menu
        self.side_menu.clear()

        for menu in self.menu_list:
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setText(menu.get("name"))
            item.setSizeHint(QSize(40, 40))
            self.side_menu.addItem(item)

        # Set default row selection to the first item and connect signals
        self.side_menu.setCurrentRow(0)
        self.side_menu.currentRowChanged.connect(self.main_content.setCurrentIndex)

    def init_stackwidget(self):
        # Clear any existing widgets in the stack widget
        while self.main_content.count() > 0:
            widget = self.main_content.widget(0)
            self.main_content.removeWidget(widget)
            widget.deleteLater()

        # Add pages to the stack widget based on menu items
        for menu in self.menu_list:
            layout = QVBoxLayout()

            if menu.get("name") == "Dashboard":
                self.video_widget = VideoWidget(self)
                layout.addWidget(self.video_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
            elif menu.get("name") == "Routes":
                self.route_editor = RouteEditor(self)
                layout.addWidget(self.route_editor)
                if hasattr(self, 'video_widget'):
                    self.route_editor.splits_updated.connect(self.video_widget.update_split_list)
            elif menu.get("name") == "Settings":
                self.settings_widget = SettingsWindow(self)
                layout.addWidget(self.settings_widget)
            else:
                # Fallback if additional pages are added in future
                label = QLabel(menu.get("name"))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont()
                font.setPixelSize(20)
                label.setFont(font)
                layout.addWidget(label)

            # Wrap the layout in a QWidget and add to the stack
            new_page = QWidget()
            new_page.setLayout(layout)
            self.main_content.addWidget(new_page)

    def show_settings(self):
        # This method gets called when the settings_requested signal is emitted
        self.main_content.setCurrentIndex(len(self.menu_list) - 1)  # Set the index to the last item ("Settings")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load style file
    with open("style.qss") as f:
        style_str = f.read()
    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
