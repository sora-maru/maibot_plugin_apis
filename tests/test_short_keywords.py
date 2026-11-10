import json
from pathlib import Path
import re

import pytest

from maibot_plugin_apis.api_aggregator.entry.api_entry import APIEntry
from maibot_plugin_apis.api_aggregator.service.preset_service import PresetService
from test_port import plugin


def test_all_default_short_rules_are_unique_and_match_one_entry():
    root = Path(__file__).resolve().parents[1]
    mapping = json.loads((root / 'presets/short_keywords.json').read_text(encoding='utf-8'))
    entries = [APIEntry(row) for row in json.loads((root / 'presets/api_pool_default.json').read_text(encoding='utf-8'))]
    assert len(mapping) == len(entries) == 621
    assert len({value.casefold() for value in mapping.values()}) == len(entries)
    for name, token in mapping.items():
        assert 1 <= len(token) <= 6 and not any(ch.isspace() for ch in token)
        assert not any(site in token for site in ('冷雨枫林', '枫雨二代', '糖豆子', '问情', '星之阁', '倾梦'))
        assert [entry.name for entry in entries if entry._match_keywords(token)] == [name]
        assert [entry.name for entry in entries if entry._match_keywords(token.swapcase())] == [name]


@pytest.mark.asyncio
async def test_reload_upgrades_legacy_keywords_without_resetting_settings(plugin):
    entry = plugin.core.api_mgr.entries[0]
    plugin.core.api_mgr.update_entries([{'name':entry.name,'payload':{
        'keywords':['^'+re.escape(entry.name)+'$'], 'params':{'custom':'keep'}, 'scope':['g1'], 'enabled':False}}])
    await plugin.on_unload()
    await plugin.on_load()
    updated = plugin.core.api_mgr.get_entry(entry.name)
    assert updated.keywords[0].startswith('(?i)^')
    assert updated.params == {'custom':'keep'} and updated.scope == ['g1'] and not updated.enabled
    backups = list(plugin.cfg.pool_files_dir.glob('api_pool_before_short_keywords_*.json'))
    assert len(backups) == 1
    before = json.loads(backups[0].read_text(encoding='utf-8'))
    assert next(row for row in before if row['name'] == entry.name)['keywords'] == ['^'+re.escape(entry.name)+'$']
    await plugin.on_unload()
    await plugin.on_load()
    assert len(list(plugin.cfg.pool_files_dir.glob('api_pool_before_short_keywords_*.json'))) == 1


@pytest.mark.asyncio
async def test_user_keywords_and_conflicts_are_preserved(plugin):
    first, second = plugin.core.api_mgr.entries[:2]
    token = json.loads((plugin.cfg.presets_dir / 'short_keywords.json').read_text(encoding='utf-8'))[first.name]
    plugin.core.api_mgr.update_entries([
        {'name':first.name,'payload':{'keywords':['^'+re.escape(first.name)+'$']}},
        {'name':second.name,'payload':{'keywords':['^我的词$']}},
    ])
    plugin.core.api_mgr.add_entries([{'name':'自定义冲突','url':'https://example.com','keywords':['^'+re.escape(token)+'$']}])
    assert PresetService(plugin.core).migrate_short_keywords() == 0
    assert plugin.core.api_mgr.get_entry(first.name).keywords == ['^'+re.escape(first.name)+'$']
    assert plugin.core.api_mgr.get_entry(second.name).keywords == ['^我的词$']
