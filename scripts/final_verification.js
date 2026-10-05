const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
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
    console.log("Starting Edge headless...");
    const edge = spawn(EDGE_PATH, [
        `--remote-debugging-port=${DEBUG_PORT}`,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--window-size=1920,1080',
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_final_verification')
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

        if (!connected) throw new Error("Could not connect to Edge CDP");

        const targets = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
        const pageTarget = targets.find(t => t.type === 'page') || targets[0];
        const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
        await client.ready();
        await client.send('Page.enable');
        await client.send('Runtime.enable');

        console.log("Loading https://capivara-club-hot.vercel.app/painel/ ...");
        await client.send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/painel/' });
        await sleep(3000);

        await client.evaluate(`
            localStorage.setItem("capivara_user", JSON.stringify({ email: "diseguro20@gmail.com", name: "Diego Segura", role: "admin", access: "full" }));
            localStorage.setItem("capivara_logged_in", "true");
            if (typeof window.openPage === "function") window.openPage("tutoriais");
        `);
        await sleep(5000);

        const allVideos = await client.evaluate(`
            (() => {
                const vids = Array.from(document.querySelectorAll("video"));
                return vids.map((v, i) => ({
                    tutorial: i + 1,
                    src: v.currentSrc,
                    durationFormatted: Math.floor(v.duration / 60) + 'm ' + Math.floor(v.duration % 60) + 's',
                    durationSeconds: v.duration,
                    readyState: v.readyState,
                    networkState: v.networkState,
                    hasError: !!v.error
                }));
            })()
        `);

        console.log("=== ALL 9 TUTORIAL VIDEOS ON VERCEL ===");
        console.table(allVideos);

        // Capture screenshot of the tutorials section
        const screenshot = await client.send('Page.captureScreenshot', { format: 'png' });
        if (screenshot && screenshot.result && screenshot.result.data) {
            const buf = Buffer.from(screenshot.result.data, 'base64');
            const scPath = path.join(process.cwd(), 'scripts', 'vercel_tutorials_verified.png');
            fs.writeFileSync(scPath, buf);
            console.log("Screenshot successfully saved to:", scPath);
        }

        client.close();
    } finally {
        edge.kill();
    }
}

run().catch(err => {
    console.error("Error:", err);
    process.exit(1);
});
