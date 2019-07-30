from pytest import mark, raises
from letra.letra import create_label_template_file
from letra import LabelTemplateCreationError
from tests.helpers import stub_labels

pytestmark = mark.asyncio
sut_module_target = "letra.letra"
get_labels_mock_target = f"{sut_module_target}.get_labels"
write_templates_to_file_mock_target = (
    f"{sut_module_target}.write_templates_to_file"
)
target_file_name = "templates.yml"
target_owner = "swellaby"
target_repository = "letra"


async def test_create_label_template_file_raises_err_on_retrieval_value_err(
    monkeypatch
):
    act_owner = ""
    act_repository = ""
    exp_err_details = "401 bad credentials"
    exp_err = (
        "Unable to retrieve labels from target due to invalid inputs. "
        f"Error details: {exp_err_details}"
    )

    async def mock_get_labels(**kwargs):
        nonlocal act_owner, act_repository
        act_owner = kwargs.get("owner")
        act_repository = kwargs.get("repository")
        raise ValueError(exp_err_details)

    monkeypatch.setattr(get_labels_mock_target, mock_get_labels)

    with raises(LabelTemplateCreationError) as err:
        await create_label_template_file(
            filepath=target_file_name,
            owner=target_owner,
            repository=target_repository,
        )

    assert str(err.value) == exp_err
    assert act_owner == target_owner
    assert act_repository == target_repository


async def test_create_label_template_file_raises_err_on_retrieval_io_err(
    monkeypatch
):
    exp_err_details = "github api crashed"
    exp_err = (
        "Encountered error while attempting to retrieve "
        f"labels from target. Error details: {exp_err_details}"
    )

    async def mock_get_labels(**kwargs):
        raise IOError(exp_err_details)

    monkeypatch.setattr(get_labels_mock_target, mock_get_labels)

    with raises(LabelTemplateCreationError) as err:
        await create_label_template_file(
            filepath=target_file_name,
            owner=target_owner,
            repository=target_repository,
        )

    assert str(err.value) == exp_err


async def test_create_label_template_file_raises_err_on_invalid_filepath(
    monkeypatch
):
    act_filepath = None
    act_labels = None
    exp_err_details = "invalid filename"
    exp_err = (
        "Failed to create label template file due to invalid inputs. "
        f"Error details: {exp_err_details}"
    )

    async def mock_get_labels(**kwargs):
        return stub_labels

    def mock_write_templates_to_file(filepath: str, labels):
        nonlocal act_filepath, act_labels
        act_filepath = filepath
        act_labels = labels
        raise ValueError(exp_err_details)

    monkeypatch.setattr(get_labels_mock_target, mock_get_labels)
    monkeypatch.setattr(
        write_templates_to_file_mock_target, mock_write_templates_to_file
    )

    with raises(LabelTemplateCreationError) as err:
        await create_label_template_file(
            filepath=target_file_name,
            owner=target_owner,
            repository=target_repository,
        )

    assert str(err.value) == exp_err
    assert act_filepath == target_file_name
    assert act_labels == stub_labels


async def test_create_label_template_file_raises_err_on_file_write_err(
    monkeypatch
):
    exp_err_details = "no permissions"
    exp_err = (
        "Encountered error while attempting to write labels to file. "
        f"Error details: {exp_err_details}"
    )

    async def mock_get_labels(**kwargs):
        return stub_labels

    def mock_write_templates_to_file(filepath: str, labels):
        raise IOError(exp_err_details)

    monkeypatch.setattr(get_labels_mock_target, mock_get_labels)
    monkeypatch.setattr(
        write_templates_to_file_mock_target, mock_write_templates_to_file
    )

    with raises(LabelTemplateCreationError) as err:
        await create_label_template_file(
            filepath=target_file_name,
            owner=target_owner,
            repository=target_repository,
        )

    assert str(err.value) == exp_err


async def test_create_label_template_file_returns_on_success(monkeypatch):
    async def mock_get_labels(**kwargs):
        return stub_labels

    monkeypatch.setattr(get_labels_mock_target, mock_get_labels)
    monkeypatch.setattr(write_templates_to_file_mock_target, lambda **x: None)

    assert (
        await create_label_template_file(
            filepath=target_file_name,
            owner=target_owner,
            repository=target_repository,
        )
        is None
    )


async def test_foo():
    from letra import create_label_template_file

    await create_label_template_file(
        filepath="tests/data/rusty-hook.yml",
        owner="swellaby",
        repository="rusty-hook",
    )
