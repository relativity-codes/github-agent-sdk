import httpx
import pytest

from github_agent_sdk.client import GitHub
from github_agent_sdk.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
    GitHubRateLimitError,
)


@pytest.mark.asyncio
async def test_request_returns_json_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer token"
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    github = GitHub(token="token")
    github.client = httpx.AsyncClient(transport=transport, headers=github.client.headers)

    result = await github.request("GET", "/health")

    assert result == {"ok": True}
    await github.close()


@pytest.mark.asyncio
async def test_request_raises_authentication_error() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="Unauthorized")

    github = GitHub(token="token")
    github.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        headers=github.client.headers,
    )

    with pytest.raises(GitHubAuthenticationError):
        await github.request("GET", "/bad")

    await github.close()


@pytest.mark.asyncio
async def test_request_raises_rate_limit_error() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(
            403,
            text="rate limit",
            headers={"X-RateLimit-Remaining": "0"},
        )

    github = GitHub(token="token")
    github.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        headers=github.client.headers,
    )

    with pytest.raises(GitHubRateLimitError):
        await github.request("GET", "/limited")

    await github.close()


@pytest.mark.asyncio
async def test_request_raises_api_error_for_other_4xx() -> None:
    async def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(422, text="unprocessable")

    github = GitHub(token="token")
    github.client = httpx.AsyncClient(
        transport=httpx.MockTransport(handler),
        headers=github.client.headers,
    )

    with pytest.raises(GitHubAPIError):
        await github.request("GET", "/invalid")

    await github.close()
