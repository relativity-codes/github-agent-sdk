from github_agent_sdk.models.pull_request import PullRequest


class PullRequestAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def create(
        self,
        owner: str,
        repo: str,
        *,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> PullRequest:
        data = await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/pulls",
            json={"title": title, "body": body, "head": head, "base": base},
        )
        return PullRequest(**data)
