import os
import json
import uuid
import datetime
import urllib.request
import urllib.error

OMEGA_PUBLIC_KEY = os.environ.get("OMEGA_PUBLIC_KEY", "diseguro20_jfja0nvfswymuvpt")
OMEGA_SECRET_KEY = os.environ.get("OMEGA_SECRET_KEY", "49b376xndh2s4n9h1rc3suzm5tnjgw3s3o26lx4rp94gi0dl5vl338dzal47eur2")
OMEGA_BASE_URL = os.environ.get("OMEGA_BASE_URL", "https://app.omegapayments.com.br/api/v1")

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_FILE = os.path.join(ROOT_DIR, "data", "paid_users.json")

def load_data():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    initial = {
        "paidUsers": ["diseguro20@gmail.com"],
        "transactions": {}
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(initial, f, indent=2)
    return initial

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def is_user_paid(email):
    if not email:
        return False
    clean = email.strip().lower()
    if clean == "diseguro20@gmail.com":
        return True
    data = load_data()
    paid_list = data.get("paidUsers", [])
    for u in paid_list:
        e = u if isinstance(u, str) else u.get("email", "")
        if e.strip().lower() == clean:
            return True
    return False

def mark_user_as_paid(email, tx_info=None):
    if not email:
        return
    clean = email.strip().lower()
    data = load_data()
    paid_list = data.setdefault("paidUsers", [])
    if clean not in [u.lower() if isinstance(u, str) else u.get("email","").lower() for u in paid_list]:
        paid_list.append(clean)
    if tx_info and "idTransaction" in tx_info:
        data.setdefault("transactions", {})[tx_info["idTransaction"]] = tx_info
    save_data(data)

def save_transaction(tx_id, tx_info):
    data = load_data()
    data.setdefault("transactions", {})[tx_id] = tx_info
    save_data(data)

def get_transaction(tx_id):
    data = load_data()
    return data.get("transactions", {}).get(tx_id)

def call_omega_api(endpoint, method="GET", payload=None):
    url = f"{OMEGA_BASE_URL}{endpoint}"
    headers = {
        "x-public-key": OMEGA_PUBLIC_KEY,
        "x-secret-key": OMEGA_SECRET_KEY,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    data_bytes = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data_bytes = json.dumps(payload).encode("utf-8") if isinstance(payload, dict) else str(payload).encode("utf-8")

    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def generate_fallback_cpf():
    import random
    n = [random.randint(0, 9) for _ in range(9)]
    d1 = sum(n[i] * (10 - i) for i in range(9)) % 11
    d1 = 0 if d1 < 2 else 11 - d1
    n.append(d1)
    d2 = sum(n[i] * (11 - i) for i in range(10)) % 11
    d2 = 0 if d2 < 2 else 11 - d2
    n.append(d2)
    return "".join(map(str, n))

def create_pix_charge(name, email, phone="", document="", coupon=""):
    clean_email = email.strip().lower()
    clean_name = name.strip()
    clean_phone = "".join(filter(str.isdigit, phone or ""))
    clean_doc = "".join(filter(str.isdigit, document or ""))

    if not clean_phone or len(clean_phone) < 10:
        clean_phone = "11982854183"

    if not clean_doc or len(clean_doc) != 11:
        clean_doc = generate_fallback_cpf()

    amount = 87.90
    discount = 0
    c = (coupon or "").strip().upper()
    if c in ("CAPIVARA10", "DESCONTO10"):
        amount = 79.11
        discount = 10
    elif c in ("VIP", "VIP20"):
        amount = 69.90
        discount = 20

    identifier = f"capivara_{int(datetime.datetime.now().timestamp()*1000)}_{uuid.uuid4().hex[:6]}"
    due_date = (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    payload = {
        "identifier": identifier,
        "amount": amount,
        "client": {
            "name": clean_name,
            "email": clean_email,
            "phone": clean_phone,
            "document": clean_doc
        },
        "dueDate": due_date,
        "products": [
            {
                "id": "capivara-club-hot-acesso",
                "name": "Acesso Completo - Capivara Club Hot",
                "price": amount,
                "quantity": 1
            }
        ]
    }

    resp = call_omega_api("/gateway/pix/receive", method="POST", payload=payload)
    tx_id = resp.get("transactionId") or resp.get("id")
    pix_code = ""
    if "pix" in resp and isinstance(resp["pix"], dict):
        pix_code = resp["pix"].get("code") or resp["pix"].get("qrCode") or ""
    elif "pixInformation" in resp and isinstance(resp["pixInformation"], dict):
        pix_code = resp["pixInformation"].get("qrCode") or ""

    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(pix_code)}"

    tx_record = {
        "idTransaction": tx_id,
        "identifier": identifier,
        "name": clean_name,
        "email": clean_email,
        "phone": clean_phone,
        "document": clean_doc,
        "amount": amount,
        "pixCode": pix_code,
        "status": "PENDING",
        "createdAt": datetime.datetime.now().isoformat()
    }
    save_transaction(tx_id, tx_record)

    return {
        "ok": True,
        "idTransaction": tx_id,
        "identifier": identifier,
        "paymentCode": pix_code,
        "paymentCodeBase64": qr_url,
        "amount": amount,
        "discountPercent": discount
    }

def check_pix_status(tx_id, email=None):
    if email and is_user_paid(email):
        return {"ok": True, "status": "paid", "paid": True, "email": email}

    tx = get_transaction(tx_id) if tx_id else None
    user_email = (tx.get("email") if tx else None) or email

    if user_email and is_user_paid(user_email):
        return {"ok": True, "status": "paid", "paid": True, "email": user_email}

    if not tx_id:
        return {"ok": True, "status": "pending", "paid": False}

    try:
        omega_tx = call_omega_api(f"/gateway/transactions?id={urllib.parse.quote(tx_id)}")
        status = (omega_tx.get("status") or "").upper()
        if status in ("COMPLETED", "PAID", "CONFIRMED", "APPROVED"):
            unlock_email = user_email or omega_tx.get("client", {}).get("email")
            if unlock_email:
                mark_user_as_paid(unlock_email, {
                    "idTransaction": tx_id,
                    "amount": omega_tx.get("amount", 87.90),
                    "email": unlock_email,
                    "name": (tx.get("name") if tx else None) or omega_tx.get("client", {}).get("name")
                })
            return {
                "ok": True,
                "status": "paid",
                "paid": True,
                "email": unlock_email,
                "redirect": "/paginas/painel.html?paid=true"
            }
        return {
            "ok": True,
            "status": status.lower() or "pending",
            "paid": False
        }
    except Exception as e:
        return {"ok": True, "status": "pending", "paid": False}
