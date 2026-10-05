import urllib.request, http.cookiejar, json, re

login_url = 'https://capivaraclubhot.com/api/login'
membros_url = 'https://capivaraclubhot.com/membros'
base_url = 'https://capivaraclubhot.com'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

try:
    with opener.open(urllib.request.Request(membros_url, headers=headers), timeout=10) as res:
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
    with opener.open(urllib.request.Request(login_url, data=login_data, headers=post_headers, method='POST'), timeout=10) as res:
        print('Login status:', res.status)

    req = urllib.request.Request(base_url + '/api/member/prompts-18', headers={'User-Agent': headers['User-Agent'], 'Accept': 'application/json', 'Referer': membros_url})
    with opener.open(req, timeout=10) as res:
        live_data = json.loads(res.read().decode('utf-8'))
        print('Live prompts-18 count:', len(live_data))
        print('Live prompt 0:', live_data[0])
        print('Live prompt 1:', live_data[1])
except Exception as e:
    print('Error checking live:', e)
