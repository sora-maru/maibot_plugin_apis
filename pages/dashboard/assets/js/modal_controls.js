/* Every dialog has a visible close control independent of its scrollable body. */
(() => {
  function close(modal) {
    const button = modal.querySelector('button[onclick^="close"], #siteTestClose, #defaultsClose, #bulkDeleteClose');
    if (button) button.click();
    else modal.classList.remove('open');
  }
  for (const modal of document.querySelectorAll('.modal')) {
    const dialog = modal.querySelector('.dialog');
    if (!dialog) continue;
    dialog.setAttribute('role','dialog');
    dialog.setAttribute('aria-modal','true');
    const button = document.createElement('button');
    button.type = 'button'; button.className = 'dialog-close';
    button.textContent = '×'; button.title = '关闭';
    button.setAttribute('aria-label','关闭弹窗');
    button.onclick = () => close(modal);
    dialog.append(button);
    modal.addEventListener('click',event=>{if(event.target===modal) close(modal);});
  }
  document.addEventListener('keydown',event=>{
    if(event.key!=='Escape') return;
    const open = [...document.querySelectorAll('.modal.open')];
    if(open.length) {event.preventDefault(); close(open[open.length-1]);}
  });
})();
