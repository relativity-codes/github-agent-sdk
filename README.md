# github-agent-sdk

Production-grade modular GitHub AI SDK for Python.

This SDK gives you:

- async GitHub REST + GraphQL access
- high-level API modules (`repos`, `issues`, `pulls`, `search`, etc.)
- an orchestration layer for common agent workflows
- typed models for key GitHub resources
- testable, composable interfaces for automation scripts and AI agents

## Install

```bash
pip install github-agent-sdk
```

## Requirements

- Python `>=3.11`
- GitHub token with required scopes for the APIs you call

## Authentication

Set your token:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## Quick Start

```python
import asyncio
import os

from github_agent_sdk.agent import GitHubAgent
from github_agent_sdk.client import GitHub


async def main():
    github = GitHub(token=os.environ["GITHUB_TOKEN"])
    agent = GitHubAgent(github)

    repos = await agent.search.repositories("ai agents python", limit=5)
    print(repos["total_count"])

    await github.close()


asyncio.run(main())
```

## Package Exports

Top-level exports from `github_agent_sdk`:

- `GitHub`
- `GitHubAgent`
- `GistAPI`
- `NotificationAPI`
- `MetaAPI`

## Core Client

### `GitHub`

Main async HTTP client wrapper.

```python
from github_agent_sdk.client import GitHub

github = GitHub(token="...")
data = await github.request("GET", "/user")
await github.close()
```

Constructor options:

- `token`: GitHub token (required)
- `timeout`: request timeout in seconds (default `60`)
- `base_url`: GitHub API base URL (default `https://api.github.com`)
- `user_agent`: custom User-Agent header

### Error Types

Handle SDK exceptions from `github_agent_sdk.exceptions`:

- `GitHubAuthenticationError` (invalid/expired token)
- `GitHubRateLimitError` (rate limit exhausted)
- `GitHubAPIError` (other API errors)
- `GitHubError` (base class)

## High-Level APIs via `GitHubAgent`

Instantiate once and use module-style APIs:

```python
agent = GitHubAgent(github)
```

Available modules:

- `agent.repositories`
- `agent.branches`
- `agent.contents`
- `agent.pulls`
- `agent.issues`
- `agent.search`
- `agent.actions`
- `agent.graphql`
- `agent.organizations`
- `agent.users`
- `agent.gists`
- `agent.notifications`
- `agent.meta`

## API Reference

### Repositories (`agent.repositories`)

- `get(owner, repo)`
- `create(name, *, private=True, description="", auto_init=True)`

```python
repo = await agent.repositories.get("octocat", "Hello-World")
new_repo = await agent.repositories.create("my-repo", private=True)
```

### Branches (`agent.branches`)

- `get_sha(owner, repo, branch)`
- `create(owner, repo, *, branch, from_branch="main")`

### Contents (`agent.contents`)

- `get(owner, repo, path, branch="main")`
- `get_text(owner, repo, path, branch="main")`
- `create_or_update(owner, repo, *, path, content, message, branch)`

```python
text = await agent.contents.get_text("acme", "repo", "README.md")
await agent.contents.create_or_update(
    "acme",
    "repo",
    path="README.md",
    content=text + "\nUpdated\n",
    message="docs: update readme",
    branch="main",
)
```

### Pull Requests (`agent.pulls`)

- `create(owner, repo, *, title, body, head, base="main")`

### Issues (`agent.issues`)

- `create(owner, repo, *, title, body, labels=None)`
- `list(*, filter="assigned", state="open", per_page=30, page=1)` (global `/issues`)

### Search (`agent.search`)

- `repositories(query, limit=10)`
- `code(query, limit=10)`
- `commits(query, limit=10)`
- `issues(query, limit=10)`
- `labels(query, repository_id, *, page=None, per_page=10)`
- `topics(query, limit=10)`
- `users(query, limit=10)`

### Actions (`agent.actions`)

- `trigger(owner, repo, *, workflow_id, ref="main", inputs=None)`

### GraphQL (`agent.graphql`)

- `query(query, variables=None)`

### Organizations (`agent.organizations`)

- `get(org)`
- `repositories(org, *, per_page=100)`
- `teams(org, *, per_page=100)`

### Users (`agent.users`)

- `me()`
- `get(username)`
- `emails()`
- `followers()`
- `following(*, per_page=30, page=1)`
- `is_following(target)` -> `bool`
- `keys()`
- `organizations()`
- `repositories(*, type="owner", page=1, per_page=30, sort="full_name")` (current user repos)
- `user_repositories(username, *, type="owner", page=1, per_page=30, sort="full_name")`
- `starred(*, page=1, per_page=30)`
- `has_starred(owner, repo)` -> `bool`

### Gists (`agent.gists`)

- `list(*, per_page=30, page=1)`
- `get(gist_id)`
- `public(*, per_page=30, page=1)`
- `starred(*, per_page=30, page=1)`

### Notifications (`agent.notifications`)

- `list(*, all=False, participating=False, per_page=30, page=1)`

### Meta (`agent.meta`)

- `emojis()`
- `events(*, per_page=30, page=1)`
- `feeds()`
- `hub()`
- `rate_limit()`

## Built-in Workflow Helper

### `GitHubAgent.create_fix_pull_request(...)`

End-to-end helper that:

1. fetches repo default branch
2. creates a new branch
3. writes/updates file content
4. opens a PR back to the default branch

```python
pr = await agent.create_fix_pull_request(
    owner="acme",
    repo="service",
    file_path="README.md",
    content="new docs",
    branch_name="fix/docs",
    commit_message="docs: update readme",
    pr_title="Fix docs",
    pr_body="Updates README wording.",
)
```

## Models

Typed models available in `github_agent_sdk.models`:

- `Repository`
- `PullRequest`
- `Issue`
- `Workflow`

## MCP Server (All Tools Ready)

This package ships with an MCP server that exposes the SDK methods as ready-to-use tools for agentic projects.

### Install MCP Support

```bash
pip install "github-agent-sdk[mcp]"
```

### Required Environment Variables

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

Optional:

- `GITHUB_SDK_TIMEOUT` (default `60`)
- `GITHUB_BASE_URL` (default `https://api.github.com`)
- `GITHUB_SDK_USER_AGENT` (default `GitHubAgentSDK-MCP/1.0`)

### Run MCP Server

```bash
github-agent-sdk-mcp
```

### Use in MCP Clients (Example)

Use `github-agent-sdk-mcp` as a stdio MCP server command in your client config.

```json
{
  "mcpServers": {
    "githubAgentSdk": {
      "command": "github-agent-sdk-mcp",
      "env": {
        "GITHUB_TOKEN": "ghp_your_token_here"
      }
    }
  }
}
```

### MCP Tool Naming

Tools are grouped by SDK module with predictable names:

- `repositories_*`, `branches_*`, `contents_*`, `pulls_*`, `issues_*`
- `search_*`, `actions_*`, `graphql_query`
- `organizations_*`, `users_*`
- `gists_*`, `notifications_*`, `meta_*`
- `create_fix_pull_request`

Examples:

- `repositories_get`
- `contents_create_or_update`
- `search_repositories`
- `users_has_starred`
- `meta_rate_limit`

## Development

Install dev dependencies and run tests:

```bash
python3 -m pip install -e ".[dev]"
python3 -m pytest -q
```
# github-agent-sdk
