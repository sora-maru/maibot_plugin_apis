from __future__ import annotations

from urllib.parse import urlsplit, urlunsplit

from ..entry import APIEntryManager, SiteEntryManager
from ..entry.api_entry import APIEntry
from ..entry.site_entry import SiteEntry
from ..model import SitePayload


class SiteSyncService:
    """Handle site matching and api-site synchronization strategy."""

    def __init__(self, api_mgr: APIEntryManager, site_mgr: SiteEntryManager) -> None:
        self.api_mgr = api_mgr
        self.site_mgr = site_mgr

    def resolve_api_site_name(self, url: str) -> str:
        full_url = str(url or "").strip()
        if not full_url:
            return ""
        site = self.site_mgr.match_entry(full_url, only_enabled=False)
        return str(site.name) if site else ""

    def sync_all_api_sites(self) -> bool:
        return self.api_mgr.sync_site_fields(self.resolve_api_site_name)

    @staticmethod
    def _base_url(value: str):
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc or parsed.query or parsed.fragment or parsed.username or parsed.password:
            raise ValueError("站点地址须为 HTTP(S) 基础地址，不包含查询参数、片段或账号密码")
        return parsed

    @classmethod
    def _move_url(cls, full_url: str, old_base: str, new_base: str) -> str:
        old, new, full = cls._base_url(old_base), cls._base_url(new_base), urlsplit(full_url)
        suffix = full.path[len(old.path.rstrip('/')):]
        path = new.path.rstrip('/') + ('/' + suffix.lstrip('/') if suffix else '')
        return urlunsplit((new.scheme, new.netloc, path, full.query, full.fragment))

    def _install_entries(self):
        # The database owns the two mutable pool lists; rebuild entries only after commit.
        self.site_mgr.entries[:] = [SiteEntry(row) for row in self.site_mgr.pool]
        self.api_mgr.entries[:] = [APIEntry(row) for row in self.api_mgr.pool]

    def update_sites(self, updates: list[dict]) -> tuple[list[dict], int]:
        original = {entry.name: entry for entry in self.site_mgr.entries}
        staged = dict(original)
        changed = {}
        switches = {}
        for update in updates:
            name, payload = update['name'], update['payload']
            old = original.get(name)
            if old is None:
                raise LookupError(f"site not found: {name}")
            if name in changed:
                raise ValueError("同一批次不能重复修改同一站点")
            row = SitePayload.from_raw({**old.to_dict(), **payload}).to_dict()
            self._base_url(row['url'])
            changed[name] = row
            if 'enabled' in payload:
                switches[name] = row['enabled']
            staged[name] = SiteEntry(row)
        if len({entry.name for entry in staged.values()}) != len(staged):
            raise ValueError("站点名称重复")
        candidates = sorted(staged.values(), key=lambda item: len(item.url.rstrip('/')), reverse=True)
        api_rows = []
        moved = 0
        for api in self.api_mgr.entries:
            row = api.to_dict()
            owner = self.site_mgr.match_entry(api.url, only_enabled=False)
            replacement = changed.get(owner.name) if owner else None
            # Explicit site switches fan out even if the site already has the
            # requested state (e.g. enable APIs after adding a key).
            if owner and owner.name in switches:
                row['enabled'] = switches[owner.name]
            if replacement and owner.url != replacement['url']:
                row['url'] = self._move_url(api.url, owner.url, replacement['url'])
                moved += 1
            row['site'] = next((site.name for site in candidates if site.is_vested(row['url'])), '')
            if row != api.to_dict():
                api_rows.append(row)
        try:
            self.api_mgr.db.batch_update_pools(
                site_upserts=list(changed.values()),
                site_delete_names=[old for old, row in changed.items() if old != row['name']],
                api_upserts=api_rows,
            )
        finally:
            self._install_entries()
        return list(changed.values()), moved

    def delete_sites(self, names: list[str]) -> dict:
        names = list(dict.fromkeys(names))
        existing = {entry.name for entry in self.site_mgr.entries}
        selected = set(names) & existing
        api_names = [api.name for api in self.api_mgr.entries
            if (owner := self.site_mgr.match_entry(api.url, only_enabled=False)) is not None and owner.name in selected]
        try:
            self.api_mgr.db.batch_update_pools(site_delete_names=list(selected), api_delete_names=api_names)
        finally:
            self._install_entries()
        return {'requested': names, 'deleted': [name for name in names if name in selected],
                'failed': [name for name in names if name not in selected], 'deleted_apis': api_names}
