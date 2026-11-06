const { spawn } = require('child_process');
const http = require('http');
const path = require('path');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const DEBUG_PORT = 9222;

async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

function getJson(url) {
    return new Promise((resolve, reject) => {
        http.get(url, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); } catch(e) { reject(e); }
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
                this.callbacks.get(msg.id)(msg);
                this.callbacks.delete(msg.id);
            }
        };
    }

    ready() {
        return new Promise((resolve) => {
            if (this.ws.readyState === WebSocket.OPEN) return resolve();
            this.ws.onopen = () => resolve();
        });
    }

    send(method, params = {}) {
        return new Promise((resolve) => {
            const reqId = this.id++;
            this.callbacks.set(reqId, resolve);
            this.ws.send(JSON.stringify({ id: reqId, method, params }));
        });
    }

    async evaluate(expression) {
        const res = await this.send('Runtime.evaluate', {
            expression,
            returnByValue: true,
            awaitPromise: true
        });
        return res.result && res.result.result ? res.result.result.value : null;
    }

    close() {
        this.ws.close();
    }
}

async function run() {
    const edge = spawn(EDGE_PATH, [
        `--remote-debugging-port=${DEBUG_PORT}`,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_profile2')
    ], { stdio: 'ignore' });

    try {
        let connected = false;
        let versionData = null;
        for (let i = 0; i < 20; i++) {
            await sleep(500);
            try {
                versionData = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
                if (versionData && versionData.webSocketDebuggerUrl) {
                    connected = true;
                    break;
                }
            } catch(e) {}
        }

        const targets = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
        const pageTarget = targets.find(t => t.type === 'page') || targets[0];
        const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
        await client.ready();
        await client.send('Page.enable');
        await client.send('Runtime.enable');

        await client.send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/painel/' });
        await sleep(3000);

        await client.evaluate(`
            localStorage.setItem("capivara_user", JSON.stringify({ email: "diseguro20@gmail.com", name: "Diego Segura", role: "admin", access: "full" }));
            localStorage.setItem("capivara_logged_in", "true");
            if (typeof window.openPage === "function") window.openPage("tutoriais");
        `);
        await sleep(5000);

        // Check video 9 specifically
        const v9Info = await client.evaluate(`
            (() => {
                const videos = Array.from(document.querySelectorAll("video"));
                const v9 = videos[8];
                if (!v9) return null;
                return {
                    currentSrc: v9.currentSrc,
                    readyState: v9.readyState,
                    duration: v9.duration,
                    networkState: v9.networkState,
                    error: v9.error ? v9.error.message : null
                };
            })()
        `);
        console.log("Video 9 Status:", JSON.stringify(v9Info, null, 2));

        // Quick play test on video 9 without blocking on promise
        const v9Play = await client.evaluate(`
            (async () => {
                const videos = Array.from(document.querySelectorAll("video"));
                const v9 = videos[8];
                v9.muted = true;
                v9.play();
                await new Promise(r => setTimeout(r, 3000));
                return {
                    video: 9,
                    currentTime: v9.currentTime,
                    paused: v9.paused,
                    duration: v9.duration,
                    readyState: v9.readyState,
                    src: v9.currentSrc
                };
            })()
        `);
        console.log("Video 9 Play Test:", JSON.stringify(v9Play, null, 2));

        client.close();
    } finally {
        edge.kill();
    }
}

run().catch(console.error);
