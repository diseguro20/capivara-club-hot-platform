import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
login_url = "https://capivaraclubhot.com/api/login"
resp = session.post(login_url, json={"email": "diseguro20@gmail.com", "senha": "diego2001"}, timeout=15)
print("Login status:", resp.status_code)

# Check all possible pages
pages = [
    "https://capivaraclubhot.com/membros",
    "https://capivaraclubhot.com/painel",
    "https://capivaraclubhot.com/workflows",
    "https://capivaraclubhot.com/paginas/membros.html",
    "https://capivaraclubhot.com/paginas/painel.html"
]

all_found = set()

for url in pages:
    r = session.get(url, timeout=15)
    print(f"Fetching {url}: status={r.status_code} len={len(r.text)}")
    matches = re.findall(r'["\']([^"\']*\.json[^"\']*)["\']', r.text)
    for m in matches:
        if 'workflow' in m.lower() or 'capivara' in m.lower() or 'json' in m.lower():
            all_found.add(m)

print(f"\nTotal unique workflow/json references found on live site: {len(all_found)}")
for idx, wf in enumerate(sorted(all_found), 1):
    print(f"{idx:02d}. {wf}")
