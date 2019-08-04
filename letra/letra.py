from ._file_io import write_templates_to_file
from ._label_platform_provider import get_labels_from_github
from letra import Label, LabelTemplateCreationError, TemplateFileFormat
from typing import List

__default_label_template_format = TemplateFileFormat.YAML


async def create_label_template_file(
    labels: List[Label],
    filepath: str,
    template_format: TemplateFileFormat = __default_label_template_format,
):
    try:
        write_templates_to_file(
            labels=labels, filepath=filepath, template_format=template_format
        )
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
    try:
        labels = await get_labels(**kwargs)
        return labels
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


async def _create_label_template_file(
    get_labels,
    filepath: str,
    target_name: str,
    template_format: TemplateFileFormat,
    **kwargs,
):
    labels = await _retrieve_labels(
        get_labels=get_labels, target_name=target_name, **kwargs
    )
    await create_label_template_file(
        filepath=filepath, labels=labels, template_format=template_format
    )


async def create_label_template_file_from_github(
    filepath: str,
    owner: str,
    repository: str,
    token: str = "",
    template_format: TemplateFileFormat = __default_label_template_format,
):
    await _create_label_template_file(
        get_labels=get_labels_from_github,
        filepath=filepath,
        template_format=template_format,
        target_name="GitHub",
        owner=owner,
        repository=repository,
        token=token,
    )
