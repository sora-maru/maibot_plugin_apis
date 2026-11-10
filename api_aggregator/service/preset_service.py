from __future__ import annotations

import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urlsplit

from ..entry.site_entry import SiteEntry
from ..model import ApiPayload


class PresetService:
    """Explicit, backed-up replacement of the two bundled pools."""

    def __init__(self, core):
        self.core = core

    def load(self):
        cfg = self.core.cfg
        api_bytes = cfg.api_pool_file.read_bytes()
        site_bytes = cfg.site_pool_file.read_bytes()
        raw_sites, raw_apis = json.loads(site_bytes), json.loads(api_bytes)
        if not isinstance(raw_sites, list) or not isinstance(raw_apis, list) or not raw_sites or not raw_apis:
            raise ValueError('内置默认数据为空或格式错误，未修改当前数据')
        sites = [SiteEntry(row) for row in raw_sites]
        ordered = sorted(sites, key=lambda site: len(site.url.rstrip('/')), reverse=True)
        resolver = lambda url: next((site.name for site in ordered if site.is_vested(url)), '')
        apis = [ApiPayload.from_raw(row, resolve_site_name=resolver).to_dict() for row in raw_apis]
        if len({site.name for site in sites}) != len(sites) or len({api['name'] for api in apis}) != len(apis):
            raise ValueError('内置默认数据存在同名项目，未修改当前数据')
        fingerprint = hashlib.sha256(site_bytes + b'\x00' + api_bytes).hexdigest()
        return [site.to_dict() for site in sites], apis, fingerprint

    def info(self):
        sites, apis, fingerprint = self.load()
        metadata_file = self.core.cfg.presets_dir / 'default_data_manifest.json'
        metadata = json.loads(metadata_file.read_text(encoding='utf-8')) if metadata_file.exists() else {}
        return {'fingerprint': fingerprint, 'sites': len(sites), 'apis': len(apis),
                'disabled_apis': sum(not row['enabled'] for row in apis),
                'current_sites': len(self.core.site_mgr.entries), 'current_apis': len(self.core.api_mgr.entries),
                'collected_at': metadata.get('collected_at', ''), 'backup_dir': str(self.core.cfg.pool_files_dir)}

    def migrate_short_keywords(self):
        """Upgrade only unchanged legacy default rules; leave user rules alone."""
        path = self.core.cfg.presets_dir / 'short_keywords.json'
        if not path.exists():
            return 0
        mapping = json.loads(path.read_text(encoding='utf-8'))
        defaults = {row['name']: row for row in json.loads(self.core.cfg.api_pool_file.read_text(encoding='utf-8'))}
        changed = []
        for entry in self.core.api_mgr.entries:
            if entry.name not in mapping or entry.name not in defaults or entry.url != defaults[entry.name]['url']:
                continue
            if entry.keywords != ['^' + re.escape(entry.name) + '$']:
                continue
            # Do not introduce a collision with an existing custom rule.
            token = mapping[entry.name]
            if any(other.name != entry.name and other._match_keywords(token) for other in self.core.api_mgr.entries):
                continue
            row = entry.to_dict()
            row['keywords'] = ['(?i)^' + re.escape(token) + '$']
            changed.append(row)
        if not changed:
            return 0
        stamp = str(time.time_ns())
        backup = self.core.cfg.pool_files_dir / f'api_pool_before_short_keywords_{stamp}.json'
        with backup.open('x', encoding='utf-8') as stream:
            json.dump([entry.to_dict() for entry in self.core.api_mgr.entries], stream, ensure_ascii=False, indent=2)
        try:
            self.core.db.batch_update_api_pool(upserts=changed)
        finally:
            self.core.site_sync_service._install_entries()
        return len(changed)

    def replace(self, fingerprint: str):
        sites, apis, actual = self.load()
        if fingerprint != actual:
            raise ValueError('内置数据版本已变化，请关闭窗口后重新确认')
        db = self.core.db
        old_sites = [dict(row) for row in db.site_pool]
        old_apis = [dict(row) for row in db.api_pool]
        retained = 0
        for site in sites:
            exact = [row for row in old_sites if row.get('url', '').rstrip('/') == site['url'].rstrip('/')]
            by_host = [row for row in old_sites if urlsplit(row.get('url', '')).hostname == urlsplit(site['url']).hostname]
            previous = exact[0] if len(exact) == 1 else by_host[0] if len(by_host) == 1 else None
            if previous:
                site['keys'] = {**site.get('keys', {}), **previous.get('keys', {})}
                site['headers'] = {**site.get('headers', {}), **previous.get('headers', {})}
                retained += 1
        stamp = time.strftime('%Y%m%d_%H%M%S', time.gmtime()) + '_' + str(time.time_ns())[-9:]
        directory = self.core.cfg.pool_files_dir
        api_backup, site_backup = directory / f'api_pool_backup_{stamp}.json', directory / f'site_pool_backup_{stamp}.json'
        # Both backups must be written before touching either database table.
        for path, rows in ((api_backup, old_apis), (site_backup, old_sites)):
            with path.open('x', encoding='utf-8') as stream:
                json.dump(rows, stream, ensure_ascii=False, indent=2)
        try:
            db.batch_update_pools(site_upserts=sites, api_upserts=apis,
                site_delete_names=[row['name'] for row in old_sites], api_delete_names=[row['name'] for row in old_apis])
        finally:
            self.core.site_sync_service._install_entries()
        return {'sites': len(sites), 'apis': len(apis), 'retained_site_credentials': retained,
                'backup_api_file': api_backup.name, 'backup_site_file': site_backup.name, 'backup_dir': str(directory)}
