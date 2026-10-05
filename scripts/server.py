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

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

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

        # API: Session (always authenticated and unlocked)
        if path == '/api/session':
            data = {
                "authenticated": True,
                "name": "Diego",
                "email": "diseguro20@gmail.com",
                "isAdmin": False,
                "workflowUnlockAt": "2020-01-01T00:00:00Z",
                "tutorialUnlockAt": "2020-01-01T00:00:00Z"
            }
            body = json.dumps(data).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
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
            body = json.dumps({"referrals": []}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # API: Sync Status
        if path == '/api/sync/status':
            if os.path.exists(STATUS_PATH):
                with open(STATUS_PATH, 'rb') as f:
                    body = f.read()
            else:
                body = json.dumps(update_status()).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        # Video files with byte-range streaming support
        # Normalize tutorial video paths so both tutorial-0X.mp4 and tutorial-X.mp4 map to the downloaded files
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
        clean_path = unquote(parsed.path.lstrip('/'))
        full_path = os.path.join(ROOT_DIR, clean_path)
        if os.path.isfile(full_path) and full_path.endswith(('.mp4', '.webm')):
            self.stream_video(full_path)
            return

        super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path in ('/api/login', '/api/change-password'):
            data = {
                "ok": True,
                "name": "Diego",
                "email": "diseguro20@gmail.com",
                "isAdmin": False,
                "workflowUnlockAt": "2020-01-01T00:00:00Z",
                "tutorialUnlockAt": "2020-01-01T00:00:00Z"
            }
            body = json.dumps(data).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if path == '/api/sync/trigger':
            def run_async():
                try:
                    engine = CapivaraSyncEngine()
                    engine.run_sync()
                except Exception as err:
                    print(f"[Sync] Erro na execução assíncrona: {err}")
            threading.Thread(target=run_async, daemon=True).start()
            body = json.dumps({
                "ok": True,
                "message": "Sincronização em tempo real iniciada com sucesso!"
            }).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
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

def unquote(s):
    return urllib.parse.unquote(s)

if __name__ == '__main__':
    cfg = load_config()
    if cfg.get('auto_sync_enabled', True):
        start_background_sync(interval_seconds=cfg.get('sync_interval_seconds', 900))
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(('0.0.0.0', PORT), CapivaraHandler) as httpd:
        print(f"Capivara local multi-threaded server running on http://localhost:{PORT}", flush=True)
        print("Real-time background sync engine is ACTIVE!", flush=True)
        httpd.serve_forever()
