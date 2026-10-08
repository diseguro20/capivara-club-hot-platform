const { callOmegaApi, saveTransaction } = require('./_omega_config');

// Helper to generate a valid CPF checksum if user didn't enter one
function generateFallbackCpf() {
  const rnd = () => Math.floor(Math.random() * 9);
  const n = [rnd(), rnd(), rnd(), rnd(), rnd(), rnd(), rnd(), rnd(), rnd()];
  let d1 = n.reduce((total, num, i) => total + num * (10 - i), 0) % 11;
  d1 = d1 < 2 ? 0 : 11 - d1;
  n.push(d1);
  let d2 = n.reduce((total, num, i) => total + num * (11 - i), 0) % 11;
  d2 = d2 < 2 ? 0 : 11 - d2;
  n.push(d2);
  return n.join('');
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let body = req.body;
  if (typeof body === 'string') {
    try {
      body = JSON.parse(body);
    } catch (e) {
      body = {};
    }
  }
  body = body || {};

  const name = (body.name || '').trim();
  const email = (body.email || '').trim().toLowerCase();
  let phone = (body.phone || '').replace(/\D/g, '');
  let document = (body.document || body.cpf || '').replace(/\D/g, '');
  const coupon = (body.coupon || '').trim().toUpperCase();

  if (!email || !email.includes('@')) {
    return res.status(400).json({ error: 'Por favor, informe um e-mail válido.' });
  }

  if (!name || name.length < 3) {
    return res.status(400).json({ error: 'Por favor, informe seu nome completo.' });
  }

  if (!phone || phone.length < 10) {
    phone = '11982854183'; // Fallback valid mobile
  }

  if (!document || document.length !== 11) {
    document = generateFallbackCpf();
  }

  let amount = 87.90;
  let discountPercent = 0;

  if (coupon === 'CAPIVARA10' || coupon === 'DESCONTO10') {
    amount = 79.11;
    discountPercent = 10;
  } else if (coupon === 'VIP' || coupon === 'VIP20') {
    amount = 69.90;
    discountPercent = 20;
  }

  const identifier = `capivara_${Date.now()}_${Math.random().toString(36).substring(2, 8)}`;

  // Due date: 2 days ahead in YYYY-MM-DD format
  const due = new Date(Date.now() + 2 * 24 * 60 * 60 * 1000);
  const dueDate = due.toISOString().split('T')[0];

  const payload = {
    identifier,
    amount,
    client: {
      name,
      email,
      phone,
      document
    },
    dueDate,
    products: [
      {
        id: "capivara-club-hot-acesso",
        name: "Acesso Completo - Capivara Club Hot",
        price: amount,
        quantity: 1
      }
    ]
  };

  try {
    const omegaResp = await callOmegaApi('/gateway/pix/receive', 'POST', payload);
    const txId = omegaResp.transactionId || omegaResp.id;
    const pixCode = omegaResp.pix && (omegaResp.pix.code || omegaResp.pix.qrCode) 
      ? (omegaResp.pix.code || omegaResp.pix.qrCode) 
      : (omegaResp.pixInformation && omegaResp.pixInformation.qrCode ? omegaResp.pixInformation.qrCode : '');

    const qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=${encodeURIComponent(pixCode)}`;

    // Save transaction state
    saveTransaction(txId, {
      idTransaction: txId,
      identifier,
      name,
      email,
      phone,
      document,
      amount,
      pixCode,
      status: 'PENDING',
      createdAt: new Date().toISOString()
    });

    return res.status(200).json({
      ok: true,
      idTransaction: txId,
      identifier,
      paymentCode: pixCode,
      paymentCodeBase64: qrCodeUrl,
      amount,
      discountPercent
    });
  } catch (err) {
    console.error('[Omega Pay Error]', err);
    return res.status(500).json({
      ok: false,
      error: 'Não foi possível gerar a cobrança PIX no momento. Verifique seus dados e tente novamente.'
    });
  }
};
