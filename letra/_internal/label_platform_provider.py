from .github import (
    get_labels_from_repository as get_labels_from_github_repository,
)
from letra import LabelPlatformType


async def get_labels_from_github(**kwargs):
    owner_key = "owner"
    repository_key = "repository"
    if owner_key not in kwargs:
        raise ValueError(
            f"{owner_key} is a required argument for GitHub target"
        )
    if repository_key not in kwargs:
        raise ValueError(
            f"{repository_key} is a required argument for GitHub target"
        )

    owner = kwargs.get(owner_key)
    repository = kwargs.get(repository_key)
    token = kwargs.get("token")
    labels = await get_labels_from_github_repository(
        owner=owner, repository=repository, token=token
    )
    return labels


async def get_labels(
    label_platform: LabelPlatformType = LabelPlatformType.GITHUB, **kwargs
):
    labels = await get_labels_from_github(**kwargs)
    return labels
