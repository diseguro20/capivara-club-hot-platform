import urllib.request, http.cookiejar, json, re, os
from concurrent.futures import ThreadPoolExecutor

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

dest_dir = "member-assets/prompts-18"
os.makedirs(dest_dir, exist_ok=True)

def download_prompt_image(item):
    idx, p = item
    raw_path = p.get('imagem_arquivo', '')
    fname = raw_path.split('/')[-1] if '/' in raw_path else raw_path
    if not fname:
        fname = f"{idx+1:03d}.jpg"
    out_path = os.path.join(dest_dir, fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return idx, fname, True, "cached"
    url = f"https://capivaraclubhot.com/member-assets/prompts-18/{fname}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
    try:
        with opener.open(req, timeout=12) as res:
            data = res.read()
            with open(out_path, "wb") as f:
                f.write(data)
            return idx, fname, True, len(data)
    except Exception as e:
        return idx, fname, False, str(e)

print(f"Starting bulk download of all {len(prompts)} prompt 18 images with correct extensions...")
with ThreadPoolExecutor(max_workers=16) as ex:
    results = list(ex.map(download_prompt_image, enumerate(prompts)))

successes = [r for r in results if r[2]]
failures = [r for r in results if not r[2]]
print(f"Finished: {len(successes)} successful, {len(failures)} failed.")
if failures:
    print(f"Sample failures: {failures[:5]}")
