const { isUserPaid } = require('./_omega_config');

module.exports = (req, res) => {
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

  const email = (body.email || '').trim().toLowerCase();
  const password = (body.password || '').trim();

  // Master access: diseguro20@gmail.com
  if (email === 'diseguro20@gmail.com' && (password === 'diego123' || password === 'diego2001')) {
    return res.status(200).json({
      ok: true,
      name: "Diego",
      email: "diseguro20@gmail.com",
      isAdmin: true,
      paid: true,
      token: "session-master-diego-jwt",
      workflowUnlockAt: "2020-01-01T00:00:00Z",
      tutorialUnlockAt: "2020-01-01T00:00:00Z"
    });
  }

  const paid = isUserPaid(email);

  if (email && password && password.length >= 4) {
    const displayName = email.split('@')[0].toUpperCase();
    return res.status(200).json({
      ok: true,
      name: displayName,
      email: email,
      isAdmin: false,
      paid: paid,
      token: `session-${Date.now()}-jwt`,
      workflowUnlockAt: "2020-01-01T00:00:00Z",
      tutorialUnlockAt: "2020-01-01T00:00:00Z"
    });
  }

  return res.status(401).json({
    ok: false,
    error: 'Credenciais inválidas. Verifique seu e-mail e senha.'
  });
};
