from loguru import logger
from typing import Union, List

class Setting:
    def __init__(
        self,
        name: str,
        loaded_value: str,
        default_value: Union[str, int, bool],
        allowed_values: List[Union[str, int, bool]],
        value_type: type
    ):
        self.name = name
        self.default_value = default_value
        self.allowed_values = allowed_values
        self.value_type = value_type
        self.value = self.set_value(loaded_value)

    def set_value(self, loaded_value: str) -> Union[str, int, bool]:
        if isinstance(loaded_value, str):
            loaded_value = loaded_value.strip()
        try:
            if loaded_value not in self.allowed_values and self.allowed_values != ["*"]:
                logger.warning(f"Value '{loaded_value}' not allowed for setting '{self.name}'. Allowed: {self.allowed_values}")
                return self.default_value
            
            if self.value_type is bool:
                return str(loaded_value).upper() == "Y"
            
            cast_value = self.value_type(loaded_value)

        except (ValueError, TypeError):
            logger.warning(f"Invalid type for setting '{self.name}': expected {self.value_type.__name__}")
            return self.default_value
        return cast_value  