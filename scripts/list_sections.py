with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<section[^>]*data-content=["\']([^"\']+)["\']', html)
print("All data-content sections:", matches)
