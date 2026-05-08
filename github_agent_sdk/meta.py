class MetaAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def emojis(self) -> dict:
        return await self.github.request("GET", "/emojis")

    async def events(self, *, per_page: int = 30, page: int = 1) -> list[dict]:
        return await self.github.request(
            "GET",
            "/events",
            params={"per_page": per_page, "page": page},
        )

    async def feeds(self) -> dict:
        return await self.github.request("GET", "/feeds")

    async def hub(self) -> dict:
        return await self.github.request("GET", "/hub")

    async def rate_limit(self) -> dict:
        return await self.github.request("GET", "/rate_limit")
