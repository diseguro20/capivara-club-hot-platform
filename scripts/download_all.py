import urllib.request
import os
from PIL import Image

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download(url_path, local_path):
    url = base_url + url_path if url_path.startswith('/') else f"{base_url}/{url_path}"
    dir_name = os.path.dirname(local_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            data = res.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {url_path} -> {local_path} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"Error downloading {url_path}: {e}")
        return False

# Download all assets
items = [
    # Carrossel images
    ("fotos-carrossel/foto-1.jpeg", "fotos-carrossel/foto-1.jpeg"),
    ("fotos-carrossel/foto-2.jpeg", "fotos-carrossel/foto-2.jpeg"),
    ("fotos-carrossel/foto-3.png", "fotos-carrossel/foto-3.png"),
    ("fotos-carrossel/foto-4.png", "fotos-carrossel/foto-4.png"),
    ("fotos-carrossel/foto-5.jpeg", "fotos-carrossel/foto-5.jpeg"),
    ("fotos-carrossel/foto-6.png", "fotos-carrossel/foto-6.png"),
    # Logo & Icons
    ("assets/embedded-4319352716121903.png", "assets/embedded-4319352716121903.png"),
    ("icons/favicon-32.png", "icons/favicon-32.png"),
    ("icons/apple-touch-icon.png", "icons/apple-touch-icon.png"),
    ("icons/icon-192.png", "icons/icon-192.png"),
    ("icons/icon-512.png", "icons/icon-512.png"),
    # CSS
    ("assets/ui.css", "assets/ui.css"),
    ("assets/site_editavel-1.css", "assets/site_editavel-1.css"),
    ("assets/area_membros_esteira_interna_ferramentas-1.css", "assets/area_membros_esteira_interna_ferramentas-1.css"),
    ("assets/area_membros_esteira_interna_ferramentas-2.css", "assets/area_membros_esteira_interna_ferramentas-2.css"),
    ("assets/area_membros_esteira_interna_ferramentas-3.css", "assets/area_membros_esteira_interna_ferramentas-3.css"),
    ("assets/area_membros_esteira_interna_ferramentas-4.css", "assets/area_membros_esteira_interna_ferramentas-4.css"),
    ("assets/area_membros_esteira_interna_ferramentas-5.css", "assets/area_membros_esteira_interna_ferramentas-5.css"),
    # JS
    ("assets/ui.js", "assets/ui.js"),
    ("assets/http.js", "assets/http.js"),
    ("assets/analytics.js", "assets/analytics.js"),
    ("assets/site_editavel-1.js", "assets/site_editavel-1.js"),
    ("assets/site_editavel-2.js", "assets/site_editavel-2.js"),
    ("assets/login.js", "assets/login.js"),
    ("sw.js", "sw.js"),
    # Manifests
    ("manifest.json", "manifest.json"),
    ("manifest-admin.json", "manifest-admin.json"),
    ("robots.txt", "robots.txt"),
]

for url_p, local_p in items:
    download(url_p, local_p)

# Populate ./imagens/ folder with both original and .webp format
os.makedirs("imagens", exist_ok=True)

image_mapping = [
    ("fotos-carrossel/foto-1.jpeg", "imagens/foto-1"),
    ("fotos-carrossel/foto-2.jpeg", "imagens/foto-2"),
    ("fotos-carrossel/foto-3.png", "imagens/foto-3"),
    ("fotos-carrossel/foto-4.png", "imagens/foto-4"),
    ("fotos-carrossel/foto-5.jpeg", "imagens/foto-5"),
    ("fotos-carrossel/foto-6.png", "imagens/foto-6"),
    ("assets/embedded-4319352716121903.png", "imagens/logo"),
    ("icons/icon-512.png", "imagens/app-icon-512"),
    ("icons/icon-192.png", "imagens/app-icon-192"),
    ("icons/favicon-32.png", "imagens/favicon-32"),
]

for src, dest_prefix in image_mapping:
    if os.path.exists(src):
        try:
            im = Image.open(src)
            # save webp
            webp_path = f"{dest_prefix}.webp"
            im.save(webp_path, "WEBP", quality=90)
            print(f"Generated WebP: {webp_path}")
            # also copy original extension
            ext = os.path.splitext(src)[1]
            orig_dest = f"{dest_prefix}{ext}"
            im.save(orig_dest)
            print(f"Saved original format: {orig_dest}")
        except Exception as e:
            print(f"Error converting {src}: {e}")

print("All downloads and conversions complete!")
