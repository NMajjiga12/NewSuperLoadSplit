import numpy as np
from PyQt5.QtCore import QSize, QObject, Qt
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont

from src.config import Config
from src.route_handler import RouteHandler

from ui.colors import Color


class PageDashboard(QObject):
    def __init__(self, ui, autosplitter):
        QObject.__init__(self)
        self.ui = ui
        self.autosplitter = autosplitter
        self.show_preview = True
        
        # Use default value if config key doesn't exist
        show_preview_config = Config.get_key("show_preview", True)
        self.set_show_preview(show_preview_config)
        
        self.reload_splits = False

        # Set Montserrat font for all dashboard elements
        self.set_montserrat_fonts()

        # Initialize preview with a black image to prevent animation
        self.initialize_preview()

        # Create counter labels to replace progress bars
        self.setup_counters()

        # Connect signals
        self.ui.page_dashboard_undo_btn.clicked.connect(self.autosplitter.undo_split)
        self.ui.page_dashboard_skip_btn.clicked.connect(self.autosplitter.skip_split)

    def setup_counters(self):
        """Replace progress bars with counter labels"""
        # Remove existing progress bars
        if hasattr(self.ui, 'page_dashboard_load_count_widget'):
            self.ui.page_dashboard_counter_layout.removeWidget(self.ui.page_dashboard_load_count_widget)
            self.ui.page_dashboard_load_count_widget.deleteLater()
            
        if hasattr(self.ui, 'page_dashboard_activations_widget'):
            self.ui.page_dashboard_counter_layout.removeWidget(self.ui.page_dashboard_activations_widget)
            self.ui.page_dashboard_activations_widget.deleteLater()

        # Create new counter labels
        self.load_counter_label = QLabel("Loads: 0/0")
        self.load_counter_label.setAlignment(Qt.AlignCenter)
        self.load_counter_label.setStyleSheet(f"""
            background-color: {Color.background};
            color: {Color.text_white};
            padding: 8px;
            border-radius: 3px;
            border: 1px solid {Color.text_dark_gray};
        """)

        self.level_counter_label = QLabel("Levels: 0/0")
        self.level_counter_label.setAlignment(Qt.AlignCenter)
        self.level_counter_label.setStyleSheet(f"""
            background-color: {Color.background};
            color: {Color.text_white};
            padding: 8px;
            border-radius: 3px;
            border: 1px solid {Color.text_dark_gray};
        """)

        # Add to layout
        self.ui.page_dashboard_counter_layout.addWidget(self.load_counter_label)
        self.ui.page_dashboard_counter_layout.addWidget(self.level_counter_label)

    def set_montserrat_fonts(self):
        """Set Montserrat font for all dashboard elements"""
        montserrat_font = QFont("Montserrat", 9)
        
        # Set font for splits list
        self.ui.splits_list.setFont(montserrat_font)
        
        # Set font for buttons
        self.ui.page_dashboard_undo_btn.setFont(montserrat_font)
        self.ui.page_dashboard_skip_btn.setFont(montserrat_font)
        self.ui.page_dashboard_close_route_btn.setFont(montserrat_font)
        self.ui.page_dashboard_load_route_btn.setFont(montserrat_font)
        self.ui.page_dashboard_save_route_btn.setFont(montserrat_font)
        self.ui.page_dashboard_save_route_as_btn.setFont(montserrat_font)
        
        # Set font for preview label
        preview_font = QFont("Montserrat", 12)
        self.ui.page_dashboard_preview.setFont(preview_font)

    def update_font_size(self, font_size):
        """Update font size for dashboard elements"""
        montserrat_font = QFont("Montserrat", font_size)
        
        self.ui.splits_list.setFont(montserrat_font)
        self.ui.page_dashboard_undo_btn.setFont(montserrat_font)
        self.ui.page_dashboard_skip_btn.setFont(montserrat_font)
        self.ui.page_dashboard_close_route_btn.setFont(montserrat_font)
        self.ui.page_dashboard_load_route_btn.setFont(montserrat_font)
        self.ui.page_dashboard_save_route_btn.setFont(montserrat_font)
        self.ui.page_dashboard_save_route_as_btn.setFont(montserrat_font)
        
        # Update counter labels
        counter_font = QFont("Montserrat", font_size)
        self.load_counter_label.setFont(counter_font)
        self.level_counter_label.setFont(counter_font)

    def initialize_preview(self):
        """Initialize the preview with a black image to prevent animation on first frame"""
        width, height = self.get_preview_size()
        if width > 0 and height > 0:
            # Create a black pixmap of the correct size
            black_pixmap = QPixmap(width, height)
            black_pixmap.fill(QColor(40, 25, 30))  # Use the background color
            self.ui.page_dashboard_preview.setPixmap(black_pixmap)

    def update_preview(self, frame):
        if self.show_preview:
            # Set the pixmap directly without clearing first
            self.ui.page_dashboard_preview.setPixmap(frame)

    def disable_preview(self):
        if self.show_preview:
            self.set_show_preview(False)

    def clear_preview(self):
        if self.show_preview:
            # Instead of setting text, set a black pixmap
            width, height = self.get_preview_size()
            if width > 0 and height > 0:
                black_pixmap = QPixmap(width, height)
                black_pixmap.fill(QColor(40, 25, 30))
                self.ui.page_dashboard_preview.setPixmap(black_pixmap)

    def enable_preview(self):
        self.set_show_preview(True)

    def set_show_preview(self, value):
        self.show_preview = value
        Config.set_key("show_preview", self.show_preview)

    def get_preview_size(self):
        # Get the actual size of the preview label
        width = self.ui.page_dashboard_preview.width()
        height = self.ui.page_dashboard_preview.height()
        
        # Ensure minimum valid size
        if width <= 0:
            width = 320
        if height <= 0:
            height = 240
            
        return width, height

    def clear_splits(self):
        self.ui.splits_list.clear()

    def add_splits(self, splits):
        if splits:
            for split in splits:
                split_name = split.name
                # Add load count to split display if available
                if hasattr(split, 'expected_loads') and split.expected_loads > 0:
                    split_name = f"{split.name} ({split.expected_loads} loads)"

                item = QListWidgetItem(split_name)
                item.setSizeHint(QSize(100, 42))
                
                # Set dark red background for splits
                item.setBackground(QColor(50, 35, 40))

                self.ui.splits_list.addItem(item)

    def component_changed(self, index):
        # Update component preview if needed
        pass

    def load_count_changed(self, value, required):
        # Update load counter label
        self.load_counter_label.setText(f"Loads: {value}/{required}")
        
        # Calculate level progress
        total_levels = len(RouteHandler.route.splits) if RouteHandler.route else 0
        current_level = self.autosplitter.current_split_index + 1 if self.autosplitter.current_split_index is not None else 0
        self.level_counter_label.setText(f"Levels: {current_level}/{total_levels}")

    def component_activated(self, value, required):
        # Update activations (not used in new design, but keep for compatibility)
        pass

    def next_split(self):
        current_index = self.get_active_split()

        if current_index is None:
            self.set_active_split(0)
        else:
            self.set_active_split(np.clip(current_index + 1, 0, self.ui.splits_list.count()))
            
        # Update level counter
        self.load_count_changed(self.autosplitter.load_count, 
                               self.autosplitter.current_split.expected_loads if self.autosplitter.current_split else 0)

    def prev_split(self):
        current_index = self.get_active_split()

        if current_index is None:
            self.set_active_split(0)
        else:
            self.set_active_split(np.clip(current_index - 1, 0, self.ui.splits_list.count() - 1))
            
        # Update level counter
        self.load_count_changed(self.autosplitter.load_count, 
                               self.autosplitter.current_split.expected_loads if self.autosplitter.current_split else 0)

    def get_active_split(self):
        selected_index = self.ui.splits_list.selectedIndexes()
        if len(selected_index) < 1:
            return None
        else:
            return selected_index[0].row()

    def set_active_split(self, row):
        # Clear previous selection
        self.ui.splits_list.clearSelection()
        
        if row < self.ui.splits_list.count():
            self.ui.splits_list.setCurrentRow(row)
            selected_item = self.ui.splits_list.item(row)
            if selected_item:
                # Highlight active split with lighter red
                selected_item.setBackground(QColor(70, 45, 50))

    def reset_splits(self):
        # Reset counter labels
        self.load_counter_label.setText("Loads: 0/0")
        self.level_counter_label.setText("Levels: 0/0")

        for i in range(self.ui.splits_list.count()):
            item = self.ui.splits_list.item(i)
            item.setBackground(QColor(50, 35, 40))  # Reset to dark red background

        self.ui.splits_list.clearSelection()

        if self.reload_splits:
            self.reload_splits = False
            self.route_updated()

    def route_updated(self):
        if self.autosplitter.run_started:
            self.reload_splits = True
            return
        else:
            self.autosplitter.wait_for_first_split = False

        self.clear_splits()

        if RouteHandler.route is not None:
            self.add_splits(RouteHandler.route.splits)
            # Update level counter with new route data
            total_levels = len(RouteHandler.route.splits)
            self.level_counter_label.setText(f"Levels: 0/{total_levels}")