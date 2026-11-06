const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const fs = require('fs');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const DEBUG_PORT = 9233;
const USER_DATA = path.join(process.cwd(), '.temp_edge_vercel_live3');

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
    if (!fs.existsSync(USER_DATA)) fs.mkdirSync(USER_DATA, { recursive: true });
    const edge = spawn(EDGE_PATH, [
        '--remote-debugging-port=' + DEBUG_PORT,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--window-size=1400,900',
        '--user-data-dir=' + USER_DATA
    ], { stdio: 'ignore' });

    try {
        await new Promise(r => setTimeout(r, 1800));
        const targets = await getJson('http://127.0.0.1:' + DEBUG_PORT + '/json/list');
        const ws = new WebSocket(targets[0].webSocketDebuggerUrl);
        await new Promise(r => ws.onopen = r);

        let id = 1;
        function send(method, params = {}) {
            return new Promise(res => {
                const reqId = id++;
                const handler = (evt) => {
                    const msg = JSON.parse(evt.data);
                    if (msg.id === reqId) {
                        ws.removeEventListener('message', handler);
                        res(msg.result);
                    }
                };
                ws.addEventListener('message', handler);
                ws.send(JSON.stringify({ id: reqId, method, params }));
            });
        }

        async function evalJs(expr) {
            const res = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
            return res && res.result ? res.result.value : null;
        }

        await send('Page.enable');
        await send('Runtime.enable');

        console.log('Navegando para https://capivara-club-hot.vercel.app ...');
        await send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/' });
        await new Promise(r => setTimeout(r, 2500));

        const locked = await evalJs(`document.getElementById('headerMembersBtn').classList.contains('locked')`);
        const text = await evalJs(`document.getElementById('headerMembersBtn').innerText`);
        console.log('Vercel Producao - Botao de membros bloqueado para novos leads:', locked);
        console.log('Vercel Producao - Texto do botao:', text);

        ws.close();
        edge.kill();
        fs.rmSync(USER_DATA, { recursive: true, force: true });
    } catch(e) {
        console.error(e);
        edge.kill();
    }
})();
