with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print('loginScreen tag:', re.findall(r'<section[^>]+id=["\']loginScreen["\'][^>]*>', html))
print('app tag:', re.findall(r'<section[^>]+id=["\']app["\'][^>]*>', html))
