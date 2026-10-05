import urllib.request
import urllib.parse
import http.cookiejar
import json
import re

login_url = "https://capivaraclubhot.com/api/login"
membros_url = "https://capivaraclubhot.com/membros"
base_url = "https://capivaraclubhot.com"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
}

# 1. First GET to get CSRF token and initial session cookie
req = urllib.request.Request(membros_url, headers=headers)
try:
    with opener.open(req) as res:
        html = res.read().decode('utf-8', errors='ignore')
        csrf_match = re.search(r'name="csrf-token"\s+content="([^"]+)"', html)
        csrf_token = csrf_match.group(1) if csrf_match else None
        print("Initial GET OK. CSRF Token:", csrf_token)
        print("Cookies after GET:", [c.name for c in cj])
except Exception as e:
    print("Error during initial GET:", e)
    csrf_token = None

# 2. POST login
post_headers = {
    'User-Agent': headers['User-Agent'],
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CSRF-TOKEN': csrf_token or '',
    'Referer': membros_url,
    'Origin': base_url
}

login_data = json.dumps({
    "email": "diseguro20@gmail.com",
    "password": "diego2001"
}).encode('utf-8')

login_req = urllib.request.Request(login_url, data=login_data, headers=post_headers, method='POST')

try:
    with opener.open(login_req) as res:
        login_resp = res.read().decode('utf-8', errors='ignore')
        print("Login status:", res.status)
        print("Login response:", login_resp)
        print("Cookies after login:", [c.name for c in cj])
except urllib.error.HTTPError as e:
    print(f"Login failed HTTP {e.code}:", e.read().decode('utf-8', errors='ignore'))
    exit(1)
except Exception as e:
    print("Login error:", e)
    exit(1)

# 3. GET authenticated /membros page
auth_headers = {
    'User-Agent': headers['User-Agent'],
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': membros_url
}

req_membros = urllib.request.Request(membros_url, headers=auth_headers)
try:
    with opener.open(req_membros) as res:
        membros_html = res.read().decode('utf-8', errors='ignore')
        print("Authenticated membros HTML length:", len(membros_html))
        with open("scripts/membros_autenticado.html", "w", encoding="utf-8") as f:
            f.write(membros_html)
        print("Saved scripts/membros_autenticado.html successfully!")
except Exception as e:
    print("Error fetching authenticated membros:", e)
