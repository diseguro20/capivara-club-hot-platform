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

  const name = (body.name || '').trim();
  const email = (body.email || '').trim().toLowerCase();
  const password = (body.password || '').trim();

  if (!email || !email.includes('@')) {
    return res.status(400).json({ ok: false, error: 'Por favor, informe um e-mail válido.' });
  }

  if (!password || password.length < 6) {
    return res.status(400).json({ ok: false, error: 'A senha deve conter no mínimo 6 caracteres.' });
  }

  const displayName = name || email.split('@')[0];

  return res.status(201).json({
    ok: true,
    message: 'Conta criada com sucesso!',
    user: {
      name: displayName,
      email: email,
      isAdmin: email === 'diseguro20@gmail.com'
    },
    token: `reg-${Date.now()}-jwt`
  });
};
