from . import get_throttle_reset_message, sut_module_target

from_timestamp_mock_target = f"{sut_module_target}.datetime"
base_message = "The GitHub API will start accepting requests again at: "
exp_epoch = 1372700873
exp_datetime_str = "2013-07-01 12:47:53"


def test_has_unknown_suffix_when_epoch_is_falsy():
    exp = f"{base_message} unknown"
    act = get_throttle_reset_message(None)
    assert act == exp


def test_has_unknown_suffix_when_timestamp_conversion_invalid(monkeypatch):
    act_epoch = None

    class MockDateTimeFromTimeStamp:
        @classmethod
        def fromtimestamp(self, t, tz={}):
            nonlocal act_epoch
            act_epoch = t
            return ""

    monkeypatch.setattr(from_timestamp_mock_target, MockDateTimeFromTimeStamp)

    exp = f"{base_message} unknown"
    act = get_throttle_reset_message(exp_epoch)
    assert act == exp
    assert act_epoch == exp_epoch


def test_has_reset_value_when_timestamp_conversion_valid(monkeypatch):
    act_format = None

    def mock_strftime(self, str_fmt):
        nonlocal act_format
        act_format = str_fmt
        return exp_datetime_str

    class MockDateTimeFromTimeStamp:
        @classmethod
        def fromtimestamp(*unused):
            return type("", (object,), {"strftime": mock_strftime})()

    monkeypatch.setattr(from_timestamp_mock_target, MockDateTimeFromTimeStamp)

    exp = f"{base_message} {exp_datetime_str}"
    act = get_throttle_reset_message(exp_epoch)
    assert act == exp
    assert act_format == "%Y-%m-%d %H:%M:%S"
