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

test_indices = [1, 2, 3, 4, 5, 6]
exts = ['jpeg', 'jpg', 'png', 'webp']

for idx in test_indices:
    print(f"=== Testing Prompt {idx} Gallery Images ===")
    for suffix in ['1', '2']:
        for ext in exts:
            candidates = [
                f"https://capivaraclubhot.com/member-assets/gallery/{idx}-{suffix}.{ext}",
                f"https://capivaraclubhot.com/member-assets/gallery/{idx}_{suffix}.{ext}",
                f"https://capivaraclubhot.com/member-assets/gallery/{idx}.{ext}",
                f"https://capivaraclubhot.com/member-assets/gallery/prompt-{idx}-{suffix}.{ext}",
            ]
            for url in candidates:
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'}, method='HEAD')
                    with opener.open(req, timeout=3) as res:
                        print(f"  FOUND: {url} -> {res.status}, size {res.headers.get('Content-Length')}")
                except Exception:
                    pass
