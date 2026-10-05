import re

with open("scripts/membros_autenticado.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find tutorial sections or video embeds
print("=== SECTIONS IN HTML ===")
sections = re.findall(r'<section[^>]*id=["\']([^"\']+)["\']', html)
print("Sections IDs:", sections)

# Search for youtube / vimeo / panda / vturb / iframe / video in html and js
for keyword in ["youtube", "vimeo", "panda", "vturb", "b-cdn", "iframe", "embed", "player", "video", "notion"]:
    matches = re.findall(rf'[^"\'<>\s]*{keyword}[^"\'<>\s]*', html, re.I)
    print(f"Keyword '{keyword}' in HTML ({len(matches)}):", set(matches[:5]))

# Also check member-scripts/area_membros_esteira_interna_ferramentas-1.js
with open("member-scripts/area_membros_esteira_interna_ferramentas-1.js", "r", encoding="utf-8", errors="ignore") as f:
    js = f.read()

print("JS length:", len(js))
for keyword in ["youtube", "vimeo", "panda", "vturb", "b-cdn", "video", "mp4", "prompt", "workflow"]:
    matches = re.findall(rf'[^"\'<>\s]*{keyword}[^"\'<>\s]*', js, re.I)
    print(f"Keyword '{keyword}' in JS ({len(matches)}):", set(matches[:5]))
