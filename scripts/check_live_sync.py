import urllib.request
import json
import http.cookiejar
import re
import os

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. GET csrf
req = urllib.request.Request('https://capivaraclubhot.com/membros', headers={'User-Agent': 'Mozilla/5.0'})
with opener.open(req) as r:
    html = r.read().decode('utf-8', errors='ignore')
    csrf_m = re.search(r'name="csrf-token"\s+content="([^"]+)"', html)
    csrf = csrf_m.group(1) if csrf_m else ''

# 2. Login
data = json.dumps({'email': 'diseguro20@gmail.com', 'password': 'diego2001'}).encode('utf-8')
login_req = urllib.request.Request(
    'https://capivaraclubhot.com/api/login',
    data=data,
    headers={
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': csrf,
        'User-Agent': 'Mozilla/5.0'
    }
)
with opener.open(login_req) as r:
    login_info = json.loads(r.read().decode('utf-8'))
    print("Login successful:", login_info.get("email"))

# 3. Check prompts
req_p = urllib.request.Request(
    'https://capivaraclubhot.com/api/member/prompts',
    headers={'User-Agent': 'Mozilla/5.0', 'X-CSRF-TOKEN': csrf}
)
with opener.open(req_p) as r:
    p_data = json.loads(r.read().decode('utf-8'))
    live_prompts = p_data.get('prompts', [])
    print(f"Live Prompts count: {len(live_prompts)}")

# 4. Check prompts-18
req_18 = urllib.request.Request(
    'https://capivaraclubhot.com/api/member/prompts-18',
    headers={'User-Agent': 'Mozilla/5.0', 'X-CSRF-TOKEN': csrf}
)
with opener.open(req_18) as r:
    p18_data = json.loads(r.read().decode('utf-8'))
    live_prompts_18 = p18_data if isinstance(p18_data, list) else p18_data.get('prompts', [])
    print(f"Live Prompts-18 count: {len(live_prompts_18)}")

# 5. Check authenticated HTML for videos and workflows
req_m = urllib.request.Request(
    'https://capivaraclubhot.com/membros',
    headers={'User-Agent': 'Mozilla/5.0'}
)
with opener.open(req_m) as r:
    m_html = r.read().decode('utf-8', errors='ignore')
    vids = re.findall(r'data-protected-src="([^"]+)"', m_html)
    video_tags = re.findall(r'<video[^>]+>', m_html)
    workflows = re.findall(r'href="([^"]+\.json)"', m_html)
    print(f"data-protected-src count: {len(vids)}")
    for v in vids:
        print("  video src:", v)
    print(f"Total video tags in HTML: {len(video_tags)}")
    for vt in video_tags:
        print("  vt:", vt)
    print("Live workflow json links count:", len(set(workflows)))
    for wf in set(workflows):
        print("  wf:", wf)

print("Probe finished.")
