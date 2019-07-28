import pytest
from letra._internal.github import (
    get_base_label_api_url,
    get_headers,
    get_labels_from_repository,
)
from tests.helpers import stub_request_json_response, stub_labels

async_test = pytest.mark.asyncio
sut_module_target = "letra._internal.github"
request_json_mock_target = f"{sut_module_target}.request_json"
extract_labels_mock_target = f"{sut_module_target}.extract_labels"
get_base_url_mock_target = f"{sut_module_target}.get_base_label_api_url"
get_headers_mock_target = f"{sut_module_target}.get_headers"
environ_get_mock_target = f"{sut_module_target}.environ.get"
exp_base_url = "https://api.github.com/repos/badges/shields/labels"
exp_default_headers = {}


def test_get_base_label_api_url_returns_correct_url():
    url = get_base_label_api_url(owner="badges", repository="shields")
    assert url == exp_base_url


def get_auth_header(token):
    return {"Authorization": f"token {token}"}


def test_get_headers_returns_empty_headers_with_no_pat_and_optional_auth(
    monkeypatch
):
    act_var = ""
    exp_var = "LETRA_GITHUB_PAT"

    def mock_environ_get(var_name):
        nonlocal act_var
        act_var = var_name
        return None

    monkeypatch.setattr(environ_get_mock_target, mock_environ_get)
    headers = get_headers()
    assert headers == exp_default_headers
    assert act_var == exp_var


def test_get_headers_raises_value_err_with_no_pat_and_required_auth(
    monkeypatch
):
    exp = (
        "GitHub PAT is required for operation, but no token was specified. "
        "Please provide a valid GitHub PAT for the `token` parameter, "
        "or set the LETRA_GITHUB_PAT environment variable with "
        "a valid GitHub PAT."
    )
    monkeypatch.setattr(environ_get_mock_target, lambda x: None)
    with pytest.raises(ValueError) as err:
        get_headers(token="", authRequired=True)
    assert str(err.value) == exp


def test_get_headers_contains_auth_when_env_set(monkeypatch):
    env_token = "abc123defXYZ"
    monkeypatch.setattr(environ_get_mock_target, lambda x: env_token)
    headers = get_headers()
    assert headers == get_auth_header(env_token)


def test_get_headers_uses_provided_token_over_env(monkeypatch):
    env_token = "environmental"
    exp_token = "123xyz987mno"
    monkeypatch.setattr(environ_get_mock_target, lambda x: env_token)
    headers = get_headers(token=exp_token)
    assert headers == get_auth_header(exp_token)


def stub_helper_functions(monkeypatch, url, headers):
    monkeypatch.setattr(get_base_url_mock_target, lambda *x: url)
    monkeypatch.setattr(get_headers_mock_target, lambda *y: headers)


@async_test
async def test_get_labels_from_repository_passes_correct_args_to_request_json(
    monkeypatch
):
    act_data = []
    act_url = ("",)
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
    assert act_url == exp_base_url
    assert act_headers == exp_default_headers
    assert act_verb == "get"
