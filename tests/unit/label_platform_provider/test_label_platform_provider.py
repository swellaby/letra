from pytest import mark, raises
from letra._label_platform_provider.label_platform_provider import (
    get_labels_from_github,
)
from tests.helpers import stub_labels

pytestmark = mark.asyncio
target_owner = "swellaby"
target_repository = "letra"
sut_mock_target = "letra._label_platform_provider.label_platform_provider"
get_from_github_mock_target = (
    f"{sut_mock_target}.get_labels_from_github_repository"
)


async def test_get_labels_from_github_retrieves_labels_when_params_valid(
    monkeypatch,
):
    act_owner = ""
    act_repository = ""
    act_token = ""
    exp_token = "abc123def456"

    async def mock_get_labels_from_github_repository(
        owner: str, repository: str, token: str
    ):
        nonlocal act_owner, act_repository, act_token
        act_owner = owner
        act_repository = repository
        act_token = token
        return stub_labels

    monkeypatch.setattr(
        get_from_github_mock_target, mock_get_labels_from_github_repository
    )

    labels = await get_labels_from_github(
        owner=target_owner, repository=target_repository, token=exp_token
    )

    assert labels == stub_labels
    assert act_owner == target_owner
    assert act_repository == target_repository
    assert act_token == exp_token
