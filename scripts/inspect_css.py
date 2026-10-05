import urllib.request
import re

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

css_files = [
    "/assets/ui.css",
    "/assets/site_editavel-1.css",
    "/assets/area_membros_esteira_interna_ferramentas-1.css",
    "/assets/area_membros_esteira_interna_ferramentas-2.css",
    "/assets/area_membros_esteira_interna_ferramentas-3.css",
    "/assets/area_membros_esteira_interna_ferramentas-4.css",
    "/assets/area_membros_esteira_interna_ferramentas-5.css",
]

for css_path in css_files:
    url = base_url + css_path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as res:
            content = res.read().decode('utf-8', errors='ignore')
            print(f"=== {css_path} (length {len(content)}) ===")
            urls = re.findall(r'url\([\'"]?([^\'"\)]+)[\'"]?\)', content)
            if urls:
                print("URLs in CSS:", set(urls))
            # Also search for any class names or comments hinting at video / player / content
            keywords = ['video', 'player', 'iframe', 'mp4', 'stream', 'panda', 'vturb', 'vimeo', 'youtube', 'download', 'prompt', 'workflow']
            for kw in keywords:
                matches = re.findall(rf'[^;{{\}}]*{kw}[^;{{\}}]*', content, re.IGNORECASE)
                if matches:
                    print(f"Keyword '{kw}' matches (sample 3):", [m.strip() for m in matches[:3]])
    except Exception as e:
        print(f"Error {css_path}: {e}")
