const loginScreen = document.getElementById('loginScreen');
const forcePasswordScreen = document.getElementById('forcePasswordScreen');
const app = document.getElementById('app');

let pendingLoginEmail = '';
let pendingTempPassword = '';
let workflowUnlockTimer = null;
let tutorialUnlockTimer = null;
let sessionHeartbeat = null;
let referralsTimer = null;
let tutorialWatermarkText = 'CAPIVARA CLUB HOT • CONTEÚDO PROTEGIDO';

function updateTutorialWatermark(name, emailValue) {
  const identity = [name, emailValue].filter(Boolean).join(' • ') || 'MEMBRO';
  tutorialWatermarkText = `${identity} • CONTEÚDO PROTEGIDO`;
  document.querySelectorAll('.video-security-watermark').forEach(watermark => {
    watermark.textContent = tutorialWatermarkText;
  });
}

function formatWorkflowCountdown(milliseconds) {
  const totalSeconds = Math.max(0, Math.floor(milliseconds / 1000));
  const days = Math.floor(totalSeconds / 86400);
  const hours = Math.floor((totalSeconds % 86400) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  return `${days}d ${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m ${String(seconds).padStart(2, '0')}s`;
}

function updateWorkflowLocks(unlockAtValue) {
  if (workflowUnlockTimer) {
    clearInterval(workflowUnlockTimer);
    workflowUnlockTimer = null;
  }

  const lockedCards = [...document.querySelectorAll('.workflow-lockable[data-workflow-locked="true"]')];
  const notice = document.getElementById('workflowUnlockNotice');
  if (!lockedCards.length) return;

  const unlockTimestamp = Date.parse(unlockAtValue || '');
  const render = () => {
    const remaining = Number.isFinite(unlockTimestamp) ? unlockTimestamp - Date.now() : null;
    const isLocked = remaining === null || remaining > 0;

    lockedCards.forEach(card => {
      let overlay = card.querySelector('.workflow-lock-overlay');
      if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'workflow-lock-overlay';
        const title = document.createElement('strong');
        title.append('LIBERA EM ');
        const countdown = document.createElement('span');
        countdown.className = 'workflow-countdown';
        title.appendChild(countdown);
        const subtitle = document.createElement('small');
        subtitle.textContent = 'Disponível após 7 dias da compra';
        overlay.append(title, subtitle);
        card.appendChild(overlay);
      }

      card.classList.toggle('workflow-locked', isLocked);
      card.classList.toggle('workflow-unlocked', !isLocked);
      overlay.classList.toggle('hidden', !isLocked);
      const countdown = overlay.querySelector('.workflow-countdown');
      if (countdown) countdown.textContent = remaining === null ? 'aguardando' : formatWorkflowCountdown(remaining);
    });

    if (notice) {
      notice.classList.toggle('hidden', !isLocked);
      notice.textContent = isLocked
        ? `Os workflows 5 a 10 serão liberados automaticamente em ${remaining === null ? 'aguardando a confirmação da compra' : formatWorkflowCountdown(remaining)}.`
        : '';
    }

    if (!isLocked && workflowUnlockTimer) {
      clearInterval(workflowUnlockTimer);
      workflowUnlockTimer = null;
    }
  };

  render();
  if (!Number.isFinite(unlockTimestamp) || unlockTimestamp > Date.now()) {
    workflowUnlockTimer = setInterval(render, 1000);
  }
}

function activateTutorialPlayer(card, number) {
  const video = card.querySelector('.tutorial-video');
  const emptyState = card.querySelector('.video-empty');
  const videoBox = card.querySelector('.video-box');
  if (!video || !emptyState || !videoBox || video.dataset.protectedSrc) return;

  const title = emptyState.querySelector('strong');
  if (title) title.textContent = 'Aula ainda sem vídeo';
  let note = emptyState.querySelector('small');
  if (!note) {
    note = document.createElement('small');
    emptyState.appendChild(note);
  }
  note.textContent = 'O arquivo desta aula ainda não está disponível na biblioteca.';

  const watermark = document.createElement('div');
  watermark.className = 'video-security-watermark';
  watermark.setAttribute('aria-hidden', 'true');
  watermark.textContent = tutorialWatermarkText;
  videoBox.appendChild(watermark);

  const fullscreenButton = document.createElement('button');
  fullscreenButton.type = 'button';
  fullscreenButton.className = 'tutorial-fullscreen-btn';
  fullscreenButton.setAttribute('aria-label', 'Abrir vídeo em tela cheia');
  fullscreenButton.textContent = '⛶';
  fullscreenButton.addEventListener('click', async event => {
    event.preventDefault();
    event.stopPropagation();
    try {
      if (document.fullscreenElement === videoBox) {
        await document.exitFullscreen();
      } else if (videoBox.requestFullscreen) {
        await videoBox.requestFullscreen();
      } else if (videoBox.webkitRequestFullscreen) {
        videoBox.webkitRequestFullscreen();
      }
    } catch (error) {
      console.warn('Não foi possível abrir o vídeo em tela cheia.', error);
    }
  });
  document.addEventListener('fullscreenchange', () => {
    const isFullscreen = document.fullscreenElement === videoBox;
    fullscreenButton.textContent = isFullscreen ? '×' : '⛶';
    fullscreenButton.setAttribute('aria-label', isFullscreen ? 'Sair da tela cheia' : 'Abrir vídeo em tela cheia');
  });
  videoBox.appendChild(fullscreenButton);
  video.setAttribute('controlsList', 'nodownload nofullscreen noremoteplayback');
  video.style.display = 'block';
  video.addEventListener('contextmenu', event => event.preventDefault());
  video.addEventListener('loadedmetadata', () => { emptyState.style.display = 'none'; });
  video.addEventListener('loadeddata', () => { emptyState.style.display = 'none'; });
  video.addEventListener('error', () => {
    video.style.display = 'none';
    emptyState.style.display = 'flex';
  });
  video.dataset.protectedSrc = `/videos-tutoriais/tutorial-${number}.mp4`;
}

function updateTutorialAvailability(unlockAtValue) {
  if (tutorialUnlockTimer) {
    clearInterval(tutorialUnlockTimer);
    tutorialUnlockTimer = null;
  }

  const cards = [...document.querySelectorAll('.tutorial-card[data-delayed-tutorial]')];
  if (!cards.length) return;
  const unlockTimestamp = Date.parse(unlockAtValue || '');
  const render = () => {
    let anyLocked = false;
    cards.forEach(card => {
      const number = card.dataset.delayedTutorial;
      const days = number === '09' ? 5 : 3;
      const remaining = Number.isFinite(unlockTimestamp) ? unlockTimestamp + (days - 3) * 86400000 - Date.now() : null;
      const locked = remaining === null || remaining > 0;
      anyLocked = anyLocked || locked;
      const video = card.querySelector('.tutorial-video');
      const emptyState = card.querySelector('.video-empty');
      const title = emptyState?.querySelector('strong');
      let note = emptyState?.querySelector('small');
      if (!note && emptyState) {
        note = document.createElement('small');
        emptyState.appendChild(note);
      }

      if (locked) {
        if (video?.dataset.protectedSrc) {
          video.pause();
          video.removeAttribute('src');
          video.load();
        }
        if (video) video.style.display = 'none';
        if (title) title.textContent = `Tutorial ${number} libera em ${remaining === null ? 'breve' : formatWorkflowCountdown(remaining)}`;
        if (note) note.textContent = `Disponível após ${days} dias da compra.`;
        if (emptyState) emptyState.style.display = 'flex';
      } else {
        activateTutorialPlayer(card, number);
      }
    });

    loadProtectedTutorials();
    if (!anyLocked) {
      if (tutorialUnlockTimer) clearInterval(tutorialUnlockTimer);
      tutorialUnlockTimer = null;
      loadProtectedTutorials();
    }
  };

  render();
  if (!Number.isFinite(unlockTimestamp) || unlockTimestamp + 2 * 86400000 > Date.now()) {
    tutorialUnlockTimer = setInterval(render, 1000);
  }
}

function formatMemberName(rawName, emailValue) {
  const source = rawName || emailValue.split('@')[0].replace(/[._-]+/g, ' ').trim();
  return source
    ? source.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
    : 'MEMBRO';
}

