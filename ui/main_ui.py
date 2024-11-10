from PyQt6 import QtCore, QtWidgets, QtGui


class Ui_MainWindow(QtWidgets.QMainWindow):  # Inherit QMainWindow for window movement
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 560)
        MainWindow.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)  # Remove default title bar
        MainWindow.setFixedSize(1000, 560)  # Disable resizing

        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Main Layout for central widget
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)

        # Custom Title Bar with increased height
        self.title_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.title_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.title_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.title_frame.setObjectName("title_frame")
        self.title_frame.setFixedHeight(40)  # Set the title bar height
        self.title_frame.setStyleSheet("background-color: #252525; color: white;")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.title_frame)
        self.horizontalLayout.setContentsMargins(10, 0, 10, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Title Icon
        self.title_icon = QtWidgets.QLabel(parent=self.title_frame)
        self.title_icon.setObjectName("title_icon")
        self.title_icon.setPixmap(
            QtGui.QPixmap("icon/Logo.png").scaled(30, 30, QtCore.Qt.AspectRatioMode.KeepAspectRatio))  # Add icon path here
        self.horizontalLayout.addWidget(self.title_icon)

        # Title Label
        self.title_label = QtWidgets.QLabel(parent=self.title_frame)
        self.title_label.setObjectName("title_label")
        self.title_label.setText("New Super Load Split")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout.addWidget(self.title_label)

        # Spacer for buttons alignment
        self.horizontalLayout.addStretch(1)

        # Minimize Button with person.svg icon
        self.minimize_button = QtWidgets.QPushButton(parent=self.title_frame)
        self.minimize_button.setObjectName("minimize_button")
        self.minimize_button.setFixedSize(30, 30)  # Increased size for better visibility
        minimize_icon = QtGui.QIcon("icon/minimize.svg")  # Load person.svg icon
        self.minimize_button.setIcon(minimize_icon)
        self.minimize_button.setStyleSheet("background-color: transparent;")  # Transparent background
        self.minimize_button.clicked.connect(MainWindow.showMinimized)
        self.horizontalLayout.addWidget(self.minimize_button)

        # Close Button with close.svg icon
        self.close_button = QtWidgets.QPushButton(parent=self.title_frame)
        self.close_button.setObjectName("close_button")
        self.close_button.setFixedSize(30, 30)  # Increased size for better visibility
        close_icon = QtGui.QIcon("icon/close.svg")  # Load close.svg icon
        self.close_button.setIcon(close_icon)
        self.close_button.setStyleSheet("background-color: transparent;")  # Transparent background
        self.close_button.clicked.connect(MainWindow.close)
        self.horizontalLayout.addWidget(self.close_button)

        # Add the title frame to the main layout
        self.verticalLayout.addWidget(self.title_frame)

        # Content Area Layout
        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_layout.setSpacing(0)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar layout
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget.setMaximumSize(QtCore.QSize(155, 16777215))  # Reduced width by 5 pixels
        self.listWidget.setObjectName("listWidget")
        self.content_layout.addWidget(self.listWidget)

        # Main Stacked Widget
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.content_layout.addWidget(self.stackedWidget)

        # Add content layout to the main vertical layout
        self.verticalLayout.addLayout(self.content_layout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.apply_styles()

        # Initialize the menu items
        self.init_list_widget()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Mouse events for dragging
        self.title_frame.mousePressEvent = self.mousePressEvent
        self.title_frame.mouseMoveEvent = self.mouseMoveEvent

    def apply_styles(self):
        # Load and apply the QSS stylesheet if needed
        try:
            with open("style.qss", "r") as style_file:
                style = style_file.read()
                QtWidgets.QApplication.instance().setStyleSheet(style)
        except FileNotFoundError:
            pass  # Ignore if the stylesheet is not available

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "New Super Load Split"))

    def init_list_widget(self):
        # Define a list of menu items with names
        self.menu_list = [
            "Dashboard",
            "Routes",
            "Settings"
        ]

        # Initialize the side menu
        self.listWidget.clear()

        for menu in self.menu_list:
            item = QtWidgets.QListWidgetItem(menu)
            self.listWidget.addItem(item)

        # Set default row selection to the first item and connect signals
        self.listWidget.setCurrentRow(0)
        self.listWidget.currentRowChanged.connect(self.update_title)

    # Method to update the title based on the selected tab
    def update_title(self, index):
        selected_tab = self.menu_list[index]
        new_title = f"New Super Load Split - {selected_tab}"
        self.title_label.setText(new_title)

    # Custom mouse event handlers for dragging the window
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()  # Save the initial position

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self._old_pos  # Calculate the difference
            MainWindow = self.centralwidget.parent()
            MainWindow.move(MainWindow.pos() + delta)  # Move the window by delta
            self._old_pos = event.globalPosition().toPoint()  # Update the old position


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
