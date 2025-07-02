import os
from dotenv import load_dotenv
from loguru import logger
from .settings import Setting


class AppSettings:
    SETTINGS_DEFAULTS_AND_ALLOWED_VALUES = [
        {"name":"ATTENDANT_KEY", "default_value":"DEMO-06-28-2025", "allowed_values":["*"], "value_type":str},
        {"name":"ATTENDANT_ORG", "default_value":"Y", "allowed_values":["T", "Y", "M"], "value_type":bool},
        {"name":"ATTENDANT_ORG_BY_TYPE", "default_value":"", "allowed_values":["Y", "N"], "value_type":bool},
        {"name":"ATTENDANT_ORG_BY_TYPE_APPLIED", "default_value":"M", "allowed_values":["T", "Y", "M"], "value_type":str},
        {"name":"ATTENDANT_WARN_DUPLICATES", "default_value":"Y", "allowed_values":["Y", "N"], "value_type":bool},
        {"name":"ATTENDANT_DELETE_DUPLICATES", "default_value":"Y", "allowed_values":["Y","N"], "value_type":bool},
        {"name":"ATTENDANT_DUPLICATE_TO_DELETE", "default_value":"O", "allowed_values":["N", "O"], "value_type":str},
        {"name":"ATTENDANT_GROUP_BY_TYPE", "default_value":"Y", "allowed_values":["Y", "N"], "value_type":bool},
        {"name":"ATTENDANT_GROUP_BY_TYPE_APPLIED", "default_value":"M", "allowed_values":["Y","M"], "value_type":str},
        {"name":"ATTENDANT_MAX_SIZE_MB", "default_value":10240, "allowed_values":["*"], "value_type":int},
        {"name":"ATTENDANT_MAX_SIZE_MB_WARN", "default_value":"N", "allowed_values":["N", "D", "W"], "value_type":str},
        {"name":"ATTENDANT_TRAY_ICON", "default_value":"Y", "allowed_values":["Y", "N"], "value_type":bool}
    ]

    def __init__(self, settings_path):
        self.env_vars_file_loaded = False
        self.settings_path = settings_path
        self.set_env_vars_from_file()
        self.get_settings()

    def set_env_vars_from_file(self):
        try:
            load_dotenv(self.settings_path)
            self.env_vars_file_loaded = True               
        except:
            logger.warning("Unable to load settings from settings.cfg file, defaults will be used.")


    def get_settings(self):
        for setting in self.SETTINGS_DEFAULTS_AND_ALLOWED_VALUES:
            setting_value = os.getenv(setting["name"])
            if setting_value is None or setting_value == "":
                setting_value = setting["default_value"]
                logger.warning(f"Unable to load setting: {setting["name"]}, default value will be used.")
            setattr(
                self,
                setting["name"].lower(),
                Setting(
                    setting["name"].lower(),
                    setting_value,
                    setting["default_value"],
                    setting["allowed_values"],
                    setting["value_type"]
                )
            )