function loadMemberGalleryImages() {
  document.querySelectorAll('[data-content="galeria"] .gallery-card img[data-src]').forEach(image => {
    image.src = image.dataset.src;
    image.removeAttribute('data-src');
  });
}

let memberPromptsPromise = null;

function loadMemberPrompts() {
  loadMemberGalleryImages();
  if (memberPromptsPromise) return memberPromptsPromise;

  memberPromptsPromise = fetch('/api/member/prompts', {cache: 'no-store', credentials: 'include'})
    .then(response => {
      if (!response.ok) throw new Error(`Falha ao carregar a galeria (${response.status}).`);
      return response.json();
    })
    .then(result => {
      window.DMCN_PROMPTS = result.prompts || [];
      document.querySelectorAll('[data-content="galeria"] .gallery-card').forEach((card, index) => {
        const prompt = window.DMCN_PROMPTS[index] || '';
        card.dataset.prompt = prompt;
        card.querySelectorAll('.gallery-image').forEach(image => { image.dataset.prompt = prompt; });
      });
      return window.DMCN_PROMPTS;
    })
    .catch(error => {
      memberPromptsPromise = null;
      console.warn('Não foi possível carregar os prompts protegidos.', error);
      const status = document.querySelector('[data-content="galeria"] .gallery-page-status');
      if (status) status.textContent = error.message.includes('(401)')
        ? 'Faça login novamente para carregar os prompts.'
        : 'Fotos carregadas; não foi possível carregar os prompts.';
      throw error;
    });

  return memberPromptsPromise;
}

function enterApp(name, emailValue, isAdmin, workflowUnlockAt, tutorialUnlockAt) {
  document.getElementById('memberName').textContent = formatMemberName(name, emailValue);
  updateTutorialWatermark(name, emailValue);
  localStorage.setItem('memberEmail', emailValue);
  localStorage.setItem('memberName', name || '');
  localStorage.setItem('memberIsAdmin', isAdmin ? '1' : '0');
  document.getElementById('adminAccessBtn')?.classList.toggle('hidden', !isAdmin);
  loginScreen.classList.add('hidden');
  forcePasswordScreen.classList.add('hidden');
  app.classList.remove('hidden');
  updateWorkflowLocks(workflowUnlockAt);
  updateTutorialAvailability(tutorialUnlockAt);
  loadProtectedTutorials();
  loadMemberPrompts().catch(() => {});
  loadProtectedGallery18();
  loadReferrals();
  if (referralsTimer) clearInterval(referralsTimer);
  referralsTimer = setInterval(() => {
    const referralsPage = document.querySelector('[data-content="indique-e-ganhe"]');
    if (!document.hidden && !app.classList.contains('hidden') && referralsPage && !referralsPage.classList.contains('hidden')) loadReferrals();
  }, 30000);
}

function leaveApp(message = '') {
  if (referralsTimer) {
    clearInterval(referralsTimer);
    referralsTimer = null;
  }
  if (sessionHeartbeat) {
    clearInterval(sessionHeartbeat);
    sessionHeartbeat = null;
  }
  if (tutorialUnlockTimer) {
    clearInterval(tutorialUnlockTimer);
    tutorialUnlockTimer = null;
  }
  localStorage.removeItem('memberEmail');
  localStorage.removeItem('memberName');
  localStorage.removeItem('memberIsAdmin');
  document.getElementById('adminAccessBtn')?.classList.add('hidden');
  app.classList.add('hidden');
  forcePasswordScreen.classList.add('hidden');
  loginScreen.classList.remove('hidden');
  if (message) ClubUI.alert(message);
}

function csrfHeaders(headers = {}) {
  const cookie = document.cookie.split('; ').find(item => item.startsWith('ia_influencer_csrf='));
  const token = cookie ? decodeURIComponent(cookie.slice('ia_influencer_csrf='.length)) : '';
  return token ? {...headers, 'X-CSRF-Token': token} : headers;
}

function startSessionHeartbeat() {
  if (sessionHeartbeat) clearInterval(sessionHeartbeat);
  sessionHeartbeat = setInterval(async () => {
    if (app.classList.contains('hidden')) return;
    try {
      const response = await fetch('/api/session', {cache: 'no-store'});
      if (!response.ok) {
        leaveApp('Sua conta foi aberta em outro dispositivo. Faça login novamente.');
      }
    } catch (error) {
      // Falhas momentâneas de rede não encerram a sessão.
    }
  }, 30000);
}

(async function restoreSession(){
  try {
    const response = await fetch('/api/session');
    if (!response.ok) return;
    const result = await response.json();
    enterApp(result.name, result.email, result.isAdmin, result.workflowUnlockAt, result.tutorialUnlockAt);
    startSessionHeartbeat();
  } catch (error) {
    // sem conexao com o servidor: mantem a tela de login
  }
})();

document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const submitButton = e.target.querySelector('button[type="submit"]');
  const emailValue = document.getElementById('email').value.trim();
  const passwordValue = document.getElementById('password').value.trim();

  submitButton.disabled = true;
  submitButton.textContent = 'ENTRANDO...';
  try {
    const response = await fetch('/api/login', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: emailValue, password: passwordValue})
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Não foi possível entrar.');

    if (result.mustChangePassword) {
      pendingLoginEmail = result.email || emailValue;
      pendingTempPassword = passwordValue;
      document.getElementById('newPassword').value = '';
      document.getElementById('newPasswordConfirm').value = '';
      loginScreen.classList.add('hidden');
      forcePasswordScreen.classList.remove('hidden');
    } else {
      enterApp(result.name, result.email || emailValue, result.isAdmin, result.workflowUnlockAt, result.tutorialUnlockAt);
      startSessionHeartbeat();
    }
  } catch (error) {
    ClubUI.alert(error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'ENTRAR NA ÁREA DE MEMBROS';
  }
});

document.getElementById('forcePasswordForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const submitButton = e.target.querySelector('button[type="submit"]');
  const newPassword = document.getElementById('newPassword').value;
  const newPasswordConfirm = document.getElementById('newPasswordConfirm').value;

  if (newPassword.length < 8) return ClubUI.alert('Use uma senha com pelo menos 8 caracteres.');
  if (newPassword !== newPasswordConfirm) return ClubUI.alert('As senhas não coincidem.');

  submitButton.disabled = true;
  submitButton.textContent = 'SALVANDO...';
  try {
    const response = await fetch('/api/set-initial-password', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: pendingLoginEmail, currentPassword: pendingTempPassword, newPassword})
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Não foi possível salvar a nova senha.');

    enterApp(result.name, pendingLoginEmail, result.isAdmin, result.workflowUnlockAt, result.tutorialUnlockAt);
    startSessionHeartbeat();
    pendingTempPassword = '';
  } catch (error) {
    ClubUI.alert(error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'SALVAR NOVA SENHA';
  }
});

