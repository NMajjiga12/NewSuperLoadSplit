import logging
import shutil
import json
import os

class Config:
    appdata = os.path.join(os.path.expandvars(r'%LOCALAPPDATA%'), "NSMBW AutoSplit")
    config_path = os.path.join(appdata, "config.json")
    default_path = "defaults.json"
    routes_directory = "routes"  # Routes folder in root directory

    version = "0.1.0"
    config = None
    default = None

    @staticmethod
    def init():
        Config.load_config()
        Config.load_default()
        Config.ensure_routes_directory()

    @staticmethod
    def ensure_routes_directory():
        """Create routes directory if it doesn't exist"""
        if not os.path.exists(Config.routes_directory):
            os.makedirs(Config.routes_directory, exist_ok=True)

    @staticmethod
    def load_config():
        if not os.path.isfile(Config.config_path):
            # Create default config if it doesn't exist
            Config.config = {}
            Config.save_config()
        try:
            with open(Config.config_path, "r") as file:
                Config.config = json.load(file)
            return True
        except Exception as e:
            Config.config = {}
            logging.exception(e)
            return False

    @staticmethod
    def save_config():
        try:
            os.makedirs(os.path.dirname(Config.config_path), exist_ok=True)
            with open(Config.config_path + "tmp", "w") as file:
                json.dump(Config.config, file, indent=4)
                file.flush()
                os.fsync(file)
            os.replace(Config.config_path + "tmp", Config.config_path)
            return True
        except Exception as e:
            logging.exception(e)
            if os.path.exists(Config.config_path + "tmp"):
                os.remove(Config.config_path + "tmp")
            return False

    @staticmethod
    def load_default():
        try:
            if os.path.exists(Config.default_path):
                with open(Config.default_path, "r") as file:
                    Config.default = json.load(file)
            else:
                # Create default values if defaults.json doesn't exist
                Config.default = {
                    "livesplit_port": 16834,
                    "capture_device": 0,
                    "show_preview": True,
                    "fullscreen": False,
                    "window_position": [100, 100],
                    "window_size": [1000, 724],
                    "current_route": "",
                    "dashboard_splitter_1": [350, 500],
                    "route_splitter_1": [350, 500],
                    "starting_detector": "manual",
                    "ending_detector": "switch",
                    "font_size": 9
                }
                # Save the default file for future use
                with open(Config.default_path, "w") as file:
                    json.dump(Config.default, file, indent=4)
            return True
        except Exception as e:
            Config.default = {}
            logging.exception(e)
            return False

    @staticmethod
    def get_key(key, default=None):
        if not key:
            return default

        if not Config.config:
            config_loaded = Config.load_config()
        else:
            config_loaded = True

        if not Config.default:
            config_loaded = config_loaded or Config.load_default()
        else:
            config_loaded = True

        if not config_loaded:
            logging.warning(f"No config file available")
            return default

        try:
            if Config.config and key in Config.config:
                return Config.config[key]
            elif Config.default and key in Config.default:
                return Config.default[key]
            else:
                logging.warning(f"Key \"{key}\" not found in \"{Config.config_path}\" or \"{Config.default_path}\"")
                return default
        except Exception as e:
            logging.exception(e)
            return default

    @staticmethod
    def set_key(key, value):
        if not key:
            return

        if not Config.config:
            if not Config.load_config():
                logging.warning(f"Config file not available")
                return

        try:
            Config.config[key] = value
        except Exception as e:
            logging.exception(e)
            return

        Config.save_config()