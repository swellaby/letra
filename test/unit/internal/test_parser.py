from letra._internal.parser import extract_labels, extract_label
from schema import SchemaError
from test.helpers import (
    bug_label,
    bug_label_contents,
    build_invalid_label_template_error,
    build_label_templates_invalid_color_schema_error,
    build_invalid_label_template_error,
    label_template_name_schema_error,
    label_templates_name_schema_error,
    stub_empty_template_file_contents,
    stub_labels,
    stub_template_file_contents,
    stub_template_label_missing_name,
)
from pytest import raises


def test_extract_label_raises_error_when_label_is_invalid(monkeypatch):
    def mock_validate(*unused):
        raise SchemaError(autos=["Missing key: 'name'"])

    monkeypatch.setattr(
        "letra._internal.parser.label_schema.validate", mock_validate
    )

    with raises(ValueError) as err:
        extract_label({})
    assert str(err.value) == label_template_name_schema_error


def test_extract_label_returns_label_when_label_is_valid(monkeypatch):
    def mock_validate(data):
        assert data == bug_label_contents
        return bug_label

    monkeypatch.setattr(
        "letra._internal.parser.label_schema.validate", mock_validate
    )
    label = extract_label(bug_label_contents)
    assert label == bug_label


def test_extract_labels_raises_error_when_template_missing_root_label():
    exp = "Invalid label template. Root level `labels` field missing."
    with raises(ValueError) as err:
        extract_labels({})
    assert str(err.value) == exp


def test_extract_labels_raises_error_when_template_contains_no_labels():
    with raises(ValueError) as err:
        extract_labels(stub_empty_template_file_contents)
    assert str(err.value) == "No labels found in provided label template."


def test_extract_labels_raises_error_when_template_is_invalid(monkeypatch):
    def mock_validate(*unused):
        raise SchemaError(autos=["Missing key: 'name'"])

    monkeypatch.setattr(
        "letra._internal.parser.labels_schema.validate", mock_validate
    )

    with raises(ValueError) as err:
        extract_labels({"labels": [{}]})
    assert str(err.value) == label_templates_name_schema_error


def test_extract_labels_returns_labels_when_template_is_valid(monkeypatch):
    def mock_validate(data):
        assert data == stub_template_file_contents["labels"]
        return stub_labels

    monkeypatch.setattr(
        "letra._internal.parser.labels_schema.validate", mock_validate
    )
    labels = extract_labels(stub_template_file_contents)
    assert labels == stub_labels
