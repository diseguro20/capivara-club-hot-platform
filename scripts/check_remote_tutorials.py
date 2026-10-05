import urllib.request, http.cookiejar, json, re

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0'}

with opener.open(urllib.request.Request('https://capivaraclubhot.com/membros', headers=headers)) as res:
    html = res.read().decode('utf-8', errors='ignore')
    csrf = re.search(r'name="csrf-token"\s+content="([^"]+)"', html).group(1)

opener.open(urllib.request.Request(
    'https://capivaraclubhot.com/api/login',
    data=json.dumps({'email': 'diseguro20@gmail.com', 'password': 'diego2001'}).encode('utf-8'),
    headers={'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json', 'X-CSRF-TOKEN': csrf, 'Referer': 'https://capivaraclubhot.com/membros'}
))

print("Checking remote server for tutorial-01.mp4 to tutorial-10.mp4...")
for i in range(1, 11):
    url = f"https://capivaraclubhot.com/videos-tutoriais/tutorial-{i:02d}.mp4"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://capivaraclubhot.com/membros'})
    try:
        with opener.open(req) as res:
            data = res.read()
            print(f"[FOUND REMOTE!] tutorial-{i:02d}.mp4 -> {len(data)} bytes")
            with open(f"videos-tutoriais/tutorial-{i:02d}.mp4", "wb") as f:
                f.write(data)
    except Exception as e:
        print(f"tutorial-{i:02d}.mp4: {e}")
