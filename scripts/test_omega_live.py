import os
import urllib.request
import json

env_path = r"c:\Users\diseg\Downloads\BubbleCash\.vercel\.env.production.local"
pub_key = None
sec_key = None

with open(env_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line.startswith("OMEGA_PUBLIC_KEY="):
            pub_key = line.split("=", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("OMEGA_SECRET_KEY="):
            sec_key = line.split("=", 1)[1].strip().strip('"').strip("'")

print(f"Loaded pub_key: {pub_key[:8]}...{pub_key[-4:] if pub_key else ''}")
print(f"Loaded sec_key: {sec_key[:8]}...{sec_key[-4:] if sec_key else ''}")

# 1. Test Producer endpoint
url = "https://app.omegapayments.com.br/api/v1/gateway/producer"
req = urllib.request.Request(url, headers={
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "x-public-key": pub_key,
    "x-secret-key": sec_key
})

try:
    with urllib.request.urlopen(req) as res:
        data = json.loads(res.read().decode("utf-8"))
        print("\n[SUCCESS] Omega Pay Authenticated!")
        print(f"Producer Name: {data.get('name')}")
        print(f"Producer Email: {data.get('email')}")
        print(f"Producer Document: {data.get('document')}")
        print(f"Producer Phone: {data.get('phone')}")
        print(f"Producer Status: {data.get('status')}")
except Exception as e:
    print(f"\n[ERROR] Omega Pay connection failed: {e}")
    if hasattr(e, 'read'):
        print("Response body:", e.read().decode('utf-8', errors='ignore'))
