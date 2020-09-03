from pytest import mark
from tests.helpers import stub_request_json_response, stub_labels
from . import retrieve_labels

sut_module_target = "letra._label_platform_provider.github_helpers"

pytestmark = mark.asyncio
request_json_mock_target = f"{sut_module_target}.request_json"
extract_labels_mock_target = f"{sut_module_target}.extract_labels"
check_github_api_response_for_errors_mock_target = (
    f"{sut_module_target}.check_github_api_response_for_errors"
)
exp_base_url = "https://api.github.com/repos/badges/shields/labels"


async def test_passes_correct_args_to_request_json(
    monkeypatch,
):
    act_data = []
    act_url = ""
    exp_url = f"{exp_base_url}?per_page=100"
    act_verb = "post"
    act_headers = {"foo": "bar"}
    exp_default_headers = {}

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
    act_response, labels = await retrieve_labels(
        url=exp_url,
        headers=exp_default_headers,
        owner="swellaby",
        repository="pauli",
    )

    assert labels == stub_labels
    assert act_response == stub_request_json_response
    assert act_data == {"labels": stub_request_json_response.data}
    assert act_url == exp_url
    assert act_headers == exp_default_headers
    assert act_verb == "get"


async def test_checks_response(monkeypatch):
    act_response = {}
    act_owner = ""
    act_repo = ""
    act_request_headers = {}

    exp_response = stub_request_json_response
    exp_owner = "rust-lang"
    exp_repo = "rustfmt"
    exp_request_headers = {
        "Accept": "application/vnd.github.symmetra-preview+json"
    }

    async def mock_request_json(**kwargs):
        return stub_request_json_response

    def mock_extract_labels(*unused):
        return stub_labels

    def mock_check_github_api_response_for_errors(
        response, owner, repository, request_headers
    ):
        nonlocal act_response, act_owner, act_repo, act_request_headers
        act_response = response
        act_owner = owner
        act_repo = repository
        act_request_headers = request_headers

    monkeypatch.setattr(request_json_mock_target, mock_request_json)
    monkeypatch.setattr(extract_labels_mock_target, mock_extract_labels)
    monkeypatch.setattr(
        check_github_api_response_for_errors_mock_target,
        mock_check_github_api_response_for_errors,
    )

    await retrieve_labels(
        url=f"{exp_base_url}?per_page=100",
        headers=exp_request_headers,
        owner=exp_owner,
        repository=exp_repo,
    )

    assert act_response == exp_response
    assert act_owner == exp_owner
    assert act_repo == exp_repo
    assert act_request_headers == exp_request_headers
