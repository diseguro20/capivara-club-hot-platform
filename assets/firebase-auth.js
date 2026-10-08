/**
 * Firebase Authentication & Session Manager
 * Suporta Firebase Auth com sincronização local e serverless
 */

const FIREBASE_CONFIG = {
  apiKey: "AIzaSyB" + "CapivaraClubHotAuth2026MasterKey",
  authDomain: "capivara-club-hot.firebaseapp.com",
  projectId: "capivara-club-hot",
  storageBucket: "capivara-club-hot.appspot.com",
  messagingSenderId: "987112004561",
  appId: "1:987112004561:web:d87b92f00a421b"
};

class CapivaraFirebaseAuth {
  constructor() {
    this.currentUser = null;
    this.listeners = [];
    this.init();
  }

  init() {
    // 1. Check local session
    const saved = localStorage.getItem('capivara_user');
    if (saved) {
      try {
        this.currentUser = JSON.parse(saved);
      } catch (e) {
        this.currentUser = null;
      }
    }

    // Initialize Firebase if SDK is available
    if (typeof firebase !== 'undefined' && firebase.initializeApp) {
      try {
        if (!firebase.apps.length) {
          firebase.initializeApp(FIREBASE_CONFIG);
        }
        this.auth = firebase.auth();
        this.auth.onAuthStateChanged(user => {
          if (user) {
            this.setUser({
              uid: user.uid,
              name: user.displayName || user.email.split('@')[0],
              email: user.email,
              isAdmin: user.email === 'diseguro20@gmail.com'
            });
          }
        });
      } catch (err) {
        console.warn('[Firebase Auth] Iniciando em modo autônomo:', err.message);
      }
    }
  }

  setUser(user) {
    this.currentUser = user;
    if (user) {
      localStorage.setItem('capivara_user', JSON.stringify(user));
      localStorage.setItem('memberEmail', user.email);
      localStorage.setItem('memberName', user.name || 'Membro');
      localStorage.setItem('memberIsAdmin', user.isAdmin ? '1' : '0');
      localStorage.setItem('memberPaid', (user.isAdmin || user.paid) ? '1' : '0');
    } else {
      localStorage.removeItem('capivara_user');
      localStorage.removeItem('memberEmail');
      localStorage.removeItem('memberName');
      localStorage.removeItem('memberIsAdmin');
      localStorage.removeItem('memberPaid');
    }
    this.listeners.forEach(cb => cb(this.currentUser));
  }

  onAuthStateChanged(callback) {
    this.listeners.push(callback);
    callback(this.currentUser);
  }

  async signIn(email, password) {
    email = (email || '').trim().toLowerCase();
    password = (password || '').trim();

    // Master Access: diseguro20@gmail.com / diego123
    if (email === 'diseguro20@gmail.com' && (password === 'diego123' || password === 'diego2001')) {
      const user = {
        uid: 'master-diego-2026',
        name: 'Diego',
        email: 'diseguro20@gmail.com',
        isAdmin: true,
        paid: true
      };
      this.setUser(user);
      return { ok: true, user };
    }

    // Try API endpoint
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        const user = {
          uid: data.uid || `user-${Date.now()}`,
          name: data.name || email.split('@')[0],
          email: data.email || email,
          isAdmin: !!data.isAdmin,
          paid: !!data.paid || !!data.isAdmin
        };
        this.setUser(user);
        return { ok: true, user };
      }
      throw new Error(data.error || 'Credenciais inválidas.');
    } catch (apiErr) {
      // Check registered users in localStorage fallback
      const registered = JSON.parse(localStorage.getItem('capivara_registered_users') || '[]');
      const match = registered.find(u => u.email === email && u.password === password);
      if (match) {
        const user = {
          uid: match.uid,
          name: match.name,
          email: match.email,
          isAdmin: match.email === 'diseguro20@gmail.com'
        };
        this.setUser(user);
        return { ok: true, user };
      }
      throw new Error(apiErr.message || 'E-mail ou senha incorretos.');
    }
  }

  async signUp(name, email, password) {
    email = (email || '').trim().toLowerCase();
    password = (password || '').trim();
    name = (name || '').trim();

    if (!email || !email.includes('@')) {
      throw new Error('E-mail inválido.');
    }
    if (!password || password.length < 6) {
      throw new Error('A senha deve ter pelo menos 6 caracteres.');
    }

    const newUser = {
      uid: `uid-${Date.now()}`,
      name: name || email.split('@')[0],
      email: email,
      password: password,
      createdAt: new Date().toISOString()
    };

    // Save to local registered list
    const registered = JSON.parse(localStorage.getItem('capivara_registered_users') || '[]');
    if (registered.some(u => u.email === email)) {
      throw new Error('Este e-mail já está cadastrado. Faça login.');
    }
    registered.push(newUser);
    localStorage.setItem('capivara_registered_users', JSON.stringify(registered));

    // Try posting to API
    try {
      await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
      });
    } catch(e) {}

    // Auto login
    this.setUser({
      uid: newUser.uid,
      name: newUser.name,
      email: newUser.email,
      isAdmin: newUser.email === 'diseguro20@gmail.com'
    });

    return { ok: true, user: this.currentUser };
  }

  signOut() {
    if (this.auth) {
      try { this.auth.signOut(); } catch(e) {}
    }
    this.setUser(null);
  }
}

window.capivaraAuth = new CapivaraFirebaseAuth();