let currentReferralBalance = 0;
async function loadReferrals() {
  const email = localStorage.getItem('memberEmail');
  const linkInput = document.getElementById('refLinkInput');
  const invitedCountEl = document.getElementById('refInvitedCount');
  const totalRevenueEl = document.getElementById('refTotalRevenue');
  const commissionValueEl = document.getElementById('refCommissionValue');
  const commissionSubEl = document.getElementById('refCommissionSub');
  const availableBalanceEl = document.getElementById('refAvailableBalance');
  const withdrawButton = document.getElementById('refWithdrawOpen');
  const withdrawHint = document.getElementById('refWithdrawHint');
  const withdrawHistory = document.getElementById('refWithdrawHistory');
  const list = document.getElementById('refList');
  const listEmpty = document.getElementById('refListEmpty');
  if (!email || !linkInput) return;

  try {
    const response = await fetch(`/api/referrals?email=${encodeURIComponent(email)}`);
    if (!response.ok) return;
    const result = await response.json();

    linkInput.value = result.referralLink;
    invitedCountEl.textContent = String(result.invitedCount);
    totalRevenueEl.textContent = `R$ ${result.totalRevenue.toFixed(2).replace('.', ',')}`;
    commissionValueEl.textContent = `R$ ${result.commissionPerSale.toFixed(2).replace('.', ',')}`;
    commissionSubEl.textContent = `R$ ${result.commissionPerSale} reais por venda`;

    const available = Number(result.availableBalance || 0);
    currentReferralBalance = available;
    if (availableBalanceEl) availableBalanceEl.textContent = `R$ ${available.toFixed(2).replace('.', ',')}`;
    if (withdrawButton) withdrawButton.disabled = available < 50;
    if (withdrawHint) withdrawHint.textContent = available >= 50 ? 'Você já pode solicitar o saque do seu saldo disponível.' : `Faltam R$ ${(50 - available).toFixed(2).replace('.', ',')} para atingir o mínimo de R$ 50,00.`;
    if (withdrawHistory) {
      const labels = {pending: 'Aguardando pagamento manual', processing: 'Enviado à gateway', review: 'Em conferência', paid: 'Pago', failed: 'Recusado'};
      withdrawHistory.replaceChildren();
      if (result.withdrawals?.length) {
        const heading = document.createElement('strong');
        heading.textContent = 'Seus saques';
        withdrawHistory.append(heading);
        result.withdrawals.forEach(withdrawal => {
          const row = document.createElement('div');
          const date = new Date(withdrawal.createdAt).toLocaleDateString('pt-BR');
          row.textContent = `R$ ${Number(withdrawal.amount).toFixed(2).replace('.', ',')} · ${labels[withdrawal.status] || 'Atualizado'} · ${date}`;
          withdrawHistory.append(row);
        });
      }
    }

    list.querySelectorAll('.ref-item').forEach(el => el.remove());
    if (result.referrals.length === 0) {
      listEmpty.style.display = '';
    } else {
      listEmpty.style.display = 'none';
      result.referrals.forEach(ref => {
        const item = document.createElement('div');
        item.className = 'ref-item';
        const date = new Date(ref.createdAt).toLocaleDateString('pt-BR');
        const statusLabel = ref.status === 'paid' ? 'Pago' : 'Pendente';
        const refInfo = document.createElement('div');
        const refName = document.createElement('div');
        const refDate = document.createElement('div');
        const refStatus = document.createElement('span');
        refName.className = 'ref-item-name';
        refName.textContent = ref.name || 'Indicação';
        refDate.className = 'ref-item-date';
        refDate.textContent = date;
        refStatus.className = `ref-item-status ${ref.status === 'paid' ? 'paid' : 'pending'}`;
        refStatus.textContent = statusLabel;
        refInfo.append(refName, refDate);
        item.append(refInfo, refStatus);
        list.appendChild(item);
      });
    }
  } catch (error) {
    console.error('Falha ao carregar indicações:', error);
  }
}

const refWithdrawModal = document.getElementById('refWithdrawModal');
const refWithdrawForm = document.getElementById('refWithdrawForm');
const refWithdrawPixKey = document.getElementById('refWithdrawPixKey');
const refWithdrawPixType = document.getElementById('refWithdrawPixType');
const refWithdrawPixHint = document.getElementById('refWithdrawPixHint');
const refWithdrawPixExamples = {
  EMAIL: {placeholder: 'seuemail@exemplo.com', type: 'text', inputmode: 'email', hint: 'Digite o e-mail cadastrado como chave PIX.'},
  CPF: {placeholder: '000.000.000-00', type: 'text', inputmode: 'numeric', hint: 'Informe o CPF vinculado à sua conta bancária.'},
  CNPJ: {placeholder: '00.000.000/0000-00', type: 'text', inputmode: 'numeric', hint: 'Informe o CNPJ vinculado à conta que receberá.'},
  PHONE: {placeholder: '+55 (11) 99999-9999', type: 'tel', inputmode: 'tel', hint: 'Digite o telefone com DDD, incluindo o código do país se necessário.'},
  RANDOM: {placeholder: 'Cole sua chave aleatória', type: 'text', inputmode: 'text', hint: 'Cole a chave aleatória completa gerada pelo seu banco.'},
};
const refWithdrawPixOptions = document.querySelectorAll('input[name="refWithdrawPixChoice"]');
const updateRefWithdrawPixType = option => {
  refWithdrawPixType.value = option.value;
  document.querySelectorAll('.ref-pix-option').forEach(card => card.classList.toggle('selected', card.contains(option)));
  const example = refWithdrawPixExamples[option.value];
  refWithdrawPixKey.type = example.type;
  refWithdrawPixKey.inputMode = example.inputmode;
  refWithdrawPixKey.placeholder = example.placeholder;
  refWithdrawPixHint.textContent = example.hint;
};
refWithdrawPixOptions.forEach(option => option.addEventListener('change', () => updateRefWithdrawPixType(option)));
const selectedRefWithdrawPixOption = [...refWithdrawPixOptions].find(option => option.checked);
if (selectedRefWithdrawPixOption) updateRefWithdrawPixType(selectedRefWithdrawPixOption);
const closeRefWithdrawModal = () => {
  refWithdrawModal?.classList.add('hidden');
  refWithdrawModal?.setAttribute('aria-hidden', 'true');
};
document.getElementById('refWithdrawOpen')?.addEventListener('click', () => {
  const balance = currentReferralBalance;
  const amount = document.getElementById('refWithdrawAmount');
  amount.max = balance.toFixed(2);
  amount.value = balance.toFixed(2);
  refWithdrawModal.classList.remove('hidden');
  refWithdrawModal.setAttribute('aria-hidden', 'false');
  document.getElementById('refWithdrawName').focus();
});
document.getElementById('refWithdrawClose')?.addEventListener('click', closeRefWithdrawModal);
document.getElementById('refWithdrawCancel')?.addEventListener('click', closeRefWithdrawModal);
refWithdrawModal?.addEventListener('click', event => { if (event.target === refWithdrawModal) closeRefWithdrawModal(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeRefWithdrawModal(); });
refWithdrawForm?.addEventListener('submit', async event => {
  event.preventDefault();
  const button = document.getElementById('refWithdrawSubmit');
  button.disabled = true;
  try {
    const response = await fetch('/api/referrals/withdrawals', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        name: document.getElementById('refWithdrawName').value.trim(),
        amount: Number(document.getElementById('refWithdrawAmount').value),
        pixKey: document.getElementById('refWithdrawPixKey').value.trim(),
        pixKeyType: document.getElementById('refWithdrawPixType').value,
      }),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Não foi possível solicitar o saque.');
    closeRefWithdrawModal();
    refWithdrawForm.reset();
    await loadReferrals();
    ClubUI.alert('Sua solicitação foi recebida. O valor ficará reservado enquanto o pagamento é organizado manualmente.', {title: 'Pedido recebido'});
  } catch (error) {
    ClubUI.alert(error.message, {title: 'Não foi possível solicitar'});
  } finally {
    button.disabled = false;
  }
});

document.getElementById('refLinkCopy')?.addEventListener('click', async () => {
  const linkInput = document.getElementById('refLinkInput');
  const btn = document.getElementById('refLinkCopy');
  try {
    await navigator.clipboard.writeText(linkInput.value);
    const original = btn.textContent;
    btn.textContent = 'Copiado!';
    setTimeout(() => { btn.textContent = original; }, 1400);
  } catch (error) {
    linkInput.select();
  }
});

document.querySelectorAll('.tutorial-card').forEach(card => {
  const number = card.querySelector('.tutorial-num')?.textContent.trim();
  const video = card.querySelector('.tutorial-video');
  const emptyState = card.querySelector('.video-empty');
  const videoBox = card.querySelector('.video-box');
  if (!number || !video || !emptyState || !videoBox) return;
  if (number === '07' || number === '08' || number === '09') {
    const title = emptyState.querySelector('strong');
    if (title) title.textContent = `Tutorial ${number} aguardando liberação`;
    const note = document.createElement('small');
    note.textContent = `Disponível após ${number === '09' ? 5 : 3} dias da compra.`;
    emptyState.appendChild(note);
    video.style.display = 'none';
    card.dataset.delayedTutorial = number;
    return;
  }
  activateTutorialPlayer(card, number);
});

function loadProtectedTutorials() {
  document.querySelectorAll('.tutorial-video[data-protected-src]').forEach(video => {
    if (video.src.endsWith(video.dataset.protectedSrc)) return;
    video.src = video.dataset.protectedSrc;
    video.load();
  });
}

