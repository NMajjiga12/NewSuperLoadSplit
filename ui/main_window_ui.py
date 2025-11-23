from PyQt5.QtCore import QMetaObject, QSize, Qt
from PyQt5.QtWidgets import *

from ui.styles import Style
from ui.colors import Color
from ui.fonts import *
from src.config import Config
from src.route_handler import RouteHandler


class MainWindowUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.close_callback = None

        # Initialize all widgets
        self.central_widget = None
        self.frame_main = None
        self.central_widget_layout = None
        self.layout_menu_bottom = None
        self.frame_menu_spacer = None
        self.layout_menus = None
        self.frame_left_menu = None
        self.label_version = None
        self.label_status = None
        self.label_status_busy_anim = None
        self.label_livesplit_status = None
        self.label_cpu_usage_percent = None
        self.label_fps_value = None
        self.stacked_widget_pages = None
        self.page_dashboard = None
        self.page_route = None
        self.page_settings = None

        # Page Dashboard widgets
        self.page_dashboard_splitter = None
        self.page_dashboard_preview = None
        self.splits_list = None
        self.page_dashboard_undo_btn = None
        self.page_dashboard_skip_btn = None
        self.page_dashboard_load_count_widget = None
        self.page_dashboard_activations_widget = None
        self.page_dashboard_close_route_btn = None
        self.page_dashboard_load_route_btn = None
        self.page_dashboard_save_route_btn = None
        self.page_dashboard_save_route_as_btn = None
        self.page_dashboard_counter_layout = None
        self.page_dashboard_counter_widget = None

        # Page Route widgets
        self.page_route_splitter = None
        self.route_splits_list = None
        self.route_splits_add_btn = None
        self.page_route_close_route_btn = None
        self.page_route_load_route_btn = None
        self.page_route_save_route_btn = None
        self.page_route_save_route_as_btn = None
        
        # New Route Page widgets
        self.page_route_start_detector_title = None
        self.page_route_start_detector = None
        self.page_route_split_options_title = None
        self.page_route_split_option_name = None
        self.page_route_split_option_split = None
        self.page_route_split_option_reset_count = None
        self.page_route_split_option_expected_loads = None
        self.page_route_split_option_load_type = None
        self.page_route_split_option_split_action = None
        self.page_route_split_options_layout = None
        self.page_route_split_options_widget = None
        self.page_route_ending_detector_title = None
        self.page_route_ending_detector = None
        self.page_route_buttons_layout = None
        self.page_route_buttons_widget = None

        # Page Settings widgets
        self.page_settings_layout = None
        self.page_settings_title_livesplit = None
        self.page_settings_title_video_capture = None
        self.page_settings_title_appearance = None
        self.page_settings_livesplit_input_port = None
        self.page_settings_dropdown_capture_device = None
        self.page_settings_update_capture_device_btn = None
        self.page_settings_font_size = None
        self.page_settings_restart_label = None

    def setup_ui(self):
        if self.objectName():
            self.setObjectName("MainWindow")

        self.setMinimumSize(QSize(622, 300))
        self.setStyleSheet(Style.main_window)

        self.central_widget = QWidget(self)
        self.central_widget.setStyleSheet(f"color: {Color.text_white};")

        self.central_widget_layout = QHBoxLayout(self.central_widget)
        self.central_widget_layout.setSpacing(0)
        self.central_widget_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_main = QFrame(self.central_widget)
        self.frame_main.setFrameShape(QFrame.NoFrame)
        self.frame_main.setFrameShadow(QFrame.Raised)

        self.frame_main_layout = QVBoxLayout(self.frame_main)
        self.frame_main_layout.setSpacing(0)
        self.frame_main_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_center = QFrame(self.frame_main)
        self.size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.size_policy.setHorizontalStretch(0)
        self.size_policy.setVerticalStretch(0)
        self.size_policy.setHeightForWidth(self.frame_center.sizePolicy().hasHeightForWidth())
        self.frame_center.setSizePolicy(self.size_policy)
        self.frame_center.setStyleSheet(f"background-color: {Color.background};")
        self.frame_center.setFrameShape(QFrame.NoFrame)
        self.frame_center.setFrameShadow(QFrame.Raised)

        self.frame_center_layout = QHBoxLayout(self.frame_center)
        self.frame_center_layout.setSpacing(0)
        self.frame_center_layout.setContentsMargins(0, 0, 0, 0)

        # ----------------------------------------------------------
        #                       Menu Left
        # ----------------------------------------------------------

        self.frame_left_menu = QFrame(self.frame_center)
        self.size_policy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.size_policy3.setHorizontalStretch(0)
        self.size_policy3.setVerticalStretch(0)
        self.size_policy3.setHeightForWidth(self.frame_left_menu.sizePolicy().hasHeightForWidth())
        self.frame_left_menu.setSizePolicy(self.size_policy3)
        self.frame_left_menu.setFixedWidth(55)
        self.frame_left_menu.setLayoutDirection(Qt.LeftToRight)
        self.frame_left_menu.setStyleSheet(f"background-color: {Color.foreground};")
        self.frame_left_menu.setFrameShape(QFrame.NoFrame)
        self.frame_left_menu.setFrameShadow(QFrame.Raised)

        self.frame_left_menu_layout = QVBoxLayout(self.frame_left_menu)
        self.frame_left_menu_layout.setSpacing(1)
        self.frame_left_menu_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_menus = QFrame(self.frame_left_menu)
        self.frame_menus.setFrameShape(QFrame.NoFrame)
        self.frame_menus.setFrameShadow(QFrame.Raised)

        self.layout_menus = QVBoxLayout(self.frame_menus)
        self.layout_menus.setSpacing(0)
        self.layout_menus.setContentsMargins(0, 0, 0, 0)

        self.frame_left_menu_layout.addWidget(self.frame_menus, 0, Qt.AlignTop)

        self.frame_extra_menus = QFrame(self.frame_left_menu)
        self.size_policy3.setHeightForWidth(self.frame_extra_menus.sizePolicy().hasHeightForWidth())
        self.frame_extra_menus.setSizePolicy(self.size_policy3)
        self.frame_extra_menus.setFrameShape(QFrame.NoFrame)
        self.frame_extra_menus.setFrameShadow(QFrame.Raised)

        self.layout_menu_bottom = QVBoxLayout(self.frame_extra_menus)
        self.layout_menu_bottom.setSpacing(0)
        self.layout_menu_bottom.setContentsMargins(0, 0, 0, 0)

        self.frame_menu_spacer = QFrame(self)
        self.frame_menu_spacer.setMinimumSize(QSize(0, 25))
        self.frame_menu_spacer.setStyleSheet(f"background-color: {Color.foreground};")

        self.frame_left_menu_layout.addWidget(self.frame_extra_menus, 0, Qt.AlignBottom)

        # ----------------------------------------------------------

        self.frame_center_layout.addWidget(self.frame_left_menu)

        self.frame_content_right = QFrame(self.frame_center)
        self.frame_content_right.setStyleSheet(f"background-color: {Color.foreground};")
        self.frame_content_right.setFrameShape(QFrame.NoFrame)
        self.frame_content_right.setFrameShadow(QFrame.Raised)

        self.frame_content_right_layout = QVBoxLayout(self.frame_content_right)
        self.frame_content_right_layout.setSpacing(0)
        self.frame_content_right_layout.setContentsMargins(0, 0, 0, 0)

        self.frame_content = QFrame(self.frame_content_right)
        self.frame_content.setFrameShape(QFrame.NoFrame)
        self.frame_content.setFrameShadow(QFrame.Raised)

        self.frame_content_layout = QVBoxLayout(self.frame_content)
        self.frame_content_layout.setSpacing(0)
        self.frame_content_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget_pages = QStackedWidget(self.frame_content)
        self.stacked_widget_pages.setMinimumWidth(20)

        # ----------------------------------------------------------
        #                     Dashboard Page
        # ----------------------------------------------------------

        self.page_dashboard = QWidget()
        self.page_dashboard_hbox_layout = QHBoxLayout(self.page_dashboard)
        self.page_dashboard_hbox_layout.setContentsMargins(18, 18, 18, 18)

        self.page_dashboard_splitter = QSplitter(Qt.Horizontal)
        self.page_dashboard_splitter.setStyleSheet(Style.splitter)

        self.page_dashboard_left_layout = QVBoxLayout()
        self.page_dashboard_left_layout.setContentsMargins(0, 0, 18, 0)

        self.page_dashboard_left_widget = QWidget()
        self.page_dashboard_left_widget.setLayout(self.page_dashboard_left_layout)

        self.splits_list = QListWidget()
        self.splits_list.setStyleSheet(Style.route_list)
        self.splits_list.setSpacing(0)
        self.splits_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.splits_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.splits_list.setFont(font_9pt)

        self.page_dashboard_skip_undo_layout = QHBoxLayout()
        self.page_dashboard_skip_undo_layout.setContentsMargins(0, 0, 0, 0)
        self.page_dashboard_skip_undo_layout.setSpacing(8)

        self.page_dashboard_skip_undo_widget = QWidget()
        self.page_dashboard_skip_undo_widget.setLayout(self.page_dashboard_skip_undo_layout)

        self.page_dashboard_undo_btn = QPushButton("Undo Split")
        self.page_dashboard_undo_btn.setFont(font_9pt)
        self.page_dashboard_undo_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_skip_btn = QPushButton("Skip Split")
        self.page_dashboard_skip_btn.setFont(font_9pt)
        self.page_dashboard_skip_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_skip_undo_layout.addWidget(self.page_dashboard_undo_btn)
        self.page_dashboard_skip_undo_layout.addWidget(self.page_dashboard_skip_btn)

        self.page_dashboard_left_layout.addWidget(self.splits_list)
        self.page_dashboard_left_layout.addWidget(self.page_dashboard_skip_undo_widget)

        # Route Buttons
        self.page_dashboard_buttons_layout = QHBoxLayout()
        self.page_dashboard_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.page_dashboard_buttons_layout.setSpacing(8)

        self.page_dashboard_buttons_widget = QWidget()
        self.page_dashboard_buttons_widget.setLayout(self.page_dashboard_buttons_layout)

        self.page_dashboard_close_route_btn = QPushButton("Close route")
        self.page_dashboard_close_route_btn.setFont(font_9pt)
        self.page_dashboard_close_route_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_load_route_btn = QPushButton("Load route")
        self.page_dashboard_load_route_btn.setFont(font_9pt)
        self.page_dashboard_load_route_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_save_route_btn = QPushButton("Save route")
        self.page_dashboard_save_route_btn.setFont(font_9pt)
        self.page_dashboard_save_route_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_save_route_as_btn = QPushButton("Save route as")
        self.page_dashboard_save_route_as_btn.setFont(font_9pt)
        self.page_dashboard_save_route_as_btn.setStyleSheet(Style.btn_centered)

        self.page_dashboard_buttons_layout.addWidget(self.page_dashboard_close_route_btn)
        self.page_dashboard_buttons_layout.addWidget(self.page_dashboard_load_route_btn)
        self.page_dashboard_buttons_layout.addWidget(self.page_dashboard_save_route_btn)
        self.page_dashboard_buttons_layout.addWidget(self.page_dashboard_save_route_as_btn)

        self.page_dashboard_right_layout = QVBoxLayout()
        self.page_dashboard_right_layout.setContentsMargins(18, 0, 0, 0)

        self.page_dashboard_right_widget = QWidget()
        self.page_dashboard_right_widget.setLayout(self.page_dashboard_right_layout)

        self.page_dashboard_preview = QLabel("Preview")
        self.page_dashboard_preview.setFont(font_12pt)
        self.page_dashboard_preview.setAlignment(Qt.AlignCenter)
        self.page_dashboard_preview.setMinimumSize(QSize(320, 240))
        self.page_dashboard_preview.setMaximumSize(QSize(640, 480))
        self.page_dashboard_preview.setStyleSheet(f"""
            background-color: {Color.preview_background}; 
            color: {Color.text_white}; 
            border: 1px solid {Color.text_dark_gray};
            qproperty-alignment: AlignCenter;
        """)
        self.page_dashboard_preview.setScaledContents(False)

        # Counter layout for load and level counters
        self.page_dashboard_counter_layout = QHBoxLayout()
        self.page_dashboard_counter_layout.setContentsMargins(0, 10, 0, 0)
        self.page_dashboard_counter_layout.setSpacing(20)

        self.page_dashboard_counter_widget = QWidget()
        self.page_dashboard_counter_widget.setLayout(self.page_dashboard_counter_layout)

        # These will be replaced with actual counter labels in page_dashboard.py
        self.page_dashboard_load_count_widget = QProgressBar()
        self.page_dashboard_load_count_widget.setMinimum(0)
        self.page_dashboard_load_count_widget.setMaximum(0)
        self.page_dashboard_load_count_widget.setValue(0)
        self.page_dashboard_load_count_widget.setFormat("Loads: %v/%m")
        self.page_dashboard_load_count_widget.setStyleSheet(Style.progress_bar)
        self.page_dashboard_load_count_widget.setFont(font_8pt)

        self.page_dashboard_activations_widget = QProgressBar()
        self.page_dashboard_activations_widget.setMinimum(0)
        self.page_dashboard_activations_widget.setMaximum(1)
        self.page_dashboard_activations_widget.setValue(0)
        self.page_dashboard_activations_widget.setFormat("Activations: %v/%m")
        self.page_dashboard_activations_widget.setStyleSheet(Style.progress_bar)
        self.page_dashboard_activations_widget.setFont(font_8pt)

        self.page_dashboard_counter_layout.addWidget(self.page_dashboard_activations_widget)
        self.page_dashboard_counter_layout.addWidget(self.page_dashboard_load_count_widget)
        self.page_dashboard_counter_layout.addStretch()

        self.page_dashboard_right_layout.addWidget(self.page_dashboard_preview)
        self.page_dashboard_right_layout.addWidget(self.page_dashboard_counter_widget)
        self.page_dashboard_right_layout.addStretch()
        self.page_dashboard_right_layout.addWidget(self.page_dashboard_buttons_widget)

        self.page_dashboard_splitter.addWidget(self.page_dashboard_left_widget)
        self.page_dashboard_splitter.addWidget(self.page_dashboard_right_widget)

        self.page_dashboard_splitter.setStretchFactor(1, 1)
        
        dashboard_sizes = Config.get_key("dashboard_splitter_1", [350, 500])
        self.page_dashboard_splitter.setSizes(dashboard_sizes)

        self.page_dashboard_hbox_layout.addWidget(self.page_dashboard_splitter)

        self.stacked_widget_pages.addWidget(self.page_dashboard)

        # ----------------------------------------------------------
        #                       Route Page
        # ----------------------------------------------------------

        self.page_route = QWidget()
        self.page_route_hbox_layout = QHBoxLayout(self.page_route)
        self.page_route_hbox_layout.setContentsMargins(18, 18, 18, 18)

        self.page_route_splitter = QSplitter(Qt.Horizontal)
        self.page_route_splitter.setStyleSheet(Style.splitter)

        self.page_route_left_layout = QVBoxLayout()
        self.page_route_left_layout.setContentsMargins(0, 0, 18, 0)

        self.page_route_left_widget = QWidget()
        self.page_route_left_widget.setLayout(self.page_route_left_layout)

        self.route_splits_list = QListWidget()
        self.route_splits_list.setStyleSheet(Style.route_list)
        self.route_splits_list.setSpacing(0)
        self.route_splits_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.route_splits_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.route_splits_list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.route_splits_list.setFont(font_11pt)

        self.route_splits_add_btn = QPushButton("Add Split")
        self.route_splits_add_btn.setFont(font_11pt)
        self.route_splits_add_btn.setStyleSheet(Style.btn_centered)

        self.page_route_left_layout.addWidget(self.route_splits_list)
        self.page_route_left_layout.addWidget(self.route_splits_add_btn)

        # NEW: Route Options Section at the top
        self.page_route_route_options_title = QLabel("Route Options")
        self.page_route_route_options_title.setFont(font_11pt)
        self.page_route_route_options_title.setStyleSheet(Style.title_label)

        # Reset Detector
        self.page_route_reset_detector_label = QLabel("Reset Detector:")
        self.page_route_reset_detector_label.setFont(font_10pt)

        self.page_route_reset_detector = QComboBox()
        self.page_route_reset_detector.setFixedHeight(32)
        self.page_route_reset_detector.setFont(font_10pt)
        self.page_route_reset_detector.setStyleSheet(Style.dropdown)
        self.page_route_reset_detector.addItems(["Manual", "Title Screen", "Super Guide", "Menu"])

        # Start Detector
        self.page_route_start_detector_label = QLabel("Start Detector:")
        self.page_route_start_detector_label.setFont(font_10pt)

        self.page_route_start_detector = QComboBox()
        self.page_route_start_detector.setFixedHeight(32)
        self.page_route_start_detector.setFont(font_10pt)
        self.page_route_start_detector.setStyleSheet(Style.dropdown)
        self.page_route_start_detector.addItems(["Manual", "File Select", "1-1 Text", "Switch Hit"])

        # Ending Detector
        self.page_route_ending_detector_label = QLabel("Ending Detector:")
        self.page_route_ending_detector_label.setFont(font_10pt)

        self.page_route_ending_detector = QComboBox()
        self.page_route_ending_detector.setFixedHeight(32)
        self.page_route_ending_detector.setFont(font_10pt)
        self.page_route_ending_detector.setStyleSheet(Style.dropdown)
        self.page_route_ending_detector.addItems(["Manual", "Switch Hit"])

        # Split Options
        self.page_route_split_options_title = QLabel("Split Options")
        self.page_route_split_options_title.setFont(font_11pt)
        self.page_route_split_options_title.setStyleSheet(Style.title_label + "QLabel{margin-top: 10px;}")

        self.page_route_split_option_name = QLineEdit()
        self.page_route_split_option_name.setFixedHeight(32)
        self.page_route_split_option_name.setFont(font_10pt)
        self.page_route_split_option_name.setStyleSheet(Style.input_field)
        self.page_route_split_option_name.setPlaceholderText("Name")

        self.page_route_split_option_split = QCheckBox("Split")
        self.page_route_split_option_split.setFont(font_10pt)
        self.page_route_split_option_split.setStyleSheet(Style.checkbox)

        self.page_route_split_option_reset_count = QCheckBox("Reset Load Count")
        self.page_route_split_option_reset_count.setFont(font_10pt)
        self.page_route_split_option_reset_count.setStyleSheet(Style.checkbox)

        self.page_route_split_option_expected_loads = QSpinBox()
        self.page_route_split_option_expected_loads.setFixedHeight(32)
        self.page_route_split_option_expected_loads.setFont(font_10pt)
        self.page_route_split_option_expected_loads.setStyleSheet(Style.spin_box)
        self.page_route_split_option_expected_loads.setRange(0, 999)
        self.page_route_split_option_expected_loads.setSuffix(" loads")

        # Load Type Dropdown
        self.page_route_split_option_load_type = QComboBox()
        self.page_route_split_option_load_type.setFixedHeight(32)
        self.page_route_split_option_load_type.setFont(font_10pt)
        self.page_route_split_option_load_type.setStyleSheet(Style.dropdown)
        self.page_route_split_option_load_type.addItems(["Regular Fade", "Tower/Castle", "Ghost House", "Banner Load"])

        # Split Action Dropdown
        self.page_route_split_option_split_action = QComboBox()
        self.page_route_split_option_split_action.setFixedHeight(32)
        self.page_route_split_option_split_action.setFont(font_10pt)
        self.page_route_split_option_split_action.setStyleSheet(Style.dropdown)
        self.page_route_split_option_split_action.addItems(["Split", "Skip Split"])

        self.page_route_split_options_layout = QGridLayout()
        self.page_route_split_options_layout.setContentsMargins(0, 0, 0, 0)
        self.page_route_split_options_layout.setSpacing(6)
        self.page_route_split_options_layout.setColumnStretch(0, 1)
        self.page_route_split_options_layout.setColumnStretch(1, 1)

        self.page_route_split_options_widget = QWidget()
        self.page_route_split_options_widget.setLayout(self.page_route_split_options_layout)

        # Add widgets to grid layout
        self.page_route_split_options_layout.addWidget(QLabel("Name:"), 0, 0)
        self.page_route_split_options_layout.addWidget(self.page_route_split_option_name, 0, 1)
        self.page_route_split_options_layout.addWidget(self.page_route_split_option_split, 1, 0)
        self.page_route_split_options_layout.addWidget(self.page_route_split_option_reset_count, 1, 1)
        self.page_route_split_options_layout.addWidget(QLabel("Expected Loads:"), 2, 0)
        self.page_route_split_options_layout.addWidget(self.page_route_split_option_expected_loads, 2, 1)
        self.page_route_split_options_layout.addWidget(QLabel("Load Type:"), 3, 0)
        self.page_route_split_options_layout.addWidget(self.page_route_split_option_load_type, 3, 1)
        self.page_route_split_options_layout.addWidget(QLabel("Split Action:"), 4, 0)
        self.page_route_split_options_layout.addWidget(self.page_route_split_option_split_action, 4, 1)

        # Route Buttons
        self.page_route_buttons_layout = QHBoxLayout()
        self.page_route_buttons_layout.setContentsMargins(0, 10, 0, 0)
        self.page_route_buttons_layout.setSpacing(8)

        self.page_route_buttons_widget = QWidget()
        self.page_route_buttons_widget.setLayout(self.page_route_buttons_layout)

        self.page_route_close_route_btn = QPushButton("Close route")
        self.page_route_close_route_btn.setFont(font_11pt)
        self.page_route_close_route_btn.setStyleSheet(Style.btn_centered)

        self.page_route_load_route_btn = QPushButton("Load route")
        self.page_route_load_route_btn.setFont(font_11pt)
        self.page_route_load_route_btn.setStyleSheet(Style.btn_centered)

        self.page_route_save_route_btn = QPushButton("Save route")
        self.page_route_save_route_btn.setFont(font_11pt)
        self.page_route_save_route_btn.setStyleSheet(Style.btn_centered)

        self.page_route_save_route_as_btn = QPushButton("Save route as")
        self.page_route_save_route_as_btn.setFont(font_11pt)
        self.page_route_save_route_as_btn.setStyleSheet(Style.btn_centered)

        self.page_route_buttons_layout.addWidget(self.page_route_close_route_btn)
        self.page_route_buttons_layout.addWidget(self.page_route_load_route_btn)
        self.page_route_buttons_layout.addWidget(self.page_route_save_route_btn)
        self.page_route_buttons_layout.addWidget(self.page_route_save_route_as_btn)

        self.page_route_right_layout = QVBoxLayout()
        self.page_route_right_layout.setContentsMargins(18, 0, 0, 0)

        self.page_route_right_widget = QWidget()
        self.page_route_right_widget.setLayout(self.page_route_right_layout)

        # Updated layout with new Route Options section at the top
        self.page_route_right_layout.addWidget(self.page_route_route_options_title)
        self.page_route_right_layout.addWidget(self.page_route_reset_detector_label)
        self.page_route_right_layout.addWidget(self.page_route_reset_detector)
        self.page_route_right_layout.addWidget(self.page_route_start_detector_label)
        self.page_route_right_layout.addWidget(self.page_route_start_detector)
        self.page_route_right_layout.addWidget(self.page_route_ending_detector_label)
        self.page_route_right_layout.addWidget(self.page_route_ending_detector)
        self.page_route_right_layout.addWidget(self.page_route_split_options_title)
        self.page_route_right_layout.addWidget(self.page_route_split_options_widget)
        self.page_route_right_layout.addStretch()
        self.page_route_right_layout.addWidget(self.page_route_buttons_widget)

        self.page_route_splitter.addWidget(self.page_route_left_widget)
        self.page_route_splitter.addWidget(self.page_route_right_widget)

        self.page_route_splitter.setStretchFactor(1, 1)

        route_sizes = Config.get_key("route_splitter_1", [350, 500])
        self.page_route_splitter.setSizes(route_sizes)

        self.page_route_hbox_layout.addWidget(self.page_route_splitter)

        self.stacked_widget_pages.addWidget(self.page_route)

        # ----------------------------------------------------------
        #                       Settings Page
        # ----------------------------------------------------------

        self.page_settings = QWidget()
        self.page_settings_layout = QVBoxLayout(self.page_settings)
        self.page_settings_layout.setContentsMargins(18, 18, 18, 18)

        self.page_settings_title_livesplit = QLabel("LiveSplit")
        self.page_settings_title_livesplit.setFont(font_9pt)
        self.page_settings_title_livesplit.setStyleSheet(Style.title_label)

        self.page_settings_livesplit_input_port = QLineEdit()
        self.page_settings_livesplit_input_port.setFixedHeight(32)
        self.page_settings_livesplit_input_port.setFont(font_8pt)
        self.page_settings_livesplit_input_port.setStyleSheet(Style.input_field)
        self.page_settings_livesplit_input_port.setFixedWidth(262)

        self.page_settings_title_video_capture = QLabel("Video Capture")
        self.page_settings_title_video_capture.setFont(font_9pt)
        self.page_settings_title_video_capture.setStyleSheet(Style.title_label + "QLabel{margin-top: 10px;}")

        self.page_settings_dropdown_capture_device = QComboBox()
        self.page_settings_dropdown_capture_device.setFixedHeight(32)
        self.page_settings_dropdown_capture_device.setFont(font_8pt)
        self.page_settings_dropdown_capture_device.setStyleSheet(Style.dropdown)
        self.page_settings_dropdown_capture_device.setMaximumWidth(530)

        # Add update capture device button
        self.page_settings_update_capture_device_btn = QPushButton("Update Capture Device")
        self.page_settings_update_capture_device_btn.setFixedHeight(32)
        self.page_settings_update_capture_device_btn.setFont(font_9pt)
        self.page_settings_update_capture_device_btn.setStyleSheet(Style.btn_centered)
        self.page_settings_update_capture_device_btn.setMaximumWidth(262)

        # Appearance Section
        self.page_settings_title_appearance = QLabel("Appearance")
        self.page_settings_title_appearance.setFont(font_9pt)
        self.page_settings_title_appearance.setStyleSheet(Style.title_label + "QLabel{margin-top: 10px;}")

        self.page_settings_font_size = QComboBox()
        self.page_settings_font_size.setFixedHeight(32)
        self.page_settings_font_size.setFont(font_8pt)
        self.page_settings_font_size.setStyleSheet(Style.dropdown)
        self.page_settings_font_size.setMaximumWidth(262)
        self.page_settings_font_size.addItems(["8", "9", "10", "11", "12", "13", "14"])

        self.page_settings_restart_label = QLabel("Note: FPS is set to 30-60 for optimal NSMBW detection.")
        self.page_settings_restart_label.setFont(font_8pt)
        self.page_settings_restart_label.setStyleSheet("margin-left: 1px;")

        # Updated settings layout (removed starting and ending detector sections)
        self.page_settings_layout.addWidget(self.page_settings_title_livesplit)
        self.page_settings_layout.addWidget(QLabel("LiveSplit Port:"))
        self.page_settings_layout.addWidget(self.page_settings_livesplit_input_port)
        self.page_settings_layout.addWidget(self.page_settings_title_video_capture)
        self.page_settings_layout.addWidget(QLabel("Capture Device:"))
        self.page_settings_layout.addWidget(self.page_settings_dropdown_capture_device)
        self.page_settings_layout.addWidget(self.page_settings_update_capture_device_btn)
        self.page_settings_layout.addWidget(self.page_settings_title_appearance)
        self.page_settings_layout.addWidget(QLabel("Font Size:"))
        self.page_settings_layout.addWidget(self.page_settings_font_size)
        self.page_settings_layout.addWidget(self.page_settings_restart_label)
        self.page_settings_layout.addStretch()

        self.stacked_widget_pages.addWidget(self.page_settings)

        # ----------------------------------------------------------

        self.frame_content_layout.addWidget(self.stacked_widget_pages)

        self.frame_content_right_layout.addWidget(self.frame_content)

        # ----------------------------------------------------------
        #                       Status Bar
        # ----------------------------------------------------------

        self.frame_bottom = QFrame(self.frame_content_right)
        self.frame_bottom.setFixedHeight(25)
        self.frame_bottom.setStyleSheet(f"background-color: {Color.foreground};")
        self.frame_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_bottom.setFrameShadow(QFrame.Raised)
        self.frame_bottom.setContentsMargins(0, 0, 0, 0)

        self.frame_bottom_layout = QHBoxLayout(self.frame_bottom)
        self.frame_bottom_layout.setSpacing(0)
        self.frame_bottom_layout.setContentsMargins(0, 0, 2, 0)

        self.frame_label_bottom = QFrame(self.frame_bottom)
        self.frame_label_bottom.setFrameShape(QFrame.NoFrame)
        self.frame_label_bottom.setFrameShadow(QFrame.Raised)
        self.frame_label_bottom.setContentsMargins(0, 0, 0, 0)

        self.layout_bottom_status_bar = QHBoxLayout(self.frame_label_bottom)
        self.layout_bottom_status_bar.setSpacing(4)
        self.layout_bottom_status_bar.setContentsMargins(0, 0, 10, 0)

        self.label_status_busy_anim = QLabel("●")
        self.label_status_busy_anim.setMaximumWidth(21)
        self.label_status_busy_anim.setStyleSheet(f"color: {Color.text_dark_gray};")

        self.label_status = QLabel(self.frame_label_bottom)
        self.label_status.setMinimumHeight(25)
        self.label_status.setFont(font_7pt)
        self.label_status.setStyleSheet(f"color: {Color.text_dark_gray};")

        self.layout_footer_status = QHBoxLayout()
        self.layout_footer_status.setContentsMargins(0, 0, 0, 0)
        self.layout_footer_status.setSpacing(5)
        self.layout_footer_status.setAlignment(Qt.AlignLeft)

        self.label_livesplit = QLabel("LiveSplit")
        self.label_livesplit.setMinimumHeight(25)
        self.label_livesplit.setFont(font_7pt)
        self.label_livesplit.setStyleSheet(f"color: {Color.text_dark_gray};")
        self.label_livesplit.adjustSize()

        self.label_livesplit_status = QLabel("Disconnected")
        self.label_livesplit_status.setMinimumHeight(25)
        self.label_livesplit_status.setFont(font_7pt)
        self.label_livesplit_status.setStyleSheet("color: rgb(153, 61, 61);")
        self.label_livesplit_status.adjustSize()

        self.label_cpu_usage = QLabel("| CPU")
        self.label_cpu_usage.setMinimumHeight(25)
        self.label_cpu_usage.setFont(font_7pt)
        self.label_cpu_usage.setStyleSheet(f"color: {Color.text_dark_gray};")
        self.label_cpu_usage.adjustSize()

        self.label_cpu_usage_percent = QLabel("0.0%")
        self.label_cpu_usage_percent.setMinimumHeight(25)
        self.label_cpu_usage_percent.setFont(font_7pt)
        self.label_cpu_usage_percent.setStyleSheet(f"color: {Color.text_light_gray};")
        self.label_cpu_usage_percent.adjustSize()

        self.label_fps = QLabel("| FPS")
        self.label_fps.setMinimumHeight(25)
        self.label_fps.setFont(font_7pt)
        self.label_fps.setStyleSheet(f"color: {Color.text_dark_gray};")
        self.label_fps.adjustSize()

        self.label_fps_value = QLabel("0.0")
        self.label_fps_value.setMinimumHeight(25)
        self.label_fps_value.setFont(font_7pt)
        self.label_fps_value.setStyleSheet(f"color: {Color.text_light_gray};")
        self.label_fps_value.adjustSize()

        self.layout_footer_status.addWidget(self.label_livesplit)
        self.layout_footer_status.addWidget(self.label_livesplit_status)
        self.layout_footer_status.addWidget(self.label_cpu_usage)
        self.layout_footer_status.addWidget(self.label_cpu_usage_percent)
        self.layout_footer_status.addWidget(self.label_fps)
        self.layout_footer_status.addWidget(self.label_fps_value)

        self.label_version = QLabel(self.frame_label_bottom)
        self.label_version.setMinimumHeight(25)
        self.label_version.setMaximumWidth(100)
        self.label_version.setFont(font_7pt)
        self.label_version.setStyleSheet(f"color: {Color.text_dark_gray};")
        self.label_version.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.layout_bottom_status_bar.addWidget(self.label_status_busy_anim)
        self.layout_bottom_status_bar.addWidget(self.label_status)
        self.layout_bottom_status_bar.addLayout(self.layout_footer_status)
        self.layout_bottom_status_bar.addWidget(self.label_version)

        self.frame_bottom_layout.addWidget(self.frame_label_bottom)

        # ----------------------------------------------------------

        self.frame_content_right_layout.addWidget(self.frame_bottom)

        self.frame_center_layout.addWidget(self.frame_content_right)

        self.frame_main_layout.addWidget(self.frame_center)

        self.central_widget_layout.addWidget(self.frame_main)

        self.setCentralWidget(self.central_widget)

        self.stacked_widget_pages.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(self)

    def closeEvent(self, event):
        if hasattr(RouteHandler, 'check_unsaved_changes') and RouteHandler.check_unsaved_changes():
            event.ignore()
            if hasattr(RouteHandler, 'window_close_btn'):
                RouteHandler.window_close_btn(self)
            return

        Config.set_key("fullscreen", self.isMaximized())
        Config.set_key("window_position", [self.pos().x(), self.pos().y()])
        if self.isMaximized():
            Config.set_key("window_size", [self.normalGeometry().width(), self.normalGeometry().height()])
        else:
            Config.set_key("window_size", [self.size().width(), self.size().height()])
        
        # Save splitter sizes
        if hasattr(self, 'page_dashboard_splitter') and self.page_dashboard_splitter:
            Config.set_key("dashboard_splitter_1", self.page_dashboard_splitter.sizes())
        if hasattr(self, 'page_route_splitter') and self.page_route_splitter:
            Config.set_key("route_splitter_1", self.page_route_splitter.sizes())

        if not isinstance(self.close_callback, type(None)):
            self.close_callback()

        event.accept()