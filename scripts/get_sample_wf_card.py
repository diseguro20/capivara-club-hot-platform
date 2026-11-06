import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('paginas/painel.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the section containing the workflow cards
idx = html.find('workflows/faceswap-capivara-duhot.json')
if idx != -1:
    start = html.rfind('<div class="workflow', 0, idx)
    if start == -1:
        start = html.rfind('<div', 0, idx)
    # find end of card
    end = html.find('</div>', idx) + 6
    print("Example card HTML:\n", html[start:end+200])
