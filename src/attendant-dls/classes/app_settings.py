import os
from dotenv import load_dotenv
from loguru import logger


APP_SETTINGS_NAMES_DEFAULTS_AND_ALLOWED_VALUES = [
    
]


class AppSettings:
    def __init__(self):
        try:
            load_dotenv("./.env")
        except:
            logger.warning("Unable to load settings from .env file, defaults will be used.")

        

        self.key=os.getenv("ATTENDANT_KEY" , "DEMO-06-28-2025")
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