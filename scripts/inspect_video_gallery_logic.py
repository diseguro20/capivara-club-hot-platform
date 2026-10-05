with open('member-scripts/area_membros_esteira_interna_ferramentas-1.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

import re

# 1. Search loadMemberGalleryImages
idx = js.find('loadMemberGalleryImages')
if idx != -1:
    print("=== loadMemberGalleryImages ===")
    print(js[idx:idx+800].encode('ascii', errors='backslashreplace').decode('ascii'))

# 2. Search all occurrences of tutorial and video
print("\n=== TUTORIAL / VIDEO LOGIC IN JS ===")
for m in re.finditer(r'(function\s+[a-zA-Z0-9_]*tutorial[a-zA-Z0-9_]*[^{]*\{[^}]*\})', js, re.I):
    print(m.group(1).encode('ascii', errors='backslashreplace').decode('ascii'))
    print('-'*40)

for m in re.finditer(r'(function\s+[a-zA-Z0-9_]*video[a-zA-Z0-9_]*[^{]*\{[^}]*\})', js, re.I):
    print(m.group(1).encode('ascii', errors='backslashreplace').decode('ascii'))
    print('-'*40)
