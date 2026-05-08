class BranchAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def get_sha(self, owner: str, repo: str, branch: str) -> str:
        data = await self.github.request(
            "GET",
            f"/repos/{owner}/{repo}/git/ref/heads/{branch}",
        )
        return data["object"]["sha"]

    async def create(
        self,
        owner: str,
        repo: str,
        *,
        branch: str,
        from_branch: str = "main",
    ) -> dict:
        sha = await self.get_sha(owner, repo, from_branch)
        return await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/git/refs",
            json={"ref": f"refs/heads/{branch}", "sha": sha},
        )
