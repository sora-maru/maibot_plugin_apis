import asyncio
import base64
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from aiohttp import web

from maibot_plugin_apis.plugin import create_plugin
from maibot_plugin_apis.api_aggregator import APIEntry
from maibot_plugin_apis.api_aggregator.model import DataResource, DataType
from maibot_plugin_apis.web_gateway import CHUNK_SIZE

PRESET_DIR = Path(__file__).resolve().parents[1] / 'presets'
DEFAULT_API_COUNT = len(json.loads((PRESET_DIR / 'api_pool_default.json').read_text(encoding='utf-8')))
DEFAULT_SITE_COUNT = len(json.loads((PRESET_DIR / 'site_pool_default.json').read_text(encoding='utf-8')))


@pytest_asyncio.fixture
async def plugin(tmp_path):
    p = create_plugin()
    p.set_plugin_config({})
    p._ctx = SimpleNamespace(paths=SimpleNamespace(data_dir=tmp_path / 'data', runtime_dir=tmp_path / 'runtime'), call_capability=AsyncMock(return_value={'sent':True}),
        send=SimpleNamespace(text=AsyncMock(return_value={'sent': True}), image=AsyncMock(return_value={'sent': True}), custom=AsyncMock(return_value={'sent': True})),
        chat=SimpleNamespace(open_session=AsyncMock(return_value={'stream_id': 'host-session'})))
    await p.on_load()
    yield p
    await p.on_unload()


def message(text='/测试 参数', **overrides):
    return {'raw_message': [{'type': 'text', 'data': text}], 'message_id': 'm1', 'platform': 'qq', 'account_id': 'bot', 'scope': 'route',
        'message_info': {'user_info': {'user_id': 'u1', 'user_nickname': '昵称'}, 'group_info': {'group_id': 'g1'}}, **overrides}


def add_api(p, **overrides):
    p.core.api_mgr.add_entries([{'name': '测试', 'url': 'http://localhost/test', 'type': 'text', 'keywords': ['^测试$'], **overrides}])


async def drain(p):
    await asyncio.gather(*list(p.tasks))


@pytest.mark.asyncio
async def test_presets_and_persistence(plugin):
    assert len(plugin.core.api_mgr.entries) == DEFAULT_API_COUNT
    assert len(plugin.core.site_mgr.entries) == DEFAULT_SITE_COUNT
    plugin.core.api_mgr.remove_entries([entry.name for entry in plugin.core.api_mgr.entries])
    await plugin.on_unload()
    await plugin.on_load()
    assert not plugin.core.api_mgr.entries  # intentional empty pool stays empty


@pytest.mark.asyncio
async def test_hook_resolves_route_and_intercepts(plugin):
    add_api(plugin)
    plugin.core.data_service.fetch = AsyncMock(return_value=DataResource(DataType.TEXT, '测试', text='结果'))
    result = await plugin.on_message(message())
    assert result == {'action': 'abort'}
    await drain(plugin)
    plugin.ctx.chat.open_session.assert_awaited_once_with(platform='qq', chat_type='group', user_id='u1', group_id='g1', account_id='bot', scope='route')
    assert plugin.ctx.send.text.await_args.args == ('结果', 'host-session')


@pytest.mark.asyncio
@pytest.mark.parametrize('incoming', [message('测试'), message('/无关'), message('/测试', is_notify=True), message('/测试', message_info={'user_info': {'user_id': 'bot'}})])
async def test_unrelated_messages_are_untouched(plugin, incoming):
    add_api(plugin)
    assert await plugin.on_message(incoming) is None
    assert not plugin.tasks
    plugin.ctx.chat.open_session.assert_not_awaited()


@pytest.mark.asyncio
async def test_scope_checks_and_mention(plugin):
    add_api(plugin, scope=['admin'])
    assert await plugin.on_message(message('测试', is_at=True)) is None
    plugin.config.trigger.admin_users = ['u1']
    plugin.core.data_service.fetch = AsyncMock(return_value=None)
    assert await plugin.on_message(message('测试', is_at=True)) == {'action': 'abort'}
    await drain(plugin)


@pytest.mark.asyncio
async def test_bare_keywords_config_and_dedup(plugin):
    plugin.config.trigger.need_prefix = False
    plugin.config.trigger.consume_message = False
    add_api(plugin)
    plugin.core.data_service.fetch = AsyncMock(return_value=None)
    await plugin.on_message(message('测试'))
    await plugin.on_message(message('测试'))
    await plugin.on_message(message('测试', message_id='m2'))  # cooldown
    await drain(plugin)
    assert plugin.core.data_service.fetch.await_count == 1


