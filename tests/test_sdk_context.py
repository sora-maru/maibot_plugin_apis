"""Integration at the real SDK RPC boundary; no live Host/account needed."""
import asyncio
import json
import re

import pytest
from maibot_sdk.context import PluginContext, PluginPaths
from maibot_sdk.config import generate_plugin_config_schema

from maibot_plugin_apis.plugin import create_plugin
from maibot_plugin_apis.config import ApisConfig
from maibot_plugin_apis.api_aggregator.model import DataResource, DataType


@pytest.mark.asyncio
async def test_real_sdk_lifecycle_and_account_route_with_host_envelope(tmp_path):
    calls = []
    async def rpc(method, plugin_id, payload, **kwargs):
        calls.append((method, plugin_id, payload))
        if payload['capability'] == 'chat.open_session':
            return {'success': True, 'stream_id': 'host-real-route', 'session_id': 'host-real-route'}
        return {'success': True, 'sent': True, 'message_id': 'receipt'}

    p = create_plugin()
    p.set_plugin_config({})
    p._ctx = PluginContext('github.sora-maru.apis', rpc_call=rpc,
        paths=PluginPaths(data_dir=tmp_path/'data', runtime_dir=tmp_path/'runtime'))
    await p.on_load()
    try:
        p.core.api_mgr.add_entries([{'name':'SDK测试','url':'https://example.com','keywords':['^上下文$']}])
        async def fetch(*args, **kwargs):
            return DataResource(DataType.TEXT, 'SDK测试', text='接口结果')
        p.core.data_service.fetch = fetch
        message = {'message_id':'ctx-1','platform':'qq','account_id':'bot-2','scope':'account-B',
            'raw_message':[{'type':'text','data':'/上下文'}],
            'message_info':{'user_info':{'user_id':'user-1','user_nickname':'用户'},'group_info':{'group_id':'group-1'}}}
        hook = next(component for component in p.get_components() if component['name']=='apis_trigger')
        result = await getattr(p, hook['metadata']['handler_name'])(message=message)
        assert result['action'] == 'abort' and result['custom_result']['reason']
        await asyncio.gather(*list(p.tasks))
        request = next(payload for _,_,payload in calls if payload['capability'] == 'chat.open_session')
        assert request['args']['account_id']=='bot-2' and request['args']['scope']=='account-B'
        assert any(payload['args'].get('stream_id')=='host-real-route' and payload['args'].get('text')=='接口结果'
                   for _,_,payload in calls)
        assert all(plugin_id=='github.sora-maru.apis' for _,plugin_id,_ in calls)
        await p.on_config_update('self', p.config.model_dump(), '1.0.0')
        assert p.ready
    finally:
        await p.on_unload()
    assert not p.ready and not p.tasks


@pytest.mark.asyncio
@pytest.mark.parametrize('kind', list(DataType))
async def test_real_sdk_send_result_and_single_media_payload(tmp_path, kind):
    recorded=[]
    async def rpc(method, plugin_id, payload, **kwargs):
        recorded.append(payload)
        # The Host reports success plus final platform ID; SDK unwraps details.
        return {'success': True, 'sent': True, 'message_id':'receipt'}
    p=create_plugin()
    p.set_plugin_config({})
    p._ctx=PluginContext('github.sora-maru.apis', rpc_call=rpc,
        paths=PluginPaths(data_dir=tmp_path/'data',runtime_dir=tmp_path/'runtime'))
    await p.on_load()
    try:
        await p.send_resource(DataResource(kind, 'sdk-media', text='正文' if kind==DataType.TEXT else None,
            binary=b'media' if kind!=DataType.TEXT else None),'stream')
        assert len(recorded)==1
        payload=recorded[0]
        assert payload['args']['return_details'] is True
        if kind in {DataType.AUDIO, DataType.VIDEO}:
            assert payload['capability']=='send.custom'
            assert payload['args']['message_type']==('voice' if kind==DataType.AUDIO else 'video')
            assert 'data' not in payload['args']
            assert json.dumps(payload).count('bWVkaWE=')==1
    finally:
        await p.on_unload()


def test_chinese_configuration_schema_and_existing_values():
    p=create_plugin()
    p.set_plugin_config({'plugin':{'config_version':'1.0.0'},'trigger':{'admin_users':['123456'],
        'need_prefix':False},'data':{'max_media_mb':5}})
    assert p.config.trigger.admin_users==['123456'] and not p.config.trigger.need_prefix
    assert p.config.data.max_media_mb==5
    schema=generate_plugin_config_schema(ApisConfig)
    assert len(schema['sections'])==3
    assert sum(len(section['fields']) for section in schema['sections'].values())==10
    for section in schema['sections'].values():
        assert re.search(r'[\u4e00-\u9fff]',section['title'])
        assert all(re.search(r'[\u4e00-\u9fff]',field['label']) for field in section['fields'].values())
