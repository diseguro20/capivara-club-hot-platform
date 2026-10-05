import re

with open('scripts/rendered_dom.html', 'r', encoding='utf-8', errors='ignore') as f:
    dom = f.read()

match = re.search(r'<div class="prompt-gallery" id="gallery18Grid">([\s\S]*?)</div>\s*<div class="gallery-pagination"', dom)
if match:
    content = match.group(1).strip()
    print('gallery18Grid content length:', len(content))
    cards = len(re.findall(r'<article class="gallery-card"', content))
    print('Number of cards in gallery18Grid:', cards)
    if cards > 0:
        first_card = content[:content.find('</article>')+10]
        print('First card:\n', first_card)
else:
    print('gallery18Grid match not found!')
