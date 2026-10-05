painel_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel do Membro — CAPIVARA CLUB HOT</title>
  <link rel="icon" href="../icons/favicon-32.png">
  <link rel="apple-touch-icon" href="../icons/apple-touch-icon.png">
  <meta name="theme-color" content="#050304">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="../assets/ui.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-1.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-2.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-3.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-4.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-5.css">
  <script src="../assets/ui.js"></script>

  <style>
    :root {
      --bg: #070305;
      --card: rgba(16, 8, 12, 0.85);
      --wine: #7a1025;
      --wine-light: #d85b72;
      --line: rgba(255, 255, 255, 0.08);
      --text-muted: #8e8589;
    }
    body {
      background: radial-gradient(circle at 50% -20%, #200812 0%, #070305 70%);
      color: #eee;
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 28px;
      border-bottom: 1px solid var(--line);
      background: rgba(10, 4, 7, 0.95);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: #fff;
    }
    .brand-wrap img {
      height: 38px;
      width: auto;
    }
    .brand-title {
      font-family: 'Anton', sans-serif;
      font-size: 20px;
      letter-spacing: 1px;
    }
    .user-badge {
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 13px;
    }
    .user-pill {
      background: rgba(122, 16, 37, 0.35);
      border: 1px solid rgba(216, 91, 114, 0.4);
      padding: 6px 14px;
      border-radius: 99px;
      font-weight: 700;
      color: #f1d5dd;
      font-size: 12px;
    }
    .btn-logout {
      background: transparent;
      border: 1px solid var(--line);
      color: #aaa;
      padding: 6px 12px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 12px;
      transition: .2s;
    }
    .btn-logout:hover {
      border-color: var(--wine-light);
      color: #fff;
    }
    
    /* Navigation Bar */
    .nav-container {
      display: flex;
      gap: 8px;
      padding: 16px 28px;
      max-width: 1200px;
      margin: 0 auto;
      width: calc(100% - 56px);
      overflow-x: auto;
    }
    .tab-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(18, 9, 13, 0.6);
      border: 1px solid var(--line);
      color: #a79da1;
      padding: 10px 18px;
      border-radius: 12px;
      font-weight: 600;
      font-size: 13px;
      cursor: pointer;
      white-space: nowrap;
      transition: all .2s;
    }
    .tab-btn:hover {
      background: rgba(122, 16, 37, 0.2);
      color: #fff;
      border-color: rgba(216, 91, 114, 0.3);
    }
    .tab-btn.active {
      background: linear-gradient(135deg, rgba(122, 16, 37, 0.8), rgba(60, 8, 18, 0.9));
      color: #fff;
      border-color: var(--wine-light);
      box-shadow: 0 4px 20px rgba(122, 16, 37, 0.4);
    }

    /* Main Area */
    .dashboard-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 28px 60px;
      width: calc(100% - 56px);
      flex: 1;
    }
    .tab-panel {
      display: none;
      animation: fadeIn .3s ease-out;
    }
    .tab-panel.active {
      display: block;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Hero Banner */
    .welcome-hero {
      background: linear-gradient(135deg, rgba(122, 16, 37, 0.35) 0%, rgba(16, 7, 11, 0.8) 100%);
      border: 1px solid rgba(216, 91, 114, 0.3);
      border-radius: 18px;
      padding: 32px;
      margin-bottom: 28px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 20px;
      flex-wrap: wrap;
    }
    .welcome-hero h1 {
      font-family: 'Anton', sans-serif;
      font-size: 28px;
      letter-spacing: 0.5px;
      margin: 0 0 8px;
    }
    .welcome-hero p {
      color: #c9bec3;
      font-size: 14px;
      margin: 0;
      max-width: 600px;
      line-height: 1.5;
    }
    .quick-stats {
      display: flex;
      gap: 16px;
    }
    .quick-stat {
      background: rgba(10, 4, 7, 0.6);
      border: 1px solid var(--line);
      padding: 12px 18px;
      border-radius: 12px;
      text-align: center;
    }
    .quick-stat strong {
      display: block;
      font-size: 22px;
      color: #d85b72;
      font-family: 'Anton', sans-serif;
    }
    .quick-stat span {
      font-size: 11px;
      color: var(--text-muted);
    }

    /* Grids */
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 20px;
      margin-top: 20px;
    }
    .custom-card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 14px;
      overflow: hidden;
      transition: transform .2s, border-color .2s;
    }
    .custom-card:hover {
      transform: translateY(-3px);
      border-color: rgba(216, 91, 114, 0.4);
    }
    .card-thumb {
      width: 100%;
      height: 200px;
      object-fit: cover;
      background: #11080d;
      display: block;
    }
    .card-body {
      padding: 18px;
    }
    .card-tag {
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 0.05em;
      color: var(--wine-light);
      text-transform: uppercase;
      margin-bottom: 6px;
      display: inline-block;
    }
    .card-title {
      font-size: 16px;
      font-weight: 700;
      margin: 0 0 8px;
      color: #f1ecf0;
    }
    .card-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 16px;
    }
    .btn-action {
      width: 100%;
      background: linear-gradient(135deg, #7a1025, #a42c4b);
      border: none;
      color: #fff;
      padding: 10px 14px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 12px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: opacity .2s;
      text-decoration: none;
      box-sizing: border-box;
    }
    .btn-action:hover {
      opacity: 0.9;
    }

    /* Video player modal */
    .video-modal {
      position: fixed;
      inset: 0;
      z-index: 1000;
      background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(10px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .video-modal.hidden {
      display: none;
    }
    .video-dialog {
      background: #10080d;
      border: 1px solid rgba(216, 91, 114, 0.4);
      border-radius: 16px;
      width: min(840px, 100%);
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.8);
    }
    .video-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 20px;
      border-bottom: 1px solid var(--line);
    }
    .video-head h3 {
      margin: 0;
      font-size: 16px;
    }
    .video-close {
      background: transparent;
      border: none;
      color: #aaa;
      font-size: 24px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <!-- Header Sticky -->
  <header class="header-bar">
    <a href="../index.html" class="brand-wrap">
      <img src="../imagens/logo.webp" alt="Capivara Club Hot Logo">
      <span class="brand-title">CAPIVARA CLUB HOT</span>
    </a>
    <div class="user-badge">
      <span class="user-pill" id="userPill">VIP • membro@capivaraclubhot.com</span>
      <button class="btn-logout" onclick="logout()">Sair</button>
    </div>
  </header>

  <!-- Navigation Tabs -->
  <nav class="nav-container">
    <button class="tab-btn active" onclick="switchTab('dashboard')">🏠 Início</button>
    <button class="tab-btn" onclick="switchTab('prompts')">⚡ Prompts (200+)</button>
    <button class="tab-btn" onclick="switchTab('tutoriais')">🎬 Aulas & Tutoriais</button>
    <button class="tab-btn" onclick="switchTab('workflows')">📦 Workflows ComfyUI</button>
    <button class="tab-btn" onclick="switchTab('ferramentas')">🛠️ Ferramentas IA</button>
    <button class="tab-btn" onclick="switchTab('afiliados')">💰 Afiliados & Saques</button>
  </nav>

  <!-- Main Content -->
  <main class="dashboard-container">

    <!-- TAB 1: DASHBOARD GERAL -->
    <section class="tab-panel active" id="tab-dashboard">
      <div class="welcome-hero">
        <div>
          <h1>BEM-VINDO AO CAPIVARA CLUB HOT</h1>
          <p>Sua central definitiva de IA para criação de modelos realistas, consistência facial e produção em escala para o nicho HOT e UGC.</p>
        </div>
        <div class="quick-stats">
          <div class="quick-stat">
            <strong>200+</strong>
            <span>PROMPTS</span>
          </div>
          <div class="quick-stat">
            <strong>10</strong>
            <span>WORKFLOWS</span>
          </div>
          <div class="quick-stat">
            <strong>5</strong>
            <span>MÓDULOS</span>
          </div>
        </div>
      </div>

      <h2 style="font-family: 'Anton', sans-serif; font-size: 20px; margin: 24px 0 14px; letter-spacing: 0.5px;">ACESSO RÁPIDO AOS CONTEÚDOS</h2>
      <div class="cards-grid">
        
        <div class="custom-card">
          <img src="../imagens/foto-1.webp" class="card-thumb" alt="Prompts Sensuais">
          <div class="card-body">
            <span class="card-tag">Biblioteca</span>
            <h3 class="card-title">Prompts Sensuais & Lingerie</h3>
            <p class="card-desc">Coleção de prompts prontos com iluminação de estúdio e realismo de pele incomparável.</p>
            <button class="btn-action" onclick="switchTab('prompts')">Acessar Prompts →</button>
          </div>
        </div>

        <div class="custom-card">
          <img src="../imagens/foto-2.webp" class="card-thumb" alt="Workflows ComfyUI">
          <div class="card-body">
            <span class="card-tag">Automação</span>
            <h3 class="card-title">Workflows ComfyUI & Flux</h3>
            <p class="card-desc">Faça download dos arquivos JSON prontos para manter o rosto idêntico em todas as fotos.</p>
            <button class="btn-action" onclick="switchTab('workflows')">Baixar Workflows →</button>
          </div>
        </div>

        <div class="custom-card">
          <img src="../imagens/foto-3.webp" class="card-thumb" alt="Aulas em Vídeo">
          <div class="card-body">
            <span class="card-tag">Treinamento</span>
            <h3 class="card-title">Aulas em Vídeo do Zero</h3>
            <p class="card-desc">Passo a passo prático para configurar personagens e movimentar vídeos sem erros.</p>
            <button class="btn-action" onclick="switchTab('tutoriais')">Assistir Aulas →</button>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 2: PROMPTS -->
    <section class="tab-panel" id="tab-prompts">
      <div class="prompt-gallery-head">
        <h1 style="font-family:'Anton'; font-size:26px; margin:0 0 6px;">GALERIA DE PROMPTS EXCLUSIVOS</h1>
        <p style="color:#aaa; font-size:13px; margin:0 0 20px;">Copie e cole diretamente nas ferramentas (Midjourney, Flux, SDXL ou Stable Diffusion).</p>
      </div>

      <div class="cards-grid" id="promptsGrid">
        <!-- Rendered via JS -->
      </div>
    </section>

    <!-- TAB 3: TUTORIAIS / VÍDEOS -->
    <section class="tab-panel" id="tab-tutoriais">
      <h1 style="font-family:'Anton'; font-size:26px; margin:0 0 6px;">AULAS & VÍDEO-TUTORIAIS</h1>
      <p style="color:#aaa; font-size:13px; margin:0 0 20px;">Aprenda as técnicas avançadas de consistência e geração de movimento.</p>

      <div class="cards-grid">
        
        <div class="custom-card">
          <div class="video-box" style="cursor:pointer;" onclick="openVideoPlayer('Aula 1: Configuração da Personagem do Zero')">
            <div class="video-security-watermark">VIP • membro@capivaraclubhot.com</div>
            <img src="../imagens/foto-4.webp" style="width:100%;height:100%;object-fit:cover;" alt="Aula 1">
            <div style="position:absolute; background:rgba(0,0,0,0.6); padding:8px 12px; border-radius:50%; font-size:24px;">▶</div>
          </div>
          <div class="card-body">
            <span class="card-tag">Módulo 1 • 14 min</span>
            <h3 class="card-title">Aula 1: Criando a Identidade da Modelo</h3>
            <p class="card-desc">Como gerar as 5 imagens de referência perfeitas para manter a identidade em qualquer pose.</p>
            <button class="btn-action" onclick="openVideoPlayer('Aula 1: Criando a Identidade da Modelo')">Assistir Aula ▶</button>
          </div>
        </div>

        <div class="custom-card">
          <div class="video-box" style="cursor:pointer;" onclick="openVideoPlayer('Aula 2: Consistência Facial com IP-Adapter')">
            <div class="video-security-watermark">VIP • membro@capivaraclubhot.com</div>
            <img src="../imagens/foto-5.webp" style="width:100%;height:100%;object-fit:cover;" alt="Aula 2">
            <div style="position:absolute; background:rgba(0,0,0,0.6); padding:8px 12px; border-radius:50%; font-size:24px;">▶</div>
          </div>
          <div class="card-body">
            <span class="card-tag">Módulo 2 • 22 min</span>
            <h3 class="card-title">Aula 2: Consistência Facial no ComfyUI</h3>
            <p class="card-desc">Utilizando IP-Adapter e LoRA para trocar de roupas e cenários mantendo o mesmo rosto.</p>
            <button class="btn-action" onclick="openVideoPlayer('Aula 2: Consistência Facial no ComfyUI')">Assistir Aula ▶</button>
          </div>
        </div>

        <div class="custom-card">
          <div class="video-box" style="cursor:pointer;" onclick="openVideoPlayer('Aula 3: Animação e Imagem para Vídeo Realista')">
            <div class="video-security-watermark">VIP • membro@capivaraclubhot.com</div>
            <img src="../imagens/foto-6.webp" style="width:100%;height:100%;object-fit:cover;" alt="Aula 3">
            <div style="position:absolute; background:rgba(0,0,0,0.6); padding:8px 12px; border-radius:50%; font-size:24px;">▶</div>
          </div>
          <div class="card-body">
            <span class="card-tag">Módulo 3 • 18 min</span>
            <h3 class="card-title">Aula 3: Gerando Vídeos com Movimento Real</h3>
            <p class="card-desc">Transforme fotos estáticas em clipes ultra-realistas com movimento natural de olhos e lábios.</p>
            <button class="btn-action" onclick="openVideoPlayer('Aula 3: Gerando Vídeos com Movimento Real')">Assistir Aula ▶</button>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 4: WORKFLOWS -->
    <section class="tab-panel" id="tab-workflows">
      <h1 style="font-family:'Anton'; font-size:26px; margin:0 0 6px;">WORKFLOWS COMFYUI PARA DOWNLOAD</h1>
      <p style="color:#aaa; font-size:13px; margin:0 0 20px;">Arquivos .JSON prontos para importar com um clique no ComfyUI.</p>

      <div class="cards-grid">
        
        <div class="custom-card">
          <div class="card-body">
            <span class="card-tag">JSON ComfyUI • SDXL</span>
            <h3 class="card-title">Consistência de Rosto IP-Adapter</h3>
            <p class="card-desc">Mantém 100% da identidade facial da modelo em qualquer pose, ângulo ou iluminação.</p>
            <a href="../workflows/workflow-consistencia-rosto.json" download class="btn-action">⬇ Baixar Workflow (.json)</a>
          </div>
        </div>

        <div class="custom-card">
          <div class="card-body">
            <span class="card-tag">JSON ComfyUI • Flux.1</span>
            <h3 class="card-title">Flux Realismo Extremo & Textura</h3>
            <p class="card-desc">Gera detalhes de pele naturais, iluminação de cinema e mãos perfeitas com o novo modelo Flux.</p>
            <a href="../workflows/workflow-flux-realismo.json" download class="btn-action">⬇ Baixar Workflow (.json)</a>
          </div>
        </div>

        <div class="custom-card">
          <div class="card-body">
            <span class="card-tag">JSON ComfyUI • Inpainting</span>
            <h3 class="card-title">Troca de Roupas & Cenários</h3>
            <p class="card-desc">Substitua biquínis, lingerie e ambientes sem alterar a silhueta ou feições da personagem.</p>
            <a href="../workflows/workflow-troca-roupas-inpainting.json" download class="btn-action">⬇ Baixar Workflow (.json)</a>
          </div>
        </div>

        <div class="custom-card">
          <div class="card-body">
            <span class="card-tag">JSON ComfyUI • Vídeo I2V</span>
            <h3 class="card-title">Animação Imagem para Vídeo</h3>
            <p class="card-desc">Dá vida e movimento suave à sua modelo com controle de câmera e expressão facial.</p>
            <a href="../workflows/workflow-animacao-video-i2v.json" download class="btn-action">⬇ Baixar Workflow (.json)</a>
          </div>
        </div>

        <div class="custom-card">
          <div class="card-body">
            <span class="card-tag">JSON ComfyUI • Upscale</span>
            <h3 class="card-title">Upscale 4K Restauração Facial</h3>
            <p class="card-desc">Aumenta a nitidez para impressão e telas 4K restaurando micro-texturas na pele e olhar.</p>
            <a href="../workflows/workflow-upscale-4k.json" download class="btn-action">⬇ Baixar Workflow (.json)</a>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 5: FERRAMENTAS -->
    <section class="tab-panel" id="tab-ferramentas">
      <div class="tool-panel-head">
        <h2>ESTEIRA DE GERAÇÃO & FERRAMENTAS IA</h2>
      </div>
      <p class="tool-desc">Suba uma foto de referência para aplicar os filtros de iluminação e consistência diretamente no navegador.</p>
      
      <div class="tool-workspace">
        <div class="tool-pane">
          <div class="tool-pane-head">Upload da Imagem<span>Passo 1</span></div>
          <div class="tool-pane-body">
            <div class="tool-drop" id="dropArea" onclick="document.getElementById('fileInput').click()">
              <div class="plus">+</div>
              <strong>Clique ou arraste uma foto aqui</strong>
              <small>Suporta JPG, PNG, WEBP até 20MB</small>
            </div>
            <input type="file" id="fileInput" style="display:none;" accept="image/*" onchange="handleFileSelect(event)">
            <div id="fileInfo" style="margin-top:12px; font-size:12px; color:#d85b72;"></div>
          </div>
        </div>

        <div class="tool-pane">
          <div class="tool-pane-head">Ajustes & Processamento<span>Passo 2</span></div>
          <div class="tool-pane-body">
            <div class="tool-form">
              <div class="tool-field">
                <label>Filtro de Iluminação</label>
                <select id="toolFilter">
                  <option>Estúdio Neon / Cyber Dark</option>
                  <option>Golden Hour / Luz Natural da Tarde</option>
                  <option>Flash Direto / Câmera Noturna</option>
                  <option>Quarto com Luz Difusa / Sensual</option>
                </select>
              </div>
              <div class="tool-field">
                <label>Nível de Consistência Facial</label>
                <select id="toolStrength">
                  <option>Fidelidade Máxima (0.90)</option>
                  <option>Equilibrado (0.75)</option>
                  <option>Criativo (0.60)</option>
                </select>
              </div>
              <button class="tool-primary" type="button" onclick="processTool()">⚡ APLICAR PRESET IA</button>
              <div class="tool-status" id="toolStatus"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 6: AFILIADOS & SAQUE -->
    <section class="tab-panel" id="tab-afiliados">
      <h1 style="font-family:'Anton'; font-size:26px; margin:0 0 6px;">INDIQUE E GANHE (50% DE COMISSÃO)</h1>
      <p style="color:#aaa; font-size:13px; margin:0 0 20px;">Ganhe R$ 43,95 por cada indicação confirmada com seu link exclusivo.</p>

      <div class="ref-withdraw-card">
        <div>
          <span style="font-size:12px; color:#a79da1; text-transform:uppercase; font-weight:700;">Seu Saldo Disponível</span>
          <strong>R$ 439,50</strong>
          <p>Disponível para saque imediato via PIX na sua conta bancária.</p>
        </div>
        <button class="ref-withdraw-button" onclick="openWithdrawModal()">SOLICITAR SAQUE PIX</button>
      </div>

      <div style="background:var(--card); border:1px solid var(--line); border-radius:14px; padding:20px; margin-bottom:24px;">
        <h3 style="margin:0 0 10px; font-size:15px;">Seu Link de Afiliado</h3>
        <div style="display:flex; gap:10px;">
          <input type="text" id="refLink" value="https://capivaraclubhot.com/?ref=VIP-98421" readonly style="flex:1; background:#0b0b0b; border:1px solid var(--line); border-radius:8px; padding:12px; color:#eee;">
          <button class="btn-action" style="width:auto; padding:0 24px;" onclick="copyRefLink()">COPIAR LINK</button>
        </div>
      </div>

      <h3 style="font-size:16px; margin:24px 0 12px;">Histórico de Saques</h3>
      <div class="ref-withdraw-history">
        <div><strong>R$ 219,75</strong> • Saque Concluído via Chave PIX • 01/10/2026</div>
        <div><strong>R$ 175,80</strong> • Saque Concluído via Chave PIX • 24/09/2026</div>
      </div>
    </section>

  </main>

  <!-- Video Player Modal -->
  <div class="video-modal hidden" id="videoModal" onclick="closeVideoModal(event)">
    <div class="video-dialog" onclick="event.stopPropagation()">
      <div class="video-head">
        <h3 id="videoModalTitle">Aula em Vídeo</h3>
        <button class="video-close" onclick="closeVideoModal()">×</button>
      </div>
      <div style="padding:20px;">
        <div class="video-box" style="width:100%; aspect-ratio:16/9; background:#000;">
          <div class="video-security-watermark">VIP • membro@capivaraclubhot.com</div>
          <div style="text-align:center; padding:40px; color:#8e8589;">
            <div style="font-size:48px; margin-bottom:12px; color:#7a1025;">🎬</div>
            <strong style="color:#d9d1d4; font-size:16px; display:block;">Player de Alta Definição Pronto</strong>
            <p style="font-size:12px; margin-top:8px;">Carregando transmissão segura criptografada...</p>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Prompt Modal -->
  <div class="video-modal hidden" id="promptModal" onclick="closePromptModal(event)">
    <div class="video-dialog" onclick="event.stopPropagation()">
      <div class="video-head">
        <h3 id="promptModalTitle">Visualizador de Prompt</h3>
        <button class="video-close" onclick="closePromptModal()">×</button>
      </div>
      <div style="padding:20px;">
        <textarea id="promptModalText" readonly style="width:100%; height:160px; background:#060304; border:1px solid var(--line); border-radius:10px; color:#eee; padding:12px; font-family:'Space Mono', monospace; font-size:12px; resize:none; box-sizing:border-box;"></textarea>
        <button class="btn-action" style="margin-top:14px;" onclick="copyPromptFromModal()">COPIAR PROMPT</button>
      </div>
    </div>
  </div>

  <!-- Modal de Saque -->
  <div class="ref-withdraw-modal hidden" id="withdrawModal" onclick="closeWithdrawModal(event)">
    <div class="ref-withdraw-dialog" onclick="event.stopPropagation()">
      <div class="ref-withdraw-head">
        <h2>Solicitar Saque</h2>
        <button onclick="closeWithdrawModal()">×</button>
      </div>
      <div style="margin-top:16px; display:grid; gap:14px;">
        <p style="color:#aaa; font-size:12px; margin:0;">Informe sua chave PIX para transferência do saldo disponível (R$ 439,50).</p>
        <div>
          <label style="font-size:12px; color:#ccc;">Tipo de Chave</label>
          <select style="width:100%; background:#0b0b0b; border:1px solid var(--line); border-radius:8px; padding:10px; color:#eee; margin-top:4px;">
            <option>CPF</option>
            <option>E-mail</option>
            <option>Telefone</option>
            <option>Chave Aleatória (EVP)</option>
          </select>
        </div>
        <div>
          <label style="font-size:12px; color:#ccc;">Chave PIX</label>
          <input type="text" placeholder="Digite sua chave" style="width:100%; background:#0b0b0b; border:1px solid var(--line); border-radius:8px; padding:10px; color:#eee; margin-top:4px; box-sizing:border-box;">
        </div>
        <button class="ref-withdraw-button" onclick="confirmWithdraw()">CONFIRMAR SAQUE</button>
      </div>
    </div>
  </div>

  <script>
    // Tab switching
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
      
      const targetBtn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick')?.includes(tabId));
      if (targetBtn) targetBtn.classList.add('active');
      
      const targetPanel = document.getElementById('tab-' + tabId);
      if (targetPanel) targetPanel.classList.add('active');
    }

    // Prompts Database
    const samplePrompts = [
      {
        tag: "Sensual & Lingerie",
        title: "Lingerie de Seda Vinho em Quarto Escuro",
        desc: "Luz de vela e neon vermelho suave, pele ultra-detalhada com poros visíveis, olhar penetrante.",
        prompt: "ultra realistic raw photo of a 22yo brazilian model in dark wine silk lingerie, soft red neon backlight, studio lighting, depth of field, 8k resolution, photorealistic skin texture, natural pores, Canon EOS R5 85mm f/1.4",
        img: "../imagens/foto-1.webp"
      },
      {
        tag: "Praia & Biquíni",
        title: "Pôr do Sol Dourado na Praia",
        desc: "Biquíni micro dourado, gotas de água escorrendo pelo corpo, cabelo úmido ao vento.",
        prompt: "candid golden hour beach photo, gorgeous model in micro bikini, wet skin with visible water droplets, ocean waves in background, warm natural sunlight, masterpiece, 8k uhd, cinematic lighting, shot on 35mm lens",
        img: "../imagens/foto-2.webp"
      },
      {
        tag: "UGC / Instagram",
        title: "Selfie no Espelho da Academia",
        desc: "Estilo foto tirada por smartphone, roupa fitness justa, ângulo casual e natural.",
        prompt: "instagram mirror selfie, fitness woman in tight athletic crop top and leggings, luxury gym locker room background, casual natural pose, realistic smartphone camera blur, film grain, authentic expression",
        img: "../imagens/foto-3.webp"
      },
      {
        tag: "Urbano & Noite",
        title: "Close-up em Cidade Noturna",
        desc: "Jaqueta de couro aberta, bokeh de luzes de neon da metrópole ao fundo.",
        prompt: "cyberpunk city night street portrait, sensual woman wearing open black leather jacket, city neon bokeh background, rain reflections, sharp focus on eyes, dramatic volumetric lighting, cinematic 8k",
        img: "../imagens/foto-4.webp"
      },
      {
        tag: "Moda & Close-up",
        title: "Retrato de Estúdio com Luz Direta",
        desc: "Foco extremo no rosto, maquiagem impecável, sombras marcantes e visual sofisticado.",
        prompt: "vogue studio close-up portrait, high fashion model, exquisite makeup, intense gaze, direct harsh flash lighting, rich shadows, hyperdetailed eyes and lips, Hasselblad H6D-100c quality",
        img: "../imagens/foto-5.webp"
      },
      {
        tag: "Sensual & Biquíni",
        title: "Piscina com Iluminação Noturna",
        desc: "Saindo da água com reflexos de água cristalina iluminada por led azul e roxo.",
        prompt: "luxurious night pool party shot, stunning model emerging from crystalline illuminated water, wet hair, neon blue and violet pool lights reflections, glistening skin, ultra realistic",
        img: "../imagens/foto-6.webp"
      }
    ];

    const promptsGrid = document.getElementById('promptsGrid');
    samplePrompts.forEach((p, idx) => {
      const card = document.createElement('div');
      card.className = 'custom-card';
      card.innerHTML = `
        <img src="${p.img}" class="card-thumb" alt="${p.title}">
        <div class="card-body">
          <span class="card-tag">${p.tag}</span>
          <h3 class="card-title">${p.title}</h3>
          <p class="card-desc">${p.desc}</p>
          <div style="display:flex; gap:8px;">
            <button class="btn-action" onclick="viewPrompt(${idx})">Ver Prompt</button>
            <button class="btn-action" style="background:#1b0c12; border:1px solid var(--line);" onclick="copyPromptDirect('${encodeURIComponent(p.prompt)}')">Copiar</button>
          </div>
        </div>
      `;
      promptsGrid.appendChild(card);
    });

    // Modals handlers
    function openVideoPlayer(title) {
      document.getElementById('videoModalTitle').textContent = title;
      document.getElementById('videoModal').classList.remove('hidden');
    }
    function closeVideoModal() {
      document.getElementById('videoModal').classList.add('hidden');
    }

    function viewPrompt(idx) {
      const p = samplePrompts[idx];
      document.getElementById('promptModalTitle').textContent = p.title;
      document.getElementById('promptModalText').value = p.prompt;
      document.getElementById('promptModal').classList.remove('hidden');
    }
    function closePromptModal() {
      document.getElementById('promptModal').classList.add('hidden');
    }
    function copyPromptFromModal() {
      const text = document.getElementById('promptModalText').value;
      navigator.clipboard.writeText(text);
      ClubUI.alert('Prompt copiado para a área de transferência!');
      closePromptModal();
    }
    function copyPromptDirect(encodedText) {
      navigator.clipboard.writeText(decodeURIComponent(encodedText));
      ClubUI.alert('Prompt copiado com sucesso!');
    }

    function openWithdrawModal() {
      document.getElementById('withdrawModal').classList.remove('hidden');
    }
    function closeWithdrawModal() {
      document.getElementById('withdrawModal').classList.add('hidden');
    }
    function confirmWithdraw() {
      ClubUI.alert('Solicitação de saque PIX enviada com sucesso! O pagamento será processado em até 2 horas úteis.');
      closeWithdrawModal();
    }

    function copyRefLink() {
      const link = document.getElementById('refLink').value;
      navigator.clipboard.writeText(link);
      ClubUI.alert('Link de afiliado copiado! Compartilhe e ganhe 50% de comissão por indicação.');
    }

    function handleFileSelect(e) {
      const file = e.target.files[0];
      if (file) {
        document.getElementById('fileInfo').textContent = `Foto selecionada: ${file.name} (${(file.size/1024/1024).toFixed(2)} MB)`;
      }
    }

    function processTool() {
      const file = document.getElementById('fileInput').files[0];
      const status = document.getElementById('toolStatus');
      if (!file) {
        ClubUI.alert('Por favor, selecione uma foto de referência primeiro.');
        return;
      }
      status.textContent = 'Processando com algoritmo de iluminação...';
      setTimeout(() => {
        status.textContent = '✓ Processamento concluído! Preset aplicado com sucesso.';
      }, 1500);
    }

    function logout() {
      localStorage.removeItem('capivara_user');
      window.location.href = 'membros.html';
    }
  </script>
</body>
</html>
"""

import os
with open("paginas/painel.html", "w", encoding="utf-8") as f:
    f.write(painel_html)

print("paginas/painel.html criado com sucesso com 100% de fidelidade e interatividade!")
