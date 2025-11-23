# ui/styles.py
from ui.colors import Color


class Style:
    btn_tabs = (
            """
            QPushButton {
                border: none;
                border-left: 16px solid """ + Color.foreground + """;
                background-color: """ + Color.foreground + """;
                text-align: center;
                outline: 0;
                color: """ + Color.text_white + """;
                font-weight: bold;
            }
            QPushButton[Active=true] {
                border: none;
                border-left: 16px solid """ + Color.foreground + """;
                border-right: 5px solid """ + Color.background + """;
                background-color: """ + Color.foreground + """;
                text-align: center;
            }
            QPushButton:hover {
                background-color: """ + Color.button_hover + """;
                border-left: 16px solid """ + Color.button_hover + """;
            }
            QPushButton:pressed {
                background-color: """ + Color.button_pressed + """;
                border-left: 16px solid """ + Color.button_pressed + """;
            }
            """
    )

    main_window = (
            """
            QMainWindow {background: transparent; }
            QToolTip {
                color: """ + Color.text_white + """;
                background-color: """ + Color.foreground + """;
                border: 1px solid rgb(40, 40, 40);
                border-radius: 2px;
            }
            """
    )

    route_list = (
            """
            QListWidget {
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                border: none;
                outline: 0;
            }
            QListWidget::item {
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                margin: 0px 0px 6px 0px;
                border-bottom: 1px solid """ + Color.background + """;
            }
            QListWidget::item:selected {
                background-color: """ + Color.button_hover + """;
                border: 2px solid """ + Color.text_light_gray + """;
            }
            QListWidget::item:hover {
                background-color: """ + Color.button_hover_light + """;
            }
            """
    )

    beta_tag = (
            """
            QLabel {
                border-radius: 8px;
                padding-left: 4px;
                padding-right: 4px;
                padding-bottom: 2px;
                margin-top: 4px;
                margin-bottom: 4px;
                margin-left: 5px;
                color: """ + Color.text_white + """;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop: 0 #f77f0e, stop:1 #f7480e);
            }
            """
    )

    btn_centered = (
            """
            QPushButton {
                border: none;
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                text-align: center;
                padding: 8px;
                outline: 0;
                border-radius: 3px;
            }
            QPushButton[Active=true] {
                background-color: """ + Color.foreground + """;
            }
            QPushButton:hover {
                background-color: """ + Color.button_hover + """;
            }
            QPushButton:pressed {
                background-color: """ + Color.button_pressed + """;
            }
            """
    )

    title_label = (
            """
            QLabel {
                border: none;
                background-color: """ + Color.foreground + """;
                color: """ + Color.text_white + """;
                text-align: left;
                padding-top: 4px;
                padding-bottom: 8px;
                padding-left: 6px;
                margin-bottom: 0px;
                font-weight: bold;
            }
            """
    )

    input_field = (
        """
        QLineEdit {
            background-color: """ + Color.background + """;
            border: none;
            border-bottom: 2px solid """ + Color.text_light_gray + """;
            border-radius: 3px;
            padding: 6px;
            color: """ + Color.text_white + """;
        }
        QLineEdit:focus {
            border-bottom: 2px solid """ + Color.text_white + """;
        }
        """
    )

    spin_box = (
        """
        QSpinBox {
            background-color: """ + Color.background + """;
            border: none;
            border-bottom: 2px solid """ + Color.text_light_gray + """;
            border-radius: 3px;
            padding: 6px;
            outline: 0;
            color: """ + Color.text_white + """;
        }
        QSpinBox:focus {
            border-bottom: 2px solid """ + Color.text_white + """;
        }
        """
    )

    dropdown = (
            """
            QComboBox{
                background-color: """ + Color.background + """;
                border: none;
                border-bottom: 2px solid """ + Color.text_light_gray + """;
                padding: 6px;
                padding-left: 10px;
                outline: 0;
                color: """ + Color.text_white + """;
                border-radius: 3px;
            }
            QComboBox:hover{
                border: none;
                border-bottom: 2px solid """ + Color.text_white + """;
                outline: 0;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                background-position: center;
                background-repeat: no-reperat;
                outline: 0;
            }
            QComboBox::drop-down:button {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: """ + Color.background + """;
                padding: 10px;
                selection-background-color: """ + Color.button_hover + """;
                outline: 0;
                color: """ + Color.text_white + """;
                border-radius: 3px;
            }
            QComboBox::down-arrow {
                color: """ + Color.text_white + """;
            }
        """
    )

    splitter = (
        """
        QSplitter::handle:vertical {
            height: 5px;
            background-color: """ + Color.background + """;
        }
        QSplitter::handle:horizontal {
            width: 5px;
            background-color: """ + Color.background + """;
        }
        """
    )

    checkbox = (
        """
        QCheckBox {
            color: """ + Color.text_white + """;
            spacing: 5px;
        }
        QCheckBox::indicator {
            width: 15px;
            height: 15px;
        }
        QCheckBox::indicator:unchecked {
            border: 1px solid """ + Color.text_dark_gray + """;
            background-color: """ + Color.background + """;
        }
        QCheckBox::indicator:checked {
            border: 1px solid """ + Color.text_light_gray + """;
            background-color: """ + Color.progress_foreground + """;
        }
        """
    )

    components_options_list = (
        """
        QListWidget {
            background-color: """ + Color.foreground + """;
            color: """ + Color.text_white + """;
            border: none;
            outline: 0;
        }
        QListWidget::item {
            background-color: """ + Color.foreground + """;
            color: """ + Color.text_white + """;
            margin: 0px 0px 6px 0px;
            border-bottom: 1px solid """ + Color.background + """;
        }
        QListWidget::item:selected {
            background-color: """ + Color.button_hover + """;
            border: none;
        }
        QListWidget::item:hover {
            background-color: """ + Color.button_hover_light + """;
        }
        QScrollBar:vertical {
            background-color: """ + Color.background + """;
            width: 16px;
            margin: 0px 3px 0px 3px;
            border: 1px transparent #2A2929;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: """ + Color.foreground + """;
            min-height: 5px;
            border-radius: 5px;
        }
        QScrollBar::sub-line:vertical, QScrollBar::add-line:vertical {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }
        QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            border: none;
            background: none;
            width: 0px;
            height: 0px;
        }
        """
    )

    # Progress bar style
    progress_bar = (
        """
        QProgressBar {
            border: none;
            background-color: """ + Color.progress_background + """;
            color: """ + Color.text_white + """;
            text-align: center;
            border-radius: 3px;
        }
        QProgressBar::chunk {
            background-color: """ + Color.progress_foreground + """;
            border-radius: 3px;
        }
        """
    )