from pytest import raises
from . import (
    HttpJsonResponse,
    check_github_api_response_for_errors,
    sut_module_target,
)

exp_owner = "swellaby"
exp_repository = "letra"
raise_github_repository_not_found_error_mock_target = (
    f"{sut_module_target}.raise_github_repository_not_found_error"
)
raise_github_unauthorized_error_mock_target = (
    f"{sut_module_target}.raise_github_unauthorized_error"
)


def call_sut_function(resp):
    return check_github_api_response_for_errors(
        response=resp,
        owner=exp_owner,
        repository=exp_repository,
        request_headers={},
    )


def test_returns_on_200_status_code():
    resp = HttpJsonResponse(status=200, headers={}, data="")
    assert call_sut_function(resp) is None


def test_returns_on_201_status_code():
    resp = HttpJsonResponse(status=201, headers={}, data="")
    assert call_sut_function(resp) is None


def test_returns_on_202_status_code():
    resp = HttpJsonResponse(status=202, headers={}, data="")
    assert call_sut_function(resp) is None


def test_returns_on_203_status_code():
    resp = HttpJsonResponse(status=203, headers={}, data="")
    assert call_sut_function(resp) is None


def test_returns_on_204_status_code():
    resp = HttpJsonResponse(status=204, headers={}, data="")
    assert call_sut_function(resp) is None


def test_raises_correct_err_on_404_status_code(monkeypatch):
    resp = HttpJsonResponse(status=404, headers={}, data="")
    exp_err = "repository not found"
    exp_headers = {"Authorization": "token 9999999"}
    act_owner = ""
    act_repository = ""
    act_req_headers = {}

    def mock_not_found(owner: str, repository: str, request_headers: dict):
        nonlocal act_owner, act_repository, act_req_headers
        act_owner = owner
        act_repository = repository
        act_req_headers = request_headers
        raise ValueError(exp_err)

    monkeypatch.setattr(
        f"{sut_module_target}.raise_github_repository_not_found_error",
        mock_not_found,
    )

    with raises(ValueError) as err:
        check_github_api_response_for_errors(
            response=resp,
            owner=exp_owner,
            repository=exp_repository,
            request_headers=exp_headers,
        )

    assert str(err.value) == exp_err
    assert act_owner == exp_owner
    assert act_repository == exp_repository
    assert act_req_headers == exp_headers


def test_raises_correct_err_on_401_status_code():
    exp_err = (
        f"Invalid authentication. Unable "
        f"to access GitHub repository: {exp_owner}/{exp_repository}"
    )
    resp = HttpJsonResponse(status=401, headers={}, data="")

    with raises(ValueError) as err:
        check_github_api_response_for_errors(
            response=resp,
            owner=exp_owner,
            repository=exp_repository,
            request_headers={},
        )

    assert str(err.value) == exp_err


def test_raises_correct_err_on_403_status_code(monkeypatch):
    resp = HttpJsonResponse(status=403, headers={}, data="")
    exp_err = "not authorized"
    exp_headers = {"Authorization": "token 123987"}
    act_response = {}
    act_owner = ""
    act_repository = ""
    act_req_headers = {}

    def mock_not_authorized(response, owner, repository, request_headers):
        nonlocal act_response, act_owner, act_repository, act_req_headers
        act_response = response
        act_owner = owner
        act_repository = repository
        act_req_headers = request_headers
        raise IOError(exp_err)

    mock_target = f"{sut_module_target}.raise_github_unauthorized_error"
    monkeypatch.setattr(mock_target, mock_not_authorized)

    with raises(IOError) as err:
        check_github_api_response_for_errors(
            response=resp,
            owner=exp_owner,
            repository=exp_repository,
            request_headers=exp_headers,
        )

    assert str(err.value) == exp_err
    assert act_response == resp
    assert act_owner == exp_owner
    assert act_repository == exp_repository
    assert act_req_headers == exp_headers


def test_raises_correct_err_on_unknown_status_code():
    status_code = 500
    exp_err = (
        "Unexpected HTTP error encountered from GitHub API. "
        f"HTTP response status code: {status_code}"
    )
    resp = HttpJsonResponse(status=status_code, headers={}, data="")

    with raises(IOError) as err:
        check_github_api_response_for_errors(
            response=resp,
            owner=exp_owner,
            repository=exp_repository,
            request_headers={},
        )

    assert str(err.value) == exp_err
