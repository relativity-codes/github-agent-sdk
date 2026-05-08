class OrganizationAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def get(self, org: str) -> dict:
        return await self.github.request("GET", f"/orgs/{org}")

    async def repositories(self, org: str, *, per_page: int = 100) -> list[dict]:
        return await self.github.request(
            "GET",
            f"/orgs/{org}/repos",
            params={"per_page": per_page},
        )

    async def teams(self, org: str, *, per_page: int = 100) -> list[dict]:
        return await self.github.request(
            "GET",
            f"/orgs/{org}/teams",
            params={"per_page": per_page},
        )
