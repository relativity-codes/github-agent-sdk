from httpx import Response

from github_agent_sdk.exceptions import GitHubRateLimitError


async def validate_rate_limit(response: Response) -> None:
    if response.status_code == 403:
        remaining = response.headers.get("X-RateLimit-Remaining")
        if remaining == "0":
            raise GitHubRateLimitError("GitHub rate limit exceeded")
