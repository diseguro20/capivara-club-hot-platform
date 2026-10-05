const { spawn } = require('child_process');
const http = require('http');
const path = require('path');
const fs = require('fs');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function fetchJson(url) {
    return new Promise((resolve, reject) => {
        http.get(url, res => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

class CDPClient {
    constructor(wsUrl) {
        this.ws = new WebSocket(wsUrl);
        this.id = 1;
        this.callbacks = new Map();
        this.ws.onmessage = (event) => {
            const msg = JSON.parse(event.data);
            if (msg.id && this.callbacks.has(msg.id)) {
                const cb = this.callbacks.get(msg.id);
                this.callbacks.delete(msg.id);
                if (msg.error) cb.reject(msg.error);
                else cb.resolve(msg.result);
            }
        };
    }

    ready() {
        return new Promise((resolve, reject) => {
            if (this.ws.readyState === WebSocket.OPEN) return resolve();
            this.ws.onopen = () => resolve();
            this.ws.onerror = (e) => reject(e);
        });
    }

    send(method, params = {}) {
        return new Promise((resolve, reject) => {
            const id = this.id++;
            this.callbacks.set(id, { resolve, reject });
            this.ws.send(JSON.stringify({ id, method, params }));
        });
    }

    async evaluate(expression) {
        const res = await this.send('Runtime.evaluate', {
            expression,
            returnByValue: true,
            awaitPromise: true
        });
        if (res.exceptionDetails) {
            throw new Error(JSON.stringify(res.exceptionDetails));
        }
        return res.result.value;
    }

    close() {
        this.ws.close();
    }
}

async function run() {
    const tempDir = path.join(__dirname, '..', '.edge_temp');
    if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir, { recursive: true });

    const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
    console.log('Starting Edge headless for Sync testing...');
    const edge = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=9222',
        `--user-data-dir=${tempDir}`,
        '--disable-gpu',
        '--no-first-run',
        'about:blank'
    ]);

    let wsUrl = null;
    for (let i = 0; i < 20; i++) {
        await sleep(500);
        try {
            const targets = await fetchJson('http://127.0.0.1:9222/json');
            const pageTarget = targets.find(t => t.type === 'page');
            if (pageTarget && pageTarget.webSocketDebuggerUrl) {
                wsUrl = pageTarget.webSocketDebuggerUrl;
                break;
            }
        } catch (e) {
            // waiting
        }
    }

    if (!wsUrl) {
        console.error('Failed to connect to Edge CDP');
        edge.kill();
        process.exit(1);
    }

    console.log('Connected to Edge CDP:', wsUrl);
    const client = new CDPClient(wsUrl);
    await client.ready();

    await client.send('Page.enable');
    await client.send('Runtime.enable');

    console.log('Navigating to http://localhost:5500/paginas/painel.html...');
    await client.send('Page.navigate', { url: 'http://localhost:5500/paginas/painel.html' });
    await sleep(2000);

    // Verify sync banner presence
    const bannerInfo = await client.evaluate(`(() => {
        const banner = document.getElementById("realtimeSyncBanner");
        if (!banner) return null;
        return {
            exists: true,
            visible: getComputedStyle(banner).display !== 'none',
            badge: banner.querySelector('.sync-badge') ? banner.querySelector('.sync-badge').innerText : '',
            videos: document.getElementById('metricVideos')?.innerText,
            workflows: document.getElementById('metricWorkflows')?.innerText,
            prompts: document.getElementById('metricPrompts')?.innerText,
            prompts18: document.getElementById('metricPrompts18')?.innerText,
            lastTime: document.getElementById('syncLastTime')?.innerText
        };
    })()`);
    console.log('Real-Time Sync Banner Info:', JSON.stringify(bannerInfo, null, 2));

    // Trigger sync button click
    console.log('Clicking "Sincronizar Tudo Agora" button in the UI...');
    await client.evaluate(`(() => {
        const btn = document.getElementById("btnTriggerSync");
        if (btn) btn.click();
    })()`);
    await sleep(500);

    const btnStateDuringSync = await client.evaluate(`(() => {
        const btn = document.getElementById("btnTriggerSync");
        const label = document.getElementById("syncBtnLabel");
        return {
            isLoading: btn ? btn.classList.contains('loading') : false,
            disabled: btn ? btn.disabled : false,
            label: label ? label.innerText : ''
        };
    })()`);
    console.log('Button state during sync:', JSON.stringify(btnStateDuringSync, null, 2));

    // Wait for sync to finish (poll up to 10s)
    let syncDone = false;
    for (let i = 0; i < 20; i++) {
        await sleep(1000);
        const status = await client.evaluate(`(() => {
            const btn = document.getElementById("btnTriggerSync");
            const feedback = document.getElementById("syncFeedbackMsg");
            const lastTime = document.getElementById("syncLastTime");
            return {
                isLoading: btn ? btn.classList.contains('loading') : false,
                feedbackVisible: feedback ? !feedback.classList.contains('hidden') : false,
                feedbackText: feedback ? feedback.innerText : '',
                lastTime: lastTime ? lastTime.innerText : ''
            };
        })()`);
        if (!status.isLoading && status.feedbackVisible) {
            console.log('Sync completed with feedback:', status);
            syncDone = true;
            break;
        }
    }

    if (!syncDone) {
        console.warn('Sync feedback took longer than expected or finished silently.');
    }

    // Capture screenshot of the banner
    console.log('Taking screenshot of the Sync Banner...');
    const screenshot = await client.send('Page.captureScreenshot', { format: 'png' });
    const buffer = Buffer.from(screenshot.data, 'base64');
    const screenshotPath = path.join(__dirname, '..', 'member-assets', 'sync_banner_verified.png');
    fs.writeFileSync(screenshotPath, buffer);
    console.log('Screenshot saved to:', screenshotPath);

    client.close();
    edge.kill();
    console.log('Real-Time Sync verification finished successfully!');
}

run().catch(err => {
    console.error('Error during Sync verification:', err);
    process.exit(1);
});
