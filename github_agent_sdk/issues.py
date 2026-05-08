from __future__ import annotations

from github_agent_sdk.models.issue import Issue


class IssueAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def create(
        self,
        owner: str,
        repo: str,
        *,
        title: str,
        body: str,
        labels: list[str] | None = None,
    ) -> Issue:
        data = await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/issues",
            json={"title": title, "body": body, "labels": labels or []},
        )
        return Issue(**data)

    async def list(
        self,
        *,
        filter: str = "assigned",
        state: str = "open",
        per_page: int = 30,
        page: int = 1,
    ) -> list[dict]:
        return await self.github.request(
            "GET",
            "/issues",
            params={
                "filter": filter,
                "state": state,
                "per_page": per_page,
                "page": page,
            },
        )
