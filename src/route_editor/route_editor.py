import json
import sys
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QLabel,
    QLineEdit, QComboBox, QAbstractItemView, QHeaderView, QMessageBox, QFileDialog
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication

class RouteEditor(QWidget):
    # Define a signal that emits the list of split names
    splits_updated = pyqtSignal(list)

    def __init__(self, parent=None):
        super(RouteEditor, self).__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Create main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)  # Add margins
        main_layout.setSpacing(10)  # Add spacing

        # Create category layout
        category_layout = QVBoxLayout()
        category_label = QLabel("Category:")
        category_label.setStyleSheet("color: white; font-size: 16px; font-family: Calibri;")
        self.category_edit = QLineEdit()
        self.apply_styles(self.category_edit)

        # Create Start Timer Detection and Reset Timer Detection layout
        timer_layout = QHBoxLayout()
        start_timer_label = QLabel("Start Timer Detection:")
        start_timer_label.setStyleSheet("color: white; font-size: 16px; font-family: Calibri;")
        self.start_timer_combo = QComboBox()
        self.start_timer_combo.addItems(["Manual Start", "Automatic Start (First Frame)", "Automatic Start (1-1 Text)"])
        self.apply_styles(self.start_timer_combo)

        reset_timer_label = QLabel("Reset Timer Detection:")
        reset_timer_label.setStyleSheet("color: white; font-size: 16px; font-family: Calibri;")
        self.reset_timer_combo = QComboBox()
        self.reset_timer_combo.addItems(["Wii Menu", "Title Screen", "Super Guide Screen"])
        self.apply_styles(self.reset_timer_combo)

        # Add widgets to timer layout
        timer_layout.addWidget(start_timer_label)
        timer_layout.addWidget(self.start_timer_combo)
        timer_layout.addWidget(reset_timer_label)
        timer_layout.addWidget(self.reset_timer_combo)

        # Add widgets to category layout
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_edit)
        category_layout.addLayout(timer_layout)

        # Create button layout
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around buttons
        button_layout.setSpacing(10)  # Add spacing between buttons

        # Create buttons
        self.insert_above_btn = QPushButton("Insert Above")
        self.insert_below_btn = QPushButton("Insert Below")
        self.remove_btn = QPushButton("Remove")
        self.move_up_btn = QPushButton("Move Up")
        self.move_down_btn = QPushButton("Move Down")
        self.save_json_btn = QPushButton("Save as JSON")
        self.load_json_btn = QPushButton("Load JSON")

        # Add buttons to layout
        button_layout.addWidget(self.insert_above_btn)
        button_layout.addWidget(self.insert_below_btn)
        button_layout.addWidget(self.remove_btn)
        button_layout.addWidget(self.move_up_btn)
        button_layout.addWidget(self.move_down_btn)
        button_layout.addWidget(self.save_json_btn)
        button_layout.addWidget(self.load_json_btn)
        button_layout.addStretch()  # Add a stretch to push buttons to the top

        # Apply styles to buttons
        self.apply_styles(self.insert_above_btn, self.insert_below_btn, self.remove_btn, self.move_up_btn,
                          self.move_down_btn, self.save_json_btn, self.load_json_btn)

        # Create apply button layout
        apply_button_layout = QHBoxLayout()
        apply_button_layout.addStretch()  # Add stretch to push apply button to the right
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.save_table)
        apply_button_layout.addWidget(self.apply_btn)
        self.apply_styles(self.apply_btn)

        # Create table
        self.route_table = QTableWidget()
        self.route_table.setColumnCount(5)
        self.route_table.setHorizontalHeaderLabels(["Split Title", "Star Load", "Fadeout", "Fadein", "Split Type"])
        self.route_table.horizontalHeader().setStretchLastSection(True)
        for col in range(4):
            self.route_table.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)
        self.route_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.route_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.route_table.verticalHeader().setDefaultSectionSize(40)  # Increase the height of each row
        self.route_table.setMinimumHeight(250)  # Set minimum height for the table
        self.route_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.route_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.route_table.setStyleSheet("""
            QTableWidget {
                background-color: #252525;
                color: white;
                border: 1px solid #303030;
                padding: 5px;
                font-size: 16px;
                font-family: Calibri;
            }
            QHeaderView::section {
                background-color: #252525;
                color: white;
                padding: 5px;
                border: 1px solid #303030;
                font-size: 16px;
                font-family: Calibri;
            }
        """)

        # Connect buttons to their respective methods
        self.insert_above_btn.clicked.connect(self.insert_above)
        self.insert_below_btn.clicked.connect(self.insert_below)
        self.remove_btn.clicked.connect(self.remove_selected)
        self.save_json_btn.clicked.connect(self.save_as_json)
        self.load_json_btn.clicked.connect(self.load_from_json)

        # Add category layout, button layout, and table to main layout
        main_layout.addLayout(category_layout)
        content_layout = QHBoxLayout()
        content_layout.addLayout(button_layout)
        content_layout.addWidget(self.route_table, 1)  # Give the table more space
        main_layout.addLayout(content_layout)
        main_layout.addLayout(apply_button_layout)

        # Set layout
        self.setLayout(main_layout)

    def apply_styles(self, *widgets):
        qss_style = """
        background-color: #252525; 
        color: white; 
        border: 1px solid #303030; 
        padding: 5px; 
        font-size: 16px; 
        font-family: Calibri;
        """
        button_style = """
        QPushButton {
            background-color: #252525;
            color: white;
            border: 1px solid #303030;
            padding: 5px;
            font-size: 16px;
            font-family: Calibri;
        }
        QPushButton:hover {
            background-color: lightgrey;
            color: white;
        }
        """
        for widget in widgets:
            if isinstance(widget, QPushButton):
                widget.setStyleSheet(button_style)
            else:
                widget.setStyleSheet(qss_style)

    def insert_above(self):
        current_row = self.route_table.currentRow()
        if current_row == -1:
            current_row = self.route_table.rowCount()
        self.route_table.insertRow(current_row)
        self.add_widgets_to_row(current_row)

    def insert_below(self):
        current_row = self.route_table.currentRow()
        if current_row == -1:
            current_row = self.route_table.rowCount()
        else:
            current_row += 1
        self.route_table.insertRow(current_row)
        self.add_widgets_to_row(current_row)

    def remove_selected(self):
        current_row = self.route_table.currentRow()
        if current_row != -1:
            self.route_table.removeRow(current_row)

    def add_widgets_to_row(self, row):
        # Add QLineEdit for Split Title
        line_edit = QLineEdit()
        line_edit.setStyleSheet(
            "background-color: #252525; color: white; border: 1px solid #303030; padding: 5px; font-size: 16px; font-family: Calibri;")
        self.route_table.setCellWidget(row, 0, line_edit)
        # Add QLineEdit with QIntValidator for Star Load, Fadeout, Fadein
        for col in range(1, 4):
            num_edit = QLineEdit()
            num_edit.setValidator(QIntValidator(0, 999))
            num_edit.setStyleSheet(
                "background-color: #252525; color: white; border: 1px solid #303030; padding: 5px; font-size: 16px; font-family: Calibri;")
            self.route_table.setCellWidget(row, col, num_edit)
        # Add QComboBox for Split Type
        combo_box = QComboBox()
        combo_box.addItems(["No Split", "2nd Last Fadeout", "Last Fadeout"])
        combo_box.setStyleSheet(
            "background-color: #252525; color: white; border: 1px solid #303030; padding: 5px; font-size: 16px; font-family: Calibri;")
        self.route_table.setCellWidget(row, 4, combo_box)

    def save_table(self):
        # Collect the split titles
        split_titles = []
        for row in range(self.route_table.rowCount()):
            item = self.route_table.cellWidget(row, 0)
            if item is not None:
                split_titles.append(item.text())

        # Emit the splits_updated signal with the collected split titles
        self.splits_updated.emit(split_titles)
        print("Table saved!")

    def save_as_json(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save JSON File", "routes", "JSON Files (*.json);;All Files (*)")
        if not file_name:
            return

        route_data = [
            {
                "Category Name": self.category_edit.text().strip(),
                "Start Timer Detection": self.start_timer_combo.currentText(),
                "Reset Timer Detection": self.reset_timer_combo.currentText()
            }
        ]

        for row in range(self.route_table.rowCount()):
            split_title = self.route_table.cellWidget(row, 0).text()
            star_load = self.route_table.cellWidget(row, 1).text()
            fadeout = self.route_table.cellWidget(row, 2).text()
            fadein = self.route_table.cellWidget(row, 3).text()
            split_type = self.route_table.cellWidget(row, 4).currentText()
            route_data.append({
                "Split Title": split_title,
                "Star Load": star_load,
                "Fadeout": fadeout,
                "Fadein": fadein,
                "Split Type": split_type
            })

        try:
            with open(file_name, 'w') as json_file:
                json.dump(route_data, json_file, indent=4)
            print(f"Data saved as {file_name}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save JSON file: {str(e)}")

    def load_from_json(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open JSON File", "routes", "JSON Files (*.json);;All Files (*)")
        if not file_name:
            return

        try:
            with open(file_name, 'r') as json_file:
                route_data = json.load(json_file)

            # Set Category Name, Start Timer Detection, and Reset Timer Detection
            self.category_edit.setText(route_data[0].get("Category Name", ""))
            self.start_timer_combo.setCurrentText(route_data[0].get("Start Timer Detection", "Option 1"))
            self.reset_timer_combo.setCurrentText(route_data[0].get("Reset Timer Detection", "Option 1"))

            # Clear existing rows in the table
            self.route_table.setRowCount(0)

            # Add rows to the table based on the JSON data
            for entry in route_data[1:]:
                current_row = self.route_table.rowCount()
                self.route_table.insertRow(current_row)
                self.add_widgets_to_row(current_row)
                self.route_table.cellWidget(current_row, 0).setText(entry.get("Split Title", ""))
                self.route_table.cellWidget(current_row, 1).setText(entry.get("Banner Load", ""))
                self.route_table.cellWidget(current_row, 2).setText(entry.get("Fadeout", ""))
                self.route_table.cellWidget(current_row, 3).setText(entry.get("Fadein", ""))
                self.route_table.cellWidget(current_row, 4).setCurrentText(entry.get("Split Type", "Option 1"))

            print(f"Data loaded from {file_name}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load JSON file: {str(e)}")

def main():
    app = QApplication(sys.argv)
    window = RouteEditor()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()