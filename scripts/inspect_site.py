import urllib.request
import re
import json
from urllib.parse import urljoin

base_url = "https://capivaraclubhot.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def get(url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            return res.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

html = get(base_url)
print("Fetched base_url length:", len(html))

with open("index_source.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n=== VIDEO / MEDIA / IFRAME TAGS ===")
for tag in re.findall(r'<(?:video|iframe|embed|source|object)[^>]+>', html, re.IGNORECASE):
    print(tag)

print("\n=== SCRIPT TAGS ===")
for src in re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE):
    print(src)

print("\n=== LINKS (A HREF) ===")
for href in re.findall(r'<a[^>]+href=["\']([^"\']+)["\']', html, re.IGNORECASE):
    print(href)

print("\n=== IMAGES ===")
for img in re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.IGNORECASE):
    print(img)

print("\n=== CSS LINKS ===")
for css in re.findall(r'<link[^>]+href=["\']([^"\']+\.css[^"\']*)["\']', html, re.IGNORECASE):
    print(css)

# Check robots.txt and sitemap
print("\n=== ROBOTS.TXT ===")
print(get("https://capivaraclubhot.com/robots.txt"))

print("\n=== SITEMAP.XML ===")
print(get("https://capivaraclubhot.com/sitemap.xml"))
