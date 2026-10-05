import urllib.request
import urllib.error

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0'}

def check_url(path):
    url = base_url + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as res:
            ct = res.headers.get('Content-Type', '')
            cl = res.headers.get('Content-Length', len(res.read()))
            return res.status, ct, cl
    except urllib.error.HTTPError as e:
        return e.code, None, None
    except Exception as e:
        return None, None, str(e)

# 1. Check variation on fotos-carrossel
print("Checking carrossel variations...")
for i in range(1, 15):
    for ext in ['jpeg', 'jpg', 'png', 'webp', 'mp4']:
        for prefix in ['foto-', 'foto_', 'photo-', 'img-']:
            for suffix in ['', '-hot', '-nude', '_hot', '_nude', '-unclothed', '_unclothed', '-2', '_2']:
                p = f"/fotos-carrossel/{prefix}{i}{suffix}.{ext}"
                status, ct, cl = check_url(p)
                if status == 200:
                    print(f"FOUND: {p} ({ct}, {cl})")

# 2. Check storage / uploads / files / downloads
print("Checking common storage / media paths...")
common_media_dirs = [
    '/storage/', '/storage/videos/', '/storage/workflows/', '/storage/prompts/', '/storage/tools/',
    '/storage/app/', '/storage/public/', '/storage/uploads/',
    '/uploads/', '/videos/', '/video/', '/media/', '/assets/video/', '/assets/videos/',
    '/workflows/', '/prompts/', '/downloads/', '/files/'
]
for d in common_media_dirs:
    status, ct, cl = check_url(d)
    if status and status != 404:
        print(f"Directory {d}: {status} ({ct})")

# 3. Check common video filenames
print("Checking video files...")
video_names = [
    'video.mp4', 'intro.mp4', 'vsl.mp4', 'demo.mp4', 'preview.mp4', 'tutorial.mp4',
    'aula-1.mp4', 'aula1.mp4', 'aula.mp4', 'capivara.mp4', 'apresentacao.mp4',
    'modelo.mp4', 'ugc.mp4', 'hot.mp4'
]
video_prefixes = ['', '/assets/', '/videos/', '/storage/', '/media/', '/static/']
for pfx in video_prefixes:
    for vn in video_names:
        status, ct, cl = check_url(f"{pfx}{vn}")
        if status == 200:
            print(f"FOUND VIDEO: {pfx}{vn} ({ct}, {cl})")
