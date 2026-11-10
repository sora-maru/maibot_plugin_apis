/* Selection is restricted to the current filter and survives pagination/sorting. */
const PoolSelection = (() => {
  const selected = {site:new Set(), api:new Set()};
  const visible = {site:[], api:[]};
  let busy = false;
  let pending = null;
  const label = kind => kind === 'site' ? '站点' : 'API';
  const table = kind => document.getElementById(kind + 'Table');
  function sync(kind) {
    const filteredRows = kind === 'site'
      ? PageHelpers.filterSites(state.sites, siteSearchText)
      : filterApisByType(filterApisBySite(PageHelpers.filterApis(state.apis, apiSearchText)));
    const filtered = new Set(filteredRows.map(row=>row.name));
    for (const name of selected[kind]) if (!filtered.has(name)) selected[kind].delete(name);
    const header = table(kind)?.querySelector('[data-select-page]');
    const count = visible[kind].filter(name=>selected[kind].has(name)).length;
    if(header) {
      header.checked = visible[kind].length > 0 && count === visible[kind].length;
      header.indeterminate = count > 0 && count < visible[kind].length;
      header.disabled = busy || !visible[kind].length;
    }
    table(kind)?.querySelectorAll('[data-select-row]').forEach(input=>{
      input.checked = selected[kind].has(input.dataset.selectRow);
      input.disabled = busy;
      input.closest('tr').classList.toggle('is-selected-row',input.checked);
    });
    const bar = document.getElementById(kind + 'BulkActions');
    if(!bar) return;
    bar.querySelector('[data-selection-count]').textContent = `已选 ${selected[kind].size} 项`;
    bar.querySelectorAll('[data-bulk-action]').forEach(button=>{button.disabled=busy || !selected[kind].size;});
  }
  function rendered(kind, names) { visible[kind]=names;sync(kind); }
  function row(kind, name, checked) {
    if(checked) selected[kind].add(name);else selected[kind].delete(name);
    sync(kind);
  }
  function page(kind, checked) { for(const name of visible[kind]) row(kind,name,checked);sync(kind); }
  function clear(kind) { selected[kind].clear();sync(kind); }
  function setBusy(value) {busy=value;sync('site');sync('api');}
  async function enable(kind, enabled) {
    if(busy || !selected[kind].size) return;
    const names=[...selected[kind]];
    setBusy(true);
    try {
      await req(`/api/${kind}/batch`,{method:'PUT',body:JSON.stringify({items:names.map(name=>({name,payload:{enabled}}))})});
      await loadPool({includeLocalData:false});
      showNoticeModal(`已${enabled?'启用':'禁用'} ${names.length} 个${label(kind)}${kind==='site'?'及其关联 API':''}。`,'success');
    } catch(error) {showNoticeModal(error.message);}
    finally {setBusy(false);}
  }
  function remove(kind) {
    if(busy || !selected[kind].size) return;
    const names=[...selected[kind]];
    pending={kind,names};
    const apiCount=kind==='site' ? state.apis.filter(api=>names.includes(resolveApiSiteName(api))).length : names.length;
    document.getElementById('bulkDeleteSummary').textContent=kind==='site'
      ? `确认删除 ${names.length} 个站点及其当前关联的 ${apiCount} 个 API？本地缓存保留。`
      : `确认删除 ${names.length} 个 API？本地缓存和站点保留。`;
    document.getElementById('bulkDeleteNames').textContent=names.join('\n');
    document.getElementById('bulkDeleteModal').classList.add('open');
  }
  function close() {if(busy)return;pending=null;document.getElementById('bulkDeleteModal').classList.remove('open');}
  async function confirm() {
    if(busy || !pending) return;
    const {kind,names}=pending;
    setBusy(true);
    document.getElementById('bulkDeleteConfirm').disabled=true;
    try {
      const result=await req(`/api/${kind}/batch`,{method:'DELETE',body:JSON.stringify({names})});
      clear(kind);
      // Discard obsolete single-row pending-delete indicators after refreshing.
      clearPendingDeleteSelection();
      await loadPool({includeLocalData:false});
      document.getElementById('bulkDeleteModal').classList.remove('open');pending=null;
      const failed=result.failed?.length || 0;
      showNoticeModal(`已删除 ${result.deleted?.length || 0} 个${label(kind)}${kind==='site' ? `、${result.deleted_apis?.length || 0} 个关联 API` : ''}。${failed?`另有 ${failed} 项未删除，请刷新检查。`:''}`,'success');
    } catch(error) {showNoticeModal(error.message);}
    finally {setBusy(false);document.getElementById('bulkDeleteConfirm').disabled=false;}
  }
  return {rendered,row,page,clear,enable,remove,close,confirm};
})();
