from ._file_io import write_templates_to_file
from ._label_platform_provider import get_labels_from_github
from letra import LabelTemplateCreationError, Label
from typing import List


async def create_label_template_file(labels: List[Label], filepath: str):
    try:
        write_templates_to_file(labels=labels, filepath=filepath)
    except ValueError as err:
        raise LabelTemplateCreationError(
            (
                "Failed to create label template file due to invalid inputs. "
                f"Error details: {str(err)}"
            )
        )
    except Exception as err:
        raise LabelTemplateCreationError(
            (
                "Encountered error while attempting to write labels to file. "
                f"Error details: {str(err)}"
            )
        )


async def _retrieve_labels(get_labels, target_name: str, **kwargs):
    labels = None
    try:
        labels = await get_labels(**kwargs)
    except ValueError as err:
        details = str(err)
        msg = (
            f"Unable to retrieve labels from {target_name} due to invalid "
            f"inputs. Error details: {details}"
        )
        raise LabelTemplateCreationError(msg)
    except Exception as err:
        details = str(err)
        msg = (
            "Encountered error while attempting to retrieve "
            f"labels from {target_name}. Error details: {details}"
        )
        raise LabelTemplateCreationError(msg)

    return labels


async def _create_label_template_file(
    get_labels, filepath: str, target_name: str, **kwargs
):
    labels = await _retrieve_labels(
        get_labels=get_labels, target_name=target_name, **kwargs
    )
    await create_label_template_file(filepath=filepath, labels=labels)


async def create_label_template_file_from_github(
    filepath: str, owner: str, repository: str, token: str = ""
):
    await _create_label_template_file(
        get_labels=get_labels_from_github,
        filepath=filepath,
        target_name="GitHub",
        owner=owner,
        repository=repository,
        token=token,
    )
