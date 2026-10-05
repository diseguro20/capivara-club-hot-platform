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

test_urls = [
    'https://capivaraclubhot.com/member-assets/gallery/1-1.jpeg',
    'https://capivaraclubhot.com/member-assets/gallery/1-2.jpeg',
    'https://capivaraclubhot.com/member-assets/gallery/1-1.jpg',
    'https://capivaraclubhot.com/member-assets/gallery/reference-612ea13bd304759a.jpg',
    'https://capivaraclubhot.com/member-assets/gallery/reference-d7a4d9bea14e8070.png',
]

for u in test_urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
        with opener.open(req, timeout=5) as r:
            print(f"[FOUND] {u} -> status {r.status}, size {r.headers.get('Content-Length')}", flush=True)
    except Exception as e:
        print(f"[FAIL] {u} -> {e}", flush=True)
