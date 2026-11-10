"""Authenticated MaiBot page APIs, chunked transfers and cancellable tests."""
from __future__ import annotations

import asyncio
import base64
import copy
import json
import re
import secrets
import time
from pathlib import Path

from .page_controller import APIPageController
from .web_compat import Request, Response, StreamResponse, current_request

CHUNK_SIZE = 24000
MAX_TRANSFER = 32 * 1024 * 1024
MAX_UPLOAD = 4 * 1024 * 1024


class WebGateway:
    def __init__(self, core):
        self.core = core
        self.routes = []
        self.transfers = {}
        self.uploads = {}
        self.jobs = {}
        self.controller = APIPageController(self, core)
        self.controller.register_routes()

    def register_web_api(self, path, handler, methods, description):
        path = path.removeprefix('/astrbot_plugin_apis/')
        pattern = re.escape(path).replace('<pool_type>', '(?P<pool_type>api|site)')
        self.routes.append((re.compile('^' + pattern + '$'), handler, methods))

    def cleanup(self):
        now = time.monotonic()
        for pool in (self.transfers, self.uploads):
            for token, item in list(pool.items()):
                if now - item['time'] > 600:
                    del pool[token]
        for token, job in list(self.jobs.items()):
            if now - job['time'] > 1800:
                job['task'].cancel()
                del self.jobs[token]

    def transfer(self, content, media_type, filename=''):
        self.cleanup()
        if len(content) > MAX_TRANSFER:
            raise ValueError('文件超过 32 MiB 预览/下载限制')
        if sum(len(item['data']) for item in self.transfers.values()) + len(content) > 64 * 1024 * 1024:
            raise ValueError('预览传输繁忙，请稍后重试')
        token = secrets.token_urlsafe(24)
        self.transfers[token] = {'data': content, 'time': time.monotonic()}
        return {'__transfer': token, 'size': len(content), 'content_type': media_type, 'filename': filename}

    def pack(self, value):
        if isinstance(value, Response):
            disposition = value.headers.get('Content-Disposition', '')
            match = re.search('filename="([^"]+)"', disposition)
            return self.transfer(value.content, value.media_type, match[1] if match else '')
        data = json.dumps(value, ensure_ascii=False).encode('utf-8')
        if len(data) > 30000:
            return self.transfer(data, 'application/x-apis-json')
        return value

    def chunk(self, token, offset):
        self.cleanup()
        item = self.transfers.get(token)
        if item is None:
            raise ValueError('传输已过期，请重新打开')
        if type(offset) is not int or not 0 <= offset <= len(item['data']):
            raise ValueError('无效的分块位置')
        item['time'] = time.monotonic()
        data = item['data'][offset:offset + CHUNK_SIZE]
        return {'data': base64.b64encode(data).decode('ascii'), 'next': offset + len(data), 'done': offset + len(data) >= len(item['data'])}

    def release(self, token):
        self.transfers.pop(token, None)
        self.uploads.pop(token, None)
        return {'ok': True}

    def upload(self, token, chunk, offset):
        self.cleanup()
        if not token:
            if len(self.uploads) >= 8:
                raise ValueError('上传任务过多')
            token = secrets.token_urlsafe(24)
            self.uploads[token] = {'data': bytearray(), 'time': time.monotonic()}
        item = self.uploads.get(token)
        if item is None or type(offset) is not int or offset != len(item['data']):
            raise ValueError('上传位置不一致，请重新上传')
        if len(chunk) > 32000:
            raise ValueError('上传分块过大')
        data = base64.b64decode(chunk, validate=True)
        if len(item['data']) + len(data) > MAX_UPLOAD:
            self.uploads.pop(token)
            raise ValueError('导入数据超过 4 MiB 限制')
        item['data'].extend(data)
        item['time'] = time.monotonic()
        return {'token': token, 'offset': len(item['data'])}

    async def dispatch(self, endpoint, method='GET', payload=None):
        self.cleanup()
        if not isinstance(payload, dict):
            raise ValueError('请求参数必须是对象')
        if endpoint == 'page/test/stream':
            raise ValueError('请通过测试任务接口启动批量测试')
        for pattern, handler, methods in self.routes:
            match = pattern.fullmatch(endpoint)
            if match and method in methods:
                context = current_request.set(Request(method, payload if method == 'GET' else {}, payload))
                try:
                    result = await handler(**match.groupdict())
                    return self.pack(result)
                finally:
                    current_request.reset(context)
        raise ValueError('未知的页面操作')

    async def commit(self, token, endpoint):
        item = self.uploads.pop(token, None)
        if item is None:
            raise ValueError('上传已过期')
        data = json.loads(bytes(item['data']).decode('utf-8-sig'))
        if not isinstance(data, dict) or not re.fullmatch(r'page/[a-zA-Z0-9_/-]+', endpoint):
            raise ValueError('无效的导入请求')
        method = str(data.pop('_method', 'POST')).upper()
        if method not in {'POST', 'PUT', 'DELETE'}:
            raise ValueError('无效的写入方法')
        return await self.dispatch(endpoint, method, data)

    async def site_test_events(self, params):
        names = params.get('names', [])
        if not isinstance(names, list) or any(not isinstance(name, str) for name in names):
            raise ValueError('站点列表必须为名称数组')
        selected = set(names)
        sites = [copy.deepcopy(site) for site in self.core.site_mgr.entries if not selected or site.name in selected]
        if selected - {site.name for site in sites}:
            raise ValueError('部分站点不存在，请刷新后重试')
        api_by_site = {site.name: [] for site in sites}
        for api in self.core.api_mgr.entries:
            owner = self.core.site_mgr.match_entry(api.url, only_enabled=False)
            if owner and owner.name in api_by_site:
                api_by_site[owner.name].append(self.core.api_test_service._with_runtime_test_defaults(api))
        yield {'event': 'start', 'total': len(sites)}
        for index, site in enumerate(sites):
            apis = api_by_site[site.name]
            success, failed = 0, 0
            reasons = []
            for offset, api in enumerate(apis):
                result = await self.core.remote.get_data(api)
                if result.is_valid():
                    success += 1
                else:
                    failed += 1
                    if len(reasons) < 3:
                        reasons.append(f'{api.name}: {self.core.remote._build_test_reason(result)}')
                yield {'event': 'site_progress', 'name': site.name, 'completed_apis': offset + 1,
                       'total_apis': len(apis), 'success': success, 'failed': failed}
            reachable = success > 0
            if not apis:
                result = await self.core.remote._request(site.url, headers=site.get_headers(), params=site.get_keys(), timeout=site.timeout)
                reachable = result.is_valid()
                if not reachable:
                    reasons.append(self.core.remote._build_test_reason(result))
            yield {'event': 'site_result', 'name': site.name, 'url': site.url, 'total_apis': len(apis),
                   'success': success, 'failed': failed, 'reachable': reachable, 'reason': '\n'.join(reasons),
                   'completed': index + 1, 'total': len(sites)}
        yield {'event': 'done', 'completed': len(sites), 'total': len(sites)}

    def start_test(self, params, site_mode=False):
        self.cleanup()
        if sum(not job['task'].done() for job in self.jobs.values()) >= 2:
            raise ValueError('已有两个测试任务，请先停止或等待完成')
        token = secrets.token_urlsafe(24)
        job = {'events': [], 'time': time.monotonic(), 'done': False}
        self.jobs[token] = job

        async def run():
            try:
                values = lambda name: params.get(name, []) if isinstance(params.get(name, []), list) else [params[name]]
                names = values('name')
                sites = values('site') + str(params.get('sites', '')).split(',')
                events = self.site_test_events(params) if site_mode else self.core.api_test_service.stream_test_apis(names=names, site_names=sites, query=str(params.get('query', '')))
                async for event in events:
                    job['events'].append(event)
                    job['time'] = time.monotonic()
                    if len(job['events']) > 10000:
                        raise ValueError('测试事件过多，请缩小测试范围')
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                job['events'].append({'event': 'error', 'message': str(exc)})
            finally:
                job['done'] = True
                job['time'] = time.monotonic()
        job['task'] = asyncio.create_task(run())
        return {'token': token}

    def poll(self, token, cursor):
        self.cleanup()
        job = self.jobs.get(token)
        if job is None or type(cursor) is not int or cursor < 0:
            raise ValueError('测试任务不存在，请重新开始')
        # Bound each response, including when a site returns a long error message.
        events = []
        size = 0
        for event in job['events'][cursor:cursor + 50]:
            serialized = json.dumps(event, ensure_ascii=False)
            if events and size + len(serialized.encode()) > 24000:
                break
            events.append(event)
            size += len(serialized.encode())
        next_cursor = cursor + len(events)
        return self.pack({'events': events, 'cursor': next_cursor, 'done': job['done'] and next_cursor >= len(job['events'])})

    async def cancel_test(self, token):
        job = self.jobs.pop(token, None)
        if job is not None:
            job['task'].cancel()
            await asyncio.gather(job['task'], return_exceptions=True)
        return {'ok': True}

    async def close(self):
        for token in list(self.jobs):
            await self.cancel_test(token)
        self.transfers.clear()
        self.uploads.clear()
