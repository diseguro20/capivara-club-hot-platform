const { spawn } = require('child_process');
const http = require('http');
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
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_profile_v9alone')
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
    // Navigate to a blank page and test video 9 standalone
    await send('Page.navigate', { url: 'about:blank' });
    await new Promise(r => setTimeout(r, 500));

    const result = await send('Runtime.evaluate', {
        expression: `
            new Promise((resolve) => {
                const v = document.createElement('video');
                v.controls = true;
                v.muted = true;
                document.body.appendChild(v);
                v.src = 'https://github.com/diseguro20/capivara-club-hot-platform/releases/download/v1.0.0-videos/tutorial-09.mp4';
                
                v.onloadedmetadata = () => {
                    resolve({
                        loadedmetadata: true,
                        duration: v.duration,
                        videoWidth: v.videoWidth,
                        videoHeight: v.videoHeight,
                        readyState: v.readyState
                    });
                };

                v.onerror = (e) => {
                    resolve({
                        loadedmetadata: false,
                        error: v.error ? v.error.message || v.error.code : 'unknown error'
                    });
                };

                setTimeout(() => {
                    resolve({
                        timeout: true,
                        duration: v.duration,
                        readyState: v.readyState,
                        networkState: v.networkState,
                        error: v.error ? v.error.message || v.error.code : null
                    });
                }, 8000);
            })
        `,
        awaitPromise: true,
        returnByValue: true
    });

    console.log("Standalone CDN Video 9 Result:", JSON.stringify(result.result.result.value, null, 2));

    ws.close();
    edge.kill();
})().catch(console.error);
