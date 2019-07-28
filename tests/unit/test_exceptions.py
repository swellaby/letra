from letra.exceptions import LabelTemplateCreationError
from pytest import raises


def test_label_template_creation_error():
    exp_err = "failed to create label template"
    with raises(LabelTemplateCreationError) as err:
        raise LabelTemplateCreationError(exp_err)
    assert str(err.value) == exp_err