@pytest.mark.parametrize('args,quote,expected', [(['显式'], '引用', {'x': '显式', 'y': '默认'}), ([], '引用 参数', {'x': '引用', 'y': '默认'}), ([], '', {'x': '昵称', 'y': '默认'}), (['一','二'], '', {'x': '二', 'y': '默认'})])
def test_parameter_precedence(args, quote, expected):
    entry = APIEntry({'name':'a', 'url':'http://localhost', 'params': {'x': '', 'y': '默认'}})
    incoming = message()
    if quote:
        incoming['raw_message'].append({'type': 'reply', 'data': {'target_message_content': quote}})
    assert create_plugin().build_params(entry, args, incoming) == expected
    assert entry.params['x'] == ''


@pytest.mark.asyncio
@pytest.mark.parametrize('kind', [DataType.TEXT, DataType.IMAGE, DataType.VIDEO, DataType.AUDIO])
async def test_media_transport_uses_content_not_runner_path(plugin, kind):
    data = DataResource(kind, 'a', text='正文', binary=b'example')
    await plugin.send_resource(data, 'target')
    if kind == DataType.TEXT:
        assert plugin.ctx.send.text.await_args.args == ('正文', 'target')
    elif kind == DataType.IMAGE:
        assert base64.b64decode(plugin.ctx.send.image.await_args.args[0]) == b'example'
    else:
        call = plugin.ctx.call_capability.await_args
        assert call.args == ('send.custom',)
        assert call.kwargs['message_type'] == ('voice' if kind == DataType.AUDIO else 'video')
        payload = call.kwargs['content'] if kind == DataType.AUDIO else call.kwargs['content']['binary_data_base64']
        assert base64.b64decode(payload) == b'example'
        assert call.kwargs['set_reply'] is False
        assert 'data' not in call.kwargs


@pytest.mark.asyncio
async def test_failed_media_is_not_retried(plugin):
    plugin.ctx.send.image.return_value = {'sent': False}
    with pytest.raises(RuntimeError):
        await plugin.send_resource(DataResource(DataType.IMAGE, 'a', binary=b'image'), 'target')
    assert plugin.ctx.send.image.await_count == 1


@pytest.mark.asyncio
async def test_maximum_video_rpc_fits_host_frame(plugin):
    plugin.cfg.max_response_bytes = 11 * 1024 * 1024
    await plugin.send_resource(DataResource(DataType.VIDEO, '大文件', binary=b'x' * plugin.cfg.max_response_bytes), 'target')
    params = plugin.ctx.call_capability.await_args.kwargs
    assert len(json.dumps({'method':'cap.call', 'params':params}).encode()) < 16 * 1024 * 1024


@pytest.mark.asyncio
async def test_cache_dataset_cannot_escape_local_directory(plugin, tmp_path):
    outside = tmp_path / 'keep'
    outside.mkdir()
    marker = outside / 'marker'
    marker.write_text('keep')
    result = plugin.core.local.delete_collections_batch([{'type':'video','name':'../../../keep'}])
    assert result.get('failed')
    assert marker.read_text() == 'keep'


@pytest.mark.asyncio
async def test_cache_fallback_and_save_disabled(plugin):
    entry = APIEntry({'name': '缓存测试', 'url':'http://localhost', 'type':'text'})
    from maibot_plugin_apis.api_aggregator.data_service.request_result import RequestResult
    plugin.core.remote.get_data = AsyncMock(return_value=RequestResult(status=200, raw_text='已缓存'))
    await plugin.core.data_service.fetch(entry)
    plugin.core.remote.get_data = AsyncMock(return_value=RequestResult(error='offline'))
    cached = await plugin.core.data_service.fetch(entry)
    assert cached.final_text == '已缓存'
    assert await plugin.core.data_service.fetch(entry, use_local=False) is None
    plugin.core.remote.get_data = AsyncMock(return_value=RequestResult(status=200, raw_text='不保存'))
    await plugin.core.data_service.fetch(entry, save_data=False)
    plugin.core.remote.get_data = AsyncMock(return_value=RequestResult(error='offline'))
    assert (await plugin.core.data_service.fetch(entry)).final_text == '已缓存'