(function initHeroAvatar() {
  const avatarInput = document.getElementById('heroAvatarInput');
  const placeholder = document.getElementById('heroAvatarPlaceholder');
  const avatarImg = document.getElementById('heroAvatarImg');
  const cropModal = document.getElementById('cropModal');
  const cropViewport = document.getElementById('cropViewport');
  const cropImage = document.getElementById('cropImage');
  const cropZoom = document.getElementById('cropZoom');
  const cropClose = document.getElementById('cropClose');
  const cropCancel = document.getElementById('cropCancel');
  const cropConfirm = document.getElementById('cropConfirm');
  const cropSwap = document.getElementById('cropSwap');
  const cropSwapInput = document.getElementById('cropSwapInput');
  if (!avatarInput || !placeholder || !avatarImg || !cropModal) return;

  let originalPhoto = localStorage.getItem('heroAvatarOriginal');

  function showSavedState() {
    const savedPhoto = localStorage.getItem('heroAvatarPhoto');
    if (savedPhoto) {
      avatarImg.src = savedPhoto;
      avatarImg.hidden = false;
      placeholder.hidden = true;
    }
  }
  showSavedState();

  function loadFile(file) {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      ClubUI.alert('Envie um arquivo de imagem.');
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      originalPhoto = reader.result;
      localStorage.setItem('heroAvatarOriginal', originalPhoto);
      openCropModal(originalPhoto);
    };
    reader.readAsDataURL(file);
  }

  function openPicker() { avatarInput.click(); }
  placeholder.addEventListener('click', openPicker);
  avatarImg.addEventListener('click', () => {
    if (originalPhoto) openCropModal(originalPhoto);
    else openPicker();
  });
  if (cropSwap && cropSwapInput) {
    cropSwap.addEventListener('click', () => cropSwapInput.click());
    cropSwapInput.addEventListener('change', () => {
      loadFile(cropSwapInput.files[0]);
      cropSwapInput.value = '';
    });
  }

  avatarInput.addEventListener('change', () => {
    loadFile(avatarInput.files[0]);
    avatarInput.value = '';
  });

  let naturalW = 0, naturalH = 0, baseScale = 1, zoom = 1, offsetX = 0, offsetY = 0;
  let viewportW = 0, viewportH = 0;

  function openCropModal(dataUrl) {
    cropImage.onload = () => {
      naturalW = cropImage.naturalWidth;
      naturalH = cropImage.naturalHeight;
      const rect = cropViewport.getBoundingClientRect();
      viewportW = rect.width;
      viewportH = rect.height;
      baseScale = Math.max(viewportW / naturalW, viewportH / naturalH);
      zoom = 1;
      cropZoom.value = 1;
      offsetX = (viewportW - naturalW * baseScale) / 2;
      offsetY = (viewportH - naturalH * baseScale) / 2;
      applyTransform();
    };
    cropImage.src = dataUrl;
    cropModal.classList.remove('hidden');
    cropModal.setAttribute('aria-hidden', 'false');
  }

  function closeCropModal() {
    cropModal.classList.add('hidden');
    cropModal.setAttribute('aria-hidden', 'true');
    avatarInput.value = '';
  }

  function currentScale() { return baseScale * zoom; }

  function clampOffsets() {
    const scale = currentScale();
    const dispW = naturalW * scale;
    const dispH = naturalH * scale;
    offsetX = Math.min(0, Math.max(viewportW - dispW, offsetX));
    offsetY = Math.min(0, Math.max(viewportH - dispH, offsetY));
  }

  function applyTransform() {
    clampOffsets();
    const scale = currentScale();
    cropImage.style.width = `${naturalW * scale}px`;
    cropImage.style.height = `${naturalH * scale}px`;
    cropImage.style.left = `${offsetX}px`;
    cropImage.style.top = `${offsetY}px`;
  }

  cropZoom.addEventListener('input', () => {
    zoom = Number(cropZoom.value);
    applyTransform();
  });

  let dragging = false, dragStartX = 0, dragStartY = 0, startOffsetX = 0, startOffsetY = 0;

  cropViewport.addEventListener('pointerdown', event => {
    dragging = true;
    cropViewport.classList.add('dragging');
    cropViewport.setPointerCapture(event.pointerId);
    dragStartX = event.clientX;
    dragStartY = event.clientY;
    startOffsetX = offsetX;
    startOffsetY = offsetY;
  });
  cropViewport.addEventListener('pointermove', event => {
    if (!dragging) return;
    offsetX = startOffsetX + (event.clientX - dragStartX);
    offsetY = startOffsetY + (event.clientY - dragStartY);
    applyTransform();
  });
  function stopDragging() {
    dragging = false;
    cropViewport.classList.remove('dragging');
  }
  cropViewport.addEventListener('pointerup', stopDragging);
  cropViewport.addEventListener('pointercancel', stopDragging);

  cropClose.addEventListener('click', closeCropModal);
  cropCancel.addEventListener('click', closeCropModal);
  cropModal.addEventListener('click', event => {
    if (event.target === cropModal) closeCropModal();
  });

  cropConfirm.addEventListener('click', () => {
    const scale = currentScale();
    const sx = -offsetX / scale;
    const sy = -offsetY / scale;
    const sWidth = viewportW / scale;
    const sHeight = viewportH / scale;

    const outputW = Math.round(viewportW * 2);
    const outputH = Math.round(viewportH * 2);
    const canvas = document.createElement('canvas');
    canvas.width = outputW;
    canvas.height = outputH;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(cropImage, sx, sy, sWidth, sHeight, 0, 0, outputW, outputH);

    const finalDataUrl = canvas.toDataURL('image/jpeg', 0.92);
    avatarImg.src = finalDataUrl;
    avatarImg.hidden = false;
    placeholder.hidden = true;
    localStorage.setItem('heroAvatarPhoto', finalDataUrl);
    closeCropModal();
  });
})();

const resendModal = document.getElementById('resendModal');
const resendEmailInput = document.getElementById('resendEmail');
const resendSubmitButton = document.getElementById('resendSubmit');

function openResendModal() {
  resendEmailInput.value = '';
  resendModal.classList.remove('hidden');
  resendModal.setAttribute('aria-hidden', 'false');
  resendEmailInput.focus();
}

function closeResendModal() {
  resendModal.classList.add('hidden');
  resendModal.setAttribute('aria-hidden', 'true');
}

document.getElementById('resendPassword').addEventListener('click', openResendModal);
document.getElementById('resendModalClose').addEventListener('click', closeResendModal);
resendModal.addEventListener('click', event => {
  if (event.target === resendModal) closeResendModal();
});

