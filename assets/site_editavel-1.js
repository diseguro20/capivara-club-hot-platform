const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.getElementById('dots');
    const current = document.getElementById('current');
    const total = document.getElementById('total');

    const accessModal = document.getElementById('accessModal');
    const accessForm = document.getElementById('accessForm');
    const accessStatus = document.getElementById('accessStatus');
    const couponInput = document.getElementById('accessCoupon');
    const couponParams = new URLSearchParams(window.location.search);
    const linkedCoupon = (couponParams.get('cupom') || couponParams.get('coupon') || '').trim().toUpperCase();
    if (couponInput && /^[A-Z0-9_-]{1,40}$/.test(linkedCoupon)) {
      couponInput.value = linkedCoupon;
      document.getElementById('accessCouponHelp').textContent = 'Cupom preenchido pelo link. O desconto será validado ao gerar o PIX.';
    }


    const accessTermsBox = document.getElementById('accessTermsBox');
    const accessTermsToggle = document.getElementById('accessTermsToggle');
    const accessTermsToggleLabel = document.getElementById('accessTermsToggleLabel');
    const accessTermsCheckLabel = document.getElementById('accessTermsCheckLabel');
    const accessTermsInput = document.getElementById('accessTerms');
    const accessSubmitBtn = document.getElementById('accessSubmitBtn');

    function resetAccessTermsGate() {
      accessTermsBox.classList.remove('open');
      accessTermsToggleLabel.textContent = 'Abrir e ler ▾';
      accessTermsInput.checked = false;
      accessTermsInput.disabled = true;
      accessTermsCheckLabel.classList.add('disabled');
      accessSubmitBtn.disabled = true;
    }

    accessTermsToggle.addEventListener('click', () => {
      const isOpen = accessTermsBox.classList.toggle('open');
      accessTermsToggleLabel.textContent = isOpen ? 'Termos lidos ✓' : 'Abrir e ler ▾';
      if (isOpen) {
        accessTermsInput.disabled = false;
        accessTermsCheckLabel.classList.remove('disabled');
      }
    });

    accessTermsInput.addEventListener('change', () => {
      accessSubmitBtn.disabled = !accessTermsInput.checked;
    });

    resetAccessTermsGate();

    function closeAccessModal() {
      accessModal.classList.remove('show');
      accessModal.setAttribute('aria-hidden', 'true');
    }

    document.querySelectorAll('.access-trigger').forEach(trigger => {
      trigger.addEventListener('click', event => {
        event.preventDefault();
        resetAccessTermsGate();
        accessModal.classList.add('show');
        accessModal.setAttribute('aria-hidden', 'false');
        document.getElementById('accessName').focus();
      });
    });

    document.getElementById('accessClose').addEventListener('click', closeAccessModal);
    accessModal.addEventListener('click', event => {
      if (event.target === accessModal) closeAccessModal();
    });

    let paymentPollTimer = null;

    function pollPaymentStatus(idTransaction) {
      clearInterval(paymentPollTimer);
      paymentPollTimer = setInterval(async () => {
        try {
          const response = await fetch(`/api/order-status?idTransaction=${encodeURIComponent(idTransaction)}`);
          const result = await response.json();
          if (response.ok && result.status === 'paid') {
            clearInterval(paymentPollTimer);
            accessStatus.textContent = 'Pagamento confirmado! Enviamos a senha para seu e-mail. Redirecionando para a área de membros...';
            setTimeout(() => {
              window.location.href = '/membros';
            }, 2000);
          }
        } catch {
          // ignora falhas de rede pontuais e tenta novamente no próximo ciclo
        }
      }, 5000);
    }

    const nicknameInput = document.getElementById('accessNickname');
    const nicknameStatus = document.getElementById('nicknameStatus');
    let nicknameAvailable = null;
    let nicknameCheckTimer = null;

    nicknameInput.addEventListener('input', () => {
      const value = nicknameInput.value.trim();
      nicknameAvailable = null;
      clearTimeout(nicknameCheckTimer);
      if (!value) {
        nicknameStatus.textContent = '';
        nicknameStatus.className = 'nickname-status';
        return;
      }
      nicknameStatus.textContent = 'Verificando disponibilidade...';
      nicknameStatus.className = 'nickname-status checking';
      nicknameCheckTimer = setTimeout(async () => {
        try {
          const response = await fetch(`/api/check-nickname?nickname=${encodeURIComponent(value)}`);
          const result = await response.json();
          nicknameAvailable = !!result.available;
          nicknameStatus.textContent = nicknameAvailable ? 'Apelido disponível ✓' : 'Esse apelido já está em uso.';
          nicknameStatus.className = `nickname-status ${nicknameAvailable ? 'available' : 'taken'}`;
        } catch {
          nicknameStatus.textContent = '';
          nicknameStatus.className = 'nickname-status';
        }
      }, 450);
    });

    accessForm.addEventListener('submit', event => {
      event.preventDefault();
      if (nicknameAvailable === false) {
        nicknameInput.focus();
        return;
      }
      const submitButton = accessForm.querySelector('.access-submit');
      const data = Object.fromEntries(new FormData(accessForm));
      const refParam = new URLSearchParams(window.location.search).get('ref');
      if (refParam) data.ref = refParam;
      submitButton.disabled = true;
      submitButton.textContent = 'GERANDO PIX...';
      fetch('/api/access-request', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.content || ''
        },
        body: JSON.stringify(data)
      }).then(async response => {
        const responseText = await response.text();
        let result;
        try {
          result = JSON.parse(responseText);
        } catch {
          throw new Error('Não foi possível concluir a solicitação agora. Atualize a página e tente novamente.');
        }
        if (!response.ok) throw new Error(result.error || 'Não foi possível gerar a cobrança.');
        document.getElementById('pixQr').src = result.paymentCodeBase64.startsWith('data:') ? result.paymentCodeBase64 : `data:image/png;base64,${result.paymentCodeBase64}`;
        document.getElementById('pixCode').value = result.paymentCode;
        document.getElementById('pixResult').classList.add('show');
        document.getElementById('accessFields').style.display = 'none';
        accessStatus.textContent = 'PIX gerado: ' + new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'}).format(result.amount) + (result.discountPercent ? ' — desconto de ' + result.discountPercent + '% aplicado.' : '.') + ' Após a confirmação do pagamento, o acesso será liberado.';
        accessStatus.classList.add('show');
        submitButton.textContent = 'PIX GERADO';
        pollPaymentStatus(result.idTransaction);
      }).catch(error => {
        accessStatus.textContent = error.message;
        accessStatus.classList.add('show');
        submitButton.disabled = false;
        submitButton.textContent = 'SOLICITAR ACESSO';
      });
    });

    document.getElementById('pixCopy').addEventListener('click', async () => {
      await navigator.clipboard.writeText(document.getElementById('pixCode').value);
      document.getElementById('pixCopy').textContent = 'PIX COPIADO';
      setTimeout(() => { document.getElementById('pixCopy').textContent = 'COPIAR PIX'; }, 1400);
    });

    let index = 0;
    total.textContent = String(slides.length).padStart(2, '0');

    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.className = 'dot' + (i === 0 ? ' active' : '');
      dot.onclick = () => showSlide(i);
      dotsContainer.appendChild(dot);
    });

    function showSlide(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach((slide, n) => {
        slide.classList.toggle('active', n === index);
        slide.querySelector('img').src = slide.dataset.clothed;
      });

      document.querySelectorAll('.dot').forEach((dot, n) => {
        dot.classList.toggle('active', n === index);
      });

      current.textContent = String(index + 1).padStart(2, '0');
    }

    function changeSlide(direction) {
      showSlide(index + direction);
    }

    document.addEventListener('contextmenu', event => event.preventDefault());
    document.addEventListener('dragstart', event => event.preventDefault());
    document.addEventListener('selectstart', event => event.preventDefault());
    document.addEventListener('keydown', event => {
      const key = event.key.toLowerCase();
      const blockedShortcut = (event.ctrlKey || event.metaKey) &&
        (key === 'u' || (event.shiftKey && ['i', 'j', 'c'].includes(key)));

      if (event.key === 'F12' || blockedShortcut) {
        event.preventDefault();
        event.stopPropagation();
      }
    });

    // Troca automática a cada 5 segundos
    setInterval(() => changeSlide(1), 5000);
