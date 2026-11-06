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
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_t8_proper')
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

    await send('Runtime.evaluate', {
        expression: `
            localStorage.setItem("capivara_user", JSON.stringify({ email: "diseguro20@gmail.com" }));
            localStorage.setItem("capivara_logged_in", "true");
            document.querySelectorAll('.member-page').forEach(s => {
                s.classList.toggle('hidden', s.dataset.content !== 'tutoriais');
            });
        `
    });
    await new Promise(r => setTimeout(r, 4000));

    const result = await send('Runtime.evaluate', {
        expression: `
            (async () => {
                const v8 = document.querySelectorAll('video')[7];
                v8.muted = true;
                v8.play();
                v8.scrollIntoView({ behavior: 'instant', block: 'center' });
                await new Promise(r => setTimeout(r, 3000));
                return {
                    tutorial: 8,
                    currentTime: v8.currentTime,
                    duration: v8.duration,
                    videoWidth: v8.videoWidth,
                    videoHeight: v8.videoHeight,
                    readyState: v8.readyState,
                    currentSrc: v8.currentSrc,
                    paused: v8.paused,
                    error: v8.error ? v8.error.message : null
                };
            })()
        `,
        awaitPromise: true,
        returnByValue: true
    });
    console.log("Tutorial 08 Play Result:", JSON.stringify(result.result.result.value, null, 2));

    const fs = require('fs');
    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    if (screenshot && screenshot.result && screenshot.result.data) {
        const buf = Buffer.from(screenshot.result.data, 'base64');
        const scPath = path.join(process.cwd(), 'scripts', 'tutorial_08_live_streaming_verified.png');
        fs.writeFileSync(scPath, buf);
        console.log("Saved live screenshot to", scPath);
    }

    ws.close();
    edge.kill();
})().catch(console.error);
