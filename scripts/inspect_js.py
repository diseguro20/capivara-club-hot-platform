import urllib.request
import re
import json

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get(path):
    url = base_url + path if path.startswith('/') else base_url + '/' + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return f"ERROR: {e}"

files_to_check = [
    "/assets/ui.js",
    "/assets/http.js",
    "/assets/analytics.js",
    "/assets/site_editavel-1.js",
    "/assets/site_editavel-2.js",
    "/assets/login.js",
    "/manifest.json"
]

for f in files_to_check:
    print(f"=== {f} ===")
    content = get(f)
    print("Length:", len(content))
    # look for endpoints, urls, mp4, vimeo, youtube, panda, etc.
    urls = set(re.findall(r'https?://[^\s"\'<>]+', content))
    endpoints = set(re.findall(r'["\'](/[a-zA-Z0-9_\-\./]+)["\']', content))
    print("Found URLs:", urls)
    print("Found endpoints:", [e for e in endpoints if not e.endswith(('.js', '.css', '.png', '.jpg'))])
    with open(f.replace('/', '_'), "w", encoding="utf-8") as out:
        out.write(content)
