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

# Test download of first 5 prompt images
with open('member-assets/member_prompts_18.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

print(f"Total prompt items to download: {len(items)}")
for i, item in enumerate(items[:5]):
    img_name = item.get('imagem_url')
    if img_name:
        url = f"https://capivaraclubhot.com/member-assets/prompts-18/{img_name}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
            with opener.open(req) as res:
                data = res.read()
                print(f"[{i+1}/5] OK: {img_name} ({len(data)} bytes)")
        except Exception as e:
            print(f"[{i+1}/5] Error {img_name}: {e}")
