from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

from ..model import SitePayload


class SiteEntry:
    """Site entry."""

    def __init__(self, data: dict[str, Any]):
        normalized = SitePayload.from_raw(
            data if isinstance(data, dict) else {},
            require_name=True,
            require_url=True,
        )
        self.name = normalized.name
        self.url = normalized.url
        self.enabled = normalized.enabled
        self.headers = dict(normalized.headers)
        self.keys = dict(normalized.keys)
        self.timeout = normalized.timeout

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "enabled": self.enabled,
            "headers": dict(self.headers),
            "keys": dict(self.keys),
            "timeout": self.timeout,
        }

    def is_vested(self, full_url: str):
        try:
            base, target = urlsplit(self.url), urlsplit(full_url)
            if (base.scheme.lower(), base.netloc.lower()) != (target.scheme.lower(), target.netloc.lower()):
                return False
            prefix = base.path.rstrip("/")
            return target.path == prefix or target.path.startswith(prefix + "/")
        except ValueError:
            return False

    def get_headers(self) -> dict[str, str]:
        return self.headers.copy()

    def get_keys(self) -> dict[str, str]:
        return self.keys.copy()
