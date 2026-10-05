import urllib.request, http.cookiejar, json, re, os
from concurrent.futures import ThreadPoolExecutor

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

dest_dir = "member-assets/gallery"
os.makedirs(dest_dir, exist_ok=True)

# Build list of 388 gallery images: 1-1.jpeg to 194-2.jpeg
tasks = []
for index in range(1, 195):
    for suffix in ('1', '2'):
        fname = f"{index}-{suffix}.jpeg"
        tasks.append(fname)

def download_img(fname):
    target = os.path.join(dest_dir, fname)
    if os.path.exists(target) and os.path.getsize(target) > 500:
        return fname, True, "cached"

    url = f"https://capivaraclubhot.com/member-assets/gallery/{fname}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
    try:
        with opener.open(req, timeout=10) as resp:
            data = resp.read()
            with open(target, 'wb') as f:
                f.write(data)
            return fname, True, len(data)
    except Exception as e:
        return fname, False, str(e)

print(f"Starting download of all {len(tasks)} gallery images into {dest_dir}...", flush=True)
with ThreadPoolExecutor(max_workers=20) as ex:
    results = list(ex.map(download_img, tasks))

successes = [r for r in results if r[1]]
failures = [r for r in results if not r[1]]
print(f"Gallery images downloaded: {len(successes)} successful, {len(failures)} failed.", flush=True)
if failures:
    print(f"First failures: {failures[:10]}", flush=True)
