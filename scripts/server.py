import http.server
import socketserver
import os
import json
import re
import urllib.parse
import threading

PORT = 5500
ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys_path = os.path.dirname(__file__)
if sys_path not in os.sys.path:
    os.sys.path.insert(0, sys_path)

from sync_engine import CapivaraSyncEngine, update_status, get_current_metrics, start_background_sync, STATUS_PATH, load_config
from omega_gateway import create_pix_charge, check_pix_status, is_user_paid, mark_user_as_paid

class CapivaraHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def send_json(self, data, status_code=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Root and clean routes
        if path == '/login':
            self.send_response(302)
            self.send_header('Location', '/login.html')
            self.end_headers()
            return

        if path == '/cadastro':
            self.send_response(302)
            self.send_header('Location', '/login.html?tab=register')
            self.end_headers()
            return

        if path in ('/membros', '/painel'):
            self.send_response(302)
            self.send_header('Location', '/paginas/painel.html')
            self.end_headers()
            return

        # Checkout & Order Status (Omega Pay)
        if path in ('/api/order-status', '/api/checkout/status'):
            tx_id = query.get('idTransaction', query.get('txId', query.get('id', [None])))[0]
            email = query.get('email', [None])[0]
            res = check_pix_status(tx_id, email)
            self.send_json(res)
            return

        # Check access permission
        if path == '/api/check-access':
            email = query.get('email', [''])[0].strip().lower()
            is_adm = email == 'diseguro20@gmail.com'
            has_access = is_adm or is_user_paid(email)
            self.send_json({
                "ok": True,
                "email": email,
                "paid": has_access,
                "isAdmin": is_adm
            })
            return

        # Check nickname availability
        if path == '/api/check-nickname':
            nick = query.get('nickname', [''])[0].strip()
            self.send_json({"ok": True, "nickname": nick, "available": True})
            return

        # API: Session
        if path == '/api/session':
            email = query.get('email', ['diseguro20@gmail.com'])[0].strip().lower()
            is_adm = email == 'diseguro20@gmail.com'
            has_paid = is_adm or is_user_paid(email)
            data = {
                "authenticated": True,
                "name": "Diego" if is_adm else email.split('@')[0],
                "email": email,
                "isAdmin": is_adm,
                "paid": has_paid,
                "workflowUnlockAt": "2020-01-01T00:00:00Z",
                "tutorialUnlockAt": "2020-01-01T00:00:00Z"
            }
            self.send_json(data)
            return

        # API: Gallery Prompts (194 original prompts)
        if path == '/api/member/prompts':
            p = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts.json')
            if os.path.exists(p):
                with open(p, 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

        # API: +18 Prompts (562 original prompts)
        if path == '/api/member/prompts-18':
            p = os.path.join(ROOT_DIR, 'member-assets', 'member_prompts_18.json')
            if os.path.exists(p):
                with open(p, 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

        # API: Referrals
        if path == '/api/referrals':
            self.send_json({"referrals": []})
            return

        # API: Sync Status
        if path == '/api/sync/status':
            if os.path.exists(STATUS_PATH):
                with open(STATUS_PATH, 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_json(update_status())
            return

        # Video files with byte-range streaming support
        if '/videos-tutoriais/' in path:
            m = re.search(r'tutorial-0?([1-9])\.mp4', path)
            if m:
                num = int(m.group(1))
                padded = f"tutorial-{num:02d}.mp4"
                video_file = os.path.join(ROOT_DIR, 'videos-tutoriais', padded)
                if not os.path.exists(video_file):
                    video_file = os.path.join(ROOT_DIR, 'videos-tutoriais', f"tutorial-{num}.mp4")
                if os.path.exists(video_file):
                    self.stream_video(video_file)
                    return

        # Fallback to standard file serving with byte ranges
        clean_path = urllib.parse.unquote(parsed.path.lstrip('/'))
        full_path = os.path.join(ROOT_DIR, clean_path)
        if os.path.isfile(full_path) and full_path.endswith(('.mp4', '.webm')):
            self.stream_video(full_path)
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        try:
            body_data = json.loads(post_body)
        except Exception:
            body_data = {}

        # Omega Pay PIX creation
        if path in ('/api/access-request', '/api/checkout/pix'):
            name = body_data.get('name', '')
            email = body_data.get('email', '')
            phone = body_data.get('phone', '')
            doc = body_data.get('document') or body_data.get('cpf', '')
            coupon = body_data.get('coupon', '')
            try:
                result = create_pix_charge(name, email, phone, doc, coupon)
                self.send_json(result)
            except Exception as e:
                print(f"[Omega PIX Error] {e}")
                self.send_json({"ok": False, "error": f"Erro ao gerar PIX: {str(e)}"}, 500)
            return

        # Omega Pay Webhook
        if path == '/api/checkout/webhook':
            status = (body_data.get('status') or (body_data.get('data', {}).get('status') if isinstance(body_data.get('data'), dict) else '') or body_data.get('event', '')).upper()
            email = None
            if isinstance(body_data.get('client'), dict):
                email = body_data['client'].get('email')
            elif isinstance(body_data.get('data'), dict):
                if isinstance(body_data['data'].get('client'), dict):
                    email = body_data['data']['client'].get('email')
                else:
                    email = body_data['data'].get('email')
            email = email or body_data.get('email')

            if status in ('COMPLETED', 'PAID', 'CONFIRMED', 'TRANSACTION_PAID', 'APPROVED') and email:
                mark_user_as_paid(email, body_data)
                print(f"[Omega Webhook] Pagamento confirmado e acesso liberado para {email}!")

            self.send_json({"received": True, "status": "ok"})
            return

        # Login endpoint
        if path in ('/api/login', '/api/change-password'):
            email = body_data.get('email', '').strip().lower()
            password = body_data.get('password', '').strip()
            is_adm = email == 'diseguro20@gmail.com'
            has_paid = is_adm or is_user_paid(email)

            if is_adm or has_paid or (email and len(password) >= 4):
                data = {
                    "ok": True,
                    "name": "Diego" if is_adm else email.split('@')[0],
                    "email": email,
                    "isAdmin": is_adm,
                    "paid": has_paid,
                    "workflowUnlockAt": "2020-01-01T00:00:00Z",
                    "tutorialUnlockAt": "2020-01-01T00:00:00Z"
                }
                self.send_json(data)
                return
            else:
                self.send_json({"ok": False, "error": "Credenciais inválidas ou pagamento pendente."}, 401)
                return

        if path == '/api/sync/trigger':
            def run_async():
                try:
                    engine = CapivaraSyncEngine()
                    engine.run_sync()
                except Exception as err:
                    print(f"[Sync] Erro na execução assíncrona: {err}")
            threading.Thread(target=run_async, daemon=True).start()
            self.send_json({
                "ok": True,
                "message": "Sincronização em tempo real iniciada com sucesso!"
            })
            return

        self.send_response(404)
        self.end_headers()

    def stream_video(self, file_path):
        file_size = os.path.getsize(file_path)
        range_header = self.headers.get('Range')

        if not range_header:
            self.send_response(200)
            self.send_header('Content-Type', 'video/mp4')
            self.send_header('Content-Length', str(file_size))
            self.send_header('Accept-Ranges', 'bytes')
            self.end_headers()
            with open(file_path, 'rb') as f:
                while chunk := f.read(1024 * 1024):
                    self.wfile.write(chunk)
            return

        # Handle Range: bytes=start-end
        range_match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if not range_match:
            self.send_error(416, 'Requested Range Not Satisfiable')
            return

        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        end = min(end, file_size - 1)
        length = end - start + 1

        self.send_response(206)
        self.send_header('Content-Type', 'video/mp4')
        self.send_header('Content-Range', f'bytes {start}-{end}/{file_size}')
        self.send_header('Content-Length', str(length))
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()

        try:
            with open(file_path, 'rb') as f:
                f.seek(start)
                bytes_left = length
                while bytes_left > 0:
                    chunk_size = min(1024 * 1024, bytes_left)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    self.wfile.write(data)
                    bytes_left -= len(data)
        except (ConnectionResetError, BrokenPipeError):
            pass

if __name__ == '__main__':
    cfg = load_config()
    if cfg.get('auto_sync_enabled', True):
        start_background_sync(interval_seconds=cfg.get('sync_interval_seconds', 900))
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('0.0.0.0', PORT), CapivaraHandler) as httpd:
        print(f"Capivara local multi-threaded server running on http://localhost:{PORT}", flush=True)
        print("Omega Pay Gateway & Real-time background sync engine are ACTIVE!", flush=True)
        httpd.serve_forever()
