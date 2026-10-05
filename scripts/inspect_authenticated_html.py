import re

with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

print('HTML length:', len(html))

# check headings and titles
titles = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', html, re.I | re.S)
print('--- HEADINGS (first 25) ---')
for t in titles[:25]:
    clean = re.sub(r'<[^>]+>', '', t).strip()
    if clean:
        print(' ', clean)

# check images
imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
print(f'--- IMAGES ({len(imgs)}) ---')
for img in imgs[:25]:
    print(' ', img)

# check videos
videos = re.findall(r'<(?:video|source|iframe)[^>]+src=["\']([^"\']+)["\']', html, re.I)
print(f'--- VIDEOS / IFRAMES ({len(videos)}) ---')
for v in videos:
    print(' ', v)

# check downloads
downloads = re.findall(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*', html, re.I)
print(f'--- ALL A HREF LINKS ({len(downloads)}) ---')
for d in set(downloads):
    print(' ', d)

# check scripts
scripts = re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', html, re.I)
print(f'--- SCRIPTS ({len(scripts)}) ---')
for s in scripts:
    print(' ', s)
