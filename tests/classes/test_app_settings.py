from attendant_dls.classes.app_settings import AppSettings
import pytest
import types
from pathlib import Path
import os

TESTING_SETTINGS_DEFAULTS_AND_ALLOWED_VALUES = [
    {"name":"TEST_KEY_ADLS", "default_value":"0987654321", "allowed_values":["*"], "value_type":str},
    {"name":"TEST_SETTING_ADLS", "default_value":"A1", "allowed_values":["A1", "B2", "C3"], "value_type":str},
    {"name":"TEST_BOOL_SETTING_ADLS", "default_value":"Y", "allowed_values":["Y", "N"], "value_type":bool}
]

@pytest.fixture(autouse=True)
def mute_logger(monkeypatch):
    no_op = types.SimpleNamespace(warning=lambda *_, **__: None)
    monkeypatch.setattr("attendant_dls.classes.app_settings.logger", no_op)

def test_set_env_vars_from_file(monkeypatch):
    monkeypatch.delenv("TEST_KEY_ADLS", raising=False)
    monkeypatch.delenv("TEST_SETTING_ADLS", raising=False)
    monkeypatch.delenv("TEST_BOOL_SETTING_ADLS", raising=False)
    monkeypatch.setattr(AppSettings, "SETTINGS_DEFAULTS_AND_ALLOWED_VALUES", TESTING_SETTINGS_DEFAULTS_AND_ALLOWED_VALUES)

    test_dir = Path(__file__).parent
    config_path = test_dir / "test.cfg"

    AppSettings(config_path)
       
    assert os.environ["TEST_KEY_ADLS"] == "1234567890"
    assert os.environ["TEST_SETTING_ADLS"] == "B2"
    assert os.environ["TEST_BOOL_SETTING_ADLS"] == "N"


def test_get_settings(monkeypatch):
    monkeypatch.delenv("TEST_KEY_ADLS", raising=False)
    monkeypatch.delenv("TEST_SETTING_ADLS", raising=False)
    monkeypatch.delenv("TEST_BOOL_SETTING_ADLS", raising=False)
    monkeypatch.setattr(AppSettings, "SETTINGS_DEFAULTS_AND_ALLOWED_VALUES", TESTING_SETTINGS_DEFAULTS_AND_ALLOWED_VALUES)

    test_dir = Path(__file__).parent
    config_path = test_dir / "test.cfg"

    app_settings = AppSettings(config_path)

    assert app_settings.env_vars_file_loaded is True   
    assert app_settings.test_key_adls.value == '1234567890'
    assert app_settings.test_setting_adls.value == 'B2'
    assert app_settings.test_bool_setting_adls.value is False


def test_get_settings_bad_cfg(monkeypatch):
    monkeypatch.delenv("TEST_KEY_ADLS", raising=False)
    monkeypatch.delenv("TEST_SETTING_ADLS", raising=False)
    monkeypatch.delenv("TEST_BOOL_SETTING_ADLS", raising=False)
    monkeypatch.setattr(AppSettings, "SETTINGS_DEFAULTS_AND_ALLOWED_VALUES", TESTING_SETTINGS_DEFAULTS_AND_ALLOWED_VALUES)

    test_dir = Path(__file__).parent
    config_path = test_dir / "bad_test.cfg"

    app_settings = AppSettings(config_path)

    assert app_settings.env_vars_file_loaded is True   
    assert app_settings.test_key_adls.value == '0987654321'
    assert app_settings.test_setting_adls.value == 'A1'
    assert app_settings.test_bool_setting_adls.value is False