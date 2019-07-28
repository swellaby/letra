from letra import Label
from .parser import extract_labels
from .http_helpers import request_json
from os import environ


def get_base_label_api_url(owner: str, repository: str):
    return f"https://api.github.com/repos/{owner}/{repository}/labels"


def get_headers(token: str = "", authRequired: bool = False):
    def create_auth_header(pat):
        return {"Authorization": f"token {pat}"}

    if token:
        return create_auth_header(token)
    else:
        token = environ.get("LETRA_GITHUB_PAT")
        if token:
            return create_auth_header(token)
        else:
            if not authRequired:
                return {}
            raise ValueError(
                (
                    "GitHub PAT is required for operation, but no token "
                    "was specified. Please provide a valid GitHub PAT for "
                    "the `token` parameter, or set the LETRA_GITHUB_PAT "
                    "environment variable with a valid GitHub PAT."
                )
            )


async def get_labels_from_repository(
    owner: str, repository: str, token: str = ""
):
    url = get_base_label_api_url(owner, repository)
    headers = get_headers(token)
    response = await request_json(url=url, http_verb="get", headers=headers)
    labels = extract_labels({"labels": response.data})
    return labels
