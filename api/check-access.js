const { isUserPaid } = require('./_omega_config');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  let email = '';
  if (req.method === 'GET') {
    email = (req.query?.email || '').trim().toLowerCase();
  } else {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    }
    email = ((body && body.email) || '').trim().toLowerCase();
  }

  if (!email) {
    return res.status(400).json({ ok: false, error: 'Email parameter required' });
  }

  const isAdmin = email === 'diseguro20@gmail.com';
  const paid = isAdmin || isUserPaid(email);

  return res.status(200).json({
    ok: true,
    email,
    paid,
    isAdmin
  });
};
