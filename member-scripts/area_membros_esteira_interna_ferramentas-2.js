/* Proteção básica de interface: dificulta inspeção casual.
   Observação: HTML/JS no navegador nunca pode impedir DevTools de forma absoluta. */
(function(){
  const block = (e) => e.preventDefault();

  document.addEventListener('contextmenu', block, {capture:true});
  document.addEventListener('dragstart', block, {capture:true});

  document.addEventListener('keydown', function(e){
    const k = String(e.key || '').toLowerCase();

    // F12
    if (k === 'f12') { e.preventDefault(); e.stopPropagation(); return false; }

    // Ctrl/Cmd + U
    if ((e.ctrlKey || e.metaKey) && k === 'u') {
      e.preventDefault(); e.stopPropagation(); return false;
    }

    // Ctrl/Cmd + Shift + I/J/C (DevTools)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && ['i','j','c'].includes(k)) {
      e.preventDefault(); e.stopPropagation(); return false;
    }

    // Ctrl/Cmd + Shift + K (console em alguns navegadores)
    if ((e.ctrlKey || e.metaKey) && e.shiftKey && k === 'k') {
      e.preventDefault(); e.stopPropagation(); return false;
    }
  }, {capture:true});

  // Bloqueia seleção de texto acidental em áreas de interface.
  document.addEventListener('selectstart', function(e){
    if (!(e.target instanceof Element) || !e.target.closest('input, textarea, video, #promptViewerContent')) e.preventDefault();
  }, {capture:true});
})();
