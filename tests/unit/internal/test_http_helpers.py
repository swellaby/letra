import pytest
from letra._internal.http_helpers import request_json
from tests.helpers import build_async_http_mock, stub_template_file_contents

pytestmark = pytest.mark.asyncio
request_mock_target = "letra._internal.http_helpers.ClientSession.request"
exp_url = "https://api.github.com/repos/swellaby/letra/labels"
exp_data = stub_template_file_contents["labels"]


async def test_request_json_uses_get_verb_by_default(monkeypatch):
    act_url = "https://google.com"
    act_verb = "post"
    exp_status = 200

    def mock_client_get(*args, method: str, url: str):
        nonlocal act_url, act_verb
        act_verb = method
        act_url = url
        mock_response = build_async_http_mock(exp_data)
        mock_response.status = exp_status
        mock_response.headers = {}
        return mock_response

    monkeypatch.setattr(request_mock_target, mock_client_get)

    response = await request_json(url=exp_url)

    assert response.status == exp_status
    assert response.data == exp_data
    assert act_verb == "get"
    assert act_url == exp_url


async def test_request_json_uses_specified_verb_and_headers(monkeypatch):
    act_verb = ""
    act_headers = {"Authorization": "token abc123def456"}
    exp_verb = "post"
    exp_headers = {
        "Authorization": "token abc123def456",
        "User-Agent": "letra",
    }

    def mock_client_get(*args, method: str, url: str):
        nonlocal act_verb
        act_verb = method
        mock_response = build_async_http_mock(exp_data)
        mock_response.status = 200
        mock_response.headers = {}
        return mock_response

    monkeypatch.setattr(request_mock_target, mock_client_get)

    response = await request_json(
        url=exp_url, http_verb=exp_verb, headers=act_headers
    )

    assert act_verb == exp_verb
    assert act_headers == exp_headers
