from pytest import mark, raises
from letra._label_platform_provider.github import (
    get_base_label_api_url,
    get_labels_from_repository,
    create_label,
)
from letra._label_platform_provider.http_helpers import HttpJsonResponse
from letra import Label
from tests.helpers import stub_request_json_response, stub_labels

sut_module_target = "letra._label_platform_provider.github"

pytestmark = mark.asyncio
request_json_mock_target = f"{sut_module_target}.request_json"
extract_labels_mock_target = f"{sut_module_target}.extract_labels"
get_base_url_mock_target = f"{sut_module_target}.get_base_label_api_url"
get_headers_mock_target = f"{sut_module_target}.get_headers"
retrieve_labels_mock_target = f"{sut_module_target}.retrieve_labels"
environ_get_mock_target = f"{sut_module_target}.environ.get"
exp_base_url = "https://api.github.com/repos/badges/shields/labels"
exp_default_headers = {}


async def test_get_base_label_api_url_returns_correct_url():
    url = get_base_label_api_url(owner="badges", repository="shields")
    assert url == exp_base_url


def stub_helper_functions(monkeypatch, url, headers):
    monkeypatch.setattr(get_base_url_mock_target, lambda *x: url)
    monkeypatch.setattr(get_headers_mock_target, lambda *y: headers)


async def test_get_labels_from_repository_sub_100_labels(monkeypatch):
    act_url = ""
    exp_url = f"{exp_base_url}?per_page=100"
    act_headers = {"foo": "bar"}
    act_owner = ""
    act_repo = ""
    exp_owner = "swellaby"
    exp_repo = "pauli"
    retrieve_labels_call_count = 0
    stub_helper_functions(monkeypatch, exp_base_url, exp_default_headers)

    async def mock_retrieve_labels(url, headers, owner, repository):
        nonlocal act_url, act_headers, act_owner
        nonlocal act_repo, retrieve_labels_call_count
        act_url = url
        act_headers = headers
        act_owner = owner
        act_repo = repository
        retrieve_labels_call_count += 1
        response = HttpJsonResponse(
            status=200,
            headers={"server": "Github.com"},
            data={},
        )
        return response, stub_labels

    monkeypatch.setattr(retrieve_labels_mock_target, mock_retrieve_labels)
    labels = await get_labels_from_repository(
        owner=exp_owner, repository=exp_repo
    )

    assert labels == stub_labels
    assert retrieve_labels_call_count == 1
    assert act_url == exp_url
    assert act_owner == exp_owner
    assert act_repo == exp_repo
    assert act_headers == exp_default_headers


async def test_get_labels_from_repository_over_100_labels(monkeypatch):
    owner = "rust-lang"
    repo = "rust"
    retrieve_labels_call_count = 0
    first_labels = stub_labels
    second_labels = [
        Label(
            name="E-Easy",
            description=(
                "Call for participation: Experience needed to fix: "
                "Easy / not much"
            ),
            color="5DBCD2",
        ),
        Label(
            name="E-help-wanted",
            description=(
                "Call for participation: Help is requested to "
                "fix this issue."
            ),
            color="FABCD2",
        ),
    ]
    third_labels = [
        Label(
            name="A-Lint",
            description=(
                "Area: Lints (warnings about flaws in source "
                "code) such as unused_mut."
            ),
            color="ffff00 ",
        ),
        Label(
            name="T-Compiler",
            description=(
                "Relevant to the compiler subteam, which "
                "will review and decide on the PR/issue."
            ),
            color="BCD2FA",
        ),
    ]
    base_link_url = "<https://api.github.com/repositories/724712"
    link = (
        f"{base_link_url}/labels?per_page=100&page=2>; "
        'rel="next", '
        f"{base_link_url}/labels?per_page=100&page=3>; "
        'rel="last"'
    )
    mock_http_response = HttpJsonResponse(
        status=200,
        headers={"server": "Github.com", "link": link},
        data={},
    )
    mocked_labels = {1: first_labels, 2: second_labels, 3: third_labels}
    act_urls = {}
    exp_labels = [*first_labels, *second_labels, *third_labels]
    exp_urls = {
        1: f"{exp_base_url}?per_page=100",
        2: f"{exp_base_url}?per_page=100&page=2",
        3: f"{exp_base_url}?per_page=100&page=3",
    }

    async def mock_retrieve_labels(url, headers, owner, repository):
        nonlocal act_urls, retrieve_labels_call_count
        retrieve_labels_call_count += 1
        act_urls[retrieve_labels_call_count] = url

        return mock_http_response, mocked_labels[retrieve_labels_call_count]

    stub_helper_functions(monkeypatch, exp_base_url, exp_default_headers)
    monkeypatch.setattr(retrieve_labels_mock_target, mock_retrieve_labels)
    labels = await get_labels_from_repository(owner=owner, repository=repo)

    assert retrieve_labels_call_count == 3
    assert labels == exp_labels
    assert act_urls == exp_urls


async def test_create_label_passes_correct_args(monkeypatch):
    label_name = "testing123"
    label_color = "8aab7c"
    label_description = "delete me"
    label = Label(
        name=label_name, color=label_color, description=label_description
    )

    act_token = ""
    exp_token = "999999"
    exp_owner = "swellaby"
    exp_repository = "letra"
    act_repository = ""
    act_owner = ""
    act_headers = None
    exp_headers = {"Accept": "application/vnd.github.symmetra-preview+json"}
    exp_url = (
        f"https://api.github.com/repos/{exp_owner}/{exp_repository}/labels"
    )
    act_url = ""
    act_verb = ""
    act_json = None

    def mock_get_base_label_api_url(owner, repository):
        nonlocal act_owner, act_repository
        act_owner = owner
        act_repository = repository
        return exp_url

    def mock_get_headers(token):
        nonlocal act_token
        act_token = token
        return exp_headers

    async def mock_request_json(url, http_verb, headers, json, **kwargs):
        nonlocal act_url, act_verb, act_headers, act_json
        act_url = url
        act_verb = http_verb
        act_headers = headers
        act_json = json
        return stub_request_json_response

    monkeypatch.setattr(get_base_url_mock_target, mock_get_base_label_api_url)
    monkeypatch.setattr(get_headers_mock_target, mock_get_headers)
    monkeypatch.setattr(request_json_mock_target, mock_request_json)

    assert (
        await create_label(
            label=label,
            owner=exp_owner,
            repository=exp_repository,
            token=exp_token,
        )
        is None
    )

    assert act_owner == exp_owner
    assert act_repository == exp_repository
    assert act_token == exp_token
    assert act_url == exp_url
    assert act_headers == exp_headers
    assert act_verb == "post"
    assert act_json == {
        "name": label_name,
        "color": label_color,
        "description": label_description,
    }
