from os import getcwd
from os.path import abspath, join
from yaml import dump, load, FullLoader, YAMLError
from letra import Label


def get_path(filepath):
    return abspath(join(getcwd(), filepath))


def read_labels_from_file(filepath):
    try:
        with open(get_path(filepath)) as stream:
            return load(stream, Loader=FullLoader)
    except YAMLError as err:
        raise ValueError("Specified template file is not valid yaml")
    except Exception:
        raise


# def write_labels_to_file(labels, filepath):
#     dump(labels, open(filepath, "w+"))
