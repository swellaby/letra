from os import getcwd
from os.path import abspath, join
from yaml import dump, load, FullLoader, YAMLError


def get_path(filepath):
    return abspath(join(getcwd(), filepath))


def read_labels_from_file(filepath):
    try:
        return load(open(get_path(filepath)), Loader=FullLoader)
    except YAMLError as err:
        raise ValueError("Unable to parse specified yaml file")
    except Exception:
        raise


# def write_labels_to_file(labels, filepath):
#     dump(labels, open(filepath, "w+"))
