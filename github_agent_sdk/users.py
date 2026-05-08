from github_agent_sdk.exceptions import GitHubAPIError, GitHubAuthenticationError


class UserAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def me(self) -> dict:
        return await self.github.request("GET", "/user")

    async def get(self, username: str) -> dict:
        return await self.github.request("GET", f"/users/{username}")

    async def emails(self) -> list[dict]:
        return await self.github.request("GET", "/user/emails")

    async def followers(self) -> list[dict]:
        return await self.github.request("GET", "/user/followers")

    async def following(self, *, per_page: int = 30, page: int = 1) -> list[dict]:
        return await self.github.request(
            "GET",
            "/user/following",
            params={"per_page": per_page, "page": page},
        )

    async def is_following(self, target: str) -> bool:
        response = await self.github.client.request(
            "GET",
            f"{self.github.base_url}/user/following/{target}",
        )
        if response.status_code == 204:
            return True
        if response.status_code == 404:
            return False
        if response.status_code == 401:
            raise GitHubAuthenticationError("Invalid GitHub token")
        if response.status_code >= 400:
            raise GitHubAPIError(response.text)
        return True

    async def keys(self) -> list[dict]:
        return await self.github.request("GET", "/user/keys")

    async def organizations(self) -> list[dict]:
        return await self.github.request("GET", "/user/orgs")

    async def repositories(
        self,
        *,
        type: str = "owner",
        page: int = 1,
        per_page: int = 30,
        sort: str = "full_name",
    ) -> list[dict]:
        return await self.github.request(
            "GET",
            "/user/repos",
            params={"type": type, "page": page, "per_page": per_page, "sort": sort},
        )

    async def user_repositories(
        self,
        username: str,
        *,
        type: str = "owner",
        page: int = 1,
        per_page: int = 30,
        sort: str = "full_name",
    ) -> list[dict]:
        return await self.github.request(
            "GET",
            f"/users/{username}/repos",
            params={"type": type, "page": page, "per_page": per_page, "sort": sort},
        )

    async def starred(
        self,
        *,
        page: int = 1,
        per_page: int = 30,
    ) -> list[dict]:
        return await self.github.request(
            "GET",
            "/user/starred",
            params={"page": page, "per_page": per_page},
        )

    async def has_starred(self, owner: str, repo: str) -> bool:
        response = await self.github.client.request(
            "GET",
            f"{self.github.base_url}/user/starred/{owner}/{repo}",
        )
        if response.status_code == 204:
            return True
        if response.status_code == 404:
            return False
        if response.status_code == 401:
            raise GitHubAuthenticationError("Invalid GitHub token")
        if response.status_code >= 400:
            raise GitHubAPIError(response.text)
        return True
