from pydantic import BaseModel


class PullRequest(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
