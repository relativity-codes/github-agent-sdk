from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.notifications import NotificationAPI


@pytest.mark.asyncio
async def test_notifications_list_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = [{"id": "thread_1"}]
    api = NotificationAPI(github)

    result = await api.list(all=True, participating=True, per_page=10, page=3)

    assert result == [{"id": "thread_1"}]
    github.request.assert_awaited_once_with(
        "GET",
        "/notifications",
        params={"all": "true", "participating": "true", "per_page": 10, "page": 3},
    )