async def unpack(p, value):
    if '__transfer' not in value:
        return value
    payload = bytearray()
    while len(payload) < value['size']:
        part = await p.web_chunk(value['__transfer'], len(payload))
        payload.extend(base64.b64decode(part['data']))
    await p.web_release(value['__transfer'])
    return json.loads(payload) if value['content_type'] == 'application/x-apis-json' else bytes(payload)


@pytest.mark.asyncio
async def test_dashboard_crud_export_import(plugin):
    state = await unpack(plugin, await plugin.web_read('page/pool'))
    assert len(state['data']['apis']) == DEFAULT_API_COUNT
    payload = {'items': [{'name':'新增', 'url':'http://localhost', 'keywords':['新增']}]}
    response = await plugin.web_write('page/api/batch', json.dumps(payload))
    assert response['status'] == 'ok'
    await plugin.web_write('page/api/batch', json.dumps({'_method':'PUT', 'items':[{'name':'新增', 'payload':{'keywords':['修改']}}]}))
    assert plugin.core.api_mgr.get_entry('新增').keywords == ['修改']
    exported = await unpack(plugin, await plugin.web_read('page/pool/export/api'))
    assert any(row['name'] == '新增' for row in json.loads(exported))
    await plugin.web_write('page/api/batch', json.dumps({'_method':'DELETE', 'names':['新增']}))
    assert plugin.core.api_mgr.get_entry('新增') is None
    await plugin.web_write('page/pool/import/api', json.dumps({'content':exported.decode()}))
    assert plugin.core.api_mgr.get_entry('新增') is not None


@pytest.mark.asyncio
async def test_chunked_upload_and_offsets(plugin):
    raw = json.dumps({'content':json.dumps([{'name':'分块', 'url':'http://localhost', 'keywords':['x']}])}).encode()
    first = await plugin.web_upload(chunk=base64.b64encode(raw[:12]).decode(), offset=0)
    with pytest.raises(ValueError):
        await plugin.web_upload(token=first['token'], chunk='YQ==', offset=0)
    await plugin.web_upload(token=first['token'], chunk=base64.b64encode(raw[12:]).decode(), offset=12)
    result = await plugin.web_commit(first['token'], 'page/pool/import/api')
    assert result['status'] == 'ok'
    assert plugin.core.api_mgr.get_entry('分块')


@pytest.mark.asyncio
async def test_large_unicode_response_roundtrip(plugin):
    data = {'text':'中文🙂' * 20000}
    packed = plugin.gateway.pack(data)
    assert packed['size'] > CHUNK_SIZE
    assert await unpack(plugin, packed) == data


@pytest.mark.asyncio
async def test_page_request_context_isolation(plugin):
    a,b = await asyncio.gather(plugin.web_read('page/editor/api-form'), plugin.web_read('page/editor/site-form'))
    assert b'apiName' in await unpack(plugin, a)
    assert b'siteName' in await unpack(plugin, b)
    with pytest.raises(ValueError):
        await plugin.web_read('page/api/batch')
    with pytest.raises(ValueError):
        await plugin.web_read('../../anything')


@pytest.mark.asyncio
async def test_export_and_preview_path_boundaries(plugin, tmp_path):
    response = await plugin.web_write('page/pool/export/api', json.dumps({'path':str(tmp_path / 'outside.json')}))
    assert response['status'] == 'error'
    assert not (tmp_path / 'outside.json').exists()
    with pytest.raises(Exception):
        plugin.core.local.resolve_local_file(str(tmp_path / 'outside.json'))


@pytest.mark.asyncio
async def test_api_scope_and_invalid_rules(plugin):
    add_api(plugin, scope=['g1'])
    assert plugin.core.api_mgr.match_entries('测试', group_id='g1')
    assert not plugin.core.api_mgr.match_entries('测试', group_id='g2')
    add_api(plugin, name='坏规则', keywords=['['])
    assert not plugin.core.api_mgr.get_entry('坏规则').check_activate(text='x', user_id='', group_id='', session_id='', is_admin=False)


@pytest.mark.asyncio
async def test_unknown_test_selection_does_not_test_everything(plugin):
    plugin.core.remote.stream_test_apis = AsyncMock()  # replaced with an async generator below
    seen = []
    async def capture(entries, **kwargs):
        seen.extend(entries)
        yield {'event':'done'}
    plugin.core.remote.stream_test_apis = capture
    events = [item async for item in plugin.core.api_test_service.stream_test_apis(names=['不存在'])]
    assert not seen
    assert events == [{'event':'done'}]


