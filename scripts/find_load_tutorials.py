with open('member-scripts/area_membros_esteira_interna_ferramentas-1.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

import re
idx = js.find('function loadProtectedTutorials')
if idx != -1:
    print(js[idx:idx+1200].encode('ascii', errors='backslashreplace').decode('ascii'))
