from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QLabel, QComboBox, QLineEdit, QCheckBox, QSpinBox, QHBoxLayout, QGridLayout, QWidget
from PyQt5.QtGui import QFont, QColor

from src.route_handler import *


class PageRoute(QObject):
    sig_route_modified = pyqtSignal()

    def __init__(self, ui):
        QObject.__init__(self)
        self.ui = ui
        self.selected_widget = None
        self.selected_split = None
        self.updating_widgets = False  # Flag to prevent recursive updates

        # Set Montserrat font for all route elements with larger font size
        self.set_montserrat_fonts()

        # Connect signals
        self.ui.route_splits_list.itemSelectionChanged.connect(self.selection_changed)
        self.ui.route_splits_add_btn.clicked.connect(self.add_split_clicked)

        # Start Detector Options
        self.ui.page_route_start_detector.currentTextChanged.connect(self.start_detector_changed)

        # Split Options
        self.ui.page_route_split_option_name.textEdited.connect(self.name_edited)
        self.ui.page_route_split_option_split.stateChanged.connect(self.split_toggled)
        self.ui.page_route_split_option_reset_count.stateChanged.connect(self.reset_count_toggled)
        self.ui.page_route_split_option_expected_loads.valueChanged.connect(self.expected_loads_changed)
        self.ui.page_route_split_option_load_type.currentTextChanged.connect(self.load_type_changed)
        self.ui.page_route_split_option_split_action.currentTextChanged.connect(self.split_action_changed)

        # Ending Detector Options
        self.ui.page_route_ending_detector.currentTextChanged.connect(self.ending_detector_changed)

    def set_montserrat_fonts(self):
        """Set Montserrat font for all route page elements with larger size"""
        montserrat_font = QFont("Montserrat", 11)  # Increased from 9
        small_montserrat_font = QFont("Montserrat", 10)  # Increased from 8
        title_montserrat_font = QFont("Montserrat", 11)  # Increased from 9
        title_montserrat_font.setBold(True)
        
        # Set font for splits list
        self.ui.route_splits_list.setFont(montserrat_font)
        
        # Set font for buttons
        self.ui.route_splits_add_btn.setFont(montserrat_font)
        self.ui.page_route_close_route_btn.setFont(montserrat_font)
        self.ui.page_route_load_route_btn.setFont(montserrat_font)
        self.ui.page_route_save_route_btn.setFont(montserrat_font)
        self.ui.page_route_save_route_as_btn.setFont(montserrat_font)
        
        # Set font for titles
        self.ui.page_route_start_detector_title.setFont(title_montserrat_font)
        self.ui.page_route_split_options_title.setFont(title_montserrat_font)
        self.ui.page_route_ending_detector_title.setFont(title_montserrat_font)
        
        # Set font for input fields
        self.ui.page_route_start_detector.setFont(small_montserrat_font)
        self.ui.page_route_split_option_name.setFont(small_montserrat_font)
        self.ui.page_route_split_option_split.setFont(small_montserrat_font)
        self.ui.page_route_split_option_reset_count.setFont(small_montserrat_font)
        self.ui.page_route_split_option_expected_loads.setFont(small_montserrat_font)
        self.ui.page_route_split_option_load_type.setFont(small_montserrat_font)
        self.ui.page_route_split_option_split_action.setFont(small_montserrat_font)
        self.ui.page_route_ending_detector.setFont(small_montserrat_font)

        # Set font for labels in split options grid
        for i in range(self.ui.page_route_split_options_layout.count()):
            widget = self.ui.page_route_split_options_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.setFont(small_montserrat_font)

    def update_font_size(self, font_size):
        """Update font size for route page elements"""
        montserrat_font = QFont("Montserrat", font_size)
        small_montserrat_font = QFont("Montserrat", font_size - 1)
        title_montserrat_font = QFont("Montserrat", font_size)
        title_montserrat_font.setBold(True)
        
        self.ui.route_splits_list.setFont(montserrat_font)
        self.ui.route_splits_add_btn.setFont(montserrat_font)
        self.ui.page_route_close_route_btn.setFont(montserrat_font)
        self.ui.page_route_load_route_btn.setFont(montserrat_font)
        self.ui.page_route_save_route_btn.setFont(montserrat_font)
        self.ui.page_route_save_route_as_btn.setFont(montserrat_font)
        self.ui.page_route_start_detector_title.setFont(title_montserrat_font)
        self.ui.page_route_split_options_title.setFont(title_montserrat_font)
        self.ui.page_route_ending_detector_title.setFont(title_montserrat_font)
        self.ui.page_route_start_detector.setFont(small_montserrat_font)
        self.ui.page_route_split_option_name.setFont(small_montserrat_font)
        self.ui.page_route_split_option_split.setFont(small_montserrat_font)
        self.ui.page_route_split_option_reset_count.setFont(small_montserrat_font)
        self.ui.page_route_split_option_expected_loads.setFont(small_montserrat_font)
        self.ui.page_route_split_option_load_type.setFont(small_montserrat_font)
        self.ui.page_route_split_option_split_action.setFont(small_montserrat_font)
        self.ui.page_route_ending_detector.setFont(small_montserrat_font)

    def add_split_clicked(self):
        if RouteHandler.route is None:
            RouteHandler.route = NSMBWRoute()

        # Create new split with default components (empty since we removed components)
        new_split = NSMBWSplit("New Split", "level", [], True, True, 1, "regular_fade", "split")
        RouteHandler.route.splits.append(new_split)
        
        self.route_updated()
        self.apply_changes_to_route()

    def selection_changed(self):
        if self.ui.route_splits_list.count() == 0:
            # Clear selection if no items
            self.selected_split = None
            self.update_split_option_widgets()
            return

        selected_items = self.ui.route_splits_list.selectedItems()
        if len(selected_items) == 1:
            selected_item = selected_items[0]
            row = self.ui.route_splits_list.row(selected_item)
            
            if RouteHandler.route and row < len(RouteHandler.route.splits):
                self.selected_split = RouteHandler.route.splits[row]
                self.update_split_option_widgets()
            else:
                self.selected_split = None
                self.update_split_option_widgets()
        else:
            self.selected_split = None
            self.update_split_option_widgets()

    def route_updated(self):
        self.ui.route_splits_list.clear()

        if RouteHandler.route is not None:
            for split in RouteHandler.route.splits:
                # Show split name with load count in parentheses
                item_text = f"{split.name} ({split.expected_loads} loads)"
                item = QListWidgetItem(item_text)
                # Set dark red background
                item.setBackground(QColor(50, 35, 40))
                self.ui.route_splits_list.addItem(item)

        self.update_start_detector_widgets()
        self.update_split_option_widgets()
        self.update_ending_detector_widgets()

    def apply_changes_to_route(self):
        if RouteHandler.route is None:
            return
        
        # Update the route name display in the title
        if hasattr(self, 'parent_process') and self.parent_process:
            self.parent_process.set_title()

        # Update splits from list
        splits = []
        for i in range(self.ui.route_splits_list.count()):
            item = self.ui.route_splits_list.item(i)
            if i < len(RouteHandler.route.splits):
                split = RouteHandler.route.splits[i]
                # Extract the name without the load count
                name_parts = item.text().split(' (')
                if len(name_parts) > 0:
                    name = name_parts[0]
                    split.name = name
                splits.append(split)

        RouteHandler.route.splits = splits
        self.sig_route_modified.emit()

    # Start Detector Options
    def start_detector_changed(self):
        if RouteHandler.route is not None and not self.updating_widgets:
            RouteHandler.route.start_detector = self.ui.page_route_start_detector.currentText().lower().replace(' ', '_')
            self.apply_changes_to_route()

    # Ending Detector Options
    def ending_detector_changed(self):
        if RouteHandler.route is not None and not self.updating_widgets:
            RouteHandler.route.ending_detector = self.ui.page_route_ending_detector.currentText().lower().replace(' ', '_')
            self.apply_changes_to_route()

    def name_edited(self):
        if hasattr(self, 'selected_split') and self.selected_split and not self.updating_widgets:
            new_name = self.ui.page_route_split_option_name.text()
            self.selected_split.name = new_name
            
            # Update the list item immediately
            current_row = self.ui.route_splits_list.currentRow()
            if current_row >= 0:
                item = self.ui.route_splits_list.item(current_row)
                # Update the display text with load count
                item.setText(f"{new_name} ({self.selected_split.expected_loads} loads)")
            
            self.apply_changes_to_route()

    def split_toggled(self):
        if hasattr(self, 'selected_split') and self.selected_split and not self.updating_widgets:
            self.selected_split.split = self.ui.page_route_split_option_split.isChecked()
            self.apply_changes_to_route()

    def expected_loads_changed(self, value):
        if hasattr(self, 'selected_split') and self.selected_split and not self.updating_widgets:
            self.selected_split.expected_loads = value
            
            # Update the list item immediately to show new load count
            current_row = self.ui.route_splits_list.currentRow()
            if current_row >= 0:
                item = self.ui.route_splits_list.item(current_row)
                item.setText(f"{self.selected_split.name} ({value} loads)")
            
            self.apply_changes_to_route()

    def reset_count_toggled(self):
        if hasattr(self, 'selected_split') and self.selected_split and not self.updating_widgets:
            self.selected_split.reset_load_count = self.ui.page_route_split_option_reset_count.isChecked()
            self.apply_changes_to_route()

    def load_type_changed(self):
        if hasattr(self, 'selected_split') and self.selected_split and not self.updating_widgets:
            load_type_text = self.ui.page_route_split_option_load_type.currentText()
            # Map display text to internal load type
            load_type_map = {
                "Regular Fade": "regular_fade",
                "Tower/Castle": "tower_castle", 
                "Ghost House": "ghost_house",
                "Banner Load": "banner_load"
            }
            load_type = load_type_map.get(load_type_text, "regular_fade")
            self.selected_split.load_type = load_type
            self.apply_changes_to_route()

    def split_action_changed(self):
        if hasattr(self, 'selected_split') and self.selected_split and not self.updating_widgets:
            split_action_text = self.ui.page_route_split_option_split_action.currentText()
            # Map display text to internal split action
            split_action_map = {
                "Split": "split",
                "Skip Split": "skip_split"
            }
            split_action = split_action_map.get(split_action_text, "split")
            self.selected_split.split_action = split_action
            self.apply_changes_to_route()

    def update_start_detector_widgets(self):
        if RouteHandler.route is None:
            # Disable start detector if no route
            self.ui.page_route_start_detector_title.setEnabled(False)
            self.ui.page_route_start_detector.setEnabled(False)
            return

        # Enable start detector
        self.ui.page_route_start_detector_title.setEnabled(True)
        self.ui.page_route_start_detector.setEnabled(True)

        # Start Detector
        self.updating_widgets = True
        self.ui.page_route_start_detector.clear()
        self.ui.page_route_start_detector.addItems(["Manual", "File Select", "1-1 Text"])
        if hasattr(RouteHandler.route, 'start_detector') and RouteHandler.route.start_detector:
            start_detector_display = RouteHandler.route.start_detector.replace('_', ' ').title()
            index = self.ui.page_route_start_detector.findText(start_detector_display)
            if index >= 0:
                self.ui.page_route_start_detector.setCurrentIndex(index)
            else:
                # Default to manual if not found
                self.ui.page_route_start_detector.setCurrentIndex(0)
                RouteHandler.route.start_detector = "manual"
        else:
            # Set default if not set
            self.ui.page_route_start_detector.setCurrentIndex(0)
            RouteHandler.route.start_detector = "manual"
        self.updating_widgets = False

    def update_ending_detector_widgets(self):
        if RouteHandler.route is None:
            # Disable ending detector if no route
            self.ui.page_route_ending_detector_title.setEnabled(False)
            self.ui.page_route_ending_detector.setEnabled(False)
            return

        # Enable ending detector
        self.ui.page_route_ending_detector_title.setEnabled(True)
        self.ui.page_route_ending_detector.setEnabled(True)

        # Ending Detector
        self.updating_widgets = True
        self.ui.page_route_ending_detector.clear()
        self.ui.page_route_ending_detector.addItems(["Manual", "Switch Hit"])
        if hasattr(RouteHandler.route, 'ending_detector') and RouteHandler.route.ending_detector:
            ending_detector_display = RouteHandler.route.ending_detector.replace('_', ' ').title()
            index = self.ui.page_route_ending_detector.findText(ending_detector_display)
            if index >= 0:
                self.ui.page_route_ending_detector.setCurrentIndex(index)
            else:
                # Default to manual if not found
                self.ui.page_route_ending_detector.setCurrentIndex(0)
                RouteHandler.route.ending_detector = "manual"
        else:
            # Set default if not set
            self.ui.page_route_ending_detector.setCurrentIndex(0)
            RouteHandler.route.ending_detector = "manual"
        self.updating_widgets = False

    def update_split_option_widgets(self):
        if not hasattr(self, 'selected_split') or self.selected_split is None:
            # Disable split options if no split selected
            self.ui.page_route_split_options_title.setEnabled(False)
            self.ui.page_route_split_option_name.setEnabled(False)
            self.ui.page_route_split_option_split.setEnabled(False)
            self.ui.page_route_split_option_reset_count.setEnabled(False)
            self.ui.page_route_split_option_expected_loads.setEnabled(False)
            self.ui.page_route_split_option_load_type.setEnabled(False)
            self.ui.page_route_split_option_split_action.setEnabled(False)
            
            # Clear values
            self.updating_widgets = True
            self.ui.page_route_split_option_name.clear()
            self.ui.page_route_split_option_split.setChecked(True)
            self.ui.page_route_split_option_reset_count.setChecked(True)
            self.ui.page_route_split_option_expected_loads.setValue(0)
            self.ui.page_route_split_option_load_type.setCurrentIndex(0)
            self.ui.page_route_split_option_split_action.setCurrentIndex(0)
            self.updating_widgets = False
            return

        # Enable split options
        self.ui.page_route_split_options_title.setEnabled(True)
        self.ui.page_route_split_option_name.setEnabled(True)
        self.ui.page_route_split_option_split.setEnabled(True)
        self.ui.page_route_split_option_reset_count.setEnabled(True)
        self.ui.page_route_split_option_expected_loads.setEnabled(True)
        self.ui.page_route_split_option_load_type.setEnabled(True)
        self.ui.page_route_split_option_split_action.setEnabled(True)

        # Update all widgets with current split data
        self.updating_widgets = True
        
        # Name
        self.ui.page_route_split_option_name.setText(self.selected_split.name)

        # Split
        self.ui.page_route_split_option_split.setChecked(self.selected_split.split)

        # Reset Load Count
        self.ui.page_route_split_option_reset_count.setChecked(self.selected_split.reset_load_count)

        # Expected Loads
        self.ui.page_route_split_option_expected_loads.setValue(self.selected_split.expected_loads)

        # Load Type
        self.ui.page_route_split_option_load_type.clear()
        self.ui.page_route_split_option_load_type.addItems(["Regular Fade", "Tower/Castle", "Ghost House", "Banner Load"])
        if hasattr(self.selected_split, 'load_type'):
            load_type_display = self.selected_split.load_type.replace('_', ' ').title()
            index = self.ui.page_route_split_option_load_type.findText(load_type_display)
            if index >= 0:
                self.ui.page_route_split_option_load_type.setCurrentIndex(index)
            else:
                self.ui.page_route_split_option_load_type.setCurrentIndex(0)
        else:
            self.ui.page_route_split_option_load_type.setCurrentIndex(0)

        # Split Action
        self.ui.page_route_split_option_split_action.clear()
        self.ui.page_route_split_option_split_action.addItems(["Split", "Skip Split"])
        if hasattr(self.selected_split, 'split_action'):
            split_action_display = self.selected_split.split_action.replace('_', ' ').title()
            index = self.ui.page_route_split_option_split_action.findText(split_action_display)
            if index >= 0:
                self.ui.page_route_split_option_split_action.setCurrentIndex(index)
            else:
                self.ui.page_route_split_option_split_action.setCurrentIndex(0)
        else:
            self.ui.page_route_split_option_split_action.setCurrentIndex(0)
            
        self.updating_widgets = False