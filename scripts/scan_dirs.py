import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

base_url = "https://capivaraclubhot.com"
headers = {'User-Agent': 'Mozilla/5.0'}

dirs = [
    'video', 'videos', 'media', 'audio', 'audios', 'download', 'downloads',
    'file', 'files', 'upload', 'uploads', 'storage', 'storage/app', 'storage/app/public',
    'content', 'contents', 'membro', 'membros', 'admin', 'painel', 'dashboard',
    'app', 'api', 'public', 'static', 'build', 'dist', 'src', 'docs',
    'workflows', 'workflow', 'prompts', 'prompt', 'tools', 'tool',
    'tutoriais', 'tutorial', 'aulas', 'aula', 'cursos', 'curso',
    'carrossel', 'fotos', 'img', 'icons', 'fonts'
]

def check(d):
    url = f"{base_url}/{d}/"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as res:
            print(f"[{res.status}] /{d}/")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"[403 DIR EXISTS] /{d}/")
        elif e.code != 404:
            print(f"[{e.code}] /{d}/")
    except:
        pass

with ThreadPoolExecutor(max_workers=8) as ex:
    ex.map(check, dirs)
