const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const path = require('path');

const EDGE_PATH = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const DEBUG_PORT = 9227;
const USER_DATA = path.join(process.cwd(), '.temp_edge_button_test');

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
    console.log('--- TESTANDO TRAVA DO BOTÃO ÁREA DE MEMBROS (ANTES E DEPOIS DO PAGAMENTO) ---');
    if (!fs.existsSync(USER_DATA)) fs.mkdirSync(USER_DATA, { recursive: true });

    const edge = spawn(EDGE_PATH, [
        '--remote-debugging-port=' + DEBUG_PORT,
        '--headless=new',
        '--disable-gpu',
        '--no-first-run',
        '--no-default-browser-check',
        '--window-size=1400,900',
        '--user-data-dir=' + USER_DATA
    ], { stdio: 'ignore' });

    try {
        await new Promise(r => setTimeout(r, 1800));
        const targets = await getJson('http://127.0.0.1:' + DEBUG_PORT + '/json/list');
        const wsUrl = targets[0].webSocketDebuggerUrl;
        const ws = new WebSocket(wsUrl);
        await new Promise(r => ws.onopen = r);

        let id = 1;
        function send(method, params = {}) {
            return new Promise(res => {
                const reqId = id++;
                const handler = (evt) => {
                    const msg = JSON.parse(evt.data);
                    if (msg.id === reqId) {
                        ws.removeEventListener('message', handler);
                        res(msg.result);
                    }
                };
                ws.addEventListener('message', handler);
                ws.send(JSON.stringify({ id: reqId, method, params }));
            });
        }

        async function evalJs(expr) {
            const res = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
            return res && res.result ? res.result.value : null;
        }

        await send('Page.enable');
        await send('Runtime.enable');

        // 1. Visitante Anônimo (Sem pagamento)
        console.log('1. Visitando página inicial como usuário não pago...');
        await send('Page.navigate', { url: 'http://localhost:5500/' });
        await new Promise(r => setTimeout(r, 1500));
        await evalJs(`localStorage.clear()`);
        await send('Page.navigate', { url: 'http://localhost:5500/' });
        await new Promise(r => setTimeout(r, 1500));

        const btnLocked = await evalJs(`document.getElementById('headerMembersBtn').classList.contains('locked')`);
        const btnText = await evalJs(`document.getElementById('headerMembersBtn').innerText`);
        console.log('Botão de membros está BLOQUEADO (locked):', btnLocked);
        console.log('Texto do botão bloqueado:', btnText);

        if (!btnLocked || !btnText.includes('🔒')) {
            throw new Error('O botão de membros deveria estar BLOQUEADO com cadeado antes do pagamento!');
        }

        // Clicar no botão bloqueado
        console.log('2. Clicando no botão bloqueado de membros...');
        await evalJs(`document.getElementById('headerMembersBtn').click()`);
        await new Promise(r => setTimeout(r, 600));

        const modalOpened = await evalJs(`document.getElementById('accessModal').classList.contains('show')`);
        const statusMsg = await evalJs(`document.getElementById('accessStatus').innerText`);
        console.log('Modal de checkout aberto para realizar pagamento:', modalOpened);
        console.log('Mensagem de aviso no modal:', statusMsg);

        if (!modalOpened) {
            throw new Error('Clicar no botão bloqueado deveria abrir o checkout para pagamento!');
        }

        // Screenshot do botão bloqueado
        const scLocked = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(process.cwd(), 'scripts', 'botao_membros_bloqueado.png'), Buffer.from(scLocked.data, 'base64'));
        console.log('Screenshot salvo em scripts/botao_membros_bloqueado.png');

        // 3. Simular Pagamento Concluído
        console.log('\n3. Simulando confirmação de pagamento para o cliente...');
        await evalJs(`
            localStorage.setItem('capivara_user', JSON.stringify({
                email: 'lead_pagante@teste.com',
                name: 'Cliente Pagante',
                paid: true
            }));
            localStorage.setItem('memberEmail', 'lead_pagante@teste.com');
            localStorage.setItem('memberPaid', '1');
            window.location.reload();
        `);
        await new Promise(r => setTimeout(r, 2000));

        const btnUnlocked = await evalJs(`document.getElementById('headerMembersBtn').classList.contains('unlocked')`);
        const btnTextUnlocked = await evalJs(`document.getElementById('headerMembersBtn').innerText`);
        const btnHref = await evalJs(`document.getElementById('headerMembersBtn').getAttribute('href')`);
        console.log('Botão de membros está LIBERADO (unlocked):', btnUnlocked);
        console.log('Texto do botão liberado:', btnTextUnlocked);
        console.log('Destino do botão liberado:', btnHref);

        if (!btnUnlocked || btnHref !== '/painel') {
            throw new Error('O botão de membros deveria estar LIBERADO após o pagamento!');
        }

        // Screenshot do botão liberado
        const scUnlocked = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync(path.join(process.cwd(), 'scripts', 'botao_membros_liberado.png'), Buffer.from(scUnlocked.data, 'base64'));
        console.log('Screenshot salvo em scripts/botao_membros_liberado.png');

        ws.close();
        edge.kill();

        console.log('\n======================================================');
        console.log('✅ VALIDAÇÃO DO BOTÃO DE MEMBROS CONCLUÍDA COM SUCESSO:');
        console.log('1. Antes do pagamento: Botão bloqueado com 🔒, abre checkout.');
        console.log('2. Após o pagamento: Botão liberado com ✨, leva à Área de Membros.');
        console.log('======================================================');
    } catch (e) {
        console.error('Erro na execução:', e);
        edge.kill();
        process.exit(1);
    }
})();
