"""MaiBot 1.3.16 / SDK 2.16 API aggregation entry point."""
from __future__ import annotations

import asyncio
import base64
import json
import logging
import re
import time

from maibot_sdk import API, HookHandler, MaiBotPlugin
from maibot_sdk.types import HookMode

from .api_aggregator import APICoreApp
from .config import ApisConfig, PluginConfig
from .web_gateway import WebGateway
from .api_aggregator.service.preset_service import PresetService

logger = logging.getLogger(__name__)
DETAIL = re.compile(r'^(?:查看api列表|查看api|api列表|apis_help)(?:\s+(.*))?$', re.I)


class ApisPlugin(MaiBotPlugin):
    config_model = ApisConfig

    def __init__(self):
        super().__init__()
        self.ready = False
        self.tasks = set()
        self.recent = {}
        self.seen = {}
        self.lifecycle_lock = asyncio.Lock()

    async def on_load(self):
        if not self.config.plugin.enabled:
            return
        self.cfg = PluginConfig(self.config, self.ctx.paths)
        self.core = APICoreApp(self.cfg)
        self.core.remote.max_response_bytes = self.cfg.max_response_bytes
        await self.core.start()
        # Import bundled presets once only. Emptying a pool later is intentional.
        marker = self.cfg.data_dir / 'presets.initialized'
        if not marker.exists():
            if not self.core.site_mgr.entries:
                self.core.load_site_pool_from_file(self.cfg.site_pool_file)
            if not self.core.api_mgr.entries:
                self.core.load_api_pool_from_file(self.cfg.api_pool_file)
            marker.write_text('3.1.2\n', encoding='utf-8')
        migrated = PresetService(self.core).migrate_short_keywords()
        if migrated:
            logger.info('已备份并更新 %s 条旧默认触发词为短关键词', migrated)
        self.gateway = WebGateway(self.core)
        self.semaphore = asyncio.Semaphore(self.config.trigger.max_concurrent)
        self.ready = True
        logger.info('API 聚合已加载：%s 个 API，%s 个站点', len(self.core.api_mgr.entries), len(self.core.site_mgr.entries))

    async def on_unload(self):
        self.ready = False
        pending = list(self.tasks)
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)
        self.tasks.clear()
        if hasattr(self, 'gateway'):
            await self.gateway.close()
        if hasattr(self, 'core'):
            await self.core.stop()
        self.recent.clear()
        self.seen.clear()

    async def on_config_update(self, scope, config_data, version):
        if scope == 'self':
            async with self.lifecycle_lock:
                await self.on_unload()
                await self.on_load()

    def require_ready(self):
        if not self.ready:
            raise ValueError('插件尚未启用或正在重新加载')

    @staticmethod
    def message_text(message):
        raw = message.get('raw_message')
        if isinstance(raw, list) and raw:
            texts = []
            for segment in raw:
                if isinstance(segment, dict) and segment.get('type') == 'text':
                    value = segment.get('data', segment.get('content', ''))
                    if isinstance(value, dict):
                        value = value.get('text', '')
                    texts.append(str(value))
            return ''.join(texts).strip()
        return str(message.get('processed_plain_text') or '').strip()

    @staticmethod
    def build_params(entry, args, message):
        params = dict(entry.params or {})
        keys = list(params)
        blank = lambda value: value is None or isinstance(value, str) and not value.strip()
        remaining = list(args)
        for key in keys:
            if remaining and blank(params[key]):
                params[key] = remaining.pop(0)
        for key, value in zip(keys, remaining):
            params[key] = value
        extra = []
        for segment in message.get('raw_message') or []:
            if isinstance(segment, dict) and segment.get('type') == 'reply':
                data = segment.get('data') or {}
                if isinstance(data, dict) and data.get('target_message_content'):
                    extra = str(data['target_message_content']).split()
                    break
        user = (message.get('message_info') or {}).get('user_info') or {}
        if not extra:
            nickname = user.get('user_nickname') or user.get('user_id')
            if nickname:
                extra = [str(nickname)]
        for key in keys:
            if blank(params[key]) and extra:
                params[key] = extra.pop(0)
        return params

    async def stream_for(self, message):
        stream_id = str(message.get('session_id') or '')
        if stream_id:
            return stream_id
        info = message.get('message_info') or {}
        user = info.get('user_info') or {}
        group = info.get('group_info') or {}
        stream = await self.ctx.chat.open_session(
            platform=str(message.get('platform') or 'qq'),
            chat_type='group' if group.get('group_id') else 'private',
            user_id=str(user.get('user_id') or ''), group_id=str(group.get('group_id') or ''),
            account_id=str(message.get('account_id') or ''), scope=str(message.get('scope') or ''),
        )
        stream_id = str(stream.get('stream_id') or stream.get('session_id') or '')
        if not stream_id:
            raise ValueError('未能打开目标聊天')
        return stream_id

    @HookHandler('chat.receive.after_process', name='apis_trigger', mode=HookMode.BLOCKING, timeout_ms=10000)
    async def on_message(self, message=None, **kwargs):
        if not self.ready or not isinstance(message, dict) or message.get('is_notify'):
            return
        info = message.get('message_info') or {}
        user = info.get('user_info') or {}
        user_id = str(user.get('user_id') or '')
        if not user_id or user_id == str(message.get('account_id') or ''):
            return
        text = self.message_text(message)
        prefixed = text.startswith('/')
        if prefixed:
            text = text[1:].lstrip()
        detail = DETAIL.fullmatch(text)
        if not detail and self.config.trigger.need_prefix and not (prefixed or message.get('is_at') or message.get('is_mentioned')):
            return
        if not text:
            return
        parts = text.split()
        group = info.get('group_info') or {}
        # Resolve the session before applying session-specific scopes.
        # Avoid creating a session for unrelated messages by doing a regex-only precheck.
        if not detail and not any(entry._match_keywords(parts[0]) and entry.enabled and entry.valid for entry in self.core.api_mgr.entries):
            return
        stream_id = await self.stream_for(message)
        entries = [] if detail else self.core.api_mgr.match_entries(
            parts[0], user_id=user_id, group_id=str(group.get('group_id') or ''),
            session_id=stream_id, is_admin=user_id in self.config.trigger.admin_users,
        )
        if not detail and not entries:
            return
        now = time.monotonic()
        self.seen = {key: stamp for key, stamp in self.seen.items() if now - stamp < 120}
        self.recent = {key: stamp for key, stamp in self.recent.items() if now - stamp < 300}
        message_key = (stream_id, str(message.get('message_id') or ''))
        action = {'action': 'abort'} if self.config.trigger.consume_message else None
        if message_key[1] and message_key in self.seen:
            return action
        if message_key[1]:
            self.seen[message_key] = now
        key = (stream_id, user_id)
        if not detail and now - self.recent.get(key, -100000) < self.config.trigger.cooldown_seconds:
            return action
        if len(self.tasks) >= self.config.trigger.max_concurrent * 4:
            await self.ctx.send.text('API 请求较多，请稍后再试。', stream_id)
            return action
        self.recent[key] = now
        task = asyncio.create_task(self.execute(stream_id, entries, parts[1:], message, detail))
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
        return action

    async def execute(self, stream_id, entries, args, message, detail=None):
        try:
            async with self.semaphore:
                if detail:
                    name = (detail[1] or '').strip()
                    if name:
                        entry = self.core.api_mgr.get_entry(name)
                        text = json.dumps(entry.to_dict(), ensure_ascii=False, indent=2) if entry else '没有找到该 API。'
                    else:
                        text = self.core.api_mgr.display_entries() + '\n\n用法：/触发词 参数；/查看api 名称。管理员请在 API 聚合面板管理站点和接口。'
                    await self.ctx.send.text(text, stream_id)
                    return
                for entry in entries:
                    try:
                        entry.updated_params = self.build_params(entry, args, message)
                        data = await self.core.data_service.fetch(entry, use_local=self.cfg.use_local, save_data=self.cfg.save_data)
                        if data is None:
                            await self.ctx.send.text(f'「{entry.name}」暂时不可用，且没有可用缓存。', stream_id)
                            continue
                        await self.send_resource(data, stream_id)
                    except asyncio.CancelledError:
                        raise
                    except Exception as exc:
                        logger.warning('API 发送失败 [%s]: %s', entry.name, type(exc).__name__)
                        # Do not retry a potentially delivered media message.
                        await self.ctx.send.text(f'「{entry.name}」处理或发送失败，请稍后再试。', stream_id)
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning('API 任务退出: %s', type(exc).__name__)

    async def send_resource(self, data, stream_id):
        if data.data_type.is_text:
            result = await self.ctx.send.text(data.final_text or '', stream_id, return_details=True)
        else:
            if data.binary is not None:
                binary = data.binary
            elif data.saved_path:
                if data.saved_path.stat().st_size > self.cfg.max_response_bytes:
                    raise ValueError('媒体超过大小限制')
                binary = await asyncio.to_thread(data.saved_path.read_bytes)
            else:
                raise ValueError('缺少媒体内容')
            if len(binary) > self.cfg.max_response_bytes:
                raise ValueError('媒体超过大小限制')
            encoded = base64.b64encode(binary).decode('ascii')
            if data.data_type.is_image:
                result = await self.ctx.send.image(encoded, stream_id, return_details=True)
            elif data.data_type.is_audio:
                result = await self.ctx.call_capability('send.custom', message_type='voice', content=encoded, stream_id=stream_id, return_details=True, set_reply=False)
            else:
                result = await self.ctx.call_capability('send.custom', message_type='video', content={'binary_data_base64': encoded}, stream_id=stream_id, return_details=True, set_reply=False)
        if result is False or isinstance(result, dict) and not result.get('sent'):
            raise RuntimeError('发送未确认')

    @API('web_read', version='1')
    async def web_read(self, endpoint: str, payload: str = '{}'):
        self.require_ready()
        return await self.gateway.dispatch(endpoint, 'GET', json.loads(payload))

    @API('web_defaults_info', version='1')
    async def web_defaults_info(self):
        self.require_ready()
        return PresetService(self.core).info()

    @API('web_defaults_replace', version='1')
    async def web_defaults_replace(self, fingerprint: str):
        self.require_ready()
        if self.tasks or any(not job['task'].done() for job in self.gateway.jobs.values()):
            raise ValueError('请先停止测试并等待正在进行的 API 请求完成，再替换默认数据')
        return PresetService(self.core).replace(fingerprint)

    @API('web_write', version='1')
    async def web_write(self, endpoint: str, payload: str = '{}'):
        self.require_ready()
        return await self.gateway.dispatch(endpoint, 'POST', json.loads(payload))

    @API('web_chunk', version='1')
    async def web_chunk(self, token: str, offset: int = 0):
        self.require_ready()
        return self.gateway.chunk(token, offset)

    @API('web_release', version='1')
    async def web_release(self, token: str):
        self.require_ready()
        return self.gateway.release(token)

    @API('web_upload', version='1')
    async def web_upload(self, token: str = '', chunk: str = '', offset: int = 0):
        self.require_ready()
        return self.gateway.upload(token, chunk, offset)

    @API('web_commit', version='1')
    async def web_commit(self, token: str, endpoint: str):
        self.require_ready()
        return await self.gateway.commit(token, endpoint)

    @API('web_test_start', version='1')
    async def web_test_start(self, payload: str = '{}'):
        self.require_ready()
        params = json.loads(payload)
        if not isinstance(params, dict):
            raise ValueError('测试参数必须是对象')
        return self.gateway.start_test(params)

    @API('web_test_poll', version='1')
    async def web_test_poll(self, token: str, cursor: int = 0):
        self.require_ready()
        return self.gateway.poll(token, cursor)

    @API('web_site_test_start', version='1')
    async def web_site_test_start(self, payload: str = '{}'):
        self.require_ready()
        params = json.loads(payload)
        if not isinstance(params, dict):
            raise ValueError('站点测试参数必须是对象')
        return self.gateway.start_test(params, site_mode=True)

    @API('web_test_cancel', version='1')
    async def web_test_cancel(self, token: str):
        self.require_ready()
        return await self.gateway.cancel_test(token)


def create_plugin():
    return ApisPlugin()
