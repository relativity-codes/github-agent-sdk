from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.agent import GitHubAgent
from github_agent_sdk.gists import GistAPI
from github_agent_sdk.meta import MetaAPI
from github_agent_sdk.notifications import NotificationAPI


@pytest.mark.asyncio
async def test_create_fix_pull_request_uses_default_branch_flow() -> None:
    github = AsyncMock()
    agent = GitHubAgent(github)

    agent.repositories.get = AsyncMock(
        return_value=type("Repo", (), {"default_branch": "develop"})()
    )
    agent.branches.create = AsyncMock()
    agent.contents.create_or_update = AsyncMock()
    agent.pulls.create = AsyncMock(return_value={"id": 1, "number": 4})

    result = await agent.create_fix_pull_request(
        owner="acme",
        repo="repo",
        file_path="README.md",
        content="updated",
        branch_name="fix/readme",
        commit_message="Update readme",
        pr_title="Fix README",
        pr_body="This updates README.",
    )

    assert result == {"id": 1, "number": 4}
    agent.repositories.get.assert_awaited_once_with("acme", "repo")
    agent.branches.create.assert_awaited_once_with(
        "acme",
        "repo",
        branch="fix/readme",
        from_branch="develop",
    )
    agent.contents.create_or_update.assert_awaited_once_with(
        "acme",
        "repo",
        path="README.md",
        content="updated",
        message="Update readme",
        branch="fix/readme",
    )
    agent.pulls.create.assert_awaited_once_with(
        "acme",
        "repo",
        title="Fix README",
        body="This updates README.",
        head="fix/readme",
        base="develop",
    )


def test_agent_wires_new_api_modules() -> None:
    github = AsyncMock()
    agent = GitHubAgent(github)

    assert isinstance(agent.gists, GistAPI)
    assert isinstance(agent.notifications, NotificationAPI)
    assert isinstance(agent.meta, MetaAPI)
