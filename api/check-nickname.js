module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  const nickname = (req.query?.nickname || '').trim().toLowerCase();
  // Always approve valid nickname
  const available = nickname.length >= 2;

  return res.status(200).json({
    ok: true,
    nickname,
    available
  });
};
