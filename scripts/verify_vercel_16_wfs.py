import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Fetch live Vercel painel HTML
url = 'https://capivara-club-hot.vercel.app/painel/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req)
html = res.read().decode('utf-8')

links = re.findall(r'<a[^>]*class="copy workflow-download"[^>]*href="([^"]+)"', html)
print(f"Found {len(links)} workflow download links on Vercel production:")

errors = 0
for i, l in enumerate(links, 1):
    wf_url = f"https://capivara-club-hot.vercel.app{l}"
    try:
        r = urllib.request.urlopen(urllib.request.Request(wf_url, headers={'User-Agent': 'Mozilla/5.0'}))
        content = r.read()
        print(f"{i:02d}. OK {l} -> Status: {r.status} ({len(content)} bytes)")
    except Exception as e:
        print(f"{i:02d}. FAIL {l} -> {e}")
        errors += 1

print(f"\nFinal Vercel verification: {len(links) - errors}/{len(links)} OK, {errors} errors.")
