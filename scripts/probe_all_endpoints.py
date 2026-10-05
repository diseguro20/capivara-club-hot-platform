import urllib.request, http.cookiejar, json, re

login_url = 'https://capivaraclubhot.com/api/login'
membros_url = 'https://capivaraclubhot.com/membros'
base_url = 'https://capivaraclubhot.com'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

with opener.open(urllib.request.Request(membros_url, headers=headers)) as res:
    html = res.read().decode('utf-8', errors='ignore')
    csrf_token = re.search(r'name="csrf-token"\s+content="([^"]+)"', html).group(1)

post_headers = {
    'User-Agent': headers['User-Agent'],
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-CSRF-TOKEN': csrf_token,
    'Referer': membros_url,
    'Origin': base_url
}
login_data = json.dumps({'email': 'diseguro20@gmail.com', 'password': 'diego2001'}).encode('utf-8')
opener.open(urllib.request.Request(login_url, data=login_data, headers=post_headers, method='POST'))

for ep in ['/api/member/prompts', '/api/member/prompts-18', '/api/prompts', '/api/prompts-18', '/api/galeria', '/api/member/gallery', '/api/member/data', '/api/data']:
    try:
        req = urllib.request.Request(base_url + ep, headers={'User-Agent': headers['User-Agent'], 'Accept': 'application/json', 'Referer': membros_url})
        with opener.open(req) as res:
            data = res.read().decode('utf-8')
            print(f'Endpoint {ep}: SUCCESS ({len(data)} chars)')
    except Exception as e:
        print(f'Endpoint {ep}: {e}')
