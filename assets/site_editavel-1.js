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
    const accessPhoneInput = document.getElementById('accessPhone');
    const accessCpfInput = document.getElementById('accessCpf');

    // Live mask for phone
    if (accessPhoneInput) {
      accessPhoneInput.addEventListener('input', (e) => {
        let val = e.target.value.replace(/\D/g, '').substring(0, 11);
        if (val.length > 10) {
          e.target.value = `(${val.substring(0,2)}) ${val.substring(2,7)}-${val.substring(7)}`;
        } else if (val.length > 6) {
          e.target.value = `(${val.substring(0,2)}) ${val.substring(2,6)}-${val.substring(6)}`;
        } else if (val.length > 2) {
          e.target.value = `(${val.substring(0,2)}) ${val.substring(2)}`;
        } else if (val.length > 0) {
          e.target.value = `(${val}`;
        }
      });
    }

    // Live mask for CPF
    if (accessCpfInput) {
      accessCpfInput.addEventListener('input', (e) => {
        let val = e.target.value.replace(/\D/g, '').substring(0, 11);
        if (val.length > 9) {
          e.target.value = `${val.substring(0,3)}.${val.substring(3,6)}.${val.substring(6,9)}-${val.substring(9)}`;
        } else if (val.length > 6) {
          e.target.value = `${val.substring(0,3)}.${val.substring(3,6)}.${val.substring(6)}`;
        } else if (val.length > 3) {
          e.target.value = `${val.substring(0,3)}.${val.substring(3)}`;
        } else {
          e.target.value = val;
        }
      });
    }

    if (accessTermsToggle) {
      accessTermsToggle.addEventListener('click', () => {
        const isOpen = accessTermsBox.classList.toggle('open');
        accessTermsToggleLabel.textContent = isOpen ? 'Fechar termos ▴' : 'Abrir e ler ▾';
      });
    }

    if (accessTermsInput) {
      accessTermsInput.disabled = false;
      accessTermsInput.addEventListener('change', () => {
        if (accessSubmitBtn) accessSubmitBtn.disabled = !accessTermsInput.checked;
      });
    }
    if (accessSubmitBtn) accessSubmitBtn.disabled = false;

    function closeAccessModal() {
      accessModal.classList.remove('show');
      accessModal.setAttribute('aria-hidden', 'true');
    }

    function openAccessModal() {
      accessModal.classList.add('show');
      accessModal.setAttribute('aria-hidden', 'false');
      const firstInput = document.getElementById('accessName');
      if (firstInput) firstInput.focus();
    }

    function updateMembersButtonState() {
      const membersBtn = document.getElementById('headerMembersBtn');
      const membersIcon = document.getElementById('headerMembersIcon');
      const membersText = document.getElementById('headerMembersText');
      const buyLink = document.getElementById('headerBuyLink');
      if (!membersBtn) return;

      let isPaid = false;
      try {
        const u = JSON.parse(localStorage.getItem('capivara_user') || 'null');
        if (u && (u.paid || u.isAdmin || u.email === 'diseguro20@gmail.com')) isPaid = true;
      } catch(e) {}
      if (localStorage.getItem('memberPaid') === '1' || localStorage.getItem('memberEmail') === 'diseguro20@gmail.com') {
        isPaid = true;
      }

      if (isPaid) {
        membersBtn.classList.remove('locked');
        membersBtn.classList.add('unlocked');
        membersBtn.href = '/painel';
        membersBtn.title = 'Acesso Liberado! Clique para entrar';
        if (membersIcon) membersIcon.textContent = '✨';
        if (membersText) membersText.textContent = 'Área de Membros →';
        if (buyLink) buyLink.style.display = 'none';
      } else {
        membersBtn.classList.remove('unlocked');
        membersBtn.classList.add('locked');
        membersBtn.href = '#accessModal';
        membersBtn.title = 'Liberado somente após confirmação do pagamento via PIX';
        if (membersIcon) membersIcon.textContent = '🔒';
        if (membersText) membersText.textContent = 'Área de Membros';
        if (buyLink) buyLink.style.display = 'inline-block';
      }
    }

    updateMembersButtonState();

    const membersBtnEl = document.getElementById('headerMembersBtn');
    if (membersBtnEl) {
      membersBtnEl.addEventListener('click', (e) => {
        let isPaid = false;
        try {
          const u = JSON.parse(localStorage.getItem('capivara_user') || 'null');
          if (u && (u.paid || u.isAdmin || u.email === 'diseguro20@gmail.com')) isPaid = true;
        } catch(e) {}
        if (localStorage.getItem('memberPaid') === '1' || localStorage.getItem('memberEmail') === 'diseguro20@gmail.com') {
          isPaid = true;
        }

        if (!isPaid) {
          e.preventDefault();
          const notice = document.getElementById('accessStatus');
          if (notice) {
            notice.innerHTML = '<span style="color:#00f0ff;font-weight:bold;">🔒 A Área de Membros só é liberada após o pagamento. Complete seus dados para gerar o PIX:</span>';
            notice.classList.add('show');
          }
          openAccessModal();
        }
      });
    }

    document.querySelectorAll('.access-trigger').forEach(trigger => {
      trigger.addEventListener('click', event => {
        event.preventDefault();
        openAccessModal();
      });
    });

    // Auto-open modal if user arrived with ?checkout=true or #checkout
    if (window.location.search.includes('checkout') || window.location.hash.includes('access') || window.location.hash.includes('checkout')) {
      openAccessModal();
    }

    const closeBtn = document.getElementById('accessClose');
    if (closeBtn) closeBtn.addEventListener('click', closeAccessModal);
    accessModal.addEventListener('click', event => {
      if (event.target === accessModal) closeAccessModal();
    });

    let paymentPollTimer = null;

    function pollPaymentStatus(idTransaction, customerData) {
      clearInterval(paymentPollTimer);
      paymentPollTimer = setInterval(async () => {
        try {
          const response = await fetch(`/api/order-status?idTransaction=${encodeURIComponent(idTransaction)}`);
          const result = await response.json();
          if (response.ok && (result.status === 'paid' || result.paid)) {
            clearInterval(paymentPollTimer);
            const approvedEmail = result.email || (customerData && customerData.email);
            const approvedName = result.name || (customerData && customerData.name) || 'Membro';
            if (approvedEmail) {
              const userSession = {
                email: approvedEmail,
                name: approvedName,
                paid: true,
                paidAt: new Date().toISOString()
              };
              localStorage.setItem('capivara_user', JSON.stringify(userSession));
              localStorage.setItem('memberEmail', approvedEmail);
              localStorage.setItem('memberName', approvedName);
              localStorage.setItem('memberPaid', '1');
              updateMembersButtonState();
            }
            accessStatus.innerHTML = '<span style="color:#00f0ff;font-weight:800;font-size:15px;">🎉 Pagamento confirmado com sucesso! Liberando acesso...</span>';
            setTimeout(() => {
              window.location.href = result.redirect || '/painel?paid=true';
            }, 1200);
          }
        } catch {
          // ignora falhas pontuais e tenta novamente
        }
      }, 3500);
    }

    accessForm.addEventListener('submit', event => {
      event.preventDefault();
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
          'Accept': 'application/json'
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
        if (!response.ok || !result.ok) throw new Error(result.error || 'Não foi possível gerar a cobrança.');

        const qrImg = document.getElementById('pixQr');
        if (qrImg) {
          qrImg.src = result.paymentCodeBase64.startsWith('data:') 
            ? result.paymentCodeBase64 
            : (result.paymentCodeBase64.startsWith('http') ? result.paymentCodeBase64 : `data:image/png;base64,${result.paymentCodeBase64}`);
        }
        document.getElementById('pixCode').value = result.paymentCode;
        document.getElementById('pixResult').classList.add('show');
        document.getElementById('accessFields').style.display = 'none';
        const dialog = document.querySelector('.access-dialog');
        if (dialog) dialog.scrollTop = 0;

        accessStatus.innerHTML = 'PIX Gerado com Sucesso! <strong>R$ ' + result.amount.toFixed(2).replace('.', ',') + '</strong>. Pague agora para liberar o acesso instantaneamente.';
        accessStatus.classList.add('show');
        submitButton.textContent = 'PIX GERADO';

        pollPaymentStatus(result.idTransaction, data);
      }).catch(error => {
        accessStatus.textContent = error.message;
        accessStatus.classList.add('show');
        submitButton.disabled = false;
        submitButton.textContent = 'GERAR PIX — R$ 87,90';
      });
    });

    const copyBtn = document.getElementById('pixCopy');
    if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        try {
          await navigator.clipboard.writeText(document.getElementById('pixCode').value);
          copyBtn.textContent = '✅ PIX COPIADO!';
          setTimeout(() => { copyBtn.textContent = 'COPIAR CÓDIGO PIX'; }, 1600);
        } catch (e) {
          document.getElementById('pixCode').select();
          document.execCommand('copy');
          copyBtn.textContent = '✅ PIX COPIADO!';
          setTimeout(() => { copyBtn.textContent = 'COPIAR CÓDIGO PIX'; }, 1600);
        }
      });
    }

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