@pytest.mark.asyncio
async def test_test_jobs_poll_and_cancel(plugin):
    cancelled = asyncio.Event()
    async def fake(**kwargs):
        try:
            yield {'event':'start', 'total':1}
            await asyncio.Event().wait()
        finally:
            cancelled.set()
    plugin.core.api_test_service.stream_test_apis = fake
    token = (await plugin.web_test_start())['token']
    await asyncio.sleep(0)
    result = await plugin.web_test_poll(token)
    assert result['events'][0]['event'] == 'start'
    await plugin.web_test_cancel(token)
    assert cancelled.is_set()


@pytest.mark.asyncio
async def test_real_local_http_parsing_and_size_limit(plugin):
    app = web.Application()
    async def respond_json(request):
        return web.json_response({'data':{'value':'本地响应'}})
    async def respond_large(request):
        return web.Response(body=b'x'*2000)
    app.router.add_get('/json', respond_json)
    app.router.add_get('/large', respond_large)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]
    try:
        entry = APIEntry({'name':'http', 'url':f'http://127.0.0.1:{port}/json', 'parse':'data.value'})
        result = await plugin.core.remote.get_data(entry)
        assert result.raw_text == '本地响应'
        plugin.core.remote.max_response_bytes = 100
        entry.url = f'http://127.0.0.1:{port}/large'
        assert not (await plugin.core.remote.get_data(entry)).ok
    finally:
        await runner.cleanup()


@pytest.mark.parametrize('old,new,url,expected', [
    ('https://old.example','https://new.example','https://old.example/api/a?key=x#part','https://new.example/api/a?key=x#part'),
    ('https://old.example/api/','http://new.example/v2/','https://old.example/api/a?x=1','http://new.example/v2/a?x=1'),
    ('https://old.example/api','https://new.example','https://old.example/api','https://new.example'),
])
@pytest.mark.asyncio
async def test_site_update_rewrites_associated_urls_and_persists(plugin,old,new,url,expected):
    plugin.core.site_mgr.add_entries([{'name':'迁移站','url':old}])
    plugin.core.api_mgr.add_entries([{'name':'迁移接口','url':url,'keywords':['迁移'],'params':{'a':'值'},'scope':['g1']}])
    result = await plugin.web_write('page/site/batch',json.dumps({'_method':'PUT','items':[{'name':'迁移站','payload':{'url':new,'name':'新站名'}}]}))
    assert result['status']=='ok'
    assert result['data']['updated_apis']==1
    api = plugin.core.api_mgr.get_entry('迁移接口')
    assert api.url == expected and api.site == '新站名'
    assert api.params=={'a':'值'} and api.scope==['g1']
    await plugin.on_unload()
    await plugin.on_load()
    assert plugin.core.site_mgr.get_entry('迁移站') is None
    assert plugin.core.site_mgr.get_entry('新站名')
    assert plugin.core.api_mgr.get_entry('迁移接口').url == expected


@pytest.mark.asyncio
async def test_site_url_boundaries_and_specific_ownership(plugin):
    plugin.core.site_mgr.add_entries([{'name':'基础站','url':'https://boundary.example/api'}, {'name':'子站','url':'https://boundary.example/api/sub'}])
    plugin.core.api_mgr.add_entries([{'name':name,'url':url} for name,url in [
        ('属于基础站','https://boundary.example/api/a'),('属于子站','https://boundary.example/api/sub/a'),
        ('相似路径','https://boundary.example/apix/a'),('相似域名','https://boundary.example.evil/api/a')]])
    result=plugin.core.site_sync_service.update_sites([{'name':'基础站','payload':{'url':'https://moved.example'}}])
    assert result[1]==1
    assert plugin.core.api_mgr.get_entry('属于子站').url=='https://boundary.example/api/sub/a'
    assert plugin.core.api_mgr.get_entry('相似路径').site==''
    assert plugin.core.api_mgr.get_entry('相似域名').site==''


