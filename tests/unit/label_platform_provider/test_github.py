from pytest import mark, raises
from letra._label_platform_provider.github import (
    get_base_label_api_url,
    get_labels_from_repository,
    create_label,
)
from letra import Label
from tests.helpers import stub_request_json_response, stub_labels

sut_module_target = "letra._label_platform_provider.github"

pytestmark = mark.asyncio
request_json_mock_target = f"{sut_module_target}.request_json"
extract_labels_mock_target = f"{sut_module_target}.extract_labels"
get_base_url_mock_target = f"{sut_module_target}.get_base_label_api_url"
get_headers_mock_target = f"{sut_module_target}.get_headers"
environ_get_mock_target = f"{sut_module_target}.environ.get"
exp_base_url = "https://api.github.com/repos/badges/shields/labels"
exp_default_headers = {}


async def test_get_base_label_api_url_returns_correct_url():
    url = get_base_label_api_url(owner="badges", repository="shields")
    assert url == exp_base_url


def stub_helper_functions(monkeypatch, url, headers):
    monkeypatch.setattr(get_base_url_mock_target, lambda *x: url)
    monkeypatch.setattr(get_headers_mock_target, lambda *y: headers)


async def test_get_labels_from_repository_passes_correct_args_to_request_json(
    monkeypatch
):
    act_data = []
    act_url = ""
    exp_url = f"{exp_base_url}?per_page=100"
    act_verb = "post"
    act_headers = {"foo": "bar"}
    stub_helper_functions(monkeypatch, exp_base_url, exp_default_headers)

    async def mock_request_json(url, http_verb, headers, **kwargs):
        nonlocal act_url, act_verb, act_headers
        act_url = url
        act_verb = http_verb
        act_headers = headers
        return stub_request_json_response

    def mock_extract_labels(data):
        nonlocal act_data
        act_data = data
        return stub_labels

    monkeypatch.setattr(request_json_mock_target, mock_request_json)
    monkeypatch.setattr(extract_labels_mock_target, mock_extract_labels)
    labels = await get_labels_from_repository(
        owner="swellaby", repository="pauli"
    )

    assert labels == stub_labels
    assert act_data == {"labels": stub_request_json_response.data}
    assert act_url == exp_url
    assert act_headers == exp_default_headers
    assert act_verb == "get"


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
