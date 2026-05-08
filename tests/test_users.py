from unittest.mock import AsyncMock

import httpx
import pytest

from github_agent_sdk.exceptions import GitHubAuthenticationError
from github_agent_sdk.users import UserAPI


@pytest.mark.asyncio
async def test_emails_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = [{"email": "a@b.com"}]
    api = UserAPI(github)

    result = await api.emails()

    assert result == [{"email": "a@b.com"}]
    github.request.assert_awaited_once_with("GET", "/user/emails")


@pytest.mark.asyncio
async def test_followers_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = [{"login": "octocat"}]
    api = UserAPI(github)

    result = await api.followers()

    assert result == [{"login": "octocat"}]
    github.request.assert_awaited_once_with("GET", "/user/followers")


@pytest.mark.asyncio
async def test_following_endpoint_with_pagination() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = UserAPI(github)

    await api.following(per_page=50, page=2)

    github.request.assert_awaited_once_with(
        "GET",
        "/user/following",
        params={"per_page": 50, "page": 2},
    )


@pytest.mark.asyncio
async def test_is_following_true_on_204() -> None:
    github = AsyncMock()
    github.base_url = "https://api.github.com"
    github.client.request = AsyncMock(return_value=httpx.Response(204))
    api = UserAPI(github)

    result = await api.is_following("octocat")

    assert result is True
    github.client.request.assert_awaited_once_with(
        "GET",
        "https://api.github.com/user/following/octocat",
    )


@pytest.mark.asyncio
async def test_is_following_false_on_404() -> None:
    github = AsyncMock()
    github.base_url = "https://api.github.com"
    github.client.request = AsyncMock(return_value=httpx.Response(404))
    api = UserAPI(github)

    result = await api.is_following("ghost")

    assert result is False


@pytest.mark.asyncio
async def test_is_following_raises_auth_on_401() -> None:
    github = AsyncMock()
    github.base_url = "https://api.github.com"
    github.client.request = AsyncMock(return_value=httpx.Response(401, text="Unauthorized"))
    api = UserAPI(github)

    with pytest.raises(GitHubAuthenticationError):
        await api.is_following("ghost")


@pytest.mark.asyncio
async def test_keys_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = [{"id": 1}]
    api = UserAPI(github)

    await api.keys()

    github.request.assert_awaited_once_with("GET", "/user/keys")


@pytest.mark.asyncio
async def test_user_orgs_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = [{"login": "acme"}]
    api = UserAPI(github)

    await api.organizations()

    github.request.assert_awaited_once_with("GET", "/user/orgs")


@pytest.mark.asyncio
async def test_current_user_repositories_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = UserAPI(github)

    await api.repositories(type="all", page=3, per_page=10, sort="updated")

    github.request.assert_awaited_once_with(
        "GET",
        "/user/repos",
        params={"type": "all", "page": 3, "per_page": 10, "sort": "updated"},
    )


@pytest.mark.asyncio
async def test_user_repositories_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = UserAPI(github)

    await api.user_repositories("octocat", type="member", page=2, per_page=5, sort="created")

    github.request.assert_awaited_once_with(
        "GET",
        "/users/octocat/repos",
        params={"type": "member", "page": 2, "per_page": 5, "sort": "created"},
    )


@pytest.mark.asyncio
async def test_starred_list_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = UserAPI(github)

    await api.starred(page=2, per_page=40)

    github.request.assert_awaited_once_with(
        "GET",
        "/user/starred",
        params={"page": 2, "per_page": 40},
    )


@pytest.mark.asyncio
async def test_has_starred_returns_true_on_204() -> None:
    github = AsyncMock()
    github.base_url = "https://api.github.com"
    github.client.request = AsyncMock(return_value=httpx.Response(204))
    api = UserAPI(github)

    result = await api.has_starred("acme", "repo")

    assert result is True
    github.client.request.assert_awaited_once_with(
        "GET",
        "https://api.github.com/user/starred/acme/repo",
    )
