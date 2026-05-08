class GitHubError(Exception):
    """Base SDK exception."""


class GitHubAPIError(GitHubError):
    """Raised when GitHub API returns a non-auth, non-rate-limit error."""


class GitHubRateLimitError(GitHubError):
    """Raised when GitHub API rate limit is exceeded."""


class GitHubAuthenticationError(GitHubError):
    """Raised when the provided token is invalid."""
