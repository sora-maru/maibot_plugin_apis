import re

_ESCAPED_BREAK = re.compile(r"\\r\\n|\\[rn]")


def normalize_response_text(value: str) -> str:
    """Normalize real and escaped line breaks without decoding Chinese or URLs."""
    value = _ESCAPED_BREAK.sub("\n", value)
    return value.replace("\r\n", "\n").replace("\r", "\n")
