/* MaiBot authenticated page transport. The existing dashboard uses this facade. */
(() => {
  const active = new Map();
  let queue = Promise.resolve();
  function call(kind, name, args) {
    const result = queue.then(() => maibot[kind](name, args));
    queue = result.catch(() => {});
    return result;
  }
  const query = (name, args) => call('query', name, args);
  const action = (name, args) => call('action', name, args);
  const normalize = value => String(value).replace(/^\/api\//, 'page/').replace(/^\//, '');
  const bytes64 = bytes => {
    let text = '';
    for (const byte of bytes) text += String.fromCharCode(byte);
    return btoa(text);
  };
  async function decode(result, binary = false) {
    if (!result || !result.__transfer) return result;
    const chunks = [];
    let offset = 0;
    try {
      while (offset < result.size) {
        const part = await query('chunk', {token: result.__transfer, offset});
        const text = atob(part.data);
        chunks.push(Uint8Array.from(text, ch => ch.charCodeAt(0)));
        if (part.next <= offset) throw new Error('文件传输未完成，请重试');
        offset = part.next;
      }
      const blob = new Blob(chunks, {type: result.content_type});
      if (binary) return {blob, filename: result.filename};
      const text = await blob.text();
      return result.content_type === 'application/x-apis-json' ? JSON.parse(text) : text;
    } finally {
      await action('release', {token: result.__transfer}).catch(() => {});
    }
  }
  async function write(endpoint, payload) {
    const serialized = JSON.stringify(payload || {});
    const bytes = new TextEncoder().encode(serialized);
    if (bytes.length < 28000) {
      return decode(await action('write', {endpoint: normalize(endpoint), payload: serialized}));
    }
    let token = '', offset = 0;
    try {
      while (offset < bytes.length) {
        const chunk = bytes.slice(offset, offset + 22000);
        const result = await action('upload', {token, chunk: bytes64(chunk), offset});
        token = result.token;
        offset = result.offset;
      }
      return decode(await action('commit', {endpoint: normalize(endpoint), token}));
    } finally {
      if (token) await action('release', {token}).catch(() => {});
    }
  }
  window.ApisPage = {
    call, decode,
    ready: async () => { await maibot.ready; },
    getContext: () => ({...maibot.context, locale: maibot.context?.language || 'zh-CN'}),
    getLocale: () => maibot.context?.language || 'zh-CN',
    onContext: callback => window.addEventListener('maibot:context', () => callback(window.ApisPage.getContext())),
    apiGet: async (endpoint, params = {}) => decode(await query('read', {endpoint: normalize(endpoint), payload: JSON.stringify(params)})),
    apiPost: write,
    upload: async (endpoint, file) => {
      if (file.size > 3 * 1024 * 1024) throw new Error('导入文件请小于 3 MiB');
      // Validate JSON before transmitting; the controller imports UTF-8 text.
      const content = (await file.text()).replace(/^\uFEFF/, '');
      JSON.parse(content);
      const response = await write(endpoint, {content});
      return unwrapBridgeResponse(response);
    },
    download: async (endpoint, params = {}, filename = '') => {
      const raw = await query('read', {endpoint: normalize(endpoint), payload: JSON.stringify(params)});
      const {blob, filename: suggested} = await decode(raw, true);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url; a.download = filename || suggested || 'api_pool.json';
      a.click(); setTimeout(() => URL.revokeObjectURL(url), 30000);
    },
    subscribeSSE: async (endpoint, handlers, params) => {
      if (normalize(endpoint) !== 'page/test/stream') throw new Error('未知测试接口');
      const {token} = await action('test_start', {payload: JSON.stringify(params || {})});
      const state = {stopped: false, timer: null, cursor: 0};
      active.set(token, state);
      const poll = async () => {
        if (state.stopped) return;
        try {
          const response = await decode(await query('test_poll', {token, cursor: state.cursor}));
          if (state.stopped) return;
          for (const parsed of response.events) handlers.onMessage?.({parsed});
          state.cursor = response.cursor;
          if (response.done) {
            active.delete(token);
            await action('test_cancel', {token});
          } else if (!state.stopped) state.timer = setTimeout(poll, 500);
        } catch (error) {
          if (!state.stopped) handlers.onError?.(error);
          await window.ApisPage.unsubscribeSSE(token);
        }
      };
      // Allow callers to bind cancellation before the first event is delivered.
      state.timer = setTimeout(poll, 50);
      return token;
    },
    unsubscribeSSE: async token => {
      const state = active.get(token);
      if (state) {state.stopped = true; clearTimeout(state.timer); active.delete(token);}
      await action('test_cancel', {token});
    }
  };
})();
