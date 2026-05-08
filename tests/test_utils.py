from github_agent_sdk.utils import decode_base64, encode_base64


def test_encode_decode_base64_round_trip() -> None:
    content = "hello sdk"
    encoded = encode_base64(content)
    decoded = decode_base64(encoded)
    assert decoded == content
