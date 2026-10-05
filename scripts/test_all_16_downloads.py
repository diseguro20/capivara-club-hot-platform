import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('paginas/painel.html', 'r', encoding='utf-8') as f:
    c = f.read()

links = re.findall(r'<a[^>]*class="copy workflow-download"[^>]*href="([^"]+)"', c)
print(f"Testing {len(links)} workflow download links on localhost:5500...")

errors = 0
for i, l in enumerate(links, 1):
    url = f"http://localhost:5500{l}"
    try:
        res = urllib.request.urlopen(url)
        content = res.read()
        print(f"{i:02d}. OK {l} -> Status: {res.status} ({len(content)} bytes)")
    except Exception as e:
        print(f"{i:02d}. FAIL {l} -> {e}")
        errors += 1

print(f"\nFinished local test: {len(links) - errors}/{len(links)} OK, {errors} errors.")
