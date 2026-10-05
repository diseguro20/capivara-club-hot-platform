import urllib.request
from concurrent.futures import ThreadPoolExecutor

base = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0'}

candidates = [
    "/video.mp4", "/videos.mp4", "/demo.mp4", "/vsl.mp4", "/intro.mp4",
    "/preview.mp4", "/capivara.mp4", "/modelo.mp4", "/hot.mp4", "/trailer.mp4",
    "/apresentacao.mp4", "/tutorial.mp4", "/aula.mp4", "/aula-1.mp4",
    "/assets/video.mp4", "/assets/demo.mp4", "/assets/intro.mp4", "/assets/vsl.mp4",
    "/assets/preview.mp4", "/assets/tutorial.mp4",
    "/videos/video.mp4", "/videos/demo.mp4", "/videos/intro.mp4", "/videos/1.mp4",
    "/media/video.mp4", "/media/demo.mp4", "/media/intro.mp4",
    "/storage/video.mp4", "/storage/demo.mp4", "/storage/intro.mp4",
    "/fotos-carrossel/video.mp4", "/fotos-carrossel/video-1.mp4",
    "/fotos-carrossel/foto-1.mp4", "/fotos-carrossel/foto-2.mp4",
    "/fotos-carrossel/foto-3.mp4", "/fotos-carrossel/foto-4.mp4",
    "/fotos-carrossel/foto-5.mp4", "/fotos-carrossel/foto-6.mp4",
    "/video.webm", "/demo.webm", "/intro.webm", "/assets/video.webm",
    "/video.m3u8", "/hls/master.m3u8", "/stream.m3u8",
]

def check(path):
    url = base + path
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as res:
            if res.status == 200:
                print(f"[FOUND VIDEO!] {path} ({res.headers.get('Content-Length')})", flush=True)
    except:
        pass

with ThreadPoolExecutor(max_workers=10) as ex:
    ex.map(check, candidates)

print("Video search done.")
