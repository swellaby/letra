from letra import LabelPlatformType


def test_github_has_correct_value():
    assert LabelPlatformType.GITHUB == LabelPlatformType(1)
