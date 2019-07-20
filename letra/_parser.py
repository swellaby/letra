from schema import Optional, Regex, Schema, SchemaError
from letra import Label

color_regex = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"

label_schema = Schema(
    {
        "name": str,
        Optional("description"): str,
        Optional("color"): Regex(color_regex),
    }
)

labels_schema = Schema([label_schema])


def build_invalid_label_error(schema_error):
    return (
        "Labels must conform to the schema:\n"
        "`name`: Required - string\n"
        "`description`: Optional - string\n"
        "`color`: Optional - valid hex color string\n"
        "Error details: " + schema_error.autos[-1]
    )


def extract_label(label):
    try:
        label_schema.validate(label)
    except SchemaError as err:
        raise ValueError(("Invalid label. " + build_invalid_label_error(err)))

    return Label(
        name=label["name"],
        description=label["description"],
        color=label["color"],
    )


def extract_labels(data):
    labels = data.get("labels")
    if labels is None:
        raise ValueError(
            "Invalid label template. Root level `labels` field missing."
        )
    if len(labels) == 0:
        raise ValueError("No labels found in provided label template.")

    try:
        labels_schema.validate(labels)
    except SchemaError as err:
        msg = (
            "One or more label templates are invalid. "
            + build_invalid_label_error(err)
        )
        raise ValueError(msg)

    return [
        Label(name=l["name"], description=l["description"], color=l["color"])
        for l in labels
    ]
