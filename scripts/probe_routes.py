import urllib.request

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

candidates = [
    # JS candidates
    "/assets/area_membros_esteira_interna_ferramentas-1.js",
    "/assets/area_membros_esteira_interna_ferramentas-2.js",
    "/assets/area_membros_esteira_interna_ferramentas-3.js",
    "/assets/area_membros_esteira_interna_ferramentas-4.js",
    "/assets/area_membros_esteira_interna_ferramentas-5.js",
    "/assets/area_membros.js",
    "/assets/membros.js",
    "/assets/app.js",
    "/assets/main.js",
    "/assets/dashboard.js",
    "/assets/workflows.js",
    "/assets/prompts.js",
    "/assets/tools.js",
    # Page candidates
    "/membros",
    "/membros/dashboard",
    "/membros/painel",
    "/membros/conteudo",
    "/membros/prompts",
    "/membros/workflows",
    "/membros/ferramentas",
    "/membros/videos",
    "/membros/aulas",
    "/dashboard",
    "/painel",
    "/conteudo",
    "/prompts",
    "/workflows",
    "/ferramentas",
    "/aulas",
    "/videos",
    # API candidates
    "/api/membros",
    "/api/conteudo",
    "/api/prompts",
    "/api/workflows",
    "/api/videos",
    "/api/tools",
    "/api/user",
    "/api/me",
    "/api/config",
]

for path in candidates:
    url = base_url + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as res:
            print(f"[FOUND {res.status}] {path} (len: {len(res.read())})")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[{e.code}] {path}")
    except Exception as e:
        pass
