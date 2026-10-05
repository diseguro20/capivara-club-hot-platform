import re

with open("index_source.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace root-relative paths with relative paths
html = html.replace('href="/assets/', 'href="assets/')
html = html.replace('src="/assets/', 'src="assets/')
html = html.replace('src="/icons/', 'src="icons/')
html = html.replace('href="/icons/', 'href="icons/')
html = html.replace('href="/manifest.json"', 'href="manifest.json"')

# Replace cloudflare beacon and analytics with local/no-op
html = re.sub(r'<script type="module" src="https://static.cloudflareinsights.com/[^>]+></script>', '', html)

# Fix script site_editavel-1.js to allow offline PIX generation simulation if backend is not reachable
offline_enhancement = """
<script>
// Mock offline PIX responder if fetch to /api/access-request fails
const _origFetch = window.fetch;
window.fetch = async (input, init = {}) => {
  try {
    const res = await _origFetch(input, init);
    if (res.ok) return res;
    throw new Error('Fallback to local offline simulation');
  } catch(e) {
    const url = typeof input === 'string' ? input : input.url;
    if (url.includes('/api/check-nickname')) {
      return new Response(JSON.stringify({available: true}), {status: 200, headers: {'Content-Type': 'application/json'}});
    }
    if (url.includes('/api/access-request')) {
      const mockPixCode = "00020126580014br.gov.bcb.pix0136capivaraclubhot@pagamento.com520400005303986540587.905802BR5917CAPIVARA CLUB HOT6009SAO PAULO62070503***6304E8A2";
      return new Response(JSON.stringify({
        idTransaction: "MOCK-" + Date.now(),
        amount: 87.90,
        paymentCode: mockPixCode,
        paymentCodeBase64: "imagens/app-icon-512.png"
      }), {status: 200, headers: {'Content-Type': 'application/json'}});
    }
    if (url.includes('/api/order-status')) {
      return new Response(JSON.stringify({status: 'pending'}), {status: 200, headers: {'Content-Type': 'application/json'}});
    }
    return _origFetch(input, init);
  }
};
</script>
"""

# Insert before closing body
html = html.replace('</body>', offline_enhancement + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html criado com sucesso com compatibilidade 100% offline!")
