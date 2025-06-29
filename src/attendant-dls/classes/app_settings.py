import os
from dotenv import load_dotenv
from loguru import logger
from typing import Union, List, Any

class Setting:
    def __init__(
        self,
        name: str,
        value: Union[str, int, bool],
        default_value: Union[str, int, bool],
        allowed_values: List[Union[str, int, bool]],
        value_type: type
    ):
        self.name = name
        self.default_value = default_value
        self.allowed_values = allowed_values
        self._value_type = value_type
        self.value = self.set_value(value)

    def set_value(self, value: Any) -> Union[str, int, bool]:
        try:
            cast_value = self._value_type(value)
            if self.allowed_values and cast_value not in self.allowed_values:
                logger.warning(f"Value '{cast_value}' not allowed for setting '{self.name}'. Allowed: {self.allowed_values}")
                return self.default_value
        except (ValueError, TypeError):
            logger.warning(f"Invalid type for setting '{self.name}': expected {self._value_type.__name__}")
            return self.default_value
        return cast_value

    


class AppSettings:
    SETTINGS_AND_DEFAULTS = [
        {"name":"ATTENDANT_KEY", "default_value":"", "allowed_values":[""], "value_type":str},
    ]
    def __init__(self):
        try:
            load_dotenv("./.env")
        except:
            logger.warning("Unable to load settings from .env file, defaults will be used.")

    def get_settings(self):
        self.today_org=os.getenv("ATTENDANT_TODAY_ORG")
        self.yesterday_org=os.getenv("ATTENDANT_YESTERDAY_ORG" , )
        self.daily_org=os.getenv("ATTENDANT_DAILY_ORG" , )
        self.monthly_org=os.getenv("ATTENDANT_MONTHLY_ORG" , )
        self.type_org=os.getenv("ATTENDANT_TYPE_ORG" , )
        self.type_org_applied=os.getenv("ATTENDANT_TYPE_ORG_APPLIED" , )
        self.warn_duplicates=os.getenv("ATTENDANT_WARN_DUPLICATES" , )
        self.delete_duplicates=os.getenv("ATTENDANT_DELETE_DUPLICATES" , )
        self.duplicate_to_delete=os.getenv("ATTENDANT_DUPLICATE_TO_DELETE" , )
        self.group_by_type=os.getenv("ATTENDANT_GROUP_BY_TYPE" , )
        self.group_by_type_applied=os.getenv("ATTENDANT_GROUP_BY_TYPE_APPLIED" , )
        self.max_size=os.getenv("ATTENDANT_MAX_SIZE" , )
        self.max_size_warn=os.getenv("ATTENDANT_MAX_SIZE_WARN" , "NDL")
        self.tray_icon=os.getenv("ATTENDANT_TRAY_ICON" , "Y")