from pytest import raises
from . import raise_github_repository_not_found_error

owner = "swellaby"
repository = "letra"
base_not_found_err = (
    f"Specified GitHub repository: {owner}/{repository} not found. "
    "Please check that you have specified the correct owner "
    "and repository name."
)


def test_has_correct_error_with_no_auth():
    exp = (
        f"{base_not_found_err} If you were trying to reference "
        "a private GitHub repository, then authentication must "
        "be provided."
    )
    with raises(ValueError) as err:
        raise_github_repository_not_found_error(
            owner=owner, repository=repository, request_headers={}
        )
    assert str(err.value) == exp


def test_has_correct_error_with_auth():
    with raises(ValueError) as err:
        raise_github_repository_not_found_error(
            owner=owner,
            repository=repository,
            request_headers={"Authorization": ""},
        )
    assert str(err.value) == base_not_found_err
