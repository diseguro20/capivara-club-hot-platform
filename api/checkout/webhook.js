const { markUserAsPaid } = require('../_omega_config');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
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

  console.log('[Omega Pay Webhook Received]', JSON.stringify(body));

  // Possible webhook formats from Omega Pay:
  // 1. { event: 'TRANSACTION_PAID', data: { id, client: { email }, amount, ... } }
  // 2. { status: 'COMPLETED', id, client: { email } }
  // 3. { transactionId, status: 'PAID' }
  const status = (body.status || (body.data && body.data.status) || body.event || '').toUpperCase();
  const email = (
    (body.client && body.client.email) ||
    (body.data && body.data.client && body.data.client.email) ||
    (body.data && body.data.email) ||
    body.email
  );
  const idTransaction = body.id || (body.data && body.data.id) || body.transactionId;

  if (['COMPLETED', 'PAID', 'CONFIRMED', 'TRANSACTION_PAID', 'APPROVED'].includes(status)) {
    if (email) {
      markUserAsPaid(email, {
        idTransaction,
        amount: body.amount || (body.data && body.data.amount),
        email,
        name: (body.client && body.client.name) || (body.data && body.data.client && body.data.client.name)
      });
      console.log(`[Omega Pay Webhook] Acesso liberado com sucesso para ${email}!`);
    }
  }

  return res.status(200).json({
    received: true,
    status: 'ok'
  });
};
