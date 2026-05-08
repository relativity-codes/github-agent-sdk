from unittest.mock import AsyncMock

import pytest

from github_agent_sdk.organizations import OrganizationAPI


@pytest.mark.asyncio
async def test_organization_teams_endpoint() -> None:
    github = AsyncMock()
    github.request.return_value = [{"id": 1, "name": "platform"}]
    api = OrganizationAPI(github)

    result = await api.teams("acme", per_page=50)

    assert result == [{"id": 1, "name": "platform"}]
    github.request.assert_awaited_once_with(
        "GET",
        "/orgs/acme/teams",
        params={"per_page": 50},
    )
