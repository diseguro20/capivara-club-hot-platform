import os
import sys
import re
import json
import time
import datetime
import urllib.request
import urllib.parse
import http.cookiejar
import threading

ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, 'sync_config.json')
STATUS_PATH = os.path.join(ROOT_DIR, 'member-assets', 'sync_status.json')
WORKFLOWS_DIR = os.path.join(ROOT_DIR, 'workflows')
VIDEOS_DIR = os.path.join(ROOT_DIR, 'videos-tutoriais')
MEMBER_ASSETS_DIR = os.path.join(ROOT_DIR, 'member-assets')

sync_lock = threading.Lock()

def load_config():
    default_config = {
        "live_url": "https://capivaraclubhot.com",
        "email": "diseguro20@gmail.com",
        "password": "diego2001",
        "sync_interval_seconds": 900,
        "auto_sync_enabled": True,
        "check_new_videos": True,
        "check_new_workflows": True,
        "check_new_prompts": True,
        "check_new_prompts_18": True
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
                default_config.update(cfg)
        except Exception as e:
            print(f"[Sync] Error reading config: {e}")
    return default_config

def get_current_metrics():
    # Videos
    video_count = 0
    if os.path.exists(VIDEOS_DIR):
        video_count = len([f for f in os.listdir(VIDEOS_DIR) if f.startswith('tutorial-') and f.endswith('.mp4') and '0' in f])
        if video_count == 0:
            video_count = len([f for f in os.listdir(VIDEOS_DIR) if f.endswith('.mp4')])

    # Workflows
    wf_count = 0
    if os.path.exists(WORKFLOWS_DIR):
        wf_count = len([f for f in os.listdir(WORKFLOWS_DIR) if f.endswith('.json')])

    # Prompts
    p_count = 0
    p_path = os.path.join(MEMBER_ASSETS_DIR, 'member_prompts.json')
    if os.path.exists(p_path):
        try:
            with open(p_path, 'r', encoding='utf-8') as f:
                p_count = len(json.load(f).get('prompts', []))
        except Exception:
            pass

    # Prompts 18
    p18_count = 0
    p18_path = os.path.join(MEMBER_ASSETS_DIR, 'member_prompts_18.json')
    if os.path.exists(p18_path):
        try:
            with open(p18_path, 'r', encoding='utf-8') as f:
                d = json.load(f)
                p18_count = len(d) if isinstance(d, list) else len(d.get('prompts', []))
        except Exception:
            pass

    return {
        "tutorial_videos": video_count,
        "workflows": wf_count,
        "prompts": p_count,
        "prompts_18": p18_count
    }

def update_status(is_syncing=False, last_result="idle", message="Sistema pronto", changes=None):
    metrics = get_current_metrics()
    status_data = {
        "last_sync": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "is_syncing": is_syncing,
        "last_result": last_result,
        "message": message,
        "metrics": metrics,
        "history": []
    }
    if os.path.exists(STATUS_PATH):
        try:
            with open(STATUS_PATH, 'r', encoding='utf-8') as f:
                prev = json.load(f)
                status_data["history"] = prev.get("history", [])
        except Exception:
            pass

    if changes:
        entry = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "changes": changes
        }
        status_data["history"].insert(0, entry)
        status_data["history"] = status_data["history"][:20]

    os.makedirs(os.path.dirname(STATUS_PATH), exist_ok=True)
    with open(STATUS_PATH, 'w', encoding='utf-8') as f:
        json.dump(status_data, f, ensure_ascii=False, indent=2)
    return status_data

