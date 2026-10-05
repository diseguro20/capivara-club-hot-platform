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
    console.log('Starting Edge headless...');
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
            // waiting for edge
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

    // Verify window.DMCN_PROMPTS_18
    const prompt18Count = await client.evaluate('window.DMCN_PROMPTS_18 ? window.DMCN_PROMPTS_18.length : 0');
    console.log(`window.DMCN_PROMPTS_18 loaded count: ${prompt18Count}`);

    const promptCount = await client.evaluate('window.DMCN_PROMPTS ? window.DMCN_PROMPTS.length : 0');
    console.log(`window.DMCN_PROMPTS loaded count: ${promptCount}`);

    // Call openPage('galeria-18')
    console.log('Opening page galeria-18...');
    await client.evaluate(`
        if (typeof openPage === 'function') {
            openPage('galeria-18');
        } else {
            const link = document.querySelector('[data-page="galeria-18"]');
            if (link) link.click();
        }
    `);
    await sleep(1500);

    // Check gallery-18 cards
    const cardCount = await client.evaluate('document.querySelectorAll("#gallery18Grid .gallery-card").length');
    console.log(`gallery18Grid rendered card count: ${cardCount}`);

    // Inspect first card data
    const firstCard = await client.evaluate(`(() => {
        const card = document.querySelector("#gallery18Grid .gallery-card");
        if (!card) return null;
        return {
            name: card.dataset.name,
            promptLength: card.dataset.prompt ? card.dataset.prompt.length : 0,
            promptSnippet: card.dataset.prompt ? card.dataset.prompt.substring(0, 100) : '',
            index: card.dataset.index,
            titleText: card.querySelector('h3') ? card.querySelector('h3').innerText : '',
            hasCopyBtn: !!card.querySelector('.gallery-copy')
        };
    })()`);
    console.log('First card info:', JSON.stringify(firstCard, null, 2));

    // Simulate click on first card to open modal
    console.log('Clicking first card...');
    await client.evaluate(`(() => {
        const card = document.querySelector("#gallery18Grid .gallery-card");
        if (card) card.click();
    })()`);
    await sleep(500);

    const modalState = await client.evaluate(`(() => {
        const viewer = document.getElementById("promptViewer");
        const title = document.getElementById("promptViewerTitle");
        const content = document.getElementById("promptViewerContent");
        return {
            modalVisible: viewer ? (viewer.style.display !== 'none' && !viewer.classList.contains('hidden') && getComputedStyle(viewer).display !== 'none') : false,
            viewerClass: viewer ? viewer.className : '',
            viewerStyleDisplay: viewer ? viewer.style.display : '',
            title: title ? title.innerText : '',
            contentLength: content ? content.textContent.length : 0,
            contentSnippet: content ? content.textContent.substring(0, 150) : ''
        };
    })()`);
    console.log('Modal state after clicking card 0:', JSON.stringify(modalState, null, 2));

    // Simulate click on card 2 (index 1)
    console.log('Clicking card index 1 (Clay mask)...');
    await client.evaluate(`(() => {
        const cards = document.querySelectorAll("#gallery18Grid .gallery-card");
        if (cards[1]) cards[1].click();
    })()`);
    await sleep(500);

    const modalState2 = await client.evaluate(`(() => {
        const title = document.getElementById("promptViewerTitle");
        const content = document.getElementById("promptViewerContent");
        return {
            title: title ? title.innerText : '',
            contentLength: content ? content.textContent.length : 0,
            contentSnippet: content ? content.textContent.substring(0, 150) : ''
        };
    })()`);
    console.log('Modal state after clicking card 1:', JSON.stringify(modalState2, null, 2));

    // Simulate click on card index 49 (Prompt 50)
    console.log('Clicking card index 49...');
    await client.evaluate(`(() => {
        const cards = document.querySelectorAll("#gallery18Grid .gallery-card");
        if (cards[49]) cards[49].click();
    })()`);
    await sleep(500);

    const modalState50 = await client.evaluate(`(() => {
        const title = document.getElementById("promptViewerTitle");
        const content = document.getElementById("promptViewerContent");
        return {
            title: title ? title.innerText : '',
            contentLength: content ? content.textContent.length : 0,
            contentSnippet: content ? content.textContent.substring(0, 150) : ''
        };
    })()`);
    console.log('Modal state after clicking card 49:', JSON.stringify(modalState50, null, 2));

    // Test clicking close button
    console.log('Clicking modal close button...');
    await client.evaluate(`(() => {
        const closeBtn = document.getElementById("promptViewerClose");
        if (closeBtn) closeBtn.click();
    })()`);
    await sleep(300);

    const closedState = await client.evaluate(`(() => {
        const viewer = document.getElementById("promptViewer");
        return {
            hasHiddenClass: viewer ? viewer.classList.contains('hidden') : false,
            styleDisplay: viewer ? viewer.style.display : ''
        };
    })()`);
    console.log('Modal state after closing:', JSON.stringify(closedState, null, 2));

    // Test pagination
    console.log('Testing gallery-18 pagination...');
    const pageStatus = await client.evaluate(`document.getElementById("gallery18PageStatus") ? document.getElementById("gallery18PageStatus").textContent : ''`);
    console.log('Initial page status:', pageStatus);

    console.log('Clicking Next page button...');
    await client.evaluate(`(() => {
        const nextBtn = document.getElementById("gallery18Next");
        if (nextBtn) nextBtn.click();
    })()`);
    await sleep(400);

    const pageStatusAfterNext = await client.evaluate(`document.getElementById("gallery18PageStatus") ? document.getElementById("gallery18PageStatus").textContent : ''`);
    console.log('Page status after Next:', pageStatusAfterNext);

    // Check visible cards on page 2
    const visibleCardsPage2 = await client.evaluate(`(() => {
        const cards = Array.from(document.querySelectorAll("#gallery18Grid .gallery-card"));
        return cards.filter(c => c.style.display !== 'none').map(c => ({
            name: c.dataset.name,
            index: c.dataset.index,
            snippet: c.dataset.prompt ? c.dataset.prompt.substring(0, 60) : ''
        }));
    })()`);
    console.log(`Page 2 visible cards count: ${visibleCardsPage2.length}`);
    console.log('First card on page 2:', JSON.stringify(visibleCardsPage2[0], null, 2));

    // Click first card on page 2 (index 12)
    console.log('Clicking card 12 on page 2...');
    await client.evaluate(`(() => {
        const cards = Array.from(document.querySelectorAll("#gallery18Grid .gallery-card"));
        const card12 = cards.find(c => c.dataset.index === "12");
        if (card12) card12.click();
    })()`);
    await sleep(400);

    const modalStatePage2 = await client.evaluate(`(() => {
        const title = document.getElementById("promptViewerTitle");
        const content = document.getElementById("promptViewerContent");
        return {
            title: title ? title.innerText : '',
            contentLength: content ? content.textContent.length : 0,
            contentSnippet: content ? content.textContent.substring(0, 150) : ''
        };
    })()`);
    console.log('Modal state for card 12:', JSON.stringify(modalStatePage2, null, 2));

    // Test standard galeria as well
    console.log('Testing standard galeria page...');
    await client.evaluate(`openPage('galeria')`);
    await sleep(1000);

    const standardCardCount = await client.evaluate('document.querySelectorAll("[data-content=\\"galeria\\"] .gallery-card").length');
    console.log(`Standard galeria card count: ${standardCardCount}`);

    // Click first card in standard galeria
    await client.evaluate(`(() => {
        const card = document.querySelector("[data-content=\\"galeria\\"] .gallery-card");
        if (card) card.click();
    })()`);
    await sleep(400);

    const standardModalState = await client.evaluate(`(() => {
        const title = document.getElementById("promptViewerTitle");
        const content = document.getElementById("promptViewerContent");
        return {
            title: title ? title.innerText : '',
            contentLength: content ? content.textContent.length : 0,
            contentSnippet: content ? content.textContent.substring(0, 150) : ''
        };
    })()`);
    console.log('Standard galeria card 0 modal state:', JSON.stringify(standardModalState, null, 2));

    client.close();
    edge.kill();
    console.log('Verification finished successfully!');
}

run().catch(err => {
    console.error('Error during verification:', err);
    process.exit(1);
});
