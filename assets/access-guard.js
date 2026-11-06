/**
 * Capivara Club Hot - Access Guard
 * ACESSO 100% GRATUITO E LIBERADO PARA TODOS
 */

(function initAccessGuard() {
  const MASTER_ADMIN_EMAIL = 'diseguro20@gmail.com';

  function getUserSession() {
    try {
      const raw = localStorage.getItem('capivara_user');
      if (raw) return JSON.parse(raw);
    } catch (e) {}

    const email = localStorage.getItem('memberEmail') || 'membro@capivaraclubhot.com';
    return {
      email: email.trim().toLowerCase(),
      name: localStorage.getItem('memberName') || 'Membro VIP',
      paid: true,
      isAdmin: email.trim().toLowerCase() === MASTER_ADMIN_EMAIL
    };
  }

  function saveUserSession(email, name, paid = true) {
    const cleanEmail = (email || 'membro@capivaraclubhot.com').trim().toLowerCase();
    const session = {
      email: cleanEmail,
      name: name || cleanEmail.split('@')[0],
      paid: true,
      isAdmin: cleanEmail === MASTER_ADMIN_EMAIL,
      unlockedAt: new Date().toISOString()
    };
    try {
      localStorage.setItem('capivara_user', JSON.stringify(session));
      localStorage.setItem('memberEmail', cleanEmail);
      localStorage.setItem('memberName', session.name);
      localStorage.setItem('memberPaid', '1');
    } catch (e) {}
    return session;
  }

  function unlockAccess() {
    // Remove any paywall or modal that could block the screen
    const overlay = document.getElementById('paywallGateScreen');
    if (overlay) overlay.style.display = 'none';

    const app = document.getElementById('app');
    if (app) {
      app.style.setProperty('display', 'block', 'important');
      app.classList.remove('hidden');
    }

    const loginScreen = document.getElementById('loginScreen');
    if (loginScreen) loginScreen.style.setProperty('display', 'none', 'important');

    const forcePassword = document.getElementById('forcePasswordScreen');
    if (forcePassword) forcePassword.style.setProperty('display', 'none', 'important');

    // Remove any workflow locking classes
    document.querySelectorAll('.workflow-locked').forEach(el => {
      el.classList.remove('workflow-locked');
      el.style.filter = 'none';
      el.style.opacity = '1';
      el.style.pointerEvents = 'auto';
    });

    // Ensure session is active
    let session = getUserSession();
    if (!session || !session.email) {
      saveUserSession('membro@capivaraclubhot.com', 'Membro VIP', true);
    }
  }

  function lockAccess() {
    // In free mode, access is never locked!
    unlockAccess();
  }

  function checkPermission() {
    unlockAccess();
  }

  // Execute immediately and on DOM load
  unlockAccess();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', unlockAccess);
  } else {
    unlockAccess();
  }

  window.capivaraAccessGuard = {
    getUserSession,
    saveUserSession,
    unlockAccess,
    lockAccess,
    checkPermission
  };
})();
