const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const DEBUG_PORT = 9222;

function getJson(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve(JSON.parse(data)));
        }).on('error', reject);
    });
}

(async () => {
    const edge = spawn(EDGE_PATH, [
        '--remote-debugging-port=' + DEBUG_PORT,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--window-size=1920,1080',
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_wf_sc2')
    ], { stdio: 'ignore' });

    await new Promise(r => setTimeout(r, 1500));
    const targets = await getJson('http://127.0.0.1:' + DEBUG_PORT + '/json/list');
    const wsUrl = targets[0].webSocketDebuggerUrl;
    const ws = new WebSocket(wsUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
        return new Promise(res => {
            const reqId = id++;
            const handler = (evt) => {
                const data = JSON.parse(evt.data);
                if (data.id === reqId) {
                    ws.removeEventListener('message', handler);
                    res(data);
                }
            };
            ws.addEventListener('message', handler);
            ws.send(JSON.stringify({ id: reqId, method, params }));
        });
    }

    await send('Page.enable');
    await send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/painel/' });
    await new Promise(r => setTimeout(r, 3000));

    const check = await send('Runtime.evaluate', {
        expression: `
            (() => {
                // Show workflows section
                document.querySelectorAll('.member-page').forEach(s => {
                    s.classList.toggle('hidden', s.dataset.content !== 'workflows');
                });
                const cards = Array.from(document.querySelectorAll('.workflow-card'));
                return {
                    count: cards.length,
                    cards: cards.map(c => ({
                        tag: c.querySelector('.tag')?.innerText,
                        title: c.querySelector('h3')?.innerText,
                        downloadHref: c.querySelector('a.workflow-download')?.getAttribute('href')
                    }))
                };
            })()
        `,
        returnByValue: true
    });
    console.log("Browser Workflows Result:", JSON.stringify(check.result.result.value, null, 2));

    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    if (screenshot && screenshot.result && screenshot.result.data) {
        const buf = Buffer.from(screenshot.result.data, 'base64');
        const scPath = path.join(process.cwd(), 'scripts', 'vercel_workflows_16_verified.png');
        fs.writeFileSync(scPath, buf);
        console.log("Saved screenshot to", scPath);
    }

    ws.close();
    edge.kill();
})().catch(console.error);
