import urllib.request
import struct

url = 'https://github.com/diseguro20/capivara-club-hot-platform/releases/download/v1.0.0-videos/tutorial-09.mp4'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-1000'})
res = urllib.request.urlopen(req)
print('Status:', res.status)
print('Content-Range:', res.headers.get('Content-Range'))
data = res.read()
print('Read length:', len(data))
h1 = data[:8]
s1, n1 = struct.unpack('>I4s', h1)
print('First atom:', n1.decode(errors='ignore'), 'size:', s1)
h2 = data[s1:s1+8]
s2, n2 = struct.unpack('>I4s', h2)
print('Second atom:', n2.decode(errors='ignore'), 'size:', s2)
