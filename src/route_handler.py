import xml.etree.ElementTree as ElementTree
import jsonschema
import logging
import copy
import json
import os

from PyQt5.QtWidgets import QFileDialog
from typing import List

from src.config import Config
from ui.popup_ui import *


class RouteHandler:
    route_updated = None

    route_path = ""
    route = None
    rollback = None

    unsaved_popup = None
    save_warning_popup = None
    ignore_unsaved = False

    @staticmethod
    def load_route_btn():
        if RouteHandler.check_unsaved_changes():
            def save_and_load():
                RouteHandler.save_route(RouteHandler.route_path)
                file_path = RouteHandler.open_file()

                if file_path is not None:
                    RouteHandler.load_route(file_path)

            def load_without_saving():
                file_path = RouteHandler.open_file()

                if file_path is not None:
                    RouteHandler.load_route(file_path)

            RouteHandler.unsaved_popup = UnsavedChangesPopup()
            RouteHandler.unsaved_popup.sig_clicked_yes.connect(save_and_load)
            RouteHandler.unsaved_popup.sig_clicked_no.connect(load_without_saving)
            RouteHandler.unsaved_popup.show()
        else:
            file_path = RouteHandler.open_file()

            if file_path is not None:
                RouteHandler.load_route(file_path)

    @staticmethod
    def validate_route(json_data):
        schema = {
            "type": "object",
            "properties": {
                "version": {"type": "string"},
                "name": {"type": "string"},
                "start_detector": {"type": "string"},
                "ending_detector": {"type": "string"},
                "splits": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "type": {"type": "string"},
                            "components": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "activations": {"type": "integer"},
                                    },
                                    "required": ["name", "activations"]
                                }
                            },
                            "split": {"type": "boolean"},
                            "reset_load_count": {"type": "boolean"},
                            "expected_loads": {"type": "integer"},
                            "load_type": {"type": "string"},
                            "split_action": {"type": "string"}
                        },
                        "required": ["name", "type", "components", "split", "reset_load_count", "expected_loads", "split_action"]
                    }
                },
            },
            "required": ["version", "name", "start_detector", "ending_detector", "splits"]
        }

        try:
            jsonschema.validate(instance=json_data, schema=schema)
        except Exception as e:
            print(f"JSON schema validation failed: {e}")
            return False
        else:
            return True

    @staticmethod
    def save_route_btn():
        if os.path.splitext(RouteHandler.route_path)[1] == ".lss" or (RouteHandler.route_path == "" and
                                                                      RouteHandler.route is not None):
            RouteHandler.save_route_as_btn()
        RouteHandler.save_route(RouteHandler.route_path)

    @staticmethod
    def save_route_as_btn():
        if not RouteHandler.route:
            logging.warning("No route is currently loaded")
            return

        file_path = RouteHandler.open_file(save=True)

        if RouteHandler.route is None:
            RouteHandler.route = NSMBWRoute()

        if file_path is not None:
            RouteHandler.save_route(file_path)
            RouteHandler.route_path = file_path

    @staticmethod
    def close_route_btn():
        if RouteHandler.check_unsaved_changes():
            def save_and_close():
                RouteHandler.save_route(RouteHandler.route_path)
                RouteHandler.close_route()

            def close_without_saving():
                RouteHandler.close_route()

            RouteHandler.unsaved_popup = UnsavedChangesPopup()
            RouteHandler.unsaved_popup.sig_clicked_yes.connect(save_and_close)
            RouteHandler.unsaved_popup.sig_clicked_no.connect(close_without_saving)
            RouteHandler.unsaved_popup.show()
        else:
            RouteHandler.close_route()

    @staticmethod
    def window_close_btn(main_window):
        def save_and_close():
            RouteHandler.save_route(RouteHandler.route_path)
            main_window.close()

        def close_without_saving():
            RouteHandler.ignore_unsaved = True
            main_window.close()

        RouteHandler.unsaved_popup = UnsavedChangesPopup()
        RouteHandler.unsaved_popup.sig_clicked_yes.connect(save_and_close)
        RouteHandler.unsaved_popup.sig_clicked_no.connect(close_without_saving)
        RouteHandler.unsaved_popup.show()

    @staticmethod
    def load_route(path):
        if path == "":
            return

        if path.endswith(".lss"):
            RouteHandler.load_livesplit_splits(path)
            return

        print(f"loading route: {path}")
        try:
            with open(path, "r") as file:
                route_object = json.load(file)
        except Exception as e:
            logging.exception(f"Error loading route file: {e}")
            return

        val_success = RouteHandler.validate_route(route_object)

        if not val_success:
            # Try to load anyway with relaxed validation for backward compatibility
            print("JSON schema validation failed, attempting to load with relaxed validation...")
            try:
                RouteHandler.route_path = path
                RouteHandler.route = RouteHandler.parse_route(route_object)
                RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
                RouteHandler.route_updated()
                Config.set_key("current_route", path)
                print("Route loaded successfully with relaxed validation")
                return
            except Exception as e:
                logging.exception(f"Failed to load route even with relaxed validation: {e}")
                load_failed_popup = RouteLoadFailedPopup()
                load_failed_popup.show()
        else:
            RouteHandler.route_path = path
            RouteHandler.route = RouteHandler.parse_route(route_object)
            RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
            RouteHandler.route_updated()
            Config.set_key("current_route", path)
            print("Route loaded successfully")

    @staticmethod
    def save_route(path):
        if not RouteHandler.route or RouteHandler.route_path == "":
            logging.warning("No route is currently loaded")
            return

        print(path)
        print(os.path.dirname(__file__)[:-4].replace("\\", "/"))
        if path.startswith(os.path.dirname(__file__)[:-4].replace("\\", "/")):
            print("In Install Dir")
            RouteHandler.save_warning_popup = RouteSaveWarningPopup()
            RouteHandler.save_warning_popup.show()

        if os.path.splitext(path)[1] == ".nsmbw":
            try:
                RouteHandler.route.name = os.path.splitext(path)[0].split('/')[-1]
                with open(path + "tmp", "w") as file:
                    json.dump(RouteHandler.serialize_route(RouteHandler.route), file, indent=4)
                    file.flush()
                    os.fsync(file)
                os.replace(path + "tmp", path)
                RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
            except Exception as e:
                logging.exception(e)
                if os.path.exists(path + "tmp"):
                    os.remove(path + "tmp")
                return
        else:
            logging.warning(f"Invalid route path \"{path}\"")
            return

        RouteHandler.route_updated()
        Config.set_key("current_route", path)

    @staticmethod
    def close_route():
        RouteHandler.route = None
        RouteHandler.rollback = None
        RouteHandler.route_path = ""
        RouteHandler.route_updated()
        Config.set_key("current_route", "")

    @staticmethod
    def get_routes_directory():
        """Get the routes directory, creating it if necessary"""
        if not os.path.exists(Config.routes_directory):
            os.makedirs(Config.routes_directory, exist_ok=True)
        return Config.routes_directory

    @staticmethod
    def load_livesplit_splits(path):
        tree = ElementTree.parse(path)
        root = tree.getroot()

        RouteHandler.route = NSMBWRoute(Config.version, os.path.splitext(path)[0].split('/')[-1], "manual", "manual", [])

        splits = []
        subsplits = []
        for element in root.findall('.//Segment/Name'):
            if element.text.startswith("-"):
                subsplits.append(element.text[1:])
            elif element.text.startswith("{"):
                subsplit_title = element.text[1:][:element.text.find("}") - 1]
                subsplits.append(element.text[element.text.find("}") + 1:])
                for split in subsplits:
                    splits.append(subsplit_title + " " + split)
                subsplits.clear()
            else:
                splits.append(element.text)

        for split in splits:
            RouteHandler.route.splits.append(NSMBWSplit(split, "", [], True, True, 0, "regular_fade", "split"))

        RouteHandler.route_path = path
        RouteHandler.rollback = copy.deepcopy(RouteHandler.route)
        RouteHandler.route_updated()
        Config.set_key("current_route", path)

    @staticmethod
    def check_unsaved_changes():
        if RouteHandler.ignore_unsaved:
            RouteHandler.ignore_unsaved = False
            return False

        if RouteHandler.route is None or RouteHandler.rollback is None:
            return False

        route_dict = RouteHandler.serialize_route(RouteHandler.route)
        rollback_dict = RouteHandler.serialize_route(RouteHandler.rollback)

        return route_dict != rollback_dict

    @staticmethod
    def parse_route(route_object):
        version = RouteHandler.get_key(route_object, "version", Config.version)
        name = RouteHandler.get_key(route_object, "name", "Unnamed Route")
        start_detector = RouteHandler.get_key(route_object, "start_detector", "manual")
        ending_detector = RouteHandler.get_key(route_object, "ending_detector", "manual")
        splits_object = RouteHandler.get_key(route_object, "splits", [])

        splits = []
        for split in splits_object:
            components_object = RouteHandler.get_key(split, "components", [])
            components = []
            for component in components_object:
                component_name = RouteHandler.get_key(component, "name", "")
                component_activations = RouteHandler.get_key(component, "activations", 1)

                components.append(Component(component_name, component_activations))

            split_name = RouteHandler.get_key(split, "name", "Unnamed Split")
            split_type = RouteHandler.get_key(split, "type", "")
            split_components = components
            split_split = RouteHandler.get_key(split, "split", True)
            split_reset_load_count = RouteHandler.get_key(split, "reset_load_count", True)
            split_expected_loads = RouteHandler.get_key(split, "expected_loads", 0)
            split_load_type = RouteHandler.get_key(split, "load_type", "regular_fade")
            split_split_action = RouteHandler.get_key(split, "split_action", "split")

            splits.append(NSMBWSplit(split_name, split_type, split_components, split_split, split_reset_load_count, split_expected_loads, split_load_type, split_split_action))

        return NSMBWRoute(version, name, start_detector, ending_detector, splits)

    @staticmethod
    def serialize_route(route_object):
        splits = []
        for split in route_object.splits:
            components = []
            for component in split.components:
                component_dict = {
                    "name": component.name,
                    "activations": component.activations
                }
                components.append(component_dict)

            split_dict = {
                "name": split.name,
                "type": split.type,
                "components": components,
                "split": split.split,
                "reset_load_count": split.reset_load_count,
                "expected_loads": split.expected_loads,
                "load_type": split.load_type,
                "split_action": split.split_action
            }
            splits.append(split_dict)

        route_dict = {
            "version": route_object.version,
            "name": route_object.name,
            "start_detector": route_object.start_detector,
            "ending_detector": route_object.ending_detector,
            "splits": splits
        }
        return route_dict

    @staticmethod
    def get_key(json_object, key, default=None):
        if not json_object or not key:
            return default

        try:
            if key in json_object:
                return json_object[key]
            else:
                # Don't log warnings for optional fields to reduce noise
                if key not in ['load_type', 'type', 'split_action', 'start_detector', 'ending_detector']:  # These are optional fields
                    logging.warning(f"Key \"{key}\" not found in route, using default: {default}")
                return default
        except Exception as e:
            logging.exception(f"Error getting key {key}: {e}")
            return default

    @staticmethod
    def open_file(save=False):
        file_dialog = QFileDialog()
        
        # Get the absolute path to the routes directory
        routes_dir = os.path.abspath(Config.routes_directory)
        print(f"Routes directory: {routes_dir}")
        
        # Ensure the routes directory exists
        if not os.path.exists(routes_dir):
            os.makedirs(routes_dir, exist_ok=True)
        
        # Always default to routes directory
        file_dialog.setDirectory(routes_dir)

        if save:
            file_dialog.setNameFilters(["NSMBW AutoSplit Route (*.nsmbw)"])
            file_dialog.selectNameFilter("NSMBW AutoSplit Route (*.nsmbw)")
            file_dialog.setWindowTitle("Save Route")
            file_dialog.setAcceptMode(QFileDialog.AcceptSave)
            # Set default file name if no route is loaded
            if RouteHandler.route and RouteHandler.route.name:
                default_name = RouteHandler.route.name
            else:
                default_name = "new_route"
            file_dialog.selectFile(f"{default_name}.nsmbw")
        else:
            file_dialog.setNameFilters(["All Supported Files (*.nsmbw *.lss)", "NSMBW AutoSplit Route (*.nsmbw)",
                                        "LiveSplit Splits (*.lss)"])
            file_dialog.selectNameFilter("All Supported Files (*.nsmbw *.lss)")
            file_dialog.setWindowTitle("Load Route")

        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            # If saving and no extension provided, add .nsmbw
            if save and not selected_file.endswith('.nsmbw'):
                selected_file += '.nsmbw'
            print(f"Selected file: {selected_file}")
            return selected_file
        else:
            return None


