from pydantic import BaseModel


class Workflow(BaseModel):
    id: int
    name: str
    path: str
    state: str | None = None
