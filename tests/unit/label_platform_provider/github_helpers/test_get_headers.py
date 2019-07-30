from pytest import raises
from tests.helpers import stub_request_json_response, stub_labels
from . import get_headers, sut_module_target

environ_get_mock_target = f"{sut_module_target}.environ.get"
exp_default_headers = {
    "Accept": "application/vnd.github.symmetra-preview+json"
}


def get_auth_header(token):
    auth_headers = {"Authorization": f"token {token}"}
    auth_headers["Accept"] = exp_default_headers["Accept"]
    return auth_headers


def test_returns_default_headers_with_no_pat_and_optional_auth(monkeypatch):
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


def test_raises_value_err_with_no_pat_and_required_auth(monkeypatch):
    exp = (
        "GitHub PAT is required for operation, but no token was specified. "
        "Please provide a valid GitHub PAT for the `token` parameter, "
        "or set the LETRA_GITHUB_PAT environment variable with "
        "a valid GitHub PAT."
    )
    monkeypatch.setattr(environ_get_mock_target, lambda x: None)
    with raises(ValueError) as err:
        get_headers(token="", auth_required=True)
    assert str(err.value) == exp


def test_contains_auth_when_env_set(monkeypatch):
    env_token = "abc123defXYZ"
    monkeypatch.setattr(environ_get_mock_target, lambda x: env_token)
    headers = get_headers()
    assert headers == get_auth_header(env_token)


def test_uses_provided_token_over_env(monkeypatch):
    env_token = "environmental"
    exp_token = "123xyz987mno"
    monkeypatch.setattr(environ_get_mock_target, lambda x: env_token)
    headers = get_headers(token=exp_token)
    assert headers == get_auth_header(exp_token)
