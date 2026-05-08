from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.models.pull_request import PullRequest
from github_agent_sdk.pulls import PullRequestAPI


@pytest.mark.asyncio
async def test_create_pull_request_returns_model() -> None:
    github = AsyncMock()
    github.request.return_value = {
        "id": 5,
        "number": 12,
        "title": "Fix bug",
        "state": "open",
        "html_url": "https://github.com/acme/repo/pull/12",
    }
    api = PullRequestAPI(github)

    result = await api.create(
        "acme",
        "repo",
        title="Fix bug",
        body="body",
        head="fix-branch",
        base="main",
    )

    assert isinstance(result, PullRequest)
    assert result.number == 12
    github.request.assert_awaited_once_with(
        "POST",
        "/repos/acme/repo/pulls",
        json={
            "title": "Fix bug",
            "body": "body",
            "head": "fix-branch",
            "base": "main",
        },
    )
