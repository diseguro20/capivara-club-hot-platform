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

with open('member-assets/member_prompts_18.json', 'r', encoding='utf-8') as f:
    prompts = json.load(f)

test_indices = [0, 10, 39, 40, 41, 50, 100, 200, 500]
for idx in test_indices:
    p = prompts[idx]
    uuid_file = p.get('imagem_url')
    num_file = p.get('imagem_arquivo').split('/')[-1]
    print(f"=== Testing Prompt {idx+1}: {num_file} / {uuid_file} ===")
    patterns = [
        f"https://capivaraclubhot.com/member-assets/prompts-18/{num_file}",
        f"https://capivaraclubhot.com/member-assets/prompts-18/{uuid_file}",
        f"https://capivaraclubhot.com/storage/{uuid_file}",
        f"https://capivaraclubhot.com/storage/prompts/{uuid_file}",
        f"https://capivaraclubhot.com/storage/prompts-18/{num_file}",
        f"https://capivaraclubhot.com/storage/prompts-18/{uuid_file}",
        f"https://capivaraclubhot.com/imagens/{num_file}",
        f"https://capivaraclubhot.com/imagens/{uuid_file}",
        f"https://capivaraclubhot.com/images/{uuid_file}",
        f"https://capivaraclubhot.com/uploads/{uuid_file}",
        f"https://capivaraclubhot.com/member-assets/gallery/{uuid_file}",
        f"https://capivaraclubhot.com/member-assets/prompts/{uuid_file}",
    ]
    found = False
    for url in patterns:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
            with opener.open(req, timeout=5) as res:
                content = res.read()
                print(f"  FOUND: {url} -> status {res.status}, len {len(content)}, type: {res.headers.get('Content-Type')}")
                found = True
                break
        except Exception as e:
            pass
    if not found:
        print(f"  NOT FOUND for {idx+1}")
