from letra._yaml import read_labels_from_file
from yaml import FullLoader, YAMLError
from test.helpers import (
    empty_mock,
    stub_context_manager,
    stub_labels,
    stub_stream,
)
from pytest import raises


def test_read_labels_from_file(monkeypatch):
    expected_file_stream = stub_stream
    file_name = "templates.yml"
    cwd = "/usr/foo/letra"
    joined = f"{cwd}/${file_name}"

    def mock_join(a, b):
        assert a == cwd
        assert b == file_name
        return joined

    def mock_abspath(filepath):
        assert filepath == joined
        return filepath

    def mock_open(filepath):
        assert filepath == joined
        return expected_file_stream

    def mock_load(stream, Loader):
        assert stream == expected_file_stream
        assert Loader == FullLoader
        return stub_labels

    monkeypatch.setattr("letra._yaml.getcwd", lambda: cwd)
    monkeypatch.setattr("letra._yaml.join", mock_join)
    monkeypatch.setattr("letra._yaml.abspath", mock_abspath)
    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("letra._yaml.load", mock_load)
    labels = read_labels_from_file(file_name)
    assert labels == stub_labels


def test_raises_error_when_file_does_not_exist(monkeypatch):
    def mock_raise(_):
        raise FileNotFoundError()

    monkeypatch.setattr("letra._yaml.getcwd", empty_mock)
    monkeypatch.setattr("letra._yaml.join", empty_mock)
    monkeypatch.setattr("letra._yaml.abspath", empty_mock)
    monkeypatch.setattr("builtins.open", mock_raise)

    with raises(FileNotFoundError):
        read_labels_from_file("")


def test_raises_value_error_when_yaml_file_not_parseable(monkeypatch):
    def mock_load(stream, Loader):
        raise YAMLError

    monkeypatch.setattr("letra._yaml.getcwd", empty_mock)
    monkeypatch.setattr("letra._yaml.join", empty_mock)
    monkeypatch.setattr("letra._yaml.abspath", empty_mock)
    monkeypatch.setattr("builtins.open", lambda x: stub_context_manager)
    monkeypatch.setattr("letra._yaml.load", mock_load)

    with raises(ValueError) as err:
        read_labels_from_file("")

    assert str(err.value) == "Specified template file is not valid yaml"
