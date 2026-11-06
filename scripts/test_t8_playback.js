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
        '--window-size=1280,720',
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_test_t8')
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
    const filePath = 'file:///' + path.resolve('videos-tutoriais/tutorial-08-h264.mp4').replace(/\\/g, '/');
    console.log("Navigating to", filePath);
    await send('Page.navigate', { url: filePath });
    await new Promise(r => setTimeout(r, 3000));

    // Seek to 10 seconds and test playback
    const check = await send('Runtime.evaluate', {
        expression: `
            (async () => {
                const v = document.querySelector('video');
                v.currentTime = 10;
                await new Promise(r => v.onseeked = r);
                return {
                    currentTime: v.currentTime,
                    duration: v.duration,
                    videoWidth: v.videoWidth,
                    videoHeight: v.videoHeight,
                    readyState: v.readyState
                };
            })()
        `,
        awaitPromise: true,
        returnByValue: true
    });
    console.log("Edge video check:", JSON.stringify(check.result.result.value, null, 2));

    const screenshot = await send('Page.captureScreenshot', { format: 'png' });
    if (screenshot && screenshot.result && screenshot.result.data) {
        const buf = Buffer.from(screenshot.result.data, 'base64');
        const scPath = path.join(process.cwd(), 'scripts', 'test_t8_frame.png');
        fs.writeFileSync(scPath, buf);
        console.log("Saved test screenshot to", scPath);
    }

    ws.close();
    edge.kill();
})().catch(console.error);
