from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.gists import GistAPI


@pytest.mark.asyncio
async def test_list_gists_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = GistAPI(github)

    await api.list(per_page=25, page=2)

    github.request.assert_awaited_once_with(
        "GET",
        "/gists",
        params={"per_page": 25, "page": 2},
    )


@pytest.mark.asyncio
async def test_get_gist_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"id": "abc"}
    api = GistAPI(github)

    result = await api.get("abc")

    assert result == {"id": "abc"}
    github.request.assert_awaited_once_with("GET", "/gists/abc")


@pytest.mark.asyncio
async def test_public_gists_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = GistAPI(github)

    await api.public(per_page=10, page=4)

    github.request.assert_awaited_once_with(
        "GET",
        "/gists/public",
        params={"per_page": 10, "page": 4},
    )


@pytest.mark.asyncio
async def test_starred_gists_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = []
    api = GistAPI(github)

    await api.starred(per_page=15, page=3)

    github.request.assert_awaited_once_with(
        "GET",
        "/gists/starred",
        params={"per_page": 15, "page": 3},
    )
