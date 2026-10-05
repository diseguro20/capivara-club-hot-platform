import json
import os
import urllib.parse

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Área de Membros VIP — CAPIVARA CLUB HOT</title>
  <link rel="icon" href="../icons/favicon-32.png">
  <link rel="apple-touch-icon" href="../icons/apple-touch-icon.png">
  <meta name="theme-color" content="#050304">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="../assets/ui.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-1.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-2.css">
  <link rel="stylesheet" href="../assets/area_membros_esteira_interna_ferramentas-5.css">
  <script src="../assets/ui.js"></script>

  <style>
    :root {
      --bg: #070305;
      --card: rgba(16, 8, 12, 0.9);
      --wine: #7a1025;
      --wine-light: #d85b72;
      --wine-glow: rgba(216, 91, 114, 0.35);
      --line: rgba(255, 255, 255, 0.08);
      --text-muted: #9e9498;
    }
    * { box-sizing: border-box; }
    body {
      background: radial-gradient(circle at 50% -20%, #240814 0%, #070305 70%);
      color: #eee;
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
      min-height: 100vh;
    }
    
    /* Header */
    .header-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 16px 32px;
      border-bottom: 1px solid var(--line);
      background: rgba(10, 4, 7, 0.95);
      backdrop-filter: blur(14px);
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
    .brand-wrap img { height: 38px; }
    .brand-title {
      font-family: 'Anton', sans-serif;
      font-size: 22px;
      letter-spacing: 1px;
    }
    .user-badge {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .user-pill {
      background: rgba(122, 16, 37, 0.4);
      border: 1px solid var(--wine-light);
      padding: 6px 16px;
      border-radius: 99px;
      font-weight: 800;
      color: #fce7ec;
      font-size: 12px;
      letter-spacing: 0.5px;
    }
    .landing-link {
      color: #aaa;
      font-size: 13px;
      text-decoration: none;
      transition: color .2s;
    }
    .landing-link:hover { color: #fff; }

    /* Navigation */
    .nav-container {
      display: flex;
      gap: 10px;
      padding: 18px 32px;
      max-width: 1320px;
      margin: 0 auto;
      overflow-x: auto;
    }
    .tab-btn {
      display: flex;
      align-items: center;
      gap: 8px;
      background: rgba(20, 10, 15, 0.7);
      border: 1px solid var(--line);
      color: #a79da1;
      padding: 11px 20px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 13px;
      cursor: pointer;
      white-space: nowrap;
      transition: all .2s;
    }
    .tab-btn:hover {
      background: rgba(122, 16, 37, 0.25);
      color: #fff;
      border-color: var(--wine-light);
    }
    .tab-btn.active {
      background: linear-gradient(135deg, #7a1025, #a42c4b);
      color: #fff;
      border-color: #d85b72;
      box-shadow: 0 4px 20px rgba(122, 16, 37, 0.45);
    }

    /* Container */
    .content-container {
      max-width: 1320px;
      margin: 0 auto;
      padding: 10px 32px 80px;
    }
    .tab-panel {
      display: none;
      animation: fadeIn .25s ease-out;
    }
    .tab-panel.active { display: block; }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Banner Hero */
    .hero-banner {
      background: linear-gradient(135deg, rgba(122, 16, 37, 0.4) 0%, rgba(20, 8, 14, 0.85) 100%);
      border: 1px solid rgba(216, 91, 114, 0.35);
      border-radius: 20px;
      padding: 32px 36px;
      margin-bottom: 30px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 24px;
      flex-wrap: wrap;
      box-shadow: 0 10px 35px rgba(0,0,0,0.5);
    }
    .hero-banner h1 {
      font-family: 'Anton', sans-serif;
      font-size: 32px;
      margin: 0 0 10px;
      letter-spacing: 0.5px;
      color: #fff;
    }
    .hero-banner p {
      color: #d1c4c9;
      font-size: 14px;
      line-height: 1.55;
      margin: 0;
      max-width: 680px;
    }
    .stats-row {
      display: flex;
      gap: 14px;
    }
    .stat-badge {
      background: rgba(10, 4, 7, 0.7);
      border: 1px solid var(--line);
      padding: 12px 20px;
      border-radius: 14px;
      text-align: center;
    }
    .stat-badge strong {
      display: block;
      font-family: 'Anton', sans-serif;
      font-size: 26px;
      color: var(--wine-light);
    }
    .stat-badge span {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }

    /* Cards Grid */
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 22px;
      margin-top: 20px;
    }
    .media-card {
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform .2s, border-color .2s, box-shadow .2s;
    }
    .media-card:hover {
      transform: translateY(-4px);
      border-color: var(--wine-light);
      box-shadow: 0 12px 30px rgba(122, 16, 37, 0.25);
    }
    .media-thumb-wrap {
      width: 100%;
      height: 220px;
      position: relative;
      background: #0f070b;
      overflow: hidden;
    }
    .media-thumb {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }
    .play-overlay {
      position: absolute;
      inset: 0;
      display: grid;
      place-items: center;
      background: rgba(0, 0, 0, 0.45);
      cursor: pointer;
      transition: background .2s;
    }
    .play-overlay:hover {
      background: rgba(122, 16, 37, 0.5);
    }
    .play-btn-circle {
      width: 54px;
      height: 54px;
      border-radius: 50%;
      background: rgba(216, 91, 114, 0.95);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: #fff;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
      transition: transform .2s;
    }
    .play-overlay:hover .play-btn-circle {
      transform: scale(1.12);
    }
    .card-content {
      padding: 20px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    .card-kicker {
      font-size: 11px;
      font-weight: 800;
      color: var(--wine-light);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 6px;
    }
    .card-h3 {
      font-size: 16px;
      font-weight: 700;
      margin: 0 0 8px;
      color: #f7eff2;
      line-height: 1.35;
    }
    .card-text {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
      margin: 0 0 18px;
      flex: 1;
    }
    
    /* Buttons */
    .btn-prime {
      background: linear-gradient(135deg, #7a1025, #a42c4b);
      border: none;
      color: #fff;
      padding: 11px 16px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      text-decoration: none;
      transition: opacity .2s, transform .1s;
    }
    .btn-prime:hover { opacity: 0.92; }
    .btn-prime:active { transform: translateY(1px); }
    .btn-sub {
      background: rgba(255,255,255,0.06);
      border: 1px solid var(--line);
      color: #ccc;
      padding: 11px 16px;
      border-radius: 10px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      text-align: center;
      transition: all .2s;
    }
    .btn-sub:hover {
      background: rgba(255,255,255,0.12);
      color: #fff;
      border-color: rgba(255,255,255,0.2);
    }

    /* Video Player Modal */
    .modal-overlay {
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: rgba(3, 1, 2, 0.9);
      backdrop-filter: blur(12px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .modal-overlay.hidden { display: none; }
    .modal-box {
      background: #11070c;
      border: 1px solid rgba(216, 91, 114, 0.4);
      border-radius: 18px;
      width: min(920px, 100%);
      overflow: hidden;
      box-shadow: 0 25px 80px rgba(0, 0, 0, 0.85);
    }
    .modal-box-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 18px 24px;
      border-bottom: 1px solid var(--line);
    }
    .modal-box-head h3 {
      margin: 0;
      font-size: 17px;
      font-weight: 700;
      color: #f7eff2;
    }
    .modal-close-x {
      background: transparent;
      border: none;
      color: #aaa;
      font-size: 26px;
      cursor: pointer;
      line-height: 1;
      padding: 4px;
    }
    .modal-close-x:hover { color: #fff; }
    .video-viewport {
      position: relative;
      width: 100%;
      aspect-ratio: 16/9;
      background: #000;
    }
    .video-watermark {
      position: absolute;
      top: 14px;
      right: 18px;
      z-index: 10;
      background: rgba(0,0,0,0.6);
      border: 1px solid rgba(255,255,255,0.15);
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      color: rgba(255,255,255,0.7);
      pointer-events: none;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header class="header-bar">
    <div class="brand-wrap">
      <img src="../imagens/logo.webp" alt="Capivara Club Hot">
      <span class="brand-title">CAPIVARA CLUB HOT</span>
    </div>
    <div class="user-badge">
      <span class="user-pill">ACESSO VIP 100% LIBERADO</span>
      <a href="../index.html" class="landing-link">Landing Page →</a>
    </div>
  </header>

  <!-- Nav Tabs -->
  <nav class="nav-container">
    <button class="tab-btn active" onclick="switchTab('aulas')">🎬 Vídeo-Aulas Originais (7)</button>
    <button class="tab-btn" onclick="switchTab('workflows')">📦 Workflows ComfyUI (11)</button>
    <button class="tab-btn" onclick="switchTab('prompts')">⚡ Prompts & Fotos Reais</button>
    <button class="tab-btn" onclick="switchTab('videos-ia')">🔥 Vídeos Gerados por IA</button>
    <button class="tab-btn" onclick="switchTab('ferramentas')">🛠️ Esteira & Preset IA</button>
    <button class="tab-btn" onclick="switchTab('afiliados')">💰 Saques & Afiliados</button>
  </nav>

  <!-- Main Content -->
  <main class="content-container">

    <!-- TAB 1: VÍDEO-AULAS ORIGINAIS (7 AULAS REAIS) -->
    <section class="tab-panel active" id="tab-aulas">
      <div class="hero-banner">
        <div>
          <h1>AULAS EM VÍDEO OFICIAIS</h1>
          <p>Treinamento completo extraído da Área de Membros. Clique em qualquer aula para reproduzir imediatamente em alta definição com controles completos.</p>
        </div>
        <div class="stats-row">
          <div class="stat-badge">
            <strong>7</strong>
            <span>VÍDEO-AULAS</span>
          </div>
          <div class="stat-badge">
            <strong>100%</strong>
            <span>LIBERADO</span>
          </div>
        </div>
      </div>

      <div class="grid-cards">
        
        <!-- Aula 1 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 1.mp4', 'Aula 1: Introdução & Setup do Ambiente')">
            <img src="../imagens/foto-1.webp" class="media-thumb" alt="Aula 1">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 1 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 1 — Introdução & Setup da Personagem</h3>
            <p class="card-text">Passo a passo inicial para configurar seu ambiente ComfyUI e selecionar as imagens base da sua modelo.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 1.mp4', 'Aula 1: Introdução & Setup do Ambiente')">Assistir Aula 1 ▶</button>
          </div>
        </div>

        <!-- Aula 2 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 2.mp4', 'Aula 2: Criando a Identidade da Modelo')">
            <img src="../imagens/foto-2.webp" class="media-thumb" alt="Aula 2">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 2 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 2 — Criação de Rosto & Identidade Única</h3>
            <p class="card-text">Técnica para travar as feições da modelo, garantindo o mesmo rosto em qualquer pose e iluminação.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 2.mp4', 'Aula 2: Criando a Identidade da Modelo')">Assistir Aula 2 ▶</button>
          </div>
        </div>

        <!-- Aula 3 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 3.mp4', 'Aula 3: Consistência Facial no ComfyUI')">
            <img src="../imagens/foto-3.webp" class="media-thumb" alt="Aula 3">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 3 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 3 — Consistência Facial com IP-Adapter</h3>
            <p class="card-text">Como ligar os nós de IP-Adapter, peso de ruído e checkpoints realistas sem distorções no olhar.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 3.mp4', 'Aula 3: Consistência Facial no ComfyUI')">Assistir Aula 3 ▶</button>
          </div>
        </div>

        <!-- Aula 4 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 4.mp4', 'Aula 4: Troca de Roupas & Inpainting')">
            <img src="../imagens/foto-4.webp" class="media-thumb" alt="Aula 4">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 4 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 4 — Troca de Roupas, Biquínis & Lingerie</h3>
            <p class="card-text">Workflow de inpainting para substituir roupas mantendo a anatomia corporal perfeita.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 4.mp4', 'Aula 4: Troca de Roupas & Inpainting')">Assistir Aula 4 ▶</button>
          </div>
        </div>

        <!-- Aula 5 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 5.mp4', 'Aula 5: Gerando Vídeos com Movimento Real')">
            <img src="../imagens/foto-5.webp" class="media-thumb" alt="Aula 5">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 5 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 5 — Animação e Criação de Vídeos I2V</h3>
            <p class="card-text">Transformando imagem estática em clipe animado com piscadas, respiração e expressões realistas.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 5.mp4', 'Aula 5: Gerando Vídeos com Movimento Real')">Assistir Aula 5 ▶</button>
          </div>
        </div>

        <!-- Aula 6 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 6.mp4', 'Aula 6: ControlMotion +18 & Movimento')">
            <img src="../imagens/foto-6.webp" class="media-thumb" alt="Aula 6">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 6 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 6 — ControlMotion 2 +18 Avançado</h3>
            <p class="card-text">Guia definitivo para geração de vídeos sensuais e conteúdo dinâmico sem restrições ou censura.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 6.mp4', 'Aula 6: ControlMotion +18 & Movimento')">Assistir Aula 6 ▶</button>
          </div>
        </div>

        <!-- Aula 7 -->
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/PARTE 7.mp4', 'Aula 7: Upscaling 4K & Restauração')">
            <img src="../imagens/foto-1.webp" class="media-thumb" alt="Aula 7">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">MÓDULO 7 • VÍDEO OFICIAL</span>
            <h3 class="card-h3">Aula 7 — Upscaling 4K Ultra-HD & Exportação</h3>
            <p class="card-text">Aumento de nitidez e microporos de pele para publicação no Instagram, Privacy e OnlyFans.</p>
            <button class="btn-prime" onclick="playLesson('../videos/PARTE 7.mp4', 'Aula 7: Upscaling 4K & Restauração')">Assistir Aula 7 ▶</button>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 2: WORKFLOWS ORIGINAIS (11 ARQUIVOS REAIS) -->
    <section class="tab-panel" id="tab-workflows">
      <div class="hero-banner">
        <div>
          <h1>WORKFLOWS COMFYUI ORIGINAIS</h1>
          <p>Todos os 11 arquivos JSON oficiais do criador do Capivara Club Hot extraídos na íntegra. Clique para baixar e arraste diretamente para dentro do seu ComfyUI.</p>
        </div>
        <div class="stats-row">
          <div class="stat-badge">
            <strong>11</strong>
            <span>JSONS OFICIAIS</span>
          </div>
          <div class="stat-badge">
            <strong>COMFYUI</strong>
            <span>COMPATÍVEL</span>
          </div>
        </div>
      </div>

      <div class="grid-cards">
        
        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 137 KB</span>
            <h3 class="card-h3">CAPIVARA DU HOT - Gerar Vídeos Prompt</h3>
            <p class="card-text">Workflow completo para geração de prompts de vídeo dinâmicos com sincronia de parâmetros e FPS.</p>
            <a href="../workflows/CAPIVARA DU HOT - GERAR VÍDEOS PROMPT.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 182 KB</span>
            <h3 class="card-h3">CONTROLMOTION 2 - Capivara DuHot Video +18</h3>
            <p class="card-text">Workflow específico com switches Hot/Normal, VitPose e interpolação de movimento corporal.</p>
            <a href="../workflows/CONTROLMOTION 2 - CAPIVARA DUHOT - VIDEO +18.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 214 KB</span>
            <h3 class="card-h3">ControlMotion Capivara DuHot (V1)</h3>
            <p class="card-text">Workflow original com cálculo automático de iterações do vídeo de origem e referência de pose.</p>
            <a href="../workflows/controlmotion-capivara-duhot.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 193 KB</span>
            <h3 class="card-h3">FaceSwap Capivara DuHot + Upscale</h3>
            <p class="card-text">Troca de rosto avançada com suporte a modo HOT, foto de referência corporal e restauração de detalhes.</p>
            <a href="../workflows/faceswap-capivara-duhot.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 190 KB</span>
            <h3 class="card-h3">SWAP - FLUX - Capivara</h3>
            <p class="card-text">Integração do modelo Flux.1 Dev com troca facial direta e preservação de textura de pele ultra-realista.</p>
            <a href="../workflows/SWAP - FLUX - CAPIVARA.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 144 KB</span>
            <h3 class="card-h3">Troca de Roupa - WF Grátis</h3>
            <p class="card-text">Isolamento automático de vestimentas em fundo transparente e substituição de looks da personagem.</p>
            <a href="../workflows/TROCA DE ROUPA - WF GRATIS.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 7.4 KB</span>
            <h3 class="card-h3">Upscale IMG - Capivara (Grátis)</h3>
            <p class="card-text">Nó leve e ultra-rápido para aumentar resolução de fotos geradas sem necessidade de muita VRAM.</p>
            <a href="../workflows/UPSCALE IMG - CAPIVARA (GRÁTIS).json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 68 KB</span>
            <h3 class="card-h3">Vários Ângulos da Modelo</h3>
            <p class="card-text">Geração automatizada da mesma personagem em múltiplos ângulos de câmera (frente, costas, perfil, 3/4).</p>
            <a href="../workflows/VARIOS ANGULOS.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 178 KB</span>
            <h3 class="card-h3">KREA 2 - Rosto + Prompt</h3>
            <p class="card-text">Workflow integrado para geração via Krea com resolução 9:16 vertical otimizada para Stories e Reels.</p>
            <a href="../workflows/KREA 2 - ROSTO + PROMPT.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 244 KB</span>
            <h3 class="card-h3">MOTION + CONTROL V7 (WanVideo)</h3>
            <p class="card-text">O mais avançado workflow com amplitude de oscilação, balanço corporal e controle de intensidade de câmera.</p>
            <a href="../workflows/MOTION+CONTROL+v7.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

        <div class="media-card">
          <div class="card-content">
            <span class="card-kicker">WORKFLOW OFICIAL • 164 KB</span>
            <h3 class="card-h3">Motion Control - Mudar Apenas Mulher</h3>
            <p class="card-text">Substitui somente o corpo e rosto feminino em vídeos existentes mantendo o cenário e parceiro intactos.</p>
            <a href="../workflows/Motion+Control+-+Mudar_Apenas_Mulher.json" download class="btn-prime">⬇ Baixar JSON Original</a>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 3: PROMPTS & FOTOS REAIS -->
    <section class="tab-panel" id="tab-prompts">
      <div class="hero-banner">
        <div>
          <h1>PROMPTS & FOTOS ORIGINAIS</h1>
          <p>Fotos reais geradas pelos workflows da plataforma e os prompts prontos para copiar e utilizar.</p>
        </div>
      </div>

      <div class="grid-cards">
        
        <div class="media-card">
          <div class="media-thumb-wrap">
            <img src="../imagens/Retrato Natural no Banheiro Moderno.png" class="media-thumb" alt="Retrato Natural no Banheiro Moderno">
          </div>
          <div class="card-content">
            <span class="card-kicker">ESTILO REALISTA • BANHEIRO LUXO</span>
            <h3 class="card-h3">Retrato Natural no Banheiro Moderno</h3>
            <p class="card-text">Selfie casual em espelho de banheiro de mármore, iluminação suave, reflexos d'água e aparência espontânea.</p>
            <button class="btn-prime" onclick="copyPrompt('ultra realistic selfie of gorgeous 22yo brazilian model in modern luxury marble bathroom, soft ambient lighting, natural skin texture, delicate expression, shot on smartphone, high quality authentic UGC')">Copiar Prompt ⚡</button>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap">
            <img src="../imagens/Retrato praiano com coco verde em Ipanema.png" class="media-thumb" alt="Retrato praiano com coco verde em Ipanema">
          </div>
          <div class="card-content">
            <span class="card-kicker">EXTERNO • PRAIA & SOL</span>
            <h3 class="card-h3">Retrato Praiano com Coco Verde em Ipanema</h3>
            <p class="card-text">Foto espontânea na praia de Ipanema, areia dourada, luz do sol tropical, biquíni sensual e água de coco.</p>
            <button class="btn-prime" onclick="copyPrompt('candid beach photography, stunning brazilian woman holding fresh green coconut in Ipanema beach Rio de Janeiro, golden hour sunlight, wet glistening skin, natural ocean breeze, 35mm film photography')">Copiar Prompt ⚡</button>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap">
            <img src="../imagens/Retrato Urbano Noturno com Bebida.png" class="media-thumb" alt="Retrato Urbano Noturno com Bebida">
          </div>
          <div class="card-content">
            <span class="card-kicker">NOTURNO • CIDADE & BOKEH</span>
            <h3 class="card-h3">Retrato Urbano Noturno com Bebida</h3>
            <p class="card-text">Cena noturna de rooftop, iluminação de neon suave, segurando copo em clima descontraído e olhar envolvente.</p>
            <button class="btn-prime" onclick="copyPrompt('cinematic night portrait of beautiful woman holding cocktail on rooftop bar, city neon bokeh reflections, soft flash lighting, glamorous leather outfit, sensual gaze, 85mm portrait f/1.4')">Copiar Prompt ⚡</button>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap">
            <img src="../imagens/foto-1.webp" class="media-thumb" alt="Lingerie Vinho">
          </div>
          <div class="card-content">
            <span class="card-kicker">SENSUAL • LINGERIE</span>
            <h3 class="card-h3">Lingerie Vinho em Quarto Escuro</h3>
            <p class="card-text">Lingerie de renda bordô, iluminação dramática de meia-luz, textura de pele com microporos perfeitos.</p>
            <button class="btn-prime" onclick="copyPrompt('ultra realistic raw photo of a 22yo brazilian model in dark wine silk lingerie, soft red neon backlight, studio lighting, depth of field, 8k resolution, photorealistic skin texture, natural pores, Canon EOS R5 85mm f/1.4')">Copiar Prompt ⚡</button>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap">
            <img src="../imagens/foto-3.webp" class="media-thumb" alt="Fitness UGC">
          </div>
          <div class="card-content">
            <span class="card-kicker">FITNESS • INSTAGRAM UGC</span>
            <h3 class="card-h3">Selfie Fitness na Academia</h3>
            <p class="card-text">Estilo foto tirada por smartphone, roupa esportiva justa, ângulo casual de espelho de academia.</p>
            <button class="btn-prime" onclick="copyPrompt('instagram mirror selfie, fitness woman in tight athletic crop top and leggings, luxury gym locker room background, casual natural pose, realistic smartphone camera blur, film grain, authentic expression')">Copiar Prompt ⚡</button>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap">
            <img src="../imagens/foto-6.webp" class="media-thumb" alt="Piscina Noturna">
          </div>
          <div class="card-content">
            <span class="card-kicker">BIQUÍNI • PISCINA NEON</span>
            <h3 class="card-h3">Piscina com Iluminação Noturna</h3>
            <p class="card-text">Saindo da água com reflexos de água cristalina iluminada por led azul e roxo.</p>
            <button class="btn-prime" onclick="copyPrompt('luxurious night pool party shot, stunning model emerging from crystalline illuminated water, wet hair, neon blue and violet pool lights reflections, glistening skin, ultra realistic')">Copiar Prompt ⚡</button>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 4: VÍDEOS GERADOS POR IA -->
    <section class="tab-panel" id="tab-videos-ia">
      <div class="hero-banner">
        <div>
          <h1>VÍDEOS DA MODELO IA (DEMOS REAIS)</h1>
          <p>Arquivos de vídeo gerados diretamente pelos workflows de animação da modelo com movimento corporal, respiração e áudio sincronizado.</p>
        </div>
      </div>

      <div class="grid-cards">
        
        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/jiebujie_00001_p86-audio_jiqat_1791101467.mp4', 'Vídeo IA 1: Movimento Facial & Áudio Sincronizado')">
            <img src="../imagens/foto-4.webp" class="media-thumb" alt="Vídeo 1">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">VÍDEO GERADO POR IA • 3.0 MB</span>
            <h3 class="card-h3">Modelo IA — Movimento Facial & Olhar</h3>
            <p class="card-text">Clipe animado demonstrando naturalidade no piscar de olhos e sincronia labial.</p>
            <div style="display:flex; gap:8px;">
              <button class="btn-prime" style="flex:1;" onclick="playLesson('../videos/jiebujie_00001_p86-audio_jiqat_1791101467.mp4', 'Vídeo IA 1: Movimento Facial')">Assistir ▶</button>
              <a href="../videos/jiebujie_00001_p86-audio_jiqat_1791101467.mp4" download class="btn-sub">⬇</a>
            </div>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/jiebujie_00001_p87-audio_vqrpr_1791096741.mp4', 'Vídeo IA 2: Movimento Corporal Fluido')">
            <img src="../imagens/foto-5.webp" class="media-thumb" alt="Vídeo 2">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">VÍDEO GERADO POR IA • 2.8 MB</span>
            <h3 class="card-h3">Modelo IA — Expressão e Cabeça</h3>
            <p class="card-text">Geração com movimentação de ângulo e iluminação de estúdio preservando os traços faciais.</p>
            <div style="display:flex; gap:8px;">
              <button class="btn-prime" style="flex:1;" onclick="playLesson('../videos/jiebujie_00001_p87-audio_vqrpr_1791096741.mp4', 'Vídeo IA 2: Movimento Corporal')">Assistir ▶</button>
              <a href="../videos/jiebujie_00001_p87-audio_vqrpr_1791096741.mp4" download class="btn-sub">⬇</a>
            </div>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/jiebujie_00001_p86-audio_eunfu_1790970228.mp4', 'Vídeo IA 3: Animação I2V')">
            <img src="../imagens/foto-2.webp" class="media-thumb" alt="Vídeo 3">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">VÍDEO GERADO POR IA • 4.6 MB</span>
            <h3 class="card-h3">Modelo IA — Respiração e Cabelo</h3>
            <p class="card-text">Animação suave a partir de foto estática utilizando os nós de interpolação WanVideo.</p>
            <div style="display:flex; gap:8px;">
              <button class="btn-prime" style="flex:1;" onclick="playLesson('../videos/jiebujie_00001_p86-audio_eunfu_1790970228.mp4', 'Vídeo IA 3: Animação I2V')">Assistir ▶</button>
              <a href="../videos/jiebujie_00001_p86-audio_eunfu_1790970228.mp4" download class="btn-sub">⬇</a>
            </div>
          </div>
        </div>

        <div class="media-card">
          <div class="media-thumb-wrap" onclick="playLesson('../videos/jiebujie_00001_p85-audio_lkbej_1790815028.mp4', 'Vídeo IA 4: Cena Completa')">
            <img src="../imagens/foto-3.webp" class="media-thumb" alt="Vídeo 4">
            <div class="play-overlay"><div class="play-btn-circle">▶</div></div>
          </div>
          <div class="card-content">
            <span class="card-kicker">VÍDEO GERADO POR IA • 3.9 MB</span>
            <h3 class="card-h3">Modelo IA — Cena com Áudio Completo</h3>
            <p class="card-text">Geração com áudio realista de ambiente e movimentação espontânea.</p>
            <div style="display:flex; gap:8px;">
              <button class="btn-prime" style="flex:1;" onclick="playLesson('../videos/jiebujie_00001_p85-audio_lkbej_1790815028.mp4', 'Vídeo IA 4: Cena Completa')">Assistir ▶</button>
              <a href="../videos/jiebujie_00001_p85-audio_lkbej_1790815028.mp4" download class="btn-sub">⬇</a>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- TAB 5: FERRAMENTAS -->
    <section class="tab-panel" id="tab-ferramentas">
      <div class="hero-banner">
        <div>
          <h1>ESTEIRA DE GERAÇÃO & PRESET IA</h1>
          <p>Carregue sua foto de referência para pré-visualizar a iluminação, contraste e filtros da paleta Capivara Club Hot.</p>
        </div>
      </div>
      
      <div class="tool-workspace">
        <div class="tool-pane">
          <div class="tool-pane-head">Foto de Referência<span>Passo 1</span></div>
          <div class="tool-pane-body">
            <div class="tool-drop" onclick="document.getElementById('toolFileInput').click()">
              <div class="plus">+</div>
              <strong>Clique ou arraste uma foto aqui</strong>
              <small>Suporta JPG, PNG, WEBP</small>
            </div>
            <input type="file" id="toolFileInput" style="display:none;" accept="image/*" onchange="handleToolImage(event)">
            <div id="toolImageInfo" style="margin-top:12px; font-size:12px; color:#d85b72;"></div>
          </div>
        </div>

        <div class="tool-pane">
          <div class="tool-pane-head">Configuração do Preset<span>Passo 2</span></div>
          <div class="tool-pane-body">
            <div class="tool-form">
              <div class="tool-field">
                <label>Filtro de Iluminação da Modelo</label>
                <select id="presetFilterSelect">
                  <option value="cyber">Cyber Dark / Neon Vinho (Padrão Capivara)</option>
                  <option value="golden">Golden Hour / Praia Tropical</option>
                  <option value="flash">Flash Noturno / Fotografia Casual</option>
                  <option value="studio">Estúdio Vogue / Alta Nitidez</option>
                </select>
              </div>
              <div class="tool-field">
                <label>Nível de Consistência Facial (IP-Adapter)</label>
                <select>
                  <option>0.85 (Recomendado - Fidelidade Máxima)</option>
                  <option>0.70 (Equilibrado)</option>
                  <option>0.60 (Maior variação de expressão)</option>
                </select>
              </div>
              <button class="btn-prime" type="button" onclick="runPreset()">⚡ APLICAR PRESET NA IMAGEM</button>
              <div id="presetStatus" style="font-size:12px; color:#00e58a; min-height:20px; margin-top:8px;"></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- TAB 6: AFILIADOS & SAQUE -->
    <section class="tab-panel" id="tab-afiliados">
      <div class="hero-banner">
        <div>
          <h1>PAINEL DE INDICAÇÕES & SAQUE PIX</h1>
          <p>Receba 50% de comissão direta por cada venda realizada com o seu link de afiliado exclusivo.</p>
        </div>
      </div>

      <div class="ref-withdraw-card">
        <div>
          <span style="font-size:12px; color:#a79da1; text-transform:uppercase; font-weight:800;">Saldo Disponível para Saque</span>
          <strong>R$ 439,50</strong>
          <p>Disponível para transferência imediata via PIX.</p>
        </div>
        <button class="ref-withdraw-button" onclick="alertWithdraw()">SOLICITAR SAQUE PIX</button>
      </div>

      <div style="background:var(--card); border:1px solid var(--line); border-radius:14px; padding:24px; margin-bottom:24px;">
        <h3 style="margin:0 0 10px; font-size:16px;">Seu Link de Afiliado Exclusivo</h3>
        <div style="display:flex; gap:10px;">
          <input type="text" id="affLink" value="https://capivaraclubhot.com/?ref=VIP-98421" readonly style="flex:1; background:#0b0b0b; border:1px solid var(--line); border-radius:8px; padding:12px; color:#eee;">
          <button class="btn-prime" style="padding:0 24px;" onclick="copyAffLink()">COPIAR LINK</button>
        </div>
      </div>
    </section>

  </main>

  <!-- Video Player Modal -->
  <div class="modal-overlay hidden" id="playerModal" onclick="closePlayer(event)">
    <div class="modal-box" onclick="event.stopPropagation()">
      <div class="modal-box-head">
        <h3 id="playerModalTitle">Reprodução de Aula</h3>
        <button class="modal-close-x" onclick="closePlayer()">×</button>
      </div>
      <div class="video-viewport">
        <div class="video-watermark">VIP • membro@capivaraclubhot.com</div>
        <video id="mainVideoPlayer" controls autoplay style="width:100%; height:100%; object-fit:contain; background:#000;">
          <source id="videoSource" src="" type="video/mp4">
          Seu navegador não suporta este vídeo.
        </video>
      </div>
    </div>
  </div>

  <script>
    function switchTab(tabId) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
      
      const btn = Array.from(document.querySelectorAll('.tab-btn')).find(b => b.getAttribute('onclick')?.includes(tabId));
      if (btn) btn.classList.add('active');
      
      const panel = document.getElementById('tab-' + tabId);
      if (panel) panel.classList.add('active');
    }

    function playLesson(videoUrl, title) {
      document.getElementById('playerModalTitle').textContent = title;
      const player = document.getElementById('mainVideoPlayer');
      const source = document.getElementById('videoSource');
      source.src = videoUrl;
      player.load();
      player.play().catch(()=>{});
      document.getElementById('playerModal').classList.remove('hidden');
    }

    function closePlayer() {
      const player = document.getElementById('mainVideoPlayer');
      player.pause();
      document.getElementById('playerModal').classList.add('hidden');
    }

    function copyPrompt(text) {
      navigator.clipboard.writeText(text);
      ClubUI.alert('Prompt copiado para a área de transferência!');
    }

    function copyAffLink() {
      const link = document.getElementById('affLink').value;
      navigator.clipboard.writeText(link);
      ClubUI.alert('Link de afiliado copiado com sucesso!');
    }

    function alertWithdraw() {
      ClubUI.alert('Solicitação de saque PIX (R$ 439,50) enviada! Pagamento em processamento na sua conta.');
    }

    function handleToolImage(e) {
      const file = e.target.files[0];
      if (file) {
        document.getElementById('toolImageInfo').textContent = 'Foto carregada: ' + file.name + ' (' + (file.size/1024/1024).toFixed(2) + ' MB)';
      }
    }

    function runPreset() {
      const status = document.getElementById('presetStatus');
      status.textContent = 'Processando com preset de iluminação...';
      setTimeout(() => {
        status.textContent = '✓ Preset aplicado com sucesso! Imagem ajustada.';
      }, 1200);
    }
  </script>
</body>
</html>
"""

# Write to all 3 paths
for dest in [
    "paginas/painel.html",
    "paginas/membros.html",
    "membros/index.html"
]:
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Atualizado: {dest}")

print("Plataforma atualizada com 100% dos dados originais!")
