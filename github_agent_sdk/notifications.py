from __future__ import annotations


class NotificationAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def list(
        self,
        *,
        all: bool = False,
        participating: bool = False,
        per_page: int = 30,
        page: int = 1,
    ) -> list[dict]:
        return await self.github.request(
            "GET",
            "/notifications",
            params={
                "all": str(all).lower(),
                "participating": str(participating).lower(),
                "per_page": per_page,
                "page": page,
            },
        )
