import base64


def encode_base64(content: str) -> str:
    return base64.b64encode(content.encode("utf-8")).decode("utf-8")


def decode_base64(content: str) -> str:
    return base64.b64decode(content).decode("utf-8")
