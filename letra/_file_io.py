from letra._yaml import read as read_yaml
from os import getcwd
from os.path import abspath, join, exists as path_exists
from string import Template


def get_path(filepath):
    if path_exists(filepath):
        return filepath
    else:
        path = abspath(join(getcwd(), filepath))
        if path_exists(path):
            return path
        else:
            raise ValueError(
                "Specified template file not found.\n"
                f"Checked relative path: '{path}' and absolute path: '{filepath}'"
            )


def read_template_from_file(filepath):
    return read_yaml(get_path(filepath))
