import os

# Read painel.html
with open("paginas/painel.html", "r", encoding="utf-8") as f:
    painel_content = f.read()

# 1. Update paginas/membros.html to be the unlocked panel directly
with open("paginas/membros.html", "w", encoding="utf-8") as f:
    f.write(painel_content)

print("paginas/membros.html agora e o painel 100% liberado sem tela de login!")

# 2. Create membros/index.html at root so /membros and /membros/ work directly
os.makedirs("membros", exist_ok=True)
membros_root_content = painel_content.replace('href="../', 'href="/').replace('src="../', 'src="/')
# Also handle relative paths properly
membros_root_content = painel_content.replace('../', '../') # from /membros/index.html, ../ goes to root!
with open("membros/index.html", "w", encoding="utf-8") as f:
    f.write(membros_root_content)

print("membros/index.html criado para suportar http://localhost:5500/membros diretamente!")

# 3. Also update index.html with a prominent VIP bar to jump straight to the unlocked member area
with open("index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

vip_banner = """
  <!-- Topbar de Acesso Liberado -->
  <div style="background: linear-gradient(90deg, #7a1025, #bd1c42, #7a1025); color: #fff; padding: 12px 20px; text-align: center; font-size: 14px; font-weight: 800; letter-spacing: 0.5px; position: sticky; top: 0; z-index: 9999; display: flex; align-items: center; justify-content: center; gap: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.6);">
    <span>🔓 ACESSO VIP LIBERADO: Todo o conteúdo, prompts e workflows estão desbloqueados!</span>
    <a href="paginas/painel.html" style="background: #fff; color: #7a1025; padding: 6px 16px; border-radius: 99px; text-decoration: none; font-size: 12px; font-weight: 800; transition: transform .2s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">ENTRAR NO PAINEL AGORA →</a>
  </div>
"""

if "<!-- Topbar de Acesso Liberado -->" not in index_html:
    index_html = index_html.replace('<body>', '<body>\n' + vip_banner)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Barra VIP adicionada ao index.html!")
