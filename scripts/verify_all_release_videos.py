import urllib.request

base = 'https://github.com/diseguro20/capivara-club-hot-platform/releases/download/v1.0.0-videos'
for i in range(1, 10):
    fn = f'tutorial-{i:02d}.mp4'
    url = f'{base}/{fn}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-10'})
        with urllib.request.urlopen(req) as res:
            cr = res.headers.get("Content-Range")
            print(f"OK {fn} -> Status: {res.status} | Content-Range: {cr}")
    except Exception as e:
        print(f"ERR {fn} -> {e}")
