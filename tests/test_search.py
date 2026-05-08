from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.search import SearchAPI


@pytest.mark.asyncio
async def test_search_commits_uses_expected_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"items": []}
    api = SearchAPI(github)

    await api.commits("repo:acme/repo fix", limit=20)

    github.request.assert_awaited_once_with(
        "GET",
        "/search/commits",
        params={"q": "repo:acme/repo fix", "per_page": 20},
    )


@pytest.mark.asyncio
async def test_search_issues_uses_expected_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"items": []}
    api = SearchAPI(github)

    await api.issues("repo:acme/repo is:open bug", limit=15)

    github.request.assert_awaited_once_with(
        "GET",
        "/search/issues",
        params={"q": "repo:acme/repo is:open bug", "per_page": 15},
    )


@pytest.mark.asyncio
async def test_search_labels_with_repository_id_and_page() -> None:
    github = AsyncMock()
    github.request.return_value = {"items": []}
    api = SearchAPI(github)

    await api.labels("bug", repository_id=42, page=3, per_page=25)

    github.request.assert_awaited_once_with(
        "GET",
        "/search/labels",
        params={"q": "bug", "repository_id": 42, "per_page": 25, "page": 3},
    )


@pytest.mark.asyncio
async def test_search_topics_uses_expected_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"items": []}
    api = SearchAPI(github)

    await api.topics("python", limit=12)

    github.request.assert_awaited_once_with(
        "GET",
        "/search/topics",
        params={"q": "python", "per_page": 12},
    )


@pytest.mark.asyncio
async def test_search_users_uses_expected_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"items": []}
    api = SearchAPI(github)

    await api.users("type:user location:nigeria", limit=8)

    github.request.assert_awaited_once_with(
        "GET",
        "/search/users",
        params={"q": "type:user location:nigeria", "per_page": 8},
    )
