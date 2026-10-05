import urllib.request
import urllib.error
import json

data = json.dumps({"email": "test@test.com", "password": "wrongpassword"}).encode('utf-8')
req = urllib.request.Request(
    'https://capivaraclubhot.com/api/login',
    data=data,
    headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
)

try:
    with urllib.request.urlopen(req) as res:
        print('Status:', res.status)
        print('Body:', res.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code)
    print('Body:', e.read().decode('utf-8'))
