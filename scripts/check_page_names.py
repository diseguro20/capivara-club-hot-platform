import re

with open('paginas/painel.html', 'r', encoding='utf-8') as f:
    c = f.read()

pages = re.findall(r'data-content="([^"]+)"', c)
print("Data-content pages in painel.html:", pages)

navs = re.findall(r'data-nav="([^"]+)"', c)
print("Data-nav buttons:", navs)

# Also check openPage function definition
m = re.search(r'function openPage\([^\)]*\)\s*\{[\s\S]*?\}', c)
if m:
    print("\nopenPage function:\n", m.group(0)[:300])
