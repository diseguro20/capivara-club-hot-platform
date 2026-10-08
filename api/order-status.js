const { callOmegaApi, getTransaction, markUserAsPaid, isUserPaid } = require('./_omega_config');

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  const query = req.query || {};
  const idTransaction = query.idTransaction || query.txId || query.id;
  const emailParam = query.email ? query.email.trim().toLowerCase() : null;

  if (!idTransaction && !emailParam) {
    return res.status(400).json({ error: 'Parâmetro idTransaction ou email obrigatório.' });
  }

  // If email is already marked as paid (or is master admin)
  if (emailParam && isUserPaid(emailParam)) {
    return res.status(200).json({
      ok: true,
      status: 'paid',
      paid: true,
      email: emailParam
    });
  }

  const txInfo = idTransaction ? getTransaction(idTransaction) : null;
  const userEmail = (txInfo && txInfo.email) || emailParam;

  if (userEmail && isUserPaid(userEmail)) {
    return res.status(200).json({
      ok: true,
      status: 'paid',
      paid: true,
      email: userEmail
    });
  }

  if (!idTransaction) {
    return res.status(200).json({
      ok: true,
      status: 'pending',
      paid: false
    });
  }

  try {
    const omegaTx = await callOmegaApi(`/gateway/transactions?id=${encodeURIComponent(idTransaction)}`);
    const status = (omegaTx.status || '').toUpperCase();

    if (status === 'COMPLETED' || status === 'PAID' || status === 'CONFIRMED' || status === 'APPROVED') {
      const emailToUnlock = userEmail || omegaTx.client?.email;
      if (emailToUnlock) {
        markUserAsPaid(emailToUnlock, {
          idTransaction,
          amount: omegaTx.amount,
          email: emailToUnlock,
          name: (txInfo && txInfo.name) || omegaTx.client?.name
        });
      }

      return res.status(200).json({
        ok: true,
        status: 'paid',
        paid: true,
        email: emailToUnlock,
        name: (txInfo && txInfo.name) || omegaTx.client?.name,
        redirect: '/paginas/painel.html?paid=true'
      });
    }

    return res.status(200).json({
      ok: true,
      status: status.toLowerCase() || 'pending',
      paid: false
    });
  } catch (err) {
    console.warn(`[Omega Status Error] tx: ${idTransaction}`, err.message);
    // If Omega Pay lookup had a transient issue, fallback to recorded state
    return res.status(200).json({
      ok: true,
      status: 'pending',
      paid: false
    });
  }
};
