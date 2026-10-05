with open('member-scripts/area_membros_esteira_interna_ferramentas-1.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

import re
endpoints = re.findall(r'["\'`](/[^"\'`\s]+)["\'`]', js)
clean_endpoints = [e for e in set(endpoints) if not e.endswith(('.css', '.png', '.jpg', '.jpeg', '.svg', '.ico'))]
print("All endpoints in JS:", clean_endpoints)

idx = js.find('loadMemberPrompts')
if idx != -1:
    print("\n--- Around loadMemberPrompts ---")
    print(js[max(0, idx - 100):min(len(js), idx + 800)])

idx_vid = js.find('videos-tutoriais')
if idx_vid != -1:
    print("\n--- Around videos-tutoriais ---")
    print(js[max(0, idx_vid - 100):min(len(js), idx_vid + 500)])
