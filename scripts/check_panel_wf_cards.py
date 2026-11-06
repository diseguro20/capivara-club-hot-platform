import re

with open('paginas/painel.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find workflows section
match = re.search(r'<section[^>]*id=["\'](?:tab-)?workflows["\'][^>]*>(.*?)</section>', html, re.DOTALL)
if match:
    section_html = match.group(1)
    # Find all download links to workflows
    links = re.findall(r'<a[^>]*href=["\']([^"\']*\.json)["\'][^>]*>', section_html)
    print(f"Total .json links in workflows section: {len(links)}")
    for i, l in enumerate(links, 1):
        print(f"{i:02d}. Link: {l}")
else:
    print("Section workflows not found in painel.html!")
