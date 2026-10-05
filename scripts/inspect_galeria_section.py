with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
gal_match = re.search(r'(<section[^>]*data-content=["\']galeria["\'][^>]*>.*?</section>)', html, re.S)
if gal_match:
    print("Found data-content='galeria' section! Length:", len(gal_match.group(1)))
    # print sample images
    imgs = re.findall(r'<img[^>]+(?:src|data-src)=["\']([^"\']+)["\']', gal_match.group(1))
    print(f"Total images in galeria: {len(imgs)}")
    for img in imgs:
        print(" ", img)
