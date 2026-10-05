const fs = require('fs');
const path = require('path');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');

  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  try {
    const jsonPath = path.join(__dirname, '..', '..', 'member-assets', 'member_prompts.json');
    if (fs.existsSync(jsonPath)) {
      const data = fs.readFileSync(jsonPath, 'utf8');
      res.setHeader('Content-Type', 'application/json');
      return res.status(200).send(data);
    }
  } catch (err) {}

  res.status(200).json({ prompts: [] });
};
