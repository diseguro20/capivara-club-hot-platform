import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('paginas/painel.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('workflow-downloads')
if idx != -1:
    start = c.rfind('<section', 0, idx)
    end = c.find('</section>', idx) + 10
    print("Workflows Section HTML:\n", c[start:end])
