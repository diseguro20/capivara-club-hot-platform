import os
import shutil

# 1. Map videos to videos-tutoriais/
os.makedirs("videos-tutoriais", exist_ok=True)
for i in range(1, 8):
    src = f"videos/PARTE {i}.mp4"
    dst = f"videos-tutoriais/tutorial-{i}.mp4"
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"Mapped {src} -> {dst}")

# 2. Map all workflows in workflows/
workflows_list = [
    "faceswap-capivara-duhot.json",
    "TROCA DE ROUPA - WF GRATIS.json",
    "controlmotion-capivara-duhot.json",
    "UPSCALE IMG - CAPIVARA (GRÁTIS).json",
    "CAPIVARA DU HOT - GERAR VÍDEOS PROMPT.json",
    "VARIOS ANGULOS.json",
    "MOTION+CONTROL+v7.json",
    "CONTROLMOTION 2 - CAPIVARA DUHOT - VIDEO +18.json",
    "SWAP - FLUX - CAPIVARA.json",
    "KREA 2 - ROSTO + PROMPT.json"
]

print("Verifying workflows...")
for wf in workflows_list:
    p = os.path.join("workflows", wf)
    print(f"  {wf}: exists={os.path.exists(p)} ({os.path.getsize(p) if os.path.exists(p) else 0} bytes)")

# 3. Read authenticated HTML
with open("scripts/membros_autenticado.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix asset paths to relative paths
html = html.replace('href="/assets/', 'href="../assets/')
html = html.replace('src="/assets/', 'src="../assets/')
html = html.replace('href="/member-assets/', 'href="../member-assets/')
html = html.replace('src="/member-assets/', 'src="../member-assets/')
html = html.replace('src="/member-scripts/', 'src="../member-scripts/')
html = html.replace('src="/icons/', 'src="../icons/')
html = html.replace('href="/icons/', 'href="../icons/')
html = html.replace('href="/manifest.json"', 'href="../manifest.json"')
html = html.replace('href="workflows/', 'href="../workflows/')

# Preload JSON data inline so prompts and prompts-18 load instantly without any network delay!
with open("member-assets/member_prompts.json", "r", encoding="utf-8") as f:
    prompts_data = f.read()

with open("member-assets/member_prompts_18.json", "r", encoding="utf-8") as f:
    prompts_18_data = f.read()

offline_api_mock = f"""
<script>
window.__OFFLINE_PROMPTS = {prompts_data};
window.__OFFLINE_PROMPTS_18 = {prompts_18_data};

const _origFetch = window.fetch;
window.fetch = async (input, init = {{}}) => {{
  const url = typeof input === 'string' ? input : input.url;
  
  if (url.includes('/api/session')) {{
    return new Response(JSON.stringify({{
      name: "segd",
      email: "diseguro20@gmail.com",
      isAdmin: false,
      paidAt: "2026-10-05T04:25:48.000000Z",
      tutorialUnlockAt: "2026-10-02T04:35:30.000000Z",
      workflowUnlockAt: "2026-10-02T04:35:30.000000Z",
      mustChangePassword: false
    }}), {{status: 200, headers: {{'Content-Type': 'application/json'}}}});
  }}

  if (url.includes('/api/member/prompts-18')) {{
    return new Response(JSON.stringify(window.__OFFLINE_PROMPTS_18), {{status: 200, headers: {{'Content-Type': 'application/json'}}}});
  }}

  if (url.includes('/api/member/prompts')) {{
    return new Response(JSON.stringify(window.__OFFLINE_PROMPTS), {{status: 200, headers: {{'Content-Type': 'application/json'}}}});
  }}

  if (url.includes('/api/referrals')) {{
    return new Response(JSON.stringify({{balance: 439.50, referrals: []}}), {{status: 200, headers: {{'Content-Type': 'application/json'}}}});
  }}

  try {{
    return await _origFetch(input, init);
  }} catch(e) {{
    return new Response(JSON.stringify({{}}), {{status: 200}});
  }}
}};

// Auto-enter app immediately and show the member platform
document.addEventListener('DOMContentLoaded', () => {{
  const loginScreen = document.getElementById('loginScreen');
  const forcePasswordScreen = document.getElementById('forcePasswordScreen');
  const app = document.getElementById('app');
  if (loginScreen) loginScreen.classList.add('hidden');
  if (forcePasswordScreen) forcePasswordScreen.classList.add('hidden');
  if (app) app.classList.remove('hidden');

  setTimeout(() => {{
    if (typeof enterApp === 'function') {{
      enterApp("segd", "diseguro20@gmail.com", false, "2026-10-02T04:35:30.000000Z", "2026-10-02T04:35:30.000000Z");
    }}
  }}, 50);
}});
</script>
"""

# Inject offline API mock before </body>
html = html.replace('</body>', offline_api_mock + '\n</body>')

# Write to paginas/painel.html, paginas/membros.html
with open("paginas/painel.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated paginas/painel.html with authentic member HTML!")

with open("paginas/membros.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Updated paginas/membros.html with authentic member HTML!")

# For membros/index.html (at root /membros/), fix relative paths from /membros/ to root
membros_root_html = html.replace('../', '../')
with open("membros/index.html", "w", encoding="utf-8") as f:
    f.write(membros_root_html)
print("Updated membros/index.html with authentic member HTML!")
