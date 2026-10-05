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

dest_dir = "member-assets/prompts-18"
os.makedirs(dest_dir, exist_ok=True)

def download_img(i):
    fname = f"{i:03d}.jpg"
    out_path = os.path.join(dest_dir, fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return i, True, "cached"
    url = f"https://capivaraclubhot.com/member-assets/prompts-18/{fname}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
    try:
        with opener.open(req, timeout=8) as res:
            data = res.read()
            with open(out_path, "wb") as f:
                f.write(data)
            return i, True, len(data)
    except Exception as e:
        return i, False, str(e)

print("Starting bulk download of all 562 prompt images...")
with ThreadPoolExecutor(max_workers=12) as ex:
    results = list(ex.map(download_img, range(1, 563)))

successes = [r for r in results if r[1]]
print(f"Completed! Total available on server: {len(successes)} / 562 images.")
