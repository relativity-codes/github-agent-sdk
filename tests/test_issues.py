from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.issues import IssueAPI
from github_agent_sdk.models.issue import Issue


@pytest.mark.asyncio
async def test_create_issue_returns_model() -> None:
    github = AsyncMock()
    github.request.return_value = {
        "id": 9,
        "number": 2,
        "title": "Bug",
        "state": "open",
        "html_url": "https://github.com/acme/repo/issues/2",
    }
    api = IssueAPI(github)

    result = await api.create(
        "acme",
        "repo",
        title="Bug",
        body="Please fix",
        labels=["bug"],
    )

    assert isinstance(result, Issue)
    assert result.title == "Bug"
    github.request.assert_awaited_once_with(
        "POST",
        "/repos/acme/repo/issues",
        json={"title": "Bug", "body": "Please fix", "labels": ["bug"]},
    )


@pytest.mark.asyncio
async def test_list_global_issues_sends_expected_query_params() -> None:
    github = AsyncMock()
    github.request.return_value = [{"id": 1, "title": "Issue"}]
    api = IssueAPI(github)

    result = await api.list(filter="created", state="all", per_page=50, page=2)

    assert result == [{"id": 1, "title": "Issue"}]
    github.request.assert_awaited_once_with(
        "GET",
        "/issues",
        params={"filter": "created", "state": "all", "per_page": 50, "page": 2},
    )
