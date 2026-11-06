import urllib.request
import hashlib
import os

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
files_to_check = [
    '/assets/ui.css?v=20260928-2',
    '/assets/ui.js?v=20260928-2',
    '/assets/site_editavel-1.css?v=20260928-2',
    '/assets/site_editavel-1.js?v=20261004-3',
    '/assets/site_editavel-2.js?v=20260928-4',
    '/assets/login.js?v=20260928-2',
    '/assets/http.js?v=20260929-1'
]

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

for uri in files_to_check:
    clean_path = uri.split('?')[0].lstrip('/')
    url = f"https://capivaraclubhot.com{uri}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req, timeout=10) as r:
            remote_bytes = r.read()
            remote_md5 = hashlib.md5(remote_bytes).hexdigest()
            remote_len = len(remote_bytes)
            
            local_path = os.path.join(ROOT_DIR, clean_path.replace('/', os.sep))
            if os.path.exists(local_path):
                with open(local_path, 'rb') as lf:
                    local_bytes = lf.read()
                    local_md5 = hashlib.md5(local_bytes).hexdigest()
                    local_len = len(local_bytes)
                print(f"{clean_path}: Remote len={remote_len} md5={remote_md5[:8]} | Local len={local_len} md5={local_md5[:8]}")
            else:
                print(f"{clean_path}: Remote len={remote_len} (not found locally)")
    except Exception as e:
        print(f"Error {uri}: {e}")
