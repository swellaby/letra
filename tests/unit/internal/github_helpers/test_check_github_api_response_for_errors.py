from pytest import raises
from . import (
    HttpJsonResponse,
    check_github_api_response_for_errors,
    sut_module_target,
)

owner = "swellaby"
repository = "letra"
raise_github_repository_not_found_error_mock_target = (
    f"{sut_module_target}.raise_github_repository_not_found_error"
)
raise_github_unauthorized_error_mock_target = (
    f"{sut_module_target}.raise_github_unauthorized_error"
)

def call_sut_function(resp):
    return check_github_api_response_for_errors(
        response=resp,
        owner=owner,
        repository=repository,
        request_headers={},
    )


def test_returns_on_200_status_code():
    resp = HttpJsonResponse(status=200, headers={}, data="")
    res = call_sut_function(resp)
    assert res == None


def test_returns_on_201_status_code():
    resp = HttpJsonResponse(status=201, headers={}, data="")
    res = call_sut_function(resp)
    assert res == None


def test_returns_on_202_status_code():
    resp = HttpJsonResponse(status=202, headers={}, data="")
    res = call_sut_function(resp)
    assert res == None


def test_returns_on_203_status_code():
    resp = HttpJsonResponse(status=203, headers={}, data="")
    res = call_sut_function(resp)
    assert res == None


def test_returns_on_204_status_code():
    resp = HttpJsonResponse(status=204, headers={}, data="")
    res = call_sut_function(resp)
    assert res == None
