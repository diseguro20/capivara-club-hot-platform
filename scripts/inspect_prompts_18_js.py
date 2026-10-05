with open('member-scripts/area_membros_esteira_interna_ferramentas-1.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

import re
matches = [m.start() for m in re.finditer(r'prompts-18', js)]
for i, m in enumerate(matches):
    print(f"--- Match {i+1} ---")
    chunk = js[max(0, m - 50):min(len(js), m + 800)]
    print(chunk.encode('ascii', errors='backslashreplace').decode('ascii'))
