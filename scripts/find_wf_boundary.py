import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'(<div class="cards workflow-downloads">[\s\S]*?</div>\s*<div class="notice workflow-notice">)', c)
if m:
    print('Found workflow-downloads container, length:', len(m.group(1)))
    print('First 120 chars:\n', m.group(1)[:120])
    print('Last 120 chars:\n', m.group(1)[-120:])
else:
    print('Not found!')
