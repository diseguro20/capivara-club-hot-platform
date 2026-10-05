import sqlite3, os, shutil, datetime

p = os.path.expanduser(r'~\AppData\Local\Microsoft\Edge\User Data\Default\History')
shutil.copyfile(p, 'temp_h.sqlite')
conn = sqlite3.connect('temp_h.sqlite')
c = conn.cursor()
c.execute("SELECT url, title, last_visit_time FROM urls WHERE url LIKE '%capivara%' ORDER BY last_visit_time DESC")
for row in c.fetchall():
    ts = row[2]
    dt = datetime.datetime(1601, 1, 1) + datetime.timedelta(microseconds=ts)
    print(f"{row[0]} | {row[1]} | {dt}")
conn.close()
os.remove('temp_h.sqlite')
