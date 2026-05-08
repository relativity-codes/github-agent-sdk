class GraphQLAPI:
    def __init__(self, github) -> None:
        self.github = github

    async def query(self, query: str, variables: dict | None = None) -> dict:
        response = await self.github.request(
            "POST",
            "/graphql",
            json={"query": query, "variables": variables or {}},
        )

        if response.get("errors"):
            raise Exception(response["errors"])

        return response["data"]
