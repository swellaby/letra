from letra._yaml import read as read_yaml
from yaml import FullLoader, YAMLError
from test.helpers import stub_context_manager, stub_labels, stub_stream
from pytest import raises


def test_read_labels_from_file(monkeypatch):
    expected_file_stream = stub_stream
    file_name = "templates.yml"

    def mock_open(filepath):
        assert filepath == file_name
        return expected_file_stream

    def mock_load(stream, Loader):
        assert stream == expected_file_stream
        assert Loader == FullLoader
        return stub_labels

    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("letra._yaml.load", mock_load)
    labels = read_yaml(file_name)
    assert labels == stub_labels


def test_raises_error_when_file_does_not_exist(monkeypatch):
    def mock_raise(_):
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_raise)

    with raises(FileNotFoundError):
        read_yaml("")


def test_raises_value_error_when_yaml_file_not_parseable(monkeypatch):
    def mock_load(stream, Loader):
        raise YAMLError

    monkeypatch.setattr("builtins.open", lambda x: stub_context_manager)
    monkeypatch.setattr("letra._yaml.load", mock_load)

    with raises(ValueError) as err:
        read_yaml("")

    assert str(err.value) == "Specified template file is not valid yaml"
