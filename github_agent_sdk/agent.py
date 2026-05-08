from github_agent_sdk.actions import ActionAPI
from github_agent_sdk.branches import BranchAPI
from github_agent_sdk.contents import ContentAPI
from github_agent_sdk.gists import GistAPI
from github_agent_sdk.graphql import GraphQLAPI
from github_agent_sdk.issues import IssueAPI
from github_agent_sdk.meta import MetaAPI
from github_agent_sdk.notifications import NotificationAPI
from github_agent_sdk.organizations import OrganizationAPI
from github_agent_sdk.pulls import PullRequestAPI
from github_agent_sdk.repositories import RepositoryAPI
from github_agent_sdk.search import SearchAPI
from github_agent_sdk.users import UserAPI


class GitHubAgent:
    def __init__(self, github) -> None:
        self.github = github
        self.repositories = RepositoryAPI(github)
        self.branches = BranchAPI(github)
        self.contents = ContentAPI(github)
        self.pulls = PullRequestAPI(github)
        self.issues = IssueAPI(github)
        self.search = SearchAPI(github)
        self.actions = ActionAPI(github)
        self.graphql = GraphQLAPI(github)
        self.organizations = OrganizationAPI(github)
        self.users = UserAPI(github)
        self.gists = GistAPI(github)
        self.notifications = NotificationAPI(github)
        self.meta = MetaAPI(github)

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
