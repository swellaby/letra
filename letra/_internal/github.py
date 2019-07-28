from letra import Label
from .parser import extract_labels
from .http_helpers import request_json, HttpJsonResponse
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


def raise_github_repository_not_found_error(
    owner: str, repository: str, request_headers: dict
):
    base_not_found_err = (
        f"Specified GitHub repository: {owner}/{repository} not found. "
        "Please check that you have specified the correct owner "
        "and repository name."
    )
    if "Authorization" not in request_headers:
        raise ValueError(
            (
                f"{base_not_found_err} If you were trying to reference "
                "a private GitHub repository, then authentication must "
                "be provided."
            )
        )
    raise ValueError(base_not_found_err)


def handle_github_api_forbidden_response(
    response: HttpJsonResponse, request_headers: dict
):
    response_headers = response.headers

    raise ValueError()
    "X-RateLimit-Remaining"


def check_github_api_response_for_errors(
    response: HttpJsonResponse,
    owner: str,
    repository: str,
    request_headers: dict,
):
    status_code = response.status
    if status_code >= 200 and status_code <= 204:
        return

    if status_code == 404:
        raise_github_repository_not_found_error(
            owner=owner, repository=repository, request_headers=request_headers
        )

    if status_code == 401:
        raise ValueError(
            f"Unauthorized to access GitHub repository: {owner}/{repository}"
        )

    if status_code == 403:
        handle_github_api_forbidden_response(
            response=response, request_headers=request_headers
        )

    raise IOError(
        (
            "Unexpected HTTP error encountered from GitHub API. "
            f"HTTP response status code: {status_code}"
        )
    )


async def get_labels_from_repository(
    owner: str, repository: str, token: str = ""
):
    url = get_base_label_api_url(owner, repository)
    headers = get_headers(token)
    response = await request_json(url=url, http_verb="get", headers=headers)
    check_github_api_response_for_errors(
        response=response,
        owner=owner,
        repository=repository,
        request_headers=headers,
    )
    labels = extract_labels({"labels": response.data})
    return labels
