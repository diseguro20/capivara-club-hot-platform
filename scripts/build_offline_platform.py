import os, re, json

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

def build():
    # 1. Ensure prompt data JS files exist
    p18_json = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts_18.json')
    p18_js = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts_18.js')
    if os.path.exists(p18_json):
        with open(p18_json, 'r', encoding='utf-8') as f:
            data_18 = json.load(f)
        with open(p18_js, 'w', encoding='utf-8') as f:
            f.write('window.DMCN_PROMPTS_18 = ' + json.dumps(data_18, ensure_ascii=False) + ';\n')
        print(f"Verified/Generated {p18_js} ({len(data_18)} items)")

    p_json = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts.json')
    p_js = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts.js')
    if os.path.exists(p_json):
        with open(p_json, 'r', encoding='utf-8') as f:
            data_p = json.load(f)
        with open(p_js, 'w', encoding='utf-8') as f:
            f.write('window.DMCN_PROMPTS = ' + json.dumps(data_p.get('prompts', []), ensure_ascii=False) + ';\n')
        print(f"Verified/Generated {p_js} ({len(data_p.get('prompts', []))} items)")

    # 2. Build unlocked HTML from scripts/membros_autenticado.html
    auth_html_path = os.path.join(ROOT_DIR, 'scripts', 'membros_autenticado.html')
    with open(auth_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Permanently hide login screen and force password screen
    html = html.replace('<section class="login-screen" id="loginScreen">',
                        '<section class="login-screen hidden" id="loginScreen" style="display: none !important;">')
    html = html.replace('<section class="login-screen hidden" id="forcePasswordScreen">',
                        '<section class="login-screen hidden" id="forcePasswordScreen" style="display: none !important;">')

    # Ensure app is directly visible
    html = html.replace('<section class="app hidden" id="app">',
                        '<section class="app" id="app" style="display: block !important;">')

    # Unlock all workflows
    html = html.replace('workflow-locked', '')
    html = html.replace('data-workflow-locked="true"', 'data-workflow-locked="false"')

    # Inject pre-filled member info and activate tutorial videos
    for i in range(1, 10):
        num_str = f"{i:02d}"
        video_tag = f'<video class="tutorial-video" controls preload="metadata" src="/videos-tutoriais/tutorial-{num_str}.mp4" style="display: block !important; width: 100%; border-radius: 8px;"></video>'
        pattern = rf'(<span class="tutorial-num">{num_str}</span>[\s\S]*?<div class="video-box">)[\s\S]*?(<div class="video-empty">)'
        replacement = rf'\1\n              {video_tag}\n              <div class="video-empty" style="display: none !important;">'
        html = re.sub(pattern, replacement, html)

    # Inject real-time sync banner right below hero in Inicio
    sync_banner_html = """
        <!-- REAL-TIME CLOUD SYNC BANNER -->
        <div class="sync-banner" id="realtimeSyncBanner">
          <div class="sync-banner-info">
            <div class="sync-badge"><span class="sync-dot"></span> SINCRONIZAÇÃO EM TEMPO REAL ATIVA</div>
            <h3>CONEXÃO DIRETA COM CAPIVARA CLUB HOT</h3>
            <p id="syncStatusSummary">Sincronizador automático monitorando novos vídeos, workflows e prompts da sua conta.</p>
            <div class="sync-metrics-grid">
              <div class="sync-metric-item"><strong id="metricVideos">9</strong> <span>Vídeos</span></div>
              <div class="sync-metric-item"><strong id="metricWorkflows">16</strong> <span>Workflows</span></div>
              <div class="sync-metric-item"><strong id="metricPrompts">194</strong> <span>Prompts</span></div>
              <div class="sync-metric-item"><strong id="metricPrompts18">562</strong> <span>Prompts +18</span></div>
            </div>
          </div>
          <div class="sync-banner-actions">
            <button type="button" class="sync-btn" id="btnTriggerSync">
              <span class="sync-icon">🔄</span> <span id="syncBtnLabel">Sincronizar Tudo Agora</span>
            </button>
            <small id="syncLastTime">Última checagem: verificando...</small>
            <div id="syncFeedbackMsg" class="sync-feedback hidden"></div>
          </div>
        </div>
    """

    hero_pattern = r'(<div class="hero">[\s\S]*?</div>\s*</div>)'
    if re.search(hero_pattern, html):
        html = re.sub(hero_pattern, r'\1\n' + sync_banner_html, html, count=1)
    else:
        # Fallback before section-head
        html = html.replace('<div class="section-head">', sync_banner_html + '\n<div class="section-head">')

    # Inject prompt data scripts before area_membros_esteira_interna_ferramentas-1.js
    scripts_to_inject = """<script src="/assets/firebase-auth.js"></script>
<script src="/member-assets/member_prompts.js?v=20261005"></script>
<script src="/member-assets/member_prompts_18.js?v=20261005"></script>
<script src="/member-scripts/area_membros_esteira_interna_ferramentas-1.js?v=20261005-prompts18-fixed"></script>
<script>
// Smart video fallback for cloud deployments (Vercel)
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tutorial-video').forEach((v, idx) => {
    v.addEventListener('error', () => {
      const num = (idx + 1).toString().padStart(2, '0');
      const remote = `https://capivaraclubhot.com/videos-tutoriais/tutorial-${num}.mp4`;
      if (v.src !== remote) {
        console.log(`Fallback de vídeo ativado para tutorial ${num}`);
        v.src = remote;
        v.load();
      }
    });
  });

  // Logout handler
  const logoutBtn = document.getElementById('logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (window.capivaraAuth) window.capivaraAuth.signOut();
      localStorage.removeItem('memberEmail');
      localStorage.removeItem('memberName');
      localStorage.removeItem('capivara_user');
      window.location.href = '/login.html';
    });
  }
});

(function initRealTimeSync() {
  const btn = document.getElementById('btnTriggerSync');
  const label = document.getElementById('syncBtnLabel');
  const summary = document.getElementById('syncStatusSummary');
  const lastTime = document.getElementById('syncLastTime');
  const feedback = document.getElementById('syncFeedbackMsg');
  const metricVideos = document.getElementById('metricVideos');
  const metricWorkflows = document.getElementById('metricWorkflows');
  const metricPrompts = document.getElementById('metricPrompts');
  const metricPrompts18 = document.getElementById('metricPrompts18');

  async function checkSyncStatus() {
    try {
      const res = await fetch('/api/sync/status');
      if (!res.ok) return;
      const data = await res.json();
      if (data.metrics) {
        if (metricVideos) metricVideos.textContent = data.metrics.tutorial_videos;
        if (metricWorkflows) metricWorkflows.textContent = data.metrics.workflows;
        if (metricPrompts) metricPrompts.textContent = data.metrics.prompts;
        if (metricPrompts18) metricPrompts18.textContent = data.metrics.prompts_18;
      }
      if (lastTime && data.last_sync) {
        lastTime.textContent = 'Última sincronização: ' + data.last_sync;
      }
      if (summary && data.message) {
        summary.textContent = data.message;
      }
      if (btn && data.is_syncing) {
        btn.classList.add('loading');
        if (label) label.textContent = 'Sincronizando com original...';
        btn.disabled = true;
      } else if (btn && !data.is_syncing && btn.classList.contains('loading')) {
        btn.classList.remove('loading');
        if (label) label.textContent = 'Sincronizar Tudo Agora';
        btn.disabled = false;
        if (feedback) {
          feedback.textContent = '✅ Sincronizado!';
          feedback.classList.remove('hidden');
          setTimeout(() => feedback.classList.add('hidden'), 5000);
        }
      }
    } catch(e) {}
  }

  if (btn) {
    btn.addEventListener('click', async () => {
      btn.classList.add('loading');
      if (label) label.textContent = 'Iniciando sincronização...';
      btn.disabled = true;
      try {
        await fetch('/api/sync/trigger', { method: 'POST' });
        let attempts = 0;
        const poll = setInterval(async () => {
          attempts++;
          const res = await fetch('/api/sync/status');
          const data = await res.json();
          if (!data.is_syncing || attempts > 60) {
            clearInterval(poll);
            await checkSyncStatus();
            if (feedback) {
              feedback.textContent = '✅ Sincronização concluída com sucesso!';
              feedback.classList.remove('hidden');
              setTimeout(() => feedback.classList.add('hidden'), 6000);
            }
          }
        }, 1500);
      } catch(e) {
        btn.classList.remove('loading');
        if (label) label.textContent = 'Sincronizar Tudo Agora';
        btn.disabled = false;
      }
    });
  }

  checkSyncStatus();
  setInterval(checkSyncStatus, 20000);
})();
</script>"""

    html = re.sub(
        r'<script\s+src="[^"]*area_membros_esteira_interna_ferramentas-1\.js[^"]*"></script>',
        scripts_to_inject,
        html
    )

    # Inject default localStorage bootstrap script and styles right before </head>
    bootstrap_script = """
<script>
  try {
    localStorage.setItem('memberEmail', 'diseguro20@gmail.com');
    localStorage.setItem('memberName', 'Diego');
    localStorage.setItem('memberIsAdmin', '0');
  } catch(e) {}
</script>
<style>
  #loginScreen, #forcePasswordScreen { display: none !important; }
  #app { display: block !important; }
  .video-empty { display: none !important; }
  .tutorial-video { display: block !important; }
  .video-security-watermark { display: none !important; opacity: 0 !important; visibility: hidden !important; pointer-events: none !important; width: 0 !important; height: 0 !important; }
  .workflow-locked { filter: none !important; opacity: 1 !important; pointer-events: auto !important; }
  .workflow-locked .tag { background: rgba(0, 240, 255, 0.2) !important; color: #00f0ff !important; }
  .workflow-locked a.copy { pointer-events: auto !important; opacity: 1 !important; display: inline-block !important; }
  .gallery-card { cursor: pointer; transition: transform 0.15s ease, box-shadow 0.15s ease; }
  .gallery-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4); }
  [data-content="galeria-18"] .gallery-copy,
  [data-content="galeria"] .gallery-copy {
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
    width: 100%;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 800;
    cursor: pointer;
    background: #2a0712 !important;
    border: 1px solid rgba(152, 29, 56, 0.65) !important;
    color: #f4e9ed !important;
    transition: all 0.2s ease;
  }
  [data-content="galeria-18"] .gallery-copy:hover,
  [data-content="galeria"] .gallery-copy:hover {
    background: #3a0918 !important;
    border-color: #b52b4e !important;
  }
  [data-content="galeria-18"] .gallery-copy.copied,
  [data-content="galeria"] .gallery-copy.copied {
    background: #173326 !important;
    border-color: #2d9364 !important;
    color: #d9ffeb !important;
  }

  /* Sync Banner Styling */
  .sync-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
    background: linear-gradient(135deg, rgba(13, 20, 36, 0.95), rgba(26, 16, 45, 0.95));
    border: 1px solid rgba(0, 240, 255, 0.35);
    border-radius: 14px;
    padding: 20px 24px;
    margin: 20px 0 28px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    position: relative;
    overflow: hidden;
  }
  .sync-banner::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #00f0ff, #ec4899);
  }
  .sync-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 4px 10px;
    background: rgba(0, 240, 255, 0.12);
    border: 1px solid rgba(0, 240, 255, 0.3);
    border-radius: 20px;
    font-size: 11px;
    font-weight: 800;
    color: #00f0ff;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
  }
  .sync-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #00f0ff;
    box-shadow: 0 0 10px #00f0ff;
    animation: syncPulse 2s infinite;
  }
  @keyframes syncPulse {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 240, 255, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(0, 240, 255, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 240, 255, 0); }
  }
  .sync-banner h3 {
    margin: 0 0 6px;
    font-size: 18px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.5px;
  }
  .sync-banner p {
    margin: 0 0 14px;
    font-size: 13px;
    color: #94a3b8;
  }
  .sync-metrics-grid {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
  }
  .sync-metric-item {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 14px;
    border-radius: 8px;
    display: flex;
    align-items: baseline;
    gap: 6px;
  }
  .sync-metric-item strong {
    font-size: 16px;
    font-weight: 800;
    color: #38bdf8;
  }
  .sync-metric-item span {
    font-size: 11px;
    color: #94a3b8;
    text-transform: uppercase;
    font-weight: 600;
  }
  .sync-banner-actions {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
    min-width: 220px;
  }
  .sync-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: linear-gradient(135deg, #0284c7, #0369a1);
    border: 1px solid rgba(56, 189, 248, 0.5);
    color: #ffffff;
    padding: 12px 20px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 14px rgba(2, 132, 199, 0.35);
    transition: all 0.2s ease;
    width: 100%;
  }
  .sync-btn:hover {
    background: linear-gradient(135deg, #0369a1, #075985);
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(2, 132, 199, 0.5);
  }
  .sync-btn.loading {
    opacity: 0.85;
    cursor: wait;
  }
  .sync-btn.loading .sync-icon {
    display: inline-block;
    animation: syncSpin 1s linear infinite;
  }
  @keyframes syncSpin {
    100% { transform: rotate(360deg); }
  }
  .sync-banner-actions small {
    font-size: 11px;
    color: #64748b;
  }
  .sync-feedback {
    font-size: 11px;
    padding: 6px 10px;
    border-radius: 6px;
    background: rgba(34, 197, 94, 0.15);
    border: 1px solid rgba(34, 197, 94, 0.3);
    color: #4ade80;
    text-align: center;
    width: 100%;
  }
</style>
"""
    html = html.replace('</head>', bootstrap_script + '\n</head>')

    # Output to painel.html and membros.html (index.html is the landing page)
    targets = [
        os.path.join(ROOT_DIR, 'paginas', 'painel.html'),
        os.path.join(ROOT_DIR, 'paginas', 'membros.html'),
    ]

    for t in targets:
        os.makedirs(os.path.dirname(t), exist_ok=True)
        with open(t, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Generated unlocked file: {t} ({len(html)} bytes)")

    print("\nOffline platform built successfully!")

if __name__ == '__main__':
    build()