@pytest.mark.asyncio
async def test_site_updates_validate_entire_batch_before_mutation(plugin):
    plugin.core.site_mgr.add_entries([{'name':'站甲','url':'https://a.example'},{'name':'站乙','url':'https://b.example'}])
    with pytest.raises(LookupError):
        plugin.core.site_sync_service.update_sites([{'name':'站甲','payload':{'url':'https://changed.example'}},{'name':'不存在','payload':{'url':'https://none.example'}}])
    assert plugin.core.site_mgr.get_entry('站甲').url=='https://a.example'
    with pytest.raises(ValueError):
        plugin.core.site_sync_service.update_sites([{'name':'站甲','payload':{'name':'站乙'}}])
    assert plugin.core.site_mgr.get_entry('站甲')


@pytest.mark.asyncio
async def test_site_delete_cascades_only_owned_apis_and_survives_reload(plugin):
    plugin.core.site_mgr.add_entries([{'name':'删除站','url':'https://delete.example'},{'name':'保留站','url':'https://keep.example'}])
    plugin.core.api_mgr.add_entries([{'name':'删除接口','url':'https://delete.example/a'},{'name':'保留接口','url':'https://keep.example/a'}])
    result=await plugin.web_write('page/site/batch',json.dumps({'_method':'DELETE','names':['删除站']}))
    assert result['data']['deleted_apis']==['删除接口']
    await plugin.on_unload()
    await plugin.on_load()
    assert plugin.core.api_mgr.get_entry('删除接口') is None
    assert plugin.core.site_mgr.get_entry('删除站') is None
    assert plugin.core.api_mgr.get_entry('保留接口')


@pytest.mark.asyncio
async def test_site_transaction_rolls_back_on_storage_error(plugin,monkeypatch):
    plugin.core.site_mgr.add_entries([{'name':'事务站','url':'https://transaction.example'}])
    plugin.core.api_mgr.add_entries([{'name':'事务接口','url':'https://transaction.example/a'}])
    original = plugin.core.db._apply_pool_table_batch
    def fail(conn, table, **kwargs):
        if table=='api_pool':
            raise RuntimeError('simulated storage error')
        return original(conn,table,**kwargs)
    monkeypatch.setattr(plugin.core.db,'_apply_pool_table_batch',fail)
    with pytest.raises(RuntimeError):
        plugin.core.site_sync_service.update_sites([{'name':'事务站','payload':{'url':'https://changed.example'}}])
    assert plugin.core.site_mgr.get_entry('事务站').url=='https://transaction.example'
    assert plugin.core.api_mgr.get_entry('事务接口').url=='https://transaction.example/a'
    with pytest.raises(RuntimeError):
        plugin.core.site_sync_service.delete_sites(['事务站'])
    assert plugin.core.site_mgr.get_entry('事务站')
    assert plugin.core.api_mgr.get_entry('事务接口')


@pytest.mark.asyncio
async def test_site_test_results_do_not_delete_or_mislabel_partial_failure(plugin):
    from maibot_plugin_apis.api_aggregator.data_service.request_result import RequestResult
    plugin.core.site_mgr.add_entries([{'name':name,'url':f'https://{domain}.example'} for name,domain in [('混合站','mixed'),('失败站','bad'),('空站','empty')]])
    plugin.core.api_mgr.add_entries([{'name':name,'url':url} for name,url in [('可用','https://mixed.example/good'),('失败','https://mixed.example/bad'),('全失败','https://bad.example/bad')]])
    async def response(entry):
        return RequestResult(status=200,raw_text='ok') if entry.name=='可用' else RequestResult(error='timeout')
    plugin.core.remote.get_data=response
    plugin.core.remote._request=AsyncMock(return_value=RequestResult(status=200,raw_text='homepage'))
    events=[event async for event in plugin.gateway.site_test_events({'names':['混合站','失败站','空站']})]
    rows={event['name']:event for event in events if event['event']=='site_result'}
    assert rows['混合站']['reachable'] and rows['混合站']['failed']==1
    assert not rows['失败站']['reachable']
    assert rows['空站']['reachable'] and rows['空站']['total_apis']==0
    assert plugin.core.site_mgr.get_entry('失败站') and plugin.core.api_mgr.get_entry('全失败')


@pytest.mark.asyncio
async def test_site_jobs_use_polling_and_cancellation(plugin):
    started=asyncio.Event()
    stopped=asyncio.Event()
    async def slow(params):
        try:
            started.set()
            yield {'event':'start','total':1}
            await asyncio.Event().wait()
        finally:
            stopped.set()
    plugin.gateway.site_test_events=slow
    token=(await plugin.web_site_test_start())['token']
    await started.wait()
    assert (await plugin.web_test_poll(token))['events'][0]['event']=='start'
    await plugin.web_test_cancel(token)
    assert stopped.is_set()


