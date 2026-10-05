(function(){
  function closePromptViewer(){
    const viewer = document.getElementById('promptViewer');
    if (!viewer) return;
    viewer.classList.add('hidden');
    viewer.setAttribute('aria-hidden', 'true');
  }

  function closePromptModal(){
    const modal = document.querySelector('.prompt-modal, #promptModal, [data-prompt-modal]');
    if (modal) {
      modal.classList.remove('show','active','open');
      modal.style.display = 'none';
    }
    document.body.classList.remove('modal-open');
  }

  function copyPromptFromModal(button){
    const modal = button.closest('.prompt-modal, #promptModal, [data-prompt-modal]') || document;
    const source = modal.querySelector('textarea, .prompt-text, .prompt-content, [data-prompt-text]');
    const text = source ? (source.value !== undefined ? source.value : source.textContent) : '';
    if (!text.trim()) return;

    navigator.clipboard.writeText(text.trim()).then(function(){
      const original = button.textContent;
      button.textContent = '✓ COPIADO';
      setTimeout(function(){ button.textContent = original; }, 1400);
    }).catch(function(){
      const ta = document.createElement('textarea');
      ta.value = text.trim();
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      ta.remove();
      const original = button.textContent;
      button.textContent = '✓ COPIADO';
      setTimeout(function(){ button.textContent = original; }, 1400);
    });
  }

  document.addEventListener('click', function(e){
    const viewerClose = e.target.closest('#promptViewerClose, #promptViewer .prompt-close');
    if (viewerClose) {
      e.preventDefault();
      e.stopPropagation();
      closePromptViewer();
      return;
    }

    const close = e.target.closest('.prompt-modal .prompt-close, #promptModal .prompt-close, [data-prompt-modal] .prompt-close, .prompt-modal [aria-label="Fechar"], #promptModal [aria-label="Fechar"]');
    if (close) {
      e.preventDefault();
      e.stopPropagation();
      closePromptModal();
      return;
    }

    const copy = e.target.closest('.prompt-modal .prompt-copy, #promptModal .prompt-copy, [data-prompt-modal] .prompt-copy');
    if (copy) {
      e.preventDefault();
      e.stopPropagation();
      copyPromptFromModal(copy);
    }
  }, true);

  document.addEventListener('keydown', function(e){
    if (e.key === 'Escape') {
      closePromptViewer();
      closePromptModal();
    }
  });
})();
