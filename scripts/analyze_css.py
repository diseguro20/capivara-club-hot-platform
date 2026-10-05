import re

with open("_assets_site_editavel-1.css", "w", encoding="utf-8") as f:
    pass

import urllib.request
headers = {'User-Agent': 'Mozilla/5.0'}
req = urllib.request.Request('https://capivaraclubhot.com/assets/area_membros_esteira_interna_ferramentas-1.css', headers=headers)
css = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

with open("area_membros.css", "w", encoding="utf-8") as f:
    f.write(css)

print("CSS saved. Total lines:", len(css.splitlines()))

# Find all background / url / font
urls = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', css)
print("All URLs in area_membros.css:", set(urls))

# Extract all class names to see what sections exist
classes = set(re.findall(r'\.([a-zA-Z0-9_\-]+)', css))
print("Sample classes count:", len(classes))
keywords = ['video', 'aula', 'module', 'modulo', 'player', 'download', 'workflow', 'prompt', 'card', 'banner', 'nav', 'tab', 'modal']
for kw in keywords:
    matching = [c for c in classes if kw in c.lower()]
    print(f"Classes with '{kw}' ({len(matching)}):", matching[:15])
