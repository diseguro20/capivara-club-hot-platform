import urllib.request
import urllib.error

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0'}

sensitive_paths = [
    '/.git/HEAD',
    '/.git/config',
    '/.env',
    '/.env.example',
    '/composer.json',
    '/package.json',
    '/storage/logs/laravel.log',
    '/storage/logs/laravel-2026-09-28.log',
    '/storage/logs/laravel-2026-10-04.log',
    '/storage/logs/laravel-2026-10-05.log',
    '/storage/framework/views/',
    '/api/documentation',
    '/api/docs',
    '/swagger.json',
    '/openapi.json',
    '/telescope',
    '/horizon',
    '/nova',
    '/sanctum/csrf-cookie'
]

for p in sensitive_paths:
    url = base_url + p
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as res:
            print(f"[FOUND {res.status}] {p} - size: {len(res.read())}")
    except urllib.error.HTTPError as e:
        if e.code not in [403, 404]:
            print(f"[{e.code}] {p}")
    except Exception as e:
        pass
print("Finished check.")
