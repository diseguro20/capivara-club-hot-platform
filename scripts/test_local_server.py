import urllib.request

try:
    with urllib.request.urlopen('http://localhost:5500/api/session', timeout=3) as r:
        print('Session API:', r.status, r.read().decode())
except Exception as e:
    print('Session API error:', e)

try:
    req = urllib.request.Request('http://localhost:5500/videos-tutoriais/tutorial-01.mp4', headers={'Range': 'bytes=0-1000'})
    with urllib.request.urlopen(req, timeout=3) as r:
        print('Video 01 Range:', r.status, r.headers.get('Content-Range'))
except Exception as e:
    print('Video 01 error:', e)

try:
    with urllib.request.urlopen('http://localhost:5500/member-assets/prompts-18/001.jpg', timeout=3) as r:
        print('Prompt image 001:', r.status, r.headers.get('Content-Length'))
except Exception as e:
    print('Prompt image 001 error:', e)

try:
    with urllib.request.urlopen('http://localhost:5500/member-assets/prompts-18/041.webp', timeout=3) as r:
        print('Prompt image 041:', r.status, r.headers.get('Content-Length'))
except Exception as e:
    print('Prompt image 041 error:', e)
