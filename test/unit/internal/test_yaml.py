from letra._internal.yaml import (
    read as read_yaml,
    represent_label,
    write as write_yaml,
)
from yaml import FullLoader, YAMLError, Dumper
from test.helpers import (
    bug_label_contents,
    stub_context_manager,
    stub_labels,
    stub_stream,
    bug_label,
)
from pytest import raises

file_name = "templates.yml"


def test_read_loads_file_contents(monkeypatch):
    expected_file_stream = stub_stream

    def mock_open(filepath):
        assert filepath == file_name
        return expected_file_stream

    def mock_load(stream, Loader):
        assert stream == expected_file_stream
        assert Loader == FullLoader
        return stub_labels

    monkeypatch.setattr("builtins.open", mock_open)
    monkeypatch.setattr("letra._internal.yaml.load", mock_load)
    labels = read_yaml(file_name)
    assert labels == stub_labels


def test_read_raises_error_when_file_does_not_exist(monkeypatch):
    def mock_raise(_):
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_raise)

    with raises(FileNotFoundError):
        read_yaml("")


def test_read_raises_value_error_when_yaml_file_not_parseable(monkeypatch):
    def mock_load(stream, Loader):
        raise YAMLError

    monkeypatch.setattr("builtins.open", lambda x: stub_context_manager)
    monkeypatch.setattr("letra._internal.yaml.load", mock_load)

    with raises(ValueError) as err:
        read_yaml("")

    assert str(err.value) == "Specified template file is not valid yaml"


def test_write_raises_value_error_when_yaml_file_not_parseable(monkeypatch):
    act_path = ""
    act_mode = ""

    def mock_raise(filepath, mode):
        nonlocal act_path, act_mode
        act_path = filepath
        act_mode = mode
        raise OSError()

    monkeypatch.setattr("builtins.open", mock_raise)

    with raises(OSError):
        write_yaml(stub_labels, file_name)
    assert act_path == file_name
    assert act_mode == "w+"


def test_write_dumps_values_when_file_exists(monkeypatch):
    expected_file_stream = stub_stream
    act_labels = None
    act_stream = None
    act_dumper = None
    act_sort = None

    def mock_dump(labels, stream, Dumper=None, sort_keys=None):
        nonlocal act_labels, act_stream, act_dumper, act_sort
        act_labels = labels
        act_stream = stream
        act_dumper = Dumper
        act_sort = sort_keys

    monkeypatch.setattr("builtins.open", lambda *unused: stub_context_manager)
    monkeypatch.setattr("letra._internal.yaml.dump", mock_dump)
    write_yaml(stub_labels, file_name)
    assert act_labels == stub_labels
    assert act_stream == stub_stream
    assert act_dumper == Dumper
    assert act_sort is False


def test_represent_label_returns_correct_value(monkeypatch):
    exp_rep = {
        "name": bug_label.name,
        "description": bug_label.description,
        "color": bug_label.color,
    }
    exp_tag = u"tag:yaml.org,2002:map"
    act_tag = ""
    act_data = ""

    class MockDumper:
        @staticmethod
        def represent_mapping(tag, data):
            nonlocal act_tag, act_data
            act_tag = tag
            act_data = data
            return exp_rep

    act_rep = represent_label(MockDumper(), bug_label)

    assert act_tag == exp_tag
    assert act_data == bug_label_contents
    assert act_rep == exp_rep
