from ._file_io import write_templates_to_file
from ._label_platform_provider import get_labels
from letra import LabelTemplateCreationError


async def create_label_template_file(filepath: str, **kwargs):
    labels = None
    try:
        labels = await get_labels(**kwargs)
    except ValueError as err:
        details = str(err)
        msg = (
            "Unable to retrieve labels from target due to invalid inputs. "
            f"Error details: {details}"
        )
        raise LabelTemplateCreationError(msg)
    except Exception as err:
        details = str(err)
        msg = (
            "Encountered error while attempting to retrieve "
            f"labels from target. Error details: {details}"
        )
        raise LabelTemplateCreationError(msg)
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
