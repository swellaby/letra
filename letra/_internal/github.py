from letra import Label
from .parser import extract_labels
from .http_helpers import request_json


def get_base_label_api_url(owner: str, repository: str):
    return f"https://api.github.com/repos/{owner}/{repository}/labels"


def get_headers(token: str = ""):
    return {}


async def get_labels_from_repository(
    owner: str, repository: str, token: str = ""
):
    url = get_base_label_api_url(owner, repository)
    headers = get_headers(token)
    response = await request_json(url=url, http_verb="get", headers=headers)
    labels = extract_labels({"labels": response.data})
    return labels
