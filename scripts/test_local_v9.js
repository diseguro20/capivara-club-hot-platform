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
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_profile_direct9')
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
    const filePath = 'file:///' + path.resolve('videos-tutoriais/tutorial-09.mp4').replace(/\\/g, '/');
    console.log('Navigating to', filePath);
    await send('Page.navigate', { url: filePath });
    await new Promise(r => setTimeout(r, 4000));

    const check = await send('Runtime.evaluate', {
        expression: `
            (() => {
                const v = document.querySelector('video');
                if (!v) return { noVideo: true };
                return {
                    src: v.currentSrc,
                    duration: v.duration,
                    readyState: v.readyState,
                    videoWidth: v.videoWidth,
                    videoHeight: v.videoHeight,
                    error: v.error ? v.error.message : null
                };
            })()
        `,
        returnByValue: true
    });

    console.log('Direct Edge file check:', JSON.stringify(check.result.result.value, null, 2));

    ws.close();
    edge.kill();
})().catch(console.error);