class Component:
    def __init__(self, name: str, activations: int = 1):
        self.name: str = name
        self.activations: int = activations


class NSMBWSplit:
    def __init__(self, name: str, type: str, components: List[Component], split: bool = True,
                 reset_load_count: bool = True, expected_loads: int = 0, load_type: str = "regular_fade", split_action: str = "split"):
        self.name: str = name
        self.type: str = type
        self.components: List[Component] = components
        self.split: bool = split
        self.reset_load_count: bool = reset_load_count
        self.expected_loads: int = expected_loads
        self.load_type: str = load_type
        self.split_action: str = split_action
        self.actual_loads: int = 0

class NSMBWRoute:
    def __init__(self, version=Config.version, name: str = "", start_detector: str = None, ending_detector: str = None, splits: List[NSMBWSplit] = None):
        self.version: str = Config.version
        self.name: str = name
        self.start_detector: str = start_detector if start_detector is not None else "manual"
        self.ending_detector: str = ending_detector if ending_detector is not None else "manual"
        self.splits: List[NSMBWSplit] = splits if splits is not None else []
        self.total_load_count: int = 0
        self.calculate_total_loads()
    
    def calculate_total_loads(self):
        """Calculate total loads across all splits for the route table column"""
        self.total_load_count = sum(split.expected_loads for split in self.splits)