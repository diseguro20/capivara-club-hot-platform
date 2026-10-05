import urllib.request
import http.cookiejar
import json
import re
import os

login_url = "https://capivaraclubhot.com/api/login"
membros_url = "https://capivaraclubhot.com/membros"
base_url = "https://capivaraclubhot.com"

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. Login
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
login_data = json.dumps({"email": "diseguro20@gmail.com", "password": "diego2001"}).encode('utf-8')
opener.open(urllib.request.Request(login_url, data=login_data, headers=post_headers, method='POST'))

def get_json(endpoint):
    url = base_url + endpoint
    req = urllib.request.Request(url, headers={'User-Agent': headers['User-Agent'], 'Accept': 'application/json', 'Referer': membros_url})
    try:
        with opener.open(req) as res:
            data = res.read().decode('utf-8')
            return json.loads(data)
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return None

# 1. Fetch prompts
print("=== Fetching /api/member/prompts ===")
prompts = get_json('/api/member/prompts')
if prompts:
    with open("member-assets/member_prompts.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    print("Saved member_prompts.json! Total prompts:", len(prompts.get('prompts', [])))

# 2. Fetch prompts-18
print("=== Fetching /api/member/prompts-18 ===")
prompts_18 = get_json('/api/member/prompts-18')
if prompts_18:
    with open("member-assets/member_prompts_18.json", "w", encoding="utf-8") as f:
        json.dump(prompts_18, f, indent=2, ensure_ascii=False)
    print("Saved member_prompts_18.json! Total items:", len(prompts_18))

# 3. Check and download videos-tutoriais
print("=== Checking /videos-tutoriais/tutorial-X.mp4 ===")
os.makedirs("videos-tutoriais", exist_ok=True)
for i in range(1, 15):
    vid_url = f"/videos-tutoriais/tutorial-{i}.mp4"
    url = base_url + vid_url
    req = urllib.request.Request(url, headers={'User-Agent': headers['User-Agent'], 'Referer': membros_url})
    try:
        with opener.open(req) as res:
            vid_data = res.read()
            local_vid = f"videos-tutoriais/tutorial-{i}.mp4"
            with open(local_vid, "wb") as vf:
                vf.write(vid_data)
            print(f"[FOUND VIDEO!] {vid_url} -> {local_vid} ({len(vid_data)} bytes)")
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print(f"[{e.code}] {vid_url}")
    except Exception as e:
        pass
