from __future__ import annotations

import os
from collections.abc import Awaitable, Callable
from typing import Any

from github_agent_sdk.agent import GitHubAgent
from github_agent_sdk.client import GitHub


def _normalize(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump()
    return value


def _read_runtime_config() -> dict[str, Any]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN is required to run github-agent-sdk MCP tools")

    timeout = int(os.getenv("GITHUB_SDK_TIMEOUT", "60"))
    base_url = os.getenv("GITHUB_BASE_URL", "https://api.github.com")
    user_agent = os.getenv("GITHUB_SDK_USER_AGENT", "GitHubAgentSDK-MCP/1.0")

    return {
        "token": token,
        "timeout": timeout,
        "base_url": base_url,
        "user_agent": user_agent,
    }


async def _with_agent(
    callback: Callable[[GitHubAgent], Awaitable[Any]],
) -> Any:
    config = _read_runtime_config()
    github = GitHub(
        token=config["token"],
        timeout=config["timeout"],
        base_url=config["base_url"],
        user_agent=config["user_agent"],
    )
    agent = GitHubAgent(github)
    try:
        result = await callback(agent)
        return _normalize(result)
    finally:
        await github.close()


def create_mcp_server():
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:
        raise ImportError(
            "Install MCP support with: pip install 'github-agent-sdk[mcp]'"
        ) from exc

    mcp = FastMCP("github-agent-sdk")

    @mcp.tool()
    async def repositories_get(owner: str, repo: str) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.repositories.get(owner, repo))

    @mcp.tool()
    async def repositories_create(
        name: str,
        private: bool = True,
        description: str = "",
        auto_init: bool = True,
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.repositories.create(
                name,
                private=private,
                description=description,
                auto_init=auto_init,
            )
        )

    @mcp.tool()
    async def branches_get_sha(owner: str, repo: str, branch: str) -> str:
        return await _with_agent(lambda agent: agent.branches.get_sha(owner, repo, branch))

    @mcp.tool()
    async def branches_create(
        owner: str,
        repo: str,
        branch: str,
        from_branch: str = "main",
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.branches.create(
                owner,
                repo,
                branch=branch,
                from_branch=from_branch,
            )
        )

    @mcp.tool()
    async def contents_get(
        owner: str,
        repo: str,
        path: str,
        branch: str = "main",
    ) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.contents.get(owner, repo, path, branch))

    @mcp.tool()
    async def contents_get_text(
        owner: str,
        repo: str,
        path: str,
        branch: str = "main",
    ) -> str:
        return await _with_agent(
            lambda agent: agent.contents.get_text(owner, repo, path, branch)
        )

    @mcp.tool()
    async def contents_create_or_update(
        owner: str,
        repo: str,
        path: str,
        content: str,
        message: str,
        branch: str,
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.contents.create_or_update(
                owner,
                repo,
                path=path,
                content=content,
                message=message,
                branch=branch,
            )
        )

    @mcp.tool()
    async def pulls_create(
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main",
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.pulls.create(
                owner,
                repo,
                title=title,
                body=body,
                head=head,
                base=base,
            )
        )

    @mcp.tool()
    async def issues_create(
        owner: str,
        repo: str,
        title: str,
        body: str,
        labels: list[str] | None = None,
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.issues.create(
                owner,
                repo,
                title=title,
                body=body,
                labels=labels,
            )
        )

    @mcp.tool()
    async def issues_list(
        filter: str = "assigned",
        state: str = "open",
        per_page: int = 30,
        page: int = 1,
    ) -> list[dict[str, Any]]:
        return await _with_agent(
            lambda agent: agent.issues.list(
                filter=filter,
                state=state,
                per_page=per_page,
                page=page,
            )
        )

    @mcp.tool()
    async def search_repositories(query: str, limit: int = 10) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.search.repositories(query, limit=limit))

    @mcp.tool()
    async def search_code(query: str, limit: int = 10) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.search.code(query, limit=limit))

    @mcp.tool()
    async def search_commits(query: str, limit: int = 10) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.search.commits(query, limit=limit))

    @mcp.tool()
    async def search_issues(query: str, limit: int = 10) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.search.issues(query, limit=limit))

    @mcp.tool()
    async def search_labels(
        query: str,
        repository_id: int,
        page: int | None = None,
        per_page: int = 10,
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.search.labels(
                query,
                repository_id,
                page=page,
                per_page=per_page,
            )
        )

    @mcp.tool()
    async def search_topics(query: str, limit: int = 10) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.search.topics(query, limit=limit))

    @mcp.tool()
    async def search_users(query: str, limit: int = 10) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.search.users(query, limit=limit))

    @mcp.tool()
    async def actions_trigger(
        owner: str,
        repo: str,
        workflow_id: str,
        ref: str = "main",
        inputs: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.actions.trigger(
                owner,
                repo,
                workflow_id=workflow_id,
                ref=ref,
                inputs=inputs,
            )
        )

    @mcp.tool()
    async def graphql_query(query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.graphql.query(query, variables=variables))

    @mcp.tool()
    async def organizations_get(org: str) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.organizations.get(org))

    @mcp.tool()
    async def organizations_repositories(org: str, per_page: int = 100) -> list[dict[str, Any]]:
        return await _with_agent(
            lambda agent: agent.organizations.repositories(org, per_page=per_page)
        )

    @mcp.tool()
    async def organizations_teams(org: str, per_page: int = 100) -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.organizations.teams(org, per_page=per_page))

    @mcp.tool()
    async def users_me() -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.users.me())

    @mcp.tool()
    async def users_get(username: str) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.users.get(username))

    @mcp.tool()
    async def users_emails() -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.users.emails())

    @mcp.tool()
    async def users_followers() -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.users.followers())

    @mcp.tool()
    async def users_following(per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        return await _with_agent(
            lambda agent: agent.users.following(per_page=per_page, page=page)
        )

    @mcp.tool()
    async def users_is_following(target: str) -> bool:
        return await _with_agent(lambda agent: agent.users.is_following(target))

    @mcp.tool()
    async def users_keys() -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.users.keys())

    @mcp.tool()
    async def users_organizations() -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.users.organizations())

    @mcp.tool()
    async def users_repositories(
        type: str = "owner",
        page: int = 1,
        per_page: int = 30,
        sort: str = "full_name",
    ) -> list[dict[str, Any]]:
        return await _with_agent(
            lambda agent: agent.users.repositories(
                type=type,
                page=page,
                per_page=per_page,
                sort=sort,
            )
        )

    @mcp.tool()
    async def users_user_repositories(
        username: str,
        type: str = "owner",
        page: int = 1,
        per_page: int = 30,
        sort: str = "full_name",
    ) -> list[dict[str, Any]]:
        return await _with_agent(
            lambda agent: agent.users.user_repositories(
                username,
                type=type,
                page=page,
                per_page=per_page,
                sort=sort,
            )
        )

    @mcp.tool()
    async def users_starred(page: int = 1, per_page: int = 30) -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.users.starred(page=page, per_page=per_page))

    @mcp.tool()
    async def users_has_starred(owner: str, repo: str) -> bool:
        return await _with_agent(lambda agent: agent.users.has_starred(owner, repo))

    @mcp.tool()
    async def gists_list(per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.gists.list(per_page=per_page, page=page))

    @mcp.tool()
    async def gists_get(gist_id: str) -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.gists.get(gist_id))

    @mcp.tool()
    async def gists_public(per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.gists.public(per_page=per_page, page=page))

    @mcp.tool()
    async def gists_starred(per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.gists.starred(per_page=per_page, page=page))

    @mcp.tool()
    async def notifications_list(
        all: bool = False,
        participating: bool = False,
        per_page: int = 30,
        page: int = 1,
    ) -> list[dict[str, Any]]:
        return await _with_agent(
            lambda agent: agent.notifications.list(
                all=all,
                participating=participating,
                per_page=per_page,
                page=page,
            )
        )

    @mcp.tool()
    async def meta_emojis() -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.meta.emojis())

    @mcp.tool()
    async def meta_events(per_page: int = 30, page: int = 1) -> list[dict[str, Any]]:
        return await _with_agent(lambda agent: agent.meta.events(per_page=per_page, page=page))

    @mcp.tool()
    async def meta_feeds() -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.meta.feeds())

    @mcp.tool()
    async def meta_hub() -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.meta.hub())

    @mcp.tool()
    async def meta_rate_limit() -> dict[str, Any]:
        return await _with_agent(lambda agent: agent.meta.rate_limit())

    @mcp.tool()
    async def create_fix_pull_request(
        owner: str,
        repo: str,
        file_path: str,
        content: str,
        branch_name: str,
        commit_message: str,
        pr_title: str,
        pr_body: str,
    ) -> dict[str, Any]:
        return await _with_agent(
            lambda agent: agent.create_fix_pull_request(
                owner=owner,
                repo=repo,
                file_path=file_path,
                content=content,
                branch_name=branch_name,
                commit_message=commit_message,
                pr_title=pr_title,
                pr_body=pr_body,
            )
        )

    return mcp


def main() -> None:
    mcp = create_mcp_server()
    mcp.run()


if __name__ == "__main__":
    main()
