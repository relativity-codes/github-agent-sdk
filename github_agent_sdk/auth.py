from dataclasses import dataclass


@dataclass(slots=True)
class TokenAuth:
    token: str

    def headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}
