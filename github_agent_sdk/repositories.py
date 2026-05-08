from github_agent_sdk.models.repository import Repository


class RepositoryAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def get(self, owner: str, repo: str) -> Repository:
        data = await self.github.request("GET", f"/repos/{owner}/{repo}")
        return Repository(**data)

    async def create(
        self,
        name: str,
        *,
        private: bool = True,
        description: str = "",
        auto_init: bool = True,
    ) -> dict:
        return await self.github.request(
            "POST",
            "/user/repos",
            json={
                "name": name,
                "private": private,
                "description": description,
                "auto_init": auto_init,
            },
        )
