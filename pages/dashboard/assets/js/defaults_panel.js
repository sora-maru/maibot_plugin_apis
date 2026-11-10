(() => {
  const $=id=>document.getElementById(id);
  let info=null;
  window.openDefaultReplacement=async()=>{
    $('defaultsModal').classList.add('open');
    $('defaultsConfirm').disabled=true;
    $('defaultsSummary').textContent='正在读取内置默认数据……';
    $('defaultsResult').textContent='';
    try {
      info=await ApisPage.call('query','defaults_info',{});
      $('defaultsSummary').textContent=`当前 ${info.current_sites} 个站点、${info.current_apis} 个 API；将替换为内置 ${info.sites} 个站点、${info.apis} 个 API（其中 ${info.disabled_apis} 个默认停用，需密钥、维护或额外配置）。采集日期：${info.collected_at || '随当前版本'}。`;
      $('defaultsConfirm').disabled=false;
    } catch(error) {$('defaultsResult').textContent=error.message;}
  };
  $('defaultsConfirm').onclick=async()=>{
    if(!info) return;
    $('defaultsConfirm').disabled=true;
    $('defaultsResult').textContent='正在备份并替换……';
    try {
      const result=await ApisPage.call('action','defaults_replace',{fingerprint:info.fingerprint});
      $('defaultsResult').textContent=`已替换为 ${result.sites} 个站点、${result.apis} 个 API。备份位置：${result.backup_dir}\n${result.backup_site_file}\n${result.backup_api_file}`;
      clearPendingDeleteSelection();
      apiSiteFilterInitialized=false;apiTypeFilterInitialized=false;
      siteSearchText='';apiSearchText='';
      $('siteSearch').value='';$('apiSearch').value='';
      await loadPool();
      info=null;
    } catch(error) {$('defaultsResult').textContent=`替换失败：${error.message}`;$('defaultsConfirm').disabled=false;}
  };
  $('defaultsClose').onclick=()=>{$('defaultsModal').classList.remove('open');};
})();
