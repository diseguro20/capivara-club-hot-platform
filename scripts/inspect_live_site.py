import urllib.request
import re

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

# 1. Fetch homepage
req = urllib.request.Request('https://capivaraclubhot.com', headers={'User-Agent': user_agent})
with urllib.request.urlopen(req, timeout=10) as r:
    home_html = r.read().decode('utf-8', errors='ignore')

print("=== CAPIVARACLUBHOT.COM HOMEPAGE ===")
print("Scripts on homepage:")
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', home_html)
for s in scripts:
    print(" ", s)

print("\nStyles on homepage:")
styles = re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', home_html)
for st in styles:
    print(" ", st)

print("\nLinks on homepage:")
links = re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', home_html)
for l in set(links):
    print(" ", l)

# 2. Fetch /membros
try:
    req2 = urllib.request.Request('https://capivaraclubhot.com/membros', headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req2, timeout=10) as r2:
        membros_html = r2.read().decode('utf-8', errors='ignore')
        print(f"\n/membros status: {r2.status}, len: {len(membros_html)}")
        m_scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', membros_html)
        print("Scripts on /membros:")
        for s in m_scripts:
            print(" ", s)
except Exception as e:
    print("Error fetching /membros:", e)