resendSubmitButton.addEventListener('click', async () => {
  const emailValue = resendEmailInput.value.trim();
  if (!emailValue) return ClubUI.alert('Informe o e-mail do cliente para reenviar o link de senha.');
  resendSubmitButton.disabled = true;
  resendSubmitButton.textContent = 'ENVIANDO...';
  try {
    const response = await fetch('/api/resend-password', {
      method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({email: emailValue})
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Não foi possível reenviar o e-mail.');
    ClubUI.alert('Link enviado. Confira sua caixa de entrada e spam.');
    closeResendModal();
  } catch (error) {
    ClubUI.alert(error.message);
  } finally {
    resendSubmitButton.disabled = false;
    resendSubmitButton.textContent = 'ENVIAR LINK DE SENHA';
  }
});

document.getElementById('logout').addEventListener('click', () => {
  fetch('/api/logout', {method: 'POST', headers: csrfHeaders()}).catch(() => {});
  leaveApp();
});

const MOBILE_FIXED_TABS = ['inicio', 'tutoriais', 'workflows', 'comunidade', 'indique-e-ganhe'];

function closeMobileDrawer() {
  document.body.classList.remove('mobile-drawer-open');
}

function openPage(page) {
  document.querySelectorAll('.member-page').forEach(section => {
    section.classList.toggle('hidden', section.dataset.content !== page);
  });

  document.querySelectorAll('.nav-btn, .sidebar-link[data-page]').forEach(button => {
    button.classList.toggle('active', button.dataset.page === page);
  });

  const mobileMoreBtn = document.getElementById('mobileMoreBtn');
  mobileMoreBtn?.classList.toggle('active', !MOBILE_FIXED_TABS.includes(page));

  window.scrollTo({top: 0, behavior: 'smooth'});
}

document.querySelectorAll('.nav-btn, .nav-card, .sidebar-link[data-page]').forEach(button => {
  button.addEventListener('click', () => {
    if (button.dataset.page) openPage(button.dataset.page);
    closeMobileDrawer();
  });
});
document.querySelector('[data-page="comunidade"]')?.addEventListener('click', event => {
  event.preventDefault();
  openPage('comunidade');
});

document.getElementById('mobileMoreBtn')?.addEventListener('click', () => {
  document.body.classList.toggle('mobile-drawer-open');
});
document.getElementById('mobileDrawerClose')?.addEventListener('click', closeMobileDrawer);
document.getElementById('mobileDrawerBackdrop')?.addEventListener('click', closeMobileDrawer);

const sidebar = document.querySelector('.sidebar');
const layout = document.querySelector('.layout');
sidebar?.addEventListener('mouseenter', () => layout?.classList.add('sidebar-open'));
sidebar?.addEventListener('mouseleave', () => layout?.classList.remove('sidebar-open'));
const topLogo = document.querySelector('.top-logo');
document.querySelectorAll('.community-brand-icon img:not([alt="Logo NX GATE"]):not([alt="Logo Shark Bot"]):not([alt="Favicon Ravenbot"])').forEach(communityLogo => {
  if (topLogo) communityLogo.src = topLogo.src;
});
const mobileDrawerLogo = document.querySelector('.mobile-drawer-logo');
if (mobileDrawerLogo && topLogo) mobileDrawerLogo.src = topLogo.src;

document.querySelectorAll('.prompt-copy').forEach(btn => {
  btn.addEventListener('click', () => {
    const card = btn.closest('.prompt-card');
    const title = card?.dataset.name || card?.querySelector('h3')?.innerText || 'PROMPT';
    const content = card?.dataset.prompt || '';
    const viewer = document.getElementById('promptViewer');
    const viewerTitle = document.getElementById('promptViewerTitle');
    const viewerContent = document.getElementById('promptViewerContent');
    const viewerCopy = document.getElementById('promptViewerCopy');
    viewerTitle.textContent = title.toUpperCase();
    viewerContent.textContent = content.trim() || 'SEU PROMPT SERÁ ADICIONADO AQUI.';
    viewerContent.classList.toggle('empty', !content.trim());
    if (viewerCopy) {
      viewerCopy.disabled = !content.trim();
      viewerCopy.textContent = '▣ COPIAR';
    }
    viewer.classList.remove('hidden');
    viewer.setAttribute('aria-hidden','false');
  });
});

const galleryGrid = document.querySelector('[data-content="galeria"] .prompt-gallery');
if (galleryGrid) {
  galleryGrid.innerHTML = '';
  for (let index = 1; index <= 194; index += 1) {
    const promptName = `Prompt ${index}`;
    const card = document.createElement('article');
    card.className = 'gallery-card';
    card.dataset.name = promptName;
    card.dataset.prompt = window.DMCN_PROMPTS?.[index - 1] || '';
    card.innerHTML = `<div class="gallery-image-pair"><img class="gallery-image" data-gallery-prompt-name="${promptName}" data-src="/member-assets/gallery/${index}-1.jpeg" alt="Imagem 1 do ${promptName}" loading="lazy"><img class="gallery-image" data-gallery-prompt-name="${promptName}" data-src="/member-assets/gallery/${index}-2.jpeg" alt="Imagem 2 do ${promptName}" loading="lazy"></div><div class="gallery-card-body"><h3>${promptName}</h3><button class="gallery-copy" type="button">▣ COPIAR PROMPT</button></div>`;
    galleryGrid.appendChild(card);
  }
}

if (galleryGrid) {
  const galleryCards = [...galleryGrid.querySelectorAll('.gallery-card')];
  const galleryPrevious = document.getElementById('galleryPrevious');
  const galleryNext = document.getElementById('galleryNext');
  const galleryPageStatus = document.getElementById('galleryPageStatus');
  const galleryPageSize = 6;
  const galleryPageCount = Math.ceil(galleryCards.length / galleryPageSize);
  let galleryPage = 1;
  const renderGalleryPage = () => {
    const firstCard = (galleryPage - 1) * galleryPageSize;
    galleryCards.forEach((card, index) => {
      const isHidden = index < firstCard || index >= firstCard + galleryPageSize;
      card.hidden = isHidden;
      card.classList.toggle('gallery-hidden', isHidden);
    });
    if (galleryPageStatus) galleryPageStatus.textContent = `Página ${galleryPage} de ${galleryPageCount}`;
    if (galleryPrevious) galleryPrevious.disabled = galleryPage === 1;
    if (galleryNext) galleryNext.disabled = galleryPage === galleryPageCount;
    document.querySelector('[data-content="galeria"]')?.scrollIntoView({behavior:'smooth',block:'start'});
  };
  galleryPrevious?.addEventListener('click', () => {
    if (galleryPage > 1) { galleryPage -= 1; renderGalleryPage(); }
  });
  galleryNext?.addEventListener('click', () => {
    if (galleryPage < galleryPageCount) { galleryPage += 1; renderGalleryPage(); }
  });
  renderGalleryPage();

  galleryGrid.addEventListener('click', event => {
    const button = event.target.closest('.gallery-copy');
    if (button) copyGalleryPrompt(button);
  });
}

async function loadProtectedGallery18() {
  const gallery18Grid = document.getElementById('gallery18Grid');
  if (gallery18Grid) {
  const gallery18Previous = document.getElementById('gallery18Previous');
  const gallery18Next = document.getElementById('gallery18Next');
  const gallery18PageStatus = document.getElementById('gallery18PageStatus');
  const gallery18PageSize = 12;

  gallery18Grid.addEventListener('click', event => {
    const button = event.target.closest('.gallery-copy');
    if (button) copyGalleryPrompt(button);
  });

  fetch('/api/member/prompts-18', {cache: 'no-store', credentials: 'include'})
    .then(response => {
      if (!response.ok) throw new Error('Não foi possível carregar os prompts +18.');
      return response.json();
    })
    .then(prompts => {
      gallery18Grid.innerHTML = '';
      prompts.forEach((prompt, index) => {
        const promptName = `Prompt ${index + 1}`;
        const card = document.createElement('article');
        const imagePair = document.createElement('div');
        const image = document.createElement('img');
        const body = document.createElement('div');
        const title = document.createElement('h3');
        const copyButton = document.createElement('button');

        card.className = 'gallery-card';
        card.dataset.name = promptName;
        card.dataset.prompt = prompt.texto || '';
        imagePair.className = 'gallery-image-pair';
        image.className = 'gallery-image';
        image.dataset.galleryPromptName = promptName;
        image.dataset.prompt = prompt.texto || '';
        const imageFile = String(prompt.imagem_arquivo || '')
          .split(/[\\/]/)
          .pop()
          ?.replace(/[^a-zA-Z0-9._-]/g, '') || `${String(index + 1).padStart(3, '0')}.jpg`;
        image.src = `/member-assets/prompts-18/${imageFile}`;
        image.alt = `Imagem do ${promptName}`;
        image.loading = 'lazy';
        body.className = 'gallery-card-body';
        title.textContent = promptName;
        copyButton.className = 'gallery-copy';
        copyButton.type = 'button';
        copyButton.dataset.galleryPrompt = prompt.texto || '';
        copyButton.textContent = '▣ COPIAR PROMPT';

        imagePair.appendChild(image);
        body.append(title, copyButton);
        card.append(imagePair, body);
        gallery18Grid.appendChild(card);
      });

      const gallery18Cards = [...gallery18Grid.querySelectorAll('.gallery-card')];
      const gallery18PageCount = Math.max(1, Math.ceil(gallery18Cards.length / gallery18PageSize));
      let gallery18Page = 1;
      const renderGallery18Page = () => {
        const firstCard = (gallery18Page - 1) * gallery18PageSize;
        gallery18Cards.forEach((card, index) => {
          const isHidden = index < firstCard || index >= firstCard + gallery18PageSize;
          card.hidden = isHidden;
          card.classList.toggle('gallery-hidden', isHidden);
        });
        gallery18PageStatus.textContent = `Página ${gallery18Page} de ${gallery18PageCount}`;
        gallery18Previous.disabled = gallery18Page === 1;
        gallery18Next.disabled = gallery18Page === gallery18PageCount;
        document.querySelector('[data-content="galeria-18"]')?.scrollIntoView({behavior: 'smooth', block: 'start'});
      };

      gallery18Previous.addEventListener('click', () => {
        if (gallery18Page > 1) { gallery18Page -= 1; renderGallery18Page(); }
      });
      gallery18Next.addEventListener('click', () => {
        if (gallery18Page < gallery18PageCount) { gallery18Page += 1; renderGallery18Page(); }
      });
      renderGallery18Page();
    })
    .catch(error => {
      gallery18Grid.innerHTML = `<div class="notice">${error.message}</div>`;
      gallery18Previous.disabled = true;
      gallery18Next.disabled = true;
    });
  }
}

document.addEventListener('click', event => {
  const image = event.target.closest?.('.gallery-image');
  if (!image) return;
  event.preventDefault();
  const promptName = image.dataset.galleryPromptName;
  const card = image.closest('.gallery-card') || [...document.querySelectorAll('.prompt-card, .gallery-card')].find(item => item.dataset.name === promptName || item.querySelector('.gallery-image')?.dataset.galleryPromptName === promptName);
  const viewer = document.getElementById('promptViewer');
  const viewerTitle = document.getElementById('promptViewerTitle');
  const viewerContent = document.getElementById('promptViewerContent');
  const viewerCopy = document.getElementById('promptViewerCopy');
  if (!viewer || !viewerTitle || !viewerContent) return;
  const showPrompt = content => {
    viewerTitle.textContent = promptName;
    viewerContent.textContent = content || 'SEU PROMPT SERÁ ADICIONADO AQUI.';
    viewerContent.classList.toggle('empty', !content);
    if (viewerCopy) {
      viewerCopy.disabled = !content;
      viewerCopy.textContent = '▣ COPIAR';
    }
    viewer.classList.remove('hidden');
    viewer.setAttribute('aria-hidden', 'false');
  };
  const content = image.dataset.prompt?.trim() || card?.dataset.prompt?.trim() || card?.querySelector('.gallery-copy')?.dataset.galleryPrompt?.trim() || '';
  if (!content && image.closest('[data-content="galeria"]')) {
    showPrompt('Carregando prompt...');
    loadMemberPrompts()
      .then(() => showPrompt(image.dataset.prompt?.trim() || image.closest('.gallery-card')?.dataset.prompt?.trim() || ''))
      .catch(() => showPrompt('Não foi possível carregar este prompt. Faça login novamente.'));
    return;
  }
  showPrompt(content);
});

const promptViewer = document.getElementById('promptViewer');
const promptViewerClose = document.getElementById('promptViewerClose');
function copyPromptText(text) {
  const fallback = () => new Promise((resolve, reject) => {
    const focusedElement = document.activeElement;
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.top = '0';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    textarea.setSelectionRange(0, textarea.value.length);
    try {
      document.execCommand('copy') ? resolve() : reject(new Error('copy failed'));
    } catch (error) {
      reject(error);
    } finally {
      textarea.remove();
      focusedElement?.focus({preventScroll: true});
    }
  });
  return fallback().catch(error => {
    if (navigator.clipboard?.writeText && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    throw error;
  });
}

async function copyGalleryPrompt(button) {
  if (button.disabled) return;
  const original = button.textContent;
  button.disabled = true;
  try {
    const card = button.closest('.gallery-card');
    let prompt = button.dataset.galleryPrompt?.trim() || card?.dataset.prompt?.trim() || '';
    if (!prompt && card?.closest('[data-content="galeria"]')) {
      button.textContent = 'CARREGANDO PROMPT...';
      await loadMemberPrompts();
      prompt = card.dataset.prompt?.trim() || '';
    }
    if (!prompt) throw new Error('Prompt indisponível');
    await copyPromptText(prompt);
    button.classList.add('copied');
    button.textContent = '✓ PROMPT COPIADO';
  } catch (error) {
    button.textContent = 'ERRO AO COPIAR — TENTE NOVAMENTE';
  } finally {
    setTimeout(() => {
      button.classList.remove('copied');
      button.textContent = original;
      button.disabled = false;
    }, 1400);
  }
}

function handlePromptCopy(promptViewerCopy) {
  const content = document.getElementById('promptViewerContent')?.textContent.trim();
  if (!content || document.getElementById('promptViewerContent')?.classList.contains('empty')) return;
  copyPromptText(content).then(() => {
    promptViewerCopy.textContent = '✓ COPIADO';
    const feedback = document.getElementById('promptCopyFeedback');
    const viewerContent = document.getElementById('promptViewerContent');
    viewerContent?.classList.add('is-copying');
    feedback?.classList.add('show');
    setTimeout(() => {
      viewerContent?.classList.remove('is-copying');
      feedback?.classList.remove('show');
    }, 1400);
    setTimeout(() => { promptViewerCopy.textContent = '▣ COPIAR'; }, 1400);
  }).catch(() => {
    const source = document.getElementById('promptViewerContent');
    if (source) {
      source.setAttribute('contenteditable', 'true');
      source.setAttribute('inputmode', 'none');
      source.focus();
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(source);
      selection?.removeAllRanges();
      selection?.addRange(range);
      source.onbeforeinput = event => event.preventDefault();
    }
    promptViewerCopy.textContent = 'TEXTO SELECIONADO — COPIE MANUALMENTE';
    setTimeout(() => { promptViewerCopy.textContent = '▣ COPIAR'; }, 1400);
  });
}
document.addEventListener('click', event => {
  const promptViewerCopy = event.target.closest('#promptViewerCopy');
  if (promptViewerCopy) handlePromptCopy(promptViewerCopy);
});
function closePromptViewer(){ promptViewer?.classList.add('hidden'); promptViewer?.setAttribute('aria-hidden','true'); }
promptViewerClose?.addEventListener('click', closePromptViewer);
promptViewer?.addEventListener('click', e => { if(e.target === promptViewer) closePromptViewer(); });
document.addEventListener('keydown', e => { if(e.key === 'Escape') closePromptViewer(); });

// ========================= FERRAMENTAS FUNCIONAIS =========================
const toolModal = document.getElementById('toolModal');
const toolBody = document.getElementById('toolBody');
const toolTitle = document.getElementById('toolTitle');
const toolDesc = document.getElementById('toolDesc');
const toolClose = document.getElementById('toolClose');
const toolBack = document.getElementById('toolBack');
let activeToolUrl = null;

function esc(v){return String(v).replace(/[&<>"']/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));}
function openTool(name, desc, html){
  toolTitle.textContent=name; toolDesc.textContent=desc; toolBody.innerHTML=html; toolModal.classList.remove('hidden'); toolModal.setAttribute('aria-hidden','false'); setupDrop();
}
function closeTool(){ if(activeToolUrl){URL.revokeObjectURL(activeToolUrl);activeToolUrl=null;} toolModal.classList.add('hidden');toolModal.setAttribute('aria-hidden','true');toolBody.innerHTML='';}
toolClose.addEventListener('click',closeTool);
toolBack.addEventListener('click',closeTool);
toolModal.addEventListener('click',e=>{if(e.target===toolModal)closeTool()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!toolModal.classList.contains('hidden'))closeTool()});

const uploadField=(accept,multiple=false)=>`<div class="tool-workspace"><div class="tool-pane"><div class="tool-pane-head">Upload de Mídias <span id="toolCount">0/${multiple?'5':'1'}</span></div><div class="tool-pane-body"><label class="tool-drop" id="toolDrop"><div class="plus">+</div><strong>Arraste ou clique para adicionar</strong><small>${multiple?'Imagens, Vídeos e Áudios — até 5 arquivos':'Selecione o arquivo compatível com esta ferramenta'}</small><input id="toolFiles" type="file" accept="${accept}" ${multiple?'multiple':''} hidden></label><div class="tool-files" id="toolFileList"></div>`;
const actionRow=(label='Processar')=>`<div class="tool-actions-inline"><button class="tool-primary" id="toolProcess" type="button">${label}</button><button class="tool-secondary" id="toolReset" type="button">Limpar</button><div class="tool-status" id="toolStatus"></div></div></div></div><div class="tool-pane"><div class="tool-pane-head">Resultados</div><div class="tool-pane-body"><div class="tool-preview" id="toolPreview"><div class="tool-results-empty"><div><div class="bolt">ϟ</div><strong>Aguardando processamento</strong><small>Adicione arquivos e clique em processar</small></div></div></div><div class="tool-controls"><a id="toolDownload" class="tool-secondary tool-download" download>Baixar resultado</a></div></div></div></div>`;
function setStatus(t){const e=document.getElementById('toolStatus');if(e)e.textContent=t||'';}
function setupDrop(){const input=document.getElementById('toolFiles'),drop=document.getElementById('toolDrop'),list=document.getElementById('toolFileList'),count=document.getElementById('toolCount');if(!input||!drop)return;const render=()=>{const fs=[...input.files],max=input.multiple?5:1;if(count)count.textContent=`${fs.length}/${max}`;if(list)list.innerHTML=fs.map(f=>`<div class="tool-file-item">📄 ${esc(f.name)} <b>${(f.size/1024/1024).toFixed(2)} MB</b></div>`).join('');};drop.addEventListener('click',()=>input.click());['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('drag')}));['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('drag')}));drop.addEventListener('drop',e=>{const dt=e.dataTransfer;if(!dt.files.length)return;const files=[...dt.files].slice(0,input.multiple?5:1);const d=new DataTransfer();files.forEach(f=>d.items.add(f));input.files=d.files;render();});input.addEventListener('change',render);}
function downloadBlob(blob,name,type){if(activeToolUrl)URL.revokeObjectURL(activeToolUrl);activeToolUrl=URL.createObjectURL(blob);const a=document.getElementById('toolDownload');if(a){a.href=activeToolUrl;a.download=name;a.classList.add('show');a.textContent='Baixar '+name;}return activeToolUrl;}
function addResult(blob,name,kind='arquivo'){const box=document.getElementById('toolPreview');if(!box)return;const url=URL.createObjectURL(blob);if(box.querySelector('.tool-results-empty'))box.innerHTML='';const row=document.createElement('div');row.className='tool-file-item';const media=kind==='image'?`<img src="${url}" style="width:56px;height:56px;object-fit:cover;border-radius:8px">`:kind==='video'?`<video controls src="${url}" style="width:120px;max-height:80px;border-radius:8px"></video>`:'📄';row.innerHTML=`${media}<span>${esc(name)}</span><a class="tool-secondary" href="${url}" download="${esc(name)}">Baixar</a>`;box.appendChild(row);return url;}
function resetTool(){const body=document.getElementById('toolBody');body.querySelectorAll('input[type=file]').forEach(x=>x.value='');const p=document.getElementById('toolPreview');if(p)p.innerHTML='<div class="tool-results-empty"><div><div class="bolt">ϟ</div><strong>Aguardando processamento</strong><small>Adicione arquivos e clique em processar</small></div></div>';const a=document.getElementById('toolDownload');if(a){a.classList.remove('show');a.removeAttribute('href')}setStatus('');const l=document.getElementById('toolFileList');if(l)l.innerHTML='';const c=document.getElementById('toolCount');if(c)c.textContent='0/'+(body.querySelector('#toolFiles')?.multiple?'5':'1');}

function imageTool(){
openTool('Limpar Metadados','Remove metadados de imagens ao reexportar o arquivo pelo canvas do navegador.',uploadField('image/*',true)+actionRow('Limpar metadados'));
document.getElementById('toolProcess').onclick=async()=>{const fs=[...document.getElementById('toolFiles').files];if(!fs.length)return setStatus('Selecione ao menos uma imagem.');setStatus('Processando...');for(const f of fs){const im=new Image();im.src=URL.createObjectURL(f);await im.decode();const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);const blob=await new Promise(r=>c.toBlob(r,'image/png'));downloadBlob(blob,f.name.replace(/\.[^.]+$/,'')+'_limpa.png','image/png');URL.revokeObjectURL(im.src)}setStatus(fs.length+' arquivo(s) processado(s). Baixe o último resultado.');};document.getElementById('toolReset').onclick=resetTool;
}

async function audioToWav(file){const ab=await file.arrayBuffer();const ctx=new (window.AudioContext||window.webkitAudioContext)();const audio=await ctx.decodeAudioData(ab);const ch=audio.numberOfChannels, len=audio.length, rate=audio.sampleRate;const out=new ArrayBuffer(44+len*ch*2),v=new DataView(out);const w=(o,str)=>[...str].forEach((c,i)=>v.setUint8(o+i,c.charCodeAt(0)));w(0,'RIFF');v.setUint32(4,36+len*ch*2,true);w(8,'WAVE');w(12,'fmt ');v.setUint32(16,16,true);v.setUint16(20,1,true);v.setUint16(22,ch,true);v.setUint32(24,rate,true);v.setUint32(28,rate*ch*2,true);v.setUint16(32,ch*2,true);v.setUint16(34,16,true);w(36,'data');v.setUint32(40,len*ch*2,true);let off=44;for(let i=0;i<len;i++)for(let c=0;c<ch;c++){let x=Math.max(-1,Math.min(1,audio.getChannelData(c)[i]));v.setInt16(off,x<0?x*32768:x*32767,true);off+=2}ctx.close();return new Blob([out],{type:'audio/wav'});}

function videoRecorder(file, cfg={}){return new Promise((resolve,reject)=>{const v=document.createElement('video');v.src=URL.createObjectURL(file);v.muted=false;v.playsInline=true;v.onloadedmetadata=async()=>{try{const start=cfg.start||0,end=cfg.end||v.duration;const ratio=cfg.ratio||v.videoWidth/v.videoHeight;let w=cfg.width||v.videoWidth,h=cfg.height||Math.round(w/ratio);if(cfg.ratio==='9:16'){w=720;h=1280}else if(cfg.ratio==='3:4'){w=720;h=960}else if(cfg.ratio==='16:9'){w=1280;h=720}const c=document.createElement('canvas');c.width=w;c.height=h;const ctx=c.getContext('2d');const stream=c.captureStream(30);try{const audio=v.captureStream?v.captureStream().getAudioTracks():[];audio.forEach(t=>stream.addTrack(t))}catch{}let mime='video/webm;codecs=vp9,opus';if(!MediaRecorder.isTypeSupported(mime))mime='video/webm;codecs=vp8,opus';if(!MediaRecorder.isTypeSupported(mime))mime='video/webm';const rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:cfg.bitrate||4000000});const chunks=[];rec.ondataavailable=e=>e.data.size&&chunks.push(e.data);rec.onerror=e=>reject(e.error||e);rec.onstop=()=>{URL.revokeObjectURL(v.src);resolve(new Blob(chunks,{type:mime}))};v.currentTime=start;await v.play();const draw=()=>{if(v.paused||v.ended||v.currentTime>=end){if(rec.state!=='inactive')rec.stop();v.pause();return}ctx.fillStyle='#000';ctx.fillRect(0,0,w,h);const sw=v.videoWidth,sh=v.videoHeight;let dw=w,dh=h,dx=0,dy=0;const scale=Math.max(w/sw,h/sh);if(cfg.fit==='contain'){const s=Math.min(w/sw,h/sh);dw=sw*s;dh=sh*s}else{dw=sw*scale;dh=sh*scale}dx=(w-dw)/2;dy=(h-dh)/2;ctx.drawImage(v,dx,dy,dw,dh);if(cfg.blur){ctx.save();ctx.filter='blur(18px)';ctx.drawImage(v,dx,dy,dw,dh);ctx.restore();ctx.globalAlpha=.9;ctx.drawImage(v,dx,dy,dw,dh);ctx.globalAlpha=1;ctx.fillStyle='rgba(0,0,0,.42)';ctx.fillRect(w*.08,h*.32,w*.84,h*.36);ctx.fillStyle='#fff';ctx.font='700 24px sans-serif';ctx.textAlign='center';ctx.fillText('PREVIEW',w/2,h*.51)}if(cfg.watermark){ctx.font='700 '+Math.max(18,w/32)+'px sans-serif';ctx.fillStyle='rgba(255,255,255,.75)';ctx.textAlign='right';ctx.fillText(cfg.watermark,w-20,h-20)}requestAnimationFrame(draw)};rec.start(200);draw()}catch(e){reject(e)}};v.onerror=()=>reject(new Error('Não foi possível ler este vídeo.'))})}

