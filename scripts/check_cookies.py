import sqlite3, os, shutil

cookie_path = os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\User Data\Default\Network\Cookies')
if os.path.exists(cookie_path):
    try:
        shutil.copyfile(cookie_path, 'temp_cookies.sqlite')
        conn = sqlite3.connect('temp_cookies.sqlite')
        c = conn.cursor()
        c.execute("SELECT host_key, name, value, encrypted_value FROM cookies WHERE host_key LIKE '%capivara%'")
        rows = c.fetchall()
        print(f"Found {len(rows)} cookies for capivara:")
        for r in rows:
            print(f"  {r[0]} | {r[1]} | val_len: {len(r[2])} | enc_len: {len(r[3])}")
        conn.close()
        os.remove('temp_cookies.sqlite')
    except Exception as e:
        print("Cookie error:", e)
else:
    print("Cookie path does not exist.")
