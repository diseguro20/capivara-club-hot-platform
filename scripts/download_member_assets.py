import urllib.request
import http.cookiejar
import json
import re
import os

login_url = "https://capivaraclubhot.com/api/login"
membros_url = "https://capivaraclubhot.com/membros"
base_url = "https://capivaraclubhot.com"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. Login
with opener.open(urllib.request.Request(membros_url, headers=headers)) as res:
    html = res.read().decode('utf-8', errors='ignore')
    csrf_token = re.search(r'name="csrf-token"\s+content="([^"]+)"', html).group(1)

post_headers = {
    'User-Agent': headers['User-Agent'],
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CSRF-TOKEN': csrf_token,
    'Referer': membros_url,
    'Origin': base_url
}
login_data = json.dumps({"email": "diseguro20@gmail.com", "password": "diego2001"}).encode('utf-8')
opener.open(urllib.request.Request(login_url, data=login_data, headers=post_headers, method='POST'))

# Function to download authenticated asset
def download_auth(path, local_path):
    url = base_url + path if path.startswith('/') else f"{base_url}/{path}"
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={'User-Agent': headers['User-Agent'], 'Referer': membros_url})
        with opener.open(req) as res:
            data = res.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"[OK] {path} -> {local_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"[FAIL] {path}: {e}")

# Download all member scripts
member_scripts = [
    "/member-scripts/area_membros_esteira_interna_ferramentas-1.js",
    "/member-scripts/area_membros_esteira_interna_ferramentas-2.js",
    "/member-scripts/area_membros_esteira_interna_ferramentas-3.js",
    "/member-scripts/area_membros_esteira_interna_ferramentas-4.js",
    "/member-scripts/area_membros_esteira_interna_ferramentas-5.js"
]

for s in member_scripts:
    download_auth(s, s.lstrip('/'))

# Download member gallery images
gallery_images = [
    "/member-assets/gallery/reference-612ea13bd304759a.jpg",
    "/member-assets/gallery/reference-d7a4d9bea14e8070.png",
    "/member-assets/gallery/reference-154eb973ba21e634.png",
    "/member-assets/gallery/reference-05df4d3f1d1a2e93.jpg",
    "/member-assets/gallery/reference-338312b31cd43a06.jpg",
    "/member-assets/gallery/reference-4e6aa26fa824f4c9.png",
    "/assets/reference-2514a67406bf4e79.ico",
    "/assets/reference-7583dc0e1686563e.svg",
    "/assets/reference-fb46ffc0bfdb8cc2.ico"
]

for img in gallery_images:
    download_auth(img, img.lstrip('/'))

# Download all member workflows directly from site
workflows_on_site = [
    "/workflows/faceswap-capivara-duhot.json",
    "/workflows/TROCA%20DE%20ROUPA%20-%20WF%20GRATIS.json",
    "/workflows/controlmotion-capivara-duhot.json",
    "/workflows/UPSCALE%20IMG%20-%20CAPIVARA%20%28GR%C3%81TIS%29.json",
    "/workflows/CAPIVARA%20DU%20HOT%20-%20GERAR%20V%C3%8DDEOS%20PROMPT.json",
    "/workflows/VARIOS%20ANGULOS.json",
    "/workflows/MOTION%2BCONTROL%2Bv7.json",
    "/workflows/CONTROLMOTION%202%20-%20CAPIVARA%20DUHOT%20-%20VIDEO%20%2B18.json",
    "/workflows/SWAP%20-%20FLUX%20-%20CAPIVARA.json",
    "/workflows/KREA%202%20-%20ROSTO%20%2B%20PROMPT.json"
]

for wf in workflows_on_site:
    clean_name = urllib.parse.unquote(wf.lstrip('/'))
    download_auth(wf, clean_name)

print("Finished downloading all member assets!")