class CapivaraSyncEngine:
    def __init__(self, config=None):
        self.config = config or load_config()
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self.csrf_token = None
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

    def login(self):
        live_url = self.config.get('live_url', 'https://capivaraclubhot.com')
        membros_url = f"{live_url}/membros"
        login_url = f"{live_url}/api/login"

        req = urllib.request.Request(membros_url, headers={
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
        with self.opener.open(req, timeout=15) as res:
            html = res.read().decode('utf-8', errors='ignore')
            m = re.search(r'name="csrf-token"\s+content="([^"]+)"', html)
            self.csrf_token = m.group(1) if m else ''

        login_data = json.dumps({
            "email": self.config.get('email', 'diseguro20@gmail.com'),
            "password": self.config.get('password', 'diego2001')
        }).encode('utf-8')

        post_headers = {
            'User-Agent': self.user_agent,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-CSRF-TOKEN': self.csrf_token,
            'Referer': membros_url,
            'Origin': live_url
        }

        login_req = urllib.request.Request(login_url, data=login_data, headers=post_headers, method='POST')
        with self.opener.open(login_req, timeout=15) as res:
            resp = json.loads(res.read().decode('utf-8'))
            print(f"[Sync] Autenticado com sucesso no {live_url} como {resp.get('email')}")
            return resp

    def run_sync(self):
        if not sync_lock.acquire(blocking=False):
            print("[Sync] Sincronização já está em andamento. Aguardando...")
            return {"status": "busy", "message": "Sincronização já em andamento"}

        try:
            update_status(is_syncing=True, last_result="running", message="Iniciando sincronização com a plataforma original...")
            print("\n[Sync] ==================================================")
            print(f"[Sync] Iniciando ciclo de sincronização: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # 1. Login
            self.login()

            changes = []
            needs_build = False
            live_url = self.config.get('live_url', 'https://capivaraclubhot.com')

            # 2. Sync Prompts Padrão
            if self.config.get('check_new_prompts', True):
                try:
                    p_req = urllib.request.Request(f"{live_url}/api/member/prompts", headers={
                        'User-Agent': self.user_agent,
                        'X-CSRF-TOKEN': self.csrf_token or ''
                    })
                    with self.opener.open(p_req, timeout=20) as r:
                        live_p_data = json.loads(r.read().decode('utf-8'))
                        live_prompts = live_p_data.get('prompts', [])

                    local_p_path = os.path.join(MEMBER_ASSETS_DIR, 'member_prompts.json')
                    local_count = 0
                    if os.path.exists(local_p_path):
                        with open(local_p_path, 'r', encoding='utf-8') as f:
                            local_count = len(json.load(f).get('prompts', []))

                    if len(live_prompts) > local_count:
                        diff = len(live_prompts) - local_count
                        with open(local_p_path, 'w', encoding='utf-8') as f:
                            json.dump(live_p_data, f, ensure_ascii=False, indent=2)
                        # Re-generate JS
                        js_p_path = os.path.join(MEMBER_ASSETS_DIR, 'member_prompts.js')
                        with open(js_p_path, 'w', encoding='utf-8') as f:
                            f.write('window.DMCN_PROMPTS = ' + json.dumps(live_prompts, ensure_ascii=False) + ';\n')
                        changes.append(f"{diff} novos prompts adicionados à Galeria padrão (Total: {len(live_prompts)})")
                        needs_build = True
                        print(f"[Sync] + {diff} novos prompts padrão encontrados!")
                except Exception as e:
                    print(f"[Sync] Erro ao sincronizar prompts padrão: {e}")

            # 3. Sync Prompts +18
            if self.config.get('check_new_prompts_18', True):
                try:
                    p18_req = urllib.request.Request(f"{live_url}/api/member/prompts-18", headers={
                        'User-Agent': self.user_agent,
                        'X-CSRF-TOKEN': self.csrf_token or ''
                    })
                    with self.opener.open(p18_req, timeout=20) as r:
                        raw_18 = json.loads(r.read().decode('utf-8'))
                        live_18 = raw_18 if isinstance(raw_18, list) else raw_18.get('prompts', [])

                    local_18_path = os.path.join(MEMBER_ASSETS_DIR, 'member_prompts_18.json')
                    local_18_count = 0
                    if os.path.exists(local_18_path):
                        with open(local_18_path, 'r', encoding='utf-8') as f:
                            d = json.load(f)
                            local_18_count = len(d) if isinstance(d, list) else len(d.get('prompts', []))

                    if len(live_18) > local_18_count:
                        diff = len(live_18) - local_18_count
                        # Check new images for new prompts
                        prompts_18_img_dir = os.path.join(MEMBER_ASSETS_DIR, 'prompts-18')
                        os.makedirs(prompts_18_img_dir, exist_ok=True)
                        for item in live_18[local_18_count:]:
                            img_path = item.get('imagem') or item.get('thumb')
                            if img_path and not os.path.exists(os.path.join(ROOT_DIR, img_path.lstrip('/'))):
                                try:
                                    img_url = f"{live_url}/{img_path.lstrip('/')}"
                                    local_dest = os.path.join(ROOT_DIR, img_path.lstrip('/'))
                                    os.makedirs(os.path.dirname(local_dest), exist_ok=True)
                                    with self.opener.open(img_url, timeout=10) as ir, open(local_dest, 'wb') as of:
                                        of.write(ir.read())
                                except Exception as err:
                                    print(f"[Sync] Não foi possível baixar imagem {img_path}: {err}")

                        with open(local_18_path, 'w', encoding='utf-8') as f:
                            json.dump(live_18, f, ensure_ascii=False, indent=2)
                        js_18_path = os.path.join(MEMBER_ASSETS_DIR, 'member_prompts_18.js')
                        with open(js_18_path, 'w', encoding='utf-8') as f:
                            f.write('window.DMCN_PROMPTS_18 = ' + json.dumps(live_18, ensure_ascii=False) + ';\n')
                        changes.append(f"{diff} novos prompts adicionados à Galeria +18 (Total: {len(live_18)})")
                        needs_build = True
                        print(f"[Sync] + {diff} novos prompts +18 encontrados!")
                except Exception as e:
                    print(f"[Sync] Erro ao sincronizar prompts +18: {e}")

            # 4. Fetch live /membros HTML
            membros_req = urllib.request.Request(f"{live_url}/membros", headers={
                'User-Agent': self.user_agent,
                'Referer': f"{live_url}/membros"
            })
            with self.opener.open(membros_req, timeout=20) as r:
                live_html = r.read().decode('utf-8', errors='ignore')

            # 5. Sync Workflows
            if self.config.get('check_new_workflows', True):
                try:
                    os.makedirs(WORKFLOWS_DIR, exist_ok=True)
                    wf_matches = re.findall(r'href=["\'](workflows/[^"\']+\.json)["\']', live_html)
                    new_wfs = 0
                    for wf_href in set(wf_matches):
                        unquoted = urllib.parse.unquote(wf_href)
                        filename = os.path.basename(unquoted)
                        dest_file = os.path.join(WORKFLOWS_DIR, filename)
                        if not os.path.exists(dest_file):
                            wf_url = f"{live_url}/{urllib.parse.quote(wf_href, safe='/:')}"
                            try:
                                with self.opener.open(wf_url, timeout=15) as wr, open(dest_file, 'wb') as of:
                                    of.write(wr.read())
                                new_wfs += 1
                                changes.append(f"Novo workflow baixado: {filename}")
                                print(f"[Sync] + Novo workflow baixado: {filename}")
                            except Exception as err:
                                print(f"[Sync] Erro ao baixar workflow {wf_url}: {err}")
                    if new_wfs > 0:
                        needs_build = True
                except Exception as e:
                    print(f"[Sync] Erro ao sincronizar workflows: {e}")

            # 6. Sync Tutorial Videos
            if self.config.get('check_new_videos', True):
                try:
                    os.makedirs(VIDEOS_DIR, exist_ok=True)
                    existing_videos = [f for f in os.listdir(VIDEOS_DIR) if f.endswith('.mp4')]
                    max_num = 9
                    for f in existing_videos:
                        m = re.search(r'tutorial-0?([0-9]+)\.mp4', f)
                        if m:
                            max_num = max(max_num, int(m.group(1)))

                    # Test next 5 potential tutorial numbers (e.g. 10..14)
                    new_vids = 0
                    for num in range(1, max_num + 5):
                        padded = f"tutorial-{num:02d}.mp4"
                        unpadded = f"tutorial-{num}.mp4"
                        target_file = os.path.join(VIDEOS_DIR, padded)
                        if not os.path.exists(target_file) and not os.path.exists(os.path.join(VIDEOS_DIR, unpadded)):
                            # Probe remote URL
                            for probe_name in (padded, unpadded):
                                v_url = f"{live_url}/videos-tutoriais/{probe_name}"
                                try:
                                    req_head = urllib.request.Request(v_url, headers={
                                        'User-Agent': self.user_agent,
                                        'Range': 'bytes=0-1024'
                                    })
                                    with self.opener.open(req_head, timeout=10) as vr:
                                        if vr.status in (200, 206):
                                            print(f"[Sync] Novo vídeo tutorial detectado: {probe_name}! Baixando...")
                                            with self.opener.open(urllib.request.Request(v_url, headers={'User-Agent': self.user_agent}), timeout=600) as full_vr, open(target_file, 'wb') as of:
                                                while chunk := full_vr.read(1024 * 1024):
                                                    of.write(chunk)
                                            new_vids += 1
                                            changes.append(f"Novo vídeo tutorial baixado: {padded}")
                                            break
                                except Exception:
                                    pass
                    if new_vids > 0:
                        needs_build = True
                except Exception as e:
                    print(f"[Sync] Erro ao sincronizar tutoriais: {e}")

            # 7. Update membros_autenticado.html if live HTML changed
            auth_html_path = os.path.join(ROOT_DIR, 'scripts', 'membros_autenticado.html')
            if os.path.exists(auth_html_path):
                with open(auth_html_path, 'r', encoding='utf-8') as f:
                    old_html = f.read()
                # Compare structural length or changes
                if abs(len(live_html) - len(old_html)) > 50 or needs_build:
                    with open(auth_html_path, 'w', encoding='utf-8') as f:
                        f.write(live_html)
                    needs_build = True

            # 8. Rebuild if changes occurred
            if needs_build:
                print("[Sync] Atualizações detectadas! Reconstruindo aplicação offline...")
                import subprocess
                subprocess.run([sys.executable, os.path.join(ROOT_DIR, 'scripts', 'build_offline_platform.py')], check=True)
                msg = f"Sincronização concluída com sucesso! {len(changes)} novas atualizações incorporadas."
            else:
                msg = "Sincronização concluída. Nenhum novo conteúdo adicionado na plataforma original (clone 100% atualizado)."

            result_status = update_status(is_syncing=False, last_result="success", message=msg, changes=changes if changes else None)
            print(f"[Sync] {msg}")
            print("[Sync] ==================================================\n")
            return result_status

        except Exception as e:
            err_msg = f"Erro na sincronização: {str(e)}"
            print(f"[Sync] {err_msg}")
            result_status = update_status(is_syncing=False, last_result="error", message=err_msg)
            return result_status
        finally:
            sync_lock.release()

def start_background_sync(interval_seconds=900):
    def loop():
        print(f"[Sync Daemon] Monitor de sincronização em tempo real iniciado (intervalo: {interval_seconds}s)")
        time.sleep(10) # Initial wait after server start
        while True:
            try:
                cfg = load_config()
                if cfg.get('auto_sync_enabled', True):
                    engine = CapivaraSyncEngine(cfg)
                    engine.run_sync()
                interval = cfg.get('sync_interval_seconds', interval_seconds)
                time.sleep(interval)
            except Exception as e:
                print(f"[Sync Daemon] Exceção no loop: {e}")
                time.sleep(60)

    t = threading.Thread(target=loop, daemon=True, name="SyncDaemonThread")
    t.start()
    return t

if __name__ == '__main__':
    engine = CapivaraSyncEngine()
    res = engine.run_sync()
    print("Resultado:", json.dumps(res, indent=2, ensure_ascii=False))