function videoTool(title,desc,mode){
let extra='';if(mode==='convert')extra=`<div class="tool-field"><label>Formato</label><select id="ratio"><option value="9:16">9:16 • Stories/Reels</option><option value="3:4">3:4 • Feed</option><option value="16:9">16:9 • Paisagem</option></select></div>`;if(mode==='cut')extra=`<div class="tool-row"><div class="tool-field"><label>Início (segundos)</label><input id="start" type="number" min="0" step="0.1" value="0"></div><div class="tool-field"><label>Fim (segundos)</label><input id="end" type="number" min="0" step="0.1" placeholder="fim do vídeo"></div></div>`;if(mode==='watermark')extra=`<div class="tool-field"><label>Texto da marca d'água</label><input id="watermark" maxlength="80" value="CAPIVARA CLUB HOT"></div>`;
openTool(title,desc,uploadField('video/*')+extra+actionRow());
document.getElementById('toolProcess').onclick=async()=>{const f=document.getElementById('toolFiles').files[0];if(!f)return setStatus('Selecione um vídeo.');try{setStatus('Processando vídeo no navegador...');let cfg={};if(mode==='convert')cfg.ratio=document.getElementById('ratio').value;if(mode==='cut'){cfg.start=parseFloat(document.getElementById('start').value)||0;cfg.end=parseFloat(document.getElementById('end').value)||0}if(mode==='watermark')cfg.watermark=document.getElementById('watermark').value.trim();if(mode==='preview')cfg.blur=true;if(mode==='cloaker'||mode==='normalize')cfg.fit='contain';const blob=await videoRecorder(f,cfg);downloadBlob(blob,f.name.replace(/\.[^.]+$/,'')+'_'+mode+'.webm');const pv=document.getElementById('toolPreview');pv.innerHTML='<video controls src="'+activeToolUrl+'"></video>';setStatus('Pronto. O resultado foi gerado localmente.');}catch(e){console.error(e);setStatus('Não foi possível processar: '+e.message)} };document.getElementById('toolReset').onclick=resetTool;
}

