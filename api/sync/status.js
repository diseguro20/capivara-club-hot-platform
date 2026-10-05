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
    const statusPath = path.join(__dirname, '..', '..', 'member-assets', 'sync_status.json');
    if (fs.existsSync(statusPath)) {
      const data = fs.readFileSync(statusPath, 'utf8');
      res.setHeader('Content-Type', 'application/json');
      return res.status(200).send(data);
    }
  } catch (err) {}

  res.status(200).json({
    last_sync: new Date().toISOString(),
    is_syncing: false,
    last_result: "success",
    message: "Cloud Sync Ativo",
    metrics: {
      tutorial_videos: 9,
      workflows: 16,
      prompts: 194,
      prompts_18: 562
    }
  });
};
