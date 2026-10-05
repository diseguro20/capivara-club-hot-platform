import re, os

with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

imgs = re.findall(r'<img[^>]+(?:src|data-src)=["\']([^"\']+)["\']', html)
print(f"Total img tags: {len(imgs)}")
gallery_imgs = [i for i in imgs if 'gallery' in i or 'member-assets' in i or 'reference' in i]
print(f"Gallery / member-assets imgs ({len(gallery_imgs)}):")
for g in set(gallery_imgs):
    print(" ", g)

all_links = re.findall(r'(?:href|src|data-src|data-protected-src)=["\']([^"\']+)["\']', html)
tutorials = [l for l in all_links if 'tutorial' in l.lower() or 'video' in l.lower()]
print(f"\nTutorial / video references ({len(tutorials)}):")
for t in set(tutorials):
    print(" ", t)

workflows = [l for l in all_links if 'workflow' in l.lower() or '.json' in l.lower()]
print(f"\nWorkflow references ({len(workflows)}):")
for w in set(workflows):
    print(" ", w)

cards = re.findall(r'(<div[^>]*class="[^"]*tutorial-card[^"]*"[^>]*>.*?</div>\s*</div>)', html, re.DOTALL)
print(f"\nTutorial cards found: {len(cards)}")
for i, c in enumerate(cards):
    title = re.search(r'<h4>(.*?)</h4>', c)
    num = re.search(r'tutorial-num">([^<]+)<', c)
    v = re.search(r'<video[^>]*>', c)
    print(f"Card {i+1}: num={num.group(1) if num else '?'}, title={title.group(1) if title else '?'}")
    print(f"  video tag: {v.group(0) if v else 'NO VIDEO TAG'}")

