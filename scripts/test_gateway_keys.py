import os
import urllib.request
import json

def test_keys(env_file):
    print(f"\n--- Testing keys from {env_file} ---")
    keys = {}
    if not os.path.exists(env_file):
        print("File does not exist.")
        return

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                keys[k.strip()] = v.strip().strip('"').strip("'")

    # Test Omega keys
    omega_pub = keys.get('OMEGA_PUBLIC_KEY') or keys.get('OMEGAPAY_API_KEY')
    omega_sec = keys.get('OMEGA_SECRET_KEY') or keys.get('OMEGAPAY_API_SECRET')
    if omega_pub and omega_sec:
        print(f"Testing Omega: {omega_pub[:8]}... / {omega_sec[:8]}...")
        url = "https://app.omegapayments.com.br/api/v1/gateway/producer"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "x-public-key": omega_pub,
            "x-secret-key": omega_sec
        })
        try:
            with urllib.request.urlopen(req) as r:
                data = json.loads(r.read().decode('utf-8'))
                print(">> [OMEGA PAY OK!]", data.get('name'), data.get('document'), data.get('email'))
        except Exception as e:
            msg = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else str(e)
            print(">> [OMEGA PAY FAIL]", msg)

    # Test Vizzion keys
    viz_pub = keys.get('VIZZION_PUBLIC_KEY')
    viz_sec = keys.get('VIZZION_SECRET_KEY')
    if viz_pub and viz_sec:
        print(f"Testing Vizzion: {viz_pub[:8]}... / {viz_sec[:8]}...")
        url = "https://app.vizzionpay.com.br/api/v1/gateway/producer"
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "x-public-key": viz_pub,
            "x-secret-key": viz_sec
        })
        try:
            with urllib.request.urlopen(req) as r:
                data = json.loads(r.read().decode('utf-8'))
                print(">> [VIZZION PAY OK!]", data.get('name'), data.get('document'), data.get('email'))
        except Exception as e:
            msg = e.read().decode('utf-8', errors='ignore') if hasattr(e, 'read') else str(e)
            print(">> [VIZZION PAY FAIL]", msg)

test_keys(r"c:\Users\diseg\Downloads\BubbleCash\.vercel\.env.production.local")
test_keys(r"c:\Users\diseg\Downloads\AUTOMAÇÃO\.vercel\.env.production.local")
