from .github import (
    get_labels_from_repository as get_labels_from_github_repository,
)


async def get_labels_from_github(owner: str, repository: str, token: str = ""):
    labels = await get_labels_from_github_repository(
        owner=owner, repository=repository, token=token
    )
    return labels
