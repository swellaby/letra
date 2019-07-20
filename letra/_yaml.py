from yaml import dump, load, FullLoader, YAMLError
from letra import Label


def read(filepath):
    try:
        with open(filepath) as stream:
            return load(stream, Loader=FullLoader)
    except YAMLError as err:
        raise ValueError("Specified template file is not valid yaml")
    except Exception:
        raise


# def write_labels_to_file(labels, filepath):
#     dump(labels, open(filepath, "w+"))
