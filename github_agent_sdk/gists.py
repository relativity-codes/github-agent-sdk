from __future__ import annotations


class GistAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def list(self, *, per_page: int = 30, page: int = 1) -> list[dict]:
        return await self.github.request(
            "GET",
            "/gists",
            params={"per_page": per_page, "page": page},
        )

    async def get(self, gist_id: str) -> dict:
        return await self.github.request("GET", f"/gists/{gist_id}")

    async def public(self, *, per_page: int = 30, page: int = 1) -> list[dict]:
        return await self.github.request(
            "GET",
            "/gists/public",
            params={"per_page": per_page, "page": page},
        )

    async def starred(self, *, per_page: int = 30, page: int = 1) -> list[dict]:
        return await self.github.request(
            "GET",
            "/gists/starred",
            params={"per_page": per_page, "page": page},
        )
