import sys
import os
sys.path.insert(0, os.path.abspath('.'))
from scripts.sync_engine import CapivaraSyncEngine
import re
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

engine = CapivaraSyncEngine()
if engine.login():
    print("Login OK!")
    membros_url = f"{engine.config.get('live_url')}/membros"
    req = urllib.request.Request(membros_url, headers={'User-Agent': engine.user_agent})
    with engine.opener.open(req) as res:
        html = res.read().decode('utf-8', errors='ignore')
    
    matches = re.findall(r'href=["\']([^"\']*\.json)["\']', html)
    print(f"Total .json href matches on live /membros: {len(matches)}")
    for m in set(matches):
        print("Live workflow href:", urllib.parse.unquote(m))
else:
    print("Login failed!")
