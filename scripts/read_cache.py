p = r'C:\Users\diseg\AppData\Local\Microsoft\Edge\User Data\Default\Cache\Cache_Data\f_0078ee'
with open(p, 'rb') as f:
    data = f.read()

import re
urls = re.findall(b'https?://[^\\s"\'<>]+', data)
for u in set(urls):
    print(u.decode('utf-8', errors='ignore'))

print('--- Text Sample ---')
text = data.decode('utf-8', errors='ignore')
print(text[:1000])
