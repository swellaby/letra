from letra import TemplateFileFormat


def test_yaml_has_correct_value():
    assert TemplateFileFormat.YAML == TemplateFileFormat(1)


def test_json_has_correct_value():
    assert TemplateFileFormat.JSON == TemplateFileFormat(2)


def test_toml_has_correct_value():
    assert TemplateFileFormat.TOML == TemplateFileFormat(3)
