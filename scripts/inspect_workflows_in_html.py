import re

with open('paginas/painel.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find cards or download links
links = re.findall(r'<a[^>]*href=["\']([^"\']*\.json)["\'][^>]*>(.*?)</a>', html, re.DOTALL)
print(f"Total .json links in painel.html: {len(links)}")
import sys
sys.stdout.reconfigure(encoding='utf-8')
for i, (href, text) in enumerate(links, 1):
    clean_text = re.sub(r'<[^>]+>', '', text).strip()
    print(f"{i:02d}. href='{href}' | text='{clean_text}'")

# Check all elements with class containing 'workflow'
wf_classes = re.findall(r'<div[^>]*class=["\'][^"\']*workflow[^"\']*["\'][^>]*>', html, re.I)
print(f"\nElements with class containing workflow: {len(wf_classes)}")

# Check tab or page navigation for workflows
tabs = re.findall(r'(\w+Page|\w+Tab)\([\'"](\w+)[\'"]\)', html)
print(f"\nPage/Tab triggers: {set(tabs)}")
