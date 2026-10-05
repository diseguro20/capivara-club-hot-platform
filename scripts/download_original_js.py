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

# Download fresh official area_membros_esteira_interna_ferramentas-1.js
url = "https://capivaraclubhot.com/member-scripts/area_membros_esteira_interna_ferramentas-1.js"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
with opener.open(req) as res:
    content = res.read().decode('utf-8', errors='ignore')
    with open('scripts/original_area_membros-1.js', 'w', encoding='utf-8') as f:
        f.write(content)
print(f"Downloaded official script: {len(content)} bytes")
