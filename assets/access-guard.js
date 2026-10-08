/**
 * Capivara Club Hot - Access Guard & Payment Gate
 * Integrado à Omega Pay
 */

(function initAccessGuard() {
  const MASTER_ADMIN_EMAIL = 'diseguro20@gmail.com';

  function getUserSession() {
    try {
      const raw = localStorage.getItem('capivara_user');
      if (raw) return JSON.parse(raw);
    } catch (e) {}

    const email = localStorage.getItem('memberEmail');
    const isPaid = localStorage.getItem('memberPaid') === '1';
    if (email) {
      return {
        email: email.trim().toLowerCase(),
        name: localStorage.getItem('memberName') || email.split('@')[0],
        paid: isPaid || email.trim().toLowerCase() === MASTER_ADMIN_EMAIL
      };
    }
    return null;
  }

  function saveUserSession(email, name, paid = true) {
    const cleanEmail = email.trim().toLowerCase();
    const session = {
      email: cleanEmail,
      name: name || cleanEmail.split('@')[0],
      paid: !!paid,
      isAdmin: cleanEmail === MASTER_ADMIN_EMAIL,
      unlockedAt: new Date().toISOString()
    };
    localStorage.setItem('capivara_user', JSON.stringify(session));
    localStorage.setItem('memberEmail', cleanEmail);
    localStorage.setItem('memberName', session.name);
    localStorage.setItem('memberPaid', paid ? '1' : '0');
    return session;
  }

  // Handle URL params
  const urlParams = new URLSearchParams(window.location.search);
  const paidParam = urlParams.get('paid');
  const emailParam = urlParams.get('email');

  if (paidParam === 'true') {
    if (emailParam) {
      saveUserSession(emailParam, emailParam.split('@')[0], true);
    } else {
      const current = getUserSession();
      if (current) saveUserSession(current.email, current.name, true);
    }
  }

  function createPaywallOverlay() {
    let overlay = document.getElementById('paywallGateScreen');
    if (overlay) return overlay;

    overlay = document.createElement('div');
    overlay.id = 'paywallGateScreen';
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      z-index: 999999;
      background: radial-gradient(circle at 50% 20%, #1a0826 0%, #050304 80%);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      color: #f3f4f6;
      backdrop-filter: blur(12px);
    `;

    overlay.innerHTML = `
      <div style="
        width: 100%;
        max-width: 480px;
        background: rgba(18, 12, 28, 0.95);
        border: 1px solid rgba(0, 240, 255, 0.35);
        border-radius: 20px;
        padding: 36px 30px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), 0 0 35px rgba(0, 240, 255, 0.15);
        text-align: center;
        box-sizing: border-box;
      ">
        <div style="display:inline-flex; align-items:center; justify-content:center; width:64px; height:64px; border-radius:50%; background:rgba(0,240,255,0.1); border:1px solid rgba(0,240,255,0.3); margin-bottom:16px;">
          <span style="font-size:30px;">🔒</span>
        </div>
        
        <div style="font-size:12px; font-weight:800; color:#00f0ff; letter-spacing:2px; text-transform:uppercase; margin-bottom:6px;">
          CONTEÚDO RESTRITO
        </div>
        
        <h2 style="font-size:24px; font-weight:800; margin:0 0 10px; color:#ffffff; letter-spacing:-0.5px;">
          Área Exclusiva para Membros
        </h2>
        
        <p style="font-size:14px; line-height:1.6; color:#94a3b8; margin:0 0 24px;">
          Para acessar todos os <strong>16 Workflows ComfyUI</strong>, os <strong>10 Tutoriais em Vídeo 1080p</strong> e os <strong>750+ Prompts +18</strong>, adquira seu acesso oficial.
        </p>

        <a href="/?checkout=true" style="
          display: block;
          width: 100%;
          box-sizing: border-box;
          background: linear-gradient(135deg, #ec4899, #f43f5e);
          color: #ffffff;
          padding: 16px;
          border-radius: 12px;
          font-size: 15px;
          font-weight: 800;
          text-decoration: none;
          letter-spacing: 0.5px;
          box-shadow: 0 8px 25px rgba(236, 72, 153, 0.45);
          transition: transform 0.2s ease;
          margin-bottom: 20px;
        " onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='none'">
          ⚡ GARANTIR MEU ACESSO AGORA — R$ 87,90
        </a>

        <div style="border-top:1px solid rgba(255,255,255,0.1); padding-top:20px; margin-top:20px;">
          <div style="font-size:13px; font-weight:600; color:#cbd5e1; margin-bottom:10px;">
            Já realizou o pagamento via PIX?
          </div>
          
          <div style="display:flex; gap:8px; margin-bottom:12px;">
            <input id="paywallEmailInput" type="email" placeholder="Seu e-mail da compra" style="
              flex: 1;
              background: rgba(10, 6, 16, 0.9);
              border: 1px solid rgba(255, 255, 255, 0.2);
              border-radius: 8px;
              padding: 10px 14px;
              color: #ffffff;
              font-size: 13px;
              outline: none;
            ">
            <button id="paywallVerifyBtn" type="button" style="
              background: rgba(0, 240, 255, 0.15);
              border: 1px solid #00f0ff;
              border-radius: 8px;
              color: #00f0ff;
              font-weight: 700;
              font-size: 13px;
              padding: 10px 16px;
              cursor: pointer;
              white-space: nowrap;
            ">Validar</button>
          </div>
          
          <div id="paywallStatusMsg" style="font-size:12px; min-height:16px; line-height:1.4;"></div>
        </div>

        <div style="margin-top:16px; display:flex; justify-content:center; gap:16px; font-size:12px; color:#64748b;">
          <a href="/" style="color:#94a3b8; text-decoration:none;">← Voltar ao Início</a>
          <span>•</span>
          <a href="#" id="paywallAdminShortcut" style="color:#64748b; text-decoration:none;">Acesso Master (Diego)</a>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    // Setup events
    const verifyBtn = document.getElementById('paywallVerifyBtn');
    const emailInput = document.getElementById('paywallEmailInput');
    const statusMsg = document.getElementById('paywallStatusMsg');
    const adminShortcut = document.getElementById('paywallAdminShortcut');

    if (verifyBtn && emailInput) {
      verifyBtn.addEventListener('click', async () => {
        const val = emailInput.value.trim().toLowerCase();
        if (!val || !val.includes('@')) {
          statusMsg.style.color = '#f43f5e';
          statusMsg.textContent = 'Informe um e-mail válido.';
          return;
        }

        verifyBtn.disabled = true;
        verifyBtn.textContent = 'Checando...';
        statusMsg.style.color = '#94a3b8';
        statusMsg.textContent = 'Consultando gateway de pagamento...';

        try {
          const res = await fetch(`/api/check-access?email=${encodeURIComponent(val)}`);
          const data = await res.json();
          if (data.ok && data.paid) {
            saveUserSession(val, val.split('@')[0], true);
            statusMsg.style.color = '#00f0ff';
            statusMsg.textContent = '✅ Pagamento confirmado! Liberando acesso...';
            setTimeout(() => {
              unlockAccess();
            }, 800);
          } else {
            statusMsg.style.color = '#f43f5e';
            statusMsg.textContent = '❌ Pagamento pendente para este e-mail. Finalize sua compra para liberar.';
            verifyBtn.disabled = false;
            verifyBtn.textContent = 'Validar';
          }
        } catch (err) {
          statusMsg.style.color = '#f43f5e';
          statusMsg.textContent = 'Erro ao verificar. Tente novamente.';
          verifyBtn.disabled = false;
          verifyBtn.textContent = 'Validar';
        }
      });
    }

    if (adminShortcut) {
      adminShortcut.addEventListener('click', (e) => {
        e.preventDefault();
        const pass = prompt('Digite a senha master do administrador:');
        if (pass === 'diego123' || pass === 'diego2001') {
          saveUserSession(MASTER_ADMIN_EMAIL, 'Diego Seguro', true);
          unlockAccess();
        } else if (pass !== null) {
          alert('Senha incorreta.');
        }
      });
    }

    return overlay;
  }

  function unlockAccess() {
    const overlay = document.getElementById('paywallGateScreen');
    if (overlay) overlay.style.display = 'none';

    const app = document.getElementById('app');
    if (app) app.style.setProperty('display', 'block', 'important');

    const loginScreen = document.getElementById('loginScreen');
    if (loginScreen) loginScreen.style.setProperty('display', 'none', 'important');

    const forcePassword = document.getElementById('forcePasswordScreen');
    if (forcePassword) forcePassword.style.setProperty('display', 'none', 'important');

    // Show celebratory banner if recently paid
    if (window.location.search.includes('paid=true') && !document.getElementById('welcomePaidToast')) {
      const toast = document.createElement('div');
      toast.id = 'welcomePaidToast';
      toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 99999;
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.95), rgba(2, 132, 199, 0.95));
        color: #040810;
        padding: 16px 22px;
        border-radius: 12px;
        font-weight: 800;
        font-size: 14px;
        box-shadow: 0 10px 30px rgba(0, 240, 255, 0.4);
        display: flex;
        align-items: center;
        gap: 10px;
      `;
      toast.innerHTML = '<span>🎉 Parabéns! Seu pagamento foi aprovado. Acesso 100% liberado!</span>';
      document.body.appendChild(toast);
      setTimeout(() => { toast.remove(); }, 6000);
    }
  }

  function lockAccess() {
    const app = document.getElementById('app');
    if (app) app.style.setProperty('display', 'none', 'important');
    createPaywallOverlay();
  }

  async function checkPermission() {
    const user = getUserSession();

    // If master admin -> immediate access
    if (user && user.email === MASTER_ADMIN_EMAIL) {
      unlockAccess();
      return;
    }

    // If user has paid flag stored in session
    if (user && user.paid) {
      unlockAccess();
      // Verify asynchronously with server
      try {
        const res = await fetch(`/api/check-access?email=${encodeURIComponent(user.email)}`);
        const data = await res.json();
        if (data.ok && !data.paid) {
          // In case access was revoked
          lockAccess();
        }
      } catch (e) {}
      return;
    }

    // If email is in localStorage but no paid flag, check API
    if (user && user.email) {
      try {
        const res = await fetch(`/api/check-access?email=${encodeURIComponent(user.email)}`);
        const data = await res.json();
        if (data.ok && data.paid) {
          saveUserSession(user.email, user.name, true);
          unlockAccess();
          return;
        }
      } catch (e) {}
    }

    // Default: block access and show paywall
    lockAccess();
  }

  // Execute as soon as DOM is ready or immediately if already loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkPermission);
  } else {
    checkPermission();
  }

  window.capivaraAccessGuard = {
    getUserSession,
    saveUserSession,
    unlockAccess,
    lockAccess,
    checkPermission
  };
})();
