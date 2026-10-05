with open('scripts/membros_autenticado.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print("CSS links:", re.findall(r'<link[^>]+href=["\']([^"\']+)["\']', html))
print("Script tags:", re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', html))
