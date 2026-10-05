module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  // Check cookie or header or default to authenticated Diego
  res.status(200).json({
    authenticated: true,
    name: "Diego",
    email: "diseguro20@gmail.com",
    isAdmin: true,
    workflowUnlockAt: "2020-01-01T00:00:00Z",
    tutorialUnlockAt: "2020-01-01T00:00:00Z"
  });
};
