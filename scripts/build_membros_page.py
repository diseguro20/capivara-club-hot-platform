import re

with open(r"C:\Users\diseg\.gemini\antigravity\brain\a4f0c672-f1e2-4549-a931-e73e7baafe31\.system_generated\steps\10\content.md", "r", encoding="utf-8") as f:
    raw = f.read()

# remove header before <!DOCTYPE html>
idx = raw.find("<!DOCTYPE html>")
if idx != -1:
    html = raw[idx:]
else:
    html = raw

# Fix paths to relative
html = html.replace('href="/assets/', 'href="../assets/')
html = html.replace('src="/assets/', 'src="../assets/')
html = html.replace('href="/icons/', 'href="../icons/')
html = html.replace('src="/icons/', 'src="../icons/')
html = html.replace('href="/manifest.json"', 'href="../manifest.json"')

# Clean out cloudflare scripts
html = re.sub(r'<script type="module" src="https://static.cloudflareinsights.com/[^>]+></script>', '', html)

# Mock login handler for local offline testing
mock_script = """
<script>
// Local offline handler
window.fetch = async (input, init = {}) => {
  const url = typeof input === 'string' ? input : input.url;
  if (url.includes('/api/login')) {
    localStorage.setItem('capivara_user', JSON.stringify({email: 'membro@capivaraclubhot.com', name: 'Membro VIP'}));
    window.location.href = 'painel.html';
    return new Response(JSON.stringify({success: true}), {status: 200, headers: {'Content-Type': 'application/json'}});
  }
  if (url.includes('/api/resend-password')) {
    return new Response(JSON.stringify({success: true}), {status: 200, headers: {'Content-Type': 'application/json'}});
  }
  return new Response(JSON.stringify({}), {status: 200});
};
</script>
"""

html = html.replace('</body>', mock_script + '\n</body>')

import os
os.makedirs("paginas", exist_ok=True)
with open("paginas/membros.html", "w", encoding="utf-8") as f:
    f.write(html)

print("paginas/membros.html criado com sucesso!")
