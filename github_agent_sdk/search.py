class SearchAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def repositories(self, query: str, limit: int = 10) -> dict:
        return await self.github.request(
            "GET",
            "/search/repositories",
            params={"q": query, "per_page": limit},
        )

    async def code(self, query: str, limit: int = 10) -> dict:
        return await self.github.request(
            "GET",
            "/search/code",
            params={"q": query, "per_page": limit},
        )

    async def commits(self, query: str, limit: int = 10) -> dict:
        return await self.github.request(
            "GET",
            "/search/commits",
            params={"q": query, "per_page": limit},
        )

    async def issues(self, query: str, limit: int = 10) -> dict:
        return await self.github.request(
            "GET",
            "/search/issues",
            params={"q": query, "per_page": limit},
        )

    async def labels(
        self,
        query: str,
        repository_id: int,
        *,
        page: int | None = None,
        per_page: int = 10,
    ) -> dict:
        params: dict[str, int | str] = {
            "q": query,
            "repository_id": repository_id,
            "per_page": per_page,
        }
        if page is not None:
            params["page"] = page
        return await self.github.request(
            "GET",
            "/search/labels",
            params=params,
        )

    async def topics(self, query: str, limit: int = 10) -> dict:
        return await self.github.request(
            "GET",
            "/search/topics",
            params={"q": query, "per_page": limit},
        )

    async def users(self, query: str, limit: int = 10) -> dict:
        return await self.github.request(
            "GET",
            "/search/users",
            params={"q": query, "per_page": limit},
        )