@pytest.mark.parametrize('raw,expected',[
    (r'第一行\r第二行','第一行\n第二行'),
    (r'第一行\r\n第二行\n第三行','第一行\n第二行\n第三行'),
    ('第一行\r\n第二行\r第三行','第一行\n第二行\n第三行'),
    ('中文🙂 https://example.com/a?q=1','中文🙂 https://example.com/a?q=1'),
])
def test_response_linebreaks_preserve_unicode_and_urls(raw,expected):
    from maibot_plugin_apis.api_aggregator.text import normalize_response_text
    assert normalize_response_text(raw)==expected
    assert DataResource(DataType.TEXT,'旧缓存',saved_text=raw).final_text==expected


@pytest.mark.asyncio
async def test_normalized_text_is_used_in_cache_and_previews(plugin):
    raw=r'中文\r\n下一行\n第三行'
    saved=await plugin.core.local.save_data(DataResource(DataType.TEXT,'换行',text=raw))
    assert saved.saved_text=='中文\n下一行\n第三行'
    details=plugin.core.local.get_collection_items_batch([{'type':'text','name':'换行'}])
    assert '\\r' not in json.dumps(details,ensure_ascii=False).replace('\\n','')


@pytest.mark.asyncio
async def test_cancelling_batch_stops_site_workers(plugin):
    began, stopped = asyncio.Event(), asyncio.Event()
    async def slow(entry):
        try:
            began.set()
            await asyncio.Event().wait()
        finally:
            stopped.set()
    plugin.core.remote.get_data = slow
    entries=[APIEntry({'name':'取消测试','url':'https://cancel.example/a'})]
    stream=plugin.core.remote.stream_test_apis(entries)
    assert (await anext(stream))['event']=='start'
    waiter=asyncio.create_task(anext(stream))
    await began.wait()
    waiter.cancel()
    await asyncio.gather(waiter,return_exceptions=True)
    assert stopped.is_set()


@pytest.mark.asyncio
async def test_linebreak_normalization_does_not_bypass_json_error_status(plugin):
    from maibot_plugin_apis.api_aggregator.data_service.request_result import RequestResult
    result=RequestResult(status=200,raw_text=json.dumps({'code':500,'message':'错误\\r请重试'}),content_type='application/json')
    plugin.core.remote._request=AsyncMock(return_value=result)
    result=await plugin.core.remote.get_data(APIEntry({'name':'json错误','url':'https://error.example'}))
    assert not result.ok


@pytest.mark.asyncio
async def test_replace_presets_creates_backups_and_preserves_keys_and_cache(plugin):
    from maibot_plugin_apis.api_aggregator.service.preset_service import PresetService
    service=PresetService(plugin.core)
    first=plugin.core.site_mgr.entries[0]
    plugin.core.site_sync_service.update_sites([{'name':first.name,'payload':{'keys':{'my_key':'private-value'},'headers':{'X-Custom':'retain'}}}])
    add_api(plugin,name='用户自定义')
    await plugin.core.local.save_data(DataResource(DataType.TEXT,'保留缓存',text='不删除'))
    old_count=len(plugin.core.api_mgr.entries)
    info=await plugin.web_defaults_info()
    result=await plugin.web_defaults_replace(info['fingerprint'])
    assert len(plugin.core.api_mgr.entries)==DEFAULT_API_COUNT
    assert plugin.core.api_mgr.get_entry('用户自定义') is None
    assert plugin.core.site_mgr.get_entry(first.name).keys['my_key']=='private-value'
    assert plugin.core.site_mgr.get_entry(first.name).headers['X-Custom']=='retain'
    backup=json.loads((plugin.cfg.pool_files_dir/result['backup_api_file']).read_text(encoding='utf-8'))
    assert len(backup)==old_count and any(row['name']=='用户自定义' for row in backup)
    assert (await plugin.core.local.get_random_data(DataType.TEXT,'保留缓存')).final_text=='不删除'
    disabled={row['name'] for row in json.loads(plugin.cfg.api_pool_file.read_text(encoding='utf-8')) if not row.get('enabled',True)}
    assert all(not plugin.core.api_mgr.get_entry(name).enabled for name in disabled)
    await plugin.on_unload()
    await plugin.on_load()
    assert len(plugin.core.api_mgr.entries)==DEFAULT_API_COUNT


