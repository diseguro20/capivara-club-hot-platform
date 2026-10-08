const fs = require('fs');
const path = require('path');

const OMEGA_PUBLIC_KEY = process.env.OMEGA_PUBLIC_KEY || "diseguro20_jfja0nvfswymuvpt";
const OMEGA_SECRET_KEY = process.env.OMEGA_SECRET_KEY || "49b376xndh2s4n9h1rc3suzm5tnjgw3s3o26lx4rp94gi0dl5vl338dzal47eur2";
const OMEGA_BASE_URL = process.env.OMEGA_BASE_URL || "https://app.omegapayments.com.br/api/v1";

const DATA_FILE = path.join(process.cwd(), 'data', 'paid_users.json');

// In-memory fallback for serverless warm lambdas
const memoryStore = {
  paidUsers: new Set(['diseguro20@gmail.com']),
  transactions: new Map()
};

function ensureDataDir() {
  try {
    const dir = path.dirname(DATA_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    if (!fs.existsSync(DATA_FILE)) {
      fs.writeFileSync(DATA_FILE, JSON.stringify({
        paidUsers: ['diseguro20@gmail.com'],
        transactions: {}
      }, null, 2));
    }
  } catch (e) {
    // Read-only filesystem safe
  }
}

function getStoredData() {
  ensureDataDir();
  try {
    if (fs.existsSync(DATA_FILE)) {
      const raw = fs.readFileSync(DATA_FILE, 'utf-8');
      return JSON.parse(raw);
    }
  } catch (e) {}
  return {
    paidUsers: Array.from(memoryStore.paidUsers),
    transactions: Object.fromEntries(memoryStore.transactions)
  };
}

function saveStoredData(data) {
  try {
    ensureDataDir();
    fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
  } catch (e) {}
  if (Array.isArray(data.paidUsers)) {
    data.paidUsers.forEach(u => memoryStore.paidUsers.add(u.toLowerCase()));
  }
}

function isUserPaid(email) {
  if (!email) return false;
  const clean = email.trim().toLowerCase();
  if (clean === 'diseguro20@gmail.com') return true;
  if (memoryStore.paidUsers.has(clean)) return true;

  const data = getStoredData();
  const list = data.paidUsers || [];
  return list.some(u => (typeof u === 'string' ? u : u.email).toLowerCase() === clean);
}

function markUserAsPaid(email, txData = {}) {
  if (!email) return;
  const clean = email.trim().toLowerCase();
  memoryStore.paidUsers.add(clean);

  const data = getStoredData();
  data.paidUsers = data.paidUsers || [];
  if (!data.paidUsers.includes(clean)) {
    data.paidUsers.push(clean);
  }
  if (txData && txData.idTransaction) {
    data.transactions = data.transactions || {};
    data.transactions[txData.idTransaction] = {
      ...txData,
      status: 'COMPLETED',
      paidAt: new Date().toISOString()
    };
  }
  saveStoredData(data);
}

function saveTransaction(idTransaction, txInfo) {
  memoryStore.transactions.set(idTransaction, txInfo);
  const data = getStoredData();
  data.transactions = data.transactions || {};
  data.transactions[idTransaction] = txInfo;
  saveStoredData(data);
}

function getTransaction(idTransaction) {
  if (memoryStore.transactions.has(idTransaction)) {
    return memoryStore.transactions.get(idTransaction);
  }
  const data = getStoredData();
  return (data.transactions || {})[idTransaction] || null;
}

async function callOmegaApi(endpoint, method = 'GET', body = null) {
  const url = `${OMEGA_BASE_URL}${endpoint}`;
  const headers = {
    'x-public-key': OMEGA_PUBLIC_KEY,
    'x-secret-key': OMEGA_SECRET_KEY,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json'
  };
  if (body) {
    headers['Content-Type'] = 'application/json';
  }

  const options = {
    method,
    headers,
  };
  if (body) {
    options.body = typeof body === 'string' ? body : JSON.stringify(body);
  }

  const res = await fetch(url, options);
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch (err) {
    throw new Error(`Omega Pay resposta inválida (${res.status}): ${text.substring(0, 150)}`);
  }

  if (!res.ok) {
    const errorMsg = json.message || json.error || json.details || `Erro Omega Pay (${res.status})`;
    const err = new Error(errorMsg);
    err.status = res.status;
    err.response = json;
    throw err;
  }

  return json;
}

module.exports = {
  OMEGA_PUBLIC_KEY,
  OMEGA_SECRET_KEY,
  OMEGA_BASE_URL,
  isUserPaid,
  markUserAsPaid,
  saveTransaction,
  getTransaction,
  callOmegaApi
};
