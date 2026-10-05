import urllib.request

for p in [
    '/videos/PARTE%201.mp4',
    '/workflows/CONTROLMOTION%202%20-%20CAPIVARA%20DUHOT%20-%20VIDEO%20%2B18.json',
    '/imagens/Retrato%20Natural%20no%20Banheiro%20Moderno.png'
]:
    try:
        url = 'http://localhost:5500' + p
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req) as res:
            print(f"OK [200]: {p} - size: {res.headers.get('Content-Length')} bytes")
    except Exception as e:
        print(f"FAIL: {p} - {e}")
