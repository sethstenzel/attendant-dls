import types
import pytest
from attendant_dls.classes.app_settings import Setting

@pytest.fixture(autouse=True)
def mute_logger(monkeypatch):
    no_op = types.SimpleNamespace(warning=lambda *_, **__: None)
    monkeypatch.setattr("attendant_dls.classes.app_settings.logger", no_op)


def test_allowed_value_casted():
    """
    When `loaded_value` is in `allowed_values`, the raw value should be
    converted with `value_type` and assigned to `.value`.
    """
    s = Setting(
        name="windows",
        loaded_value="11",
        default_value=4,
        allowed_values=["11", "10", "7"],
        value_type=int,
    )
    assert s.value == 11


def test_wildcard_allows_anything():
    """
    A literal ["*"] in `allowed_values` is treated as a wildcard:
    "every" input is accepted and type-cast.
    """
    s = Setting(
        name="anything",
        loaded_value="you can do i can do better",
        default_value="no you can't",
        allowed_values=["*"],
        value_type=str,
    )
    assert s.value == "you can do i can do better"


def test_disallowed_value_falls_back_to_default():
    """
    If the value is *not* in the list (and no wildcard), the class should
    ignore the supplied value and keep the provided default.
    """
    s = Setting(
        name="favorite_foods",
        loaded_value="avacado",
        default_value="pizza",
        allowed_values=["sushi", "steak", "blt"],
        value_type=str,
    )
    assert s.value == "pizza"


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Y", True),
        ("N", False),
        ("  Y  ", True),
        ("      N     ", False)
    ],
)


def test_boolean_translation(raw, expected):
    """
    When `value_type` is `bool`, the code should **bypass** normal casting
    and use the custom `"Y" == loaded_value.strip()` rule.
    """
    s = Setting(
        name="enabled",
        loaded_value=raw,
        default_value=True,
        allowed_values=["Y", "N"],
        value_type=bool,
    )
    assert s.value is expected


def test_invalid_cast_returns_default():
    """
    If casting the supplied value raises `ValueError` or `TypeError`,
    `.value` must fall back to `default_value`.
    """
    s = Setting(
        name="iq",
        loaded_value="not-an-int",
        default_value=150,
        allowed_values=["*"],
        value_type=int,
    )
    assert s.value == 150
