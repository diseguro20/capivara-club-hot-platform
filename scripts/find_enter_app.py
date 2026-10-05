with open('member-scripts/area_membros_esteira_interna_ferramentas-1.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'enterApp', js)]
for m in matches:
    print("--- enterApp call in JS ---")
    print(js[max(0, m - 50):min(len(js), m + 350)])
