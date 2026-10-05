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

def download_one(i):
    fname = f"{i:03d}.jpg"
    out_path = os.path.join(dest_dir, fname)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return True
    url = f"https://capivaraclubhot.com/member-assets/prompts-18/{fname}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
    try:
        with opener.open(req, timeout=10) as res:
            data = res.read()
            with open(out_path, "wb") as f:
                f.write(data)
            return True
    except:
        return False

# Download first 50 prompt images immediately for instant full offline rendering
print("Downloading first 60 prompt images...")
with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(download_one, range(1, 61)))

print(f"Downloaded {sum(results)} / 60 images successfully!")
