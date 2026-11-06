import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
req = urllib.request.Request('https://capivaraclubhot.com/membros', headers={'User-Agent': user_agent})
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

print("Membros length:", len(html))
print(html[:1500])
print("...")
print(html[-1500:])
