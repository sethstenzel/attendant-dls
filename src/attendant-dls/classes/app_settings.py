import os
from dotenv import load_dotenv
from loguru import logger
from typing import Union, List, Any

class Setting:
    def __init__(
        self,
        name: str,
        loaded_value: Union[str, int, bool],
        default_value: Union[str, int, bool],
        allowed_values: List[Union[str, int, bool]],
        value_type: type
    ):
        self.name = name
        self.default_value = default_value
        self.allowed_values = allowed_values
        self.value_type = value_type
        self.value = self.set_value(loaded_value)

    def set_value(self, loaded_value: Any) -> Union[str, int, bool]:
        try:
            if loaded_value not in self.allowed_values and self.allowed_values != ["*"]:
                logger.warning(f"Value '{loaded_value}' not allowed for setting '{self.name}'. Allowed: {self.allowed_values}")
                return self.default_value
            
            if isinstance(self.value_type, bool):
                return "Y" == loaded_value.strip()
            
            cast_value = self.value_type(loaded_value)

        except (ValueError, TypeError):
            logger.warning(f"Invalid type for setting '{self.name}': expected {self.value_type.__name__}")
            return self.default_value
        return cast_value  


class AppSettings:
    SETTINGS_AND_DEFAULTS = [
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

    def __init__(self):
        try:
            load_dotenv("./settings.cfg")
            self.dotenv_loaded = True
        except:
            logger.warning("Unable to load settings from settings.cfg file, defaults will be used.")
            self.dotenv_loaded = False

        self.set_settings()

    def set_settings(self):
        for setting in self.SETTINGS_AND_DEFAULTS:
            setattr(
                self,
                setting["name"].lower(),
                Setting(
                    setting["name"].lower(),
                    os.getenv(setting["name"], setting["default_value"]),
                    setting["default_value"],
                    setting["allowed_values"],
                    setting["value_type"]
                )
            )
