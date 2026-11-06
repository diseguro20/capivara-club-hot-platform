const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const fs = require('fs');

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
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_t8_live')
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
    console.log("Navigating to https://capivara-club-hot.vercel.app/painel/ ...");
    await send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/painel/' });
    await new Promise(r => setTimeout(r, 3000));

    // Authenticate and open tutoriais tab
    await send('Runtime.evaluate', {
        expression: `
            localStorage.setItem("capivara_user", JSON.stringify({ email: "diseguro20@gmail.com" }));
            localStorage.setItem("capivara_logged_in", "true");
            document.querySelectorAll('.member-page').forEach(s => {
                s.classList.toggle('hidden', s.dataset.content !== 'tutoriais');
            });
        `
    });
    await new Promise(r => setTimeout(r, 3000));

    // Play Tutorial 08 (index 7)
    const playResult = await send('Runtime.evaluate', {
        expression: `
            (async () => {
                const vids = Array.from(document.querySelectorAll('video'));
                const v8 = vids[7];
                if (!v8) return { error: "v8 not found" };
                v8.muted = true;
                v8.currentTime = 5;
                v8.play();
                await new Promise(r => setTimeout(r, 2000));
                v8.scrollIntoView({ behavior: 'instant', block: 'center' });
                return {
                    tutorial: 8,
                    currentTime: v8.currentTime,
                    duration: v8.duration,
                    videoWidth: v8.videoWidth,
                    videoHeight: v8.videoHeight,
                    readyState: v8.readyState,
                    currentSrc: v8.currentSrc
                };
            })()
        `,
        awaitPromise: true,
        returnByValue: true
    });
    console.log("Tutorial 08 Live Playback:", JSON.stringify(playResult.result.result.value, null, 2));

    await new Promise(r => setTimeout(r, 1000));

    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    if (screenshot && screenshot.result && screenshot.result.data) {
        const buf = Buffer.from(screenshot.result.data, 'base64');
        const scPath = path.join(process.cwd(), 'scripts', 'vercel_tutorial_08_fixed.png');
        fs.writeFileSync(scPath, buf);
        console.log("Saved live screenshot to", scPath);
    }

    ws.close();
    edge.kill();
})().catch(console.error);
