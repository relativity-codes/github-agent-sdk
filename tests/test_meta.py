from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.meta import MetaAPI


@pytest.mark.asyncio
async def test_emojis_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"smile": "https://example.com/smile.png"}
    api = MetaAPI(github)

    result = await api.emojis()

    assert "smile" in result
    github.request.assert_awaited_once_with("GET", "/emojis")


@pytest.mark.asyncio
async def test_events_endpoint_with_pagination() -> None:
    github = AsyncMock()
    github.request.return_value = [{"id": "1"}]
    api = MetaAPI(github)

    result = await api.events(per_page=50, page=2)

    assert result == [{"id": "1"}]
    github.request.assert_awaited_once_with(
        "GET",
        "/events",
        params={"per_page": 50, "page": 2},
    )


@pytest.mark.asyncio
async def test_feeds_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"timeline_url": "https://github.com/timeline"}
    api = MetaAPI(github)

    await api.feeds()

    github.request.assert_awaited_once_with("GET", "/feeds")


@pytest.mark.asyncio
async def test_hub_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"hub_url": "https://api.github.com/hub"}
    api = MetaAPI(github)

    await api.hub()

    github.request.assert_awaited_once_with("GET", "/hub")


@pytest.mark.asyncio
async def test_rate_limit_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = {"resources": {}}
    api = MetaAPI(github)

    await api.rate_limit()

    github.request.assert_awaited_once_with("GET", "/rate_limit")
