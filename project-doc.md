# github-agent-sdk

Production-grade modular GitHub AI SDK for Python.

Designed for:

* AI agents
* autonomous GitHub workflows
* PR automation
* repository management
* code intelligence
* CI/CD orchestration
* OpenAI/LangGraph/CrewAI integration

No MCP server required.
No extra runtime.
Direct GitHub API communication.

---

# Project Structure

```txt
github-agent-sdk/
├── pyproject.toml
├── README.md
├── .env.example
├── github_agent_sdk/
│   ├── __init__.py
│   ├── client.py
│   ├── auth.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── pagination.py
│   ├── rate_limit.py
│   ├── utils.py
│   ├── types.py
│   ├── agent.py
│   ├── graphql.py
│   ├── repositories.py
│   ├── branches.py
│   ├── contents.py
│   ├── pulls.py
│   ├── issues.py
│   ├── actions.py
│   ├── search.py
│   ├── organizations.py
│   ├── users.py
│   └── models/
│       ├── repository.py
│       ├── pull_request.py
│       ├── issue.py
│       └── workflow.py
└── tests/
    ├── test_repositories.py
    ├── test_pulls.py
    └── test_issues.py
```

---

# pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "github-agent-sdk"
version = "0.1.0"
description = "Production-grade GitHub AI SDK"
authors = [
    { name = "Everest" }
]
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "httpx>=0.28.0",
    "pydantic>=2.8.0",
    "tenacity>=9.0.0",
    "python-dotenv>=1.0.1",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["github_agent_sdk*"]
```

---

# github_agent_sdk/**init**.py

```python
from github_agent_sdk.client import GitHub

__all__ = ["GitHub"]
```

---

# github_agent_sdk/constants.py

```python
BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"
DEFAULT_TIMEOUT = 60
DEFAULT_USER_AGENT = "GitHubAgentSDK/1.0"
```

---

# github_agent_sdk/exceptions.py

```python
class GitHubError(Exception):
    pass


class GitHubAPIError(GitHubError):
    pass


class GitHubRateLimitError(GitHubError):
    pass


class GitHubAuthenticationError(GitHubError):
    pass
```

---

# github_agent_sdk/types.py

```python
from typing import Any

JSON = dict[str, Any]
```

---

# github_agent_sdk/auth.py

```python
from dataclasses import dataclass


@dataclass
class TokenAuth:
    token: str

    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }
```

---

# github_agent_sdk/utils.py

```python
import base64


def encode_base64(content: str) -> str:
    return base64.b64encode(content.encode()).decode()



def decode_base64(content: str) -> str:
    return base64.b64decode(content).decode()
```

---

# github_agent_sdk/rate_limit.py

```python
from github_agent_sdk.exceptions import GitHubRateLimitError


async def validate_rate_limit(response):
    if response.status_code == 403:
        remaining = response.headers.get("X-RateLimit-Remaining")

        if remaining == "0":
            raise GitHubRateLimitError("GitHub rate limit exceeded")
```

---

# github_agent_sdk/pagination.py

```python
async def paginate(fetcher, *, page_size=100):
    page = 1

    while True:
        data = await fetcher(page, page_size)

        items = data if isinstance(data, list) else data.get("items", [])

        if not items:
            break

        for item in items:
            yield item

        if len(items) < page_size:
            break

        page += 1
```

---

# github_agent_sdk/models/repository.py

```python
from pydantic import BaseModel


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    default_branch: str | None = None
```

---

# github_agent_sdk/models/pull_request.py

```python
from pydantic import BaseModel


class PullRequest(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
```

---

# github_agent_sdk/models/issue.py

```python
from pydantic import BaseModel


class Issue(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
```

---

# github_agent_sdk/client.py

```python
from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from github_agent_sdk.auth import TokenAuth
from github_agent_sdk.constants import (
    API_VERSION,
    BASE_URL,
    DEFAULT_TIMEOUT,
    DEFAULT_USER_AGENT,
)
from github_agent_sdk.exceptions import (
    GitHubAPIError,
    GitHubAuthenticationError,
)
from github_agent_sdk.rate_limit import validate_rate_limit


class GitHub:
    def __init__(
        self,
        token: str,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        base_url: str = BASE_URL,
        user_agent: str = DEFAULT_USER_AGENT,
    ):
        self.base_url = base_url

        auth = TokenAuth(token)

        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                **auth.headers(),
                "Accept": "application/vnd.github+json",
                "User-Agent": user_agent,
                "X-GitHub-Api-Version": API_VERSION,
            },
        )

    async def close(self):
        await self.client.aclose()

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=20),
    )
    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ):
        response = await self.client.request(
            method,
            f"{self.base_url}{endpoint}",
            params=params,
            json=json,
        )

        await validate_rate_limit(response)

        if response.status_code == 401:
            raise GitHubAuthenticationError("Invalid GitHub token")

        if response.status_code >= 400:
            raise GitHubAPIError(response.text)

        if not response.content:
            return {}

        return response.json()
```

---

# github_agent_sdk/repositories.py

```python
from github_agent_sdk.models.repository import Repository


class RepositoryAPI:
    def __init__(self, github):
        self.github = github

    async def get(self, owner: str, repo: str):
        data = await self.github.request(
            "GET",
            f"/repos/{owner}/{repo}",
        )

        return Repository(**data)

    async def create(
        self,
        name: str,
        *,
        private: bool = True,
        description: str = "",
        auto_init: bool = True,
    ):
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
```

---

# github_agent_sdk/branches.py

```python
class BranchAPI:
    def __init__(self, github):
        self.github = github

    async def get_sha(
        self,
        owner: str,
        repo: str,
        branch: str,
    ):
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
    ):
        sha = await self.get_sha(owner, repo, from_branch)

        return await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/git/refs",
            json={
                "ref": f"refs/heads/{branch}",
                "sha": sha,
            },
        )
