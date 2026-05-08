from github_agent_sdk.utils import decode_base64, encode_base64


class ContentAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def get(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str = "main",
    ) -> dict:
        return await self.github.request(
            "GET",
            f"/repos/{owner}/{repo}/contents/{path}",
            params={"ref": branch},
        )

    async def get_text(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str = "main",
    ) -> str:
        data = await self.get(owner, repo, path, branch)
        return decode_base64(data["content"])

    async def create_or_update(
        self,
        owner: str,
        repo: str,
        *,
        path: str,
        content: str,
        message: str,
        branch: str,
    ) -> dict:
        encoded = encode_base64(content)
        sha = None
        try:
            existing = await self.get(owner, repo, path, branch)
            sha = existing["sha"]
        except Exception:
            sha = None

        payload = {"message": message, "content": encoded, "branch": branch}
        if sha:
            payload["sha"] = sha

        return await self.github.request(
            "PUT",
            f"/repos/{owner}/{repo}/contents/{path}",
            json=payload,
        )
