import sys
from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QSize  # Change PyQt6.QtCore to PySide6.QtCore
from PySide6.QtGui import QIcon, QFont  # Change PyQt6.QtGui to PySide6.QtGui

# Import the UI class from the 'main_ui' module
from ui.main_ui import Ui_MainWindow
from src.dashboard.video_widget import VideoWidget
from src.route_editor.route_editor import RouteEditor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated 'main_ui' class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window properties
        self.setWindowIcon(QIcon("./icon/Logo.png"))
        self.setWindowTitle("New Super Loadless Splitter")

        # Initialize UI elements
        self.title_label = self.ui.title_label
        self.title_label.setText("Options Menu/Tab")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.title_icon = self.ui.title_icon
        self.title_icon.setScaledContents(True)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.main_content = self.ui.stackedWidget

        # Define a list of menu items with names and icons
        self.menu_list = [
            {
                "name": "Dashboard",
                "icon": "./icon/dashboard-white.svg"
            },
            {
                "name": "Routes",
                "icon": "./icon/map.svg"
            },
            {
                "name": "Settings",
                "icon": "./icon/settings-white.svg"
            }
        ]

        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()

    def init_list_widget(self):
        # Initialize the side menu
        self.side_menu.clear()

        for menu in self.menu_list:
            # Set items for the side menu with icons and text
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setText(menu.get("name"))
            item.setSizeHint(QSize(40, 40))
            self.side_menu.addItem(item)
        self.side_menu.setCurrentRow(0)

        # Connect signals and slots for switching between menu items
        self.side_menu.currentRowChanged.connect(self.main_content.setCurrentIndex)

    def init_stackwidget(self):
        # Initialize the stack widget with content pages
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        for menu in self.menu_list:
            layout = QVBoxLayout()

            if menu.get("name") == "Dashboard":
                # Replace QLabel with VideoWidget
                self.video_widget = VideoWidget(self)
                layout.addWidget(self.video_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
            elif menu.get("name") == "Routes":
                # Add the RouteEditor widget
                self.route_editor = RouteEditor(self)
                layout.addWidget(self.route_editor)
                # Connect the signal
                self.route_editor.splits_updated.connect(self.video_widget.update_split_list)
            else:
                label = QLabel(menu.get("name"))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont()
                font.setPixelSize(20)
                label.setFont(font)
                layout.addWidget(label)

            new_page = QWidget()
            new_page.setLayout(layout)
            self.main_content.addWidget(new_page)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Load style file
    with open("style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
