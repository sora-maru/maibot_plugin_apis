import json

import pytest

from test_port import plugin


@pytest.mark.asyncio
async def test_batch_api_switches_preserve_rules_and_persist(plugin):
    entries = plugin.core.api_mgr.entries[:12]
    names = [entry.name for entry in entries]
    originals = {entry.name:entry.to_dict() for entry in entries}
    for enabled in (False, True):
        response = await plugin.web_write('page/api/batch', json.dumps({'_method':'PUT','items':[
            {'name':name,'payload':{'enabled':enabled}} for name in names]}))
        assert response['status'] == 'ok'
        await plugin.on_unload()
        await plugin.on_load()
        for name in names:
            entry = plugin.core.api_mgr.get_entry(name)
            assert entry.enabled is enabled
            assert {k:v for k,v in entry.to_dict().items() if k != 'enabled'} == {
                k:v for k,v in originals[name].items() if k != 'enabled'}


@pytest.mark.asyncio
async def test_batch_site_switches_follow_apis_and_cascade_delete_selected_only(plugin):
    plugin.core.site_mgr.add_entries([{'name':'批量甲','url':'https://batch-a.example'},
        {'name':'批量乙','url':'https://batch-b.example'}, {'name':'保留','url':'https://remain.example'}])
    plugin.core.api_mgr.add_entries([{'name':'甲接口','url':'https://batch-a.example/a'},
        {'name':'乙接口','url':'https://batch-b.example/a'}, {'name':'保留接口','url':'https://remain.example/a'}])
    for enabled in (False, True):
        response = await plugin.web_write('page/site/batch', json.dumps({'_method':'PUT','items':[
            {'name':name,'payload':{'enabled':enabled}} for name in ('批量甲','批量乙')]}))
        assert response['status'] == 'ok'
        assert all(plugin.core.site_mgr.get_entry(name).enabled is enabled for name in ('批量甲','批量乙'))
        assert plugin.core.api_mgr.get_entry('甲接口').enabled is enabled
        assert plugin.core.api_mgr.get_entry('乙接口').enabled is enabled
        assert plugin.core.api_mgr.get_entry('保留接口').enabled
    result = await plugin.web_write('page/site/batch', json.dumps({'_method':'DELETE','names':['批量甲','批量乙']}))
    assert result['status'] == 'ok'
    assert set(result['data']['deleted_apis']) == {'甲接口','乙接口'}
    await plugin.on_unload()
    await plugin.on_load()
    assert plugin.core.api_mgr.get_entry('甲接口') is None
    assert plugin.core.api_mgr.get_entry('乙接口') is None
    assert plugin.core.api_mgr.get_entry('保留接口')
    assert plugin.core.site_mgr.get_entry('保留')


@pytest.mark.asyncio
async def test_site_switch_updates_disabled_apis_and_keeps_other_fields(plugin):
    plugin.core.site_mgr.add_entries([{'name':'联动站','url':'https://follow.example','keys':{'key':'private'}},
        {'name':'子站','url':'https://follow.example/sub'}])
    plugin.core.api_mgr.add_entries([
        {'name':'父接口','url':'https://follow.example/a','enabled':False,'valid':False,'scope':['g1'],'params':{'x':'value'},'keywords':['^自定义$']},
        {'name':'子接口','url':'https://follow.example/sub/a','enabled':False}])
    original=plugin.core.api_mgr.get_entry('父接口').to_dict()
    # Explicit same-state true still enables a disabled API.
    result=await plugin.web_write('page/site/batch',json.dumps({'_method':'PUT','items':[{'name':'联动站','payload':{'enabled':True}}]}))
    assert result['status']=='ok'
    current=plugin.core.api_mgr.get_entry('父接口')
    assert current.enabled and not current.valid
    assert all(current.to_dict()[key]==original[key] for key in ('params','keywords','scope','valid','url'))
    assert not plugin.core.api_mgr.get_entry('子接口').enabled
    assert plugin.core.site_mgr.get_entry('联动站').keys=={'key':'private'}
    await plugin.on_unload()
    await plugin.on_load()
    assert plugin.core.api_mgr.get_entry('父接口').enabled
    assert not plugin.core.api_mgr.get_entry('子接口').enabled


@pytest.mark.asyncio
async def test_saving_site_credentials_does_not_switch_apis(plugin):
    plugin.core.site_mgr.add_entries([{'name':'凭据站','url':'https://credentials.example'}])
    plugin.core.api_mgr.add_entries([{'name':'关接口','url':'https://credentials.example/off','enabled':False},
        {'name':'开接口','url':'https://credentials.example/on','enabled':True}])
    plugin.core.site_sync_service.update_sites([{'name':'凭据站','payload':{'keys':{'key':'value'},'url':'https://moved.example','name':'新名'}}])
    assert not plugin.core.api_mgr.get_entry('关接口').enabled
    assert plugin.core.api_mgr.get_entry('开接口').enabled


@pytest.mark.asyncio
async def test_site_switch_rolls_back_site_and_api_on_failure(plugin,monkeypatch):
    plugin.core.site_mgr.add_entries([{'name':'回滚站','url':'https://rollback.example'}])
    plugin.core.api_mgr.add_entries([{'name':'回滚接口','url':'https://rollback.example/a'}])
    original=plugin.core.db._apply_pool_table_batch
    def fail(conn,table,**kwargs):
        if table=='api_pool':raise RuntimeError('storage failure')
        return original(conn,table,**kwargs)
    monkeypatch.setattr(plugin.core.db,'_apply_pool_table_batch',fail)
    with pytest.raises(RuntimeError):
        plugin.core.site_sync_service.update_sites([{'name':'回滚站','payload':{'enabled':False}}])
    assert plugin.core.site_mgr.get_entry('回滚站').enabled
    assert plugin.core.api_mgr.get_entry('回滚接口').enabled
