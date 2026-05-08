from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.models.repository import Repository
from github_agent_sdk.repositories import RepositoryAPI


@pytest.mark.asyncio
async def test_get_repository_returns_model() -> None:
    github = AsyncMock()
    github.request.return_value = {
        "id": 1,
        "name": "repo",
        "full_name": "acme/repo",
        "private": False,
        "default_branch": "main",
    }
    api = RepositoryAPI(github)

    result = await api.get("acme", "repo")

    assert isinstance(result, Repository)
    assert result.full_name == "acme/repo"
    github.request.assert_awaited_once_with("GET", "/repos/acme/repo")


@pytest.mark.asyncio
async def test_create_repository_sends_expected_payload() -> None:
    github = AsyncMock()
    github.request.return_value = {"name": "my-repo"}
    api = RepositoryAPI(github)

    await api.create(
        "my-repo",
        private=True,
        description="desc",
        auto_init=False,
    )

    github.request.assert_awaited_once_with(
        "POST",
        "/user/repos",
        json={
            "name": "my-repo",
            "private": True,
            "description": "desc",
            "auto_init": False,
        },
    )
