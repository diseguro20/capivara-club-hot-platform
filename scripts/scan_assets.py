import urllib.request

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0'}

prefixes = [
    "area_membros", "area-membros", "membros", "dashboard", "admin", "painel",
    "site_editavel", "site-editavel", "tools", "workflow", "workflows", "prompts",
    "esteira", "ferramentas", "tutorial", "tutoriais"
]

extensions = ["js", "css", "json", "html"]

candidates = []
for p in prefixes:
    for ext in extensions:
        candidates.append(f"/assets/{p}.{ext}")
        for i in range(1, 10):
            candidates.append(f"/assets/{p}-{i}.{ext}")
            candidates.append(f"/assets/{p}_{i}.{ext}")
            candidates.append(f"/assets/{p}-v{i}.{ext}")
            candidates.append(f"/assets/{p}_esteira_interna_ferramentas-{i}.{ext}")
            candidates.append(f"/assets/{p}_esteira_interna_ferramentas.{ext}")

found = []
for c in candidates:
    try:
        url = base_url + c
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=3) as res:
            if res.status == 200:
                print(f"FOUND: {c} ({len(res.read())} bytes)", flush=True)
                found.append(c)
    except:
        pass

print("Scan complete. Total found:", len(found))
