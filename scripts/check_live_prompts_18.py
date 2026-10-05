import urllib.request, http.cookiejar, json, re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0'}

with opener.open(urllib.request.Request('https://capivaraclubhot.com/membros', headers=headers)) as res:
    html = res.read().decode('utf-8', errors='ignore')
csrf = re.search(r'name="csrf-token"\s+content="([^"]+)"', html).group(1)

opener.open(urllib.request.Request(
    'https://capivaraclubhot.com/api/login',
    data=json.dumps({'email': 'diseguro20@gmail.com', 'password': 'diego2001'}).encode('utf-8'),
    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'X-CSRF-TOKEN': csrf, 'Referer': 'https://capivaraclubhot.com/membros'}
))

# Fetch /api/member/prompts-18
url = "https://capivaraclubhot.com/api/member/prompts-18"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
with opener.open(req) as res:
    data = json.loads(res.read().decode('utf-8'))

print(f"Total live prompts from /api/member/prompts-18: {len(data)}", flush=True)
for i in range(min(5, len(data))):
    p = data[i]
    print(f"\n--- Live Prompt {i+1} ---", flush=True)
    print("ID:", p.get('id'), flush=True)
    print("Titulo:", p.get('titulo'), flush=True)
    print("Categoria:", p.get('categoria'), flush=True)
    print("Texto preview:", p.get('texto', '')[:200], flush=True)
    print("Imagem URL:", p.get('imagem_url'), flush=True)
    print("Imagem Arquivo:", p.get('imagem_arquivo'), flush=True)
