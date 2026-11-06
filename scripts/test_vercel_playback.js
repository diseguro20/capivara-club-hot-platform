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
        '--user-data-dir=' + path.join(process.cwd(), '.temp_edge_profile')
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

        if (!connected) {
            throw new Error("Could not connect to Edge DevTools port 9222");
        }

        console.log("Connecting to target page...");
        const targets = await getJson(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
        const pageTarget = targets.find(t => t.type === 'page') || targets[0];
        const client = new CDPClient(pageTarget.webSocketDebuggerUrl);
        await client.ready();
        await client.send('Page.enable');
        await client.send('Runtime.enable');

        console.log("Navigating to https://capivara-club-hot.vercel.app/painel/ ...");
        await client.send('Page.navigate', { url: 'https://capivara-club-hot.vercel.app/painel/' });
        await sleep(5000);

        // Bypass or set auth session
        await client.evaluate(`
            localStorage.setItem("capivara_user", JSON.stringify({ email: "diseguro20@gmail.com", name: "Diego Segura", role: "admin", access: "full" }));
            localStorage.setItem("capivara_logged_in", "true");
        `);

        // Switch to tutoriais tab
        console.log("Opening tutoriais tab...");
        await client.evaluate(`
            if (typeof window.openPage === "function") {
                window.openPage("tutoriais");
            } else if (typeof window.switchTab === "function") {
                window.switchTab("tutoriais");
            }
        `);
        await sleep(4000);

        // Query all video elements
        const videoSummary = await client.evaluate(`
            (() => {
                const videos = Array.from(document.querySelectorAll("video"));
                return videos.map((v, i) => {
                    const sources = Array.from(v.querySelectorAll("source")).map(s => s.src);
                    return {
                        index: i + 1,
                        currentSrc: v.currentSrc,
                        src: v.src,
                        sourcesCount: sources.length,
                        firstSource: sources[0] || null,
                        secondSource: sources[1] || null,
                        readyState: v.readyState,
                        networkState: v.networkState,
                        paused: v.paused,
                        duration: v.duration,
                        error: v.error ? (v.error.message || v.error.code) : null
                    };
                });
            })()
        `);

        console.log("Found videos:", JSON.stringify(videoSummary, null, 2));

        // Test playing each video for 1.5 seconds to confirm streaming & decoding
        console.log("\n--- Testing Video Playback Streaming ---");
        const playResults = await client.evaluate(`
            (async () => {
                const videos = Array.from(document.querySelectorAll("video"));
                const results = [];
                for (let i = 0; i < videos.length; i++) {
                    const v = videos[i];
                    try {
                        v.muted = true;
                        const p = v.play();
                        if (p !== undefined) {
                            await p;
                        }
                        await new Promise(r => setTimeout(r, 1200));
                        results.push({
                            video: i + 1,
                            status: "PLAYING_OK",
                            currentTime: v.currentTime,
                            duration: v.duration,
                            src: v.currentSrc || v.src
                        });
                        v.pause();
                    } catch (e) {
                        results.push({
                            video: i + 1,
                            status: "PLAY_FAILED",
                            error: e.toString(),
                            currentSrc: v.currentSrc,
                            readyState: v.readyState
                        });
                    }
                }
                return results;
            })()
        `);

        console.log("Playback Results:", JSON.stringify(playResults, null, 2));

        // Take a screenshot of the page
        const screenshot = await client.send('Page.captureScreenshot', { format: 'png' });
        if (screenshot && screenshot.result && screenshot.result.data) {
            const buf = Buffer.from(screenshot.result.data, 'base64');
            const scPath = path.join(process.cwd(), 'scripts', 'vercel_tutorials_test.png');
            fs.writeFileSync(scPath, buf);
            console.log("Screenshot saved to", scPath);
        }

        client.close();
    } finally {
        edge.kill();
    }
}

run().catch(err => {
    console.error("Error during verification:", err);
    process.exit(1);
});
