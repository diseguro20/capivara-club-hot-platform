// Feedback visual sem bloquear o download nativo do navegador.
document.querySelectorAll('.workflow-download').forEach(function(link){
  link.addEventListener('click', function(event){
    if (link.closest('.workflow-lockable.workflow-locked')) {
      event.preventDefault();
      return;
    }
    const original = link.textContent;
    link.textContent = 'Baixando...';
    setTimeout(function(){ link.textContent = original; }, 1200);
  });
});
