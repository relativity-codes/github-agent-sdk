from pydantic import BaseModel


class Issue(BaseModel):
    id: int
    number: int
    title: str
    state: str
    html_url: str
