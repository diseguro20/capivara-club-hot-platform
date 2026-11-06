import urllib.request

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
for url in [
    'https://capivaraclubhot.com/assets/login.js?v=20260928-2',
    'https://capivaraclubhot.com/assets/http.js?v=20260929-1',
    'https://capivaraclubhot.com/assets/site_editavel-1.js?v=20261004-3'
]:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
            print(f"=== {url} ===")
            print(f"Length: {len(content)}")
            print(content[:300])
            print("...")
    except Exception as e:
        print(f"Error {url}: {e}")
