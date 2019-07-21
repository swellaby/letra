from letra._internal.file_io import (
    read_templates_from_file,
    get_path,
    write_templates_to_file,
)
from yaml import FullLoader, YAMLError
from test.helpers import (
    stub_labels,
    mock_empty,
    mock_false,
    mock_true,
    stub_template_file_contents,
)
from pytest import raises

file_name = "templates.yml"
cwd = "/usr/foo/letra"
joined = f"{cwd}/{file_name}"
relative_template_file = f"../{file_name}"
exp_relative = f"/usr/foo/{file_name}"


def test_get_path_returns_path_when_exact_path_exists(monkeypatch):
    monkeypatch.setattr("letra._internal.file_io.path_exists", mock_true)
    exp = f"/bar/{file_name}"
    filepath = get_path(exp)
    assert filepath == exp


def test_get_path_returns_path_when_relative_path_exists(monkeypatch):
    def mock_path_exists(path):
        if path == exp_relative:
            return True
        return False

    def mock_join(a, b):
        assert a == cwd
        assert b == relative_template_file
        return joined

    def mock_abspath(filepath):
        assert filepath == joined
        return exp_relative

    monkeypatch.setattr("letra._internal.file_io.getcwd", lambda: cwd)
    monkeypatch.setattr("letra._internal.file_io.join", mock_join)
    monkeypatch.setattr("letra._internal.file_io.abspath", mock_abspath)
    monkeypatch.setattr(
        "letra._internal.file_io.path_exists", mock_path_exists
    )

    filepath = get_path(relative_template_file)
    assert filepath == exp_relative


def test_get_path_raises_error_when_file_does_not_exist(monkeypatch):
    exp_err = (
        "Specified template file not found.\n"
        f"Checked relative path: '{relative_template_file}' "
        f"and absolute path: '{exp_relative}'"
    )

    monkeypatch.setattr("letra._internal.file_io.path_exists", mock_false)
    monkeypatch.setattr("letra._internal.file_io.getcwd", mock_empty)
    monkeypatch.setattr("letra._internal.file_io.join", mock_empty)
    monkeypatch.setattr(
        "letra._internal.file_io.abspath", lambda x: exp_relative
    )

    with raises(ValueError) as err:
        get_path(relative_template_file)
    assert str(err.value) == exp_err


def test_read_template_from_file_returns_contents(monkeypatch):
    def mock_read_yaml(path):
        assert path == joined
        return stub_template_file_contents

    monkeypatch.setattr("letra._internal.file_io.path_exists", mock_true)
    monkeypatch.setattr("letra._internal.file_io.read_yaml", mock_read_yaml)
    contents = read_templates_from_file(joined)
    assert contents == stub_template_file_contents


def test_read_template_bubbles_errors_from_yaml_loading(monkeypatch):
    exp_err = "invalid yaml"

    def mock_read_yaml(path):
        raise ValueError(exp_err)

    monkeypatch.setattr("letra._internal.file_io.path_exists", mock_true)
    monkeypatch.setattr("letra._internal.file_io.read_yaml", mock_read_yaml)

    with raises(ValueError) as err:
        read_templates_from_file(joined)
    assert str(err.value) == exp_err


def test_write_templates_to_file(monkeypatch):
    act_path = ""
    act_labels = []

    def mock_write_yaml(labels, path):
        nonlocal act_labels, act_path
        act_labels = labels
        act_path = path

    monkeypatch.setattr("letra._internal.file_io.path_exists", mock_true)
    monkeypatch.setattr("letra._internal.file_io.write_yaml", mock_write_yaml)
    write_templates_to_file(stub_labels, file_name)
    assert act_labels == {"labels": stub_labels}
    assert act_path == file_name


def test_write_templates_bubbles_errors_from_yaml_loading(monkeypatch):
    exp_err = "crashed"

    def mock_write_yaml(*unused):
        raise ValueError(exp_err)

    monkeypatch.setattr("letra._internal.file_io.path_exists", mock_true)
    monkeypatch.setattr("letra._internal.file_io.write_yaml", mock_write_yaml)

    with raises(ValueError) as err:
        write_templates_to_file(stub_labels, joined)
    assert str(err.value) == exp_err
