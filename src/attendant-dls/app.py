from loguru import logger
from classes.app_settings import AppSettings
import sys

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("errors.log", level="ERROR")

app_settings = AppSettings()