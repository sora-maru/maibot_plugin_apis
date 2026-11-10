/* Site health tests report observed failures; deletion always requires confirmation. */
(() => {
  let token = '', timer = null, cursor = 0, polling = false;
  const rows = new Map();
  const selected = new Set();
  const $ = id => document.getElementById(id);
  const escape = value => escapeHtml(String(value ?? ''));
  const rpc = async (kind, name, args = {}) => {
    // Use the same serial request queue as the other dashboard operations.
    return window.ApisPage.call(kind, name, args);
  };
  const tell = text => { $('siteTestSummary').textContent = text; };

  function render() {
    $('siteTestRows').innerHTML = [...rows.values()].map(row => {
      const label = row.pending ? '等待测试' : row.testing ? `测试中 ${row.completed_apis}/${row.total_apis}` :
        row.reachable ? '有可用响应' : '本次全部失败，待确认';
      return `<tr><td><input type="checkbox" aria-label="选择站点 ${escape(row.name)}" data-site-select="${escape(row.name)}" ${selected.has(row.name) ? 'checked' : ''}></td>
        <td>${escape(row.name)}</td><td>${escape(label)}</td><td>${row.success || 0} / ${row.failed || 0}</td>
        <td>${row.total_apis || 0}</td><td class="site-test-reason">${escape(row.reason || row.url)}</td></tr>`;
    }).join('');
    $('siteDeleteSelected').disabled = Boolean(token) || selected.size === 0;
    $('siteSelectFailed').disabled = Boolean(token);
  }

  async function cancel() {
    clearTimeout(timer);
    const current = token;
    token = '';
    if (current) await rpc('action', 'test_cancel', {token: current});
    $('siteTestStop').disabled = true;
    render();
  }

  async function poll(current) {
    if (!current || current !== token || polling) return;
    polling = true;
    try {
      const result = await window.ApisPage.decode(await rpc('query','test_poll',{token:current,cursor}));
      if (current !== token) return;
      cursor = result.cursor;
      for (const event of result.events) {
        if (event.event === 'site_progress') {
          rows.set(event.name, {...rows.get(event.name), ...event, pending:false, testing:true});
          tell(`正在测试 ${event.name}：${event.completed_apis}/${event.total_apis} 个 API`);
        } else if (event.event === 'site_result') {
          rows.set(event.name, {...event, pending:false, testing:false});
          tell(`已完成 ${event.completed}/${event.total} 个站点`);
        } else if (event.event === 'error') throw new Error(event.message);
      }
      render();
      if (result.done) {
        const failed = [...rows.values()].filter(row=>!row.pending && !row.reachable).length;
        tell(`测试完成：${rows.size} 个站点，${failed} 个站点本次无可用响应。失败不等同于关站，请核实后选择删除。`);
        await cancel();
      } else timer = setTimeout(()=>poll(current),500);
    } catch(error) {
      tell(`站点测试失败：${error.message}`);
      await cancel().catch(()=>{});
    } finally { polling = false; }
  }

  async function start(names) {
    $('siteTestModal').classList.add('open');
    if (token) {tell('已有站点测试正在运行，可先停止后重新测试。'); return;}
    rows.clear(); selected.clear(); cursor = 0;
    $('siteDeleteConfirmation').hidden = true;
    for(const site of state.sites.filter(site=>names.includes(site.name))) rows.set(site.name,{...site,pending:true});
    if(!rows.size) {tell('当前没有可测试的站点。');render();return;}
    tell('正在启动站点测试……'); render();
    $('siteBatchTestStart').disabled = true;
    try {
      token = (await rpc('action','site_test_start',{payload:JSON.stringify({names:[...rows.keys()]})})).token;
      $('siteTestStop').disabled = false;
      timer = setTimeout(()=>poll(token),50);
    } catch(error) {tell(error.message);}
    finally {$('siteBatchTestStart').disabled = false;render();}
  }

  window.testSites = names => start(names || getDisplayedSiteRows().map(site=>site.name));
  window.testOneSite = name => start([decodeURIComponent(name)]);
  $('siteTestRows').addEventListener('change',event=>{
    const name = event.target.dataset.siteSelect;
    if(!name) return;
    if(event.target.checked) selected.add(name); else selected.delete(name);
    $('siteDeleteConfirmation').hidden = true;
    render();
  });
  $('siteSelectFailed').onclick = () => {
    selected.clear();
    for(const row of rows.values()) if(!row.pending && !row.testing && !row.reachable) selected.add(row.name);
    $('siteDeleteConfirmation').hidden = true;
    render();
  };
  $('siteDeleteSelected').onclick = () => {
    $('siteDeleteConfirmation').hidden = false;
    const count = state.apis.filter(api=>selected.has(api.site)).length;
    $('siteDeleteDetails').textContent = `确认删除 ${selected.size} 个站点及其关联的 ${count} 个 API？站点：${[...selected].join('、')}。本地缓存保留。`;
  };
  $('siteCancelDelete').onclick = () => { $('siteDeleteConfirmation').hidden = true; };
  $('siteConfirmDelete').onclick = async () => {
    if(token || !selected.size) return;
    $('siteConfirmDelete').disabled = true;
    try {
      const result = await req('/api/site/batch',{method:'DELETE',body:JSON.stringify({names:[...selected]})});
      for(const name of result.deleted) rows.delete(name);
      selected.clear();
      $('siteDeleteConfirmation').hidden = true;
      tell(`已删除 ${result.deleted.length} 个站点及 ${result.deleted_apis.length} 个关联 API。`);
      await loadPool({includeLocalData:false}); render();
    } catch(error) {tell(`删除失败：${error.message}`);}
    finally { $('siteConfirmDelete').disabled = false; }
  };
  $('siteTestStop').onclick = () => cancel().then(()=>tell('站点测试已停止。')).catch(error=>tell(error.message));
  const close = () => { $('siteTestModal').classList.remove('open'); };
  $('siteTestClose').onclick = close;
  $('siteTestModal').onclick = event => {if(event.target.id==='siteTestModal') close();};
})();