@pytest.mark.asyncio
async def test_replace_wrong_fingerprint_does_not_change_data(plugin):
    original=[row.to_dict() for row in plugin.core.api_mgr.entries]
    with pytest.raises(ValueError):await plugin.web_defaults_replace('wrong-version')
    assert [row.to_dict() for row in plugin.core.api_mgr.entries]==original


@pytest.mark.asyncio
async def test_replace_backup_failure_does_not_change_database(plugin,monkeypatch):
    add_api(plugin,name='不要丢失')
    real_open=Path.open
    def fail(path,*args,**kwargs):
        if path.name.startswith('site_pool_backup_'):
            raise OSError('backup disk full')
        return real_open(path,*args,**kwargs)
    monkeypatch.setattr(Path,'open',fail)
    with pytest.raises(OSError):await plugin.web_defaults_replace((await plugin.web_defaults_info())['fingerprint'])
    assert plugin.core.api_mgr.get_entry('不要丢失')


@pytest.mark.asyncio
async def test_replace_rejects_running_test(plugin):
    async def slow(**kwargs):
        yield {'event':'start'}
        await asyncio.Event().wait()
    plugin.core.api_test_service.stream_test_apis=slow
    token=(await plugin.web_test_start())['token']
    with pytest.raises(ValueError):await plugin.web_defaults_replace((await plugin.web_defaults_info())['fingerprint'])
    await plugin.web_test_cancel(token)


@pytest.mark.asyncio
async def test_replace_db_failure_keeps_original_pools(plugin,monkeypatch):
    add_api(plugin,name='事务保留')
    original=plugin.core.db._apply_pool_table_batch
    def fail(conn,table,**kwargs):
        if table=='api_pool':raise RuntimeError('replace failure')
        return original(conn,table,**kwargs)
    monkeypatch.setattr(plugin.core.db,'_apply_pool_table_batch',fail)
    with pytest.raises(RuntimeError):await plugin.web_defaults_replace((await plugin.web_defaults_info())['fingerprint'])
    assert plugin.core.api_mgr.get_entry('事务保留')
    assert len(plugin.core.site_mgr.entries)==DEFAULT_SITE_COUNT


@pytest.mark.asyncio
async def test_text_result_with_url_is_not_downloaded_as_cover(plugin):
    from maibot_plugin_apis.api_aggregator.data_service.request_result import RequestResult
    plugin.core.remote._request=AsyncMock(return_value=RequestResult(status=200,raw_text='{"code":1,"data":{"title":"标题","cover":"https://images.example/a.jpg"}}'))
    result=await plugin.core.remote.get_data(APIEntry({'name':'文字JSON','url':'https://text.example','type':'text','parse':'data'}))
    assert result.ok and '标题' in result.raw_text and 'https://images.example/a.jpg' in result.raw_text
    assert plugin.core.remote._request.await_count==1


@pytest.mark.asyncio
async def test_signed_media_url_is_preserved_without_leaking_credentials(plugin):
    from maibot_plugin_apis.api_aggregator.data_service.request_result import RequestResult
    plugin.core.site_mgr.add_entries([{'name':'有密钥的站点','url':'https://api.example','keys':{'key':'private'},'headers':{'Cookie':'private-cookie'}}])
    signed='https://cdn.example/a.mp3?signature=a%2Bb%3D&x=1'
    plugin.core.remote._request=AsyncMock(side_effect=[RequestResult(status=200,raw_text=json.dumps({'code':0,'data':{'url':signed}})),RequestResult(status=200,raw_content=b'mp3',content_type='audio/mpeg')])
    result=await plugin.core.remote.get_data(APIEntry({'name':'音频','url':'https://api.example/a','type':'audio','parse':'data.url'}))
    assert result.raw_content==b'mp3'
    second=plugin.core.remote._request.await_args_list[1]
    assert second.args[0]==signed and second.kwargs['params']=={}
    assert 'Cookie' not in second.kwargs['headers'] and 'key' not in second.kwargs['headers']


def test_nested_array_response_preserves_scalar_values():
    from maibot_plugin_apis.api_aggregator.data_service.request_result import RequestResult
    result=RequestResult(raw_text='{"data":{"images":["a","b"],"count":2}}')
    result.parse_nested('data')
    assert 'a' in result.raw_text and 'b' in result.raw_text and '2' in result.raw_text
