import sqlite3, os, shutil

for browser in [
    r'~\AppData\Local\Google\Chrome\User Data\Default\History',
    r'~\AppData\Local\Microsoft\Edge\User Data\Default\History',
    r'~\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History'
]:
    p = os.path.expanduser(browser)
    if os.path.exists(p):
        print("Checking:", browser)
        try:
            shutil.copyfile(p, 'temp_hist.sqlite')
            conn = sqlite3.connect('temp_hist.sqlite')
            c = conn.cursor()
            c.execute("SELECT url, title FROM urls WHERE url LIKE '%capivara%' ORDER BY last_visit_time DESC LIMIT 30")
            for row in c.fetchall():
                print("  URL:", row[0], "-->", row[1])
            conn.close()
            os.remove('temp_hist.sqlite')
        except Exception as e:
            print("  Error:", e)
