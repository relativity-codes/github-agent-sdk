from pydantic import BaseModel


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    private: bool
    default_branch: str | None = None
