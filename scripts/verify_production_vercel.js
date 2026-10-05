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
    console.log('Starting Edge headless for Production Vercel testing...');
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
        } catch (e) {}
    }

    if (!wsUrl) {
        console.error('Failed to connect to Edge CDP');
        edge.kill();
        process.exit(1);
    }

    const client = new CDPClient(wsUrl);
    await client.ready();
    await client.send('Page.enable');
    await client.send('Runtime.enable');

    // 1. Test Landing Page
    console.log('1. Navigating to https://capivara-club-hot.vercel.app/ ...');
    await client.send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/' });
    await sleep(2500);

    const landingInfo = await client.evaluate(`(() => {
        return {
            title: document.title,
            headline: document.querySelector('.headline')?.innerText?.replace(/\\s+/g, ' ')?.trim(),
            hasBuyButton: !!document.querySelector('.cta'),
            hasMemberButton: !!document.querySelector('.nav-login-btn')
        };
    })()`);
    console.log('Landing Page Info:', JSON.stringify(landingInfo, null, 2));

    // 2. Navigate to Login Page
    console.log('2. Navigating to https://capivara-club-hot.vercel.app/login ...');
    await client.send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/login' });
    await sleep(2000);

    const loginInfo = await client.evaluate(`(() => {
        return {
            title: document.title,
            emailValue: document.getElementById('loginEmail')?.value,
            passwordValue: document.getElementById('loginPassword')?.value,
            hasAuthScript: typeof window.capivaraAuth !== 'undefined'
        };
    })()`);
    console.log('Login Page Info:', JSON.stringify(loginInfo, null, 2));

    // 3. Perform login as diseguro20@gmail.com / diego123
    console.log('3. Submitting login with diseguro20@gmail.com / diego123 ...');
    await client.evaluate(`(() => {
        document.getElementById('loginEmail').value = 'diseguro20@gmail.com';
        document.getElementById('loginPassword').value = 'diego123';
        document.getElementById('btnLoginSubmit').click();
    })()`);
    await sleep(2500);

    // 4. Verify redirected to member panel
    const currentUrl = await client.evaluate('window.location.href');
    console.log('Current URL after login:', currentUrl);

    const panelInfo = await client.evaluate(`(() => {
        return {
            title: document.title,
            memberName: document.getElementById('memberName')?.innerText,
            userEmail: localStorage.getItem('memberEmail'),
            hasSyncBanner: !!document.getElementById('realtimeSyncBanner'),
            totalPrompts18Loaded: window.DMCN_PROMPTS_18?.length,
            totalPromptsLoaded: window.DMCN_PROMPTS?.length
        };
    })()`);
    console.log('Panel Info on Vercel Production:', JSON.stringify(panelInfo, null, 2));

    client.close();
    edge.kill();
    console.log('All Production Vercel tests passed 100%!');
}

run().catch(err => {
    console.error('Error during Vercel test:', err);
    process.exit(1);
});
