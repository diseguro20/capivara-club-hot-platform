import os
import re

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
source_path = os.path.join(ROOT_DIR, 'scripts', 'index_source.html')
target_path = os.path.join(ROOT_DIR, 'index.html')

with open(source_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace header with enhanced navbar
new_header = """
  <header class="site-header">
    <div class="header-nav">
      <a href="/" class="header-brand">
        <img src="/assets/embedded-4319352716121903.png" alt="Logo Capivara">
        <span>CAPIVARA CLUB HOT</span>
      </a>
      <div class="header-actions">
        <a href="#oferta" class="nav-buy-link">Garantir Acesso</a>
        <a href="/login.html" class="nav-login-btn">Área de Membros →</a>
      </div>
    </div>
  </header>
"""

html = re.sub(r'<header class="logo-area">[\s\S]*?</header>', new_header, html)

# Inject navbar styles before </head>
nav_styles = """
<style>
  .site-header {
    width: 100%;
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(5, 3, 4, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }
  .header-nav {
    max-width: 1200px;
    margin: 0 auto;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
  }
  .header-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
    color: #ffffff;
  }
  .header-brand img {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
  }
  .header-brand span {
    font-size: 14px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #f3f4f6;
  }
  .header-actions {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .nav-buy-link {
    color: #cbd5e1;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    transition: color 0.2s ease;
  }
  .nav-buy-link:hover {
    color: #00f0ff;
  }
  .nav-login-btn {
    background: linear-gradient(135deg, #0284c7, #00f0ff);
    color: #040810 !important;
    text-decoration: none;
    padding: 8px 18px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 800;
    box-shadow: 0 4px 14px rgba(0, 240, 255, 0.35);
    transition: all 0.2s ease;
  }
  .nav-login-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0, 240, 255, 0.55);
  }
  @media (max-width: 600px) {
    .header-brand span { font-size: 12px; }
    .nav-buy-link { display: none; }
  }
</style>
"""

html = html.replace('</head>', nav_styles + '\n</head>')

with open(target_path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Generated Landing Page: {target_path} ({len(html)} bytes)")