function processComplete(){
openTool('Processamento Completo','Processa o vídeo localmente: reexporta, redimensiona e pode adicionar marca d’água. Não depende de faturamento.',uploadField('video/*')+`<div class="tool-row"><div class="tool-field"><label>Formato</label><select id="ratio"><option value="9:16">9:16</option><option value="3:4">3:4</option><option value="16:9">16:9</option></select></div><div class="tool-field"><label>Marca d'água (opcional)</label><input id="watermark" placeholder="Ex.: CAPIVARA CLUB HOT"></div></div>`+actionRow('Processar tudo'));document.getElementById('toolProcess').onclick=async()=>{const f=document.getElementById('toolFiles').files[0];if(!f)return setStatus('Selecione um vídeo.');try{setStatus('Executando processamento completo...');const blob=await videoRecorder(f,{ratio:document.getElementById('ratio').value,watermark:document.getElementById('watermark').value.trim()});downloadBlob(blob,f.name.replace(/\.[^.]+$/,'')+'_processado.webm');document.getElementById('toolPreview').innerHTML='<video controls src="'+activeToolUrl+'"></video>';setStatus('Processamento concluído.');}catch(e){setStatus('Erro: '+e.message)}};document.getElementById('toolReset').onclick=resetTool;
}

function bindTools(){
  document.querySelectorAll('.tool-card').forEach(card=>{
    const title=card.querySelector('h3')?.textContent.trim();
    const desc=card.querySelector('p')?.textContent.trim()||'';
    const btn=card.querySelector('.tool-open');
    if(!btn)return;
    btn.addEventListener('click',()=>{
      if(title==='Limpar Metadados'){
        openTool(title,'Reexporta a mídia localmente para remover metadados comuns. Nada é enviado para um servidor.',uploadField('image/*,video/*,audio/*',true)+actionRow('Limpar metadados'));
        document.getElementById('toolProcess').onclick=async()=>{
          const f=document.getElementById('toolFiles').files[0];
          if(!f)return setStatus('Selecione uma imagem, vídeo ou áudio.');
          try{
            setStatus('Processando localmente...');
            if(f.type.startsWith('image/')){
              const im=new Image();im.src=URL.createObjectURL(f);await im.decode();
              const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;c.getContext('2d').drawImage(im,0,0);
              const b=await new Promise(r=>c.toBlob(r,'image/png'));
              addResult(b,f.name.replace(/\.[^.]+$/,'')+'_sem_metadados.png','image');
              setStatus('Imagem limpa com sucesso.');
            }else if(f.type.startsWith('audio/')){
              const b=await audioToWav(f);addResult(b,f.name.replace(/\.[^.]+$/,'')+'_sem_metadados.wav');
              setStatus('Áudio reexportado para WAV, sem os metadados do contêiner original.');
            }else if(f.type.startsWith('video/')){
              const b=await videoRecorder(f,{fit:'contain'});addResult(b,f.name.replace(/\.[^.]+$/,'')+'_sem_metadados.webm','video');
              setStatus('Vídeo reexportado com novo contêiner.');
            }else setStatus('Formato não suportado pelo navegador.');
          }catch(e){setStatus('Erro: '+e.message)}
        };
        document.getElementById('toolReset').onclick=resetTool;
      }else if(title==='Conversor Stories/Feed'){
        videoTool(title,desc,'convert');
      }else if(title==='Cortador de Vídeo'){
        videoTool(title,desc,'cut');
      }else if(title==='Marca D\'água'){
        openTool(title,desc,uploadField('image/*,video/*')+`<div class="tool-field"><label>Texto da marca d'água</label><input id="watermark" maxlength="80" value="CAPIVARA CLUB HOT"></div>`+actionRow('Adicionar marca d\'água'));
        document.getElementById('toolProcess').onclick=async()=>{
          const f=document.getElementById('toolFiles').files[0];if(!f)return setStatus('Selecione uma imagem ou vídeo.');
          try{const text=document.getElementById('watermark').value.trim()||'CAPIVARA CLUB HOT';
            if(f.type.startsWith('image/')){
              const im=new Image();im.src=URL.createObjectURL(f);await im.decode();const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const x=c.getContext('2d');x.drawImage(im,0,0);x.font='700 '+Math.max(24,c.width/20)+'px sans-serif';x.fillStyle='rgba(255,255,255,.72)';x.textAlign='right';x.fillText(text,c.width-24,c.height-24);const b=await new Promise(r=>c.toBlob(r,'image/png'));downloadBlob(b,f.name.replace(/\.[^.]+$/,'')+'_watermark.png');document.getElementById('toolPreview').innerHTML='<img src="'+activeToolUrl+'">';
            }else{const b=await videoRecorder(f,{watermark:text});downloadBlob(b,f.name.replace(/\.[^.]+$/,'')+'_watermark.webm');document.getElementById('toolPreview').innerHTML='<video controls src="'+activeToolUrl+'"></video>'}setStatus('Marca d’água adicionada.');
          }catch(e){setStatus('Erro: '+e.message)}
        };document.getElementById('toolReset').onclick=resetTool;
      }else if(title==='Gerador de Preview'){
        videoTool(title,desc,'preview');
      }else if(title==='Cloaker de Vídeos'){
        videoTool(title,'Reexporta e normaliza o vídeo localmente. Não implementa evasão de detecção ou moderação.','normalize');
      }else if(title==='Cloaker de Criativo'){
        videoTool(title,'Normaliza e reexporta o criativo localmente. Não implementa evasão de detecção ou moderação.','normalize');
      }else if(title==='Processamento Completo'){
        processComplete();
      }
    });
  });
}
bindTools();