```

---

# github_agent_sdk/contents.py

```python
from github_agent_sdk.utils import decode_base64, encode_base64


class ContentAPI:
    def __init__(self, github):
        self.github = github

    async def get(
        self,
        owner: str,
        repo: str,
        path: str,
        branch: str = "main",
    ):
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
    ):
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
    ):
        encoded = encode_base64(content)

        sha = None

        try:
            existing = await self.get(owner, repo, path, branch)
            sha = existing["sha"]
        except Exception:
            pass

        payload = {
            "message": message,
            "content": encoded,
            "branch": branch,
        }

        if sha:
            payload["sha"] = sha

        return await self.github.request(
            "PUT",
            f"/repos/{owner}/{repo}/contents/{path}",
            json=payload,
        )
```

---

# github_agent_sdk/pulls.py

```python
from github_agent_sdk.models.pull_request import PullRequest


class PullRequestAPI:
    def __init__(self, github):
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
    ):
        data = await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/pulls",
            json={
                "title": title,
                "body": body,
                "head": head,
                "base": base,
            },
        )

        return PullRequest(**data)
```

---

# github_agent_sdk/issues.py

```python
from github_agent_sdk.models.issue import Issue


class IssueAPI:
    def __init__(self, github):
        self.github = github

    async def create(
        self,
        owner: str,
        repo: str,
        *,
        title: str,
        body: str,
        labels: list[str] | None = None,
    ):
        data = await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/issues",
            json={
                "title": title,
                "body": body,
                "labels": labels or [],
            },
        )

        return Issue(**data)
```

---

# github_agent_sdk/search.py

```python
class SearchAPI:
    def __init__(self, github):
        self.github = github

    async def repositories(self, query: str, limit: int = 10):
        return await self.github.request(
            "GET",
            "/search/repositories",
            params={
                "q": query,
                "per_page": limit,
            },
        )

    async def code(self, query: str, limit: int = 10):
        return await self.github.request(
            "GET",
            "/search/code",
            params={
                "q": query,
                "per_page": limit,
            },
        )
```

---

# github_agent_sdk/graphql.py

```python
class GraphQLAPI:
    def __init__(self, github):
        self.github = github

    async def query(
        self,
        query: str,
        variables: dict | None = None,
    ):
        response = await self.github.request(
            "POST",
            "/graphql",
            json={
                "query": query,
                "variables": variables or {},
            },
        )

        if response.get("errors"):
            raise Exception(response["errors"])

        return response["data"]
```

---

# github_agent_sdk/actions.py

```python
class ActionAPI:
    def __init__(self, github):
        self.github = github

    async def trigger(
        self,
        owner: str,
        repo: str,
        *,
        workflow_id: str,
        ref: str = "main",
        inputs: dict | None = None,
    ):
        return await self.github.request(
            "POST",
            f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches",
            json={
                "ref": ref,
                "inputs": inputs or {},
            },
        )
```

---

# github_agent_sdk/agent.py

```python
from github_agent_sdk.actions import ActionAPI
from github_agent_sdk.branches import BranchAPI
from github_agent_sdk.contents import ContentAPI
from github_agent_sdk.graphql import GraphQLAPI
from github_agent_sdk.issues import IssueAPI
from github_agent_sdk.pulls import PullRequestAPI
from github_agent_sdk.repositories import RepositoryAPI
from github_agent_sdk.search import SearchAPI


class GitHubAgent:
    def __init__(self, github):
        self.github = github

        self.repositories = RepositoryAPI(github)
        self.branches = BranchAPI(github)
        self.contents = ContentAPI(github)
        self.pulls = PullRequestAPI(github)
        self.issues = IssueAPI(github)
        self.search = SearchAPI(github)
        self.actions = ActionAPI(github)
        self.graphql = GraphQLAPI(github)

    async def create_fix_pull_request(
        self,
        *,
        owner: str,
        repo: str,
        file_path: str,
        content: str,
        branch_name: str,
        commit_message: str,
        pr_title: str,
        pr_body: str,
    ):
        repository = await self.repositories.get(owner, repo)

        base_branch = repository.default_branch or "main"

        await self.branches.create(
            owner,
            repo,
            branch=branch_name,
            from_branch=base_branch,
        )

        await self.contents.create_or_update(
            owner,
            repo,
            path=file_path,
            content=content,
            message=commit_message,
            branch=branch_name,
        )

        return await self.pulls.create(
            owner,
            repo,
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base=base_branch,
        )
```

---

# Example Usage

```python
import asyncio
import os

from github_agent_sdk.agent import GitHubAgent
from github_agent_sdk.client import GitHub


async def main():
    github = GitHub(
        token=os.getenv("GITHUB_TOKEN")
    )

    agent = GitHubAgent(github)

    repos = await agent.search.repositories(
        "ai agents python"
    )

    print(repos)

    await github.close()


asyncio.run(main())
```

---

# Build Package

```bash
python -m build
```

---

# Publish To PyPI

```bash
pip install twine

python -m twine upload dist/*
```

---

# Install

```bash
pip install github-agent-sdk
```

---

# Recommended Production Upgrades

Add next:

* GitHub App auth
* installation tokens
* websocket events
* webhook server
* distributed rate limiting
* ETag caching
* diff parsers
* AST-aware editors
* semantic code search
* repo graph indexing
* OpenAI tools adapter
* LangGraph executor
* streaming logs
* audit trail
* org-level RBAC
* branch protection handling
* review comments
* checks API
* releases API
* discussions API
* security alerts
* Dependabot APIs
* batch git trees
* low-level git object APIs
* multi-file atomic commits
* repo cloning support
* local git fallback
