import os
import re

for fn in os.listdir('member-scripts'):
    if not fn.endswith('.js'): continue
    with open(os.path.join('member-scripts', fn), 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if 'data-content' in content or 'workflows' in content:
        print(f"File {fn} has data-content/workflows:")
        for line in content.split('\n'):
            if 'data-content' in line or 'workflows' in line or 'function' in line and 'page' in line.lower():
                print("  ", line[:120])
