import urllib.request
from concurrent.futures import ThreadPoolExecutor

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0'}

def check(path):
    url = base_url + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as res:
            if res.status == 200:
                print(f"[FOUND 200] {path} - length: {len(res.read())}", flush=True)
    except:
        pass

targets = []
# fotos-carrossel
for i in range(1, 10):
    for ext in ['jpeg', 'jpg', 'png', 'webp', 'mp4']:
        targets.append(f"/fotos-carrossel/foto-{i}.{ext}")
        targets.append(f"/fotos-carrossel/foto{i}.{ext}")

# common files
targets.extend([
    "/favicon.ico",
    "/logo.png",
    "/assets/logo.png",
    "/assets/capivara.png",
    "/assets/bg.jpg",
    "/assets/bg.png",
    "/manifest.json",
    "/manifest-admin.json",
])

with ThreadPoolExecutor(max_workers=8) as ex:
    ex.map(check, targets)
