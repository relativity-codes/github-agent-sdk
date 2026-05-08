from __future__ import annotations

from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from github_agent_sdk.auth import TokenAuth
from github_agent_sdk.constants import (
    API_VERSION,
    BASE_URL,
    DEFAULT_TIMEOUT,
    DEFAULT_USER_AGENT,
)
from github_agent_sdk.exceptions import GitHubAPIError, GitHubAuthenticationError
from github_agent_sdk.rate_limit import validate_rate_limit


class GitHub:
    def __init__(
        self,
        token: str,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        base_url: str = BASE_URL,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.base_url = base_url
        auth = TokenAuth(token)
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                **auth.headers(),
                "Accept": "application/vnd.github+json",
                "User-Agent": user_agent,
                "X-GitHub-Api-Version": API_VERSION,
            },
        )

    async def close(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> GitHub:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    @retry(
        retry=retry_if_exception_type(httpx.TransportError),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=20),
    )
    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        response = await self.client.request(
            method,
            f"{self.base_url}{endpoint}",
            params=params,
            json=json,
        )

        await validate_rate_limit(response)

        if response.status_code == 401:
            raise GitHubAuthenticationError("Invalid GitHub token")

        if response.status_code >= 400:
            raise GitHubAPIError(response.text)

        if not response.content:
            return {}

        return response.json()
