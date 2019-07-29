from letra._internal.file_io import (
    read_templates_from_file,
    get_path_for_read,
    get_path_for_write,
    write_templates_to_file,
)
from yaml import FullLoader, YAMLError
from tests.helpers import (
    stub_labels,
    mock_empty,
    mock_false,
    mock_true,
    stub_template_file_contents,
)
from pytest import raises

sut_module_target = "letra._internal.file_io"
path_exists_mock_target = f"{sut_module_target}.path_exists"
getcwd_mock_target = f"{sut_module_target}.getcwd"
join_mock_target = f"{sut_module_target}.join"
abspath_mock_target = f"{sut_module_target}.abspath"
read_yaml_mock_target = f"{sut_module_target}.read_yaml"
write_yaml_mock_target = f"{sut_module_target}.write_yaml"
file_name = "templates.yml"
cwd = "/usr/foo/letra"
joined = f"{cwd}/{file_name}"
relative_template_file = f"../{file_name}"
exp_relative = f"/usr/foo/{file_name}"


def test_get_path_for_read_returns_path_when_exact_path_exists(monkeypatch):
    monkeypatch.setattr(path_exists_mock_target, mock_true)
    exp = f"/bar/{file_name}"
    filepath = get_path_for_read(exp)
    assert filepath == exp


def test_get_path_for_read_returns_path_when_relative_path_exists(monkeypatch):
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

    monkeypatch.setattr(getcwd_mock_target, lambda: cwd)
    monkeypatch.setattr(join_mock_target, mock_join)
    monkeypatch.setattr(abspath_mock_target, mock_abspath)
    monkeypatch.setattr(path_exists_mock_target, mock_path_exists)

    filepath = get_path_for_read(relative_template_file)
    assert filepath == exp_relative


def test_get_path_for_read_raises_error_when_file_does_not_exist(monkeypatch):
    exp_err = (
        "Specified template file not found.\n"
        f"Checked relative path: '{relative_template_file}' "
        f"and absolute path: '{exp_relative}'"
    )

    monkeypatch.setattr(path_exists_mock_target, mock_false)
    monkeypatch.setattr(getcwd_mock_target, mock_empty)
    monkeypatch.setattr(join_mock_target, mock_empty)
    monkeypatch.setattr(abspath_mock_target, lambda x: exp_relative)

    with raises(ValueError) as err:
        get_path_for_read(relative_template_file)
    assert str(err.value) == exp_err


def test_get_path_for_write_raises_err_on_invalid_filepath():
    exp_err = "Invalid filepath specified"
    with raises(ValueError) as err:
        get_path_for_write(None)
    assert str(err.value) == exp_err


def test_get_path_for_write_returns_correct_path_on_relative_filepath(
    monkeypatch
):
    def mock_join(a, b):
        assert a == cwd
        assert b == relative_template_file
        return joined

    def mock_abspath(filepath):
        assert filepath == joined
        return exp_relative

    monkeypatch.setattr(getcwd_mock_target, lambda: cwd)
    monkeypatch.setattr(join_mock_target, mock_join)
    monkeypatch.setattr(abspath_mock_target, mock_abspath)
    act = get_path_for_write(filepath=relative_template_file)
    assert act == exp_relative


def test_get_path_for_write_returns_filepath_on_non_relative_value():
    exp = f"foo/{file_name}"
    act = get_path_for_write(filepath=exp)
    assert act == exp


def test_read_template_from_file_returns_contents(monkeypatch):
    def mock_read_yaml(path):
        assert path == joined
        return stub_template_file_contents

    monkeypatch.setattr(path_exists_mock_target, mock_true)
    monkeypatch.setattr(read_yaml_mock_target, mock_read_yaml)
    contents = read_templates_from_file(joined)
    assert contents == stub_template_file_contents


def test_read_template_bubbles_errors_from_yaml_loading(monkeypatch):
    exp_err = "invalid yaml"

    def mock_read_yaml(path):
        raise ValueError(exp_err)

    monkeypatch.setattr(path_exists_mock_target, mock_true)
    monkeypatch.setattr(read_yaml_mock_target, mock_read_yaml)

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

    monkeypatch.setattr(write_yaml_mock_target, mock_write_yaml)
    write_templates_to_file(stub_labels, joined)
    assert act_labels == {"labels": stub_labels}
    assert act_path == joined


def test_write_templates_bubbles_errors_from_yaml_loading(monkeypatch):
    exp_err = "crashed"

    def mock_write_yaml(*unused):
        raise ValueError(exp_err)

    monkeypatch.setattr(write_yaml_mock_target, mock_write_yaml)

    with raises(ValueError) as err:
        write_templates_to_file(stub_labels, joined)
    assert str(err.value) == exp_err
