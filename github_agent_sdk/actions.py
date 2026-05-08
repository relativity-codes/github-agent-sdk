class ActionAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def trigger(
        self,
        owner: str,
        repo: str,
        *,
        workflow_id: str,
        ref: str = "main",
        inputs: dict | None = None,
    ) -> dict:
        return await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            json={"ref": ref, "inputs": inputs or {}},
        )
