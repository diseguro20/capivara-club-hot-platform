import urllib.request, json

tests = [
    ("Page: painel.html", "http://localhost:5500/paginas/painel.html"),
    ("Page: index.html (redirect)", "http://localhost:5500/"),
    ("API: session", "http://localhost:5500/api/session"),
    ("API: prompts", "http://localhost:5500/api/member/prompts"),
    ("API: prompts-18", "http://localhost:5500/api/member/prompts-18"),
    ("Workflow 1: faceswap", "http://localhost:5500/workflows/faceswap-capivara-duhot.json"),
    ("Workflow 4: video+18", "http://localhost:5500/workflows/CONTROLMOTION%202%20-%20CAPIVARA%20DUHOT%20-%20VIDEO%20%2B18.json"),
    ("Image: 001.jpg", "http://localhost:5500/member-assets/prompts-18/001.jpg"),
    ("Image: 041.webp", "http://localhost:5500/member-assets/prompts-18/041.webp"),
    ("Image: 562.webp", "http://localhost:5500/member-assets/prompts-18/562.webp"),
]

for label, url in tests:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            body = r.read()
            print(f"[OK] {label}: status {r.status}, length {len(body):,} bytes", flush=True)
    except Exception as e:
        print(f"[FAIL] {label}: {e}", flush=True)

print("\n--- Verifying All 9 Official Tutorial Videos (HTTP 206 Partial Content) ---", flush=True)
for i in range(1, 10):
    url = f"http://localhost:5500/videos-tutoriais/tutorial-{i:02d}.mp4"
    try:
        req = urllib.request.Request(url, headers={'Range': 'bytes=0-1048576', 'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            print(f"[OK] Tutorial {i:02d}: status {r.status}, range {r.headers.get('Content-Range')}, content-type {r.headers.get('Content-Type')}", flush=True)
    except Exception as e:
        print(f"[FAIL] Tutorial {i:02d}: {e}", flush=True)
