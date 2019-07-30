from pytest import raises
from . import (
    HttpJsonResponse,
    raise_github_unauthorized_error,
    sut_module_target,
)

owner = "swellaby"
repository = "letra"
throttling_err_message_prefix = (
    "GitHub API requests are being rejected due to rate limiting. "
)
throttling_err_message = (
    "The GitHub API will start accepting requests again at: "
    "2013-07-01 12:47:53"
)
exp_non_limited_err = (
    f"Not authorized to access GitHub repository: {owner}/{repository}"
)
get_throttle_reset_message_mock_target = (
    f"{sut_module_target}.get_throttle_reset_message"
)


def test_raises_correct_error_without_rate_limit_header():
    resp = HttpJsonResponse(status=403, headers={}, data="")
    with raises(IOError) as err:
        raise_github_unauthorized_error(
            response=resp,
            owner=owner,
            repository=repository,
            request_headers={},
        )
    assert str(err.value) == exp_non_limited_err


def get_rate_limited_headers(remaining: int = 0, reset: float = 1372700873):
    return {"X-RateLimit-Remaining": remaining, "X-RateLimit-Reset": reset}


def test_raises_correct_error_with_rate_limit_above_zero():
    headers = get_rate_limited_headers(remaining=1)
    resp = HttpJsonResponse(status=403, headers=headers, data="")
    with raises(IOError) as err:
        raise_github_unauthorized_error(
            response=resp,
            owner=owner,
            repository=repository,
            request_headers={},
        )
    assert str(err.value) == exp_non_limited_err


def test_raises_correct_error_with_rate_limit_when_request_has_auth(
    monkeypatch
):
    exp_err = f"{throttling_err_message_prefix}{throttling_err_message}"
    exp_epoch = 1372799123
    act_epoch = 0
    headers = get_rate_limited_headers(remaining=0, reset=exp_epoch)
    resp = HttpJsonResponse(status=403, headers=headers, data="")

    def mock_get_throttle_reset_message(reset_epoch):
        nonlocal act_epoch
        act_epoch = reset_epoch
        return throttling_err_message

    monkeypatch.setattr(
        get_throttle_reset_message_mock_target, mock_get_throttle_reset_message
    )
    with raises(IOError) as err:
        raise_github_unauthorized_error(
            response=resp,
            owner=owner,
            repository=repository,
            request_headers={"Authorization": ""},
        )
    assert str(err.value) == exp_err
    assert act_epoch == exp_epoch


def test_raises_correct_error_with_rate_limit_when_request_missing_auth(
    monkeypatch
):
    exp_err = (
        f"{throttling_err_message_prefix}"
        "You can increase the number of requests that can be "
        "made by including GitHub authentication information. "
        f"{throttling_err_message}"
    )
    headers = get_rate_limited_headers(remaining=0)
    resp = HttpJsonResponse(status=403, headers=headers, data="")
    monkeypatch.setattr(
        get_throttle_reset_message_mock_target,
        lambda x: throttling_err_message,
    )

    with raises(IOError) as err:
        raise_github_unauthorized_error(
            response=resp,
            owner=owner,
            repository=repository,
            request_headers={},
        )
    assert str(err.value) == exp_err
