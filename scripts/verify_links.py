import os
import re

def check_html(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    rel_dir = os.path.dirname(filepath)
    refs = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
    missing = []
    for r in refs:
        if r.startswith(('http://', 'https://', '#', 'mailto:', 'tel:', 'data:', 'javascript:')):
            continue
        clean_r = r.split('?')[0].split('#')[0]
        if not clean_r:
            continue
        full_p = os.path.normpath(os.path.join(rel_dir, clean_r))
        if not os.path.exists(full_p):
            missing.append((r, full_p))
    print(f"=== {filepath} ===")
    if missing:
        print("Missing files:", missing)
    else:
        print("All local references exist! OK.")

check_html('index.html')
check_html('paginas/membros.html')
check_html('paginas/painel.html')
check_html('paginas/admin.html')
