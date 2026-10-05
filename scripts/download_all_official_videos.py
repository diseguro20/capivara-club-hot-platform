import urllib.request, http.cookiejar, json, re, os, time, sys

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0'}

print("Authenticating with capivaraclubhot.com...", flush=True)
with opener.open(urllib.request.Request('https://capivaraclubhot.com/membros', headers=headers)) as res:
    html = res.read().decode('utf-8', errors='ignore')
csrf = re.search(r'name="csrf-token"\s+content="([^"]+)"', html).group(1)

opener.open(urllib.request.Request(
    'https://capivaraclubhot.com/api/login',
    data=json.dumps({'email': 'diseguro20@gmail.com', 'password': 'diego2001'}).encode('utf-8'),
    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'X-CSRF-TOKEN': csrf, 'Referer': 'https://capivaraclubhot.com/membros'}
))
print("Authenticated successfully!", flush=True)

dest_dir = "videos-tutoriais"
os.makedirs(dest_dir, exist_ok=True)

videos_to_download = [
    ("tutorial-02.mp4", 348380246),
    ("tutorial-03.mp4", 104773249),
    ("tutorial-04.mp4", 81753818),
    ("tutorial-05.mp4", 329101747),
    ("tutorial-06.mp4", 292021371),
    ("tutorial-07.mp4", 123363477),
    ("tutorial-08.mp4", 86152180),
    ("tutorial-09.mp4", 71719399),
]

for filename, expected_size in videos_to_download:
    target_path = os.path.join(dest_dir, filename)
    if os.path.exists(target_path) and os.path.getsize(target_path) == expected_size:
        print(f"[OK] {filename} already fully downloaded ({expected_size} bytes).", flush=True)
        continue

    tmp_path = target_path + ".tmp"
    url = f"https://capivaraclubhot.com/videos-tutoriais/{filename}"
    print(f"\n[START] Downloading {filename} ({expected_size / 1024 / 1024:.1f} MB)...", flush=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
    
    t0 = time.time()
    last_print = t0
    downloaded = 0
    with opener.open(req, timeout=120) as resp, open(tmp_path, "wb") as out_file:
        while True:
            chunk = resp.read(64 * 1024)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            now = time.time()
            if now - last_print >= 2.0:
                last_print = now
                elapsed = max(0.1, now - t0)
                mb = downloaded / 1024 / 1024
                speed = mb / elapsed
                pct = downloaded * 100 / expected_size
                print(f"  {filename}: {mb:.1f}MB / {expected_size / 1024 / 1024:.1f}MB ({pct:.1f}%) - {speed:.2f} MB/s", flush=True)

    if os.path.exists(target_path):
        os.remove(target_path)
    os.rename(tmp_path, target_path)
    print(f"[COMPLETE] {filename} finished ({expected_size / 1024 / 1024:.1f} MB) in {time.time() - t0:.1f}s.", flush=True)

print("\nALL 9 OFFICIAL TUTORIAL VIDEOS ARE NOW DOWNLOADED!", flush=True)
